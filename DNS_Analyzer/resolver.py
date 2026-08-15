import dns.resolver
import dns.exception
import dns.reversename

RECORD_TYPES = [
    "A",
    "AAAA",
    "MX",
    "NS",
    "CNAME",
    "TXT",
    "SOA"
]

def reverse_dns(ip_address):
    try:
        reverse_name = dns.reversename.from_address(ip_address)
        print(f"Reverse DNS name: {reverse_name}")

        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8"]
        
        answers = dns.resolver.resolve(
            reverse_name,
            "PTR"
        )

        records = []

        for answer in answers:
            records.append(str(answer))

        return records

    except dns.resolver.NXDOMAIN:
        print(f"No PTR record exists for {ip_address}")
        return []

    except dns.resolver.NoAnswer:
        print(f"No PTR record found for {ip_address}")
        return []

    except dns.exception.Timeout:
        print(f"Reverse DNS timeout for {ip_address}")
        return []

    except Exception as error:
        print(f"Reverse DNS failed: {error}")
        return []

def query_record(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)

        ttl = answers.rrset.ttl
        records = []

        for answer in answers:
            records.append({
                "value":str(answer),
                "ttl":ttl
            })

        return records

    except dns.resolver.NoAnswer:
        return []

    except dns.resolver.NXDOMAIN:
        raise ValueError(f"Domain does not exist: {domain}")

    except dns.resolver.NoNameservers:
        raise ValueError(f"No nameserver available for: {domain}")

    except dns.exception.Timeout:
        print(f"DNS timeout for {record_type}")
        return []
    
    except Exception as error:
        raise RuntimeError(f"DNS query failed: {error}")