. "$PSScriptRoot\TBP_AB_TEST_COMMON.ps1"
try { Show-AbStatus; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }
