from scapy.all import sniff,IP,TCP,UDP,ICMP,wrpcap
from collections import Counter;

protocol = Counter()
source_ip = Counter()
destination_ips = Counter()
source_ports = Counter()
destination_ports = Counter()
total_bytes = 0
packet_count = 0
tcp_flags = Counter()
connections = Counter()
captured_packets = []

def analyzer_packet(packet):

    global total_bytes,packet_count

    captured_packets.append(packet) 
    packet_count+=1
    total_bytes += len(packet)
   
    if IP not in packet:
        return

    source_ip[packet[IP].src]+=1
    destination_ips[packet[IP].dst]+=1
    if TCP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        protocol["TCP"] +=1
        source_ports[src_port]+=1
        destination_ports[dst_port]+=1

        endpoint1 = (src_ip,src_port)
        endpoint2=(dst_ip,dst_port)
        connection = tuple(sorted([endpoint1,endpoint2]))

        if connection not in connections:
         connections[connection]={
            "packets":0,
            "bytes":0
        }
        connections[connection]["packets"]+=1
        connections[connection]["bytes"]+=len(packet)

        # connections[connection] +=1
      
        flags = packet[TCP].flags

        if "S" in flags:
          tcp_flags["SYN"]+=1

        if "A" in flags:
            tcp_flags["ACK"] +=1

        if "F" in flags:
            tcp_flags["FIN"]+=1

        if "R" in flags:
            tcp_flags["RST"]+=1 

        if "P" in flags:
            tcp_flags["PSH"]+=1

    elif UDP in packet:
        protocol["UDP"]+=1
        source_ports[packet[UDP].sport]+=1
        destination_ports[packet[UDP].dport]+=1

    elif ICMP in packet:
        protocol["ICMP"] +=1

    else:
        protocol["OTHER"] +=1


sniff(prn=analyzer_packet,
      count=100)
wrpcap("captures/capture.pcap",captured_packets)

print("\n ===Protocol Statistics ===")

for protocol, count in protocol.items():
    print(f"{protocol}: {count}")


print("\n === Top Source IPs ===")

for ip,count in source_ip.most_common(10):
    print(f"{ip}: {count}")

print("\n === Top Destination IPs ===")

for ip,count in destination_ips.most_common(10):
    print(f"{ip}: {count}")

print("\n === Top Source Ports ===")
for port, count in source_ports.most_common(10):
    print(f"{port}: {count}")

print("\n === Top Destination Ports ===")
for port, count in destination_ports.most_common(10):
    print(f"{port}: {count}")


print("\n=== Traffic Statistics ===")

print(f"Packets Captured: {packet_count}")
print(f"Total KB: {total_bytes / 1024:.2f}")

print("\n=== TCP Flags ===")

for flag, count in tcp_flags.most_common():
    print(f"{flag}: {count}")

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