# Start Frontend Script
$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\frontend"
Write-Host "Starting Vite frontend dev server..." -ForegroundColor Cyan
npm run dev
