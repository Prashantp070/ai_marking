Write-Host "Starting FastAPI backend server..."
$pythonExe = "C:/Python313/python.exe"
$apiPath = "$PSScriptRoot\apps\api"

Set-Location $apiPath
Write-Host "Working directory: $(Get-Location)"

# Install dependencies
Write-Host "Installing dependencies..."
& $pythonExe -m pip install -q -r requirements.txt 2>&1 | Where-Object {$_ -notmatch "already satisfied"}

# Start server
Write-Host "Starting uvicorn server on http://127.0.0.1:8000"
& $pythonExe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

