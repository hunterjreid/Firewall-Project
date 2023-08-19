import sys
from scapy.all import *

# Define allowed IP addresses
allowed_ips = ['192.168.1.2', '192.168.1.3']

# Define a function to filter incoming packets
def packet_filter(packet):
    if IP in packet:
        source_ip = packet[IP].src
        if source_ip not in allowed_ips:
            print(f"Blocking packet from {source_ip}")
            return
    send(packet)

# Set up a sniffing filter
sniff(filter="ip", prn=packet_filter)