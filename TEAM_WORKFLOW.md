# CyberShield AI - Team Git Workflow Quick Start

## ✅ Status: Repository Initialized Locally

Your Git repository has been initialized with the initial commit. Now follow these steps to get your team set up!

---

## 🚀 STEP 1: Project Owner - Connect to GitHub

### 1.1 Create GitHub Repository

1. **Go to [github.com](https://github.com)** and log in
2. **Click `+` icon** (top right corner) → Select **"New repository"**
3. **Fill in these details:**
   - **Repository name:** `cybershield-ai`
   - **Description:** "Advanced AI-powered security detection system with dual capabilities for detecting phishing URLs and fake/spam messages"
   - **Visibility:** Select **Public** (for team collaboration) or **Private** (invitation only)
   - **Do NOT check:** "Initialize this repository with a README"
   - **Do NOT add** .gitignore or license (already configured)

4. **Click "Create repository"**

### 1.2 Connect Local Repository to GitHub

After creating the repository, GitHub shows you a page. Copy the **HTTPS URL** (looking like: `https://github.com/yourusername/cybershield-ai.git`)

Run this command in your terminal:

```bash
cd c:\Users\DELL\OneDrive\Desktop\cyber_detection\cybercrime-detection

git remote add origin https://github.com/yourusername/cybershield-ai.git
```

**Replace `yourusername` with your actual GitHub username!**

### 1.3 Verify Remote Connection

```bash
git remote -v
```

**Expected output:**
```
origin  https://github.com/yourusername/cybershield-ai.git (fetch)
origin  https://github.com/yourusername/cybershield-ai.git (push)
```

### 1.4 Push to GitHub

```bash
git push -u origin master
```

**First time?** GitHub will ask for authentication:
- **Option A:** Use GitHub Personal Access Token (recommended)
- **Option B:** Use GitHub CLI for authentication

### 1.5 Create GitHub Personal Access Token (PAT)

If GitHub asks for password:

1. Go to **GitHub Settings** → **Developer settings** → **Personal access tokens**
2. Click **"Generate new token"**
3. **Token name:** "Git CLI"
4. **Expiration:** 30 days (or longer)
5. **Scopes:** Check `repo` (full control of repositories)
6. Click **"Generate token"**
7. **Copy and save the token securely** ⚠️

Use this token as your password when Git prompts.

### 1.6 Verify Push Success

✅ Go to your GitHub repo URL and verify:
- All files are visible
- Commit history shows your initial commit
- Branches section shows `master`

---

## 📥 STEP 2: Team Members - Clone Repository

Each team member should run:

```bash
# Navigate to desired location
cd C:\Users\YourName\Desktop

# Clone the repository
git clone https://github.com/yourusername/cybershield-ai.git

# Navigate into project
cd cybershield-ai

# View project files
dir
```

This downloads the complete project with full history.

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔄 STEP 3: Everyone - Daily Workflow

### A. Start Your Day - Get Latest Changes

```bash
git checkout master
git pull origin master
```

This downloads any changes pushed by teammates.

### B. Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name
```

**Good branch names:**
```
feature/phishing-detection-v2
feature/add-user-dashboard
bugfix/accuracy-calculation-error
feature/message-encryption
hotfix/critical-security-patch
```

### C. Make Changes

Edit files in VS Code. For example:
- Modify `app.py` to add new routes
- Update `feature_extraction.py` for better model
- Edit templates for UI improvements

### D. Save Your Work to Git

```bash
# Check what changed
git status

# See detailed changes
git diff

# Stage all changes
git add .

# Or stage specific file
git add app.py

# Create commit (save point)
git commit -m "Your descriptive message"
```

**Good commit messages:**
```
✓ "Add authentication bypass fix for OAuth2 login"
✓ "Improve phishing model accuracy from 92% to 96%"
✓ "Refactor URL feature extraction for better performance"
✓ "Update requirements.txt with new dependencies"

✗ "Fix bug"
✗ "Changes made"
✗ "Update"
```

### E. Upload Your Branch to GitHub

```bash
git push -u origin feature/your-feature-name
```

(First time pushing new branch, use `-u` to set upstream)

### F. Create Pull Request on GitHub

1. Go to your GitHub repository
2. GitHub shows: **"Compare & pull request"** button
   - Or click **"Pull requests"** → **"New pull request"**
3. **Select branches:** your feature branch → `master`
4. **Add title:** "Add OAuth2 authentication to login"
5. **Add description:**
   ```
   ## What changed?
   - Implemented OAuth2 for secure authentication
   - Added Google Sign-In option
   - Updated login.html with new button
   
   ## Why?
   - Improves security with industry standard
   - Easier for users to log in
   
   ## Testing
   - Tested with Google account ✓
   - Tested with GitHub account ✓
   - No breaking changes ✓
   ```
6. **Click "Create pull request"**

### G. Code Review Process

**Teammates:**
- Review code changes
- Leave comments on specific lines (click line number)
- Request changes or approve

**You:**
- Respond to comments
- Make requested changes:
  ```bash
  git add .
  git commit -m "Address review feedback"
  git push origin feature/your-feature-name
  ```

### H. Merge to Master

Once approved:
1. Click **"Merge pull request"** on GitHub
2. Confirm merge

### I. Sync Local Repository

```bash
# Switch to master  
git checkout master

# Download merged changes
git pull origin master

# Delete old feature branch (keep clean)
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## 🔥 Common Situations

### I made changes but forgot to create a branch

```bash
# Check current branch
git status

# Stash changes temporarily
git stash

# Create and switch to new branch
git checkout -b feature/my-feature

# Apply changes
git stash pop

# Now commit normally
git add .
git commit -m "Your message"
git push -u origin feature/my-feature
```

### I want to see what changed from last commit

```bash
# Before staging
git diff

# After staging
git diff --staged

# Between branches
git diff master feature/my-feature
```

### Someone pushed changes and I need them

```bash
git pull origin master
```

If conflicts occur, see **Merge Conflicts** section below.

### I committed to wrong branch

```bash
# Check current state
git log --oneline -3

# Reset to before bad commit (keeps changes)
git reset --soft HEAD~1

# Switch to correct branch
git checkout -b correct-branch

# Commit properly
git commit -m "Correct message"
```

### I want to undo my last commit

```bash
# Soft undo (keep changes)
git reset --soft HEAD~1

# Or hard undo (delete changes) ⚠️
git reset --hard HEAD~1
```

---

## 🚨 Resolving Merge Conflicts

### What causes conflicts?

Two developers edit the same file at the same location.

### How to fix:

**1. When pulling changes:**
```bash
git pull origin master
```

**2. Git marks conflicts in your files:**
```
<<<<<<< HEAD
    return simple_detection(url)
=======
    return advanced_detection(url)
>>>>>>> feature/message-detection-v2
```

**3. In VS Code:**
- Conflicted files show red dot
- Blue buttons appear:
  - **"Accept Current Change"** - Keep your version
  - **"Accept Incoming Change"** - Use their version  
  - **"Accept Both Changes"** - Keep both versions
  - **"Compare Changes"** - View side-by-side

**4. Choose the correct code:**
- Delete the `<<<<<<<`, `=======`, `>>>>>>>` markers
- Keep the code that makes sense
- Or combine both versions if needed

**5. Commit the merge:**
```bash
git add .
git commit -m "Resolve merge conflict in app.py"
git push origin feature/my-branch
```

---

## 📋 Command Cheat Sheet

| What you want | Command |
|---|---|
| Check status | `git status` |
| See recent commits | `git log --oneline -5` |
| See branches | `git branch -a` |
| Create branch | `git checkout -b feature/name` |
| Switch branch | `git checkout branch-name` |
| Save changes | `git add .` then `git commit -m "msg"` |
| Upload to GitHub | `git push origin branch-name` |
| Download from GitHub | `git pull origin master` |
| View changes | `git diff` |
| Delete branch | `git branch -d branch-name` |
| Undo last commit | `git reset --soft HEAD~1` |

---

## 🎯 Best Practices for Team Success

### ✅ DO:
- **Pull before starting work:** `git pull origin master`
- **Use descriptive branch names:** `feature/add-2fa-authentication`
- **Commit frequently** with clear messages
- **Test your code** before pushing
- **Keep PRs small** (< 400 lines of code)
- **Review teammates' code** - learn from each other
- **Respond to feedback** - it makes code better
- **Pull latest changes** regularly to avoid conflicts

### ❌ DON'T:
- Don't push directly to `master` without PR review
- Don't commit large downloaded models (> 100MB)
- Don't hardcode credentials:
  ```
  ❌ password = "Mahi@123456"
  ✅ password = os.getenv('DB_PASSWORD')
  ```
- Don't merge your own pull request (let others review)
- Don't force push (`git push -f`) unless you know consequences
- Don't commit `.env` files or API keys
- Don't ignore merge conflicts - resolve them!

### 🔐 Security Checklist

Before pushing code, ensure:
- [ ] No hardcoded passwords or API keys
- [ ] No `.env` files committed
- [ ] No sensitive data in comments
- [ ] No credentials in commit messages
- [ ] Third-party API keys not exposed
- [ ] Database passwords not in code

---

## 📞 Getting Help

### GitHub Issues (Track bugs and features)
1. Go to **Issues** tab in repository
2. Click **"New issue"**
3. Describe the bug or feature request
4. Assign to team member if needed
5. Add labels: `bug`, `feature`, `documentation`, etc.

### Pull Request Comments
- Click a line number to comment on specific code
- Use `@username` to mention someone
- Suggest code changes directly

### GitHub Discussions
- Go to **Discussions** tab
- Ask questions about the project
- Share ideas and best practices

---

## 📚 Additional Learning Resources

- **Git Basics:** https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control
- **GitHub Docs:** https://docs.github.com/
- **GitHub Guides:** https://www.youtube.com/githubguides
- **Interactive Git Tutorial:** https://learngitbranching.js.org/

---

## ✨ Your Next Steps

1. **Project Owner (You):**
   - [ ] Create GitHub repository
   - [ ] Connect local repository to GitHub
   - [ ] Push to GitHub
   - [ ] Invite team members

2. **Team Members:**
   - [ ] Clone repository
   - [ ] Set up Python environment
   - [ ] Configure Git (name/email)
   - [ ] Create first feature branch

3. **Everyone:**
   - [ ] Read this guide completely
   - [ ] Understand the workflow
   - [ ] Ask questions!

---

## 🎉 Ready to Collaborate!

Once everyone has cloned the repository and understands this workflow, your team is ready to build amazing features on CyberShield AI!

**Happy coding! 🚀**

---

## Questions?

Refer to [GIT_GITHUB_GUIDE.md](GIT_GITHUB_GUIDE.md) for comprehensive documentation or ask your team lead!
