# Nokia Network Lab — Phase 3: Script 1 — HTTP Traffic Generator
## Python Automation | Automated HTTP Traffic Generation + Wireshark Validation
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE

---

## JD Mapping

Script 1 directly addresses two Nokia JD requirements: *"Develop automated test cases in a Linux-based regression environment to validate application signatures"* and *"Python proficiency (essential) for automation, test development, and debugging."* Manually running curl once or twice is a test. Running a script that sends 20 measured, timestamped, logged requests automatically — and reports a pass/fail summary — is a test case. This is the distinction between ad-hoc testing and professional automated regression testing.

---

## Script Overview

| Property | Value |
|---|---|
| Script name | `script1_http_generator.py` |
| Location on Ubuntu | `~/Nokia-Network-lab/scripts/` |
| Target | `http://192.168.6.129:8080` |
| Requests sent | 20 |
| Delay between requests | 1 second |
| Total run time | ~20 seconds |
| Nokia JD mapping | Automated test cases, Python proficiency, test environments |

**What the script does in plain English:** Sends 20 HTTP GET requests to the Ubuntu HTTP server one per second, measures how long each one takes in milliseconds, logs a timestamped SUCCESS or FAIL line for every request, catches and logs connection errors and timeouts gracefully without crashing, then prints a final summary of total sent, succeeded, and failed.

---

## Bugs Found and Fixed Before Running

Three bugs were identified during code review before execution — exactly the kind of pre-run validation a Nokia test engineer performs.

| Bug | What Was Wrong | Fix Applied |
|---|---|---|
| Typo in module name | `datatime` instead of `datetime` | Corrected spelling |
| Variable name mismatch | Stored result in `resp0nse` (zero) but read from `response` (letter o) | Unified to `response` throughout |
| Function never called | `send_requests()` was defined but never triggered | Added `if __name__ == "__main__": send_requests()` at bottom |

---

## File Transfer — Windows VS Code to Ubuntu

Script was written and edited in VS Code on Windows, then transferred to Ubuntu using scp from PowerShell.

```powershell
# Run in PowerShell on Windows — transfers script into Ubuntu scripts folder
scp "C:\path\to\script1_http_generator.py" ubuntu@192.168.6.129:~/Nokia-Network-lab/scripts/
```

**Why scp and not copy-paste:** scp transfers the exact file over an encrypted SSH connection. No formatting gets lost, no invisible characters get introduced, and the file lands exactly where it needs to be for execution and Git tracking.

**Confirm file arrived on Ubuntu:**
```bash
ls ~/Nokia-Network-lab/scripts/
```

Expected output:
```
script1_http_generator.py
```

---

## Pre-Run Setup — Start HTTP Server and tcpdump

Two terminal windows are needed before running the script. Open two separate PowerShell windows, both SSH'd into Ubuntu.

**Window 1 — Start HTTP server:**
```bash
python3 -m http.server 8080
```

**Window 2 — Start traffic capture:**
```bash
sudo tcpdump -i ens33 port 8080 -w ~/Nokia-Network-lab/pcaps/script1_capture.pcap
```

Leave both running. Open a third window to run the script.

---

## Script Execution

```bash
cd ~/Nokia-Network-lab/scripts/
python3 script1_http_generator.py
```

**Install requests library first if not already installed:**
```bash
pip3 install requests --break-system-packages
```

**Expected terminal output:**
```
Starting HTTP Traffic Generator
Target: http://192.168.6.129:8080
Sending 20 requests with 1s delay
--------------------------------------------------
[2026-05-04 14:32:01] Request 1: SUCCESS | Status: 200 | Time: 3.41ms
[2026-05-04 14:32:02] Request 2: SUCCESS | Status: 200 | Time: 2.87ms
...
[2026-05-04 14:32:20] Request 20: SUCCESS | Status: 200 | Time: 3.12ms
--------------------------------------------------
RESULTS: 20 requests sent
  SUCCESS: 20
  FAILED:  0
```

After script finishes, stop tcpdump with Ctrl+C in Window 2.

---

## Transfer pcap to Kali for Wireshark Analysis

