# Upload to GitHub

## Problem
GitHub web upload has a 100-file limit. This project has many files so you need Git.

## Solution: Install Git

### Step 1: Install Git
1. Download from: https://git-scm.com/downloads
2. Run installer with default options
3. Restart VS Code/terminal after installation

### Step 2: Push to GitHub
```bash
# Navigate to project folder
cd a:\Career\SkillSetu

git init
git add .
git commit -m "initial commit - SkillSetu AI"

# Create repo on github.com first, then:
git remote add origin https://github.com/YOUR-USERNAME/skillsetu.git
git branch -M main
git push -u origin main
```

## Alternative: GitHub Desktop
1. Download from: https://desktop.github.com
2. Sign in, add "SkillSetu" folder
3. Publish repository

## Note
The `.gitignore` file is already created to exclude:
- node_modules (800+ files)
- __pycache__ files
- .env and database files
- IDE settings