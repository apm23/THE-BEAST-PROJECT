param(
    [string]$GameDir
)

$ErrorActionPreference='Stop'
$toolsDir=Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot=Split-Path -Parent $toolsDir
$extractor=Join-Path $toolsDir 'extract_targeted_baseline_1.71E.ps1'
$builder=Join-Path $toolsDir 'build_user_special45_payload.py'

function Find-Python {
    $py=Get-Command py.exe -ErrorAction SilentlyContinue
    if($py){return [PSCustomObject]@{Exe=$py.Source;Args=@('-3')}}
    $python=Get-Command python.exe -ErrorAction SilentlyContinue
    if($python){return [PSCustomObject]@{Exe=$python.Source;Args=@()}}
    $python3=Get-Command python3.exe -ErrorAction SilentlyContinue
    if($python3){return [PSCustomObject]@{Exe=$python3.Source;Args=@()}}
    return $null
}

Write-Host '=============================================================='
Write-Host ' THE BEAST PROJECT - 1.71E PORTABLE BOOTSTRAP'
Write-Host '=============================================================='
Write-Host ''
Write-Host '1/2 Verify + extract exact 58-file 1.71E local baseline'
if($GameDir){
    & $extractor -GameDir $GameDir
}else{
    & $extractor
}
if($LASTEXITCODE -and $LASTEXITCODE -ne 0){throw "Baseline extractor gagal. ExitCode=$LASTEXITCODE"}

$py=Find-Python
if(-not $py){throw 'Python 3 tidak ditemukan. Install Python 3 lalu jalankan bootstrap lagi.'}

Write-Host ''
Write-Host '2/2 Rebuild exact USER HIGH LOOT SPECIAL45 payload + prepare switcher'
$args=@();$args+=$py.Args;$args+=@($builder,'--prepare-switcher')
& $py.Exe @args
if($LASTEXITCODE -ne 0){throw "Payload builder gagal. ExitCode=$LASTEXITCODE"}

$payload=Join-Path $repoRoot 'tools\runtime_switcher\data2_payload.pak'
if(-not(Test-Path $payload)){throw 'Verified payload belum muncul di runtime_switcher.'}
$hash=(Get-FileHash $payload -Algorithm SHA256).Hash.ToLowerInvariant()
$expected='190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'
if($hash -ne $expected){throw "Final payload hash mismatch. Expected=$expected Actual=$hash"}

Write-Host ''
Write-Host '=============================================================='
Write-Host ' BOOTSTRAP = PASS'
Write-Host '=============================================================='
Write-Host "Payload=$payload"
Write-Host "SHA256=$hash"
Write-Host ''
Write-Host 'Switcher source sekarang siap dipakai:'
Write-Host ' tools\runtime_switcher\1_SWITCH_TO_COOP_MULTIMOD.cmd'
Write-Host ' tools\runtime_switcher\2_SWITCH_BACK_NORMAL_PROVEN.cmd'
Write-Host ' tools\runtime_switcher\3_CHECK_CURRENT_MODE.cmd'
