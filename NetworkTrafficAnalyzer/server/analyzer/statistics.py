from collections import Counter
from scapy.all import IP, IPv6, TCP, UDP, ICMP


class TrafficStatistics:
    """Class for aggregating and displaying network traffic statistics."""

    def __init__(self):
        self.protocol = Counter()
        self.source_ip = Counter()
        self.destination_ips = Counter()
        self.source_ports = Counter()
        self.destination_ports = Counter()
        self.tcp_flags = Counter()
        self.connections = {}
        self.packet_count = 0
        self.total_bytes = 0

    def process_packet(self, packet):
        """Analyze a packet and update internal counters."""
        self.packet_count += 1
        self.total_bytes += len(packet)

        # IP Address Statistics
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            self.source_ip[src_ip] += 1
            self.destination_ips[dst_ip] += 1
        elif IPv6 in packet:
            src_ip = packet[IPv6].src
            dst_ip = packet[IPv6].dst
            self.source_ip[src_ip] += 1
            self.destination_ips[dst_ip] += 1
        else:
            src_ip = None
            dst_ip = None

        # Protocol & Transport Layer Statistics
        if TCP in packet:
            self.protocol["TCP"] += 1
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            self.source_ports[src_port] += 1
            self.destination_ports[dst_port] += 1

            # Connection tracking
            if src_ip is not None and dst_ip is not None:
                endpoint1 = (src_ip, src_port)
                endpoint2 = (dst_ip, dst_port)
                connection = tuple(sorted([endpoint1, endpoint2]))

                if connection not in self.connections:
                    self.connections[connection] = {"packets": 0, "bytes": 0}

                self.connections[connection]["packets"] += 1
                self.connections[connection]["bytes"] += len(packet)

            # TCP Flags
            flags = packet[TCP].flags
            if "S" in flags:
                self.tcp_flags["SYN"] += 1
            if "A" in flags:
                self.tcp_flags["ACK"] += 1
            if "F" in flags:
                self.tcp_flags["FIN"] += 1
            if "R" in flags:
                self.tcp_flags["RST"] += 1
            if "P" in flags:
                self.tcp_flags["PSH"] += 1

        elif UDP in packet:
            self.protocol["UDP"] += 1
            self.source_ports[packet[UDP].sport] += 1
            self.destination_ports[packet[UDP].dport] += 1

        elif ICMP in packet:
            self.protocol["ICMP"] += 1

        else:
            self.protocol["OTHER"] += 1

    def get_summary(self):
        """Return statistics as a dictionary for programmatic consumption."""
        sorted_conns = sorted(
            self.connections.items(),
            key=lambda item: item[1]["packets"],
            reverse=True
        )

        formatted_conns = []
        for connection, stats in sorted_conns[:10]:
            endpoint1, endpoint2 = connection
            formatted_conns.append({
                "endpoint1": f"{endpoint1[0]}:{endpoint1[1]}",
                "endpoint2": f"{endpoint2[0]}:{endpoint2[1]}",
                "packets": stats["packets"],
                "bytes": stats["bytes"]
            })

        return {
            "packet_count": self.packet_count,
            "total_bytes": self.total_bytes,
            "total_kb": round(self.total_bytes / 1024, 2),
            "protocols": dict(self.protocol),
            "top_source_ips": dict(self.source_ip.most_common(10)),
            "top_destination_ips": dict(self.destination_ips.most_common(10)),
            "top_source_ports": dict(self.source_ports.most_common(10)),
            "top_destination_ports": dict(self.destination_ports.most_common(10)),
            "tcp_flags": dict(self.tcp_flags.most_common()),
            "top_connections": formatted_conns
        }

    def print_report(self):
        """Print formatted traffic report to standard output."""
        print("\n=== Protocol Statistics ===")
        for proto, count in self.protocol.items():
            print(f"{proto}: {count}")

        print("\n=== Top Source IPs ===")
        for ip, count in self.source_ip.most_common(10):
            print(f"{ip}: {count}")

        print("\n=== Top Destination IPs ===")
        for ip, count in self.destination_ips.most_common(10):
            print(f"{ip}: {count}")

        print("\n=== Top Source Ports ===")
        for port, count in self.source_ports.most_common(10):
            print(f"{port}: {count}")

        print("\n=== Top Destination Ports ===")
        for port, count in self.destination_ports.most_common(10):
            print(f"{port}: {count}")

        print("\n=== Traffic Statistics ===")
        print(f"Packets Analyzed: {self.packet_count}")
        print(f"Total KB: {self.total_bytes / 1024:.2f}")

        print("\n=== TCP Flags ===")
        for flag, count in self.tcp_flags.most_common():
            print(f"{flag}: {count}")

        print("\n=== TCP Connections ===")
        sorted_conns = sorted(
            self.connections.items(),
            key=lambda item: item[1]["packets"],
            reverse=True
        )
        for connection, stats in sorted_conns[:10]:
            endpoint1, endpoint2 = connection
            print(
                f"{endpoint1[0]}:{endpoint1[1]} <-> "
                f"{endpoint2[0]}:{endpoint2[1]} | "
                f"Packets: {stats['packets']} | Bytes: {stats['bytes']}"
            )
