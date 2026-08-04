import socket
import argparse
import time


open_ports = []


def scan_port(host: str, port: int):
    """Scan a single TCP port."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.05)

    try:
        result = sock.connect_ex((host, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"

            open_ports.append((port, service))
            print(f"Port {port:<5} | {service:<10} | OPEN")

    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP Port Scanner"
    )

    parser.add_argument(
        "host",
        help="Target hostname or IP address"
    )

    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help="Port range (Example: 1-1024)"
    )

    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print("[-] Unable to resolve hostname.")
        return

    try:
        port_min, port_max = map(int, args.ports.split("-"))
    except ValueError:
        print("[-] Invalid port range.")
        return

    print("=" * 50)
    print(f"Target : {args.host}")
    print(f"IP      : {ip}")
    print(f"Ports   : {port_min}-{port_max}")
    print("=" * 50)

    start = time.time()

    for port in range(port_min, port_max + 1):
        scan_port(args.host, port)

    end = time.time()

    print("\n" + "=" * 50)
    print("Open Ports")
    print("-" * 50)

    for port, service in open_ports:
        print(f"{port:<5} | {service}")

    print("-" * 50)
    print(f"Total Open Ports : {len(open_ports)}")
    print(f"Scan Time        : {end - start:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()