# Nokia Network Lab — Phase 2: Protocol Analysis
## Complete Notes | DNS · HTTPS/TLS · QUIC · RTP
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE

---

## JD Mapping

Phase 2 directly addresses two of the most specific bullets in the Nokia JD. "Verify and analyze application detection mechanisms along with network behaviors involving QUIC, HTTPS, RTP and other protocols" is covered completely — every named protocol was captured and analyzed in Wireshark. "Strong understanding of computer networking protocols, including TCP/IP, DHCP, ARP, DNS" is covered through hands-on DNS capture and deep UDP vs TCP comparison. The overarching theme of Phase 2 is understanding how Nokia's application identification systems classify traffic — and the answer in every protocol section is the same: they read the metadata and behavioral signatures that remain visible even when payload is encrypted.

---

## Lab Environment

Ubuntu Server VM at 192.168.6.129 (username: ubuntu) acted as the traffic generator and capture host throughout Phase 2. Kali Linux VM at 192.168.6.130 acted as the receiving host for RTP and the browser host for QUIC generation. Both VMs sit on VMnet8 NAT in VMware, meaning all inter-VM traffic flows through the same virtual switch and is visible to tcpdump on either interface. tcpdump requires sudo because it puts the interface into **promiscuous mode** — the interface reads every packet on the segment regardless of destination address, not just packets addressed to itself. This is why tcpdump can capture Kali's browser traffic from Ubuntu's interface without specifying Kali's IP.

---

## Protocol 1 — DNS

### What DNS Is and Why Nokia Cares

DNS (Domain Name System) is the internet's directory service. Every application connection begins with a DNS query to resolve a hostname to an IP address. Nokia's application identification systems treat DNS as a primary signal — the domain being queried often reveals what application is generating traffic before a single byte of that app's actual data has been sent. DNS flood attacks, NXDOMAIN floods, and DNS amplification are also major DDoS vectors that Nokia's mitigation systems defend against.

### How DNS Works at the Packet Level

DNS uses UDP port 53 for standard queries because UDP's connectionless model — fire a question, receive an answer, no handshake — is fast and lightweight for the billions of DNS lookups that happen every second globally. DNS falls back to TCP port 53 only when responses exceed 512 bytes, which typically happens during zone transfers between DNS servers. The entire DNS exchange for a standard A record query takes two packets: one query from client to server, one response from server to client.

### DNS Record Types — What You Need to Know

An **A record** maps a domain to an IPv4 address and is the most common query type. An **AAAA record** maps a domain to an IPv6 address — the response packet is 12 bytes larger than an A record response because IPv6 addresses are 16 bytes vs IPv4's 4 bytes, a measurable difference that shows up in packet size analysis. An **MX record** specifies the mail server for a domain. An **SOA (Start of Authority) record** is returned when you query for a record type that doesn't exist — rather than returning nothing, the DNS server tells you who is authoritative for that domain. When querying `nokianetworks.com MX`, the response returned an SOA showing Nokia uses Cloudflare for DNS management. A **PTR record** is reverse DNS — resolving an IP back to a hostname — frequently seen in network scanning and reconnaissance, which Nokia's detection systems flag accordingly.

### The Transaction ID — DNS Anti-Spoofing Mechanism

Every DNS query contains a randomly generated 16-bit Transaction ID. The DNS server must echo the exact same ID in its response. The client discards any response where the Transaction ID doesn't match its outstanding query. This prevents basic DNS spoofing where an attacker fires a forged response to redirect a client to a malicious IP. Port randomisation (ephemeral source ports) adds a second layer — an attacker must guess both the correct Transaction ID and the correct ephemeral port simultaneously to successfully spoof a response. Nokia's detection systems can identify DNS spoofing attempts by monitoring for patterns of Transaction ID mismatches.

### TTL and Fast-Flux DNS

