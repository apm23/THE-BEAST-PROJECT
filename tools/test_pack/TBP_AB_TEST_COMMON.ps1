$ErrorActionPreference='Stop'

$TestPackRoot=Split-Path -Parent $PSScriptRoot
$RepoRoot=Split-Path -Parent $TestPackRoot
$RuntimeDir=Join-Path $TestPackRoot 'runtime_switcher'
$CleanupBackupName='_THE_BEAST_PROJECT_BACKUPS'
$AbStateName='DLTB_TBP_AB_TEST_STATE.json'
$ProvenHash='190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'

. (Join-Path $RuntimeDir 'TBP_COMMON.ps1')

function Assert-GameClosed {
    if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){
        throw 'Tutup Dying Light: The Beast dulu.'
    }
}

function Find-Python3 {
    $py=Get-Command py.exe -ErrorAction SilentlyContinue
    if($py){return [PSCustomObject]@{Exe=$py.Source;Args=@('-3')}}
    $python=Get-Command python.exe -ErrorAction SilentlyContinue
    if($python){return [PSCustomObject]@{Exe=$python.Source;Args=@()}}
    $python3=Get-Command python3.exe -ErrorAction SilentlyContinue
    if($python3){return [PSCustomObject]@{Exe=$python3.Source;Args=@()}}
    throw 'Python 3 tidak ditemukan.'
}

function Get-AbPaths($g) {
    $ph=Join-Path $g.GameDir 'ph_ft'
    [PSCustomObject]@{
        PhFt=$ph
        Source=$g.SourceDir
        Data0=$g.Data0
        Data1=$g.Data1
        Data2=$g.Data2
        Data3=$g.Data3
        MultiMod=(Join-Path $ph 'MultiMod')
        CustomPakIni=(Join-Path $ph 'work\bin\x64\CustomPak.ini')
        AbState=(Join-Path $ph $AbStateName)
        ModeState=(Join-Path $ph 'DLTB_TBP_MODE_STATE.json')
        OneClickState=(Join-Path $g.SourceDir 'DLTB_TBP_ONECLICK_STATE.json')
        OldV4State=(Join-Path $g.SourceDir 'DLTB_STEP1_SEPARATE_PAK_V4_STATE.json')
    }
}

function New-AbBackupRoot($g,[string]$tag) {
    $p=Get-AbPaths $g
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
    $root=Join-Path $p.PhFt ($CleanupBackupName+'\AB_'+$tag+'_'+$stamp)
    New-Item -ItemType Directory -Force -Path $root|Out-Null
    return $root
}

function Move-Safe([string]$src,[string]$dst) {
    if(-not(Test-Path -LiteralPath $src)){return $false}
    $parent=Split-Path $dst -Parent
    New-Item -ItemType Directory -Force -Path $parent|Out-Null
    if(Test-Path -LiteralPath $dst){
        $dst=$dst+'.'+[guid]::NewGuid().ToString('N')
    }
    Move-Item -LiteralPath $src -Destination $dst -Force
    return $true
}

function Get-LiveModPaks($g) {
    $p=Get-AbPaths $g
    $official=@(
        [IO.Path]::GetFullPath($p.Data0).ToLowerInvariant(),
        [IO.Path]::GetFullPath($p.Data1).ToLowerInvariant()
    )
    $backupRoot=Join-Path $p.PhFt $CleanupBackupName
    $out=@()
    if(Test-Path $p.PhFt){
        Get-ChildItem -LiteralPath $p.PhFt -Recurse -File -Filter 'data*.pak' -ErrorAction SilentlyContinue | ForEach-Object {
            $full=[IO.Path]::GetFullPath($_.FullName)
            $low=$full.ToLowerInvariant()
            if($official -contains $low){return}
            if($full.StartsWith($backupRoot,[StringComparison]::OrdinalIgnoreCase)){return}
            if($_.Name -match '^data\d+\.pak$'){$out+=$_}
        }
    }
    return @($out)
}

