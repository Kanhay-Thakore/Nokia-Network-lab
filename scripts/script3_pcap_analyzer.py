# Nokia Network Lab - Script3: PCAP Analyzer.
# Reads a .pcap file and produces a traqffic summary report:
    # - Top 5 source IPS
#   - Top 5 destination ports
#   - Protocol breakdown (TCP / UDP / ICMP / Other)
#   - TCP flag counts (SYN, ACK, FIN, RST, PSH)
# Library: scapy
# Run on: Ubuntu 192.168.6.129
# Usage: python3 script3_pcap_analyzer.py
# ============================================================ 

from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from collections import Counter
import sys
import os

# Configuration
# Change this path to point whichever pcap you want to analyze.
#Using the Script 1 HTTP Capture as the defualt target.

PCAP_FILE = os.path.expanduser("~/Nokia-Network-lab/pcaps/dns_script_capture.pcap")

#How many "top" results to showin each section

TOP_N = 5

def load_pcap(filepath):
    """
    Opens the pcap file from disk and loads every packet into memory. Returns the full list of packets, 
    or exits with an error message if the file does not exist.
    """

    if not os.path.exists(filepath):
        print(f"[ERROR] FILE not found: {filepath}")
        print("         Check the PCAP_FILE path at the top of the script.")
        sys.exit(1)

    print(f"[*] Loading pcap file: {filepath}")
    packets = rdpcap(filepath)
    print(f"[*] {len(packets)} packets loaded.\n")
    return packets

def analyze_packets(packets):
    """
    Loops through every packet in the pcap once.
    Builds up four data structures as it goes:
      - src_ip_counter    : how many times each source Ip appeared 
      - dst_port_counter  : how many times each destination port appeared
      - protocol_counter  : how many packets were TCP / UDP / ICMP
      - flag_counter      : how many packets had each TCP flag set
    
      Returns all five counters.
    """

    # Counter is a special dictionary that automatically starts every
    # new key at zero increments it each time you add to it.
    # It also has a .most_common(n) method that returns the top N items.

    src_ip_counter   = Counter()
    dst_ip_counter   = Counter()
    dst_port_counter = Counter()
    protocol_counter = Counter()
    flag_counter     = Counter()

    for packet in packets:

        # -- Layer Check ----------------------
        # Not every packet in a pcap has an IP layer.
        # ARP packets, for example, operate at Layer 2 only.
        # We skip any packet that has no IP layer so we only
        # analyse packets we can actually read IP addresses from.
        if not packet.haslayer(IP):
            continue

        # --- SOURCE IP ------------------------
        # packet[IP].src is the source IP address string.
        # for example "192.168.6.1".
        # Every time we see this IP, we add 1 to its counter.
        src_ip = packet[IP].src
        src_ip_counter[src_ip] += 1

        dst_ip = packet[IP].dst
        dst_ip_counter[dst_ip] += 1
    

        # ---- PROTOCOL DETECTION + DESTINATION PORT ----------
        # We check which transport layer protocol this packet uses.
        # haslayer() returns True/False - does this packet contain
        # this protocol anywhere in its layer stack?

        if packet.haslayer(TCP):
            protocol_counter["TCP"] += 1

            # packet[TCP].dport is the destination port number (integer).
            # For HTTP this be 8080. For HTTPS it will be 443.
            dst_port = packet[TCP].dport
            dst_port_counter[dst_port] += 1

            # ---TCP FLAGS ---------------------
            # pacet[TCP].flags is a special Scapy object that holds
            # all the TCP control bits packed into one value.
            # Weconvert it to a strin (e.g. "SA" for SYN-ACK,
            # "F" for FIN, "S" for SYN) and then check whether
            # each individual flag letter appears in that string.
            
            flags = str(packet[TCP].flags)

            # "S" = SYN flag. Appears in the very first packet of
            # every new TCP connection (the handshake initiator).
            if "S" in flags:
                flag_counter["SYN"] += 1

            # "A" = ACK flag. Appears in almost every packet after
            # the first SYN - confirms receipt of previous data.
            if "A" in flags:
                flag_counter["ACK"] += 1

            # "F" = FIN flag. Signals the sender is done sending --
            # begins the graceful four-way connection teardown.
            if "F" in flags:
                flag_counter["FIN"] += 1

            # "R" = RST flag. Abruptly terminates a connecitons --
            # used in error conditions or rejected connections.
            if "R" in flags:
                flag_counter["RST"] += 1

            # "P" = PSH flag. Tells the receiver to deliver data
            # to the application immidiately instead of buffering.
            # Appears on packets carrying actual payload (HTTP body).

            if "P" in flags:
                flag_counter["PSH"] += 1

        elif packet.haslayer(UDP):
            protocol_counter["UDP"] += 1
            dst_port = packet[UDP].dport
            dst_port_counter[dst_port] += 1

        elif packet.haslayer(ICMP):
            # ICMP is the protocol that carries ping traffic and
            #network error messages (e.g. "host unreachable")
            # It has no ports -  it operates at Layer 3 only.
            protocol_counter["ICMP"] += 1

        else:
            #Any IP packet that is not TCP, UDP, o ICMP goes here.
            # In a real network this might be OSPF routing traffic,
            # GRE tunnels, or other specialised protocols.
            protocol_counter["Other"] += 1
    return src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter

def print_report(src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter, total_packets):
    """
    Takes the four counters built by analyze_packets() and prints
    a formatted summary report to the terminal.
    """

    print("=" * 60)
    print(" Nokia Network Lab - Script 3: PCAP Analysis Report")
    print("=" * 60)
    print(f"    Total packets analyzed: {total_packets}")
    print("=" * 60)

 # ── SECTION 1: TOP SOURCE IPs ──────────────────────────
    # .most_common(n) returns a list of (item, count) tuples,
    # sorted from highest count to lowest.
    # Example: [("192.168.6.1", 80), ("192.168.6.129", 40)]
    print(f"\n TOP {TOP_N} SOURCE IP ADDRESSES")
    print("     " + "-" * 40)

    for ip, count in src_ip_counter.most_common(TOP_N):
        # Calculate what percentage of all packets this IP produced.
        # round() limits the decimal places — 2 means two digits after
        # the decimal point, so 66.666... becomes 66.67.
        percentage = round((count / total_packets) * 100, 2)
        # The <20 in the format string left-aligns the IP address
        # in a 20-character wide column so all the counts line up neatly
        print(f"    {ip:<20} {count:>5} packets ({percentage}%)")

    # ── SECTION 2: TOP DESTINATION PORTS ──────────────────
    print(f"\n TOP {TOP_N} DESTINATION IP ADDRESSES")
    print("   " + "-" * 40)

    for ip, count in dst_ip_counter.most_common(TOP_N):
        percentage = round((count / total_packets) * 100, 2)
        print(f"    {ip:<20} {count:>5} packets  ({percentage}%)")

    print(f"\n  TOP {TOP_N} DESTINATION PORTS")
    print("   " + "-" * 40)

    port_names = {
        80:     "HTTP",
        443:    "HTTPS/QUIC",        
        8080:   "HTTP-alt",
        53:     "DNS",
        22:     "SSH",
        21:     "FTP",
        25:     "SMTP",
        5004:   "RTP"
    }

    for port, count in dst_port_counter.most_common(TOP_N):
        service = port_names.get(port, "unknown")
        percentage  = round((count / total_packets) * 100, 2)
        print(f"    Port {port:>5} ({service:<12})  {count:>5} packets ({percentage}%)")
    # ── SECTION 3: PROTOCOL BREAKDOWN ─────────────────────
    print(f"\n  PROTOCOL BREAKDOWN")
    print("    " + "-" * 40)
    for proto in ["TCP", "UDP", "ICMP", "Other"]:
        # dict.get(proto, 0) returns 0 if that protocol was never seen —
        # this avoids a KeyError crash if e.g. there were no ICMP packets.
        count = protocol_counter.get(proto, 0)
        if count > 0:
            percentage = round((count / total_packets)  * 100, 2)
            print(f"    {proto:<8}  {count:>5} packets ({percentage}%)")

    # ── SECTION 4: TCP FLAG COUNTS ─────────────────────────
    print(f"\n TCP FLAG COUNTS")
    print("  " + "-" * 40)

    tcp_total = protocol_counter.get("TCP", 0)

    if tcp_total == 0:
        print("     No TCP packets found in this capture.")
    else:
        for flag in ["SYN", "ACK", "FIN", "RST", "PSH"]:
            count = flag_counter.get(flag, 0)
            # Percentage here is out of TCP packets only, not all packets.
            percentage = round((count / tcp_total) * 100, 2)
            print(f"    {flag:<6}  {count:>5} packets  ({percentage}% of TCP)")

        #         # ── BONUS: SYN FLOOD INDICATOR ────────────────────
        # In a healthy connection, almost every SYN is followed by
        # a SYN-ACK and then an ACK — so SYN count should roughly
        # equal ACK count. In a SYN flood, SYN count is enormous
        # and ACK count is tiny because attackers never complete
        # the handshake. This ratio is exactly what Nokia's DDoS
        # detection systems monitor in production traffic.
        syn_count = flag_counter.get("SYN", 0)
        ack_count = flag_counter.get("ACK", 0)

        print()
        if ack_count > 0:
            syn_ack_ratio = round(syn_count / ack_count, 3)
            print(f"    SYN/ACK ratio:  {syn_ack_ratio}")
            if syn_ack_ratio > 0.7:
                print("     [WARNING] High SYN/ ACK ratio - possible SYN flood pattern.")
                print("               In normal traffic this ratio is well below 0.5.")
            else:
                print("   [OK] SYN/ACK ratio is normal - no flood pattern detected.")
        else:
            print("   [INFO] No ACK packets found -- cannot compute SYN/ACK ratio.")
    print("\n" + "=" * 60)
    print("     Analysis complete.")
    print("=" * 60 + "\n")

def main():
    """
    Entry point. Calls the three functions in order:
    load -> analyse -. report.
    This separation (load / analyze / report) is standard
    professional script structure - each function does one job."""

    packets = load_pcap(PCAP_FILE)
    total = len(packets)

    src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter = analyze_packets(packets)
    print_report(src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter, total)


# Standard Python entry point guard.
# This means: only run main() if this file is being executed directly
# (python3 script3_pcap_analyzer.py), not if it is being imported
# as a module by another script. Script 5 will import this later.
if __name__ == "__main__":
    main()
