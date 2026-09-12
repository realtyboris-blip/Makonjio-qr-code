# run.ps1 - Generate the QR code
# Usage: .\run.ps1

Write-Host ""
Write-Host "=== Boris QR Code Generator ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip install failed. Make sure Python is on your PATH." -ForegroundColor Red
    exit 1
}

Write-Host "      Dependencies ready." -ForegroundColor Green
Write-Host ""

Write-Host "[2/2] Generating QR code..." -ForegroundColor Yellow
python main.py

Write-Host ""
Write-Host "Done! Your QR code is in output/boris_qr.png" -ForegroundColor Green
