# 🚀 LAN Scanner

A simple **ARP-based LAN Scanner** built with **Python** and **Scapy**. It discovers active devices connected to a local network by sending ARP requests and displaying their **IP** and **MAC addresses**.

---

## 📖 Overview

LAN Scanner performs **Layer 2 network discovery** using the **Address Resolution Protocol (ARP)**.

Instead of using ICMP (Ping), the scanner broadcasts ARP requests across the local network. Every active device responds with its MAC address, allowing the scanner to identify devices connected to the LAN.

---

## ✨ Features

* 🔍 Discover active devices on a Local Area Network (LAN)
* 🌐 Scan any IPv4 CIDR network (e.g. `192.168.1.0/24`)
* 📡 Uses ARP Broadcast for reliable host discovery
* 🖥 Displays:

  * IP Address
  * MAC Address
* ✅ Validates network input before scanning
* 🐍 Built with Python and Scapy

---

## 🛠 Tech Stack

* Python 3.x
* Scapy
* ipaddress (Standard Library)

---

## 📂 Project Structure

```text
LAN-Scanner/
│
├── network_scanner.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/LAN-Scanner.git
```

```bash
cd LAN-Scanner
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install scapy
```

or

```bash
pip install -r requirements.txt
```

---

## ⚠ Windows Requirement

Scapy requires **Npcap** for sending Layer 2 packets on Windows.

Download:

https://npcap.com/

During installation enable:

* ✅ Install Npcap in WinPcap API-compatible Mode

Run the terminal as **Administrator** if required.

---

## ▶ Usage

Run:

```bash
python network_scanner.py
```

Example:

```text
Enter the network range (e.g., 192.168.1.0/24):
192.168.1.0/24
```

---

## Example Output

```text
---------------------------------------------
IP Address         MAC Address
---------------------------------------------
192.168.1.1        54:AF:97:AA:BB:CC
192.168.1.5        C0:35:32:18:8D:15
192.168.1.10       44:11:22:33:44:55
```

---

## 🧠 How It Works

The scanner follows these steps:

```text
User enters network range
        │
        ▼
Validate CIDR
        │
        ▼
Create ARP Request
        │
        ▼
Create Ethernet Broadcast Frame
        │
        ▼
Combine Ethernet + ARP Packet
        │
        ▼
Broadcast Packet
        │
        ▼
Receive ARP Replies
        │
        ▼
Extract IP Address
        │
        ▼
Extract MAC Address
        │
        ▼
Display Results
```

---

## 📦 Technologies Used

### Scapy

Used to:

* Create Ethernet Frames
* Create ARP Packets
* Broadcast packets
* Receive responses

### ARP (Address Resolution Protocol)

Maps an IPv4 address to its physical MAC address on a local network.

### Ethernet Broadcast

Packets are sent to:

```text
ff:ff:ff:ff:ff:ff
```

Every device on the LAN receives the request.

---

## 📚 Networking Concepts Learned

This project demonstrates:

* IPv4 Addressing
* CIDR Notation
* Ethernet Frames
* MAC Addresses
* ARP (Address Resolution Protocol)
* Layer 2 Communication
* Broadcast Communication
* Packet Crafting
* Network Discovery

---

## 💡 Use Cases

* Discover devices connected to your Wi-Fi or LAN
* Home network monitoring
* Network troubleshooting
* Device inventory
* Cybersecurity reconnaissance
* Learn packet crafting with Scapy


---

## 📸 Demo

```text
█████  ███  █   █
█     █   █ ██  █
█     █████ █ █ █
█     █   █ █  ██
█████ █   █ █   █

LAN Scanner

Enter the network range:
192.168.1.0/24

---------------------------------------------
IP Address         MAC Address
---------------------------------------------
192.168.1.1        54:AF:97:AA:BB:CC
192.168.1.5        C0:35:32:18:8D:15
192.168.1.20       A4:BB:6D:98:21:77
```

---

## 🎯 Learning Objectives

By building this project, you gain practical experience with:

* Python Networking
* Scapy
* Packet Creation
* Layer 2 Networking
* ARP Protocol
* Ethernet Communication
* Network Reconnaissance
* Cybersecurity Fundamentals

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Harsh Chauhan**

BCA Student | Backend Developer | Python Networking & Cybersecurity Enthusiast

If you found this project helpful, consider giving it a ⭐ on GitHub!
