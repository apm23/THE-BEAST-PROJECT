. "$PSScriptRoot\MODE_SWITCH_COMMON.ps1"

if(-not(IsAdmin)){
 Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
 exit $LASTEXITCODE
}

$snaps=@()
try{
 if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){throw 'Tutup game dulu.'}
 AssertPayload
 $r=PrintModeStatus 'PRE-SWITCH -> COOP MULTIMOD'
 $g=$r.Game;$p=$r.Info.Paths
 if(-not $r.Info.Loader.Confirmed){throw "MultiMod belum terdeteksi lengkap. Butuh folder ph_ft\MultiMod DAN ph_ft\work\bin\x64\CustomPak.ini. Install Data Pak Limit Bypass dulu, lalu jalankan switch ini lagi."}
 AssertOurOrAbsent $g $p.Source2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Source3 'data3'|Out-Null
 AssertOurOrAbsent $g $p.Multi2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Multi3 'data3'|Out-Null
 $tempRecipe=Join-Path $env:TEMP ('DLTB_SWITCH_RECIPE_'+[guid]::NewGuid().ToString('N')+'.pak')
 $recipe=BuildRecipePak $g $tempRecipe
 $backupRoot=NewBackupRoot $g 'TO_COOP'
 $save=BackupSaves $backupRoot
 $snaps=@(
  (Snapshot $p.Source2 $backupRoot 'source_data2_before.pak'),
  (Snapshot $p.Source3 $backupRoot 'source_data3_before.pak'),
  (Snapshot $p.Multi2 $backupRoot 'multimod_data2_before.pak'),
  (Snapshot $p.Multi3 $backupRoot 'multimod_data3_before.pak')
 )
 InstallVerified $SwitchPayload $p.Multi2 $SwitchPayloadHash $backupRoot 'replace_multimod_data2.pak'
 InstallVerified $tempRecipe $p.Multi3 $recipe.Hash $backupRoot 'replace_multimod_data3.pak'
 if(Test-Path $p.Source2){if(-not(IsKnownData2 (HashOrAbsent $p.Source2))){throw 'Source data2 became unknown during switch.'};Remove-Item $p.Source2 -Force}
 if(Test-Path $p.Source3){if(-not(IsKnownRecipe $g (HashOrAbsent $p.Source3))){throw 'Source data3 became unknown during switch.'};Remove-Item $p.Source3 -Force}
 if((HashOrAbsent $p.Source2) -ne 'ABSENT' -or (HashOrAbsent $p.Source3) -ne 'ABSENT'){throw 'Source cleanup verify gagal.'}
 if((HashOrAbsent $p.Multi2) -ne $SwitchPayloadHash){throw 'MultiMod data2 verify gagal.'}
 if((HashOrAbsent $p.Multi3) -ne $recipe.Hash){throw 'MultiMod data3 verify gagal.'}
 WriteSwitchState $g 'COOP_MULTIMOD' $SwitchPayloadHash $recipe.Hash $p.Multi2 $p.Multi3 $backupRoot $save
 RemoveLegacyStates $g
 PrintModeStatus 'POST-SWITCH -> COOP MULTIMOD'|Out-Null
 Write-Host '';Write-Host 'SWITCH TO COOP = PASS';Write-Host 'Mod kita sekarang hanya aktif lewat ph_ft\MultiMod.'
}catch{
 $msg=$_.Exception.Message
 Write-Host '';Write-Host 'SWITCH TO COOP STOP / FAIL-SAFE';Write-Host $msg
 if($snaps.Count -gt 0){Write-Host 'Mencoba rollback empat slot...';foreach($s in $snaps){try{RestoreSnapshot $s}catch{}}}
 try{PrintModeStatus 'STATUS AFTER FAIL / ROLLBACK'|Out-Null}catch{}
 exit 1
}
