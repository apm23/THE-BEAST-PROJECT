. "$PSScriptRoot\TBP_AB_TEST_COMMON.ps1"

try {
    $clean=Backup-And-Clean-ModState 'BEFORE_PROVEN_CONTROL'
    $g=$clean.Game
    $p=$clean.Paths

    Write-Host ''
    Write-Host '1/4 Extract + verify exact 1.71E baseline'
    $extractor=Join-Path $TestPackRoot 'extract_targeted_baseline_1.71E.ps1'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $extractor -GameDir $g.GameDir -NoGui
    if($LASTEXITCODE -ne 0){throw "Baseline extraction gagal. ExitCode=$LASTEXITCODE"}

    Write-Host ''
    Write-Host '2/4 Rebuild exact proven USER HIGH LOOT SPECIAL45'
    $py=Find-Python3
    $builder=Join-Path $TestPackRoot 'build_user_special45_payload.py'
    $pyArgs=@();$pyArgs+=$py.Args;$pyArgs+=@($builder,'--prepare-switcher')
    & $py.Exe @pyArgs
    if($LASTEXITCODE -ne 0){throw "SPECIAL45 builder gagal. ExitCode=$LASTEXITCODE"}

    $payload=Join-Path $RuntimeDir 'data2_payload.pak'
    if(-not(Test-Path $payload)){throw 'Proven SPECIAL45 payload tidak ditemukan.'}
    $payloadHash=(Get-FileHash $payload -Algorithm SHA256).Hash.ToLowerInvariant()
    if($payloadHash -ne $ProvenHash){throw "Proven hash mismatch. Expected=$ProvenHash Actual=$payloadHash"}

    Write-Host ''
    Write-Host '3/4 Build proven recipe data3 from official current game archives'
    $tempRecipe=Join-Path $env:TEMP ('DLTB_AB_RECIPE_'+[guid]::NewGuid().ToString('N')+'.pak')
    $recipe=BuildRecipePak $g $tempRecipe

    Write-Host ''
    Write-Host '4/4 Install exact proven SPECIAL45 into clean NORMAL source slots'
    Install-VerifiedDynamic $payload $p.Data2 $ProvenHash
    Install-VerifiedDynamic $tempRecipe $p.Data3 $recipe.Hash
    Write-AbState $g 'PROVEN_SPECIAL45_CONTROL' $ProvenHash $recipe.Hash $clean.BackupRoot

    if((HashOrAbsent $p.Data2) -ne $ProvenHash){throw 'Final proven data2 verify gagal.'}
    if((HashOrAbsent $p.Data3) -ne $recipe.Hash){throw 'Final proven data3 verify gagal.'}
    if(Test-Path $p.MultiMod){throw 'MultiMod kembali muncul saat install proven.'}
    if(Test-Path $p.CustomPakIni){throw 'CustomPak.ini kembali muncul saat install proven.'}

    Write-Host ''
    Write-Host '=============================================================='
    Write-Host ' PROVEN SPECIAL45 CONTROL = INSTALLED'
    Write-Host '=============================================================='
    Write-Host "data2 SHA256=$ProvenHash"
    Write-Host "Recipe SHA256=$($recipe.Hash)"
    Write-Host 'Mode=NORMAL source; clean control for direct A/B comparison.'
    exit 0
} catch {
    Write-Host ''
    Write-Host 'INSTALL PROVEN CONTROL = STOP / FAIL-SAFE'
    Write-Host $_.Exception.Message
    try{Show-AbStatus}catch{}
    exit 1
}
