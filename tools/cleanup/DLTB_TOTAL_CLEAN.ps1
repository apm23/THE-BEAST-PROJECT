param(
    [ValidateSet('Scan','Delete')]
    [string]$Mode = 'Scan'
)

$ErrorActionPreference = 'Stop'
$AppId = '3008130'
$GameNames = @('Dying Light The Beast','DyingLightTheBeast')

function Is-Admin {$id=[Security.Principal.WindowsIdentity]::GetCurrent();$p=New-Object Security.Principal.WindowsPrincipal($id);return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)}
function Add-UniquePath($List,[string]$Path) {if([string]::IsNullOrWhiteSpace($Path)){return};try{$full=[IO.Path]::GetFullPath($Path)}catch{$full=$Path};if(-not($List|Where-Object{$_ -ieq $full})){$List.Add($full)}}
function Get-SteamRoots {$roots=New-Object System.Collections.Generic.List[string];try{$p=(Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction Stop).SteamPath;if($p){Add-UniquePath $roots $p}}catch{};try{$p=(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam' -ErrorAction Stop).InstallPath;if($p){Add-UniquePath $roots $p}}catch{};foreach($p in @("${env:ProgramFiles(x86)}\Steam","${env:ProgramFiles}\Steam","C:\Steam")){if($p){Add-UniquePath $roots $p}};return $roots|Where-Object{Test-Path -LiteralPath $_}}
function Get-SteamLibraries([string[]]$SteamRoots) {$libs=New-Object System.Collections.Generic.List[string];foreach($root in $SteamRoots){Add-UniquePath $libs $root;$vdf=Join-Path $root 'steamapps\libraryfolders.vdf';if(Test-Path -LiteralPath $vdf){try{$txt=Get-Content -Raw -LiteralPath $vdf;foreach($m in [regex]::Matches($txt,'"path"\s*"([^"]+)"')){$p=$m.Groups[1].Value -replace '\\\\','\';Add-UniquePath $libs $p}}catch{}}};return $libs|Where-Object{Test-Path -LiteralPath $_}}
function Get-Targets {
    $targets=New-Object System.Collections.Generic.List[string]
    $steamRoots=@(Get-SteamRoots);$libraries=@(Get-SteamLibraries $steamRoots)
    foreach($lib in $libraries){foreach($name in $GameNames){Add-UniquePath $targets (Join-Path $lib "steamapps\common\$name")};Add-UniquePath $targets (Join-Path $lib "steamapps\shadercache\$AppId");Add-UniquePath $targets (Join-Path $lib "steamapps\downloading\$AppId");Add-UniquePath $targets (Join-Path $lib "steamapps\compatdata\$AppId");Add-UniquePath $targets (Join-Path $lib "steamapps\appmanifest_$AppId.acf")}
    foreach($root in $steamRoots){$userdata=Join-Path $root 'userdata';if(Test-Path -LiteralPath $userdata){Get-ChildItem -LiteralPath $userdata -Directory -ErrorAction SilentlyContinue|ForEach-Object{Add-UniquePath $targets (Join-Path $_.FullName $AppId)}}}
    if($env:USERPROFILE){Add-UniquePath $targets (Join-Path $env:USERPROFILE 'Documents\dying light the beast');Add-UniquePath $targets (Join-Path $env:USERPROFILE 'Documents\Dying Light The Beast')}
    if($env:LOCALAPPDATA){foreach($root in $steamRoots){$drive=[IO.Path]::GetPathRoot($root);if($drive){$relative=$root.Substring($drive.Length).TrimStart('\');foreach($name in $GameNames){Add-UniquePath $targets (Join-Path $env:LOCALAPPDATA ("VirtualStore\"+$relative+"\steamapps\common\"+$name))}}}}
    return $targets
}
function Write-Report([string]$Name,[string[]]$Lines){$p=Join-Path $PSScriptRoot $Name;$Lines|Set-Content -LiteralPath $p -Encoding UTF8;return $p}

if($Mode -eq 'Delete' -and -not(Is-Admin)){Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"",' -Mode','Delete');exit $LASTEXITCODE}
if(Get-Process -ErrorAction SilentlyContinue|Where-Object{$_.ProcessName -like '*DyingLight*' -or $_.ProcessName -like '*TheBeast*'}){Write-Host 'STOP: game masih berjalan.'; exit 10}
if($Mode -eq 'Delete' -and (Get-Process -Name steam,steamwebhelper -ErrorAction SilentlyContinue)){Write-Host 'STOP: Steam masih berjalan. Steam > Exit dulu.'; exit 11}

$targets=@(Get-Targets);$timestamp=Get-Date -Format 'yyyyMMdd_HHmmss';$scan=@("Generated=$((Get-Date).ToString('o'))","Mode=$Mode","AppID=$AppId","");$found=0
Write-Host '';Write-Host '==============================================================';Write-Host ' DLTB TOTAL CLEAN - TARGET REPORT';Write-Host '=============================================================='
foreach($p in $targets){if(Test-Path -LiteralPath $p){$found++;$item=Get-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue;$type=if($item -and $item.PSIsContainer){'DIR '}else{'FILE'};Write-Host "[FOUND][$type] $p";$scan+="FOUND`t$p"}else{Write-Host "[MISS ]       $p";$scan+="MISS`t$p"}}
$report=Write-Report "DLTB_CLEAN_SCAN_$timestamp.txt" $scan
Write-Host '';Write-Host "Existing targets found: $found";Write-Host "Report: $report"
if($Mode -eq 'Scan'){Write-Host 'SCAN ONLY selesai. Tidak ada file yang dihapus.';exit 0}
Write-Host '';Write-Host 'TOTAL LOCAL RESET akan menghapus save/profile/config lokal AppID 3008130,';Write-Host 'folder game, sisa mod, shader cache, downloading cache, compatdata,';Write-Host 'Documents DLTB, dan appmanifest 3008130.';Write-Host 'Steam Cloud SERVER tidak dihapus oleh script ini.'
$confirm=Read-Host 'Ketik persis DELETE-3008130 untuk lanjut';if($confirm -cne 'DELETE-3008130'){Write-Host 'Dibatalkan.';exit 2}
$deleted=New-Object System.Collections.Generic.List[string];$failed=New-Object System.Collections.Generic.List[string]
foreach($p in $targets){if(-not(Test-Path -LiteralPath $p)){continue};try{$item=Get-Item -LiteralPath $p -Force;if($item.PSIsContainer){Get-ChildItem -LiteralPath $p -Recurse -Force -ErrorAction SilentlyContinue|ForEach-Object{try{$_.Attributes=$_.Attributes -band (-bnot [IO.FileAttributes]::ReadOnly)}catch{}};Remove-Item -LiteralPath $p -Recurse -Force}else{try{$item.Attributes=$item.Attributes -band (-bnot [IO.FileAttributes]::ReadOnly)}catch{};Remove-Item -LiteralPath $p -Force};$deleted.Add($p);Write-Host "[DELETED] $p"}catch{$msg="$p :: $($_.Exception.Message)";$failed.Add($msg);Write-Host "[FAILED ] $msg"}}
$remaining=New-Object System.Collections.Generic.List[string];foreach($p in $targets){if(Test-Path -LiteralPath $p){$remaining.Add($p)}}
$result=@("Generated=$((Get-Date).ToString('o'))","Mode=Delete","AppID=$AppId","","=== DELETED ===")+$deleted+@("","=== FAILED ===")+$failed+@("","=== STILL EXISTS ===")+$remaining;$resultPath=Write-Report "DLTB_CLEAN_RESULT_$timestamp.txt" $result
Write-Host '';Write-Host '==============================================================';Write-Host ' DLTB LOCAL CLEAN FINISHED';Write-Host '==============================================================';Write-Host "Deleted : $($deleted.Count)";Write-Host "Failed  : $($failed.Count)";Write-Host "Remain  : $($remaining.Count)";Write-Host "Log     : $resultPath"
if($failed.Count -gt 0 -or $remaining.Count -gt 0){Write-Host 'BELUM 100% bersih. Kirim DLTB_CLEAN_RESULT_*.txt ke ChatGPT.';exit 20}
Write-Host 'LOCAL CLEAN = PASS';Write-Host 'Cloud DLTB tetap OFF -> reinstall -> launch VANILLA -> buat save baru.';exit 0
