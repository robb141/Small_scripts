<#
.SYNOPSIS
    Encrypt config.ini using GPG (GNU Privacy Guard)
    
.DESCRIPTION
    Encrypts config.ini to config.ini.gpg using GPG symmetric encryption.
    The encrypted file can be safely pushed to GitHub.
    Anyone with the password can decrypt it on any machine.
    
.NOTES
    - Requires GPG to be installed (cross-platform)
    - macOS: brew install gnupg
    - Windows: https://gpg4win.org/
    - Linux: apt install gnupg / yum install gnupg
    - Password-protected encryption
    - Works on any device with GPG installed
    - Encrypted file: config.ini.gpg
    - Original config.ini will be deleted after encryption

.EXAMPLE
    .\Encrypt-Config.ps1
    # Prompts for password, encrypts to config.ini.gpg
#>

param(
    [string]$ConfigPath = "$PSScriptRoot/config.ini"
)

Write-Host "═" * 60
Write-Host "Config Encryption Tool (GPG - Multi-Device)"
Write-Host "═" * 60

# Check if GPG is installed
try {
    $gpgVersion = gpg --version 2>$null | Select-Object -First 1
    if (-not $gpgVersion) {
        throw "GPG not found"
    }
    Write-Host "✓ GPG found: $gpgVersion"
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

# Check if config.ini exists
if (-not (Test-Path $ConfigPath)) {
    Write-Error "config.ini not found at: $ConfigPath"
    exit 1
}

# Check if already encrypted
$encryptedPath = "$($ConfigPath).gpg"
if (Test-Path $encryptedPath) {
    Write-Host "⚠ Warning: $encryptedPath already exists"
    $response = Read-Host "Overwrite? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Cancelled."
        exit 0
    }
    Remove-Item $encryptedPath -Force
}

try {
    Write-Host ""
    Write-Host "Encrypting config.ini with GPG..."
    Write-Host "You will be prompted for a password (use a strong one!)"
    Write-Host ""
    
    # Encrypt using GPG symmetric encryption
    # -c = symmetric encryption
    # --batch = non-interactive
    # --yes = overwrite without asking
    gpg --symmetric --cipher-algo AES256 --output $encryptedPath $ConfigPath
    
    if (Test-Path $encryptedPath) {
        # Remove original
        Write-Host "Removing unencrypted config.ini..."
        Remove-Item $ConfigPath -Force
        
        Write-Host ""
        Write-Host "✓ Encryption successful!"
        Write-Host "  Encrypted file: config.ini.gpg"
        Write-Host "  Original file: deleted"
        Write-Host ""
        Write-Host "Next steps:"
        Write-Host "  1. Commit config.ini.gpg to GitHub"
        Write-Host "  2. To use on another device: run Decrypt-Config.ps1"
        Write-Host "  3. Enter the password you just set"
        Write-Host "═" * 60
    }
    else {
        Write-Error "Encryption failed - config.ini.gpg not created"
        exit 1
    }
    
}
catch {
    Write-Error "Encryption failed: $_"
    exit 1
}

