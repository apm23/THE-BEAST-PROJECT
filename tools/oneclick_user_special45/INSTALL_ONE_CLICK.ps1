. "$PSScriptRoot\TBP_COMMON.ps1"
$Edition='USER_HIGH_LOOT_SPECIAL45'
$PayloadHash='190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'
$Payload=Join-Path $PSScriptRoot 'data2_payload.pak'

if(-not(IsAdmin)){
 Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
 exit $LASTEXITCODE
}

$game=$null;$pre2='ABSENT';$pre3='ABSENT';$backup2=$null;$backup3=$null
$wrote2=$false;$wrote3=$false
try{
 if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){throw 'Tutup game dulu.'}
 $game=ShowStatus 'PRE-INSTALL DETECTOR'
 if(-not(Test-Path $game.Data1)){throw 'data1.pak tidak ditemukan.'}

 $ph=(Get-FileHash $Payload -Algorithm SHA256).Hash.ToLowerInvariant()
 if($ph -ne $PayloadHash){throw "Payload data2 corrupt. Expected=$PayloadHash Actual=$ph"}

 $pre2=HashOrAbsent $game.Data2;$pre3=HashOrAbsent $game.Data3
 $label2=LabelData2 $pre2
 if($pre2 -ne 'ABSENT' -and $label2 -eq 'UNKNOWN'){throw "STOP AMAN: data2.pak unknown. SHA=$pre2"}

 if($pre3 -ne 'ABSENT'){
  $allow=$false
  $st=ReadState $game;if($st -and $st.Data3Hash -eq $pre3){$allow=$true}
  $v4=GetOldV4State $game;if($v4 -and $v4.RecipePakHash -eq $pre3){$allow=$true}
  if($pre3 -eq $KnownOldRecipeHash){$allow=$true}
  if(-not $allow){throw "STOP AMAN: data3.pak unknown. SHA=$pre3"}
 }

 $tempRecipe=Join-Path $env:TEMP ('DLTB_ONECLICK_RECIPE_FINAL_'+[guid]::NewGuid().ToString('N')+'.pak')
 $recipe=BuildRecipePak $game $tempRecipe

 $stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
 $backupRoot=Join-Path $game.SourceDir ("_THE_BEAST_PROJECT_BACKUPS\ONECLICK_"+$Edition+"_"+$stamp)
 New-Item -ItemType Directory -Force -Path $backupRoot|Out-Null
 $save=BackupSaves $backupRoot
 if(Test-Path $game.Data2){$backup2=Join-Path $backupRoot 'data2_before.pak';Copy-Item $game.Data2 $backup2 -Force}
 if(Test-Path $game.Data3){$backup3=Join-Path $backupRoot 'data3_before.pak';Copy-Item $game.Data3 $backup3 -Force}

 $side2=Join-Path $game.SourceDir ('.data2.'+[guid]::NewGuid().ToString('N')+'.tmp')
 $side3=Join-Path $game.SourceDir ('.data3.'+[guid]::NewGuid().ToString('N')+'.tmp')
 Copy-Item $Payload $side2 -Force;Copy-Item $tempRecipe $side3 -Force
 if((Get-FileHash $side2 -Algorithm SHA256).Hash.ToLowerInvariant() -ne $PayloadHash){throw 'Side data2 checksum mismatch.'}
 if((Get-FileHash $side3 -Algorithm SHA256).Hash.ToLowerInvariant() -ne $recipe.Hash){throw 'Side data3 checksum mismatch.'}

 if(Test-Path $game.Data2){$rb=Join-Path $backupRoot 'replace_data2_backup.pak';[IO.File]::Replace($side2,$game.Data2,$rb,$true)}else{Move-Item $side2 $game.Data2}
 $wrote2=$true
 if((HashOrAbsent $game.Data2) -ne $PayloadHash){throw 'Installed data2 checksum mismatch.'}

 if(Test-Path $game.Data3){$rb3=Join-Path $backupRoot 'replace_data3_backup.pak';[IO.File]::Replace($side3,$game.Data3,$rb3,$true)}else{Move-Item $side3 $game.Data3}
 $wrote3=$true
 if((HashOrAbsent $game.Data3) -ne $recipe.Hash){throw 'Installed data3 checksum mismatch.'}

 $state=[ordered]@{
  Edition=$Edition;InstalledAt=(Get-Date -Format o);GameDir=$game.GameDir;
  Data2Hash=$PayloadHash;Data3Hash=$recipe.Hash;Data3Path=$game.Data3;
  BackupRoot=$backupRoot;SaveBackup=$save.Path;SaveBackupCount=$save.Count;
  PreviousData2Hash=$pre2;PreviousData3Hash=$pre3;RecipeFiles=$recipe.Files
 }
 $state|ConvertTo-Json -Depth 8|Set-Content (Join-Path $game.SourceDir $StateName) -Encoding UTF8

 foreach($old in @('DLTB_STEP1_SEPARATE_PAK_V4_STATE.json','DLTB_V3_GREEN_BALANCED_STATE.json')){
  $p=Join-Path $game.SourceDir $old;if(Test-Path $p){Remove-Item $p -Force}
 }

 @('INSTALL=PASS',"EDITION=$Edition","DATA2_SHA=$PayloadHash","DATA3_SHA=$($recipe.Hash)","SAVE_BACKUPS=$($save.Count)",'','RECIPE AUDIT:',$recipe.Audit) |
  Set-Content (Join-Path $PSScriptRoot 'LAST_INSTALL_AUDIT.txt') -Encoding UTF8

 ShowStatus 'POST-INSTALL DETECTOR'
 Write-Host ''
 Write-Host 'ONE-CLICK INSTALL = PASS'
 Write-Host 'Langsung launch game: cek no DLC Disabled + F corpse, lalu main.'
}catch{
 $msg=$_.Exception.Message
 if($game){
  try{
   if($wrote3){
    if($backup3 -and(Test-Path $backup3)){Copy-Item $backup3 $game.Data3 -Force}else{if(Test-Path $game.Data3){Remove-Item $game.Data3 -Force}}
   }
   if($wrote2){
    if($backup2 -and(Test-Path $backup2)){Copy-Item $backup2 $game.Data2 -Force}else{if(Test-Path $game.Data2){Remove-Item $game.Data2 -Force}}
   }
  }catch{}
 }
 @('INSTALL=FAIL',"ERROR=$msg","STACK=$($_.ScriptStackTrace)")|Set-Content (Join-Path $PSScriptRoot 'LAST_INSTALL_AUDIT.txt') -Encoding UTF8
 Write-Host '';Write-Host 'ONE-CLICK INSTALL STOP / FAIL-SAFE';Write-Host $msg
 if($game){try{ShowStatus 'STATUS AFTER FAIL/ROLLBACK'|Out-Null}catch{}}
 exit 1
}
