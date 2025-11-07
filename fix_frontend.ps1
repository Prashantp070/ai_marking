Write-Host "Cleaning existing Node processes..."
taskkill /F /IM node.exe /T > $null 2>&1

Write-Host "Removing node_modules and lock files..."
Remove-Item -Path "apps\web\node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "apps\web\package-lock.json" -Force -ErrorAction SilentlyContinue

Write-Host "Changing directory to apps/web..."
Set-Location "apps\web"

Write-Host "Cleaning npm cache..."
npm cache clean --force

Write-Host "Installing frontend dependencies..."
npm install react react-dom @headlessui/react vite @vitejs/plugin-react --save-dev

Write-Host "Node modules reinstalled successfully."
Write-Host "Starting Vite dev server..."
npm run dev
