# run.ps1 - One-command launcher for the custom QR landing page
# Usage: .\run.ps1

Write-Host ""
Write-Host "=== Custom QR Code Launcher ===" -ForegroundColor Cyan
Write-Host ""

# 1. Install / update dependencies
Write-Host "[1/2] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip install failed. Make sure Python is on your PATH." -ForegroundColor Red
    exit 1
}

Write-Host "      Dependencies ready." -ForegroundColor Green
Write-Host ""

# 2. Start the app (Flask + ngrok + QR generation)
Write-Host "[2/2] Starting server and generating QR..." -ForegroundColor Yellow
Write-Host "      Local preview : http://localhost:5000" -ForegroundColor Gray
Write-Host "      QR image will be saved to output/boris_qr.png" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

python main.py
