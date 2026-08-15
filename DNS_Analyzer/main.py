from resolver import query_record, RECORD_TYPES,reverse_dns


def main():
    domain = input("\n=== Enter domain name ===\n").strip()

    print(f"\n Analyzing: {domain}\n")

    for record_type in RECORD_TYPES:
        print(f"[{record_type}]")

        records = query_record(domain, record_type)

        if records:
            for record in records:
                print(f"  Value {record['value']}")
                print(f"  TTL: {record['ttl']}")
        else:
            print("  No records found")

        print()
    print("=== Reverse DNS ===")
    ip_address = input("Enter IP address: ").strip()  
    hostname = reverse_dns(ip_address)
    if hostname in hostname:
        print(f"  {ip_address} -> {hostname}")
    else:
        print("  No PTR record found")      


if __name__ == "__main__":
    main()