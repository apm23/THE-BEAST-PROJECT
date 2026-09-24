. "$PSScriptRoot\TBP_COMMON.ps1"

$SwitchEdition='USER_HIGH_LOOT_SPECIAL45'
$SwitchPayloadHash='190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'
$SwitchPayload=Join-Path $PSScriptRoot 'data2_payload.pak'
$SwitchStateName='DLTB_TBP_MODE_STATE.json'

function GetModePaths($g){
 $ph=Join-Path $g.GameDir 'ph_ft'
 return [PSCustomObject]@{
  PhFt=$ph
  SourceDir=$g.SourceDir
  Source2=$g.Data2
  Source3=$g.Data3
  MultiDir=(Join-Path $ph 'MultiMod')
  Multi2=(Join-Path $ph 'MultiMod\data2.pak')
  Multi3=(Join-Path $ph 'MultiMod\data3.pak')
  CustomPakIni=(Join-Path $ph 'work\bin\x64\CustomPak.ini')
  State=(Join-Path $ph $SwitchStateName)
  OldOneClickState=(Join-Path $g.SourceDir $StateName)
  OldV4State=(Join-Path $g.SourceDir 'DLTB_STEP1_SEPARATE_PAK_V4_STATE.json')
 }
}
function ReadJsonSafe([string]$p){
 if(-not(Test-Path $p)){return $null}
 try{return (Get-Content -Raw $p|ConvertFrom-Json)}catch{return $null}
}
function ReadSwitchState($g){$p=GetModePaths $g; return ReadJsonSafe $p.State}
function IsKnownData2([string]$h){
 if($h -eq 'ABSENT'){return $true}
 if($h -eq $SwitchPayloadHash){return $true}
 foreach($k in $KnownData2.Keys){if($KnownData2[$k] -eq $h){return $true}}
 return $false
}
function IsKnownRecipe($g,[string]$h){
 if($h -eq 'ABSENT'){return $true}
 if($h -eq $KnownOldRecipeHash){return $true}
 $p=GetModePaths $g
 $s=ReadJsonSafe $p.State;if($s -and $s.Data3Hash -eq $h){return $true}
 $o=ReadJsonSafe $p.OldOneClickState;if($o -and $o.Data3Hash -eq $h){return $true}
 $v=ReadJsonSafe $p.OldV4State;if($v -and $v.RecipePakHash -eq $h){return $true}
 return $false
}
function GetLoaderStatus($g){
 $p=GetModePaths $g;$dir=Test-Path $p.MultiDir;$ini=Test-Path $p.CustomPakIni
 return [PSCustomObject]@{MultiModDir=$dir;CustomPakIni=$ini;Confirmed=($dir -and $ini)}
}
function Data2Label([string]$h){
 if($h -eq 'ABSENT'){return 'ABSENT'}
 if($h -eq $SwitchPayloadHash){return 'USER_SPECIAL45_CURRENT'}
 foreach($k in $KnownData2.Keys){if($KnownData2[$k] -eq $h){return $k}}
 return 'UNKNOWN'
}
function RecipeLabel($g,[string]$h){if($h -eq 'ABSENT'){return 'ABSENT'};if(IsKnownRecipe $g $h){return 'OUR_RECIPE/KNOWN'};return 'UNKNOWN'}
function GetModeInfo($g){
 $p=GetModePaths $g;$s2=HashOrAbsent $p.Source2;$s3=HashOrAbsent $p.Source3;$m2=HashOrAbsent $p.Multi2;$m3=HashOrAbsent $p.Multi3;$st=ReadSwitchState $g
 $mode='PARTIAL/LEGACY/UNKNOWN'
 $sourcePair=($s2 -eq $SwitchPayloadHash -and (IsKnownRecipe $g $s3) -and $s3 -ne 'ABSENT')
 $multiPair=($m2 -eq $SwitchPayloadHash -and (IsKnownRecipe $g $m3) -and $m3 -ne 'ABSENT')
 if($sourcePair -and $m2 -eq 'ABSENT' -and $m3 -eq 'ABSENT'){$mode='NORMAL_SOURCE'}
 elseif($multiPair -and $s2 -eq 'ABSENT' -and $s3 -eq 'ABSENT'){$mode='COOP_MULTIMOD'}
 elseif($s2 -eq 'ABSENT' -and $s3 -eq 'ABSENT' -and $m2 -eq 'ABSENT' -and $m3 -eq 'ABSENT'){$mode='OUR_MOD_DISABLED'}
 elseif(($s2 -ne 'ABSENT' -or $s3 -ne 'ABSENT') -and ($m2 -ne 'ABSENT' -or $m3 -ne 'ABSENT')){$mode='MIXED_BOTH_LOCATIONS'}
 return [PSCustomObject]@{Mode=$mode;Paths=$p;State=$st;Source2=$s2;Source3=$s3;Multi2=$m2;Multi3=$m3;Loader=(GetLoaderStatus $g)}
}
function PrintModeStatus([string]$Title){
 $g=FindGame;$i=GetModeInfo $g
 Write-Host '';Write-Host '================================================================';Write-Host " $Title";Write-Host '================================================================'
 Write-Host "GAME=$($g.GameDir)";Write-Host "MODE=$($i.Mode)";Write-Host ''
 Write-Host "SOURCE data2=$($i.Source2) [$((Data2Label $i.Source2))]";Write-Host "SOURCE data3=$($i.Source3) [$((RecipeLabel $g $i.Source3))]"
 Write-Host "MULTIMOD data2=$($i.Multi2) [$((Data2Label $i.Multi2))]";Write-Host "MULTIMOD data3=$($i.Multi3) [$((RecipeLabel $g $i.Multi3))]";Write-Host ''
 Write-Host "MultiMod folder=$($i.Loader.MultiModDir)";Write-Host "CustomPak.ini=$($i.Loader.CustomPakIni)"
 if($i.Loader.Confirmed){Write-Host 'MULTIMOD_LOADER=DETECTED'}else{Write-Host 'MULTIMOD_LOADER=NOT CONFIRMED'}
 if($i.State){Write-Host "SWITCH_STATE=ADA | StoredMode=$($i.State.Mode)"}else{Write-Host 'SWITCH_STATE=tidak ada'}
 return [PSCustomObject]@{Game=$g;Info=$i}
}
function AssertPayload(){if(-not(Test-Path $SwitchPayload)){throw 'data2_payload.pak paket switcher tidak ada.'};$h=(Get-FileHash $SwitchPayload -Algorithm SHA256).Hash.ToLowerInvariant();if($h -ne $SwitchPayloadHash){throw "Payload corrupt. Expected=$SwitchPayloadHash Actual=$h"}}
function AssertOurOrAbsent($g,[string]$path,[string]$type){$h=HashOrAbsent $path;if($type -eq 'data2'){if(-not(IsKnownData2 $h)){throw "STOP AMAN: $path adalah data2 UNKNOWN. SHA=$h"}}else{if(-not(IsKnownRecipe $g $h)){throw "STOP AMAN: $path adalah data3 UNKNOWN. SHA=$h"}};return $h}
function NewBackupRoot($g,[string]$tag){$p=GetModePaths $g;$stamp=Get-Date -Format 'yyyyMMdd_HHmmss';$root=Join-Path $p.PhFt ("_THE_BEAST_PROJECT_BACKUPS\MODE_SWITCH_"+$tag+"_"+$stamp);New-Item -ItemType Directory -Force -Path $root|Out-Null;return $root}
function Snapshot([string]$path,[string]$backupRoot,[string]$name){$exists=Test-Path $path;$b=$null;if($exists){$b=Join-Path $backupRoot $name;Copy-Item $path $b -Force};return [PSCustomObject]@{Path=$path;Existed=$exists;Backup=$b}}
function RestoreSnapshot($s){if($s.Existed){if(-not(Test-Path $s.Backup)){throw "Backup hilang: $($s.Backup)"};Copy-Item $s.Backup $s.Path -Force}else{if(Test-Path $s.Path){Remove-Item $s.Path -Force}}}
function InstallVerified([string]$src,[string]$dst,[string]$hash,[string]$backupRoot,[string]$backupName){
 New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent)|Out-Null;$side=Join-Path (Split-Path $dst -Parent) ('.tbp.'+[guid]::NewGuid().ToString('N')+'.tmp');Copy-Item $src $side -Force
 $sh=(Get-FileHash $side -Algorithm SHA256).Hash.ToLowerInvariant();if($sh -ne $hash){Remove-Item $side -Force;throw "Side checksum mismatch untuk $dst"}
 if(Test-Path $dst){$rb=Join-Path $backupRoot $backupName;[IO.File]::Replace($side,$dst,$rb,$true)}else{Move-Item $side $dst}
 $fh=(Get-FileHash $dst -Algorithm SHA256).Hash.ToLowerInvariant();if($fh -ne $hash){throw "Installed checksum mismatch untuk $dst"}
}
function WriteSwitchState($g,[string]$mode,[string]$d2hash,[string]$d3hash,[string]$d2path,[string]$d3path,[string]$backupRoot,$save){$p=GetModePaths $g;$o=[ordered]@{Edition=$SwitchEdition;Mode=$mode;UpdatedAt=(Get-Date -Format o);GameDir=$g.GameDir;Data2Hash=$d2hash;Data3Hash=$d3hash;Data2Path=$d2path;Data3Path=$d3path;BackupRoot=$backupRoot;SaveBackup=$save.Path;SaveBackupCount=$save.Count};$o|ConvertTo-Json -Depth 8|Set-Content $p.State -Encoding UTF8}
function RemoveLegacyStates($g){$p=GetModePaths $g;foreach($x in @($p.OldOneClickState,$p.OldV4State)){if(Test-Path $x){Remove-Item $x -Force}}}