The TTL (Time to Live) field in a DNS response tells resolvers how long to cache the answer before querying again. Google's `google.com` A record has a TTL of 5 seconds — deliberately short so their load balancers can shift traffic between servers continuously. From a Nokia security perspective, abnormally low TTLs combined with rapid IP rotation is the signature of **fast-flux DNS**, a technique attackers use to make malicious domains nearly impossible to block. A C2 (command-and-control) server using fast-flux DNS swaps its IP every few seconds, so by the time a defender blocklists one IP, the domain has already moved. Nokia's detection systems flag domains with sub-10-second TTLs combined with IP churn as suspected malicious infrastructure.

### Ephemeral Ports and the Full Port Model

Every outgoing DNS query uses a randomly chosen source port from the OS ephemeral range — on Linux this is 32768–60999. You observed this directly: google.com used port 44307, nokia.com used 45997, github.com used 36951. The randomisation is intentional for security — predictable ports would make spoofing easier. The full port space on any system is 0–65535, defined by the 16-bit port field in TCP and UDP headers. Well-known ports (0–1023) require root to bind to and map to standard services: 22=SSH, 53=DNS, 80=HTTP, 443=HTTPS. This is why Phase 1 used port 8080 — binding below 1024 requires root. Registered ports (1024–49151) are associated with known applications but don't require root. Ephemeral ports (49152–65535 per IANA, 32768–60999 on Linux) are temporarily assigned by the OS to outgoing connections and released when the connection ends.

### DNS Capture Commands

```bash
# Install dig
sudo apt install dnsutils -y

# Query A record (IPv4)
dig google.com

# Query AAAA record (IPv6)
dig google.com AAAA

# Query MX record (mail server)
dig google.com MX

# Query a domain that returns SOA (no MX configured)
dig nokianetworks.com MX

# Capture DNS traffic
sudo tcpdump -i ens33 port 53 -w dns_capture.pcap

# Read pcap without resolving hostnames
sudo tcpdump -r dns_capture.pcap -n

# Transfer to Kali
scp ubuntu@192.168.6.129:~/dns_capture.pcap /home/kali/Desktop/dns_capture.pcap

# Open in Wireshark
wireshark /home/kali/Desktop/dns_capture.pcap
```

### DNS Wireshark Analysis

With 3 dig queries you captured exactly 6 packets — 2 per query, one outbound query and one inbound response. The Protocol column shows DNS throughout. The layer stack in the middle pane reads Ethernet → IP → UDP → DNS, confirming the connectionless transport. The Transaction ID matches between query and response packets. The Answers section of each response contains the Resource Record with Type, Class (always IN for Internet), TTL, and the resolved IP address.

### ![DNS Wireshark Screenshot]
*Caption: Wireshark showing 6-packet DNS capture with google.com response selected, Answers section expanded showing Type A record, TTL 5 seconds, and resolved IP address. Note UDP transport — no handshake visible unlike Phase 1 HTTP/TCP capture.*

---

## Protocol 2 — HTTPS/TLS

### What HTTPS Is

HTTPS is not a separate protocol — it is HTTP traffic carried inside a TLS (Transport Layer Security) tunnel, running over TCP port 443. TLS encrypts the application payload completely, making the HTTP requests and responses inside unreadable to anyone capturing the traffic. However the TLS handshake that establishes the encrypted session happens before encryption activates, and this handshake contains critical plaintext metadata that Nokia's application identification systems read to classify encrypted traffic without ever decrypting it.

### The TLS Handshake Sequence

Your capture of `curl https://www.google.com` produced 85 packets. The first three are the familiar TCP three-way handshake — SYN, SYN-ACK, ACK — establishing the TCP connection before TLS even begins. Packet 4 is the **Client Hello**, the first TLS message, sent in plain text because no encryption has been negotiated yet. Packet 7 is the **Server Hello** plus Certificate, where Google responds and proposes cipher suite parameters. Packet 11 is **Change Cipher Spec** — both sides signal they're switching to encrypted mode. Every subsequent packet is **Application Data** — the encrypted payload that is completely unreadable without the session keys.

### The SNI Field — Nokia's Primary HTTPS Classification Signal

