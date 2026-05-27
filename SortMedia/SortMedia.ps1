<#
.SYNOPSIS
    SortMedia - Organizes media files by year or holiday events
    
.DESCRIPTION
    Reads media files from source folder and organizes them into destination folder
    based on year or holiday date ranges defined in config.ini.
    Detects and handles duplicates.

.NOTES
    Configuration file: config.ini
    Logs: See LogFolder in config.ini
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\config.ini"
)

# ======================================================================
# HELPER FUNCTIONS
# ======================================================================

function Read-ConfigFile {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        Write-Error "Configuration file not found: $Path"
        exit 1
    }
    
    $config = @{}
    $currentSection = $null
    
    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        
        # Skip empty lines and comments
        if ([string]::IsNullOrEmpty($line) -or $line.StartsWith("#")) {
            return
        }
        
        # Check for section headers
        if ($line -match "^\[(.+)\]$") {
            $currentSection = $matches[1]
            $config[$currentSection] = @{}
        }
        elseif ($line -match "^(.+?)=(.*)$") {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            if ($currentSection) {
                $config[$currentSection][$key] = $value
            }
        }
    }
    
    return $config
}

function Test-FileExtension {
    param(
        [string]$Extension,
        [string]$ExtensionList
    )
    
    $extensions = $ExtensionList.Split(",") | ForEach-Object { $_.Trim().ToLower() }
    return $extensions -contains $Extension.ToLower()
}

function Get-HolidayFolder {
    param(
        [datetime]$FileDate,
        [hashtable]$Holidays
    )
    
    foreach ($Holiday in $Holidays.Keys) {
        $HolidayStart = [DateTime]$Holidays[$Holiday][0]
        $HolidayEnd = ([DateTime]$Holidays[$Holiday][1]).AddDays(1)
        
        if ($FileDate -ge $HolidayStart -and $FileDate -le $HolidayEnd) {
            return "$($HolidayStart.ToString("yyyyMM")) - $($HolidayEnd.ToString("yyyyMM")) $($Holiday)"
        }
    }
    
    return $null
}

function Get-TargetFolder {
    param(
        [datetime]$FileDate,
        [string]$DestinationFolder,
        [hashtable]$Holidays
    )
    
    $HolidayFolder = Get-HolidayFolder -FileDate $FileDate -Holidays $Holidays
    
    if ($HolidayFolder) {
        return Join-Path -Path $DestinationFolder -ChildPath $HolidayFolder
    }
    else {
        return Join-Path -Path $DestinationFolder -ChildPath $FileDate.Year
    }
}

function Move-OrLogDuplicate {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [string]$ToDeleteFolder,
        [bool]$LogDuplicates = $true
    )
    
    $ExistingFile = Get-Item -Path $DestinationPath
    
    if ($ExistingFile.Length -eq (Get-Item $SourcePath).Length) {
        # Duplicate - move to delete folder
        $deleteFileName = "$((Get-Date).ToString('yyyyMMddTHHmmssffff'))_$(Split-Path -Leaf $SourcePath)"
        Move-Item -Path $SourcePath -Destination (Join-Path $ToDeleteFolder $deleteFileName) -Force
        Write-Host "Deleted duplicate: $SourcePath"
        return $true
    }
    else {
        # Different file - flag for manual review
        Write-Host "⚠ Check file: $SourcePath (different from existing: $DestinationPath)"
        
        if ($LogDuplicates) {
            Add-Content (Join-Path $ToDeleteFolder "review.log") -Value "Check file: $SourcePath`nExisting: $DestinationPath`n---"
        }
        return $false
    }
}

# ======================================================================
# MAIN SCRIPT
# ======================================================================

# Load configuration
$config = Read-ConfigFile -Path $ConfigPath
$Paths = $config["Paths"]
$Processing = $config["Processing"]

$SourceFolder = $Paths["SourceFolder"]
$DestinationFolder = $Paths["DestinationFolder"]
$ToDeleteFolder = $Paths["ToDeleteFolder"]
$LogFolder = $Paths["LogFolder"]

$ProgressInterval = [int]$Processing["ProgressInterval"]
$LogDuplicates = [bool]::Parse($Processing["LogDuplicates"])

# Parse holidays from config
$Holidays = @{}
if ($config.ContainsKey("Holidays")) {
    foreach ($Holiday in $config["Holidays"].Keys) {
        $dates = $config["Holidays"][$Holiday].Split(",")
        $Holidays[$Holiday] = @($dates[0].Trim(), $dates[1].Trim())
    }
}

# Validate paths
@($SourceFolder, $DestinationFolder, $ToDeleteFolder, $LogFolder) | ForEach-Object {
    if (-not (Test-Path $_)) {
        Write-Error "Path not found: $_"
        exit 1
    }
}

Write-Host "═" * 60
Write-Host "SortMedia - Organizing files..."
Write-Host "Source: $SourceFolder"
Write-Host "Destination: $DestinationFolder"
Write-Host "═" * 60

# Get all files
$Files = Get-ChildItem -Path $SourceFolder -Recurse -File
Write-Host "Found $($Files.Count) files to process."

$processedCount = 0
$duplicateCount = 0
$conflictCount = 0

foreach ($File in $Files) {
    # Progress indicator
    if ($processedCount % $ProgressInterval -eq 0) {
        Write-Host "Progress: $processedCount / $($Files.Count)"
    }
    
    # Determine target folder
    $TargetFolder = Get-TargetFolder -FileDate $File.LastWriteTime -DestinationFolder $DestinationFolder -Holidays $Holidays
    
    # Create target folder if needed
    if (-not (Test-Path -Path $TargetFolder)) {
        New-Item -ItemType Directory -Path $TargetFolder -Force | Out-Null
    }
    
    $DestinationFile = Join-Path -Path $TargetFolder -ChildPath $File.Name
    
    # Handle existing files
    if (Test-Path -Path $DestinationFile) {
        if (Move-OrLogDuplicate -SourcePath $File.FullName -DestinationPath $DestinationFile -ToDeleteFolder $ToDeleteFolder -LogDuplicates $LogDuplicates) {
            $duplicateCount++
        }
        else {
            $conflictCount++
        }
    }
    else {
        # Move file
        try {
            Move-Item -Path $File.FullName -Destination $DestinationFile -ErrorAction Stop
        }
        catch {
            Write-Host "❌ Error moving file: $($File.FullName)"
            Write-Host "   Error: $_"
        }
    }
    
    $processedCount++
}

Write-Host "═" * 60
Write-Host "✓ Processing complete!"
Write-Host "  Total processed: $processedCount"
Write-Host "  Duplicates moved: $duplicateCount"
Write-Host "  Manual review needed: $conflictCount"
Write-Host "═" * 60
