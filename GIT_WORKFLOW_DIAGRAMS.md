# Git Workflow Diagrams & Examples

Visual guide to understanding Git and GitHub collaboration workflows.

---

## 1️⃣ Project Initialization Diagram

```
You (Project Owner)
│
├─ LOCAL MACHINE
│  ├─ cybercrime-detection/
│  │  ├─ app.py
│  │  ├─ requirements.txt
│  │  ├─ .git/ ← Git Repository ✓ INITIALIZED
│  │  └─ ...files...
│  │
│  └─ git remote add origin [GitHub URL]  ← Connect to GitHub
│
├─ GITHUB.COM (Cloud)
│  └─ yourusername/cybershield-ai
│     └─ (Empty, waiting for push)
│
└─ git push -u origin master  ← Upload to GitHub
   │
   └─ GITHUB.COM
      └─ yourusername/cybershield-ai
         └─ master branch with all files ✓
```

---

## 2️⃣ Team Member Cloning

```
Team Member (Developer A)
│
├─ LOCAL MACHINE
│  ├─ Clone Command
│  │  git clone https://github.com/yourusername/cybershield-ai.git
│  │
│  └─ cybershield-ai/ ← Complete copy with history
│     ├─ app.py
│     ├─ requirements.txt
│     ├─ .git/ ← Full repository history
│     └─ ...all files...
│
└─ Ready to work! ✓
```

---

## 3️⃣ Feature Development Workflow

```
STARTING STATE: master branch is stable

Developer A                          Developer B
    │                                    │
    ├─ git pull                          ├─ git pull
    │  (Get latest)                      │  (Get latest)
    │                                    │
    ├─ git checkout -b                   ├─ git checkout -b
    │  feature/auth                      │  feature/model-v2
    │  │                                 │
    │  ├─ Edit login.html                ├─ Edit train_model.py
    │  ├─ Edit app.py                    ├─ Edit feature_extraction.py
    │  │                                 │
    │  ├─ git add .                      ├─ git add .
    │  ├─ git commit                     ├─ git commit
    │  ├─ git commit                     ├─ git commit
    │  │                                 │
    │  └─ git push origin feature/auth   └─ git push origin feature/model-v2
    │     │                                 │
    │     └─[GitHub: Create Pull Request]─┘
    │         (Request code review)
    │
    ├─ [Teammate reviews code]
    ├─ [Make changes if requested]
    │  git add . → git commit → git push
    │
    └─ [Code approved & merged to master]
       │
       ├─ git checkout master
       ├─ git pull origin master
       │  (Get the merged code)
       │
       └─ Continue with next feature...
```

---

## 4️⃣ Single Developer Workflow - Detailed

### Step-by-step with real example:

#### Day 1: Start New Feature

```bash
# 1. Get latest code
git checkout master
git pull origin master

# 2. Create feature branch
git checkout -b feature/add-export-reports

# 3. Make changes (in VS Code)
# Edit: app.py, templates/reports.html, README.md

# 4. Check what changed
git status
# Output:
#  modified:   app.py
#  modified:   templates/reports.html
#  new file:   utils/export.py

# 5. Stage changes
git add .

# 6. Commit
git commit -m "Add PDF export functionality for security reports"

# 7. Push to GitHub
git push -u origin feature/add-export-reports
```

#### GitHub: Create Pull Request
```
Go to GitHub → Click "Compare & pull request"

Title: Add PDF export for security reports

Description:
## Changes Made
- Added PDF export button to reports page
- Created export.py utility module
- Updated requirements.txt with reportlab dependency

## How to Test
1. Go to Reports page
2. Click "Export as PDF"
3. Verify PDF downloads with proper formatting

## Related Issues
Closes #12
```

#### Day 2: Address Review Feedback

```bash
# 1. Look at review comments (on GitHub)
# Reviewer said: "Add error handling for missing data"

# 2. Make requested changes
# Edit: utils/export.py

# 3. Stage and commit
git add utils/export.py
git commit -m "Add error handling for missing data in PDF export"

# 4. Push (same branch)
git push origin feature/add-export-reports

# 5. Comment on PR: "Done! Added try-catch blocks for all edge cases"
```

#### Day 3: Merge Complete

```bash
# On GitHub: Teammate clicks "Merge pull request" ✓

# 1. Your local: sync with master
git checkout master
git pull origin master

# 2. Delete old branch
git branch -d feature/add-export-reports
git push origin --delete feature/add-export-reports

# 3. Start next feature...
git checkout -b feature/add-email-notifications
```

---

## 5️⃣ Multiple Developers - Parallel Development