Inside the Client Hello packet, buried in the Extensions section under `server_name`, is the **SNI (Server Name Indication)** field. This field contains the hostname the client wants to connect to — `www.google.com` — in completely plain text, even though the subsequent traffic will be encrypted. SNI exists because a single server IP can host thousands of different HTTPS websites, and the server needs to know which certificate to present before encryption starts. Nokia's application identification systems read the SNI field to classify encrypted HTTPS traffic — they can identify that traffic is destined for google.com, nokia.com, or any other domain without decrypting a single byte of the payload. This is called **passive TLS fingerprinting**.

### TLS Fingerprinting Beyond SNI

The Client Hello contains far more than just the SNI. It also includes the list of cipher suites the client supports (30 suites in your capture), the TLS versions supported (TLS 1.3 and 1.2), the supported elliptic curve groups, the signature algorithms, and various other extensions. The specific combination of these fields — which cipher suites are listed, in what order, which extensions are present — creates a unique fingerprint for each client application. Chrome has a measurably different TLS fingerprint than Firefox, which is different from curl, which is different from a mobile app. Nokia's systems build and maintain databases of these fingerprints to classify not just what domain is being contacted but what application is generating the traffic.

### Why Application Data Is Unreadable

After the Change Cipher Spec packet, every Application Data packet in Wireshark shows as a wall of random hex bytes in the raw data pane with no readable ASCII text. The actual HTML, JavaScript, and all page content of google.com is in those packets — you saw it all dumped as plain text when curl printed it to the terminal — but after TLS encryption it is indistinguishable from random noise without the session keys. This is TLS working exactly as designed.

### HTTPS Capture Commands

```bash
# Generate HTTPS traffic
curl https://www.google.com

# Capture HTTPS traffic — use port 443, not hostname (Anycast IP rotation causes hostname filter to miss packets)
sudo tcpdump -i ens33 port 443 -w tls_capture.pcap

# Transfer to Kali
scp ubuntu@192.168.6.129:~/tls_capture.pcap /home/kali/Desktop/tls_capture.pcap

# Open in Wireshark
wireshark /home/kali/Desktop/tls_capture.pcap
```

**Important lesson learned:** Using `host google.com` as the tcpdump filter captured 0 packets because Google's Anycast infrastructure resolves to different IPs on every query. tcpdump resolved the hostname to one IP when it started but curl connected to a different IP seconds later. Always filter by port number for HTTPS captures, never by hostname.

### ![HTTPS/TLS Wireshark Screenshot]
*Caption: Wireshark showing TLS capture with Client Hello selected (packet 4). Middle pane shows Extension: server_name (len=19) name=www.google.com highlighted — the SNI field visible in plaintext before encryption activates. Packet list shows full handshake sequence: TCP SYN/SYN-ACK/ACK followed by Client Hello, Server Hello, Change Cipher Spec, then encrypted Application Data packets.*

---

## Protocol 3 — QUIC

### What QUIC Is

QUIC is a modern transport protocol developed by Google and standardised as RFC 9000 in 2021. It runs over **UDP port 443** — not TCP port 443 like HTTPS. This is the most important single fact about QUIC: it replaces TCP entirely rather than layering on top of it. QUIC combines what previously required three separate layers — TCP for reliable delivery, TLS for encryption, HTTP/2 for multiplexing — into a single unified protocol. HTTP/3, the latest version of the HTTP protocol, runs exclusively over QUIC. When your browser loads google.com today, a large proportion of that traffic is HTTP/3 over QUIC, not HTTP/2 over TLS/TCP.

### Why QUIC Exists — The Problem It Solves

TCP was designed in 1974 and has fundamental limitations for modern web traffic. Every TCP connection requires a three-way handshake before any data moves, and every TLS session requires an additional 1-2 round trips for the TLS handshake on top of that. For a short-lived connection — fetching a small resource — the handshake overhead can be longer than the actual data transfer. QUIC reduces connection establishment to a single round trip for new connections and zero round trips for resumed connections (0-RTT), dramatically reducing latency for users on mobile networks where round-trip times are high.

TCP also has **head-of-line blocking**: if one packet is lost, all subsequent data in the stream waits for retransmission even if it belongs to completely independent requests. QUIC eliminates this by multiplexing independent streams within a single connection so that packet loss in one stream doesn't affect others.

### Connection IDs — QUIC's Key Innovation for Nokia

