$env:N8N_USER_FOLDER = "C:\Radar\n8n\instance"
$env:GENERIC_TIMEZONE = "America/Bogota"
$env:TZ = "America/Bogota"

$env:N8N_HOST = "127.0.0.1"
$env:N8N_PORT = "5678"
$env:N8N_PROTOCOL = "http"

$env:N8N_DIAGNOSTICS_ENABLED = "false"
$env:N8N_PERSONALIZATION_ENABLED = "false"

Set-Location "C:\Radar\n8n"

Write-Host ""
Write-Host "============================================"
Write-Host " RADAR"
Write-Host " n8n Automation Engine"
Write-Host "============================================"
Write-Host ""
Write-Host "Local address:"
Write-Host "http://127.0.0.1:5678"
Write-Host ""
Write-Host "Keep this window OPEN while RADAR is running."
Write-Host ""

npm start
