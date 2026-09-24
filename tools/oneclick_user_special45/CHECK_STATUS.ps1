. "$PSScriptRoot\TBP_COMMON.ps1"
try{ShowStatus 'DLTB ONE-CLICK MOD STATUS'|Out-Null}catch{Write-Host 'STATUS FAIL';Write-Host $_.Exception.Message;exit 1}
