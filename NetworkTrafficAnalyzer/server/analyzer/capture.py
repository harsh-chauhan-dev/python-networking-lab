import os
from scapy.all import sniff, wrpcap, rdpcap


class PacketCapture:
    """Handles packet capture and PCAP storage."""

    def __init__(self, packet_filter=None, stats=None):
        """
        Initialize PacketCapture.

        :param packet_filter: PacketFilter instance or None
        :param stats: TrafficStatistics instance or None
        """
        self.packet_filter = packet_filter
        self.stats = stats
        self.captured_packets = []

    def _packet_callback(self, packet):
        """Callback executed for each sniffed packet."""
        if self.packet_filter and not self.packet_filter.matches(packet):
            return

        self.captured_packets.append(packet)
        if self.stats:
            self.stats.process_packet(packet)

    def capture(self, count=100, interface=None, timeout=None):
        """
        Start live packet capture.

        :param count: Number of packets to capture
        :param interface: Network interface to listen on
        :param timeout: Capture timeout in seconds
        :return: List of captured packets
        """
        print("Starting packet capture...")
        sniff_kwargs = {
            "prn": self._packet_callback,
            "count": count
        }
        if interface:
            sniff_kwargs["iface"] = interface
        if timeout:
            sniff_kwargs["timeout"] = timeout

        sniff(**sniff_kwargs)
        return self.captured_packets

    def load_pcap(self, pcap_path):
        """
        Read and analyze an existing PCAP file.

        :param pcap_path: Path to .pcap file
        :return: List of loaded packets
        """
        if not os.path.exists(pcap_path):
            raise FileNotFoundError(f"PCAP file not found: {pcap_path}")

        packets = rdpcap(pcap_path)
        for pkt in packets:
            self._packet_callback(pkt)
        return self.captured_packets

    def save_pcap(self, filepath="captures/capture.pcap"):
        """
        Save captured packets to a PCAP file.

        :param filepath: Path where the PCAP file should be written
        """
        if not self.captured_packets:
            print("\nNo packets captured to save.")
            return False

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wrpcap(filepath, self.captured_packets)
        print(f"\nPCAP saved: {filepath}")
        return True
