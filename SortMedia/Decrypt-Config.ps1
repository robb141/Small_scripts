<#
.SYNOPSIS
    Decrypt config.ini.gpg back to config.ini
    
.DESCRIPTION
    Decrypts config.ini.gpg using GPG.
    Works on any device with GPG installed and the correct password.
    Run this before executing SortMedia.ps1.
    
.NOTES
    - Requires GPG to be installed
    - Works on macOS, Windows, Linux
    - Creates config.ini in current directory
    - config.ini is git-ignored (safe to have unencrypted locally)
    - You'll be prompted for the password that was set during encryption

.EXAMPLE
    .\Decrypt-Config.ps1
    # Prompts for password, creates config.ini
#>

param(
    [string]$EncryptedPath = "$PSScriptRoot/config.ini.gpg"
)

Write-Host "═" * 60
Write-Host "Config Decryption Tool (GPG - Multi-Device)"
Write-Host "═" * 60

# Check if GPG is installed
try {
    $gpgVersion = gpg --version 2>$null | Select-Object -First 1
    if (-not $gpgVersion) {
        throw "GPG not found"
    }
}
catch {
    Write-Error "GPG is not installed!"
    Write-Host ""
    Write-Host "Install GPG:"
    Write-Host "  macOS:   brew install gnupg"
    Write-Host "  Windows: https://gpg4win.org/"
    Write-Host "  Linux:   apt install gnupg  (or yum install gnupg)"
    Write-Host ""
    exit 1
}

# Check if encrypted file exists
if (-not (Test-Path $EncryptedPath)) {
    Write-Error "config.ini.gpg not found at: $EncryptedPath"
    exit 1
}

$configPath = [System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($EncryptedPath), "config.ini")

# Check if config.ini already exists
if (Test-Path $configPath) {
    Write-Host "✓ config.ini already exists - no decryption needed"
    Write-Host "  Ready to use with SortMedia.ps1"
    Write-Host "═" * 60
    exit 0
}

try {
    Write-Host "Decrypting config.ini.gpg..."
    Write-Host "You will be prompted for the password."
    Write-Host ""
    
    # Decrypt using GPG
    gpg --decrypt --output $configPath $EncryptedPath
    
    if (Test-Path $configPath) {
        Write-Host ""
        Write-Host "✓ Decryption successful!"
        Write-Host "  Config file: config.ini"
        Write-Host "  Ready to use with SortMedia.ps1"
        Write-Host "═" * 60
    }
    else {
        Write-Error "Decryption failed - config.ini not created"
        exit 1
    }
    
}
catch {
    Write-Error "Decryption failed: $_"
    Write-Host ""
    Write-Host "Possible causes:"
    Write-Host "  - Wrong password"
    Write-Host "  - Corrupted encrypted file"
    Write-Host "  - GPG not properly installed"
    exit 1
}

