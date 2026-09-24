$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$AppId='3008130'
$StateName='DLTB_TBP_ONECLICK_STATE.json'
$KnownOldRecipeHash='2eed30bc4f9eda3bd72f39c71e9921fadb090d9efdcdca78bfd6224a32704741'
$KnownData2=[ordered]@{
    'CORPSE_SAFE_OLD' = 'dc7dc7970088f7a4f3e7c547c0a6fb7229abaadca8a30f3836491e4624015c75'
    'GREEN_BALANCED_OLD' = 'ecbbbc1ca3725c4507ce6e3f893c5e3438dc882e1a4bd4b69dbff4457812609e'
    'SIBLING_OLD_40PCT' = 'cc207aea957124075b9856d79daacb51607e54f0326db2ccb2abab9c4eecd31c'
    'USER_OLD_40PCT' = '363eb050b075d9bdc3448da145a532541b49e8c48b3608877ec12c0e6f5175ec'
    'SIBLING_REVISED' = '311a75f919c499e71c56c35eb5a96d3827312048f4559ad120e8389f211b64c2'
    'USER_REVISED' = '8757a6e57d88d2d049f38f6db32cfe9eec773f2a35c3b28501d91faeb2717c94'
    'SIBLING_SPECIAL45' = 'ab18b545bffbee00ff8ff8ee1e0a9b241bfb2f5864aa88bedc282dab428e771d'
    'USER_SPECIAL45' = '190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'
}
$RecipeTargets=[ordered]@{
    'Craftplan_Arrows_FT' = 35
    'Craftplan_Arrows_Fire_FT' = 35
    'Craftplan_Arrows_Shock_FT' = 35
    'Craftplan_Bolt_FT' = 35
    'Craftplan_Bolts_Fire_FT' = 35
    'Craftplan_Bolts_Shock_FT' = 35
    'Craftplan_GrenadeLauncher_Ammo_Electric_FT' = 35
    'Craftplan_GrenadeLauncher_Ammo_Explosive_FT' = 35
    'Craftplan_GrenadeLauncher_Ammo_Flashbang_FT' = 35
    'Craftplan_GrenadeLauncher_Ammo_Freeze_FT' = 35
    'Craftplan_GrenadeLauncher_Ammo_Incendiary_FT' = 35
    'Craftplan_SawbladeLauncher_Ammo_FT' = 35
    'Craftplan_Flamethrower_Ammo_FT' = 400
}
$ForbiddenFragments=@('/versioning/','inventory_versioning','inventory_items_version_','stash_dlc','player_variables','/savegame/','entitlement','dlcmanager','dlc_manager')

