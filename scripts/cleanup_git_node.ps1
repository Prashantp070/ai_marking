Write-Host "Removing apps/web/node_modules from git tracking..."

git rm -r --cached apps/web/node_modules 2>$null

git add .gitignore

git commit -m "Remove node_modules and add .gitignore" || Write-Host "Nothing to commit."

