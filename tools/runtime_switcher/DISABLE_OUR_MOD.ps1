. "$PSScriptRoot\MODE_SWITCH_COMMON.ps1"

if(-not(IsAdmin)){
 Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
 exit $LASTEXITCODE
}
$snaps=@()
try{
 if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){throw 'Tutup game dulu.'}
 $r=PrintModeStatus 'PRE-DISABLE OUR MOD'
 $g=$r.Game;$p=$r.Info.Paths
 AssertOurOrAbsent $g $p.Source2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Source3 'data3'|Out-Null
 AssertOurOrAbsent $g $p.Multi2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Multi3 'data3'|Out-Null
 $backupRoot=NewBackupRoot $g 'DISABLE'
 $save=BackupSaves $backupRoot
 $snaps=@(
  (Snapshot $p.Source2 $backupRoot 'source_data2_before.pak'),
  (Snapshot $p.Source3 $backupRoot 'source_data3_before.pak'),
  (Snapshot $p.Multi2 $backupRoot 'multimod_data2_before.pak'),
  (Snapshot $p.Multi3 $backupRoot 'multimod_data3_before.pak')
 )
 foreach($x in @($p.Source2,$p.Source3,$p.Multi2,$p.Multi3)){if(Test-Path $x){Remove-Item $x -Force}}
 if(Test-Path $p.State){Remove-Item $p.State -Force}
 RemoveLegacyStates $g
 $post=PrintModeStatus 'POST-DISABLE OUR MOD'
 if($post.Info.Mode -ne 'OUR_MOD_DISABLED'){throw 'Disable verify gagal.'}
 Write-Host '';Write-Host 'DISABLE OUR MOD = PASS';Write-Host 'MultiMod loader tidak dihapus; hanya PAK milik mod kita yang dibersihkan.'
}catch{
 $msg=$_.Exception.Message
 Write-Host '';Write-Host 'DISABLE STOP / FAIL-SAFE';Write-Host $msg
 if($snaps.Count -gt 0){foreach($s in $snaps){try{RestoreSnapshot $s}catch{}}}
 exit 1
}
