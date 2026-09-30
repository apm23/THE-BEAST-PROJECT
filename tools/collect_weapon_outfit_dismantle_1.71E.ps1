param(
    [string]$GameDir,
    [switch]$NoGui
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# THE BEAST PROJECT - READ-ONLY collector.
# Purpose:
#   1) inventory every weapon-like Item definition;
#   2) record dismantle/drop/share flags and native dismantle family;
#   3) inventory all OutfitPart definitions, especially Vanguard/Night Sovereign carriers;
#   4) produce metadata only for later deterministic patching.
#
# SAFETY:
#   - reads official/current PAKs only;
#   - writes only under repository local_research/;
#   - never writes game PAKs, saves, configs, inventory versioning, or MultiMod;
#   - never deletes/reorders/renames Item definitions.

function Find-7Zip {
    $candidates = @(
        (Get-Command 7z.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -Unique

    if ($candidates.Count -gt 0) {
        return $candidates[0]
    }
    throw '7-Zip diperlukan untuk collector read-only ini.'
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
        if ($p -and (Test-Path -LiteralPath $p)) { $roots += $p }
    }

    return @($roots | Select-Object -Unique)
}

function Auto-FindGame {
    $games = @()

    foreach ($root in Get-SteamRoots) {
        $vdf = Join-Path $root 'steamapps\libraryfolders.vdf'
        $libs = @($root)

        if (Test-Path -LiteralPath $vdf) {
            $txt = Get-Content -Raw -LiteralPath $vdf
            foreach ($m in [regex]::Matches($txt, '"path"\s*"([^"]+)"')) {
                $libs += ($m.Groups[1].Value -replace '\\\\', '\')
            }
        }

        foreach ($lib in ($libs | Select-Object -Unique)) {
            $g = Join-Path $lib 'steamapps\common\Dying Light The Beast'
            if (Test-Path -LiteralPath (Join-Path $g 'ph_ft\source\data0.pak')) {
                $games += $g
            }
        }
    }

    $games = @(
        $games |
            ForEach-Object { [IO.Path]::GetFullPath($_).TrimEnd('\') } |
            Select-Object -Unique
    )

    if ($games.Count -eq 1) { return $games[0] }
    if ($games.Count -gt 1) {
        throw 'Lebih dari satu instalasi Dying Light The Beast ditemukan; jalankan dengan -GameDir.'
    }
    return $null
}

function Select-GameFolder {
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = 'Pilih folder Dying Light The Beast (folder yang berisi ph_ft)'
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $dialog.SelectedPath
    }
    return $null
}

function Write-Utf8NoBomLines {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string[]]$Lines
    )
    $enc = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllLines($Path, $Lines, $enc)
}

function Get-ArchiveInventoryEntries {
    param(
        [Parameter(Mandatory = $true)][string]$SevenZip,
        [Parameter(Mandatory = $true)][string]$ArchivePath
    )

    $raw = & $SevenZip l -slt -- $ArchivePath
    if ($LASTEXITCODE -ne 0) {
        throw "Gagal membaca daftar archive: $ArchivePath"
    }

    $paths = New-Object System.Collections.Generic.List[string]

    foreach ($line in $raw) {
        $m = [regex]::Match($line, '^Path = (.+)$')
        if (-not $m.Success) { continue }

        $p = $m.Groups[1].Value.Trim()
        if (
            $p -match '(?i)^scripts[\\/]inventory[\\/].*\.scr$' -or
            $p -match '(?i)^scripts[\\/]menu[\\/]menumodifyweapon\.scr$'
        ) {
            $paths.Add($p)
        }
    }

    return @($paths | Sort-Object -Unique)
}

function Extract-ArchiveTargets {
    param(
        [Parameter(Mandatory = $true)][string]$SevenZip,
        [Parameter(Mandatory = $true)][string]$ArchivePath,
        [Parameter(Mandatory = $true)][string]$OutputDir,
        [Parameter(Mandatory = $true)][string[]]$Entries
    )

    if ($Entries.Count -eq 0) { return }

    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    $listFile = Join-Path $OutputDir '_collector_targets.txt'
    Write-Utf8NoBomLines -Path $listFile -Lines $Entries

    & $SevenZip x -y -scsUTF-8 "-o$OutputDir" -- $ArchivePath "@$listFile" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Gagal extract target inventory dari: $ArchivePath"
    }

    Remove-Item -LiteralPath $listFile -Force -ErrorAction SilentlyContinue
}

function Get-CallArg {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $escaped = [regex]::Escape($Name)
    $m = [regex]::Match(
        $Text,
        "(?im)^\s*$escaped\(\s*(.*?)\s*\)\s*;"
    )

    if (-not $m.Success) { return $null }

    $v = $m.Groups[1].Value.Trim()
    if ($v.Length -ge 2 -and $v.StartsWith('"') -and $v.EndsWith('"')) {
        $v = $v.Substring(1, $v.Length - 2)
    }
    return $v
}

function Get-UseCall {
    param([Parameter(Mandatory = $true)][string]$Text)
    $m = [regex]::Match($Text, '(?im)^\s*use\s+([A-Za-z0-9_]+)\s*\(')
    if ($m.Success) { return $m.Groups[1].Value }
    return $null
}

function Get-ItemRecordsFromFile {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string]$LogicalPath,
        [Parameter(Mandatory = $true)][string]$ArchiveKey,
        [Parameter(Mandatory = $true)][int]$ArchivePriority
    )

    $lines = @(Get-Content -LiteralPath $FilePath)
    $records = New-Object System.Collections.Generic.List[object]

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = [string]$lines[$i]
        $header = [regex]::Match(
            $line,
            '^\s*Item\(\s*"([^"]+)"\s*,\s*([^)]+?)\s*\)'
        )

        if (-not $header.Success) { continue }

        $itemId = $header.Groups[1].Value.Trim()
        $category = $header.Groups[2].Value.Trim()

        $blockLines = New-Object System.Collections.Generic.List[string]
        $depth = 0
        $opened = $false
        $j = $i

        while ($j -lt $lines.Count) {
            $current = [string]$lines[$j]
            $blockLines.Add($current)

            # Ignore // comments while balancing braces.
            $braceText = [regex]::Replace($current, '//.*$', '')
            $opens = ([regex]::Matches($braceText, '\{')).Count
            $closes = ([regex]::Matches($braceText, '\}')).Count

            if ($opens -gt 0) { $opened = $true }
            $depth += ($opens - $closes)

            if ($opened -and $depth -le 0) { break }
            $j++
        }

        if (-not $opened) {
            # Malformed/unexpected source form: keep scanning instead of inventing a block.
            continue
        }

        $block = $blockLines -join "`n"
        $itemType = Get-CallArg -Text $block -Name 'ItemType'
        $genType = Get-CallArg -Text $block -Name 'GenType'
        $dismantle = Get-CallArg -Text $block -Name 'DismantleResult'
        $canDrop = Get-CallArg -Text $block -Name 'CanDrop'
        $isShareable = Get-CallArg -Text $block -Name 'IsShareable'
        $allowedInShop = Get-CallArg -Text $block -Name 'AllowedInShop'
        $canThrow = Get-CallArg -Text $block -Name 'CanThrow'
        $color = Get-CallArg -Text $block -Name 'Color'
        $lootType = Get-CallArg -Text $block -Name 'LootType'
        $uid = Get-CallArg -Text $block -Name 'UID'
        $name = Get-CallArg -Text $block -Name 'Name'
        $description = Get-CallArg -Text $block -Name 'Description'
        $hudIcon = Get-CallArg -Text $block -Name 'HudIcon'
        $outfitSlot = Get-CallArg -Text $block -Name 'OutfitPartSlot'
        $outfitVis = Get-CallArg -Text $block -Name 'OutfitPartVisualization'
        $forcedAffix = Get-CallArg -Text $block -Name 'OutfitPartForcedAffixGroup'
        $randomAffix = Get-CallArg -Text $block -Name 'OutfitPartRandomAffixGroup'
        $useCall = Get-UseCall -Text $block

        $weaponByCategory = ($category -match '(?i)(Melee|Firearm|Ranged|Bow|Crossbow|Weapon)')
        $weaponByDismantle = ($dismantle -match '(?i)^Dismantle_T\d+_(Blunt|Slash|Ranged|Firearm)$')
        $isWeapon = ($weaponByCategory -or $weaponByDismantle)
        $isOutfit = (
            $category -match '(?i)OutfitPart' -or
            ($itemType -and $itemType -match '(?i)OutfitPart')
        )

        if (-not $isWeapon -and -not $isOutfit) {
            $i = $j
            continue
        }

        $status = 'UNCLASSIFIED'
        if ($isWeapon) {
            if ([string]::IsNullOrWhiteSpace($dismantle)) {
                $status = 'WEAPON_NO_EXPLICIT_DISMANTLE'
            } elseif ($dismantle -ieq 'empty') {
                $status = 'WEAPON_EMPTY_DISMANTLE_REVIEW'
            } else {
                $status = 'WEAPON_DISMANTLE_PRESENT'
            }
        } elseif ($isOutfit) {
            if ([string]::IsNullOrWhiteSpace($dismantle)) {
                $status = 'OUTFIT_NO_EXPLICIT_DELETE'
            } elseif ($dismantle -ieq 'empty') {
                $status = 'OUTFIT_DELETE_NATIVE_PRESENT'
            } else {
                $status = 'OUTFIT_NONEMPTY_DISMANTLE_REVIEW'
            }
        }

        $identityText = @(
            $itemId, $category, $itemType, $useCall, $name, $description,
            $hudIcon, $outfitVis, $forcedAffix, $randomAffix
        ) -join ' '

        $carrierHint = ''
        if ($identityText -match '(?i)night[_ .-]*sovereign') {
            $carrierHint = 'NIGHT_SOVEREIGN'
        } elseif ($identityText -match '(?i)vanguard') {
            $carrierHint = 'VANGUARD'
        }

        $records.Add([pscustomobject]@{
            ArchiveKey = $ArchiveKey
            ArchivePriority = $ArchivePriority
            LogicalPath = $LogicalPath
            StartLine = ($i + 1)
            EndLine = ($j + 1)
            ItemId = $itemId
            Category = $category
            ItemType = $itemType
            GenType = $genType
            Use = $useCall
            DismantleResult = $dismantle
            CanDrop = $canDrop
            IsShareable = $isShareable
            AllowedInShop = $allowedInShop
            CanThrow = $canThrow
            Color = $color
            LootType = $lootType
            UID = $uid
            Name = $name
            Description = $description
            HudIcon = $hudIcon
            OutfitPartSlot = $outfitSlot
            OutfitPartVisualization = $outfitVis
            OutfitPartForcedAffixGroup = $forcedAffix
            OutfitPartRandomAffixGroup = $randomAffix
            IsWeapon = [bool]$isWeapon
            IsOutfit = [bool]$isOutfit
            CandidateStatus = $status
            CarrierHint = $carrierHint
            LikelyEffective = $false
        })

        $i = $j
    }

    return @($records)
}

