$env:N8N_USER_FOLDER = "C:\Radar\n8n\instance"
$env:GENERIC_TIMEZONE = "America/Bogota"
$env:TZ = "America/Bogota"

$env:N8N_HOST = "127.0.0.1"
$env:N8N_PORT = "5678"
$env:N8N_PROTOCOL = "http"

$env:N8N_DIAGNOSTICS_ENABLED = "false"
$env:N8N_PERSONALIZATION_ENABLED = "false"
$env:N8N_VERSION_NOTIFICATIONS_ENABLED = "false"
$env:N8N_TEMPLATES_ENABLED = "false"

# 1. Start RADAR App Server (port 8080) if not running
$existingApp = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if (-not $existingApp) {
    Write-Host "Iniciando servidor de aplicaciones RADAR (Puerto 8080)..."
    Start-Process -FilePath "python" -ArgumentList "C:\Radar\app\server.py" -WindowStyle Hidden
    Start-Sleep -Seconds 2
}

# 2. Get Local IP for Mobile Access
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254*" } | Select-Object -First 1).IPAddress
if (-not $localIp) { $localIp = "127.0.0.1" }

Write-Host ""
Write-Host "========================================================"
Write-Host "  RADAR - MOTOR DE OPORTUNIDADES E INGRESOS"
Write-Host "========================================================"
Write-Host ""
Write-Host "  [1] DASHBOARD DE INGRESOS & PITCHES:"
Write-Host "      Local PC:        http://127.0.0.1:8080"
Write-Host "      Móvil (Wi-Fi):   http://$($localIp):8080"
Write-Host ""
Write-Host "  [2] MOTOR n8n AUTOMATION:"
Write-Host "      Editor n8n:      http://127.0.0.1:5678"
Write-Host ""
Write-Host "  Mantén esta ventana ABIERTA mientras utilices RADAR."
Write-Host "========================================================"
Write-Host ""

# 3. Open Dashboard in Browser
Start-Process "http://127.0.0.1:8080"

# 4. Start n8n engine
Set-Location "C:\Radar\n8n"
npm start
