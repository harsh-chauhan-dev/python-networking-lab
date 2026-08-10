from scapy.all import IP, IPv6, TCP, UDP, ICMP


class PacketFilter:
    """Filter network packets based on protocol, host IP, and port."""

    def __init__(self, protocol=None, host=None, port=None):
        """
        Initialize PacketFilter.

        :param protocol: Protocol to filter ('tcp', 'udp', 'icmp') or None for all
        :param host: Host IP address to filter (src or dst) or None for all
        :param port: Port number to filter (src or dst) or None for all
        """
        self.protocol = protocol.lower() if protocol else None
        self.host = host
        self.port = int(port) if port is not None else None

    def matches(self, packet):
        """
        Check if a given packet matches the filter criteria.

        :param packet: Scapy packet object
        :return: True if packet matches filter criteria, False otherwise
        """
        # Protocol filter
        if self.protocol == "tcp":
            if TCP not in packet:
                return False
        elif self.protocol == "udp":
            if UDP not in packet:
                return False
        elif self.protocol == "icmp":
            if ICMP not in packet:
                return False

        # Host filter
        if self.host:
            if IP in packet:
                src = packet[IP].src
                dst = packet[IP].dst
            elif IPv6 in packet:
                src = packet[IPv6].src
                dst = packet[IPv6].dst
            else:
                return False

            if src != self.host and dst != self.host:
                return False

        # Port filter
        if self.port:
            if TCP in packet:
                if packet[TCP].sport != self.port and packet[TCP].dport != self.port:
                    return False
            elif UDP in packet:
                if packet[UDP].sport != self.port and packet[UDP].dport != self.port:
                    return False
            else:
                return False

        return True
