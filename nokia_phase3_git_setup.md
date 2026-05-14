# Nokia Network Lab — Phase 3: Git Setup & GitHub Portfolio
## Complete Notes | Git · GitHub · Source Control · Windows-to-Ubuntu File Transfer · VS Code Setup
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE (Git Setup & Repository Initialization)

---

## JD Mapping

This section directly addresses the Nokia JD requirement: *"Experience with Git or similar source control systems."* Every command in this section is real professional Git workflow — the same workflow Nokia engineers use daily to version-control test scripts, automation code, and lab tooling. By the end of this setup, a fully structured GitHub portfolio repository exists at https://github.com/Kanhay-Thakore/Nokia-Network-lab, containing Phase 1 and Phase 2 lab notes, with the folder structure ready to receive all Phase 3 Python scripts. The entire workflow — configuring Git identity, initializing a local repository, linking it to a remote, and pushing files — mirrors exactly what is expected of a junior developer contributing to a team codebase.

---

## Lab Environment

| Component | Details | Purpose |
|---|---|---|
| Ubuntu Server VM | Ubuntu 26.04 LTS at 192.168.6.129 | Git repository host, script execution environment |
| Kali Linux VM | kali-linux-2025.2 at 192.168.6.130 | Secondary analyst machine |
| Windows Desktop | Host laptop (C:\Users\thako) | VS Code development, Git push to GitHub |
| GitHub Repository | https://github.com/Kanhay-Thakore/Nokia-Network-lab | Remote portfolio repository (public) |
| Git Version (Ubuntu) | 2.53.0 | Installed on Ubuntu during Phase 0 |
| Git Version (Windows) | 2.54.0 | Installed on Windows for VS Code workflow |
| Python Version (Ubuntu) | 3.14.4 | Script execution environment on Ubuntu |
| Python Version (Windows) | 3.12.10 | Local syntax checking and IntelliSense in VS Code |
| VS Code | Latest | Script development IDE on Windows |
| Network | VMnet8 NAT | Both VMs on same subnet |

---

## Why Git Matters for Nokia

Git is the industry-standard version control system used by virtually every professional software and network engineering team. In Nokia's context, Git serves several purposes: test scripts and automation code are committed to shared repositories so the entire team can collaborate, track changes, and roll back to a previous working version if a new script breaks something. Every bug fix, new test case, and feature addition is a commit — a permanent record of what changed, when, and by whom. When the Nokia JD lists "Experience with Git or similar source control systems," they are looking for candidates who understand this workflow and can contribute to a shared codebase from day one without needing to be taught the basics.

---

## Where Python Scripts Are Written and Run

Before touching Git, it is important to establish the correct development workflow for this lab. The scripts in Phase 3 need to read pcap files, send HTTP requests to the Ubuntu server, and analyze packet-level data — all of which lives on the Linux VMs. Python 3.14.4 is already installed on Ubuntu for execution. The correct professional workflow is:

```
VS Code on Windows (write + syntax check)
        ↓
git push to GitHub
        ↓
Ubuntu VM — git pull
        ↓
Run script on Ubuntu against the lab
        ↓
Capture results and screenshots for portfolio
```

This mirrors the professional workflow Nokia engineers use daily — develop code in a proper IDE, version-control it through Git, deploy it onto a Linux server, and execute it against real infrastructure. Writing scripts in `nano` directly on the server is avoided because it has no syntax highlighting, no error detection, no autocomplete, and no debugger — making every typo and indentation error invisible until the script crashes at runtime.

**Why Git and not SCP:** SCP transfers the file to Ubuntu but leaves no version history, no commit messages, no portfolio evidence, and no rollback capability. If a script breaks after 10 changes, SCP gives you no way to identify which change caused the problem. Git gives you a permanent record of every change, visible to Nokia interviewers on your public GitHub portfolio. The extra cost is exactly 4 commands — `git add .`, `git commit -m "message"`, `git push` on Windows, and `git pull` on Ubuntu.

---

## Windows Development Environment Setup

This section covers the complete setup of the Windows development environment — installing Git, cloning the repository, setting up VS Code, and installing Python — so that script development follows a professional IDE-to-GitHub-to-Linux workflow rather than writing code in a terminal text editor.

### Step W1 — Install Git on Windows

