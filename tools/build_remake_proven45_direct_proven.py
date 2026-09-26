#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path

import build_remake_proven45_recovered_candidate as recovered

EXPECTED = recovered.special45.CANONICAL_DATA2_SHA256


def direct_special45_files(repo: Path, runtime: Path) -> dict[str, bytes]:
    raw = os.environ.get('TBP_SPECIAL45_PROVEN_PAK', '').strip()
    if not raw:
        raise RuntimeError('TBP_SPECIAL45_PROVEN_PAK is not set')
    pak = Path(raw)
    if not pak.exists():
        raise FileNotFoundError(pak)
    data = pak.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != EXPECTED:
        raise RuntimeError(f'Proven SPECIAL45 hash mismatch: expected {EXPECTED}, got {got}')

    files: dict[str, bytes] = {}
    with zipfile.ZipFile(pak, 'r') as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'Proven SPECIAL45 PAK integrity failure: {bad}')
        for rel in recovered.special45.PATCH_MAP:
            try:
                files[rel] = z.read(rel)
            except KeyError as e:
                raise RuntimeError(f'Proven SPECIAL45 PAK missing member: {rel}') from e

    # Recreate the 3-member canonical archive deterministically and prove identity.
    bio = recovered.io.BytesIO()
    with recovered.zipfile.ZipFile(bio, 'w', recovered.zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(files):
            info = recovered.zipfile.ZipInfo(rel, date_time=recovered.special45.ZIP_TIMESTAMP)
            info.compress_type = recovered.zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[rel], compress_type=recovered.zipfile.ZIP_DEFLATED, compresslevel=9)
    rebuilt = hashlib.sha256(bio.getvalue()).hexdigest()
    if rebuilt != EXPECTED:
        raise RuntimeError(f'Direct proven reconstruction hash mismatch: expected {EXPECTED}, got {rebuilt}')

    print(f'DIRECT PROVEN SPECIAL45 PASS: {pak}')
    print(f'SHA256={got}')
    return files


recovered.build_special45_files = direct_special45_files

if __name__ == '__main__':
    raise SystemExit(recovered.main())
