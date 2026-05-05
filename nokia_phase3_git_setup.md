# Nokia Network Lab — Phase 3: Git Setup & GitHub Portfolio
## Complete Notes | Git · GitHub · Source Control · Windows-to-Ubuntu File Transfer
> Mapped to Nokia Junior Developer JD Requirements
> Status: ✅ COMPLETE (Git Setup & Repository Initialization)

---

## JD Mapping

This section directly addresses the Nokia JD requirement: *"Experience with Git or similar source control systems."* Every command in this section is real professional Git workflow — the same workflow Nokia engineers use daily to version-control test scripts, automation code, and lab tooling. By the end of this setup, a fully structured GitHub portfolio repository exists at https://github.com/Kanhay-Thakore/Nokia-Network-lab, containing Phase 1 and Phase 2 lab notes, with the folder structure ready to receive all Phase 3 Python scripts. The entire workflow — configuring Git identity, initializing a local repository, linking it to a remote, and pushing files — mirrors exactly what is expected of a junior developer contributing to a team codebase.

---

## Lab Environment

| Component | Details | Purpose |
|---|---|---|
| Ubuntu Server VM | Ubuntu 26.04 LTS at 192.168.6.129 | Git repository host, script development environment |
| Kali Linux VM | kali-linux-2025.2 at 192.168.6.130 | Secondary analyst machine |
| Windows Desktop | Host laptop | SSH client, source of MD files transferred via scp |
| GitHub Repository | https://github.com/Kanhay-Thakore/Nokia-Network-lab | Remote portfolio repository (public) |
| Git Version | 2.53.0 | Installed on Ubuntu during Phase 0 |
| Python Version | 3.14.4 | Confirmed ready on Ubuntu for Phase 3 scripts |
| Network | VMnet8 NAT | Both VMs on same subnet |

---

## Why Git Matters for Nokia

Git is the industry-standard version control system used by virtually every professional software and network engineering team. In Nokia's context, Git serves several purposes: test scripts and automation code are committed to shared repositories so the entire team can collaborate, track changes, and roll back to a previous working version if a new script breaks something. Every bug fix, new test case, and feature addition is a commit — a permanent record of what changed, when, and by whom. When the Nokia JD lists "Experience with Git or similar source control systems," they are looking for candidates who understand this workflow and can contribute to a shared codebase from day one without needing to be taught the basics.

---

## Where Python Scripts Are Written and Run

Before touching Git, it is important to establish the correct development workflow for this lab. The scripts in Phase 3 need to read pcap files, send HTTP requests to the Ubuntu server, and analyze packet-level data — all of which lives on the Linux VMs. Python 3.14.4 is already installed on Ubuntu. The correct workflow is:

```
PowerShell (SSH into Ubuntu) → write script with nano → run script on Ubuntu → git push to GitHub
```

This mirrors the professional workflow Nokia engineers use daily — SSH into a remote Linux server, write and run scripts in the terminal, commit working code to Git. There is no GUI, no clicking, just terminal. Developing directly on Ubuntu means zero file-transfer friction between writing and running, and it is the same environment where the scripts will be executed against real network traffic.

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

```bash
git add .
git commit -m "Describe what you changed"
git push
```

That is the complete professional Git workflow. Three commands. Every time.

**Good commit message examples for Phase 3:**
- `"Add Script 1 HTTP traffic generator"`
- `"Add Script 2 DNS test script"`
- `"Add Script 3 pcap analyzer"`
- `"Fix DNS timeout handling in Script 2"`
- `"Add Phase 3 complete notes"`

---

## Key Concepts Summary

### Git vs GitHub
Git is the version control software installed on Ubuntu — it tracks changes locally. GitHub is the cloud hosting service where your repository lives online — it stores your history and makes it accessible to collaborators and interviewers. Git and GitHub are separate things. You use Git commands on Ubuntu to push your local history up to GitHub.

### Commits
A commit is a permanent snapshot of your project at a specific moment in time. Every commit has a unique ID, an author name and email, a timestamp, a message describing what changed, and a record of exactly which lines were added or removed. The commit history is the complete story of how your project evolved.

### Branches
A branch is an independent timeline of commits. The `main` branch is the primary timeline. In professional teams, developers create separate branches for new features or experiments, work on them without affecting `main`, then merge them in when the work is complete. For this lab, working directly on `main` is appropriate.

### Remote vs Local
Your local repository is the `.git` folder on Ubuntu — it stores everything on disk. Your remote repository is GitHub — it stores the same history in the cloud. `git push` uploads your local commits to the remote. `git pull` downloads changes from the remote to your local machine. Both must be kept in sync for collaborative work.

### The Three-Step Ritual
```
git add .           → Stage: select what goes in the next save point
git commit -m "..."  → Commit: create the save point with a label
git push            → Push: upload the save point to GitHub
```

---

## Commands Quick Reference — Git Setup

| Command | What It Does |
|---|---|
| `python3 --version` | Confirm Python 3 is installed and check version |
| `git --version` | Confirm Git is installed and check version |
| `git config --global user.name "Name"` | Set Git author name for all repositories on this machine |
| `git config --global user.email "email"` | Set Git author email for all repositories on this machine |
| `git config --list` | Show all current Git configuration settings |
| `mkdir -p ~/Nokia-Network-lab/scripts` | Create project folder and scripts subfolder |
| `git init` | Initialize current folder as a Git repository |
| `git branch -m main` | Rename current branch from master to main |
| `git config --global init.defaultBranch main` | Set main as default branch for all future repos |
| `git status` | Show current state of the repository |
| `git remote add origin URL` | Link local repository to GitHub remote |
| `git remote -v` | Show all remote connections with their URLs |
| `git add .` | Stage all files in current folder for next commit |
| `git commit -m "message"` | Create a save point with a description |
| `git push -u origin main` | Upload commits to GitHub and set upstream tracking |
| `git push` | Upload commits to GitHub (after upstream is set) |

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
*"I set up a Git repository on an Ubuntu Server VM, configured my identity, linked it to a remote GitHub repository, and established the complete push workflow. I understand the stage-commit-push cycle and have used it to version-control lab notes and Python automation scripts across multiple phases of a network testing project."*

**If asked about source control in a team environment:**
*"Git gives a team a shared history of every change ever made to a codebase — who changed what, when, and why. In a Nokia testing context, that means if a new test script breaks the regression suite, you can identify exactly which commit introduced the problem and roll back to the last known good state. I understand the distinction between local repositories and remote repositories, and the workflow of committing locally then pushing to a shared remote."*

**If asked about your GitHub portfolio:**
*"My Nokia lab work is documented and version-controlled at github.com/Kanhay-Thakore/Nokia-Network-lab. It contains complete notes from three lab phases covering HTTP packet capture, DNS analysis, HTTPS/TLS fingerprinting, QUIC, RTP, and Python automation scripts — all organized by folder and committed with descriptive messages so the progression of the project is visible in the commit history."*

---

*Git Setup Completed: May 4, 2026*
*Repository: https://github.com/Kanhay-Thakore/Nokia-Network-lab*
*Lab: Ubuntu 192.168.6.129 | Kali 192.168.6.130 | VMnet8 NAT*
*Next: Phase 3 — Python Automation Scripts (5 scripts)*
