param(
    [string]$GameDir,
    [switch]$NoGui
)

$ErrorActionPreference = 'Stop'

# READ-ONLY research collector.
# It reads only official data0.pak, writes only under local_research/, and never
# writes ph_ft\source, data2/data3, saves, DLC files, MultiMod, or game configs.

function Find-7Zip {
    $candidates = @(
        (Get-Command 7z.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
    ) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique
    if ($candidates.Count -gt 0) { return $candidates[0] }
    throw '7-Zip diperlukan untuk collector read-only ini.'
}

function Get-SteamRoots {
    $roots=@()
    try { $p=(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath; if($p){$roots+=$p} } catch {}
    try { $p=(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath; if($p){$roots+=$p} } catch {}
    foreach($p in @("${env:ProgramFiles(x86)}\Steam","${env:ProgramFiles}\Steam",'C:\Steam')){ if($p -and (Test-Path $p)){$roots+=$p} }
    @($roots|Select-Object -Unique)
}
function Auto-FindGame {
    $games=@()
    foreach($root in Get-SteamRoots){
        $vdf=Join-Path $root 'steamapps\libraryfolders.vdf'
        $libs=@($root)
        if(Test-Path $vdf){
            $txt=Get-Content -Raw $vdf
            foreach($m in [regex]::Matches($txt,'"path"\s*"([^"]+)"')){$libs+=($m.Groups[1].Value -replace '\\\\','\')}
        }
        foreach($lib in $libs){
            $g=Join-Path $lib 'steamapps\common\Dying Light The Beast'
            if(Test-Path (Join-Path $g 'ph_ft\source\data0.pak')){$games+=$g}
        }
    }
    $games=@($games|ForEach-Object{[IO.Path]::GetFullPath($_).TrimEnd('\')}|Select-Object -Unique)
    if($games.Count -eq 1){return $games[0]}
    if($games.Count -gt 1){throw 'Lebih dari satu instalasi ditemukan; gunakan -GameDir.'}
    $null
}
function Select-GameFolder {
    Add-Type -AssemblyName System.Windows.Forms
    $d=New-Object System.Windows.Forms.FolderBrowserDialog
    $d.Description='Pilih folder Dying Light The Beast (berisi ph_ft)'
    if($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){return $d.SelectedPath}
    $null
}

$repoRoot=Split-Path -Parent $PSScriptRoot
if(-not $GameDir){$GameDir=Auto-FindGame}
if(-not $GameDir -and -not $NoGui){$GameDir=Select-GameFolder}
if(-not $GameDir){throw 'GameDir tidak ditemukan.'}
$GameDir=[IO.Path]::GetFullPath($GameDir).TrimEnd('\')
$data0=Join-Path $GameDir 'ph_ft\source\data0.pak'
if(-not(Test-Path $data0)){throw "data0.pak tidak ditemukan: $data0"}
$seven=Find-7Zip

$targets=@(
'ai/includes/infected_data_params.scr',
'presets/logic/humanai/humanai_infected_special.def',
'presets/logic/humanai/humanai_entity_variants.def',
'presets/logic/humanai/humanai_dlc_ft_ailife.def',
'presets/logic/humanai/humanai_dlc_ft_combat.def',
'presets/logic/humanai/humanai_open_world.def',
'presets/owa_infected_set_settings.def',
'presets/pm_infected_set_settings.def',
'presets/dlc_dlo/dlo_owa_infected_set_settings.def',
'scripts/inventory/inventory_infected.scr',
'ai/datapresets/biter_armored.scr',
'ai/datapresets/m_biter_armored_boss_reinforcement.scr',
'ai/datapresets/m_biter_boss_reinforcement.scr',
'ai/datapresets/m_biter_gre.scr',
'ai/datapresets/m_biter_woman_gre.scr'
)

$out=Join-Path $repoRoot 'local_research\special_infected_mapping_1.71E'
if(Test-Path $out){Remove-Item -Recurse -Force $out}
New-Item -ItemType Directory -Force -Path $out|Out-Null

foreach($target in $targets){
    Write-Host "READ-ONLY EXTRACT: $target"
    & $seven x -y $data0 $target "-o$out" | Out-Null
}
$missing=@()
foreach($target in $targets){
    $p=Join-Path $out ($target -replace '/','\')
    if(-not(Test-Path $p)){$missing+=$target}
}
if($missing.Count){throw "Collector incomplete. Missing: $($missing -join ', ')"}

$terms='loot|Loot|inventory|Inventory|demol|Demol|goon|Goon|charger|Charger|volatile|Volatile|tyrant|Tyrant|screamer|Screamer|spitter|Spitter|banshee|Banshee|suicider|Suicider|special|Special'
$hits=@()
Get-ChildItem $out -Recurse -File | Where-Object {$_.Name -ne '_SPECIAL_INFECTED_MAPPING_REPORT.txt'} | ForEach-Object {
    $rel=$_.FullName.Substring($out.Length+1).Replace('\','/')
    $ln=0
    Get-Content $_.FullName | ForEach-Object {
        $ln++
        if($_ -match $terms){$hits += ('{0}:{1}: {2}' -f $rel,$ln,$_)}
    }
}
$report=Join-Path $out '_SPECIAL_INFECTED_MAPPING_REPORT.txt'
@(
'THE BEAST PROJECT - SPECIAL INFECTED MAPPING REPORT',
'READ-ONLY collector; NO gameplay/DLC/save files modified.',
"GameDir=$GameDir",
"Source=$data0",
"Targets=$($targets.Count)",
"Missing=$($missing.Count)",
'',
'=== MATCHES ==='
)+$hits | Set-Content -Encoding UTF8 $report

Write-Host ''
Write-Host 'PASS: collector selesai tanpa mengubah instalasi game.'
Write-Host "Report=$report"
Write-Host 'Upload _SPECIAL_INFECTED_MAPPING_REPORT.txt ke chat untuk analisis.'
