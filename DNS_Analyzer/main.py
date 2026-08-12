from resolver import query_record, RECORD_TYPES


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


if __name__ == "__main__":
    main()