In TCP, a connection is uniquely identified by the four-tuple of source IP, source port, destination IP, and destination port. If any of those change — for example when a mobile phone switches from WiFi to cellular mid-session — the TCP connection breaks and must be restarted from scratch. QUIC uses **Connection IDs** instead: a DCID (Destination Connection ID) and SCID (Source Connection ID) embedded in every packet. As long as the Connection ID is preserved, the QUIC connection survives complete changes in the underlying network path. Your capture showed DCIDs like `840f337508861a62` persisting across packets even as different Google server IPs appeared in the destination column. Nokia's traffic classification systems track these Connection IDs to follow QUIC flows across the network even when the underlying IP addresses change — something impossible with TCP-based connection tracking.

### QUIC Handshake and Encryption

Your capture showed the QUIC handshake sequence clearly: Initial packets (carrying cryptographic setup material), Handshake packets (completing the TLS-equivalent negotiation), then Protected Payload packets (KP0 = Key Phase 0, the first encryption key). Unlike TLS over TCP where the Client Hello is entirely in plain text, QUIC encrypts its handshake packets at a basic level from the very start — the Initial packets use a fixed key derived from the Connection ID, providing weak but non-zero protection. Full forward-secret encryption is established by the Handshake phase. This means even less plaintext metadata is visible in QUIC than in TLS/TCP, making Nokia's classification work harder but the Connection ID and statistical traffic analysis compensate.

### The 952-Packet Capture Explained

Loading a single Google homepage generated 952 QUIC packets. This is because a modern webpage is assembled from dozens of separate resources — HTML, JavaScript bundles, CSS, fonts, analytics, tracking pixels — all fetched simultaneously. QUIC's stream multiplexing handles all of these over a single UDP connection with no per-resource connection overhead, which is why the packet count is high but the total time is fast. The multiple destination IPs (`34.107.243.93`, `142.250.69.138`, etc.) reflect Google's Anycast infrastructure routing different resource types to different server clusters simultaneously.

### QUIC Capture Commands

```bash
# QUIC runs on UDP port 443 — filter specifically for UDP to exclude TCP/443 HTTPS
sudo tcpdump -i ens33 udp port 443 -w quic_capture.pcap

# Generate QUIC traffic — open Firefox on Kali and browse to https://www.google.com
# (curl does not support HTTP/3/QUIC without special compilation flags)

# Transfer to Kali
scp ubuntu@192.168.6.129:~/quic_capture.pcap /home/kali/Desktop/quic_capture.pcap

# Open in Wireshark and apply display filter
wireshark /home/kali/Desktop/quic_capture.pcap
# Then type in filter bar: quic
```

**Note on curl and HTTP/3:** curl 8.18.0 on Ubuntu 26.04 does not include HTTP3 support — it was not compiled with the required libraries. This is a realistic lab constraint that would be encountered in real Nokia environments. The browser-based approach using Firefox on Kali generates authentic QUIC traffic from a real HTTP/3 implementation.

### ![QUIC Wireshark Screenshot]
*Caption: Wireshark showing 952-packet QUIC capture with quic display filter applied. Packet list shows Initial, Handshake, and Protected Payload (KP0) phases. Middle pane shows Ethernet → IP → UDP → QUIC IETF layer stack confirming UDP transport. Connection IDs (DCID/SCID) visible in Info column. Note absence of TCP — QUIC replaces TCP entirely rather than layering on top of it.*

---

## Protocol 4 — RTP

### What RTP Is

RTP (Real-time Transport Protocol) is the protocol that carries live audio and video across IP networks. Every VoIP call, video conference, and live stream uses RTP to deliver the actual media data. RTP runs over UDP — like DNS, it prioritises low latency over guaranteed delivery, because a retransmitted voice packet arriving 200ms late is useless for real-time conversation. RTP is explicitly named in the Nokia JD because Nokia's traffic classification and DDoS mitigation systems must handle VoIP traffic at scale, both to protect it from attacks and to correctly classify it for QoS prioritisation.

### How RTP Was Generated in the Lab

