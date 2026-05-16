# Nokia Network Lab — Phase 3: Script 3 — PCAP Analyzer
## Python Automation | Automated PCAP Traffic Analysis + Report Generation
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE

---

## JD Mapping

Script 3 directly addresses: *"Break down complex problems piece by piece, diving deep into
traffic flows, signatures, packet behavior, and system interactions"* and *"Verify and analyze
application detection mechanisms along with network behaviors."* A Nokia test engineer does not
just capture traffic — they read it systematically, extract meaningful statistics, and flag
anomalies. Script 3 automates exactly that process: it reads any pcap file and produces a
structured report covering source and destination IPs, destination ports with service name
mapping, protocol breakdown, TCP flag counts, and a SYN/ACK ratio check that directly mirrors
the logic Nokia's DDoS mitigation systems use in production.

---

## Script Overview

| Property | Value |
|---|---|
| Script name | `script3_pcap_analyzer.py` |
| Location on Ubuntu | `~/Nokia-Network-lab/scripts/` |
| Input | Any `.pcap` file — set via `PCAP_FILE` at top of script |
| Default target | `~/Nokia-Network-lab/pcaps/http_python_script_capture.pcap` |
| Library | `scapy` |
| Nokia JD mapping | Traffic flow analysis, packet behavior, automated test tooling |

**What the script does in plain English:** Opens any pcap file, loops through every packet once,
builds five counters tracking source IPs, destination IPs, destination ports, protocols, and TCP
flags, then prints a formatted report with top results in each category and a SYN/ACK ratio
check that flags potential SYN flood patterns.

---

## Library Used — Scapy

Scapy is a Python library built specifically for network packet work. It can read pcap files,
decode every protocol layer automatically, build packets from scratch, and send them on the wire.
In Script 3 it is used purely as a reader — `rdpcap()` opens the pcap file and returns all
packets as a list where each item is a fully decoded packet with all its layers accessible via
`packet[IP].src`, `packet[TCP].flags`, etc.

**Install on Ubuntu:**
```bash
pip install scapy --break-system-packages
```

---

## Bugs Found and Fixed During Development

| Bug | What Was Wrong | Fix Applied |
|---|---|---|
| Missing quotes on ICMP key | `protocol_counter[ICMP]` used the Scapy class as dict key instead of string | Changed to `protocol_counter["ICMP"]` |
| Comma instead of dot | `dst_port_counter,most_common(TOP_N)` treated as tuple not method call | Changed to `dst_port_counter.most_common(TOP_N)` |
| Function not called | `analyze_packets` referenced without parentheses or argument | Changed to `analyze_packets(packets)` |
| Duplicate destination IP block | Block added during dst_ip refactor landed twice in print_report | Deleted the duplicate block |

---

## Development Workflow

Script written in VS Code on Windows, edited directly on Ubuntu via nano for path updates,
executed on Ubuntu. No SCP required for the path fix since nano edits the file in place on Ubuntu.

```bash
# Edit directly on Ubuntu
sudo nano ~/Nokia-Network-lab/scripts/script3_pcap_analyzer.py

# Run
python3 ~/Nokia-Network-lab/scripts/script3_pcap_analyzer.py
```

---

## Script — Full Code

