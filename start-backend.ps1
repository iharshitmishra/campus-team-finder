# Start Backend Script
$ErrorActionPreference = "Stop"

# Check if JDK 17 is in tools folder
$toolsDir = "$env:USERPROFILE\tools"
$jdkPath = Get-ChildItem "$toolsDir" -Filter "*corretto*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
if (-not $jdkPath) {
    $jdkPath = Get-ChildItem "$toolsDir" -Filter "*jdk*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
}

if ($jdkPath) {
    $env:JAVA_HOME = $jdkPath
    $env:PATH = "$jdkPath\bin;$env:PATH"
    Write-Host "Using Java from: $jdkPath" -ForegroundColor Green
}

# Check if Maven is in tools folder
$mvnPath = "$toolsDir\apache-maven-3.9.6\bin"
if (Test-Path "$mvnPath\mvn.cmd") {
    $env:PATH = "$mvnPath;$env:PATH"
    Write-Host "Using Maven from: $mvnPath" -ForegroundColor Green
}

Set-Location "$PSScriptRoot\backend"
Write-Host "Compiling and starting Javalin backend on http://localhost:7070..." -ForegroundColor Cyan
mvn clean compile exec:java