$repoRoot = Split-Path -Parent $PSScriptRoot

if (-not $GameDir) { $GameDir = Auto-FindGame }
if (-not $GameDir -and -not $NoGui) { $GameDir = Select-GameFolder }
if (-not $GameDir) { throw 'GameDir tidak ditemukan.' }

$GameDir = [IO.Path]::GetFullPath($GameDir).TrimEnd('\')
$data0 = Join-Path $GameDir 'ph_ft\source\data0.pak'

if (-not (Test-Path -LiteralPath $data0)) {
    throw "data0.pak tidak ditemukan: $data0"
}

$seven = Find-7Zip
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outBase = Join-Path $repoRoot 'local_research\weapon_outfit_dismantle_1.71E'
$outRoot = Join-Path $outBase $stamp
$extractRoot = Join-Path $outRoot '_extracted_local_only'

New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null

$archiveCandidates = @(
    [pscustomobject]@{
        Key = 'data0'
        Path = (Join-Path $GameDir 'ph_ft\source\data0.pak')
        Priority = 10
        Role = 'official-base'
    },
    [pscustomobject]@{
        Key = 'data1'
        Path = (Join-Path $GameDir 'ph_ft\source\data1.pak')
        Priority = 20
        Role = 'official-overlay'
    },
    [pscustomobject]@{
        Key = 'source_data2'
        Path = (Join-Path $GameDir 'ph_ft\source\data2.pak')
        Priority = 30
        Role = 'source-mod'
    },
    [pscustomobject]@{
        Key = 'source_data3'
        Path = (Join-Path $GameDir 'ph_ft\source\data3.pak')
        Priority = 40
        Role = 'source-overlay'
    },
    [pscustomobject]@{
        Key = 'multimod_data2'
        Path = (Join-Path $GameDir 'ph_ft\MultiMod\data2.pak')
        Priority = 50
        Role = 'multimod-mod'
    },
    [pscustomobject]@{
        Key = 'multimod_data3'
        Path = (Join-Path $GameDir 'ph_ft\MultiMod\data3.pak')
        Priority = 60
        Role = 'multimod-overlay'
    }
)

$archives = @($archiveCandidates | Where-Object { Test-Path -LiteralPath $_.Path })
if ($archives.Count -eq 0) {
    throw 'Tidak ada PAK yang dapat dibaca.'
}

$layoutWarnings = New-Object System.Collections.Generic.List[string]
if (
    (Test-Path -LiteralPath (Join-Path $GameDir 'ph_ft\source\data2.pak')) -and
    (Test-Path -LiteralPath (Join-Path $GameDir 'ph_ft\MultiMod\data2.pak'))
) {
    $layoutWarnings.Add('source\data2.pak dan MultiMod\data2.pak sama-sama ada. LikelyEffective hanya heuristic; jangan patch otomatis dari keadaan ini.')
}
if (
    (Test-Path -LiteralPath (Join-Path $GameDir 'ph_ft\source\data3.pak')) -and
    (Test-Path -LiteralPath (Join-Path $GameDir 'ph_ft\MultiMod\data3.pak'))
) {
    $layoutWarnings.Add('source\data3.pak dan MultiMod\data3.pak sama-sama ada. LikelyEffective hanya heuristic; jangan patch otomatis dari keadaan ini.')
}

$archiveMeta = New-Object System.Collections.Generic.List[object]
$allRecords = New-Object System.Collections.Generic.List[object]
$fileLayers = @{}

foreach ($archive in $archives) {
    Write-Host "READ-ONLY SCAN: $($archive.Key)"
    Write-Host "  $($archive.Path)"

    $hash = (Get-FileHash -LiteralPath $archive.Path -Algorithm SHA256).Hash.ToLowerInvariant()
    $entries = @(Get-ArchiveInventoryEntries -SevenZip $seven -ArchivePath $archive.Path)
    $outExtract = Join-Path $extractRoot $archive.Key

    Extract-ArchiveTargets `
        -SevenZip $seven `
        -ArchivePath $archive.Path `
        -OutputDir $outExtract `
        -Entries $entries

    $archiveMeta.Add([pscustomobject]@{
        Key = $archive.Key
        Role = $archive.Role
        Priority = $archive.Priority
        Path = $archive.Path
        Sha256 = $hash
        InventoryScrEntries = $entries.Count
    })

    if (-not (Test-Path -LiteralPath $outExtract)) {
        continue
    }

    foreach ($file in (Get-ChildItem -LiteralPath $outExtract -Recurse -File -Filter '*.scr')) {
        $rel = $file.FullName.Substring($outExtract.Length).TrimStart('\', '/').Replace('\', '/')

        if (-not $fileLayers.ContainsKey($rel)) {
            $fileLayers[$rel] = New-Object System.Collections.Generic.List[object]
        }
        $fileLayers[$rel].Add([pscustomobject]@{
            ArchiveKey = $archive.Key
            Priority = [int]$archive.Priority
        })

        $records = @(
            Get-ItemRecordsFromFile `
                -FilePath $file.FullName `
                -LogicalPath $rel `
                -ArchiveKey $archive.Key `
                -ArchivePriority $archive.Priority
        )
        foreach ($record in $records) { $allRecords.Add($record) }
    }
}

# Mark records from the highest discovered layer for each logical file.
$effectiveLayerByFile = @{}
foreach ($logicalPath in $fileLayers.Keys) {
    $winner = @(
        $fileLayers[$logicalPath] |
            Sort-Object Priority -Descending |
            Select-Object -First 1
    )[0]
    $effectiveLayerByFile[$logicalPath] = $winner.ArchiveKey
}

foreach ($record in $allRecords) {
    if (
        $effectiveLayerByFile.ContainsKey($record.LogicalPath) -and
        $effectiveLayerByFile[$record.LogicalPath] -eq $record.ArchiveKey
    ) {
        $record.LikelyEffective = $true
    }
}

$allSorted = @(
    $allRecords |
        Sort-Object LogicalPath, StartLine, ArchivePriority, ItemId
)
$effective = @(
    $allRecords |
        Where-Object { $_.LikelyEffective } |
        Sort-Object LogicalPath, StartLine, ItemId
)

$weapons = @($effective | Where-Object { $_.IsWeapon })
$outfits = @($effective | Where-Object { $_.IsOutfit })
$weaponReview = @(
    $weapons |
        Where-Object { $_.CandidateStatus -ne 'WEAPON_DISMANTLE_PRESENT' }
)
$outfitReview = @(
    $outfits |
        Where-Object { $_.CandidateStatus -ne 'OUTFIT_DELETE_NATIVE_PRESENT' }
)
$carrierCandidates = @(
    $outfits |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_.CarrierHint) }
)

