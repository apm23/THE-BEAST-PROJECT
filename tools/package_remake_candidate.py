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
    if m.get('runtime_status') == 'RUNTIME_GREEN':
        status = 'RUNTIME_GREEN'
    else:
        status = 'CANDIDATE_NOT_RUNTIME_GREEN'

    outdir = repo / 'local_build' / 'REMAKE_PROVEN45_PACKAGE'
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    package_manifest = {
        'profile': 'REMAKE_PROVEN45_SINGLEPLAYER_CORE',
        'runtime_target': '1.71PE',
        'runtime_status': status,
        'data2_sha256': sha256_file(pak),
        'source_manifest': m,
        'warnings': [
            'Sense is not included.',
            'CO-OP is not included.',
            'Do not label this package runtime-green until the committed test matrix passes in game.'
        ]
    }
    (outdir / 'PACKAGE_MANIFEST.json').write_text(json.dumps(package_manifest, indent=2), encoding='utf-8')
    shutil.copy2(pak, outdir / 'data2_payload.pak')

    install = r'''@echo off
setlocal
set "GAME=%~1"
if "%GAME%"=="" set "GAME=%ProgramFiles(x86)%\Steam\steamapps\common\Dying Light The Beast"
set "DST=%GAME%\ph_ft\source"
if not exist "%DST%" (
  echo ERROR: game source folder not found: %DST%
  exit /b 2
)
if exist "%DST%\data2.pak" copy /y "%DST%\data2.pak" "%DST%\data2.pak.REMAKE_BACKUP" >nul
copy /y "%~dp0data2_payload.pak" "%DST%\data2.pak" >nul || exit /b 3
echo INSTALLED REMAKE candidate to %DST%\data2.pak
'''
    rollback = r'''@echo off
setlocal
set "GAME=%~1"
if "%GAME%"=="" set "GAME=%ProgramFiles(x86)%\Steam\steamapps\common\Dying Light The Beast"
set "DST=%GAME%\ph_ft\source"
if exist "%DST%\data2.pak.REMAKE_BACKUP" (
  copy /y "%DST%\data2.pak.REMAKE_BACKUP" "%DST%\data2.pak" >nul
  del /q "%DST%\data2.pak.REMAKE_BACKUP" >nul 2>nul
  echo ROLLBACK restored previous data2.pak
  exit /b 0
)
echo No REMAKE backup found. Current data2.pak was not changed.
'''
    (outdir / '1_INSTALL_CANDIDATE.cmd').write_text(install, encoding='utf-8')
    (outdir / '3_ROLLBACK_CANDIDATE.cmd').write_text(rollback, encoding='utf-8')
    shutil.copy2(repo / 'config' / 'remake_singleplayer_test_matrix.json', outdir / 'TEST_MATRIX.json')

    zip_path = repo / 'local_build' / 'DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip'
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(outdir.iterdir()):
            z.write(p, p.name)

    print(json.dumps({
        'package': str(zip_path),
        'package_sha256': sha256_file(zip_path),
        'data2_sha256': package_manifest['data2_sha256'],
        'runtime_status': status
    }, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
