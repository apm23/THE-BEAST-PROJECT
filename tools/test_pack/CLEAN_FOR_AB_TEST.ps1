. "$PSScriptRoot\TBP_AB_TEST_COMMON.ps1"

try {
    $r=Backup-And-Clean-ModState 'MANUAL_CLEAN'
    Write-Host ''
    Write-Host 'READY: game sekarang bersih dari live mod dataN PAK / MultiMod routing.'
    Write-Host 'Save tidak dihapus; backup save dibuat sebelum clean.'
    Write-Host "Quarantine=$($r.BackupRoot)"
    exit 0
} catch {
    Write-Host ''
    Write-Host 'CLEAN = STOP / FAIL-SAFE'
    Write-Host $_.Exception.Message
    exit 1
}