```python
from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from collections import Counter
import sys
import os

PCAP_FILE = os.path.expanduser("~/Nokia-Network-lab/pcaps/http_python_script_capture.pcap")
TOP_N = 5


def load_pcap(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        print("        Check the PCAP_FILE path at the top of the script.")
        sys.exit(1)

    print(f"[*] Loading pcap file: {filepath}")
    packets = rdpcap(filepath)
    print(f"[*] {len(packets)} packets loaded.\n")
    return packets


def analyze_packets(packets):
    src_ip_counter   = Counter()
    dst_ip_counter   = Counter()
    dst_port_counter = Counter()
    protocol_counter = Counter()
    flag_counter     = Counter()

    for packet in packets:
        if not packet.haslayer(IP):
            continue

        src_ip = packet[IP].src
        src_ip_counter[src_ip] += 1

        dst_ip = packet[IP].dst
        dst_ip_counter[dst_ip] += 1

        if packet.haslayer(TCP):
            protocol_counter["TCP"] += 1
            dst_port = packet[TCP].dport
            dst_port_counter[dst_port] += 1

            flags = str(packet[TCP].flags)

            if "S" in flags:
                flag_counter["SYN"] += 1
            if "A" in flags:
                flag_counter["ACK"] += 1
            if "F" in flags:
                flag_counter["FIN"] += 1
            if "R" in flags:
                flag_counter["RST"] += 1
            if "P" in flags:
                flag_counter["PSH"] += 1

        elif packet.haslayer(UDP):
            protocol_counter["UDP"] += 1
            dst_port = packet[UDP].dport
            dst_port_counter[dst_port] += 1

        elif packet.haslayer(ICMP):
            protocol_counter["ICMP"] += 1

        else:
            protocol_counter["Other"] += 1

    return src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter


def print_report(src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter, total_packets):

    print("=" * 60)
    print("  Nokia Network Lab — Script 3: PCAP Analysis Report")
    print("=" * 60)
    print(f"  Total packets analyzed: {total_packets}")
    print("=" * 60)

    print(f"\n  TOP {TOP_N} SOURCE IP ADDRESSES")
    print("  " + "-" * 40)
    for ip, count in src_ip_counter.most_common(TOP_N):
        percentage = round((count / total_packets) * 100, 2)
        print(f"  {ip:<20} {count:>5} packets  ({percentage}%)")

    print(f"\n  TOP {TOP_N} DESTINATION IP ADDRESSES")
    print("  " + "-" * 40)
    for ip, count in dst_ip_counter.most_common(TOP_N):
        percentage = round((count / total_packets) * 100, 2)
        print(f"  {ip:<20} {count:>5} packets  ({percentage}%)")

    print(f"\n  TOP {TOP_N} DESTINATION PORTS")
    print("  " + "-" * 40)

    port_names = {
        80:   "HTTP",
        443:  "HTTPS/QUIC",
        8080: "HTTP-alt",
        53:   "DNS",
        22:   "SSH",
        21:   "FTP",
        25:   "SMTP",
        5004: "RTP",
    }

    for port, count in dst_port_counter.most_common(TOP_N):
        service = port_names.get(port, "unknown")
        percentage = round((count / total_packets) * 100, 2)
        print(f"  Port {port:>5} ({service:<12})  {count:>5} packets  ({percentage}%)")

    print(f"\n  PROTOCOL BREAKDOWN")
    print("  " + "-" * 40)
    for proto in ["TCP", "UDP", "ICMP", "Other"]:
        count = protocol_counter.get(proto, 0)
        if count > 0:
            percentage = round((count / total_packets) * 100, 2)
            print(f"  {proto:<8}  {count:>5} packets  ({percentage}%)")

    print(f"\n  TCP FLAG COUNTS")
    print("  " + "-" * 40)

    tcp_total = protocol_counter.get("TCP", 0)

    if tcp_total == 0:
        print("  No TCP packets found in this capture.")
    else:
        for flag in ["SYN", "ACK", "FIN", "RST", "PSH"]:
            count = flag_counter.get(flag, 0)
            percentage = round((count / tcp_total) * 100, 2)
            print(f"  {flag:<6}  {count:>5} packets  ({percentage}% of TCP)")

        syn_count = flag_counter.get("SYN", 0)
        ack_count = flag_counter.get("ACK", 0)

        print()
        if ack_count > 0:
            syn_ack_ratio = round(syn_count / ack_count, 3)
            print(f"  SYN/ACK ratio: {syn_ack_ratio}")
            if syn_ack_ratio > 0.7:
                print("  [WARNING] High SYN/ACK ratio — possible SYN flood pattern.")
                print("            In normal traffic this ratio is well below 0.5.")
            else:
                print("  [OK] SYN/ACK ratio is normal — no flood pattern detected.")
        else:
            print("  [INFO] No ACK packets found — cannot compute SYN/ACK ratio.")

    print("\n" + "=" * 60)
    print("  Analysis complete.")
    print("=" * 60 + "\n")


def main():
    packets = load_pcap(PCAP_FILE)
    total   = len(packets)
    src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter = analyze_packets(packets)
    print_report(src_ip_counter, dst_ip_counter, dst_port_counter, protocol_counter, flag_counter, total)


if __name__ == "__main__":
    main()
```

---

## Execution — Run 1: HTTP Traffic

```bash
python3 ~/Nokia-Network-lab/scripts/script3_pcap_analyzer.py
```

**Results — http_python_script_capture.pcap:**

