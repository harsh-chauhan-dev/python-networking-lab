import argparse
import sys
import os
from pathlib import Path

# Add server directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyzer import PacketFilter, TrafficStatistics, PacketCapture


def main():
    parser = argparse.ArgumentParser(
        description="Python Network Traffic Analyzer Server"
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

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of packets to capture (default: 100)"
    )

    parser.add_argument(
        "--output",
        default="captures/capture.pcap",
        help="Path to save captured PCAP file (default: captures/capture.pcap)"
    )

    parser.add_argument(
        "--pcap",
        help="Path to an existing PCAP file to read and analyze instead of live capture"
    )

    parser.add_argument(
        "--api",
        action="store_true",
        help="Launch the REST API server"
    )

    args = parser.parse_args()

    if args.api:
        print("Starting Network Traffic Analyzer API Server...")
        try:
            from api.server import start_server
            start_server()
        except Exception as e:
            print(f"Error starting API server: {e}")
        return

    # Initialize Filter and Statistics module
    packet_filter = PacketFilter(
        protocol=args.protocol,
        host=args.host,
        port=args.port
    )
    stats = TrafficStatistics()
    capturer = PacketCapture(packet_filter=packet_filter, stats=stats)

    if args.pcap:
        print(f"Analyzing offline PCAP file: {args.pcap}...")
        capturer.load_pcap(args.pcap)
    else:
        capturer.capture(count=args.count)
        capturer.save_pcap(args.output)

    # Output detailed report
    stats.print_report()


if __name__ == "__main__":
    main()
