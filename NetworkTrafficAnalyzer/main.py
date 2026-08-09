from scapy.all import (
    sniff,
    IP,
    IPv6,
    TCP,
    UDP,
    ICMP,
    wrpcap
)

from collections import Counter
import argparse


# ==========================================
# Statistics
# ==========================================

protocol = Counter()

source_ip = Counter()
destination_ips = Counter()

source_ports = Counter()
destination_ports = Counter()

tcp_flags = Counter()

connections = {}

captured_packets = []

total_bytes = 0
packet_count = 0


# ==========================================
# CLI Arguments
# ==========================================

parser = argparse.ArgumentParser(
    description="Python Network Traffic Analyzer"
)

parser.add_argument(
    "--protocol",
    choices=["tcp", "udp", "icmp"],
    help="Filter traffic by protocol"
)

parser.add_argument(
    "--port",
    type=int,
    help="Filter traffic by port"
)

parser.add_argument(
    "--host",
    help="Filter traffic by IP address"
)

args = parser.parse_args()


# ==========================================
# Packet Filter
# ==========================================

def packet_matches_filter(packet):

    # Protocol filter
    if args.protocol == "tcp":
        if TCP not in packet:
            return False

    elif args.protocol == "udp":
        if UDP not in packet:
            return False

    elif args.protocol == "icmp":
        if ICMP not in packet:
            return False


    # Host filter
    if args.host:

        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst

        elif IPv6 in packet:
            src = packet[IPv6].src
            dst = packet[IPv6].dst

        else:
            return False

        if src != args.host and dst != args.host:
            return False


    # Port filter
    if args.port:

        if TCP in packet:

            if (
                packet[TCP].sport != args.port
                and packet[TCP].dport != args.port
            ):
                return False

        elif UDP in packet:

            if (
                packet[UDP].sport != args.port
                and packet[UDP].dport != args.port
            ):
                return False

        else:
            return False


    return True


# ==========================================
# Packet Analyzer
# ==========================================

def analyzer_packet(packet):

    global total_bytes
    global packet_count


    # ======================================
    # Apply filters FIRST
    # ======================================

    if not packet_matches_filter(packet):
        return


    # ======================================
    # Packet passed the filter
    # ======================================

    captured_packets.append(packet)

    packet_count += 1

    total_bytes += len(packet)


    # ======================================
    # IP Address Statistics
    # ======================================

    if IP in packet:

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        source_ip[src_ip] += 1
        destination_ips[dst_ip] += 1

    elif IPv6 in packet:

        src_ip = packet[IPv6].src
        dst_ip = packet[IPv6].dst

        source_ip[src_ip] += 1
        destination_ips[dst_ip] += 1

    else:

        src_ip = None
        dst_ip = None


    # ======================================
    # TCP
    # ======================================

    if TCP in packet:

        protocol["TCP"] += 1


        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport


        # -------------------------
        # Port statistics
        # -------------------------

        source_ports[src_port] += 1
        destination_ports[dst_port] += 1


        # -------------------------
        # Connection tracking
        # -------------------------

        if src_ip is not None:

            endpoint1 = (src_ip, src_port)
            endpoint2 = (dst_ip, dst_port)

            connection = tuple(
                sorted([endpoint1, endpoint2])
            )


            if connection not in connections:

                connections[connection] = {
                    "packets": 0,
                    "bytes": 0
                }


            connections[connection]["packets"] += 1

            connections[connection]["bytes"] += len(packet)


        # -------------------------
        # TCP Flags
        # -------------------------

        flags = packet[TCP].flags


        if "S" in flags:
            tcp_flags["SYN"] += 1


        if "A" in flags:
            tcp_flags["ACK"] += 1


        if "F" in flags:
            tcp_flags["FIN"] += 1


        if "R" in flags:
            tcp_flags["RST"] += 1


        if "P" in flags:
            tcp_flags["PSH"] += 1


    # ======================================
    # UDP
    # ======================================

    elif UDP in packet:

        protocol["UDP"] += 1


        source_ports[
            packet[UDP].sport
        ] += 1


        destination_ports[
            packet[UDP].dport
        ] += 1


    # ======================================
    # ICMP
    # ======================================

    elif ICMP in packet:

        protocol["ICMP"] += 1


    # ======================================
    # Other
    # ======================================

    else:

        protocol["OTHER"] += 1


# ==========================================
# Capture
# ==========================================

print("Starting packet capture...")

sniff(
    lfilter=packet_matches_filter,
    prn=analyzer_packet,
    count=100
)


# ==========================================
# Save PCAP
# ==========================================

if captured_packets:

    wrpcap(
        "captures/capture.pcap",
        captured_packets
    )

    print(
        "\nPCAP saved: captures/capture.pcap"
    )

else:

    print(
        "\nNo packets matched the filter."
    )


# ==========================================
# Protocol Statistics
# ==========================================

print("\n=== Protocol Statistics ===")

for proto, count in protocol.items():

    print(f"{proto}: {count}")


# ==========================================
# Source IP
# ==========================================

print("\n=== Top Source IPs ===")

for ip, count in source_ip.most_common(10):

    print(f"{ip}: {count}")


# ==========================================
# Destination IP
# ==========================================

print("\n=== Top Destination IPs ===")

for ip, count in destination_ips.most_common(10):

    print(f"{ip}: {count}")


# ==========================================
# Source Ports
# ==========================================

print("\n=== Top Source Ports ===")

for port, count in source_ports.most_common(10):

    print(f"{port}: {count}")


# ==========================================
# Destination Ports
# ==========================================

print("\n=== Top Destination Ports ===")

for port, count in destination_ports.most_common(10):

    print(f"{port}: {count}")


# ==========================================
# Traffic Statistics
# ==========================================

print("\n=== Traffic Statistics ===")

print(
    f"Packets Analyzed: {packet_count}"
)

print(
    f"Total KB: {total_bytes / 1024:.2f}"
)


# ==========================================
# TCP Flags
# ==========================================

print("\n=== TCP Flags ===")

for flag, count in tcp_flags.most_common():

    print(f"{flag}: {count}")


# ==========================================
# TCP Connections
# ==========================================

print("\n=== TCP Connections ===")


sorted_connections = sorted(
    connections.items(),
    key=lambda item: item[1]["packets"],
    reverse=True
)


for connection, stats in sorted_connections[:10]:

    endpoint1, endpoint2 = connection


    print(
        f"{endpoint1[0]}:{endpoint1[1]} "
        f"<-> "
        f"{endpoint2[0]}:{endpoint2[1]} "
        f"| Packets: {stats['packets']} "
        f"| Bytes: {stats['bytes']}"
    )