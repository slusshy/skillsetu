Remove-Item .git/index.lock -Force
git add .
git commit -m "Add fixes for Railway deployment"
git pull origin main --rebase
git push -u origin main