```
[*] Loading pcap file: /home/ubuntu/Nokia-Network-lab/pcaps/http_python_script_capture.pcap
[*] 200 packets loaded.

============================================================
  Nokia Network Lab — Script 3: PCAP Analysis Report
============================================================
  Total packets analyzed: 200
============================================================

  TOP 5 SOURCE IP ADDRESSES
  ----------------------------------------
  192.168.6.1          100 packets  (50.0%)
  192.168.6.129        100 packets  (50.0%)

  TOP 5 DESTINATION IP ADDRESSES
  ----------------------------------------
  192.168.6.129        100 packets  (50.0%)
  192.168.6.1          100 packets  (50.0%)

  TOP 5 DESTINATION PORTS
  ----------------------------------------
  Port  8080 (HTTP-alt   )    100 packets  (50.0%)
  Port  8293 (unknown    )      5 packets  (2.5%)
  Port  8294 (unknown    )      5 packets  (2.5%)
  Port  8295 (unknown    )      5 packets  (2.5%)
  Port  8296 (unknown    )      5 packets  (2.5%)

  PROTOCOL BREAKDOWN
  ----------------------------------------
  TCP       200 packets  (100.0%)

  TCP FLAG COUNTS
  ----------------------------------------
  SYN        40 packets  (20.0% of TCP)
  ACK       180 packets  (90.0% of TCP)
  FIN        40 packets  (20.0% of TCP)
  RST         0 packets  (0.0% of TCP)
  PSH        60 packets  (30.0% of TCP)

  SYN/ACK ratio: 0.222
  [OK] SYN/ACK ratio is normal — no flood pattern detected.
============================================================
  Analysis complete.
============================================================
```

**What the numbers prove:**
- 200 packets total — 20 requests × ~10 packets per connection (handshake + data + teardown)
- 50/50 source IP split — traffic flows both directions between client and server
- Port 8080 = 100 packets — HTTP test server port, confirms Script 1 traffic identified correctly
- Unknown ports 8293-8296 — ephemeral source ports randomly assigned per connection, normal
- TCP 100% — HTTP is TCP-based, correct
- SYN 40 = exactly 2 SYNs per request (one from client, one SYN-ACK from server), 20 requests × 2 = 40
- FIN 40 = 20 connections opened and 20 closed cleanly
- SYN/ACK ratio 0.222 — healthy, well below 0.7 threshold
- [OK] no flood pattern — correct for normal automated HTTP traffic

---

## Execution — Run 2: DNS Traffic

Change PCAP_FILE to dns_script_capture.pcap and run again.

```bash
sudo nano ~/Nokia-Network-lab/scripts/script3_pcap_analyzer.py
# Change PCAP_FILE line to:
# PCAP_FILE = os.path.expanduser("~/Nokia-Network-lab/pcaps/dns_script_capture.pcap")

python3 ~/Nokia-Network-lab/scripts/script3_pcap_analyzer.py
```

**Results — dns_script_capture.pcap:**

```
[*] Loading pcap file: /home/ubuntu/Nokia-Network-lab/pcaps/dns_script_capture.pcap
[*] 38 packets loaded.

============================================================
  Nokia Network Lab — Script 3: PCAP Analysis Report
============================================================
  Total packets analyzed: 38
============================================================

  TOP 5 SOURCE IP ADDRESSES
  ----------------------------------------
  192.168.6.129         19 packets  (50.0%)
  192.168.6.2           19 packets  (50.0%)

  TOP 5 DESTINATION IP ADDRESSES
  ----------------------------------------
  192.168.6.2           19 packets  (50.0%)
  192.168.6.129         19 packets  (50.0%)

  TOP 5 DESTINATION PORTS
  ----------------------------------------
  Port    53 (DNS        )     19 packets  (50.0%)
  Port 39699 (unknown    )      1 packets  (2.63%)
  Port 51795 (unknown    )      1 packets  (2.63%)
  Port 46472 (unknown    )      1 packets  (2.63%)
  Port 40372 (unknown    )      1 packets  (2.63%)

  PROTOCOL BREAKDOWN
  ----------------------------------------
  UDP        38 packets  (100.0%)

  TCP FLAG COUNTS
  ----------------------------------------
  No TCP packets found in this capture.

============================================================
  Analysis complete.
============================================================
```

**What the numbers prove:**
- 38 packets — 19 DNS queries + 19 responses (Script 2 sent 15 queries plus background system DNS)
- 192.168.6.2 — VMware's built-in NAT DNS resolver, only visible in DNS capture not HTTP capture
- Port 53 = DNS, correctly labelled by port_names dictionary
- Unknown ports 39699-40372 — ephemeral source ports per DNS query, normal
- UDP 100% — DNS uses UDP, correct
- No TCP packets — DNS has no flags section, script handled this gracefully without crashing

