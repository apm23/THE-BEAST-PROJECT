param(
    [Parameter(Mandatory = $true)]
    [string]$GameDir
)

$ErrorActionPreference = 'Stop'

$sourceDir = Join-Path $GameDir 'ph_ft\source'
if (-not (Test-Path $sourceDir)) {
    throw "Could not find ph_ft\source under: $GameDir"
}

$pakFiles = Get-ChildItem -Path $sourceDir -Filter 'data*.pak' -File | Sort-Object Name
if (-not $pakFiles) {
    throw "No data*.pak files found in $sourceDir"
}

$root = Split-Path -Parent $PSScriptRoot
$outDir = Join-Path $root 'local_baseline'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$allPaths = New-Object System.Collections.Generic.List[string]

function Get-ArchivePaths([string]$Archive) {
    $sevenZipCandidates = @(
        (Get-Command 7z.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    ) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

    if ($sevenZipCandidates.Count -gt 0) {
        $sevenZip = $sevenZipCandidates[0]
        $lines = & $sevenZip l -slt -- $Archive
        return $lines |
            Where-Object { $_ -like 'Path = *' } |
            ForEach-Object { $_.Substring(7).Trim() }
    }

    $tar = Get-Command tar.exe -ErrorAction SilentlyContinue
    if ($tar) {
        try {
            return & $tar.Source -tf $Archive
        }
        catch {
            # fall through to clear error below
        }
    }

    throw "Need 7-Zip (recommended) or a tar.exe build capable of listing this PAK. Install 7-Zip and rerun."
}

foreach ($pak in $pakFiles) {
    Write-Host "Listing $($pak.Name)..."
    $paths = Get-ArchivePaths $pak.FullName
    foreach ($p in $paths) {
        if ($p) {
            $allPaths.Add("$($pak.Name)`t$p")
        }
    }
}

$fullList = Join-Path $outDir 'all_archive_paths.txt'
$allPaths | Set-Content -Encoding UTF8 $fullList

$pattern = '(?i)(inventory|weapon|rarity|quality|affix|loot|blueprint|craft|upgrade|item|human|biter|viral|infected|container).*(\.scr|\.loot|\.def|\.xml|\.json)$'
$relevant = $allPaths | Where-Object { $_ -match $pattern } | Sort-Object -Unique
$relevantList = Join-Path $outDir 'relevant_file_list.txt'
$relevant | Set-Content -Encoding UTF8 $relevantList

$summary = Join-Path $outDir 'baseline_summary.txt'
@(
    "GameDir=$GameDir",
    "SourceDir=$sourceDir",
    "PAKs=$($pakFiles.Name -join ',')",
    "AllPathCount=$($allPaths.Count)",
    "RelevantPathCount=$($relevant.Count)",
    "Generated=$(Get-Date -Format o)"
) | Set-Content -Encoding UTF8 $summary

Write-Host ''
Write-Host 'Baseline listing complete.'
Write-Host "Relevant list: $relevantList"
Write-Host "Summary:       $summary"
Write-Host ''
Write-Host 'Do NOT commit local_baseline; it is intentionally gitignored.'