ffmpeg was used to generate a real G.711 mu-law audio stream — a 1000Hz sine wave test tone for 10 seconds — from Ubuntu (192.168.6.129) to Kali (192.168.6.130) on UDP port 5004. The G.711 mu-law codec (also written as PCMU or g711U) is the codec that has carried telephone calls globally since the 1960s. Every landline call, every PSTN network, every VoIP gateway bridging internet calls to the telephone network uses G.711. Generating G.711 traffic in the lab means you generated the exact same codec format that carries billions of phone calls daily.

```bash
# Install ffmpeg
sudo apt install ffmpeg -y

# Start capture in second window before running ffmpeg
sudo tcpdump -i ens33 udp port 5004 -w rtp_capture.pcap

# Generate 10-second G.711 RTP stream to Kali
ffmpeg -f lavfi -i "sine=frequency=1000:duration=10" -ar 8000 -acodec pcm_mulaw -f rtp rtp://192.168.6.130:5004

# Transfer to Kali
scp ubuntu@192.168.6.129:~/rtp_capture.pcap /home/kali/Desktop/rtp_capture.pcap

# Open in Wireshark
wireshark /home/kali/Desktop/rtp_capture.pcap

# Wireshark won't auto-detect RTP on port 5004 — manually decode:
# Right-click any packet → Decode As → add UDP port 5004 = RTP → OK

# View RTP stream analysis
# Telephony → RTP → RTP Streams
```

### The SDP Block — VoIP Call Setup

When ffmpeg started streaming it printed an SDP (Session Description Protocol) block to the terminal. SDP is the standardised format real VoIP systems use to negotiate call parameters before RTP begins. The SDP showed the media type (audio), port (5004), protocol (RTP/AVP), codec (payload type 0 = G.711 PCMU), and bitrate (64 kbps). In a real VoIP system this SDP would be exchanged via SIP (Session Initiation Protocol) before the RTP stream starts — Nokia's systems analyze both SIP signaling and RTP media streams together to fully classify and monitor VoIP traffic.

### RTP Packet Structure — What Makes It Unique

Your Wireshark RTP analysis revealed 432 packets captured over the 10-second stream — approximately 43 packets per second, one packet every ~20 milliseconds. This rate is not accidental. G.711 at 8000 samples per second with 20ms packets means each packet carries 160 audio samples (8000 ÷ 50 = 160). The **RTP timestamp** increments by exactly 160 on every packet, reflecting this mathematical relationship. Nokia's classification systems use this timestamp regularity as a primary RTP signature — web browsing and file transfer traffic have bursty, irregular packet timing; RTP has a metronomic heartbeat that is immediately recognisable.

The **Sequence Number** increments by 1 on every packet. Receivers use this to detect lost packets — if sequence 4116 arrives followed by 4118, packet 4117 was lost. The **SSRC (Synchronisation Source identifier)** — `0x85d12484` in your capture — is a random 32-bit number assigned to the stream, used to distinguish multiple speakers in a conference call. The capture showed 0 packets lost and a mean jitter of 1.23ms — near-perfect quality, which makes sense for a local VM-to-VM stream with no network congestion.

### Jitter and Packet Loss — The Nokia QoS Connection

Jitter is variation in packet inter-arrival time. Your capture showed min jitter 1.23ms and max jitter 23.14ms. For context, ITU-T G.114 recommends maximum one-way delay of 150ms for good voice quality, and jitter above 50ms causes audible degradation. Nokia's NetGuard and other QoS systems monitor RTP streams in real time and can prioritise VoIP traffic to keep jitter and loss below acceptable thresholds. A sudden spike in jitter or packet loss on an RTP stream is a signal that either network congestion or an active attack is degrading call quality.

### RTP in DDoS Context

RTP floods are a specific DDoS attack vector — sending massive volumes of UDP packets mimicking RTP format to overwhelm VoIP infrastructure. Nokia's mitigation systems distinguish legitimate RTP streams (consistent packet rate, valid sequence numbers, proper SSRC, G.711/G.729/Opus payload types) from RTP flood traffic (irregular timing, sequential or zeroed SSRCs, abnormal payload sizes) using exactly the packet-level signatures you examined in your capture.

