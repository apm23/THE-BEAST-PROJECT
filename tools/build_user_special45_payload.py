#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, io, json, shutil, sys, zlib, zipfile
from pathlib import Path

CANONICAL_DATA2_SHA256 = '190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657'
ZIP_TIMESTAMP = (2026, 9, 22, 23, 31, 20)
PATCH_MAP = {
    'scripts/inventory/inventory_ranged.scr': 'scripts__inventory__inventory_ranged_scr',
    'scripts/inventory/loot/lootpools_ft.loot': 'scripts__inventory__loot__lootpools_ft_loot',
    'scripts/inventory/loot/lootsets_ft.loot': 'scripts__inventory__loot__lootsets_ft_loot',
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_patch(patch_dir: Path, stem: str) -> dict:
    parts = sorted(patch_dir.glob(stem + '.part*.b64'))
    if not parts:
        raise FileNotFoundError(f'Patch parts not found for {stem} in {patch_dir}')
    encoded = ''.join(p.read_text(encoding='ascii').strip() for p in parts)
    raw = zlib.decompress(base64.b64decode(encoded))
    return json.loads(raw.decode('utf-8'))


def apply_patch(base: bytes, spec: dict) -> bytes:
    if sha256(base) != spec['baseline_sha256'] or len(base) != spec['baseline_size']:
        raise RuntimeError(
            f"Baseline mismatch for {spec['path']}: expected {spec['baseline_sha256']} / {spec['baseline_size']} bytes, "
            f"got {sha256(base)} / {len(base)} bytes"
        )
    lines = base.decode('latin1').splitlines(True)
    for op in reversed(spec['operations']):
        insert = op['insert']
        lines[op['i1']:op['i2']] = [insert] if insert else []
    out = ''.join(lines).encode('latin1')
    if sha256(out) != spec['final_sha256'] or len(out) != spec['final_size']:
        raise RuntimeError(f"Final patched file verification failed: {spec['path']}")
    return out


def write_canonical_pak(files: dict[str, bytes], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(path, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = bio.getvalue()
    if sha256(data) != CANONICAL_DATA2_SHA256:
        raise RuntimeError(
            f'Canonical data2 hash mismatch: expected {CANONICAL_DATA2_SHA256}, got {sha256(data)}'
        )
    out_path.write_bytes(data)


def main() -> int:
    here = Path(__file__).resolve()
    repo = here.parents[1]
    ap = argparse.ArgumentParser(description='Rebuild exact USER HIGH LOOT SPECIAL45 data2 from verified local 1.71E baseline.')
    ap.add_argument('--baseline', type=Path, default=repo / 'local_baseline' / '1.71E')
    ap.add_argument('--patch-dir', type=Path, default=repo / 'patches' / 'runtime' / 'USER_HIGH_LOOT_SPECIAL45_1.71E')
    ap.add_argument('--output', type=Path, default=repo / 'local_build' / 'USER_HIGH_LOOT_SPECIAL45' / 'data2_payload.pak')
    ap.add_argument('--prepare-switcher', action='store_true', help='Also copy verified payload to tools/runtime_switcher/data2_payload.pak (gitignored).')
    args = ap.parse_args()

    files: dict[str, bytes] = {}
    for path, stem in PATCH_MAP.items():
        base_path = args.baseline / Path(path)
        if not base_path.exists():
            raise FileNotFoundError(f'Missing baseline file: {base_path}. Run tools/extract_targeted_baseline_1.71E.ps1 first.')
        spec = load_patch(args.patch_dir, stem)
        if spec['path'] != path:
            raise RuntimeError(f'Patch path mismatch: {stem}')
        files[path] = apply_patch(base_path.read_bytes(), spec)
        print(f'PATCH PASS: {path} -> {spec["final_sha256"]}')

    write_canonical_pak(files, args.output)
    print(f'DATA2 PASS: {args.output}')
    print(f'SHA256={CANONICAL_DATA2_SHA256}')

    if args.prepare_switcher:
        dst = repo / 'tools' / 'runtime_switcher' / 'data2_payload.pak'
        shutil.copy2(args.output, dst)
        if sha256(dst.read_bytes()) != CANONICAL_DATA2_SHA256:
            raise RuntimeError('Switcher payload copy verification failed.')
        print(f'SWITCHER READY: {dst}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f'BUILD FAIL: {e}', file=sys.stderr)
        raise
