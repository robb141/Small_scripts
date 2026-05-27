# SortMedia - Media File Organizer

A PowerShell script that organizes media files into folders by year or holiday events.

## Overview

The refactored SortMedia project has been reorganized into a modular structure with configuration separated from code:

```
SortMedia/
├── SortMedia.ps1          # Main script
├── Encrypt-Config.ps1     # Encrypt config.ini before git push (GPG)
├── Decrypt-Config.ps1     # Decrypt config.ini.gpg after git pull (GPG)
├── config.template.ini    # Configuration template (for reference only)
├── config.ini.gpg         # Encrypted configuration (committed to git)
├── .gitignore             # Git configuration
└── README.md              # This file
```

**Note**: Uses GPG encryption (cross-platform, multi-device)

## Features

- **Holiday-based organization**: Files are sorted into folders named after holidays/events with date ranges
- **Fallback to yearly organization**: Files outside holiday ranges are sorted by year
- **Duplicate detection**: Identifies duplicate files by size and moves them to a delete folder
- **Conflict detection**: Flags files with same name but different size for manual review
- **Progress tracking**: Shows processing progress every N files
- **Flexible configuration**: All settings in `config.ini`, no code changes needed

## Configuration

The `config.ini` file is encrypted and not stored in plaintext. To configure:

1. **First time - create from template:**
```powershell
# Copy template as your working config
Copy-Item config.template.ini config.ini
```

2. **Edit `config.ini` with your settings:**
   - `[Paths]`: Set your source/destination folders
   - `[FileTypes]`: Customize file extensions (optional)
   - `[Processing]`: Adjust progress interval, logging (optional)
   - `[Holidays]`: Add or modify event date ranges

3. **Encrypt before committing:**
```powershell
.\Encrypt-Config.ps1
# Enter a strong password when prompted
```

4. **On other devices, decrypt after cloning/pulling:**
```powershell
.\Decrypt-Config.ps1
# Enter the same password you used above
```

**See `config.template.ini` for configuration format reference.**

### Configuration Sections

#### [Paths]
- `SourceFolder`: Where to read media files from
- `DestinationFolder`: Where to organize files to
- `ToDeleteFolder`: Where to move duplicate files
- `LogFolder`: Where to write logs and conflict reports

#### [FileTypes]
- `PhotoExtensions`: Comma-separated list of photo file extensions
- `VideoExtensions`: Comma-separated list of video file extensions

#### [Processing]
- `ProgressInterval`: Show progress every N files (default: 200)
- `LogDuplicates`: Write conflict details to log file (true/false)
- `OrganizeByCategory`: Not currently used (future feature)

#### [Holidays]
Define your events in format: `EventName=StartDate,EndDate`
- Dates in YYYY-MM-DD format
- End date is inclusive (becomes end of day)

## Usage

### Quick Start

```powershell
# 1. Install GPG (if not already installed)
# macOS:   brew install gnupg
# Windows: https://gpg4win.org/
# Linux:   apt install gnupg

# 2. Decrypt config (first time after cloning/pulling)
.\Decrypt-Config.ps1
# Enter password when prompted

# 3. Run the sorter
.\SortMedia.ps1
```

### Full Workflow

**First Time Setup:**
```powershell
# 1. Edit config.ini with your paths
# 2. Encrypt it
.\Encrypt-Config.ps1
# Enter a strong password when prompted

# 3. Commit encrypted config
git add config.ini.gpg .gitignore
git commit -m "Add encrypted config"
```

**Regular Usage (After Clone/Pull or on New Device):**
```powershell
# Always decrypt first
.\Decrypt-Config.ps1
# Enter the password you set during encryption

# Then run
.\SortMedia.ps1
```

### With Custom Config Path

```powershell
.\Decrypt-Config.ps1 -EncryptedPath "C:\path\to\config.ini.gpg"
.\SortMedia.ps1 -ConfigPath "C:\path\to\config.ini"
```

### Expected Output
```
════════════════════════════════════════════════════════
SortMedia - Organizing files...
Source: C:\path\to\source\folder
Destination: D:\path\to\destination\folder
════════════════════════════════════════════════════════
Found 36031 files to process.
Progress: 0 / 36031
Progress: 200 / 36031
...
════════════════════════════════════════════════════════
✓ Processing complete!
  Total processed: 36031
  Duplicates moved: 1234
  Manual review needed: 5
════════════════════════════════════════════════════════
```

## What Changed from Original

### Improvements
✓ **Removed code redundancies**:
  - Deleted commented-out code for category organization
  - Consolidated duplicate logic into single function
  - Removed unused file type checking

✓ **Configuration extraction**:
  - All paths, extensions, and holidays moved to `config.ini`
  - Easy to modify without editing PowerShell code

✓ **Better code organization**:
  - Helper functions for reusability
  - Clear separation of concerns
  - Improved readability with comments

✓ **Enhanced logging**:
  - Better progress indicators
  - Clearer output messages
  - Log file for manual review conflicts

✓ **Folder structure**:
  - Organized in dedicated `SortMedia/` folder
  - Separate config from script
  - Ready for version control

### Maintained Features
- All original holiday definitions preserved
- Same duplicate detection logic
- Same file organization structure
- Progress tracking with configurable interval

## Logs and Reports

- **Duplicates**: Moved to `ToDeleteFolder` with timestamp prefix
- **Conflicts**: Logged to `review.log` in `ToDeleteFolder` (if enabled)
- **Console output**: Real-time progress and summary statistics

## Security: Encrypted Configuration (GPG Multi-Device)

### Prerequisites

Install GPG on your system:

**macOS:**
```bash
brew install gnupg
```

**Windows:**
- Download from https://gpg4win.org/
- Run the installer

**Linux:**
```bash
sudo apt install gnupg    # Debian/Ubuntu
# or
sudo yum install gnupg    # CentOS/RHEL
```

### Setup (First Time)

1. **Edit your paths in `config.ini`** with your actual source/destination folders

2. **Encrypt the config:**
```powershell
.\Encrypt-Config.ps1
```
   - Prompts you for a password (use a strong one!)
   - Encrypts `config.ini` → `config.ini.gpg` using AES256
   - Deletes the unencrypted `config.ini`
   - Creates `config.ini.gpg` (safe to commit)

3. **Add to git and commit:**
```powershell
git add config.ini.gpg .gitignore
git commit -m "Add encrypted config"
git push
```

### Usage (Every Time You Clone/Pull or Switch Device)

1. **Decrypt the config:**
```powershell
.\Decrypt-Config.ps1
```
   - Prompts for the password you set during encryption
   - Creates `config.ini` from `config.ini.gpg`
   - Works on any device with GPG installed

2. **Run SortMedia:**
```powershell
.\SortMedia.ps1
```

### Important Notes

- ✅ **Works across devices**: Any machine with GPG installed + password
- ✅ **Safe for GitHub**: `config.ini.gpg` is committed, `config.ini` is `.gitignore`'d
- ✅ **Password-protected**: Uses AES256 encryption
- 🔑 **Remember your password**: Needed on every device to decrypt
- 📝 **Same password everywhere**: Use the same password you set during encryption

### For Multi-Device Setup

1. **Device A (your current machine):** Follow setup steps above
2. **Device B (new machine):**
   - Clone the repo
   - Install GPG
   - Run `.\Decrypt-Config.ps1`
   - Enter the password you used on Device A
   - Run `.\SortMedia.ps1`

All devices can use the same `config.ini.gpg` file!