$allCsv = Join-Path $outRoot '_WEAPON_OUTFIT_ALL_OCCURRENCES.csv'
$effectiveCsv = Join-Path $outRoot '_WEAPON_OUTFIT_EFFECTIVE.csv'
$jsonPath = Join-Path $outRoot '_WEAPON_OUTFIT_SNAPSHOT.json'
$reportPath = Join-Path $outRoot '_WEAPON_OUTFIT_DISMANTLE_REPORT.txt'
$hashPath = Join-Path $outRoot '_ARCHIVE_HASHES.txt'
$readmePath = Join-Path $outRoot '_READ_ME_FIRST.txt'

$allSorted | Export-Csv -LiteralPath $allCsv -NoTypeInformation -Encoding UTF8
$effective | Export-Csv -LiteralPath $effectiveCsv -NoTypeInformation -Encoding UTF8

$snapshot = [ordered]@{
    Collector = 'THE BEAST PROJECT - Weapon + Outfit Dismantle Collector'
    Timestamp = (Get-Date).ToString('o')
    GameDir = $GameDir
    ReadOnly = $true
    EngineEffectiveResolution = 'Heuristic by highest discovered PAK layer per logical file; not runtime proof.'
    LayoutWarnings = @($layoutWarnings)
    Archives = @($archiveMeta)
    Summary = [ordered]@{
        EffectiveWeaponRecords = $weapons.Count
        EffectiveOutfitRecords = $outfits.Count
        WeaponReviewRecords = $weaponReview.Count
        OutfitReviewRecords = $outfitReview.Count
        VanguardOrNightSovereignHints = $carrierCandidates.Count
    }
    EffectiveRecords = @($effective)
}

