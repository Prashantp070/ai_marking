param(
  [string]$pgUser = "postgres",
  [string]$pgPassword = "postgres",
  [string]$dbName = "markingdb"
)

$psqlPath = "C:\Program Files\PostgreSQL\16\bin\psql.exe"
if (Test-Path $psqlPath) {
  Write-Host "Creating database $dbName..."
  & $psqlPath -U $pgUser -c "CREATE DATABASE $dbName;" 2>$null
  Write-Host "Done. If error about already exists, ignore."
} else {
  Write-Host "psql not found. Please install PostgreSQL and add psql to PATH, or run manually:"
  Write-Host "  psql -U postgres"
  Write-Host "  CREATE DATABASE markingdb;"
}

