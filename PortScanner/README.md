# 🚀 Python TCP Port Scanner

A lightweight **TCP Port Scanner** built with Python using the built-in `socket` module. This project scans a target host for open TCP ports, identifies common services running on those ports, and provides a clean scan summary.

> **Educational Purpose:** This project was built to learn Python socket programming, TCP networking, DNS resolution, and command-line argument parsing.

---

## 📖 Overview

A port scanner attempts to connect to a range of TCP ports on a target host. If a connection is successful, the port is considered **open**, indicating that a service is listening on that port.

This project demonstrates the fundamentals of how TCP-based port scanners work using Python's standard library.

---

## ✨ Features

* 🔍 Scan any hostname or IPv4 address
* 🌐 Automatic hostname to IP resolution
* 📡 Detect open TCP ports
* 🏷️ Identify common services (HTTP, HTTPS, SSH, etc.)
* ⚙️ Custom port range support
* 🖥️ Command-line interface using `argparse`
* ⏱️ Scan execution time measurement
* 📊 Summary of all discovered open ports
* 🐍 Built entirely with Python standard library (no third-party packages)

---

## 🛠️ Technologies Used

* Python 3
* socket
* argparse
* time

---

## 📂 Project Structure

```text
PortScanner/
│
├── scanner.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/harsh-chauhan-dev/python-network-lab.git
```

Move into the project directory:

```bash
cd PortScanner
```

(Optional) Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 🚀 Usage

Scan the default port range (1–1024):

```bash
python scanner.py google.com
```

Scan a custom range:

```bash
python scanner.py google.com -p 1-5000
```

Scan a deployed application:

```bash
python scanner.py devhub-one-beta.vercel.app
```

Scan a local machine:

```bash
python scanner.py 127.0.0.1
```

---

## 💻 Example Output

```text
==================================================
Target : google.com
IP      : 142.250.xxx.xxx
Ports   : 1-1024
==================================================

Port 80    | http       | OPEN
Port 443   | https      | OPEN

==================================================
Open Ports
--------------------------------------------------
80    | http
443   | https
--------------------------------------------------
Total Open Ports : 2
Scan Time        : 1.21 seconds
==================================================
```

---

## 🧠 How It Works

1. Accepts a hostname or IP address from the command line.
2. Resolves the hostname to an IP address.
3. Iterates through the specified port range.
4. Creates a TCP socket for each port.
5. Attempts to establish a TCP connection using `connect_ex()`.
6. If the connection succeeds, the port is marked as **OPEN**.
7. Retrieves the standard service name using `socket.getservbyport()`.
8. Displays the results and scan summary.

---

## 📚 Concepts Learned

This project helped reinforce the following networking and Python concepts:

### Networking

* TCP Protocol
* TCP Ports
* Client-Server Communication
* DNS Resolution
* Socket Programming
* Network Services

### Python

* Functions
* Exception Handling
* Command-Line Arguments (`argparse`)
* Lists
* Loops
* Time Measurement
* Resource Management


---

## ⚠️ Disclaimer

This tool is intended for **educational purposes** and for scanning systems that you own or have explicit permission to test.

Always ensure you have authorization before scanning any network or system.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Harsh Chauhan**

* BCA Student
* Backend Developer
* Python Networking Learner
* Aspiring Cybersecurity Engineer

If you found this project useful, consider giving it a ⭐ on GitHub.
