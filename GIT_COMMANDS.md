# Git Commands Reference

## Your Repository
**GitHub URL:** https://github.com/janhavishedge2008-stack/waste-management-system

---

## Clone Repository (On New Computer)

```bash
git clone https://github.com/janhavishedge2008-stack/waste-management-system.git
cd waste-management-system
```

---

## Daily Git Workflow

### 1. Check Status
See what files have changed:
```bash
git status
```

### 2. Add Changes
Add all changed files:
```bash
git add .
```

Add specific file:
```bash
git add filename.py
```

### 3. Commit Changes
Save changes with a message:
```bash
git commit -m "Description of what you changed"
```

Examples:
```bash
git commit -m "Added new feature"
git commit -m "Fixed bug in pickup form"
git commit -m "Updated README"
```

### 4. Push to GitHub
Upload your changes:
```bash
git push
```

First time pushing a new branch:
```bash
git push -u origin main
```

### 5. Pull from GitHub
Download latest changes:
```bash
git pull
```

---

## Branch Management

### View Branches
```bash
git branch
```

### Create New Branch
```bash
git branch feature-name
```

### Switch Branch
```bash
git checkout feature-name
```

### Create and Switch in One Command
```bash
git checkout -b feature-name
```

### Merge Branch
```bash
git checkout main
git merge feature-name
```

### Delete Branch
```bash
git branch -d feature-name
```

---

## View History

### View Commit History
```bash
git log
```

### View Short History
```bash
git log --oneline
```

### View Last 5 Commits
```bash
git log -5
```

---

## Undo Changes

### Discard Changes in File (Before Commit)
```bash
git checkout -- filename.py
```

### Unstage File (After git add)
```bash
git reset filename.py
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Undo Last Commit (Discard Changes)
```bash
git reset --hard HEAD~1
```

---

## Remote Repository

### View Remote URL
```bash
git remote -v
```

### Change Remote URL
```bash
git remote set-url origin https://github.com/username/repo.git
```

### Add Remote
```bash
git remote add origin https://github.com/username/repo.git
```

---

## Useful Commands

### View Differences
See what changed:
```bash
git diff
```

### View Differences for Specific File
```bash
git diff filename.py
```

### Stash Changes (Save for Later)
```bash
git stash
```

### Apply Stashed Changes
```bash
git stash pop
```

### View Stash List
```bash
git stash list
```

---

## Complete Setup on New Computer

```bash
# 1. Clone repository
git clone https://github.com/janhavishedge2008-stack/waste-management-system.git
cd waste-management-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env
# Edit .env with your settings

# 6. Run migrations
python manage.py migrate

# 7. Load initial data (if setup.py exists)
python setup.py

# 8. Create superuser
python manage.py createsuperuser

# 9. Start server
python manage.py runserver
```

---

## Common Workflows

### Making Changes and Pushing

```bash
# 1. Make your code changes in editor

# 2. Check what changed
git status

# 3. Add all changes
git add .

# 4. Commit with message
git commit -m "Added new feature"

# 5. Push to GitHub
git push
```

### Working with Team

```bash
# 1. Pull latest changes before starting work
git pull

# 2. Make your changes

# 3. Add and commit
git add .
git commit -m "Your changes"

# 4. Pull again (in case someone else pushed)
git pull

# 5. Push your changes
git push
```

### Creating a Feature

```bash
# 1. Create new branch
git checkout -b feature-name

# 2. Make changes

# 3. Commit changes
git add .
git commit -m "Added feature"

# 4. Push branch to GitHub
git push -u origin feature-name

# 5. Create Pull Request on GitHub

# 6. After merge, switch back to main
git checkout main
git pull
```

---

## Git Configuration

### Set Your Name and Email
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### View Configuration
```bash
git config --list
```

---

## Troubleshooting

### Authentication Issues
If asked for password, use Personal Access Token instead:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Use token as password

### Merge Conflicts
```bash
# 1. Pull latest changes
git pull

# 2. If conflict, open conflicted files
# 3. Look for <<<<<<< and >>>>>>> markers
# 4. Edit file to resolve conflict
# 5. Add resolved file
git add filename.py

# 6. Commit
git commit -m "Resolved merge conflict"

# 7. Push
git push
```

### Reset to GitHub Version
```bash
git fetch origin
git reset --hard origin/main
```

---

## .gitignore

Files that won't be pushed to GitHub (already configured):

```
*.pyc
__pycache__/
db.sqlite3
.env
media/
staticfiles/
*.log
.DS_Store
venv/
env/
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `git status` | Check status |
| `git add .` | Add all changes |
| `git commit -m "msg"` | Commit changes |
| `git push` | Push to GitHub |
| `git pull` | Pull from GitHub |
| `git clone URL` | Clone repository |
| `git branch` | List branches |
| `git checkout -b name` | Create new branch |
| `git log` | View history |
| `git diff` | View changes |

---

## Your Project Specific Commands

### Start Development
```bash
cd C:\Users\LENOVO\Desktop\new
venv\Scripts\activate
python manage.py runserver
```

### After Making Changes
```bash
git add .
git commit -m "Description of changes"
git push
```

### Update from GitHub
```bash
git pull
python manage.py migrate  # If database changes
```

---

## GitHub Repository Links

- **Repository:** https://github.com/janhavishedge2008-stack/waste-management-system
- **Clone URL:** https://github.com/janhavishedge2008-stack/waste-management-system.git
- **Issues:** https://github.com/janhavishedge2008-stack/waste-management-system/issues
- **Pull Requests:** https://github.com/janhavishedge2008-stack/waste-management-system/pulls

---

## Tips

1. **Commit often** - Small, frequent commits are better than large ones
2. **Write clear commit messages** - Describe what and why
3. **Pull before push** - Always pull latest changes before pushing
4. **Use branches** - Create branches for new features
5. **Don't commit secrets** - Never commit .env or passwords
6. **Review before commit** - Use `git status` and `git diff`

---

## Need Help?

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf
