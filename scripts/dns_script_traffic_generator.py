import dns.resolver
import time
import datetime

DOMAINS = [
    "google.com",
    "nokia.com",
    "github.com",
    "cloudflare.com",
    "nonexistentdomain12345abc.com" # intentionally fake - tests error handling
]

RECORD_TYPES = ["A", "AAAA", "MX"]
DELAY_SECONDS = 0.5 #Pause between each query so we don't spam the dns server

#COUNTERS - track how many queries succeed or fail

SUCCESS_COUNT = 0
FAIL_COUNT = 0

# FUNCTION 1-query_dns
# Job: send ONE DNS quesry for DNE domain + ONE record type, print the result

def query_dns(domain, record_type):
    global SUCCESS_COUNT , FAIL_COUNT
    

    # Grab the current time so every printed line has a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Start the stopwatch
        start_time = time.time()

        # THeACTUAL DNS QUERY - ask the DNS server to look up this domain

        answers = dns.resolver.resolve(domain, record_type)

        # Stop the stopwatch
        end_time = time.time()

        # Calculate how many milliseconds the querytook
        duration = round((end_time - start_time) * 1000, 2)

        # Read the TTL (Time to Live) - how long this answer is cached
        ttl = answers.rrset.ttl

        #Collect all the IP addresses (or mail server) returend in the answer

        results = [str(r) for r in answers]

        #Query worked - count it as a success
        SUCCESS_COUNT += 1

        print(f"[{timestamp}] {domain:<35} {record_type:<6} SUCCESS | {duration}ms | TTL: {ttl}s | {results}")


        # ----- Error handlers - one for each type of DNS failures

    except dns.resolver.NXDOMAIN:
        # NXDOMAIN = "NON- Existent DOMAIN" - THE DOMAIN DOEES NOT EXIST
        FAIL_COUNT += 1
        print(f"[{timestamp}] {domain:<35} {record_type:<6} NXDOMAIN | Domain does not exist")

    except dns.resolver.NoAnswer:
        # The Domain EXISTS but has no record of this type (e. asking for MX on a domain with no mail server)
        FAIL_COUNT += 1
        print(f"[{timestamp}] {domain:<35} {record_type:<6} NO ANSWER | No {record_type} record configured")

    except dns.resolver.Timeout:
        #DNS server took too long to reply
        FAIL_COUNT += 1
        print(f"[{timestamp}] {domain:<35} {record_type:<6} TIMEOUT | DNS server did not respond")

    except Exception as e:
        # Catch-all for any other unexpected error
        FAIL_COUNT += 1
        print(f"[{timestamp}] {domain:<35} {record_type:<6} ERROR | {e}")



# Function 2 - run_dns_tests
# Job: loop through every domain + every record type and call query_dns each time
# # This is the "controller" - it decides What to test and in what order
# 

def run_dns_tests():
    total_queries = len(DOMAINS) * len(RECORD_TYPES)

    print("=" * 75)
    print(" Nokia Network Lab - Script 2: DNS Test Script")
    print(f" Domains: {len(DOMAINS)}    |    Record types: {RECORD_TYPES}   |   Total queries: {total_queries}")
    print("=" * 75)

    for domain in DOMAINS:
        print(f"\n  ── {domain}  ──")

        for record_type in RECORD_TYPES:
            query_dns(domain, record_type)
            time.sleep(DELAY_SECONDS)
# Print the final summary after all queries are done  ──

    print("\n" + "=" * 75)
    print(" RESULTS SUMMARY")
    print(f" Total queries  : {total_queries}")
    print(f" Successful     : {SUCCESS_COUNT}")
    print(f" Failed     : {FAIL_COUNT}")
    print(f"    Success rate : {round((SUCCESS_COUNT /  total_queries) * 100, 1)}%")
    print("=" * 75)

    # Entry poin - this runs first when you execute the script

if __name__ == "__main__":
    run_dns_tests()
        