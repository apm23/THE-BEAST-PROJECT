. "$PSScriptRoot\TBP_AB_TEST_COMMON.ps1"

try {
    $clean=Backup-And-Clean-ModState 'BEFORE_NEW_TEST'
    $g=$clean.Game
    $p=$clean.Paths

    Write-Host ''
    Write-Host '1/4 Extract + verify exact 1.71E baseline'
    $extractor=Join-Path $TestPackRoot 'extract_targeted_baseline_1.71E.ps1'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $extractor -GameDir $g.GameDir -NoGui
    if($LASTEXITCODE -ne 0){throw "Baseline extraction gagal. ExitCode=$LASTEXITCODE"}

    Write-Host ''
    Write-Host '2/4 Build SPECIAL45-derived Biter resource parity candidate'
    $py=Find-Python3
    $builder=Join-Path $TestPackRoot 'build_user_special45_biter_resource_parity.py'
    $pyArgs=@();$pyArgs+=$py.Args;$pyArgs+=@($builder)
    & $py.Exe @pyArgs
    if($LASTEXITCODE -ne 0){throw "Candidate builder gagal. ExitCode=$LASTEXITCODE"}

    $candidate=Join-Path $RepoRoot 'local_build\USER_SPECIAL45_BITER_RESOURCE_PARITY\data2_payload.pak'
    $manifest=Join-Path $RepoRoot 'local_build\USER_SPECIAL45_BITER_RESOURCE_PARITY\BUILD_MANIFEST.json'
    if(-not(Test-Path $candidate) -or -not(Test-Path $manifest)){throw 'Candidate output/manifest tidak ditemukan.'}
    $m=Get-Content -Raw $manifest|ConvertFrom-Json
    if($m.runtime_status -ne 'CANDIDATE_NOT_RUNTIME_GREEN'){throw 'Candidate manifest status tidak sesuai.'}
    if($m.derived_from_data2_sha256 -ne $ProvenHash){throw 'Candidate bukan turunan exact SPECIAL45 proven.'}
    $candidateHash=(Get-FileHash $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
    if($candidateHash -ne [string]$m.candidate_data2_sha256){throw 'Candidate hash tidak cocok dengan manifest.'}

    Write-Host ''
    Write-Host '3/4 Build proven recipe data3 from official current game archives'
    $tempRecipe=Join-Path $env:TEMP ('DLTB_AB_RECIPE_'+[guid]::NewGuid().ToString('N')+'.pak')
    $recipe=BuildRecipePak $g $tempRecipe

    Write-Host ''
    Write-Host '4/4 Install candidate into clean NORMAL source slots'
    Install-VerifiedDynamic $candidate $p.Data2 $candidateHash
    Install-VerifiedDynamic $tempRecipe $p.Data3 $recipe.Hash
    Write-AbState $g 'NEW_BITER_RESOURCE_TEST' $candidateHash $recipe.Hash $clean.BackupRoot

    if((HashOrAbsent $p.Data2) -ne $candidateHash){throw 'Final data2 verify gagal.'}
    if((HashOrAbsent $p.Data3) -ne $recipe.Hash){throw 'Final data3 verify gagal.'}
    if(Test-Path $p.MultiMod){throw 'MultiMod kembali muncul saat install.'}
    if(Test-Path $p.CustomPakIni){throw 'CustomPak.ini kembali muncul saat install.'}

    Write-Host ''
    Write-Host '=============================================================='
    Write-Host ' NEW BITER RESOURCE TEST = INSTALLED'
    Write-Host '=============================================================='
    Write-Host "Candidate SHA256=$candidateHash"
    Write-Host "Parent SPECIAL45=$ProvenHash"
    Write-Host "Recipe SHA256=$($recipe.Hash)"
    Write-Host 'Mode=NORMAL source; MultiMod disabled for isolated test.'
    Write-Host 'TEST: corpse F, Battery/Electrical Parts/Pigments/Oxidizer, quantity, DLC popup, save/reload.'
    exit 0
} catch {
    Write-Host ''
    Write-Host 'INSTALL NEW TEST = STOP / FAIL-SAFE'
    Write-Host $_.Exception.Message
    try{Show-AbStatus}catch{}
    exit 1
}
