Write-Host "Stopping node processes (if any)..."
taskkill /F /IM node.exe /T > $null 2>&1

Write-Host "Removing node_modules and package-lock in apps/web..."
Remove-Item -Path "apps\web\node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "apps\web\package-lock.json" -Force -ErrorAction SilentlyContinue

Write-Host "Changing directory to apps/web..."
Push-Location "apps\web"

Write-Host "Cleaning npm cache..."
npm cache clean --force

Write-Host "Installing frontend dependencies..."
npm install

Write-Host "Starting Vite dev server..."
npm run dev

Pop-Location