### ![RTP Streams Analysis Screenshot]
*Caption: Wireshark RTP Streams window showing detected stream: Source 192.168.6.129:53528 → Destination 192.168.6.130:5004, SSRC 0x85d12484, Payload g711U, 432 packets, 0 (0.0%) lost, Mean Delta 0.12ms, Mean Jitter 1.23ms. This is the engineer's view of VoIP stream quality metrics — the same metrics Nokia's QoS systems monitor in production.*

### ![RTP Packet Detail Screenshot]
*Caption: Wireshark packet list showing RTP protocol decoded with full RTP header visible in middle pane: Version RFC 1889, Payload type ITU-T G.711 PCMU, incrementing Sequence Numbers, Timestamps incrementing by 160 (= 20ms of audio at 8000Hz sample rate), and SSRC 0x85d12484. Green filter bar shows Wireshark display filter isolating this specific RTP stream.*

---

## Phase 2 — Protocol Comparison Summary

This table captures the key architectural differences across every protocol you captured. Understanding these differences at the packet level is what the Nokia JD means by "strong understanding of computer networking protocols."

| Property | DNS | HTTPS/TLS | QUIC | RTP |
|---|---|---|---|---|
| Transport | UDP | TCP | UDP | UDP |
| Port | 53 | 443 | 443 | 5004 (varies) |
| Handshake | None | TCP + TLS (2 round trips) | QUIC Initial+Handshake (1 round trip) | None |
| Encryption | None | TLS (after handshake) | Built-in from start | None (plaintext payload) |
| Plaintext metadata visible | Full query/response | SNI in Client Hello | Connection IDs in Initial packets | Full RTP header + payload |
| Packet pattern | Request-response pairs | Bursty, variable size | Bursty, high volume | Metronomic, fixed interval |
| Nokia classification signal | Domain name, query type, TTL | SNI, TLS fingerprint | Connection ID, QUIC fingerprint | Codec type, packet rate, SSRC |
| DDoS relevance | Amplification, NXDOMAIN flood | HTTPS flood | QUIC flood | RTP flood, jitter attacks |

---

## Phase 2 — Screenshots for GitHub Repository

These are the screenshots to include in your GitHub README for Phase 2, in order:

**Screenshot 1 — DNS Wireshark:** Full Wireshark window showing the 6-packet DNS capture, with a response packet selected and the Answers section expanded showing the Resource Record fields (Type A, Class IN, TTL 5, IP address). Shows UDP transport in the middle pane.

**Screenshot 2 — HTTPS/TLS Client Hello:** Full Wireshark window showing the TLS capture with packet 4 (Client Hello) selected, middle pane expanded to show the `Extension: server_name name=www.google.com` field highlighted. Packet list shows the full SYN/SYN-ACK/ACK/ClientHello/ServerHello/ChangeCipherSpec/ApplicationData sequence.

**Screenshot 3 — QUIC Capture:** Full Wireshark window with `quic` display filter applied, showing 952 packets all labelled QUIC in the Protocol column. Packet list shows Initial, Handshake, and Protected Payload phases. Middle pane shows the UDP → QUIC IETF layer stack with Connection ID visible.

**Screenshot 4 — RTP Streams Window:** Wireshark RTP Streams analysis window showing the detected g711U stream with all quality metrics — 432 packets, 0% loss, jitter values.

**Screenshot 5 — RTP Packet Detail:** Wireshark main window with RTP display filter applied, showing full RTP header decoded in the middle pane with sequence numbers, timestamps, SSRC, and G.711 PCMU payload type all labelled.

---

## Phase 2 — Interview Talking Points

**If asked about DNS:**
"I captured DNS traffic using tcpdump filtering on port 53 and analyzed the query and response structure in Wireshark. I observed how DNS uses UDP for connectionless resolution, the Transaction ID matching mechanism that prevents spoofing, TTL values down to 5 seconds for Google which relates directly to fast-flux DNS attacks, and the difference between A, AAAA, MX, and SOA record types. I understand how Nokia's detection systems use anomalous DNS patterns — low TTLs, NXDOMAIN floods, TXT record abuse — to identify malicious traffic."

