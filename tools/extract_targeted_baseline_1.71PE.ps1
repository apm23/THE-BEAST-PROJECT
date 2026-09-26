param(
    [string]$GameDir,
    [switch]$NoGui
)

$ErrorActionPreference = 'Stop'

function Find-7Zip {
    $candidates = @(@(
        (Get-Command 7z.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    ) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique)
    if ($candidates.Count -gt 0) { return [string]$candidates[0] }
    return $null
}

function Get-SteamRoots {
    $roots = @()
    try { $p = (Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath; if ($p) { $roots += $p } } catch {}
    try { $p = (Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath; if ($p) { $roots += $p } } catch {}
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
    if ($games.Count -gt 1) { throw "Lebih dari satu instalasi DLTB ditemukan. Gunakan -GameDir." }
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

function Extract-One {
    param(
        [string]$Target,
        [string]$ArchiveName,
        [bool]$Required,
        [string]$Kind
    )
    if (-not $archives.ContainsKey($ArchiveName) -or -not (Test-Path $archives[$ArchiveName])) {
        $ArchiveName = 'data0.pak'
    }
    $archivePath = $archives[$ArchiveName]
    Write-Host "Extract [$ArchiveName][$Kind]: $Target"
    if ($sevenZip) {
        & $sevenZip x -y $archivePath $Target "-o$outRoot" | Out-Null
        if ($LASTEXITCODE -ne 0) { Write-Host "Extractor exit code: $LASTEXITCODE" -ForegroundColor Yellow }
    } else {
        & $tar.Source -xf $archivePath -C $outRoot $Target 2>$null
    }

    $local = Join-Path $outRoot ($Target -replace '/', '\')
    $status = 'MISSING'
    $actualHash = $null
    $actualSize = 0
    if (Test-Path $local) {
        $actualSize = (Get-Item $local).Length
        $actualHash = (Get-FileHash $local -Algorithm SHA256).Hash.ToLowerInvariant()
        $status = 'EXTRACTED'
    }
    return [PSCustomObject]@{
        path = $Target
        archive = $ArchiveName
        kind = $Kind
        required = $Required
        status = $status
        sha256 = $actualHash
        size = $actualSize
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot 'config\baseline_1.71E_manifest.json'
$extraPath = Join-Path $repoRoot 'config\remake_1.71PE_extra_targets.json'
if (-not (Test-Path $manifestPath)) { throw "Manifest target-list tidak ditemukan: $manifestPath" }
if (-not (Test-Path $extraPath)) { throw "Extra target-list tidak ditemukan: $extraPath" }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
$extras = Get-Content -Raw $extraPath | ConvertFrom-Json

if (-not $GameDir) { $GameDir = Auto-FindGame }
if (-not $GameDir -and -not $NoGui) { $GameDir = Select-GameFolder }
if (-not $GameDir) { throw 'GameDir tidak ditemukan. Gunakan -GameDir "C:\...\Dying Light The Beast".' }
$GameDir = [IO.Path]::GetFullPath($GameDir).TrimEnd('\')

$archives = @{
    'data0.pak' = Join-Path $GameDir 'ph_ft\source\data0.pak'
    'data1.pak' = Join-Path $GameDir 'ph_ft\source\data1.pak'
}
if (-not (Test-Path $archives['data0.pak'])) { throw "data0.pak tidak ditemukan: $($archives['data0.pak'])" }

$sevenZip = Find-7Zip
$tar = Get-Command tar.exe -ErrorAction SilentlyContinue
if (-not $sevenZip -and -not $tar) { throw 'Butuh 7-Zip atau tar.exe yang bisa membaca PAK.' }
if ($sevenZip) { Write-Host "Extractor: 7-Zip = $sevenZip" }
else { Write-Host "Extractor: tar = $($tar.Source)" }

$outRoot = Join-Path $repoRoot 'local_baseline\1.71PE'
if (Test-Path $outRoot) { Remove-Item -Recurse -Force $outRoot }
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

$results = @()
$seen = @{}
foreach ($f in $manifest.files) {
    $target = [string]$f.path
    $key = $target.ToLowerInvariant()
    if ($seen.ContainsKey($key)) { continue }
    $seen[$key] = $true
    $results += Extract-One -Target $target -ArchiveName ([string]$f.archive) -Required $true -Kind 'compat58'
}

# Current schema: required[] / optional[]. Keep legacy extra_targets[] support too.
$extraItems = @()
if ($extras.required) {
    foreach ($f in @($extras.required)) {
        $extraItems += [PSCustomObject]@{ item=$f; required=$true; kind='remake_required' }
    }
}
if ($extras.optional) {
    foreach ($f in @($extras.optional)) {
        $extraItems += [PSCustomObject]@{ item=$f; required=$false; kind='remake_optional' }
    }
}
if ($extras.extra_targets) {
    foreach ($f in @($extras.extra_targets)) {
        $req = if ($null -ne $f.required) { [bool]$f.required } else { $false }
        $kind = if ($f.kind) { [string]$f.kind } else { 'remake_extra_legacy' }
        $extraItems += [PSCustomObject]@{ item=$f; required=$req; kind=$kind }
    }
}

foreach ($x in $extraItems) {
    $f = $x.item
    $target = [string]$f.path
    $key = $target.ToLowerInvariant()
    if ($seen.ContainsKey($key)) { continue }
    $seen[$key] = $true
    $archive = if ($f.archive) { [string]$f.archive } else { 'data0.pak' }
    $results += Extract-One -Target $target -ArchiveName $archive -Required ([bool]$x.required) -Kind ([string]$x.kind)
}

$missingRequired = @($results | Where-Object { $_.required -and $_.status -ne 'EXTRACTED' })
$report = [ordered]@{
    runtime = '1.71PE'
    game_dir = $GameDir
    extractor = if ($sevenZip) { $sevenZip } else { $tar.Source }
    extracted_at = (Get-Date).ToString('o')
    total = $results.Count
    extracted = @($results | Where-Object status -eq 'EXTRACTED').Count
    missing_required = $missingRequired.Count
    files = $results
}
$reportPath = Join-Path $outRoot '_EXTRACT_REPORT.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Host ''
Write-Host "1.71PE extraction complete: $($report.extracted)/$($report.total)"
Write-Host "Report: $reportPath"
if ($missingRequired.Count -gt 0) {
    $missingRequired | ForEach-Object { Write-Host "MISSING REQUIRED: $($_.path)" -ForegroundColor Red }
    exit 2
}
exit 0