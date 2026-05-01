# Nokia Network Lab — Phase 1 Complete
## HTTP Server + Packet Capture + Traffic Analysis
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE

---

## Lab Environment

| Component | Details | Purpose |
|---|---|---|
| Kali Linux VM | kali-linux-2025.2 | Traffic generation, Wireshark, attack simulation |
| Ubuntu Server VM | Ubuntu 26.04 LTS (kt_ubuntu_server) | HTTP/DNS test servers, tcpdump, Python scripts |
| Windows Desktop | Host laptop | SSH client, curl traffic generation |
| Ubuntu IP | 192.168.6.129 | Target server address |
| Kali IP | 192.168.6.130 | Attacker/analyst machine |
| Ubuntu Username | ubuntu | SSH login user |
| Network | VMnet8 (NAT) | Both VMs on same subnet |

---

## Phase 1 Objective
**Nokia JD Mapping:** *"Set up and configure test servers/services (e.g., HTTP servers, DNS servers) to create realistic test environments"* and *"Verify and analyze application detection mechanisms along with network behaviors"*

The goal of Phase 1 was to:
1. Run a real HTTP server on Ubuntu
2. Generate HTTP traffic from an external machine
3. Capture that traffic with tcpdump
4. Transfer the pcap file to Kali
5. Analyze the packets visually in Wireshark

This is the foundational workflow that Nokia engineers use to validate application identification algorithms — generate traffic, capture it, verify it looks correct at the packet level.

---

## Tools Used in Phase 1

| Tool | Version | Purpose |
|---|---|---|
| Python 3 | 3.14.4 | Run built-in HTTP server module |
| tcpdump | 4.99.6 | Capture live network traffic to pcap file |
| Wireshark | Latest | Visual packet analysis |
| scp | Built-in SSH | Securely transfer pcap between VMs |
| curl | Windows PowerShell | Generate HTTP requests as test traffic |

---

## SSH — Connecting to Ubuntu from Windows

```powershell
ssh ubuntu@192.168.6.129
```

**What it does:** Creates an encrypted tunnel between your Windows machine and Ubuntu VM. Everything you type travels through that tunnel securely over port 22.

**Why it matters for Nokia:** Real servers never have a GUI. Engineers always connect remotely over SSH to run commands, deploy scripts, and debug. This is the standard professional workflow.

**Why copy-paste works in PowerShell SSH but not VMware console:** The VMware VM console is a raw display of the VM screen with no clipboard bridge to Windows. When you SSH via PowerShell, you're in a Windows terminal so right-click paste works normally.

**Pro tip for interviews:** In production environments, SSH keys (public/private key pairs) replace passwords for security. For our lab, password auth is sufficient.

---

## Step 1 — Start HTTP Test Server on Ubuntu

```bash
python3 -m http.server 8080
```

**Breaking down every part:**

| Part | Explanation |
|---|---|
| `python3` | Use Python version 3 |
| `-m` | Run a built-in Python module as a script instead of a .py file |
| `http.server` | Python's built-in HTTP server module — no configuration needed |
| `8080` | Port to listen on. Port 80 is standard HTTP but requires root. Port 8080 is the standard alternative any user can bind to |

