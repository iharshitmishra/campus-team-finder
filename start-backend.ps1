# Start Backend Script
$ErrorActionPreference = "Stop"

$toolsDir = "$env:USERPROFILE\tools"

# 1. Locate Java JDK
$jdkPath = Get-ChildItem "$toolsDir" -Filter "*jdk*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
if (-not $jdkPath) {
    $jdkPath = Get-ChildItem "$toolsDir" -Filter "*corretto*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
}
if ($jdkPath) {
    $env:JAVA_HOME = $jdkPath
    $env:PATH = "$jdkPath\bin;$env:PATH"
    Write-Host "[OK] Using Java from: $jdkPath" -ForegroundColor Green
}

# 2. Locate Apache Maven
$mvnDir = Get-ChildItem "$toolsDir" -Filter "*apache-maven*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
if ($mvnDir -and (Test-Path "$mvnDir\bin\mvn.cmd")) {
    $env:PATH = "$mvnDir\bin;$env:PATH"
    Write-Host "[OK] Using Maven from: $mvnDir\bin" -ForegroundColor Green
}

Set-Location "$PSScriptRoot\backend"
Write-Host "Starting Javalin backend on http://localhost:7070..." -ForegroundColor Cyan
mvn clean compile exec:java