---

## Key Concepts in Script 3

**Counter from collections:** Special dictionary that starts every new key at zero and
auto-increments. `.most_common(n)` returns top n items sorted by count — built-in ranking
with no sorting code required.

**packet.haslayer(IP):** Returns True/False — does this packet contain this protocol layer?
Used to skip ARP and other non-IP packets cleanly with `continue`.

**packet[IP].src / packet[IP].dst:** Access source and destination IP address fields directly
from the IP layer of any packet. Returns a string like "192.168.6.1".

**packet[TCP].dport:** Destination port number as an integer from the TCP layer. Port 8080 for
HTTP, 53 for DNS, 443 for HTTPS/QUIC.

**str(packet[TCP].flags):** Converts Scapy's packed TCP flags object to a readable string like
"SA" for SYN-ACK, "F" for FIN, "PA" for PSH-ACK. The `in` operator then checks for individual
flag letters without needing to decode the bit field manually.

**SYN/ACK ratio:** In normal traffic every SYN is completed by SYN-ACK then ACK so ACK count
is always much larger than SYN count — ratio stays well below 0.5. In a SYN flood, attacker
sends massive SYNs but never completes the ACK so ratio spikes above 1.0. Threshold of 0.7
flags suspicious patterns. This is the same ratio Nokia's NetGuard systems monitor in production.

**os.path.expanduser("~"):** Converts the tilde shortcut to the full home directory path
/home/ubuntu so Python can find the file regardless of which directory the script is run from.

**port_names dictionary with .get(port, "unknown"):** Maps known port numbers to service names
for human-readable output. `.get(key, default)` returns "unknown" instead of crashing with
KeyError when an ephemeral port number is not in the dictionary.

---

## Why Script 3 Can Analyze Any Pcap

Script 3 does not know or care how the pcap was generated — manual tcpdump, Python automation,
Wireshark export, or any other tool. It reads the binary pcap format which is universal across
all capture tools. Changing the `PCAP_FILE` path is all that is required to analyze a completely
different capture. This makes it a genuinely reusable test tool, not a one-off script.

Tested against:
- `http_python_script_capture.pcap` — TCP, port 8080, SYN/ACK ratio analysis
- `dns_script_capture.pcap` — UDP, port 53, graceful no-TCP handling

Compatible with all other lab pcaps:
- `tls_capture.pcap` — TCP port 443, encrypted HTTPS
- `quic_capture.pcap` — UDP port 443, QUIC/HTTP3
- `rtp_capture.pcap` — UDP port 5004, VoIP

---

## Git Commit

```bash
cd ~/Nokia-Network-lab
git add .
git commit -m "Add Script 3 PCAP analyzer"
git push
```

**Commit output:**
```
[main f2b8c42] Add Script 3 PCAP Analyzer
 1 file changed, 277 insertions(+)
 create mode 100644 scripts/script3_pcap_analyzer.py
```

---

## Screenshots Taken

**Screenshot 1 — HTTP pcap analysis terminal output**
Full terminal showing Script 3 report for http_python_script_capture.pcap — 200 packets,
TCP 100%, port 8080, SYN/ACK ratio 0.222, [OK] status.

**Screenshot 2 — DNS pcap analysis terminal output**
Full terminal showing Script 3 report for dns_script_capture.pcap — 38 packets, UDP 100%,
port 53, no TCP packets found message.

---

## Interview Talking Point

*"Script 3 is a Python PCAP analyzer built with Scapy that reads any pcap file and produces
a structured traffic report: top source and destination IPs by volume, top destination ports
with service name mapping, protocol breakdown across TCP UDP ICMP and other, and complete TCP
flag counts. It also computes the SYN to ACK ratio and flags it if it exceeds the threshold
associated with SYN flood patterns — the same ratio that Nokia's DDoS mitigation systems monitor
in production. I ran it against two different captures — HTTP traffic showing TCP, port 8080,
and a healthy SYN/ACK ratio of 0.222, then DNS traffic showing UDP, port 53, and graceful
handling of a capture with no TCP packets at all. One script, two completely different protocols,
correct output both times. Changing the input file path is the only change required to analyze
any new capture."*

---

*Script 3 Completed: May 2026*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Script 4 — Mini DDoS Detector*
