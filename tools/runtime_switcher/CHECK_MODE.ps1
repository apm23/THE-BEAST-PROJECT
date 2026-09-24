. "$PSScriptRoot\MODE_SWITCH_COMMON.ps1"
try{
 $r=PrintModeStatus 'DLTB USER MOD MODE DETECTOR'
 Write-Host ''
 switch($r.Info.Mode){
  'NORMAL_SOURCE' {Write-Host 'READY: mode normal/proven aktif.'}
  'COOP_MULTIMOD' {Write-Host 'READY: mode CO-OP MultiMod aktif.'}
  'OUR_MOD_DISABLED' {Write-Host 'INFO: mod kita sedang disabled/bersih.'}
  'MIXED_BOTH_LOCATIONS' {Write-Host 'WARNING: mod ada di source DAN MultiMod. Jangan launch sebelum dibereskan.'}
  default {Write-Host 'WARNING: partial/legacy/unknown. Jangan hapus manual; gunakan switcher atau kirim screenshot.'}
 }
}catch{Write-Host 'CHECK MODE FAIL';Write-Host $_.Exception.Message;exit 1}
