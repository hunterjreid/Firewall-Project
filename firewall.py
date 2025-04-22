import sys
import json
import logging
import time
from datetime import datetime
from scapy.all import *
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename='firewall.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Firewall:
    def __init__(self, config_file='firewall_config.json'):
        self.allowed_ips = set()
        self.blocked_ips = set()
        self.allowed_ports = set()
        self.blocked_ports = set()
        self.protocol_rules = {}
        self.rate_limits = defaultdict(lambda: {'count': 0, 'timestamp': time.time()})
        self.connection_states = {}
        self.load_config(config_file)

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.allowed_ips = set(config.get('allowed_ips', []))
                self.blocked_ips = set(config.get('blocked_ips', []))
                self.allowed_ports = set(config.get('allowed_ports', []))
                self.blocked_ports = set(config.get('blocked_ports', []))
                self.protocol_rules = config.get('protocol_rules', {})
        except FileNotFoundError:
            logging.warning(f"Configuration file {config_file} not found. Using default settings.")

    def check_rate_limit(self, ip):
        current_time = time.time()
        if current_time - self.rate_limits[ip]['timestamp'] > 60:  # Reset after 1 minute
            self.rate_limits[ip] = {'count': 0, 'timestamp': current_time}
        
        self.rate_limits[ip]['count'] += 1
        return self.rate_limits[ip]['count'] <= 100  # Max 100 packets per minute

    def check_connection_state(self, packet):
        if TCP in packet:
            key = (packet[IP].src, packet[IP].dst, packet[TCP].sport, packet[TCP].dport)
            if packet[TCP].flags & 0x02:  # SYN
                self.connection_states[key] = 'SYN_SENT'
            elif packet[TCP].flags & 0x10:  # ACK
                if key in self.connection_states:
                    self.connection_states[key] = 'ESTABLISHED'
            elif packet[TCP].flags & 0x04:  # RST
                self.connection_states.pop(key, None)
            elif packet[TCP].flags & 0x01:  # FIN
                self.connection_states.pop(key, None)

    def packet_filter(self, packet):
        if IP not in packet:
            return False

        source_ip = packet[IP].src
        dest_ip = packet[IP].dst

        # Check if IP is blocked
        if source_ip in self.blocked_ips:
            logging.warning(f"Blocked packet from blocked IP: {source_ip}")
            return False

        # Check if IP is allowed (if whitelist is enabled)
        if self.allowed_ips and source_ip not in self.allowed_ips:
            logging.warning(f"Blocked packet from non-allowed IP: {source_ip}")
            return False

        # Check rate limiting
        if not self.check_rate_limit(source_ip):
            logging.warning(f"Rate limit exceeded for IP: {source_ip}")
            return False

        # Check port rules
        if TCP in packet:
            if packet[TCP].dport in self.blocked_ports:
                logging.warning(f"Blocked packet to blocked port: {packet[TCP].dport}")
                return False
            if self.allowed_ports and packet[TCP].dport not in self.allowed_ports:
                logging.warning(f"Blocked packet to non-allowed port: {packet[TCP].dport}")
                return False

        # Check protocol rules
        if TCP in packet:
            protocol = 'TCP'
        elif UDP in packet:
            protocol = 'UDP'
        else:
            protocol = 'OTHER'

        if protocol in self.protocol_rules and not self.protocol_rules[protocol]:
            logging.warning(f"Blocked {protocol} packet")
            return False

        # Update connection state
        self.check_connection_state(packet)

        logging.info(f"Allowed packet from {source_ip} to {dest_ip}")
        return True

    def start(self):
        logging.info("Firewall started")
        try:
            sniff(filter="ip", prn=lambda p: send(p) if self.packet_filter(p) else None)
        except KeyboardInterrupt:
            logging.info("Firewall stopped by user")
        except Exception as e:
            logging.error(f"Error in firewall: {str(e)}")

if __name__ == "__main__":
    firewall = Firewall()
    firewall.start()