$snapshot |
    ConvertTo-Json -Depth 8 |
    Set-Content -LiteralPath $jsonPath -Encoding UTF8

$hashLines = New-Object System.Collections.Generic.List[string]
$hashLines.Add('THE BEAST PROJECT - ARCHIVE HASHES (READ-ONLY)')
foreach ($a in $archiveMeta) {
    $hashLines.Add(('{0} | {1} | {2} | {3}' -f $a.Key, $a.Sha256, $a.InventoryScrEntries, $a.Path))
}
Write-Utf8NoBomLines -Path $hashPath -Lines @($hashLines)

$report = New-Object System.Collections.Generic.List[string]
$report.Add('THE BEAST PROJECT - WEAPON + OUTFIT DISMANTLE REPORT')
$report.Add('READ-ONLY: no game/save/config/PAK mutation performed.')
$report.Add("Timestamp=$((Get-Date).ToString('o'))")
$report.Add("GameDir=$GameDir")
$report.Add('')
$report.Add('=== ARCHIVE LAYOUT ===')
foreach ($a in ($archiveMeta | Sort-Object Priority)) {
    $report.Add(('{0,-16} priority={1,-2} role={2,-16} sha256={3} inventory_scr={4}' -f
        $a.Key, $a.Priority, $a.Role, $a.Sha256, $a.InventoryScrEntries))
}
if ($layoutWarnings.Count -gt 0) {
    $report.Add('')
    $report.Add('=== LAYOUT WARNINGS ===')
    foreach ($w in $layoutWarnings) { $report.Add("WARNING: $w") }
}