**If asked about HTTPS and encrypted traffic classification:**
"I captured HTTPS traffic and analyzed the TLS handshake in Wireshark. The key insight is that even though the payload is completely encrypted, the TLS Client Hello packet is sent in plain text and contains the SNI field — the hostname the client wants to connect to — which Nokia's application identification systems use to classify encrypted traffic without decrypting it. Beyond SNI, the combination of cipher suites, TLS version, and extension ordering creates a unique TLS fingerprint per application that Nokia's systems use for more granular classification."

**If asked about QUIC:**
"I captured QUIC traffic by generating it through a browser on my Kali VM while tcpdump captured on Ubuntu's interface. QUIC runs over UDP port 443 and replaces TCP entirely — it integrates reliable delivery, multiplexing, and encryption into a single protocol, reducing connection setup from two round trips for HTTPS over TCP to one round trip. The key structural difference from TLS over TCP is QUIC's Connection IDs, which allow connections to survive network path changes like WiFi to cellular handoffs. Nokia's systems track these Connection IDs to follow QUIC flows even when underlying IP addresses change."

**If asked about RTP and VoIP:**
"I generated a real G.711 mu-law RTP stream using ffmpeg, captured it with tcpdump, and analyzed it in Wireshark's built-in RTP analyzer. I observed the metronomic packet timing — one packet every 20 milliseconds, with the RTP timestamp incrementing by exactly 160 per packet reflecting 160 audio samples at 8000Hz. The capture showed 432 packets with 0% loss and sub-2ms mean jitter. I understand how Nokia's QoS systems use these RTP metrics — packet rate consistency, sequence number continuity, jitter and loss statistics — to both classify VoIP traffic and monitor call quality in real time."

**If asked about UDP vs TCP:**
"I've captured both protocols extensively. TCP provides reliable ordered delivery through sequence numbers, acknowledgments, and retransmission, but requires a three-way handshake before any data moves and maintains per-connection state that DDoS SYN floods exploit. UDP is connectionless — no handshake, no guaranteed delivery, no per-connection state — which makes it faster and lower overhead, which is why DNS, QUIC, and RTP all use it. The tradeoff is that UDP is easier to spoof and amplify, which is why DNS amplification and UDP floods are major DDoS attack vectors that Nokia's mitigation systems specifically handle."

**If asked about DDoS and the protocols:**
"Each protocol I studied has specific DDoS implications. DNS is used for amplification attacks — a small spoofed query generates a response 28-54x larger directed at the victim. HTTPS floods exhaust server TLS handshake processing capacity. QUIC floods exploit the stateless nature of UDP. RTP floods overwhelm VoIP infrastructure. In each case Nokia's detection systems look for behavioral anomalies in the traffic signatures — abnormal query rates, malformed handshakes, irregular packet timing — rather than just volume thresholds, because sophisticated attackers specifically craft their traffic to look legitimate until it's at scale."

---

## Phase 2 — Commands Master Reference

```bash
# DNS
sudo apt install dnsutils -y
dig google.com
dig google.com AAAA
dig google.com MX
dig nokianetworks.com MX
sudo tcpdump -i ens33 port 53 -w dns_capture.pcap
sudo tcpdump -r dns_capture.pcap -n

# HTTPS/TLS
curl https://www.google.com
sudo tcpdump -i ens33 port 443 -w tls_capture.pcap

# QUIC
sudo tcpdump -i ens33 udp port 443 -w quic_capture.pcap
# Generate traffic: open Firefox on Kali → https://www.google.com

# RTP
sudo apt install ffmpeg -y
sudo tcpdump -i ens33 udp port 5004 -w rtp_capture.pcap
ffmpeg -f lavfi -i "sine=frequency=1000:duration=10" -ar 8000 -acodec pcm_mulaw -f rtp rtp://192.168.6.130:5004

# Transfer any pcap to Kali
scp ubuntu@192.168.6.129:~/[filename].pcap /home/kali/Desktop/[filename].pcap

# Open in Wireshark
wireshark /home/kali/Desktop/[filename].pcap

# Wireshark display filters
dns
tls
quic
rtp
```

---

*Phase 2 Completed: May 1, 2026*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Phase 3 — Python Automation & Test Scripts*
