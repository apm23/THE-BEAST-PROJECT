param(
    [string]$GameDir,
    [switch]$NoGui,
    [switch]$SkipHashValidation
)

$ErrorActionPreference = 'Stop'

function Find-7Zip {
    $candidates = @(
        (Get-Command 7z.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    ) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique
    if ($candidates.Count -gt 0) { return $candidates[0] }
    return $null
}

function Get-SteamRoots {
    $roots = @()
    try {
        $p = (Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath
        if ($p) { $roots += $p }
    } catch {}
    try {
        $p = (Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath
        if ($p) { $roots += $p }
    } catch {}
    foreach ($p in @("${env:ProgramFiles(x86)}\Steam", "${env:ProgramFiles}\Steam", 'C:\Steam')) {
        if ($p -and (Test-Path $p)) { $roots += $p }
    }
    return @($roots | Select-Object -Unique)
}

function Get-SteamLibraries {
    $libs = @()
    foreach ($root in Get-SteamRoots) {
        if (Test-Path $root) { $libs += $root }
        $vdf = Join-Path $root 'steamapps\libraryfolders.vdf'
        if (Test-Path $vdf) {
            try {
                $txt = Get-Content -Raw $vdf
                foreach ($m in [regex]::Matches($txt, '"path"\s*"([^"]+)"')) {
                    $p = $m.Groups[1].Value -replace '\\\\','\'
                    if (Test-Path $p) { $libs += $p }
                }
            } catch {}
        }
    }
    return @($libs | Select-Object -Unique)
}

function Auto-FindGame {
    $games = @()
    foreach ($lib in Get-SteamLibraries) {
        $g = Join-Path $lib 'steamapps\common\Dying Light The Beast'
        if (Test-Path (Join-Path $g 'ph_ft\source\data0.pak')) { $games += $g }
    }
    $games = @($games | ForEach-Object { [IO.Path]::GetFullPath($_).TrimEnd('\') } | Select-Object -Unique)
    if ($games.Count -eq 1) { return $games[0] }
    if ($games.Count -gt 1) {
        throw "Lebih dari satu instalasi DLTB ditemukan. Jalankan lagi dengan -GameDir. Ditemukan:`r`n$($games -join "`r`n")"
    }
    return $null
}

function Select-GameFolder {
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = 'Pilih folder utama Dying Light The Beast (folder yang berisi ph_ft)'
    $dialog.ShowNewFolderButton = $false
    if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
    return $dialog.SelectedPath
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot 'config\baseline_1.71E_manifest.json'
if (-not (Test-Path $manifestPath)) { throw "Manifest repo tidak ditemukan: $manifestPath" }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
if ($manifest.observed_version -ne '1.71E' -or [int]$manifest.target_count -ne 58) {
    throw 'Manifest baseline bukan contract 1.71E / 58-target yang diharapkan.'
}

if (-not $GameDir) { $GameDir = Auto-FindGame }
if (-not $GameDir -and -not $NoGui) { $GameDir = Select-GameFolder }
if (-not $GameDir) { throw 'GameDir tidak ditemukan. Gunakan -GameDir "C:\...\Dying Light The Beast".' }
$GameDir = [IO.Path]::GetFullPath($GameDir).TrimEnd('\')

$data0 = Join-Path $GameDir 'ph_ft\source\data0.pak'
if (-not (Test-Path $data0)) { throw "data0.pak tidak ditemukan: $data0" }

$sevenZip = Find-7Zip
$tar = Get-Command tar.exe -ErrorAction SilentlyContinue
if (-not $sevenZip -and -not $tar) { throw 'Butuh 7-Zip (recommended) atau tar.exe yang bisa membaca PAK.' }

$outRoot = Join-Path $repoRoot 'local_baseline\1.71E'
if (Test-Path $outRoot) { Remove-Item -Recurse -Force $outRoot }
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

$results = @()
foreach ($f in $manifest.files) {
    $target = [string]$f.path
    Write-Host "Extract: $target"
    if ($sevenZip) {
        & $sevenZip x -y $data0 $target "-o$outRoot" | Out-Null
    } else {
        & $tar.Source -xf $data0 -C $outRoot $target 2>$null
    }

    $local = Join-Path $outRoot ($target -replace '/', '\')
    $status = 'MISSING'
    $actualHash = $null
    $actualSize = 0
    if (Test-Path $local) {
        $actualSize = (Get-Item $local).Length
        $actualHash = (Get-FileHash $local -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($SkipHashValidation) {
            $status = 'EXTRACTED_UNVERIFIED'
        } elseif ($actualHash -eq [string]$f.sha256 -and $actualSize -eq [int64]$f.size) {
            $status = 'VERIFIED_1.71E'
        } else {
            $status = 'HASH_OR_SIZE_MISMATCH'
        }
    }
    $results += [PSCustomObject]@{
        path = $target
        status = $status
        expected_sha256 = [string]$f.sha256
        actual_sha256 = $actualHash
        expected_size = [int64]$f.size
        actual_size = $actualSize
    }
}

$verified = @($results | Where-Object { $_.status -eq 'VERIFIED_1.71E' }).Count
$missing = @($results | Where-Object { $_.status -eq 'MISSING' }).Count
$mismatch = @($results | Where-Object { $_.status -eq 'HASH_OR_SIZE_MISMATCH' }).Count
$report = [ordered]@{
    game = 'Dying Light: The Beast'
    expected_version = '1.71E'
    game_dir = $GameDir
    data0 = $data0
    generated = (Get-Date -Format o)
    targets = $results.Count
    verified_1_71E = $verified
    missing = $missing
    mismatch = $mismatch
    skip_hash_validation = [bool]$SkipHashValidation
    results = $results
}
$reportPath = Join-Path $outRoot '_VERIFY_REPORT.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $reportPath

Write-Host ''
Write-Host '=============================================================='
Write-Host ' DLTB 1.71E LOCAL BASELINE'
Write-Host '=============================================================='
Write-Host "GameDir=$GameDir"
Write-Host "Output=$outRoot"
Write-Host "Targets=$($results.Count)"
Write-Host "Verified=$verified"
Write-Host "Missing=$missing"
Write-Host "Mismatch=$mismatch"
Write-Host ''

if (-not $SkipHashValidation -and ($verified -ne 58 -or $missing -ne 0 -or $mismatch -ne 0)) {
    throw "Baseline bukan exact captured 1.71E. Lihat $reportPath"
}
if ($SkipHashValidation -and $missing -ne 0) {
    throw "Ada target yang tidak ter-extract. Lihat $reportPath"
}

Write-Host 'PASS: local proprietary baseline siap dipakai oleh tooling repo.'
Write-Host 'Folder local_baseline/ di-gitignore dan JANGAN di-commit.'
