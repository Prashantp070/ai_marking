# Frontend startup script
$webPath = "$PSScriptRoot\apps\web"
Set-Location $webPath
Write-Host "Starting frontend on http://localhost:5173"
npm run dev