$report.Add('')
$report.Add('=== EFFECTIVE SUMMARY (HEURISTIC) ===')
$report.Add("Weapon records=$($weapons.Count)")
$report.Add("Weapon records needing review/patch=$($weaponReview.Count)")
$report.Add("Outfit records=$($outfits.Count)")
$report.Add("Outfit records needing review=$($outfitReview.Count)")
$report.Add("Vanguard/Night Sovereign text hints=$($carrierCandidates.Count)")
$report.Add('')
$report.Add('NOTE: "NO_EXPLICIT_DISMANTLE" can still inherit behavior through use(...).')
$report.Add('It is a review flag, not automatic proof that dismantle is impossible.')
$report.Add('NOTE: DismantleResult("empty") on OutfitPart is treated as the native delete candidate,')
$report.Add('but runtime UI behavior must still be tested before calling it GREEN.')

$report.Add('')
$report.Add('=== WEAPON DISMANTLE RESULT COUNTS ===')
$weaponGroups = @(
    $weapons |
        Group-Object {
            if ([string]::IsNullOrWhiteSpace($_.DismantleResult)) {
                '<none-explicit>'
            } else {
                $_.DismantleResult
            }
        } |
        Sort-Object @{ Expression = 'Count'; Descending = $true }, Name
)
foreach ($g in $weaponGroups) {
    $report.Add(('{0,5}  {1}' -f $g.Count, $g.Name))
}

