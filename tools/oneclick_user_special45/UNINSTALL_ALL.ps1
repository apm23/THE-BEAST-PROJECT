. "$PSScriptRoot\TBP_COMMON.ps1"
if(-not(IsAdmin)){
 Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$PSCommandPath`"")
 exit $LASTEXITCODE
}
try{
 if(Get-Process -Name 'DyingLightGame_TheBeast_x64_rwdi' -ErrorAction SilentlyContinue){throw 'Tutup game dulu.'}
 $g=ShowStatus 'PRE-UNINSTALL DETECTOR'
 $state=ReadState $g
 if(-not $state){throw 'State one-click tidak ada. Biar aman uninstaller tidak akan menebak file.'}

 $h2=HashOrAbsent $g.Data2;$h3=HashOrAbsent $g.Data3
 if($h2 -ne $state.Data2Hash){throw "STOP AMAN: data2 berubah/beda. Current=$h2 Expected=$($state.Data2Hash)"}
 if($h3 -ne $state.Data3Hash){throw "STOP AMAN: data3 berubah/beda. Current=$h3 Expected=$($state.Data3Hash)"}

 Remove-Item $g.Data3 -Force
 Remove-Item $g.Data2 -Force
 Remove-Item (Join-Path $g.SourceDir $StateName) -Force

 ShowStatus 'POST-UNINSTALL DETECTOR'
 if((HashOrAbsent $g.Data2) -ne 'ABSENT' -or (HashOrAbsent $g.Data3) -ne 'ABSENT'){throw 'Uninstall verify gagal: data2/data3 belum bersih.'}
 Write-Host ''
 Write-Host 'UNINSTALL ALL = PASS'
 Write-Host 'data2 + data3 paket ini sudah bersih.'
}catch{
 Write-Host '';Write-Host 'UNINSTALL STOP / FAIL-SAFE';Write-Host $_.Exception.Message
 exit 1
}
