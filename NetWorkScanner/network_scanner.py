import scapy.all as scapy
import ipaddress


def get_network():
    """ 
    Ask the user for a network range and validate the input.
    """
    while True:
        network = input("Enter the network range (e.g., 192.168.1.0/24): ")

        try:
            ipaddress.ip_network(network)
            return network
        except ValueError:
            print("Invalid newtwork . Try again.\n")



def create_arp_request(network):
    """
    Create an ARP Request packet .

    pdst = Destination IP Range
    """            
    return scapy.ARP(pdst=network)


def create_broadcast():
    """
    Create an Ethernet Broadcast Frame.

    ff:ff:ff:ff:ff:ff means
    "Send this packet to everyone"
    """
    return scapy.Ether(dst="ff:ff:ff:ff:ff:ff")


def send_request(packet):
    """
    Send packet and receive Packet replies.

    srp()
    Send and Receive Packet at Layer 2.
    """
    answered,unanswerd = scapy.srp(
        packet,
        timeout = 2,
        verbose  = False
    )
    return answered


def print_result(answered):
    """
    Print scan result.
    """
    print("\n" + "-"*45)
    print("{:<18} {}".format("IP Address ","MAC Address"))
    print("-" *45)

    for sent ,received in answered:
        print("{:<18} {}".format(
            received.psrc,
            received.hwsrc
        ))


def print_app_name():
    print("""
    \n
█      ███  █   █     ████  ███   ███  █   █ █   █ █████ ████  
█     █   █ ██  █    █     █     █   █ ██  █ ██  █ █     █   █ 
█     █████ █ █ █     ███  █     █████ █ █ █ █ █ █ ████  ████  
█     █   █ █  ██        █ █     █   █ █  ██ █  ██ █     █  █  
█████ █   █ █   █    ████   ███  █   █ █   █ █   █ █████ █   █ 
    \n """)


def main():
    print_app_name()

    network = get_network()

    arp_request = create_arp_request(network)

    broadcast = create_broadcast()

    packet = broadcast / arp_request

    answered = send_request(packet)

    print_result(answered)




if __name__ =="__main__":
    main()