```
Timestamp: Monday 9:00 AM
Status: master branch latest (commit abc123)

DevA: feature/auth          DevB: feature/model         DevC: feature/ui
│                           │                           │
├─ 9:30 AM                  ├─ 9:30 AM                  ├─ 9:30 AM
│  git pull                 │  git pull                 │  git pull
│  git checkout -b          │  git checkout -b          │  git checkout -b
│  feature/2fa-auth         │  feature/ml-v2            │  feature/dark-theme
│                           │                           │
├─ 10:00 AM: Edits files    ├─ 10:00 AM: Edits files    ├─ 10:00 AM: Edits files
│                           │                           │
├─ 10:30 AM: Commits (def1) ├─ 10:30 AM: Commits (def2) ├─ 10:30 AM: Commits (def3)
│                           │                           │
├─ 11:00 AM: git push       ├─ 11:00 AM: git push       ├─ 11:00 AM: git push
│  ↓ Pull Request            ↓ Pull Request              ↓ Pull Request
│                           │                           │
├─ 12:00 PM: Reviewed ✓     ├─ 12:00 PM: Reviewed ✓     ├─ 12:00 PM: Reviewed ✓
│                           │                           │
├─ 1:00 PM: Merged ✓        ├─ 1:00 PM: Merged ✓        ├─ 1:30 PM: CONFLICT! ✗
│                           │                           │  (DevB changed same files)
└─ master now has:          └─ master now has:          │
   auth + model updates        model updates            └─ DevC must:
                                                           1. Pull latest master
                                                           2. Resolve conflicts
                                                           3. Commit & push
                                                        
All developers updated →
git checkout master
git pull origin master
→ Everyone has all 3 features! ✓
```

---

## 6️⃣ Merge Conflict Example

### Scenario: Two developers edit same file

```
DevA's version (app.py):
    def detect_phishing(url):
        # Using machine learning model
        score = ml_model.predict(url)
        return score > 0.5

DevB's version (app.py):
    def detect_phishing(url):
        # Using heuristic rules
        return check_phishing_url(url)
```

### Conflict notice in file:

```python
<<<<<<< HEAD
    def detect_phishing(url):
        score = ml_model.predict(url)
        return score > 0.5
=======
    def detect_phishing(url):
        return check_phishing_url(url)
>>>>>>> feature/heuristic-method
```

### Resolution options:

