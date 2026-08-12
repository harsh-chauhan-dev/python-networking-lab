import dns.resolver
import dns.exception

RECORD_TYPES = [
    "A",
    "AAAA",
    "MX",
    "NS",
    "CNAME",
    "TXT",
    "SOA"
]


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