$report.Add('')
$report.Add('=== WEAPON REVIEW CANDIDATES ===')
if ($weaponReview.Count -eq 0) {
    $report.Add('NONE')
} else {
    foreach ($r in $weaponReview) {
        $report.Add(('{0} | {1} | {2}:{3} | use={4} | dismantle={5} | drop={6} | share={7} | {8}' -f
            $r.ItemId,
            $r.Category,
            $r.LogicalPath,
            $r.StartLine,
            $r.Use,
            $r.DismantleResult,
            $r.CanDrop,
            $r.IsShareable,
            $r.CandidateStatus))
    }
}

$report.Add('')
$report.Add('=== OUTFIT DELETE/DISMANTLE COUNTS ===')
$outfitGroups = @(
    $outfits |
        Group-Object {
            if ([string]::IsNullOrWhiteSpace($_.DismantleResult)) {
                '<none-explicit>'
            } else {
                $_.DismantleResult
            }
        } |
        Sort-Object @{ Expression = 'Count'; Descending = $true }, Name
)
foreach ($g in $outfitGroups) {
    $report.Add(('{0,5}  {1}' -f $g.Count, $g.Name))
}

$report.Add('')
$report.Add('=== VANGUARD / NIGHT SOVEREIGN CARRIER HINTS ===')
if ($carrierCandidates.Count -eq 0) {
    $report.Add('No text hint matched. Use _WEAPON_OUTFIT_EFFECTIVE.csv to inspect all OutfitPart records.')
} else {
    foreach ($r in $carrierCandidates) {
        $report.Add(('{0} | hint={1} | slot={2} | name={3} | vis={4} | dismantle={5} | drop={6} | {7}:{8}' -f
            $r.ItemId,
            $r.CarrierHint,
            $r.OutfitPartSlot,
            $r.Name,
            $r.OutfitPartVisualization,
            $r.DismantleResult,
            $r.CanDrop,
            $r.LogicalPath,
            $r.StartLine))
    }
}

