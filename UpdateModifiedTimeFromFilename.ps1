<#
.SYNOPSIS
Updates file modified times from dates found in file names.

.DESCRIPTION
Scans SourceFolder recursively. If a file name contains a valid date such as
IMG-20210419.jpg, IMG_20210419.jpg, or photo_2021-04-19.jpg, the script sets the
file's LastWriteTime to that date. Files without a valid date in the name are
left unchanged.

Use -WhatIf to preview changes without updating files.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter()]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string] $SourceFolder = "C:\path\to\source\folder",

    [Parameter()]
    [string] $LogPath = "C:\path\to\log\file.log"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-DirectoryIfMissing {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return
    }

    if (-not (Test-Path -LiteralPath $Path -PathType Container) -and $PSCmdlet.ShouldProcess($Path, "Create directory")) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Write-RunLog {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Message
    )

    if ($WhatIfPreference) {
        return
    }

    $logFolder = Split-Path -Parent $LogPath
    New-DirectoryIfMissing -Path $logFolder

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -LiteralPath $LogPath -Value "[$timestamp] $Message"
}

function Get-DateFromFileName {
    param(
        [Parameter(Mandatory = $true)]
        [string] $FileName
    )

    $datePattern = "(?<!\d)(?<year>19\d{2}|20\d{2})[-_. ]?(?<month>0[1-9]|1[0-2])[-_. ]?(?<day>0[1-9]|[12]\d|3[01])(?!\d)"
    $matches = [regex]::Matches($FileName, $datePattern)

    foreach ($match in $matches) {
        $dateText = "{0}-{1}-{2}" -f $match.Groups["year"].Value, $match.Groups["month"].Value, $match.Groups["day"].Value
        $parsedDate = [datetime]::MinValue

        if ([datetime]::TryParseExact(
                $dateText,
                "yyyy-MM-dd",
                [Globalization.CultureInfo]::InvariantCulture,
                [Globalization.DateTimeStyles]::None,
                [ref] $parsedDate
            )) {
            return $parsedDate.Date
        }
    }

    return $null
}

$files = Get-ChildItem -LiteralPath $SourceFolder -Recurse -File
$stats = [ordered]@{
    Total       = $files.Count
    Updated     = 0
    AlreadySame = 0
    NoDate      = 0
    Failed      = 0
}

Write-Host "Found $($stats.Total) files in $SourceFolder."

for ($index = 0; $index -lt $files.Count; $index++) {
    $file = $files[$index]

    if ($index % 200 -eq 0) {
        Write-Progress -Activity "Updating modified times" -Status "Processing $index of $($files.Count)" -PercentComplete (($index / [Math]::Max($files.Count, 1)) * 100)
    }

    try {
        $dateFromName = Get-DateFromFileName -FileName $file.Name

        if ($null -eq $dateFromName) {
            $stats.NoDate++
            continue
        }

        $oldLastWriteTime = $file.LastWriteTime

        if ($oldLastWriteTime.Date -eq $dateFromName) {
            $stats.AlreadySame++
            continue
        }

        if ($PSCmdlet.ShouldProcess($file.FullName, "Set LastWriteTime to $($dateFromName.ToString("yyyy-MM-dd"))")) {
            $file.LastWriteTime = $dateFromName
        }

        $stats.Updated++
        Write-RunLog "Updated: $($file.FullName) from $($oldLastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")) to $($dateFromName.ToString("yyyy-MM-dd"))"
    }
    catch {
        $stats.Failed++
        Write-Warning "Failed to process $($file.FullName): $($_.Exception.Message)"
        Write-RunLog "Failed: $($file.FullName): $($_.Exception.Message)"
    }
}

Write-Progress -Activity "Updating modified times" -Completed

Write-Host "Modified time update finished."
Write-Host "Updated: $($stats.Updated)"
Write-Host "Already same date: $($stats.AlreadySame)"
Write-Host "No filename date: $($stats.NoDate)"
Write-Host "Failed: $($stats.Failed)"