Git is the version control software. On Ubuntu it was already installed during Phase 0. On Windows it needs to be installed separately so the VS Code terminal can push to GitHub directly.

Download from:
```
https://git-scm.com/download/win
```

Run the installer with all default options — click Next through every screen. After installation, **fully close and reopen PowerShell** so the new PATH entry takes effect.

Verify installation:

```powershell
git --version
```

**Expected output:**
```
git version 2.54.0.windows.1
```

**Why close and reopen PowerShell:** When an installer adds a new entry to the Windows PATH, running programs don't see the change until they restart. PowerShell reads the PATH only when it launches — an already-open window holds the old PATH in memory and will not find Git until it is closed and reopened.

---

### Step W2 — Clone the Repository onto Windows

Navigate to your home folder first:

```powershell
cd ~
```

`~` on Windows PowerShell means your user home directory — `C:\Users\thako`. Always clone projects here, never in system folders like `C:\Windows\system32`.

Clone the repository:

```powershell
git clone https://github.com/Kanhay-Thakore/Nokia-Network-lab
```

| Part | Explanation |
|---|---|
| `git clone` | Downloads a complete copy of the remote repository — every file, every folder, every commit in the history — onto your local machine |
| `https://github.com/Kanhay-Thakore/Nokia-Network-lab` | The URL of your GitHub repository |

**What clone does that SCP does not:** `git clone` doesn't just copy files — it copies the entire Git history and permanently links this local folder to GitHub as its remote origin. From this moment, every `git push` from this folder goes directly to your GitHub repository. SCP has no such link.

**Expected output:**
```
Cloning into 'Nokia-Network-lab'...
remote: Enumerating objects: 4, done.
remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), 18.24 KiB | 18.24 MiB/s, done.
```

A new folder `Nokia-Network-lab` is now at `C:\Users\thako\Nokia-Network-lab` — permanently linked to GitHub.

---

### Step W3 — Open the Project in VS Code

Navigate into the cloned folder:

```powershell
cd Nokia-Network-lab
```

Open VS Code with this folder as the project root:

```powershell
code .
```

| Part | Explanation |
|---|---|
| `code` | The VS Code command-line launcher — installed automatically when VS Code is installed |
| `.` | "Open VS Code using the current directory as the project root" — VS Code loads with your entire Nokia-Network-lab folder visible in the left sidebar |

VS Code opens showing the project folder structure in the Explorer panel on the left — `scripts/`, `nokia_phase1_complete.md`, `nokia_phase2_complete.md`. This is the project view Nokia developers work in daily.

---

### Step W4 — Install VS Code Extensions

Two extensions are required for Python development in VS Code. Open the Extensions panel:

```
Ctrl + Shift + X
```

Install these two, in order:

| Extension | Publisher | Downloads | Purpose |
|---|---|---|---|
| Python | Microsoft | 216M+ | Syntax highlighting, IntelliSense, error detection for .py files |
| Pylance | Microsoft | 183M+ | Language server — real-time type checking, accurate autocomplete, function signatures |

**Python extension** gives VS Code the ability to understand Python syntax — code turns colourful, errors get underlined in red, and the file is recognised as Python rather than plain text.

**Pylance extension** is the intelligence layer on top — it analyses your code in real time as you type, tells you what arguments a function expects, catches type mismatches before you run the script, and provides far more accurate autocomplete than the base Python extension alone.

Search each by name, click the result published by Microsoft, click Install.

---

### Step W5 — Install Python 3.12 on Windows

VS Code needs a local Python installation for IntelliSense and syntax checking. The scripts will execute on Ubuntu (Python 3.14.4), but VS Code needs a local interpreter to provide real-time error detection while writing.

Download Python 3.12.x from:
```
https://www.python.org/downloads/release/python-3128/
```

Scroll to the Files section → click **Windows installer (64-bit)**.

**CRITICAL — on the first installer screen, check this box before clicking anything:**
```
☑ Add python.exe to PATH
```

This checkbox adds Python to the Windows PATH automatically. If missed, Python installs correctly but Windows cannot find it by name — requiring manual PATH repair.

Click **Install Now**.

**Why Python 3.12 and not 3.14:** Python 3.14 is the latest version installed on Ubuntu but is too new for stable library support on Windows. Python 3.12 is the current stable LTS-equivalent — every library used in Phase 3 (`requests`, `scapy`, `dpkt`) is fully tested and supported on 3.12.

