# Fix Git Lock File Error

Another git process is running or the lock file is stale.

## Solution

1. Close all other terminals/IDEs that might be running git in this folder
2. Delete the lock file:
   ```bash
   rm -f .git/index.lock
   ```
   On Windows:
   ```bash
   del .git\index.lock
   ```

3. Then continue with git commands:
   ```bash
   git add .
   git commit -m "Add fixes for Railway deployment"
   git pull origin main --rebase
   git push -u origin main