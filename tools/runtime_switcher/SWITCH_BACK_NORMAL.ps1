. "$PSScriptRoot\MODE_SWITCH_COMMON.ps1"

if(-not(IsAdmin)){
 Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
 exit $LASTEXITCODE
}

$snaps=@()
try{
 if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){throw 'Tutup game dulu.'}
 AssertPayload
 $r=PrintModeStatus 'PRE-SWITCH -> NORMAL PROVEN'
 $g=$r.Game;$p=$r.Info.Paths
 AssertOurOrAbsent $g $p.Source2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Source3 'data3'|Out-Null
 AssertOurOrAbsent $g $p.Multi2 'data2'|Out-Null
 AssertOurOrAbsent $g $p.Multi3 'data3'|Out-Null
 $tempRecipe=Join-Path $env:TEMP ('DLTB_SWITCH_RECIPE_'+[guid]::NewGuid().ToString('N')+'.pak')
 $recipe=BuildRecipePak $g $tempRecipe
 $backupRoot=NewBackupRoot $g 'TO_NORMAL'
 $save=BackupSaves $backupRoot
 $snaps=@(
  (Snapshot $p.Source2 $backupRoot 'source_data2_before.pak'),
  (Snapshot $p.Source3 $backupRoot 'source_data3_before.pak'),
  (Snapshot $p.Multi2 $backupRoot 'multimod_data2_before.pak'),
  (Snapshot $p.Multi3 $backupRoot 'multimod_data3_before.pak')
 )
 InstallVerified $SwitchPayload $p.Source2 $SwitchPayloadHash $backupRoot 'replace_source_data2.pak'
 InstallVerified $tempRecipe $p.Source3 $recipe.Hash $backupRoot 'replace_source_data3.pak'
 if(Test-Path $p.Multi2){if(-not(IsKnownData2 (HashOrAbsent $p.Multi2))){throw 'MultiMod data2 became unknown during switch.'};Remove-Item $p.Multi2 -Force}
 if(Test-Path $p.Multi3){if(-not(IsKnownRecipe $g (HashOrAbsent $p.Multi3))){throw 'MultiMod data3 became unknown during switch.'};Remove-Item $p.Multi3 -Force}
 if((HashOrAbsent $p.Source2) -ne $SwitchPayloadHash){throw 'Source data2 verify gagal.'}
 if((HashOrAbsent $p.Source3) -ne $recipe.Hash){throw 'Source data3 verify gagal.'}
 if((HashOrAbsent $p.Multi2) -ne 'ABSENT' -or (HashOrAbsent $p.Multi3) -ne 'ABSENT'){throw 'MultiMod cleanup verify gagal.'}
 WriteSwitchState $g 'NORMAL_SOURCE' $SwitchPayloadHash $recipe.Hash $p.Source2 $p.Source3 $backupRoot $save
 RemoveLegacyStates $g
 PrintModeStatus 'POST-SWITCH -> NORMAL PROVEN'|Out-Null
 Write-Host '';Write-Host 'SWITCH BACK NORMAL = PASS';Write-Host 'Mod kembali ke ph_ft\source data2 + data3.'
}catch{
 $msg=$_.Exception.Message
 Write-Host '';Write-Host 'SWITCH BACK NORMAL STOP / FAIL-SAFE';Write-Host $msg
 if($snaps.Count -gt 0){Write-Host 'Mencoba rollback empat slot...';foreach($s in $snaps){try{RestoreSnapshot $s}catch{}}}
 try{PrintModeStatus 'STATUS AFTER FAIL / ROLLBACK'|Out-Null}catch{}
 exit 1
}