---

### Step W6 — Fix Windows App Execution Aliases

Windows ships with fake "python" shortcuts in the Microsoft Store that intercept the `python` command and redirect to the Store instead of launching real Python. These must be disabled.

Navigate to:
```
Windows Settings → Apps → Advanced app settings → App execution aliases
```

Or search: **App execution aliases** in the Start menu.

Find these two entries and toggle both **OFF**:

| Entry | Toggle |
|---|---|
| App Installer — python.exe | OFF |
| App Installer — python3.exe | OFF |

Without disabling these, typing `python` in any terminal will open the Microsoft Store regardless of whether Python 3.12 is installed.

---

### Step W7 — Fix Python PATH Permanently

If `python --version` still fails after installation, add Python to the PATH manually through Windows System Properties:

Press **Windows + R** → type `sysdm.cpl` → Enter → **Advanced** tab → **Environment Variables**.

In the **User variables** section, double-click **Path** → click **New** twice and add:

```
C:\Users\thako\AppData\Local\Programs\Python\Python312
C:\Users\thako\AppData\Local\Programs\Python\Python312\Scripts
```

Click OK → OK → OK. Then **fully close and reopen VS Code**.

**Why fully closing VS Code is required:** VS Code reads the PATH only at launch. Any terminal opened inside VS Code inherits the PATH that existed when VS Code started. Adding Python to the PATH while VS Code is running has no effect on existing terminals — a full restart is required.

**Verify Python is working:**

```powershell
python --version
```

**Expected output:**
```
Python 3.12.10
```

---

### Step W8 — Install the requests Library on Windows

The `requests` library is used in Script 1 and must be installed into Windows Python 3.12 for VS Code's IntelliSense to recognise it without red underlines:

```powershell
python -m pip install requests
```

