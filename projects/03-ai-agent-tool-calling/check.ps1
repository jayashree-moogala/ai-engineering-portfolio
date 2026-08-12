# Project quality checks for Project 03
# Run from the project root:
#   .\check.ps1

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Formatting with Black..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
black app tests

if ($LASTEXITCODE -ne 0) {
    Write-Host "Black formatting failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Running Ruff..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
ruff check app tests

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ruff checks failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Running Pytest..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pytest failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "All checks passed!" -ForegroundColor Green
Write-Host "Ready to commit and push." -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