**Option A: Accept Current Change (DevA's ML version)**
```python
def detect_phishing(url):
    score = ml_model.predict(url)
    return score > 0.5
```

**Option B: Accept Incoming Change (DevB's heuristic version)**
```python
def detect_phishing(url):
    return check_phishing_url(url)
```

**Option C: Combine Both (Best approach)**
```python
def detect_phishing(url):
    # ML-based detection (primary)
    try:
        score = ml_model.predict(url)
        if score > 0.5:
            return True
    except:
        # Fallback to heuristic rules if ML fails
        return check_phishing_url(url)
    
    return False
```

### Steps to resolve:

```bash
# 1. Pull the conflicting changes
git pull origin master

# 2. Edit app.py - choose correct version or combine

# 3. Stage the resolved file
git add app.py

# 4. Commit the merge
git commit -m "Resolve merge conflict: combine ML and heuristic detection"

# 5. Push the resolution
git push origin feature/your-branch
```

---

## 7️⃣ Complete Daily Workflow - Visual Timeline

```
MORNING (9:00 AM)
├─ Open terminal
├─ git status
│  └─ Review current branch
├─ git pull origin master
│  └─ Get latest code from team
└─ git checkout -b feature/your-task
   └─ Start isolated development

DEVELOPMENT (10:00 AM - 12:00 PM)
├─ Edit files in VS Code
├─ Test your code
│  └─ Run python train_model.py
│  └─ Test in browser at localhost:5000
├─ Review changes
│  └─ git diff
├─ Commit frequently
│  ├─ git add .
│  ├─ git commit -m "Improve model accuracy"
│  ├─ git add .
│  └─ git commit -m "Add error handling"
└─ Push to GitHub
   └─ git push -u origin feature/your-task

LUNCH (12:00 - 1:00 PM)
├─ GitHub: Create Pull Request
├─ Add clear description
├─ Request review from teammates
└─ Teammates can review changes

AFTERNOON (1:00 PM - 5:00 PM)
├─ Teammates leave code reviews
│  └─ Comments: "Please add docstrings"
├─ Address feedback
│  ├─ Edit files
│  ├─ git add .
│  └─ git commit -m "Address review: add docstrings"
├─ Push changes
│  └─ git push origin feature/your-task
├─ Teammates approve ✓
└─ Merge to master
   └─ Click "Merge pull request" on GitHub

END OF DAY (5:00 PM)
├─ git checkout master
├─ git pull origin master
└─ Clean local branches
   └─ git branch -d feature/your-task
```

---

## 8️⃣ Branch Management Visualization

```
BRANCH STRUCTURE AFTER MULTIPLE FEATURES:

master (main production branch)
│
├─ [merged← feature/auth]                (2FA authentication)
├─ [merged← feature/model-v2]            (Improved ML model)
├─ [merged← feature/export-pdf]          (PDF reports)
│
└─ [in-progress]
   ├─ feature/email-notifications        (DevA working)
   ├─ feature/dashboard-ui              (DevB working)
   └─ hotfix/security-patch             (DevC working)

VISUALIZATION:
                    ┌─── feature/email ──┐
                    │                    │
master: ab1─cd2─ef3─┼── feature/dash ────┤─→ will merge back
  ↑       ↑         │                    │
  │       │         └─── feature/hotfix──┘
  │       └─ All 3 features built on solid foundation
  │
  └─ Stable base everyone trusts
```

---

## 9️⃣ GitHub Interface Quick Guide

```
REPOSITORY PAGE:
https://github.com/yourusername/cybershield-ai

├─ Code tab
│  ├─ File browser
│  ├─ Commit history
│  └─ .gitignore, README.md visible
│
├─ Issues tab
│  ├─ Track bugs
│  ├─ Feature requests
│  └─ Assign work to team
│
├─ Pull Requests tab
│  ├─ Ongoing code reviews
│  ├─ Merged pull requests
│  └─ View changes & discussions
│
├─ Branches tab
│  ├─ All branches
│  ├─ Delete old branches
│  └─ See branch protection rules
│
├─ Settings tab  (Admin only)
│  ├─ Repository settings
│  ├─ Manage collaborators
│  └─ Set branch protection
│
└─ Discussions tab
   ├─ Team questions
   ├─ Share knowledge
   └─ Propose improvements
```

---

## 🔟 Emergency Situations

### Scenario: "Oh no! I committed to master instead of feature branch!"

```
BEFORE (Current bad state):
master: [commit with your changes] ← HEAD

SOLUTION:
# 1. Create new branch with current changes
git branch feature/oops

# 2. Reset master to before your commit
git reset --soft HEAD~1

# 3. Switch to feature branch
git checkout feature/oops

# 4. Stage and commit properly
git add .
git commit -m "Your feature"

# 5. Switch back to master
git checkout master

# 6. Verify master is clean
git status
# "nothing to commit, working tree clean" ✓
```

### Scenario: "I deleted my feature branch by accident!"

```bash
# Find the commit hash
git reflog
# Output:
# abc1234 HEAD@{0}: checkout: switching to master
# def5678 HEAD@{1}: commit: my work
# ← This is it!

# Recreate the branch
git checkout -b feature/restored-work def5678

# Problem solved! ✓
```

### Scenario: "My changes got overwritten by git pull"

```bash
# Find your lost commits
git reflog

# Go back to a safe point
git checkout -b feature/recovery abc1234

# Merge your changes back in
git checkout master
git merge feature/recovery
```

---

## 💡 Pro Tips

1. **Commit message template for clarity:**
   ```
   [TYPE] Brief description
   
   More details if needed
   
   Related to: #issue-number
   ```
   
   Example:
   ```
   [FEATURE] Add OAuth2 authentication
   
   Implemented Google and GitHub Sign-In
   Added session management
   Updated user model schema
   
   Related to: #45
   ```

2. **Create meaningful branches:**
   ```
   ✓ feature/oauth2-authentication
   ✓ bugfix/memory-leak-in-model
   ✓ refactor/improve-ui-performance
   ✓ docs/api-documentation
   
   ✗ feature/stuff
   ✗ bugfix/fix
   ✗ test123
   ```

3. **Review PR titles:**
   ```
   ✓ "Add two-factor authentication to login flow"
   ✓ "Fix: Prevent SQL injection in search feature"
   ✓ "Refactor: Simplify model training pipeline"
   ✓ "Docs: Update API documentation"
   ```

4. **Use commit count as progress:**
   ```bash
   git log --oneline | head -20
   # 20 commits = good progress tracking
   ```

5. **See what you're about to push:**
   ```bash
   git log --oneline master..feature/your-branch
   # Shows commits to be pushed
   ```

---

## ✅ Ready for Team Collaboration!

Your Git and GitHub are fully configured. Print or bookmark this guide for quick reference!

Good luck building CyberShield AI with your team! 🚀

---

**Next Step:** Follow instructions in [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) to complete GitHub setup and invite team members.