| Part | Explanation |
|---|---|
| `python` | Calls Python 3.12 on Windows |
| `-m pip` | Runs pip (Python's package manager) as a module — this guarantees pip installs into the exact same Python that the `python` command uses, avoiding environment mismatch |
| `install requests` | Downloads and installs the requests library from PyPI (Python Package Index) |

**Verify the library installed correctly:**

```powershell
python -c "import requests; print(requests.__version__)"
```

**Expected output:**
```
2.33.1
```

`-c` means "run this short Python code directly from the command line." This one-liner imports requests and prints its version — if a version number appears, the library is fully accessible.

---

### Step W9 — Create the Scripts Folder and First Script File in VS Code

In VS Code's Explorer panel (left sidebar), right-click on `NOKIA-NETWORK-LAB` → **New Folder** → name it:

```
scripts
```

Then right-click the `scripts` folder → **New File** → name it:

```
http_traffic_generator.py
```

**Why creating the folder in VS Code and not on Ubuntu first:** Git does not track empty folders — they are completely invisible to Git. The `scripts/`, `pcaps/`, and `results/` folders created on Ubuntu during Phase 0 were never pushed to GitHub because they were empty. When the Windows clone pulled from GitHub, those folders did not come down. Creating the `scripts` folder in VS Code and immediately putting a file inside it means Git will track it the moment we push.

**No conflict with Ubuntu's empty scripts folder:** Git only conflicts when two sides have different content in the same file. An empty folder on Ubuntu versus a new script file in the same folder is not a conflict — Git simply adds the new file to the empty folder when Ubuntu pulls.

---

### Complete Windows Development Environment — Summary

| Component | Version | Status | Purpose |
|---|---|---|---|
| Git for Windows | 2.54.0 | ✅ Installed | Push scripts to GitHub from VS Code terminal |
| Repo cloned | Nokia-Network-lab | ✅ Linked to GitHub | `C:\Users\thako\Nokia-Network-lab` permanently linked to remote origin |
| VS Code | Latest | ✅ Open with project | Script development IDE |
| Python extension | Microsoft | ✅ Installed | Syntax highlighting, .py file recognition |
| Pylance extension | Microsoft | ✅ Installed | Real-time type checking, IntelliSense |
| Python 3.12.10 | 3.12.10 | ✅ Installed | Local interpreter for VS Code |
| requests library | 2.33.1 | ✅ Installed | HTTP library for Script 1 |
| App execution aliases | python.exe, python3.exe | ✅ Disabled | Prevents Microsoft Store from hijacking python command |
| PATH | System Environment Variables | ✅ Fixed permanently | Python 3.12 accessible from any terminal |

---

## Step 1 — Confirm Python is Ready on Ubuntu

SSH into Ubuntu from PowerShell first:

```powershell
ssh ubuntu@192.168.6.129
```

Then confirm Python is installed and at the correct version:

```bash
python3 --version
```

**Expected output:**
```
Python 3.14.4
```

| Part | Explanation |
|---|---|
| `python3` | Calls Python version 3 — always use `python3` on Ubuntu, never just `python` which may point to Python 2 |
| `--version` | Prints the installed version number and exits |

**Why this matters for Nokia:** Python is listed as *essential* (not optional) in the Nokia JD. Confirming the version before writing any code is good professional practice — scripts written for Python 3.14 may use features unavailable in older versions. Always verify your environment before developing.

---

## Step 2 — Confirm Git is Installed

Git was installed during Phase 0. Verify it is present and check the version:

```bash
git --version
```

**Expected output:**
```
git version 2.53.0
```

| Part | Explanation |
|---|---|
| `git` | Calls the Git command-line tool |
| `--version` | Prints installed version and exits |

---

## Step 3 — Configure Git Identity

Git stamps every commit (save point) with the author's name and email. This must be configured before making any commits. Run these two commands, using the GitHub account username and email:

```bash
git config --global user.name "Kanhay-Thakore"
git config --global user.email "thakorekanhay70@gmail.com"
```

| Part | Explanation |
|---|---|
| `git config` | The Git command for reading and writing configuration settings |
| `--global` | Apply this setting to every Git repository on this machine — you only run this once per machine, not once per project |
| `user.name` | The key being set — Git's setting for author name |
| `"Kanhay-Thakore"` | The value — your GitHub username, which will appear on every commit in the repository history |
| `user.email` | The key for author email |

**Confirm the settings saved correctly:**

```bash
git config --list
```

`git config --list` prints every Git configuration setting currently active on the machine. You should see `user.name=Kanhay-Thakore` and `user.email=thakorekanhay70@gmail.com` in the output.

**Expected output:**
```
user.name=Kanhay-Thakore
user.email=thakorekanhay70@gmail.com
```

**Nokia interview relevance:** In a team environment, the author identity on commits is how code review and blame tracking works — when a bug is introduced, the team can look at the commit history and see exactly who changed what and when. Configuring this correctly from the start is baseline professional practice.

---

## Step 4 — Create the Project Folder Structure

Create the project directory and all subfolders on Ubuntu. These folders mirror the repository structure that will appear on GitHub:

```bash
mkdir -p ~/Nokia-Network-lab/scripts
mkdir -p ~/Nokia-Network-lab/pcaps
mkdir -p ~/Nokia-Network-lab/results
cd ~/Nokia-Network-lab
pwd
ls
```

| Command | Explanation |
|---|---|
| `mkdir` | "Make directory" — creates a folder |
| `-p` | "Parent" flag — creates all parent directories too if they don't exist. So if `Nokia-Network-lab` doesn't exist yet, it creates that first, then creates `scripts` inside it, all in one command |
| `~/Nokia-Network-lab/scripts` | `~` is a shortcut that always means your home directory (`/home/ubuntu`). This creates a `scripts` subfolder inside the project folder |
| `~/Nokia-Network-lab/pcaps` | Creates the `pcaps` subfolder where packet capture files will be stored |
| `~/Nokia-Network-lab/results` | Creates the `results` subfolder for test output and screenshots |
| `cd ~/Nokia-Network-lab` | "Change directory" — moves you inside the project folder, like double-clicking to open it |
| `pwd` | "Print working directory" — confirms exactly where you are in the filesystem |
| `ls` | "List" — shows everything inside the current folder, confirming all three subfolders were created |

**Expected output from pwd and ls:**
```
/home/ubuntu/Nokia-Network-lab
pcaps  results  scripts
```

**Repository folder structure:**
```
Nokia-Network-lab/
├── scripts/       ← Python automation scripts go here
├── pcaps/         ← Packet capture files go here
└── results/       ← Test output and screenshots go here
```

---

## Step 5 — Initialize a Git Repository

Turn the project folder into a Git repository:

```bash
git init
```

`git init` means "initialize" — it creates a hidden `.git` folder inside your current directory. That hidden folder is where Git stores its entire history, all commit snapshots, branch information, and configuration. You will never need to touch it directly, but its presence is what makes this folder a "repository" rather than just a regular folder. You only ever run `git init` once per project.

**Expected output:**
```
Initialized empty Git repository in /home/ubuntu/Nokia-Network-lab/.git/
```

Git may also print hints about branch naming. This is addressed in the next step.

---

## Step 6 — Rename Branch to Main

By default Git creates a branch called `master`. GitHub uses `main` as its default. Rename the branch so they match, which prevents conflicts when pushing:

```bash
git branch -m main
```

| Part | Explanation |
|---|---|
| `git branch` | The command for managing branches in Git |
| `-m` | "Move" flag — renames a branch |
| `main` | The new name for the branch |

A branch is like a timeline of your project. The `main` branch is the primary timeline where all finished, working code lives. Keeping the local and remote branch names identical (`main` on both Ubuntu and GitHub) is essential for clean push and pull operations.

Also suppress the branch name warning permanently for all future repositories on this machine:

```bash
git config --global init.defaultBranch main
```

This tells Git that every new repository initialized on this machine from now on should use `main` as the default branch name automatically.

**Confirm the current state:**

```bash
git status
```

`git status` is one of the most frequently used Git commands — it shows which branch you are on, which files are being tracked, which have been modified, and which are staged for the next commit. Run it constantly to understand what state your repository is in.

**Expected output:**
```
On branch main
No commits yet
nothing to commit (create/copy files and use "git add" to track)
```

This output means: you are on the `main` branch, no save points have been recorded yet (which is correct — the repo was just created), and there are no files here yet for Git to track.

---

## Step 7 — Create a GitHub Personal Access Token

GitHub no longer accepts account passwords for Git operations over HTTPS. Instead it uses a Personal Access Token (PAT) — a long randomly-generated string that acts as a password replacement specifically for terminal operations.

**Steps to generate a PAT:**

1. Go to GitHub in your browser
2. Click your profile photo (top right) → **Settings**
3. Scroll all the way down the left sidebar → click **Developer settings**
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Note field: `ubuntu-lab`
7. Expiration: **90 days**
8. Under Select scopes: check the **repo** checkbox — this automatically checks all sub-scopes beneath it (repo:status, repo_deployment, public_repo, repo:invite, security_events)
9. Scroll down → click **Generate token**
10. **Copy the token immediately** — GitHub displays it only once. It begins with `ghp_`

**Important:** Do not check `workflow`, `write:packages`, `delete:packages`, or any other scope. The `repo` scope alone is sufficient for all push and pull operations on your repositories.

Save the token temporarily in Notepad on Windows. It will be embedded in the remote URL in the next step.

**Why PATs exist:** Plain passwords over HTTPS are a security risk because if intercepted they grant full account access. A PAT can be scoped to only the permissions it needs (in this case, repository access only), can be revoked independently without changing your account password, and expires automatically. This is standard security practice — least privilege access for the shortest time needed.

---

## Step 8 — Create the GitHub Repository

On GitHub in your browser, create a new repository with these exact settings:

| Setting | Value |
|---|---|
| Repository name | `Nokia-Network-lab` |
| Description | `Linux network testing lab — HTTP, DNS, TLS, QUIC, RTP, Python automation` |
| Visibility | Public |
| Add README | No — leave unchecked |
| Add .gitignore | No — leave unchecked |
| Choose a license | No — leave unchecked |

**Why leave it completely empty:** If you initialize the GitHub repo with a README, GitHub creates an initial commit on its side. When you then try to push from Ubuntu, Git sees two different histories (one on GitHub, one local) and throws a conflict error. Starting empty means GitHub has no commits, so your first push from Ubuntu becomes the one true history with no conflicts.

Click **Create Repository**. GitHub shows an empty repo page with the URL at the top.

---

## Step 9 — Link Local Repository to GitHub

Connect your Ubuntu project folder to the GitHub repository. The remote URL embeds your GitHub username and Personal Access Token so Git never needs to prompt for credentials interactively:

```bash
git remote add origin https://Kanhay-Thakore:YOUR_TOKEN_HERE@github.com/Kanhay-Thakore/Nokia-Network-lab.git
```

Replace `YOUR_TOKEN_HERE` with the actual token from your Notepad.

| Part | Explanation |
|---|---|
| `git remote add` | Adds a connection to a remote repository |
| `origin` | The conventional nickname given to the primary GitHub remote. Instead of typing the full URL every time you push, you just say `origin` |
| `https://Kanhay-Thakore:TOKEN@github.com/...` | The URL format with credentials embedded. `username:token` before the `@` symbol tells Git who you are without an interactive prompt |

**Confirm the connection saved correctly:**

```bash
git remote -v
```

`git remote -v` means "show all remote connections verbosely" — the `-v` flag (verbose) prints the full URL next to each remote name. You should see `origin` listed twice.

**Expected output:**
```
origin  https://Kanhay-Thakore:ghp_xxxx...@github.com/Kanhay-Thakore/Nokia-Network-lab.git (fetch)
origin  https://Kanhay-Thakore:ghp_xxxx...@github.com/Kanhay-Thakore/Nokia-Network-lab.git (push)
```

Two entries appear because Git separates the fetch URL (for downloading from GitHub) and the push URL (for uploading to GitHub). Both point to the same place — this is normal.

---

## Step 10 — Transfer MD Files from Windows to Ubuntu

The Phase 1 and Phase 2 MD files live on Windows. Transfer them to Ubuntu using `scp` — the same Secure Copy Protocol used in Phase 1 to transfer pcap files, just in the opposite direction (Windows to Ubuntu instead of Ubuntu to Kali).

Open a **new PowerShell window** (keep the Ubuntu SSH window open separately). Run:

```powershell
scp "C:\Users\thako\OneDrive\Desktop\Github\NOKIA job tasks project\nokia_phase1_complete.md" ubuntu@192.168.6.129:~/Nokia-Network-lab/
```

Then transfer the Phase 2 file:

```powershell
scp "C:\Users\thako\OneDrive\Desktop\Github\NOKIA job tasks project\nokia_phase2_complete.md" ubuntu@192.168.6.129:~/Nokia-Network-lab/
```

| Part | Explanation |
|---|---|
| `scp` | Secure Copy Protocol — transfers files securely over SSH using the same encryption and authentication as your SSH connection |
| `"C:\Users\thako\...\nokia_phase1_complete.md"` | The source file path on Windows. Quotes are required because the path contains spaces |
| `ubuntu@192.168.6.129` | The same user@address format used when SSHing into Ubuntu |
| `:~/Nokia-Network-lab/` | The colon separates the address from the destination path on Ubuntu. The trailing `/` means "put the file inside this folder" |

**Confirm both files arrived on Ubuntu** — switch back to your Ubuntu SSH window and run:

```bash
ls ~/Nokia-Network-lab/
```

**Expected output:**
```
nokia_phase1_complete.md  nokia_phase2_complete.md  pcaps  results  scripts
```

Both MD files and all three subfolders should be visible.

---

## Step 11 — Stage, Commit, and Push to GitHub

This three-step ritual is the core Git workflow you will use every single time you save work to GitHub. Stage → Commit → Push.

### Stage

```bash
git add .
```

`git add` tells Git "start tracking these files and include them in the next commit." The `.` means "everything in the current folder and all subfolders." This stages both MD files at once. Think of staging like putting items into a box before sealing it — you are selecting what goes into this save point. Git produces no output for this command when it succeeds — silence means it worked.

### Commit

```bash
git commit -m "Add Phase 1 and Phase 2 lab notes"
```

| Part | Explanation |
|---|---|
| `git commit` | Takes everything staged with `git add` and creates a permanent save point in the repository history |
| `-m` | "Message" flag — lets you write a description of this save point directly on the same line |
| `"Add Phase 1 and Phase 2 lab notes"` | The commit message. Good messages are short, specific, and written in present tense. This tells anyone reading the history exactly what changed in this snapshot |

**Expected output:**
```
[main (root-commit) a3eed41] Add Phase 1 and Phase 2 lab notes
 2 files changed, 732 insertions(+)
 create mode 100644 nokia_phase1_complete.md
 create mode 100644 nokia_phase2_complete.md
```

| Output field | Meaning |
|---|---|
| `main` | The branch this commit landed on |
| `root-commit` | This is the very first commit in the repository — the root of the entire history |
| `a3eed41` | The unique short ID Git assigned to this commit. Every commit gets its own ID so you can reference any specific point in history |
| `2 files changed, 732 insertions(+)` | Git counted exactly 2 files and 732 lines added across both MD files |
| `create mode 100644` | Git created a new file entry. `100644` is a Unix permission code meaning normal readable file |

### Push

```bash
git push -u origin main
```

| Part | Explanation |
|---|---|
| `git push` | Uploads committed changes from Ubuntu to GitHub |
| `-u` | "Set upstream" — permanently links your local `main` branch to the remote `main` branch. After this first push, you can just type `git push` with no arguments for all future pushes |
| `origin` | The nickname for your GitHub remote URL |
| `main` | The branch being pushed |

**Expected output:**
```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 2 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 18.24 KiB | 6.08 MiB/s, done.
Total 4 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/Kanhay-Thakore/Nokia-Network-lab.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

| Output field | Meaning |
|---|---|
| `Enumerating objects: 4` | Git identified 4 objects to transfer (2 files + folder metadata) |
| `Writing objects: 100% (4/4)` | All 4 objects successfully uploaded |
| `18.24 KiB / 6.08 MiB/s` | Total data transferred and upload speed |
| `[new branch] main -> main` | Created the `main` branch on GitHub for the first time, matching your local `main` |
| `branch 'main' set up to track 'origin/main'` | Upstream tracking configured — future pushes need only `git push` |

---

## Important Git Concept — Why Empty Folders Don't Appear on GitHub

After the push, the `scripts`, `pcaps`, and `results` folders are visible on Ubuntu but not on GitHub. This is expected and is a fundamental Git behavior: **Git tracks files, not folders.** When `git add .` ran, Git looked inside each subfolder, found nothing, and skipped them entirely. The folders exist perfectly on Ubuntu — they just have no content for Git to snapshot.

Those folders will appear on GitHub automatically the moment a file is placed inside them. When Script 1 is saved into `scripts/` and pushed, the `scripts` folder will appear on GitHub with the script inside it. This is how all professional repositories work.

---

## The Git Workflow Going Forward

From this point forward, every time a script is written or modified, the workflow to save it to GitHub is always the same three commands:

**On Windows (VS Code terminal) — push the script:**
```powershell
git add .
git commit -m "Describe what you changed"
git push
```

**On Ubuntu — pull the script and run it:**
```bash
git pull
python3 scripts/http_traffic_generator.py
```

That is the complete professional Git workflow. Four commands total across two machines. Every time.

**Good commit message examples for Phase 3:**
- `"Add Script 1 HTTP traffic generator"`
- `"Add Script 2 DNS test script"`
- `"Add Script 3 pcap analyzer"`
- `"Fix DNS timeout handling in Script 2"`
- `"Add Phase 3 complete notes"`

---

## Key Concepts Summary

### Git vs GitHub
Git is the version control software — installed on both Ubuntu and Windows. GitHub is the cloud hosting service where your repository lives online — it stores your history and makes it accessible to collaborators and interviewers. Git and GitHub are separate things. You use Git commands to push your local history up to GitHub from either machine.

### VS Code as the Development Environment
VS Code is not just a text editor — it is a full IDE (Integrated Development Environment) with syntax highlighting, real-time error detection, Git integration, and a built-in terminal. The Git integration means VS Code's terminal already knows where the repository is and who it belongs to. Opening the project with `code .` from inside the cloned folder links VS Code directly to that repository — no additional configuration needed.

### Commits
A commit is a permanent snapshot of your project at a specific moment in time. Every commit has a unique ID, an author name and email, a timestamp, a message describing what changed, and a record of exactly which lines were added or removed. The commit history is the complete story of how your project evolved.

### Branches
A branch is an independent timeline of commits. The `main` branch is the primary timeline. In professional teams, developers create separate branches for new features or experiments, work on them without affecting `main`, then merge them in when the work is complete. For this lab, working directly on `main` is appropriate.

### Remote vs Local
Your local repositories are the `.git` folders on Ubuntu and in `C:\Users\thako\Nokia-Network-lab` on Windows — they each store the full history on disk. Your remote repository is GitHub — it stores the same history in the cloud. `git push` uploads local commits to the remote. `git pull` downloads changes from the remote to your local machine. Both machines push and pull to the same GitHub remote — this is how teams collaborate.

### The Complete Workflow
```
VS Code (Windows)     → Write script
git add .             → Stage changes
git commit -m "..."   → Create save point
git push              → Upload to GitHub

Ubuntu VM
git pull              → Download from GitHub
python3 script.py     → Execute in lab
```

---

## Commands Quick Reference — Git Setup

| Command | Where | What It Does |
|---|---|---|
| `python3 --version` | Ubuntu | Confirm Python 3 is installed and check version |
| `git --version` | Both | Confirm Git is installed and check version |
| `git config --global user.name "Name"` | Ubuntu | Set Git author name for all repositories on this machine |
| `git config --global user.email "email"` | Ubuntu | Set Git author email for all repositories on this machine |
| `git config --list` | Both | Show all current Git configuration settings |
| `mkdir -p ~/Nokia-Network-lab/scripts` | Ubuntu | Create project folder and scripts subfolder |
| `git init` | Ubuntu | Initialize current folder as a Git repository |
| `git branch -m main` | Ubuntu | Rename current branch from master to main |
| `git config --global init.defaultBranch main` | Both | Set main as default branch for all future repos |
| `git status` | Both | Show current state of the repository |
| `git remote add origin URL` | Ubuntu | Link local repository to GitHub remote |
| `git remote -v` | Both | Show all remote connections with their URLs |
| `git add .` | Both | Stage all files in current folder for next commit |
| `git commit -m "message"` | Both | Create a save point with a description |
| `git push -u origin main` | Both | Upload commits to GitHub and set upstream tracking |
| `git push` | Both | Upload commits to GitHub (after upstream is set) |
| `git pull` | Ubuntu | Download latest commits from GitHub |
| `git clone URL` | Windows | Download a full copy of a GitHub repository |
| `code .` | Windows | Open VS Code with current folder as project root |
| `python -m pip install requests` | Windows | Install Python library into Windows Python 3.12 |

---

## scp Quick Reference — Windows to Ubuntu

```powershell
# Run this in PowerShell on Windows
scp "C:\path\to\your\file.md" ubuntu@192.168.6.129:~/Nokia-Network-lab/
```

Always use quotes around the Windows path if it contains spaces. The colon after the IP address separates the address from the destination path on Ubuntu.

---

## Interview Talking Points — Git and Source Control

**If asked about Git experience:**
*"I set up a complete Git workflow across two environments — Ubuntu Server VM and a Windows development machine. On Ubuntu I initialized the repository, configured identity, and linked it to GitHub. On Windows I installed Git, cloned the repository into VS Code, and established the push workflow so scripts written in VS Code are pushed to GitHub and pulled onto Ubuntu for execution. I understand the stage-commit-push cycle and have used it to version-control lab notes and Python automation scripts across multiple phases of a network testing project."*

**If asked about your development workflow:**
*"I write Python scripts locally in VS Code on Windows, which gives me full syntax highlighting, IntelliSense, and real-time error detection through the Python and Pylance extensions. When the script is ready I push it to GitHub with a descriptive commit message, then SSH into my Ubuntu VM, pull the latest version, and execute it against the lab environment. This is the same workflow professional Nokia developers use — develop locally in an IDE, version-control through Git, deploy and execute on Linux."*

**If asked about source control in a team environment:**
*"Git gives a team a shared history of every change ever made to a codebase — who changed what, when, and why. In a Nokia testing context, that means if a new test script breaks the regression suite, you can identify exactly which commit introduced the problem and roll back to the last known good state. I understand the distinction between local repositories and remote repositories, and the workflow of committing locally then pushing to a shared remote."*

**If asked about your GitHub portfolio:**
*"My Nokia lab work is documented and version-controlled at github.com/Kanhay-Thakore/Nokia-Network-lab. It contains complete notes from three lab phases covering HTTP packet capture, DNS analysis, HTTPS/TLS fingerprinting, QUIC, RTP, and Python automation scripts — all organized by folder and committed with descriptive messages so the progression of the project is visible in the commit history."*

---

*Git Setup Completed: May 4, 2026*
*Windows Development Environment Setup Completed: May 14, 2026*
*Repository: https://github.com/Kanhay-Thakore/Nokia-Network-lab*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Phase 3 — Python Automation Scripts (5 scripts)*