```bash
# Run on Kali
scp ubuntu@192.168.6.129:~/Nokia-Network-lab/pcaps/script1_capture.pcap /home/kali/Desktop/script1_capture.pcap

# Open in Wireshark
wireshark /home/kali/Desktop/script1_capture.pcap
```

---

## Wireshark Analysis — What to Look For

Apply display filter `http` in Wireshark to isolate HTTP traffic. You should see 20 complete HTTP transaction cycles — one per script request. Each cycle contains the TCP three-way handshake, the GET request, the 200 OK response, and the connection teardown. The metronomic spacing between transactions (approximately 1 second apart) is visible in the timestamps — this is the automated timing created by `time.sleep(1)` in the script, distinguishing it from manual curl traffic.

---

## Screenshots to Take

Take all screenshots from Wireshark on Kali after opening `script1_capture.pcap`.

**Screenshot 1 — Full packet list overview**
Show the complete Wireshark packet list with all 20 request cycles visible. The Protocol column should show TCP and HTTP alternating. The Time column should show ~1 second spacing between each HTTP transaction. This proves the script ran 20 automated requests with consistent timing.

![Screenshot 1 — Wireshark full packet list showing 20 HTTP transaction cycles with 1-second spacing]()

---

**Screenshot 2 — Single HTTP GET request packet detail**
Click on one GET request packet. Show the middle pane expanded to reveal the HTTP layer with `GET / HTTP/1.1` and the Host header. This confirms the script generated real HTTP GET requests identical in structure to a browser or curl request.

![Screenshot 2 — Wireshark packet detail showing HTTP GET request with headers expanded]()

---

**Screenshot 3 — HTTP 200 OK response packet detail**
Click on the corresponding 200 OK response packet. Show the middle pane with the HTTP layer expanded showing `HTTP/1.0 200 OK`, the Server banner (`SimpleHTTP Python/3.14.4`), and Content-Type. This is the server banner Nokia application identification algorithms read to classify traffic.

![Screenshot 3 — Wireshark packet detail showing HTTP 200 OK response with Server banner visible]()

---

**Screenshot 4 — Script terminal output**
Screenshot of the Ubuntu terminal showing the full script output — all 20 timestamped request lines and the final RESULTS summary showing 20 sent, 20 SUCCESS, 0 FAILED. This is your proof of automated test execution.

![Screenshot 4 — Ubuntu terminal showing full script output with 20 SUCCESS lines and final summary]()

---

## Git — Commit and Push

```bash
cd ~/Nokia-Network-lab
git add .
git commit -m "Add Script 1 HTTP traffic generator and Phase 3 notes"
git push
```

---

## Key Concepts Introduced in Script 1

**requests library:** Third-party Python library that handles all HTTP connection management, request formatting, and response parsing. The professional standard for HTTP automation in Python.

**try/except:** Python's error handling structure — attempt risky operations (network calls) and catch specific failure types (ConnectionError, Timeout) without crashing the script. Essential for any production test tool.

**time.time():** Returns current Unix timestamp in seconds. Subtracting two measurements gives precise elapsed time. Multiplying by 1000 converts to milliseconds for human-readable latency reporting.

**time.sleep():** Pauses script execution for a specified number of seconds. Creates realistic traffic spacing that looks like real application behaviour rather than a flood.

**global keyword:** Tells Python that a variable name inside a function refers to the one defined at the top of the file, not a new local copy. Required whenever a function needs to update a counter or shared state.

---

## Interview Talking Point — Script 1

*"I built a Python HTTP traffic generator that sends 20 automated GET requests to a test server with configurable timing and full error handling. Each request is timestamped, measured in milliseconds, and logged as SUCCESS or FAIL. The script catches connection errors and timeouts gracefully without crashing — exactly the behaviour required in a regression test environment. I captured the resulting traffic with tcpdump and verified in Wireshark that the packet-level structure matched expected HTTP behaviour including TCP handshakes, GET requests, 200 OK responses with server banners, and metronomic 1-second request spacing from the automated timing."*

---

*Script 1 Completed: May 2026*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Script 2 — DNS Test Script*