function IsAdmin {$i=[Security.Principal.WindowsIdentity]::GetCurrent();$p=New-Object Security.Principal.WindowsPrincipal($i);return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)}
function Norm([string]$p){return ($p -replace '\\','/').TrimStart('/')}
function GetSteamRoots {$r=@();try{$p=(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath;if($p){$r+=$p}}catch{};try{$p=(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath;if($p){$r+=$p}}catch{};foreach($p in @("${env:ProgramFiles(x86)}\Steam","${env:ProgramFiles}\Steam","C:\Steam")){if($p -and(Test-Path $p)){$r+=$p}};return @($r|Select-Object -Unique)}
function GetSteamLibraries {$l=@();foreach($r in GetSteamRoots){if(Test-Path $r){$l+=$r};$v=Join-Path $r 'steamapps\libraryfolders.vdf';if(Test-Path $v){try{$t=Get-Content -Raw $v;foreach($m in [regex]::Matches($t,'"path"\s*"([^"]+)"')){$p=$m.Groups[1].Value -replace '\\\\','\';if(Test-Path $p){$l+=$p}}}catch{}}};return @($l|Select-Object -Unique)}
function FindGame {$by=@{};foreach($lib in GetSteamLibraries){$g=Join-Path $lib 'steamapps\common\Dying Light The Beast';$s=Join-Path $g 'ph_ft\source';if(-not(Test-Path (Join-Path $s 'data0.pak'))){continue};try{$key=[IO.Path]::GetFullPath($g).TrimEnd('\').ToLowerInvariant()}catch{$key=$g.TrimEnd('\').ToLowerInvariant()};if($by.ContainsKey($key)){continue};$by[$key]=[PSCustomObject]@{GameDir=$g;SourceDir=$s;Data0=(Join-Path $s 'data0.pak');Data1=(Join-Path $s 'data1.pak');Data2=(Join-Path $s 'data2.pak');Data3=(Join-Path $s 'data3.pak')}};$games=@($by.Values);if($games.Count -eq 0){throw 'Instalasi DLTB tidak ditemukan.'};if($games.Count -gt 1){$msg=($games|ForEach-Object{$_.GameDir}) -join "`r`n";throw "Lebih dari satu instalasi DLTB nyata ditemukan. STOP AMAN.`r`n$msg"};return $games[0]}
function HashOrAbsent([string]$p){if(-not(Test-Path $p)){return 'ABSENT'};return (Get-FileHash $p -Algorithm SHA256).Hash.ToLowerInvariant()}
function LabelData2([string]$h){if($h -eq 'ABSENT'){return 'ABSENT'};foreach($k in $KnownData2.Keys){if($KnownData2[$k] -eq $h){return $k}};return 'UNKNOWN'}
function ReadState($game){$p=Join-Path $game.SourceDir $StateName;if(Test-Path $p){try{return (Get-Content -Raw $p|ConvertFrom-Json)}catch{}};return $null}
function GetOldV4State($game){$p=Join-Path $game.SourceDir 'DLTB_STEP1_SEPARATE_PAK_V4_STATE.json';if(Test-Path $p){try{return (Get-Content -Raw $p|ConvertFrom-Json)}catch{}};return $null}
function ShowStatus([string]$Title){$g=FindGame;$h2=HashOrAbsent $g.Data2;$h3=HashOrAbsent $g.Data3;$state=ReadState $g;$recipeLabel='UNKNOWN';if($h3 -eq 'ABSENT'){$recipeLabel='ABSENT'}elseif($state -and $state.Data3Hash -eq $h3){$recipeLabel='ONECLICK_RECIPE'}else{$v4=GetOldV4State $g;if(($v4 -and $v4.RecipePakHash -eq $h3) -or $h3 -eq $KnownOldRecipeHash){$recipeLabel='OLD_PROVEN_RECIPE'}};Write-Host '';Write-Host '==============================================================';Write-Host " $Title";Write-Host '==============================================================';Write-Host "GAME=$($g.GameDir)";Write-Host "data2.pak=$h2 [$((LabelData2 $h2))]";Write-Host "data3.pak=$h3 [$recipeLabel]";if($state){Write-Host "ONECLICK_STATE=ADA | Edition=$($state.Edition)"}else{Write-Host 'ONECLICK_STATE=tidak ada'};if($h2 -eq 'ABSENT' -and $h3 -eq 'ABSENT'){Write-Host 'OVERALL=CLEAN / NO MOD DATA2+DATA3'}elseif($state -and $state.Data2Hash -eq $h2 -and $state.Data3Hash -eq $h3){Write-Host "OVERALL=INSTALLED OK [$($state.Edition)]"}else{Write-Host 'OVERALL=PARTIAL / LEGACY / UNKNOWN - lihat hash di atas'};return $g}
function ReadEntryText($e){$sr=New-Object IO.StreamReader($e.Open(),[Text.Encoding]::UTF8,$true);try{return $sr.ReadToEnd()}finally{$sr.Dispose()}}
function GetDef([string]$Text,[string]$Id){$needle='Item("'+$Id+'"';$defs=@();$from=0;while($true){$p=$Text.IndexOf($needle,$from,[StringComparison]::Ordinal);if($p -lt 0){break};$from=$p+$needle.Length;$brace=$Text.IndexOf('{',$p);if($brace -lt 0){continue};$semi=$Text.IndexOf(';',$p);if($semi -ge 0 -and $semi -lt $brace){continue};$header=$Text.Substring($p,$brace-$p);if($header -notmatch 'CategoryType_'){continue};$ls=$Text.LastIndexOf("`n",$p);if($ls -lt 0){$ls=0}else{$ls++};$d=0;$end=-1;for($i=$brace;$i -lt $Text.Length;$i++){if($Text[$i] -eq '{'){$d++}elseif($Text[$i] -eq '}'){$d--;if($d -eq 0){$end=$i+1;break}}};if($end -gt 0){$defs += [PSCustomObject]@{Start=$ls;End=$end;Text=$Text.Substring($ls,$end-$ls)}}};return @($defs)}
function Crafted([string]$Block){$m=[regex]::Matches($Block,'CraftedItem\("([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*\);');if($m.Count -ne 1){throw "CraftedItem count=$($m.Count), expected 1."};return [PSCustomObject]@{Output=$m[0].Groups[1].Value;Amount=[int]$m[0].Groups[2].Value;Third=[int]$m[0].Groups[3].Value;Index=$m[0].Index;Length=$m[0].Length}}
function ReqSig([string]$Block){$a=@();foreach($m in [regex]::Matches($Block,'RequiredItem\("([^"]+)"\s*,\s*(\d+)\s*\);')){$a+=($m.Groups[1].Value+'='+$m.Groups[2].Value)};return ($a -join '|')}
function Mask([string]$Block){return [regex]::Replace($Block,'CraftedItem\("([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*\);','CraftedItem("$1", __OUTPUT__, $3);',1)}
function PatchBlock([string]$Block,[int]$NewAmount){$b=Crafted $Block;$req=ReqSig $Block;$rep='CraftedItem("'+$b.Output+'", '+$NewAmount+', '+$b.Third+');';$out=$Block.Substring(0,$b.Index)+$rep+$Block.Substring($b.Index+$b.Length);$a=Crafted $out;if((ReqSig $out) -cne $req){throw 'RequiredItem berubah.'};if($a.Output -cne $b.Output -or $a.Third -ne $b.Third -or $a.Amount -ne $NewAmount){throw 'CraftedItem audit gagal.'};if((Mask $Block) -cne (Mask $out)){throw 'Recipe block berubah di luar output amount.'};return [PSCustomObject]@{Text=$out;Old=$b.Amount;Output=$b.Output;Req=$req}}
function BackupSaves([string]$Root){$dest=Join-Path $Root 'SAVE_BEFORE_ONECLICK';New-Item -ItemType Directory -Force -Path $dest|Out-Null;$n=0;foreach($steam in GetSteamRoots){$ud=Join-Path $steam 'userdata';if(-not(Test-Path $ud)){continue};Get-ChildItem $ud -Directory -ErrorAction SilentlyContinue|ForEach-Object{$src=Join-Path $_.FullName '3008130\remote\out';if(Test-Path $src){Copy-Item $src (Join-Path $dest ('Steam_'+$_.Name+'_out')) -Recurse -Force;$n++}}};return [PSCustomObject]@{Path=$dest;Count=$n}}
function BuildRecipePak($game,[string]$OutPak){
 $z0=$null;$z1=$null
 try{
  $z0=[IO.Compression.ZipFile]::OpenRead($game.Data0);$z1=[IO.Compression.ZipFile]::OpenRead($game.Data1);$effective=@{}
  foreach($pair in @([PSCustomObject]@{Zip=$z0;Label='data0'},[PSCustomObject]@{Zip=$z1;Label='data1'})){foreach($e in $pair.Zip.Entries){if([string]::IsNullOrEmpty($e.Name)){continue};$n=Norm $e.FullName;if($n.StartsWith('scripts/',[StringComparison]::OrdinalIgnoreCase) -and $n.EndsWith('.scr',[StringComparison]::OrdinalIgnoreCase)){$effective[$n]=[PSCustomObject]@{Entry=$e;Archive=$pair.Label}}}}
  $found=@{};$texts=@{}
  foreach($path in ($effective.Keys|Sort-Object)){$text=$null;foreach($id in $RecipeTargets.Keys){if($found.ContainsKey($id)){continue};if($null -eq $text){$text=ReadEntryText $effective[$path].Entry};if($text.IndexOf(('Item("'+$id+'"'),[StringComparison]::Ordinal) -lt 0){continue};$defs=@(GetDef $text $id);if($defs.Count -gt 1){throw "Definisi recipe ambigu: $id pada $path"};if($defs.Count -eq 1){$low=(Norm $path).ToLowerInvariant();foreach($frag in $ForbiddenFragments){if($low.Contains($frag)){throw "Recipe berada di source sensitif: $path"}};if($low -eq 'scripts/inventory/inventory_ranged.scr' -or $low -eq 'scripts/inventory/loot/lootsets_ft.loot' -or $low -eq 'scripts/inventory/loot/lootpools_ft.loot'){throw "Recipe bentrok dengan core data2: $path"};$found[$id]=[PSCustomObject]@{Path=(Norm $path);Archive=$effective[$path].Archive};$texts[(Norm $path)]=$text}}}
  $missing=@($RecipeTargets.Keys|Where-Object{-not $found.ContainsKey($_)});if($missing.Count -gt 0){throw ('Recipe tidak ditemukan: '+($missing -join ', '))}
  $patched=@{};$audit=@()
  foreach($path in ($texts.Keys|Sort-Object)){$original=$texts[$path];$work=$original;$ids=@($RecipeTargets.Keys|Where-Object{$found[$_].Path -eq $path});$ops=@();foreach($id in $ids){$d=@(GetDef $original $id);if($d.Count -ne 1){throw "Definition count bukan 1: $id"};$ops += [PSCustomObject]@{Id=$id;Start=$d[0].Start;End=$d[0].End;Block=$d[0].Text;Amount=[int]$RecipeTargets[$id]}};foreach($op in ($ops|Sort-Object Start -Descending)){$r=PatchBlock $op.Block $op.Amount;$work=$work.Substring(0,$op.Start)+$r.Text+$work.Substring($op.End);$audit += "$($op.Id): $($r.Old) -> $($op.Amount) | $($r.Output) | Required=[$($r.Req)] | $path | $($found[$op.Id].Archive)"};$mo=$original;$mp=$work;$oo=@();$pp=@();foreach($id in $ids){$do=@(GetDef $mo $id);$dp=@(GetDef $mp $id);if($do.Count -ne 1 -or $dp.Count -ne 1){throw "Mask count error: $id"};$oo += [PSCustomObject]@{Start=$do[0].Start;End=$do[0].End;Text=(Mask $do[0].Text)};$pp += [PSCustomObject]@{Start=$dp[0].Start;End=$dp[0].End;Text=(Mask $dp[0].Text)}};foreach($x in ($oo|Sort-Object Start -Descending)){$mo=$mo.Substring(0,$x.Start)+$x.Text+$mo.Substring($x.End)};foreach($x in ($pp|Sort-Object Start -Descending)){$mp=$mp.Substring(0,$x.Start)+$x.Text+$mp.Substring($x.End)};if($mo -cne $mp){throw "Whole-file output-only audit gagal: $path"};$patched[$path]=$work}
  $tmpdir=Join-Path $env:TEMP ('DLTB_ONECLICK_RECIPE_'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Force -Path $tmpdir|Out-Null;foreach($path in $patched.Keys){$o=Join-Path $tmpdir ($path -replace '/','\');New-Item -ItemType Directory -Force -Path (Split-Path $o -Parent)|Out-Null;[IO.File]::WriteAllText($o,$patched[$path],(New-Object Text.UTF8Encoding($false)))};[IO.Compression.ZipFile]::CreateFromDirectory($tmpdir,$OutPak,[IO.Compression.CompressionLevel]::Optimal,$false)
  $v=[IO.Compression.ZipFile]::OpenRead($OutPak);try{$actual=@($v.Entries|Where-Object{-not[string]::IsNullOrEmpty($_.Name)}|ForEach-Object{Norm $_.FullName}|Sort-Object);$expected=@($patched.Keys|Sort-Object);if(($actual -join '|') -cne ($expected -join '|')){throw 'Recipe PAK member audit gagal.'}}finally{$v.Dispose()};return [PSCustomObject]@{Hash=(Get-FileHash $OutPak -Algorithm SHA256).Hash.ToLowerInvariant();Audit=$audit;Files=@($patched.Keys)}
 }finally{if($z0){$z0.Dispose()};if($z1){$z1.Dispose()}}
}
