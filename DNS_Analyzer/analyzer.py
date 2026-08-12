from resolver import RECORD_TYPE,query_record

def analyze_domain(domain):
    results = {}

    for record_type in RECORD_TYPE:
        results[record_type] = query_record(domain,record_type)

        return results
    
