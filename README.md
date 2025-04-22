# 🔒 Firewall Project

Beginner friendly network firewall that helps protect your computer or home network

## 🛠️ Getting Started

### Simple Installation Steps

1. First, let's install the required software:
```bash
pip install scapy
```

2. Download the firewall files:
```bash
git clone https://github.com/hunterjreid/Firewall-Project.git
cd Firewall-Project
```

## 🍓 Raspberry Pi Setup (Recommended for Home Networks)

This firewall works great on a Raspberry Pi! Here's how to set it up:

1. **Update Your Raspberry Pi**:
```bash
sudo apt update
sudo apt upgrade
```

2. **Install Required Software**:
```bash
sudo apt install python3 python3-pip
pip3 install scapy
```

3. **Set Up Automatic Start**:
Create a new file called `firewall.service`:
```bash
sudo nano /etc/systemd/system/firewall.service
```

Add these settings:
```ini
[Unit]
Description=Network Firewall Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /path/to/your/firewall.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start the Firewall**:
```bash
sudo systemctl enable firewall
sudo systemctl start firewall
```

5. **Check if Everything is Working**:
```bash
sudo systemctl status firewall
```

## ⚙️ Setting Up Your Rules

The firewall uses a simple configuration file. Here's an example of how to set it up:

```json
{
    "allowed_ips": ["192.168.1.1", "192.168.1.2"],
    "blocked_ips": ["10.0.0.1", "10.0.0.2"],
    "allowed_ports": [80, 443, 22, 53],
    "blocked_ports": [23, 445, 139],
    "protocol_rules": {
        "TCP": true,
        "UDP": true,
        "ICMP": true
    }
}
```



### Understanding the Settings

- **allowed_ips**: Computers you trust (like your family's devices)
- **blocked_ips**: Computers you want to keep out
- **allowed_ports**: Services you want to allow (like web browsing or email)
- **blocked_ports**: Services you want to block
- **protocol_rules**: Types of internet traffic to allow

## 🚀 Starting the Firewall

To start protecting your network, simply run:
```bash
sudo python firewall.py
```



## 📊 Checking Activity

The firewall keeps a detailed log of all activity. You can view it with:
```bash
tail -f firewall.log
```

You'll see entries like this:
```
2023-04-22 10:15:30 - INFO - Firewall started
2023-04-22 10:15:31 - INFO - Allowed connection from 192.168.1.1
2023-04-22 10:15:32 - WARNING - Blocked connection from 10.0.0.1
```

## 📜 License Information

This project is available under the MIT License, which means you're free to use it for any purpose, as long as you give credit.

