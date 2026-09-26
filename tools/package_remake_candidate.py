#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    build = repo / 'local_build' / 'REMAKE_PROVEN45_SINGLEPLAYER_CORE'
    pak = build / 'data2_payload.pak'
    manifest = build / 'BUILD_MANIFEST.json'
    if not pak.exists() or not manifest.exists():
        raise FileNotFoundError('Final candidate or BUILD_MANIFEST.json missing. Do not package a partial build.')

    m = json.loads(manifest.read_text(encoding='utf-8'))
    if m.get('profile') != 'REMAKE_PROVEN45_SINGLEPLAYER_CORE':
        raise RuntimeError('Unexpected build profile; refusing package.')
    if m.get('foundation_sha256') != '190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657':
        raise RuntimeError('Candidate does not declare canonical SPECIAL45 foundation.')
    if m.get('sense_included') is not False or m.get('coop_included') is not False:
        raise RuntimeError('Sense/CO-OP must remain deferred in this package.')

    status = 'RUNTIME_GREEN' if m.get('runtime_status') == 'RUNTIME_GREEN' else 'CANDIDATE_NOT_RUNTIME_GREEN'
    payload_hash = sha256_file(pak)
    if payload_hash != m.get('candidate_data2_sha256'):
        raise RuntimeError('Build manifest data2 hash mismatch.')

    outdir = repo / 'local_build' / 'REMAKE_PROVEN45_PACKAGE'
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    package_manifest = {
        'profile': 'REMAKE_PROVEN45_SINGLEPLAYER_CORE',
        'runtime_target': '1.71PE',
        'runtime_status': status,
        'data2_sha256': payload_hash,
        'source_manifest': m,
        'warnings': [
            'Sense is not included.',
            'CO-OP is not included.',
            'This is a runtime-test candidate until the committed test matrix passes in game.'
        ]
    }
    (outdir / 'PACKAGE_MANIFEST.json').write_text(json.dumps(package_manifest, indent=2), encoding='utf-8')
    shutil.copy2(pak, outdir / 'data2_payload.pak')
    shutil.copy2(repo / 'config' / 'remake_singleplayer_test_matrix.json', outdir / 'TEST_MATRIX.json')
    shutil.copy2(repo / 'tools' / 'runtime_test_gate.py', outdir / 'runtime_test_gate.py')
    shutil.copy2(repo / 'tools' / 'finalize_runtime_green.py', outdir / 'finalize_runtime_green.py')

    ps = r'''param(
  [ValidateSet('Install','Status','Rollback')][string]$Action='Status',
  [string]$GameDir=''
)
$ErrorActionPreference='Stop'
$ExpectedHash='__HASH__'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload=Join-Path $Root 'data2_payload.pak'
$State=Join-Path $Root '_INSTALL_STATE.json'
if(-not $GameDir){$GameDir="${env:ProgramFiles(x86)}\Steam\steamapps\common\Dying Light The Beast"}
$GameDir=[IO.Path]::GetFullPath($GameDir).TrimEnd('\')
$Source=Join-Path $GameDir 'ph_ft\source'
$Dest=Join-Path $Source 'data2.pak'
function H([string]$p){ if(!(Test-Path $p)){return $null}; return (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Closed {
  $open=@(Get-Process -ErrorAction SilentlyContinue | Where-Object { try { $_.Path -and ([IO.Path]::GetFullPath($_.Path).StartsWith($GameDir,[StringComparison]::OrdinalIgnoreCase)) } catch { $false } })
  if($open.Count -gt 0){ throw 'DLTB masih berjalan. Tutup game dulu sebelum install/rollback.' }
}
function Show-Status {
  Write-Host "GAME=$GameDir"
  Write-Host "SOURCE=$Source"
  Write-Host "PAYLOAD_HASH=$(H $Payload)"
  Write-Host "INSTALLED_HASH=$(H $Dest)"
  Write-Host "EXPECTED=$ExpectedHash"
  Write-Host "STATE_PRESENT=$(Test-Path $State)"
}
if($Action -eq 'Status'){Show-Status; exit 0}
if(!(Test-Path $Source)){throw "Folder game tidak ditemukan: $Source"}
if(!(Test-Path $Payload)){throw "Payload tidak ditemukan: $Payload"}
if((H $Payload) -ne $ExpectedHash){throw 'Payload hash mismatch. Stop.'}
Require-Closed
if($Action -eq 'Install'){
  if(Test-Path $State){throw 'Install state sudah ada. Rollback dulu atau pindahkan paket ke folder baru.'}
  $stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
  $backupDir=Join-Path $GameDir "ph_ft\_THE_BEAST_PROJECT_BACKUPS\REMAKE_$stamp"
  New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
  $hadData2=Test-Path $Dest
  $backup=$null
  if($hadData2){
    $backup=Join-Path $backupDir 'data2_before.pak'
    Copy-Item -LiteralPath $Dest -Destination $backup -Force
    if((H $backup) -ne (H $Dest)){throw 'Backup hash verification failed.'}
  }
  $st=[ordered]@{game_dir=$GameDir;dest=$Dest;had_data2=$hadData2;backup=$backup;before_hash=(H $Dest);installed_hash=$ExpectedHash;installed=(Get-Date -Format o)}
  $st|ConvertTo-Json|Set-Content -LiteralPath $State -Encoding UTF8
  Copy-Item -LiteralPath $Payload -Destination $Dest -Force
  if((H $Dest) -ne $ExpectedHash){throw 'Installed data2 hash verification failed.'}
  Write-Host 'INSTALL PASS - REMAKE candidate installed.'
  Write-Host "BACKUP=$backupDir"
  Show-Status
  exit 0
}
if($Action -eq 'Rollback'){
  if(!(Test-Path $State)){throw 'Tidak ada _INSTALL_STATE.json untuk rollback paket ini.'}
  $st=Get-Content -Raw -LiteralPath $State|ConvertFrom-Json
  if([IO.Path]::GetFullPath([string]$st.game_dir).TrimEnd('\') -ne $GameDir){throw 'GameDir berbeda dari install state.'}
  $cur=H $Dest
  if($cur -ne [string]$st.installed_hash){throw "Installed data2 berubah sejak install ($cur). Stop agar tidak menimpa mod lain."}
  if([bool]$st.had_data2){
    if(!(Test-Path ([string]$st.backup))){throw 'Backup sebelumnya hilang.'}
    Copy-Item -LiteralPath ([string]$st.backup) -Destination $Dest -Force
    if((H $Dest) -ne [string]$st.before_hash){throw 'Rollback hash verification failed.'}
  } else {
    Remove-Item -LiteralPath $Dest -Force
  }
  Remove-Item -LiteralPath $State -Force
  Write-Host 'ROLLBACK PASS - state sebelum candidate dipulihkan.'
  Show-Status
  exit 0
}
''' .replace('__HASH__', payload_hash)
    (outdir / 'REMAKE_INSTALLER.ps1').write_text(ps, encoding='utf-8')

    launchers = {
        '1_INSTALL_CANDIDATE.cmd': '@echo off\r\ncd /d "%~dp0"\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REMAKE_INSTALLER.ps1" -Action Install %*\r\npause\r\n',
        '2_CHECK_STATUS.cmd': '@echo off\r\ncd /d "%~dp0"\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REMAKE_INSTALLER.ps1" -Action Status %*\r\npause\r\n',
        '3_ROLLBACK_CANDIDATE.cmd': '@echo off\r\ncd /d "%~dp0"\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REMAKE_INSTALLER.ps1" -Action Rollback %*\r\npause\r\n',
        '4_TEST_GATE.cmd': '@echo off\r\ncd /d "%~dp0"\r\nif "%~1"=="" goto help\r\npython "%~dp0runtime_test_gate.py" %* --root "%~dp0"\r\npause\r\nexit /b %ERRORLEVEL%\r\n:help\r\necho Examples:\r\necho   4_TEST_GATE.cmd init\r\necho   4_TEST_GATE.cmd pass T01 --note "boot normal"\r\necho   4_TEST_GATE.cmd fail T03 --note "corpse F missing"\r\necho   4_TEST_GATE.cmd status\r\necho   4_TEST_GATE.cmd promote\r\npause\r\n',
        '5_FINALIZE_RUNTIME_GREEN.cmd': '@echo off\r\ncd /d "%~dp0"\r\npython "%~dp0finalize_runtime_green.py"\r\nset ERR=%ERRORLEVEL%\r\necho.\r\nif "%ERR%"=="0" (echo RUNTIME GREEN CERTIFICATE CREATED) else (echo FINALIZE BLOCKED - TEST GATE/HASH NOT VALID)\r\npause\r\nexit /b %ERR%\r\n',
    }
    for name, text in launchers.items():
        (outdir / name).write_text(text, encoding='utf-8')

    readme = f'''DLTB REMAKE PROVEN45 - 1.71PE SINGLEPLAYER CORE\n\nSTATUS: {status}\nDATA2 SHA256: {payload_hash}\n\nIncluded:\n- canonical SPECIAL45 loot foundation\n- native rarity route through Exotic\n- human corpse project loot route inherited from SPECIAL45/G1 lineage\n- special infected high-tier/Exotic route\n- Night Sovereign powerful outfit\n- inventory 34 / 34 / 68 / 42\n- material/consumable/throwable stack target 99,999\n- proven weapon drop/share/dismantle definition normalization\n\nDeferred: Sense and CO-OP.\n\nRun 1_INSTALL_CANDIDATE.cmd with the game closed.\nUse 4_TEST_GATE.cmd to record T01-T15 and then run: 4_TEST_GATE.cmd promote\nOnly after promote succeeds, run 5_FINALIZE_RUNTIME_GREEN.cmd.\nThe finalizer rechecks all T01-T15, hard-fail history, SPECIAL45 declaration and exact data2 hash before creating RUNTIME_GREEN_CERTIFICATE.json.\nUse 3_ROLLBACK_CANDIDATE.cmd if any hard gate fails.\n'''
    (outdir / 'README_FIRST.txt').write_text(readme, encoding='utf-8')

    zip_path = repo / 'local_build' / 'DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip'
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(outdir.iterdir()):
            z.write(p, p.name)

    print(json.dumps({
        'package': str(zip_path),
        'package_sha256': sha256_file(zip_path),
        'data2_sha256': payload_hash,
        'runtime_status': status
    }, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
