# Git & GitHub Setup Guide for CyberShield AI

Complete step-by-step guide for initializing Git, connecting to GitHub, and establishing team collaboration workflows.

---

## 📋 Table of Contents
1. [Initial Setup: Initialize Git Repository](#1-initial-setup)
2. [Step 1: Initialize Git Repository Locally](#step-1-initialize-git-locally)
3. [Step 2: Add Files to Git](#step-2-add-files)
4. [Step 3: Create Initial Commit](#step-3-initial-commit)
5. [Step 4: Create GitHub Repository](#step-4-create-github-repo)
6. [Step 5: Connect Local to GitHub](#step-5-connect-local-to-github)
7. [Step 6: Push to GitHub](#step-6-push-to-github)
8. [Team Collaboration: Cloning Repository](#team-collaboration)
9. [Team Collaboration: Pulling Changes](#pulling-changes)
10. [Feature Development with Branches](#feature-branches)
11. [Complete Team Workflow](#complete-workflow)
12. [Resolving Merge Conflicts](#merge-conflicts)
13. [Best Practices](#best-practices)

---

## 1. Initial Setup

Before starting, ensure you have:
- **Git installed**: [Download from git-scm.com](https://git-scm.com/)
- **GitHub account**: [Create at github.com](https://github.com/)
- **Git Bash** or PowerShell terminal

### Configure Git (First time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Verify configuration:
```bash
git config --global --list
```

---

## Step 1: Initialize Git Locally

This creates a `.git` folder in your project directory.

```bash
cd c:\Users\DELL\OneDrive\Desktop\cyber_detection\cybercrime-detection
git init
```

**What happens:**
- Creates a hidden `.git` directory
- Initializes the repository
- Ready to track changes

**Verify:**
```bash
git status
```

Expected output:
```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        app.py
        feature_extraction.py
        README.md
        ...
```

---

## Step 2: Add Files to Git

### Add all files at once:
```bash
git add .
```

### Or add specific files:
```bash
git add app.py
git add requirements.txt
git add -A  # Alternative: add all changes
```

### Check what's staged:
```bash
git status
```

Expected output:
```
On branch master

No commits yet

Changes to be committed:
  (use "rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   app.py
        new file:   feature_extraction.py
        ...
```

---

## Step 3: Create Initial Commit

A commit is a snapshot of your project at a point in time.

```bash
git commit -m "Initial commit: CyberShield AI project setup"
```

**What this does:**
- Saves all staged changes permanently to history
- Creates a checkpoint you can return to
- `-m` flag adds a commit message (brief description)

### Good commit message guidelines:
```
✓ "Add user authentication to Flask app"
✓ "Fix phishing detection model accuracy"
✓ "Update requirements.txt with new dependencies"
✗ "Update"
✗ "Changes made"
```

### View commit history:
```bash
git log
```

Output shows commits with author, date, hash, and message.

---

## Step 4: Create GitHub Repository

### On GitHub.com:

1. **Go to github.com** and log in
2. **Click + icon** (top right) → "New repository"
3. **Fill in details:**
   - Repository name: `cybershield-ai` (or your preference)
   - Description: "AI-powered phishing URL and message detection system"
   - Visibility: Choose **Public** (team can see) or **Private** (invite only)
   - Do NOT initialize with README (you already have one)
   - Do NOT add .gitignore (you already have one)
4. **Click "Create repository"**

You'll see a page with commands - **don't follow them yet**. Use the instructions below instead.

---

## Step 5: Connect Local Repository to GitHub

Once you've created a GitHub repository, connect your local git to it.

### Get your repository URL:
- On GitHub, click the green **"Code"** button
- Copy the **HTTPS URL** (looks like: `https://github.com/yourusername/cybershield-ai.git`)

### Add remote origin (connection to GitHub):
```bash
git remote add origin https://github.com/yourusername/cybershield-ai.git
```

Replace `yourusername` with your actual GitHub username.

### Verify connection:
```bash
git remote -v
```

Expected output:
```
origin  https://github.com/yourusername/cybershield-ai.git (fetch)
origin  https://github.com/yourusername/cybershield-ai.git (push)
```

---

## Step 6: Push to GitHub

Upload your local commits to GitHub.

```bash
git push -u origin master
```

**What this does:**
- `-u`: Sets `origin/master` as upstream (default for future pushes)
- `origin`: The GitHub repository
- `master`: The branch name

**First push authentication:**
If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (NOT your password!)

### Create a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Scopes: Check `repo` (full control of private repositories)
4. Copy the token and save it securely
5. Use this token when Git asks for password

### After successful push:
- Go to your GitHub repository
- You should see all your files in the `master` branch
- Commit history visible in the repository

---

## Team Collaboration: Cloning Repository

### For team members to get the project:

```bash
cd desired/folder/location
git clone https://github.com/yourusername/cybershield-ai.git
cd cybershield-ai
```

**What happens:**
- Downloads entire repository with full history
- Creates local copy with remote connection
- Ready to work immediately

### Set up environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

---

## Team Collaboration: Pulling Changes

### When a team member pushes updates, others pull them:

**Check for updates:**
```bash
git fetch origin
```
(Downloads latest without changing your files)

**Apply updates to your files:**
```bash
git pull origin master
```

**Shorthand (after first push/pull):**
```bash
git pull
```

**View what will be pulled:**
```bash
git log --oneline origin/master -5
```

---

## Feature Branches

### Why use branches?
- Keep `master` branch stable
- Develop features independently
- Test before merging
- Parallel development by multiple team members

### Create a new branch:
```bash
git branch feature/phishing-detector-v2
```

### View all branches:
```bash
git branch -a
```

### Switch to branch:
```bash
git checkout feature/phishing-detector-v2
```

### Create AND switch in one command:
```bash
git checkout -b feature/phishing-detector-v2
```

### Delete a branch:
```bash
git branch -d feature/phishing-detector-v2
```

---

## Complete Team Workflow

### **Developer A: Starting new feature**

**1. Update from master:**
```bash
git checkout master
git pull origin master
```

**2. Create feature branch:**
```bash
git checkout -b feature/message-detection-improvement
```

**3. Make changes** (edit files in VS Code)

**4. Check changes:**
```bash
git status
git diff  # See detailed changes
```

**5. Stage and commit:**
```bash
git add .
git commit -m "Improve message detection accuracy using TF-IDF"
```

**6. Push feature branch:**
```bash
git push -u origin feature/message-detection-improvement
```

### **Developer A: Creating Pull Request (PR)**

1. Go to GitHub repository
2. Click "Pull requests" tab
3. Click "New pull request"
4. Compare: `feature/message-detection-improvement` → `master`
5. Add title and description:
   ```
   Title: Improve message detection accuracy
   
   Description:
   - Implemented TF-IDF vectorization
   - Improved accuracy from 92% to 96%
   - Added unit tests for edge cases
   ```
6. Click "Create pull request"

### **Developer B: Reviewing PR**

1. Open the pull request
2. Review code changes
3. Leave comments (click line to comment)
4. Request changes or approve
5. Once approved, click "Merge pull request"

### **After merge:**
Other team members pull the changes:
```bash
git checkout master
git pull origin master
```

---

## Step-by-Step Workflow for Team Members

```bash
# ===== START OF DAY =====
# 1. Update to latest code
git checkout master
git pull origin master

# ===== START WORKING ON FEATURE =====
# 2. Create feature branch
git checkout -b feature/your-feature-name

# ===== DURING DEVELOPMENT =====
# 3. Make changes in VS Code
# ... edit files ...

# 4. Check status
git status

# 5. Stage changes
git add .
# or git add specific_file.py

# 6. Commit regularly
git commit -m "Add feature description"

# 7. Repeat steps 3-6 as you make progress
git add .
git commit -m "Fix bug in authentication"

# ===== READY TO SHARE =====
# 8. Push to GitHub
git push -u origin feature/your-feature-name

# 9. Create Pull Request on GitHub
# (GitHub will show a prompt, or go to Pull requests tab)

# ===== AFTER CODE REVIEW & MERGE =====
# 10. Switch back to master
git checkout master

# 11. Pull merged changes
git pull origin master

# 12. Delete old branch (keep repository clean)
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## Resolving Merge Conflicts

### What causes conflicts?
- Two developers edit the same file at same location
- Git can't automatically merge changes

### Example conflict in file:

```
def detect_phishing(url):
<<<<<<< HEAD
    # Version A: Using new method
    return advanced_detection(url)
=======
    # Version B: Using old method
    return simple_detection(url)
>>>>>>> feature/message-detection-improvement
```

### How to resolve:

**1. Pull the conflicting changes:**
```bash
git pull origin master
```

VS Code will highlight conflicts in red.

**2. Open the conflicted file** and choose:
- **Accept Current Change** (keep your version)
- **Accept Incoming Change** (use their version)
- **Accept Both Changes** (keep both)
- **Compare Changes** (see side-by-side)

**3. Manually edit if needed** - delete `<<<<<<<`, `=======`, `>>>>>>>`

**4. Stage and commit:**
```bash
git add .
git commit -m "Resolve merge conflict in app.py"
```

**5. Push:**
```bash
git push origin feature/your-branch
```

---

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `git init` | Initialize new repository |
| `git status` | See current state |
| `git add .` | Stage all changes |
| `git add file.py` | Stage specific file |
| `git commit -m "message"` | Create snapshot |
| `git log` | View commit history |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| `git branch` | List branches |
| `git checkout -b feature/name` | Create & switch branch |
| `git merge feature/name` | Merge branch to current |
| `git fetch` | Download without applying |
| `git diff` | See changes before commit |
| `git reset --hard HEAD~1` | Undo last commit (⚠️ dangerous) |

---

## Best Practices for Team Collaboration

### 📌 Branch Naming Conventions
```
feature/user-authentication      # New features
bugfix/phishing-detection-error  # Bug fixes
hotfix/critical-security-issue   # Urgent fixes
docs/update-readme               # Documentation
refactor/simplify-model-code     # Code improvements
```

### 📌 Commit Message Standards
```
✓ "Add OAuth2 authentication to login page"
✓ "Fix accuracy calculation in phishing model"
✓ "Update dependencies in requirements.txt"
✓ "Refactor URL feature extraction logic"

✗ "bug fix"
✗ "changes"
✗ "update stuff"
```

### 📌 Pull Request Best Practices
- **Keep PRs small** (< 400 lines of code)
- **Clear description** of what changed and why
- **Reference issues** if applicable (#123)
- **Test before pushing** (run train_model.py, test in browser)
- **Respond to reviews** promptly
- **Never merge your own PR** - wait for team review

### 📌 Code Review Checklist
- [ ] Code follows project style
- [ ] No hardcoded credentials or passwords
- [ ] Tests pass and coverage is acceptable
- [ ] Comments explain complex logic
- [ ] No unnecessary dependencies added
- [ ] Performance impact analyzed (if applicable)

### 📌 Directory Structure in Commits
Never commit:
```
__pycache__/        (Python bytecode)
venv/              (Virtual environment)
*.pyc              (Compiled Python)
.env               (API keys, credentials)
model/*.pkl        (Large ML models - use Git LFS)
dataset/*.csv      (Large data files - use Git LFS)
```

These are already in `.gitignore` ✓

### 📌 Team Communication
- Use **GitHub Discussions** for questions
- Use **Issues** to track bugs and features
- Use **PR comments** for code-specific feedback
- Update **README.md** as project evolves

### 📌 Preventing Credentials in Code
```bash
# ❌ WRONG - Don't do this
password = "Mahi@123456"
api_key = "sk_live_12345..."

# ✅ RIGHT - Use environment variables
import os
password = os.getenv('DB_PASSWORD')
api_key = os.getenv('API_KEY')
```

Create `.env` file (in .gitignore):
```
DB_PASSWORD=Mahi@123456
API_KEY=sk_live_12345...
```

### 📌 Large Files with Git LFS
For large model files (> 100MB):
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add model/large_model.pkl
git commit -m "Add large model with Git LFS"
```

---

## Troubleshooting

### "fatal: not a git repository"
```bash
cd /path/to/project
git init
```

### Changes not being tracked
```bash
git add .
git status  # Verify files are staged
git commit -m "Your message"
```

### Accidentally committed wrong file
```bash
git reset --soft HEAD~1  # Undo last commit, keep changes
git reset /path/to/file  # Unstage specific file
git commit -m "Correct message"
```

### Want to discard all local changes
```bash
git reset --hard HEAD  # ⚠️ Deletes all unsaved work!
```

### Forgot to add something to commit
```bash
git add forgotten_file.py
git commit --amend --no-edit  # Adds to previous commit
```

### Need to update from main branch
```bash
git status  # Make sure working directory is clean
git fetch origin master
git rebase origin/master  # or git merge origin/master
```

---

## Quick Start Checklist

- [ ] **You (Project Owner):**
  - [ ] Initialize repo: `git init`
  - [ ] Add files: `git add .`
  - [ ] Commit: `git commit -m "Initial commit"`
  - [ ] Create GitHub repo
  - [ ] Add remote: `git remote add origin [URL]`
  - [ ] Push: `git push -u origin master`
  - [ ] Invite team members on GitHub

- [ ] **Team Members:**
  - [ ] Clone repo: `git clone [URL]`
  - [ ] Create virtual environment
  - [ ] Install requirements: `pip install -r requirements.txt`
  - [ ] Configure Git (user.name, user.email)
  - [ ] Start working on feature branch

---

## Additional Resources
- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Tutorials](https://www.youtube.com/githubguides)
- [Pro Git Book](https://git-scm.com/book/en/v2)

---

**Need help?** Contact your project lead or refer to specific sections above.

Good luck with CyberShield AI! 🚀
