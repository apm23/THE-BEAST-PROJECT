param(
    [ValidateSet("Status","EnterVanillaRecovery","RestoreMods","FindSaveBackups")]
    [string]$Action = "Status"
)

$ErrorActionPreference = "Stop"
$StateName = "TBP_DLC_RECOVERY_STATE.json"
$AppId = "3008130"
$PocMarker = "TBP_PHASE_C_EXOTIC_POC1_PISTOL_B_LEGENDARY.marker.json"

function Banner([string]$t) {
    Write-Host ""
    Write-Host "================================================================"
    Write-Host " $t"
    Write-Host "================================================================"
}

function Add-Unique([hashtable]$map,[string]$path) {
    if([string]::IsNullOrWhiteSpace($path)){ return }
    try { $full=[IO.Path]::GetFullPath($path).TrimEnd('\') } catch { return }
    $k=$full.ToLowerInvariant()
    if(-not $map.ContainsKey($k)){ $map[$k]=$full }
}

function Get-SteamRoots {
    $m=@{}
    try {
        $p=(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath
        if($p){ Add-Unique $m $p }
    } catch {}
    try {
        $p=(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath
        if($p){ Add-Unique $m $p }
    } catch {}
    foreach($p in @("${env:ProgramFiles(x86)}\Steam","${env:ProgramFiles}\Steam","C:\Steam")) {
        if($p -and (Test-Path -LiteralPath $p)){ Add-Unique $m $p }
    }
    @($m.Values)
}

function Get-SteamLibraries {
    $m=@{}
    foreach($r in Get-SteamRoots) {
        if(Test-Path -LiteralPath $r){ Add-Unique $m $r }
        $vdf=Join-Path $r 'steamapps\libraryfolders.vdf'
        if(Test-Path -LiteralPath $vdf) {
            try {
                $t=Get-Content -Raw -LiteralPath $vdf
                foreach($x in [regex]::Matches($t,'"path"\s*"([^"]+)"')) {
                    $p=$x.Groups[1].Value -replace '\\\\','\'
                    if(Test-Path -LiteralPath $p){ Add-Unique $m $p }
                }
            } catch {}
        }
    }
    @($m.Values)
}

function Find-Game {
    $m=@{}
    foreach($lib in Get-SteamLibraries) {
        $g=Join-Path $lib 'steamapps\common\Dying Light The Beast'
        if(Test-Path -LiteralPath (Join-Path $g 'ph_ft\source\data0.pak')) {
            Add-Unique $m $g
        }
    }
    $games=@($m.Values)
    if($games.Count -eq 0){ throw "Dying Light The Beast tidak ditemukan." }
    if($games.Count -gt 1){ throw "Lebih dari satu instalasi nyata ditemukan.`r`n$($games -join "`r`n")" }
    $games[0]
}

function Assert-GameClosed {
    if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue) {
        throw "Tutup Dying Light: The Beast dulu."
    }
}

function HashFile([string]$p) {
    if(-not(Test-Path -LiteralPath $p)){ return $null }
    (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-SourceDataPaks([string]$source) {
    $out=@()
    Get-ChildItem -LiteralPath $source -File -ErrorAction SilentlyContinue | ForEach-Object {
        $m=[regex]::Match($_.Name,'^data(\d+)\.pak$',[Text.RegularExpressions.RegexOptions]::IgnoreCase)
        if($m.Success) {
            $n=[int]$m.Groups[1].Value
            if($n -ge 2){ $out += $_ }
        }
    }
    @($out | Sort-Object Name)
}

function Get-MultiModPaks([string]$mm) {
    if(-not(Test-Path -LiteralPath $mm)){ return @() }
    @(
        Get-ChildItem -LiteralPath $mm -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^data\d+\.pak$' } |
        Sort-Object Name
    )
}

function Backup-CurrentSaves([string]$dest) {
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    $copied=@()
    foreach($steam in Get-SteamRoots) {
        $ud=Join-Path $steam 'userdata'
        if(-not(Test-Path -LiteralPath $ud)){ continue }
        Get-ChildItem -LiteralPath $ud -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $src=Join-Path $_.FullName "$AppId\remote\out"
            if(Test-Path -LiteralPath $src) {
                $d=Join-Path $dest ("Steam_"+$_.Name+"_out")
                Copy-Item -LiteralPath $src -Destination $d -Recurse -Force
                $copied += [pscustomobject]@{Source=$src; Backup=$d}
            }
        }
    }
    @($copied)
}

function Test-ZipReadable([string]$path) {
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $z=[IO.Compression.ZipFile]::OpenRead($path)
        try {
            $entryCount=$z.Entries.Count
            $hasPoc=$false
            foreach($e in $z.Entries) {
                if($e.FullName.Replace('\','/').ToLowerInvariant() -eq $PocMarker.ToLowerInvariant()) {
                    $hasPoc=$true; break
                }
            }
            [pscustomobject]@{Readable=$true; Entries=$entryCount; HasRejectedPocMarker=$hasPoc}
        } finally { $z.Dispose() }
    } catch {
        [pscustomobject]@{Readable=$false; Entries=0; HasRejectedPocMarker=$false; Error=$_.Exception.Message}
    }
}

function Status {
    $game=Find-Game
    $ph=Join-Path $game 'ph_ft'
    $source=Join-Path $ph 'source'
    $mm=Join-Path $ph 'MultiMod'
    $cp=Join-Path $ph 'work\bin\x64\CustomPak.ini'
    $state=Join-Path $ph $StateName

    Banner "GH1 DLC RECOVERY STATUS"
    Write-Host "GAME=$game"
    Write-Host "STATE=$(if(Test-Path $state){'RECOVERY_ACTIVE'}else{'NORMAL'})"
    Write-Host "CustomPak.ini=$(if(Test-Path $cp){'PRESENT'}else{'ABSENT'})"
    Write-Host ""
    Write-Host "SOURCE ACTIVE DATA PAKS:"
    foreach($p in Get-SourceDataPaks $source) {
        $z=Test-ZipReadable $p.FullName
        Write-Host (" - {0} sha={1} readable={2} rejectedPOC={3}" -f $p.Name,(HashFile $p.FullName),$z.Readable,$z.HasRejectedPocMarker)
    }
    Write-Host ""
    Write-Host "MULTIMOD ACTIVE DATA PAKS:"
    foreach($p in Get-MultiModPaks $mm) {
        $z=Test-ZipReadable $p.FullName
        Write-Host (" - {0} sha={1} readable={2} rejectedPOC={3}" -f $p.Name,(HashFile $p.FullName),$z.Readable,$z.HasRejectedPocMarker)
    }
}

function Enter-VanillaRecovery {
    Assert-GameClosed
    $game=Find-Game
    $ph=Join-Path $game 'ph_ft'
    $source=Join-Path $ph 'source'
    $mm=Join-Path $ph 'MultiMod'
    $cp=Join-Path $ph 'work\bin\x64\CustomPak.ini'
    $statePath=Join-Path $ph $StateName
    if(Test-Path -LiteralPath $statePath) {
        throw "Recovery state sudah aktif. Jalankan restore dulu."
    }

    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
    $root=Join-Path $ph ("_THE_BEAST_PROJECT_BACKUPS\DLC_RECOVERY_"+$stamp)
    $q=Join-Path $root 'QUARANTINE'
    New-Item -ItemType Directory -Force -Path $q | Out-Null

    Banner "BACKUP CURRENT SAVE"
    $saveBackup=Join-Path $root 'SAVE_CURRENT_BEFORE_DLC_RECOVERY'
    $saves=@(Backup-CurrentSaves $saveBackup)
    Write-Host "SAVE_BACKUPS=$($saves.Count)"
    Write-Host "SAVE_BACKUP_DIR=$saveBackup"

    $moved=@()
    foreach($p in Get-SourceDataPaks $source) {
        $z=Test-ZipReadable $p.FullName
        $destDir=Join-Path $q 'source'
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        $dest=Join-Path $destDir $p.Name
        Move-Item -LiteralPath $p.FullName -Destination $dest -Force
        $moved += [pscustomobject]@{
            Original=$p.FullName; Quarantine=$dest; SHA256=(HashFile $dest);
            ZipReadable=$z.Readable; RejectedPoc=$z.HasRejectedPocMarker
        }
    }

    foreach($p in Get-MultiModPaks $mm) {
        $destDir=Join-Path $q 'MultiMod'
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        $dest=Join-Path $destDir $p.Name
        Move-Item -LiteralPath $p.FullName -Destination $dest -Force
        $moved += [pscustomobject]@{
            Original=$p.FullName; Quarantine=$dest; SHA256=(HashFile $dest);
            ZipReadable=$true; RejectedPoc=$false
        }
    }

    $customPakBackup=$null
    if(Test-Path -LiteralPath $cp) {
        $destDir=Join-Path $q 'loader'
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        $customPakBackup=Join-Path $destDir 'CustomPak.ini'
        Move-Item -LiteralPath $cp -Destination $customPakBackup -Force
    }

    $state=[ordered]@{
        Version='GH1_DLC_RECOVERY_VANILLA_CYCLE_V1'
        Created=(Get-Date).ToString('o')
        Game=$game
        BackupRoot=$root
        SaveBackup=$saveBackup
        SaveBackupCount=$saves.Count
        Moved=@($moved)
        CustomPakOriginal=$cp
        CustomPakBackup=$customPakBackup
    }
    $state | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $statePath -Encoding UTF8

    Banner "VANILLA RECOVERY MODE READY"
    Write-Host "Launch game once in vanilla state, check DLC popup, close game, then restore."
}

function Restore-Mods {
    Assert-GameClosed
    $game=Find-Game
    $ph=Join-Path $game 'ph_ft'
    $statePath=Join-Path $ph $StateName
    if(-not(Test-Path -LiteralPath $statePath)) {
        throw "Recovery state tidak ditemukan."
    }
    $st=Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json
    foreach($x in @($st.Moved)) {
        if(-not(Test-Path -LiteralPath $x.Quarantine)) { throw "Quarantine file hilang: $($x.Quarantine)" }
        if(Test-Path -LiteralPath $x.Original) { throw "Target sudah ada; stop aman: $($x.Original)" }
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $x.Original) | Out-Null
        Move-Item -LiteralPath $x.Quarantine -Destination $x.Original
        if((HashFile $x.Original) -ne $x.SHA256) { throw "Hash mismatch setelah restore: $($x.Original)" }
    }
    if($st.CustomPakBackup -and (Test-Path -LiteralPath $st.CustomPakBackup)) {
        if(Test-Path -LiteralPath $st.CustomPakOriginal) { throw "CustomPak.ini target sudah ada." }
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $st.CustomPakOriginal) | Out-Null
        Move-Item -LiteralPath $st.CustomPakBackup -Destination $st.CustomPakOriginal
    }
    Remove-Item -LiteralPath $statePath -Force
    Banner "RESTORE COMPLETE"
}

function Find-SaveBackups {
    $game=Find-Game
    $ph=Join-Path $game 'ph_ft'
    $root=Join-Path $ph '_THE_BEAST_PROJECT_BACKUPS'
    if(-not(Test-Path -LiteralPath $root)) { Write-Host "Backup root tidak ditemukan."; return }
    $rows=@()
    Get-ChildItem -LiteralPath $root -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^SAVE_' -or $_.Name -eq 'SAVE_BEFORE_CHANGE' } |
        ForEach-Object {
            $files=Get-ChildItem -LiteralPath $_.FullName -File -Recurse -ErrorAction SilentlyContinue
            if($files) {
                $latest=($files | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
                $rows += [pscustomobject]@{Path=$_.FullName;FileCount=@($files).Count;LatestWrite=$latest}
            }
        }
    $report=Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'GH1_DLC_RECOVERY_SAVE_BACKUPS.txt'
    $rows | Sort-Object LatestWrite -Descending | Format-Table -AutoSize | Out-String | Set-Content -LiteralPath $report -Encoding UTF8
    $rows | Sort-Object LatestWrite -Descending | Format-Table -AutoSize
    Write-Host "REPORT=$report"
}

switch($Action) {
    "Status" { Status }
    "EnterVanillaRecovery" { Enter-VanillaRecovery }
    "RestoreMods" { Restore-Mods }
    "FindSaveBackups" { Find-SaveBackups }
}