$report.Add('')
$report.Add('=== ALL EFFECTIVE OUTFIT PARTS ===')
foreach ($r in $outfits) {
    $report.Add(('{0} | slot={1} | name={2} | use={3} | dismantle={4} | drop={5} | affix={6} | {7}:{8}' -f
        $r.ItemId,
        $r.OutfitPartSlot,
        $r.Name,
        $r.Use,
        $r.DismantleResult,
        $r.CanDrop,
        $r.OutfitPartForcedAffixGroup,
        $r.LogicalPath,
        $r.StartLine))
}

$report.Add('')
$report.Add('=== SAFE PATCH INTENT FOR NEXT STEP ===')
$report.Add('Weapons: assign/retain a native dismantle family appropriate to the existing weapon class/tier.')
$report.Add('Outfit/Night Sovereign: prefer native delete semantics using DismantleResult("empty");')
$report.Add('do not delete/reorder/rename Item definitions and do not touch inventory versioning/save data.')
$report.Add('No patch is applied by this collector.')

Write-Utf8NoBomLines -Path $reportPath -Lines @($report)

$readme = @(
    'UPLOAD THESE GENERATED METADATA FILES / ZIP TO CHAT.',
    '',
    'This result contains collector-generated metadata only.',
    'Temporary raw game-script extracts are kept only during the scan and deleted before successful completion.',
    '',
    'Main files:',
    '  _WEAPON_OUTFIT_DISMANTLE_REPORT.txt',
    '  _WEAPON_OUTFIT_EFFECTIVE.csv',
    '  _WEAPON_OUTFIT_SNAPSHOT.json',
    '  _ARCHIVE_HASHES.txt',
    '',
    'Safety:',
    '  - no game PAK changed',
    '  - no save changed',
    '  - no inventory versioning changed',
    '  - no registry Item removed/reordered/renamed'
)
Write-Utf8NoBomLines -Path $readmePath -Lines $readme

# Raw extracted source is not part of the result. Remove collector temp data after metadata is complete.
if (Test-Path -LiteralPath $extractRoot) {
    Remove-Item -LiteralPath $extractRoot -Recurse -Force
}

$zipPath = Join-Path $outBase ("DLTB_WEAPON_OUTFIT_DISMANTLE_RESULT_{0}.zip" -f $stamp)
$zipInputs = @(
    $reportPath,
    $effectiveCsv,
    $allCsv,
    $jsonPath,
    $hashPath,
    $readmePath
)
Compress-Archive -LiteralPath $zipInputs -DestinationPath $zipPath -CompressionLevel Optimal -Force

Write-Host ''
Write-Host 'PASS: collector READ-ONLY selesai.'
Write-Host "Weapon records (effective heuristic): $($weapons.Count)"
Write-Host "Weapon review candidates: $($weaponReview.Count)"
Write-Host "Outfit records (effective heuristic): $($outfits.Count)"
Write-Host "Vanguard/Night Sovereign hints: $($carrierCandidates.Count)"
Write-Host ''
Write-Host "UPLOAD ZIP INI KE CHAT:"
Write-Host $zipPath
Write-Host ''
Write-Host 'Tidak ada PAK/save/config game yang diubah.'