**What happens when it runs:**
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/)
```
The `0.0.0.0` means it's listening on ALL network interfaces — any machine that can reach your Ubuntu VM can send HTTP requests to it. It serves the contents of the current directory as a file listing.

**Nokia JD relevance:** This is exactly what the JD means by "set up and configure test servers." In Nokia's lab, testers spin up HTTP servers, DNS servers, and custom application servers to generate realistic traffic for testing their identification algorithms.

**Interview talking point:** *"I set up a Python HTTP test server on Ubuntu to simulate realistic application traffic for protocol analysis and packet capture validation."*

---

## Step 2 — Capture Traffic with tcpdump

```bash
sudo tcpdump -i ens33 port 8080 -w http_capture2.pcap
```

**Breaking down every part:**

| Part | Explanation |
|---|---|
| `sudo` | tcpdump needs root privileges to access raw network interface |
| `tcpdump` | Packet capture tool — terminal equivalent of Wireshark |
| `-i ens33` | Network interface to capture on — `ens33` is Ubuntu VM's virtual NIC |
| `port 8080` | Capture filter — only capture packets on port 8080, ignore everything else |
| `-w http_capture2.pcap` | Write captured packets to file instead of printing to screen |

**What the output means:**
```
tcpdump: listening on ens33, link-type EN10MB (Ethernet), snapshot length 262144 bytes
```
- `listening on ens33` — Confirmed capturing on the right interface
- `link-type EN10MB (Ethernet)` — Standard Ethernet network type
- `snapshot length 262144` — Maximum bytes captured per packet (essentially the full packet)

**After stopping with Ctrl+C:**
```
120 packets captured
120 packets received by filter
0 packets dropped by kernel
```
- `120 packets captured` — Successfully saved to pcap file
- `packets received by filter = packets captured` — No packets were missed
- `0 packets dropped` — Critical for Nokia work. Drops happen when traffic arrives faster than the system can process it. In DDoS scenarios, you'd see drops because the flood overwhelms the capture buffer. Detecting that pattern is part of what Nokia's mitigation systems do.

**How to find your network interface name:**
```bash
ip a
```
Look for the interface that has your VM's IP address (192.168.6.129). That's the interface name to use with `-i`.

---

## Step 3 — Generate HTTP Traffic

```powershell
# From Windows PowerShell — run 8-10 times
curl http://192.168.6.129:8080
```

**Why Windows curl shows a security warning:** PowerShell's `curl` is actually an alias for `Invoke-WebRequest`, Microsoft's own HTTP tool. It shows a security warning because it parses HTML. The real curl on Linux/Kali silently fetches content with no warnings. In the lab, just type `Y` to continue.

**Understanding the HTTP response:**

```
StatusCode        : 200
StatusDescription : OK
Server            : SimpleHTTP/0.6 Python/3.14.4
Content-Type      : text/html; charset=utf-8
RawContent        : HTTP/1.0 200 OK
```

| Field | Value | What it means |
|---|---|---|
| StatusCode | 200 | Request succeeded — "OK" |
| Server | SimpleHTTP/0.6 Python/3.14.4 | Server banner identifying the software |
| Content-Type | text/html | Type of content being returned |
| HTTP version | HTTP/1.0 | Protocol version used |

**HTTP Status Codes — Essential for Nokia interviews:**
- `200` — OK, request succeeded
- `301/302` — Redirect
- `404` — Not Found
- `500` — Server Error
- `403` — Forbidden

Nokia's application identification algorithms look at status code patterns as part of traffic classification. Abnormal patterns (all 404s, sudden 500s) can indicate attack traffic.

**Server Banners and Application Identification:**
The `Server: SimpleHTTP/0.6 Python/3.14.4` field is a server banner — a signature that identifies what software is running. This is exactly what Nokia's application identification algorithms analyze. Different applications have completely different banners — Apache, Nginx, IIS, custom apps all look different. Nokia's NetGuard systems read these signatures along with traffic patterns, port numbers, protocol behaviors, and packet timing to classify what application is generating the traffic. This is the core of what the Nokia JD is about.

---

## Step 4 — Verify pcap File Saved Correctly

```bash
ls -lh http_capture2.pcap
```

**Breaking down the command:**

| Part | Explanation |
|---|---|
| `ls` | List files in current directory |
| `-l` | Long format — show size, date, permissions, owner |
| `-h` | Human readable — show KB/MB instead of raw bytes |

**Sample output:**
```
-rw-r--r-- 1 tcpdump tcpdump 1.7K Apr 27 20:18 http_test.pcap
```

| Part | Meaning |
|---|---|
| `-rw-r--r--` | File permissions — owner can read/write, others can only read |
| `tcpdump tcpdump` | Owner and group — tcpdump drops privileges after opening interface (security feature called privilege dropping) |
| `1.7K` | File size — 1.7 kilobytes for 10 packets |
| `Apr 27 20:18` | Timestamp of last write |

**Privilege dropping concept:** tcpdump needs root to open the network interface, but once it's capturing it switches to a less privileged `tcpdump` user. This means even if someone exploited tcpdump, they wouldn't have full root access. This is standard security practice in Linux — request only the privileges you need, for only as long as you need them.

---

## Step 5 — Transfer pcap from Ubuntu to Kali

```bash
# Run this on KALI, not Ubuntu
scp ubuntu@192.168.6.129:~/desktop/http_capture2.pcap /home/kali/Desktop/http_capture2.pcap
```

**Breaking down every part:**

| Part | Explanation |
|---|---|
| `scp` | Secure Copy Protocol — file transfer over SSH |
| `ubuntu@192.168.6.129` | Same user@address format as SSH |
| `:~/desktop/http_capture2.pcap` | Colon separates address from file path on remote machine |
| `/home/kali/Desktop/http_capture2.pcap` | Destination path on Kali |

**Why scp runs on Kali not Ubuntu:** scp works by connecting TO the remote machine and pulling the file FROM it. Since we want the file on Kali, we run the command on Kali and tell it to reach out to Ubuntu.

**Important Linux concept — home directories:**
- Regular users: `/home/username/` (e.g., `/home/ubuntu/`, `/home/kali/`)
- Root user: `/root/` (completely separate location)
- `~` always expands to YOUR current user's home directory
- When logged in as root, `~` = `/root/`, not `/home/kali/`
- Always use full paths (`/home/kali/Desktop/`) when there's any ambiguity about which user you're running as

**Network requirement:** Both VMs must be on the same VMnet (VMnet8 NAT) for scp to work. If they're on different VMnets, you'll get "Network is unreachable."

---

## Step 6 — Open pcap in Wireshark

```bash
wireshark /home/kali/Desktop/http_capture2.pcap
```

---

## Step 7 — Wireshark Analysis

### Wireshark Interface Layout

**Top pane — Packet List:** Each row is one packet. Shows timestamp, source IP, destination IP, protocol, length, and brief description. Bird's eye view of all traffic.

**Middle pane — Packet Details:** Click any packet to see every protocol layer expanded as a tree. From bottom to top: Ethernet → IP → TCP → HTTP. This is the OSI model made visible in real captured data.

**Bottom pane — Raw Bytes:** Hex and ASCII representation of every byte in the packet. Used when reverse engineering unknown protocols — exactly what Nokia engineers do with new application signatures.

---

### The TCP Three-Way Handshake

This is one of the most fundamental concepts in networking and it appears clearly in your capture.

```
Packet 11: [SYN]         192.168.6.1   → 192.168.6.129   "I want to connect"
Packet 12: [SYN, ACK]    192.168.6.129 → 192.168.6.1     "OK, I'm ready"
Packet 13: [ACK]         192.168.6.1   → 192.168.6.129   "Great, connected"
```

**Why it matters for Nokia:** DDoS SYN flood attacks exploit this handshake by sending millions of SYN packets without ever sending the final ACK. This leaves the server with thousands of half-open connections, consuming memory until it crashes. Nokia's mitigation systems detect this by monitoring the ratio of SYN packets to SYN-ACK responses and flagging sources that never complete the handshake. You can see normal SYN→SYN-ACK→ACK patterns in your pcap — in a SYN flood you'd see thousands of SYNs with no corresponding ACKs.

---

### The Complete HTTP Transaction

One complete HTTP request/response cycle in your pcap looks like this:

```
[SYN]           — TCP connection initiated
[SYN, ACK]      — Server accepts connection  
[ACK]           — Connection established
GET / HTTP/1.1  — Client requests the page
[ACK]           — Server acknowledges request
HTTP/1.0 200 OK — Server sends response with HTML
[ACK]           — Client acknowledges response
[FIN, ACK]      — Client initiates connection close
[ACK]           — Server acknowledges close
```

**TCP Flags explained:**

| Flag | Meaning | When you see it |
|---|---|---|
| SYN | Synchronize — initiate connection | Start of every TCP connection |
| ACK | Acknowledge — confirming receipt | Almost every packet after the first SYN |
| FIN | Finish — close connection gracefully | End of normal connections |
| RST | Reset — close connection abruptly | Error conditions, rejected connections |
| PSH | Push — send data immediately | When HTTP response data is being sent |

---

### Key Packet Details to Note

**Packet showing HTTP GET request:**
- Source: `192.168.6.1` (Windows machine)
- Destination: `192.168.6.129` (Ubuntu server)
- Protocol: HTTP
- Info: `GET / HTTP/1.1`

**Packet showing HTTP 200 OK response:**
- Source: `192.168.6.129` (Ubuntu server)
- Destination: `192.168.6.1` (Windows machine)
- Protocol: HTTP
- Info: `HTTP/1.0 200 OK (text/html)`
- Length: 666 bytes (includes HTML content)

**What the lengths tell you:** The GET request packet is small (~217 bytes) because it's just headers. The 200 OK response is larger (~666 bytes) because it includes the actual HTML page content. In application identification, packet size distributions are one of the signatures used to classify traffic — different applications have characteristic size patterns.

---

## Key Networking Concepts Covered in Phase 1

### Ports
Ports are like apartment numbers — the IP address gets you to the right building (server), the port gets you to the right service. Standard ports: 80=HTTP, 443=HTTPS, 22=SSH, 53=DNS, 8080=alternative HTTP.

### pcap Files
pcap (packet capture) files are recordings of raw network traffic containing every packet — headers, payload, timing — exactly as it appeared on the wire. tcpdump creates them, Wireshark opens them. Both use the same file format. These files are the primary evidence used when debugging application identification failures at Nokia.

### Network Interfaces
Every machine has one or more network interfaces (NICs). In VMware, Ubuntu's virtual NIC is named `ens33`. The `lo` (loopback) interface at `127.0.0.1` is a virtual internal interface — traffic sent to it never leaves the machine. Always specify the correct interface with `-i` in tcpdump or you'll miss traffic.

### NAT Networking in VMware
NAT (Network Address Translation) lets VMs share your laptop's internet connection while living on their own private virtual network. VMnet8 is VMware's dedicated NAT switch. For two VMs to communicate, they must both be on the same VMnet. Ubuntu and Kali are both on VMnet8 (NAT), giving them IPs in the `192.168.6.x` range from VMware's built-in DHCP server.

### The OSI Model in Real Traffic
Your pcap shows the OSI model in action on every single packet:
- **Layer 2 (Data Link):** Ethernet — MAC addresses (`00:0c:29:5a:5e:e0`)
- **Layer 3 (Network):** IP — IP addresses (`192.168.6.1` → `192.168.6.129`)
- **Layer 4 (Transport):** TCP — ports, sequence numbers, flags (SYN, ACK, FIN)
- **Layer 7 (Application):** HTTP — GET requests, 200 OK responses, headers

Nokia's application identification works primarily at Layer 7 — it looks at the application-level behavior to classify traffic. But to understand Layer 7, you need to understand the layers below it, which is exactly what this phase built.

---

## Commands Quick Reference — Phase 1

| Command | What It Does |
|---|---|
| `ssh ubuntu@192.168.6.129` | SSH into Ubuntu VM from Windows/Kali |
| `python3 -m http.server 8080` | Start HTTP test server on port 8080 |
| `sudo tcpdump -i ens33 port 8080 -w capture.pcap` | Capture HTTP traffic to file |
| `sudo tcpdump -i ens33 port 8080` | Capture and print HTTP traffic live (no file) |
| `ls -lh filename.pcap` | Check pcap file size and permissions |
| `scp user@IP:~/remote/file.pcap /local/path/file.pcap` | Transfer pcap from remote machine |
| `wireshark /path/to/file.pcap` | Open pcap in Wireshark |
| `ip a` | Show all network interfaces and IP addresses |
| `cd ~` | Go to home directory from anywhere |
| `ls ~/` | List files in home directory |

---

## Interview Talking Points — Phase 1

**If asked about Linux experience:**
*"I set up an Ubuntu Server VM and configured it as a test server environment, running HTTP services and capturing traffic using tcpdump from the command line."*

**If asked about network traffic analysis:**
*"I captured HTTP traffic using tcpdump in a Linux test environment, transferred the pcap to Wireshark, and analyzed the complete TCP three-way handshake, HTTP GET requests, 200 OK responses including server banners, and connection teardown sequences."*

**If asked about test environments:**
*"I built a two-VM lab with Kali as the client and Ubuntu as the server, both on the same NAT network, to generate realistic HTTP traffic for packet-level analysis and protocol validation."*

**If asked about DDoS concepts:**
*"I understand how SYN flood attacks exploit the TCP three-way handshake — by sending SYNs without completing the ACK, attackers leave half-open connections that exhaust server memory. I've seen normal SYN-SYN/ACK-ACK patterns in my Wireshark captures and understand what anomalous patterns indicating a flood would look like."*

---

## What's Next — Phase 2

**Phase 2: Protocol Analysis**
- DNS traffic capture and analysis
- TCP handshake deep dive
- HTTPS/TLS traffic observation
- QUIC protocol basics
- RTP traffic (VoIP)

**Start Phase 2 with:**
```bash
# On Ubuntu — install DNS tools
sudo apt install dnsutils -y

# Generate DNS query traffic
dig google.com
nslookup nokia.com

# Capture DNS traffic (port 53)
sudo tcpdump -i ens33 port 53 -w dns_capture.pcap
```

---

*Phase 1 Completed: April 27, 2026*
*Next Session: Start with Phase 2 — DNS Traffic Analysis*
*Continue message for new chat: "Continuing Nokia lab — Phase 1 complete. Starting Phase 2 DNS analysis. Ubuntu IP 192.168.6.129, Kali IP 192.168.6.130."*
