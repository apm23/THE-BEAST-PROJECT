#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path

import build_remake_proven45_recovered_candidate as recovered

EXPECTED = recovered.special45.CANONICAL_DATA2_SHA256
_ORIGINAL_APPLY_CONTEXT_SPEC = recovered.apply_context_spec


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


def direct_apply_context_spec(data: bytes, spec: dict) -> bytes:
    """Exact historical bases may legitimately contain repeated identical contexts.

    Recovered delta generation emitted one op per historical occurrence. For the
    exact captured base we therefore apply exactly one remaining occurrence per
    op and rely on the pinned target SHA as the final authority. If the source is
    not the exact captured base, retain the original strict unique-context logic.
    """
    if recovered.sha256(data) != spec.get('base_sha256'):
        return _ORIGINAL_APPLY_CONTEXT_SPEC(data, spec)

    text = data.decode('latin1')
    for i, op in enumerate(spec['ops'], 1):
        needle = op['before'] + op['old'] + op['after']
        repl = op['before'] + op['new'] + op['after']
        count = text.count(needle)
        if count < 1:
            already = text.count(repl)
            raise RuntimeError(
                f"{spec['path']} exact op#{i}: no remaining old context "
                f"(new-context count={already})"
            )
        text = text.replace(needle, repl, 1)

    out = text.encode('latin1')
    got = recovered.sha256(out)
    expected = spec.get('target_sha256')
    if got != expected:
        raise RuntimeError(
            f"Historical target hash mismatch after exact transplant: {spec['path']} "
            f"expected={expected} got={got}"
        )
    return out


recovered.build_special45_files = direct_special45_files
recovered.apply_context_spec = direct_apply_context_spec

if __name__ == '__main__':
    raise SystemExit(recovered.main())