function Backup-And-Clean-ModState([string]$Tag='CLEAN') {
    Assert-GameClosed
    $g=FindGame
    $p=Get-AbPaths $g
    if(-not(Test-Path $p.Data0) -or -not(Test-Path $p.Data1)){
        throw 'Official data0.pak/data1.pak tidak lengkap. STOP.'
    }

    $backup=New-AbBackupRoot $g $Tag
    $save=BackupSaves $backup
    $moved=New-Object System.Collections.Generic.List[string]

    # Disable and quarantine the complete MultiMod directory first.
    if(Test-Path $p.MultiMod){
        $dst=Join-Path $backup 'loader\MultiMod'
        if(Move-Safe $p.MultiMod $dst){$moved.Add($p.MultiMod)}
    }
    if(Test-Path $p.CustomPakIni){
        $dst=Join-Path $backup 'loader\CustomPak.ini'
        if(Move-Safe $p.CustomPakIni $dst){$moved.Add($p.CustomPakIni)}
    }

    # Quarantine every live dataN.pak except official data0/data1, including
    # old source data2/data3 and stray experiment PAKs from prior tests.
    foreach($f in @(Get-LiveModPaks $g)){
        $relative=$f.FullName.Substring($p.PhFt.Length).TrimStart('\')
        $dst=Join-Path $backup ('paks\'+$relative)
        if(Move-Safe $f.FullName $dst){$moved.Add($f.FullName)}
    }

    # Quarantine project state markers so no previous experiment is mistaken for current state.
    foreach($state in @($p.AbState,$p.ModeState,$p.OneClickState,$p.OldV4State)){
        if(Test-Path $state){
            $dst=Join-Path $backup ('state\'+(Split-Path $state -Leaf))
            if(Move-Safe $state $dst){$moved.Add($state)}
        }
    }

    $remain=@(Get-LiveModPaks $g)
    if($remain.Count -ne 0){
        throw ('CLEAN verify gagal. Live mod PAK masih ada: '+(($remain|ForEach-Object{$_.FullName}) -join '; '))
    }
    if(Test-Path $p.MultiMod){throw 'CLEAN verify gagal: MultiMod masih live.'}
    if(Test-Path $p.CustomPakIni){throw 'CLEAN verify gagal: CustomPak.ini masih live.'}

    $report=[ordered]@{
        Generated=(Get-Date -Format o)
        GameDir=$g.GameDir
        Status='VANILLA_DATA_PAK_CLEAN'
        OfficialData0=$p.Data0
        OfficialData1=$p.Data1
        MovedCount=$moved.Count
        Moved=@($moved)
        SaveBackup=$save.Path
        SaveBackupCount=$save.Count
        BackupRoot=$backup
    }
    $reportPath=Join-Path $backup 'CLEAN_REPORT.json'
    $report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $reportPath -Encoding UTF8

    Write-Host ''
    Write-Host '=============================================================='
    Write-Host ' CLEAN MOD STATE = PASS'
    Write-Host '=============================================================='
    Write-Host "Official kept : data0.pak + data1.pak"
    Write-Host "Moved/quarantine: $($moved.Count)"
    Write-Host "Backup        : $backup"
    Write-Host "Save backup   : $($save.Path)"
    Write-Host 'Live MultiMod : ABSENT'
    Write-Host 'Live mod PAKs : ABSENT'
    return [PSCustomObject]@{Game=$g;Paths=$p;BackupRoot=$backup;Save=$save;Report=$reportPath}
}

function Install-VerifiedDynamic([string]$src,[string]$dst,[string]$expected) {
    if(-not(Test-Path $src)){throw "Source tidak ada: $src"}
    $actual=(Get-FileHash $src -Algorithm SHA256).Hash.ToLowerInvariant()
    if($actual -ne $expected){throw "Source hash mismatch: $src"}
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent)|Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
    $installed=(Get-FileHash $dst -Algorithm SHA256).Hash.ToLowerInvariant()
    if($installed -ne $expected){throw "Installed hash mismatch: $dst"}
}

function Write-AbState($g,[string]$mode,[string]$d2hash,[string]$d3hash,[string]$cleanBackup) {
    $p=Get-AbPaths $g
    $o=[ordered]@{
        Edition='USER_SPECIAL45_AB_TEST'
        Mode=$mode
        UpdatedAt=(Get-Date -Format o)
        GameDir=$g.GameDir
        Data2Hash=$d2hash
        Data3Hash=$d3hash
        ParentProvenSpecial45=$ProvenHash
        CleanBackup=$cleanBackup
    }
    $o|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $p.AbState -Encoding UTF8
}

function Show-AbStatus {
    $g=FindGame
    $p=Get-AbPaths $g
    $mods=@(Get-LiveModPaks $g)
    Write-Host ''
    Write-Host '=============================================================='
    Write-Host ' THE BEAST PROJECT - A/B TEST STATUS'
    Write-Host '=============================================================='
    Write-Host "GAME=$($g.GameDir)"
    Write-Host "data0=$((HashOrAbsent $p.Data0)) [OFFICIAL SLOT]"
    Write-Host "data1=$((HashOrAbsent $p.Data1)) [OFFICIAL SLOT]"
    Write-Host "data2=$((HashOrAbsent $p.Data2))"
    Write-Host "data3=$((HashOrAbsent $p.Data3))"
    Write-Host "MultiMod=$(if(Test-Path $p.MultiMod){'PRESENT'}else{'ABSENT'})"
    Write-Host "CustomPak.ini=$(if(Test-Path $p.CustomPakIni){'PRESENT'}else{'ABSENT'})"
    Write-Host "Live non-official dataN PAK count=$($mods.Count)"
    if(Test-Path $p.AbState){
        try{$s=Get-Content -Raw $p.AbState|ConvertFrom-Json;Write-Host "AB_MODE=$($s.Mode)";Write-Host "AB_D2=$($s.Data2Hash)"}catch{Write-Host 'AB_STATE=INVALID'}
    }else{Write-Host 'AB_STATE=ABSENT'}
}
