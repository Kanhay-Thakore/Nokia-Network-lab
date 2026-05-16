# Nokia Network Lab — Phase 3: Script 2 — DNS Test Script
> Status: ✅ COMPLETE | Nokia JD: "Develop automated test cases" + "Validate application signatures"

---

## What This Script Does

Automated DNS query tool that fires A, AAAA, and MX record lookups across 5 domains — including one intentionally fake domain to test error handling. Logs response time, TTL, and resolved records for every query. Prints a final results summary with success rate.

| Property | Value |
|---|---|
| Script name | `dns_script_traffic_generator.py` |
| Runs on | Ubuntu 192.168.6.129 |
| Queries | 15 total (5 domains × 3 record types) |
| Library | `dnspython` |
| Traffic captured | Port 53 UDP via tcpdump |

---

## Workflow

### Step 1 — Write script on Windows in VS Code, then SCP to Ubuntu

```powershell
scp "C:\Users\thako\Nokia-Network-lab\scripts\dns_script_traffic_generator.py" ubuntu@192.168.6.129:/home/ubuntu/Nokia-Network-lab/scripts
```

### Step 2 — SSH into Ubuntu and install the DNS library

```bash
ssh ubuntu@192.168.6.129
pip install dnspython --break-system-packages
```

### Step 3 — Start tcpdump capturing in Window 1

```bash
sudo tcpdump -i ens33 port 53 -w dns_script_capture.pcap
```

### Step 4 — Run the script in Window 2

```bash
cd ~/Nokia-Network-lab/scripts
python3 dns_script_traffic_generator.py
```

### Step 5 — Stop tcpdump (Ctrl+C), transfer pcap to Kali, open in Wireshark

```bash
scp ubuntu@192.168.6.129:~/dns_script_capture.pcap /home/kali/Desktop/dns_script_capture.pcap
wireshark /home/kali/Desktop/dns_script_capture.pcap
```

### Step 6 — Commit and push to GitHub

```bash
cd ~/Nokia-Network-lab
git add .
git commit -m "Add Script 2 DNS test script"
git push
```

---

## Results

- 15 queries fired automatically across 5 domains and 3 record types
- `nokia.com` and `github.com` returned `NO ANSWER` on AAAA — correct behavior, neither domain has IPv6 configured
- `nonexistentdomain12345abc.com` returned `NXDOMAIN` on all 3 record types — error handling confirmed working
- 10 successful / 5 expected failures / 66.7% success rate

---

## Screenshots

### Script Terminal Output
*Python script running on Ubuntu — 15 automated DNS queries with SUCCESS, NO ANSWER, NXDOMAIN results and final summary*

![Script 2 Terminal Output](../results/script2_terminal_output.png)

---

### Wireshark — Full DNS Traffic Capture (Packet List)
*tcpdump capture of all 15 DNS queries on port 53 — UDP transport visible, NXDOMAIN responses for fake domain visible in packet list*

![Script 2 Wireshark Packet List](../results/script2_wireshark_packetlist.png)

---

### Wireshark — Successful DNS Response Expanded
*google.com A record response with Answers section expanded — Type A, TTL 5s, resolved IP address visible*

![Script 2 Wireshark Success Response](../results/script2_wireshark_success_response.png)

---

### Wireshark — NXDOMAIN Response Expanded
*nonexistentdomain12345abc.com response packet expanded — NXDOMAIN flag visible in DNS layer confirming domain does not exist*

![Script 2 Wireshark NXDOMAIN](../results/script2_wireshark_nxdomain.png)

---

## Interview Talking Point

*"Script 2 automates DNS resolution across multiple domains and record types using Python's dnspython library. It logs response times, TTL values, and handles four distinct DNS error conditions — NXDOMAIN, NoAnswer, Timeout, and general exceptions. Running it while tcpdump captures on port 53 generates a pcap showing exactly the same DNS query-response pairs as manual dig commands, proving the script produces real, analyzable network traffic. Nokia's application identification systems use DNS behavior — query patterns, TTL anomalies, NXDOMAIN rates — as primary signals for traffic classification and DDoS detection."*

---

*Script 2 Completed: May 8, 2026*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Script 3 — PCAP Analyzer*
