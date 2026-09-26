#!/usr/bin/env python3
from __future__ import annotations
import base64, json, zlib
from pathlib import Path

PATCH_MAP = {
    'inventory_ranged':'scripts__inventory__inventory_ranged_scr',
    'lootpools':'scripts__inventory__loot__lootpools_ft_loot',
    'lootsets':'scripts__inventory__loot__lootsets_ft_loot',
}

def main() -> int:
    repo=Path(__file__).resolve().parents[1]
    root=repo/'patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E'
    bad=[]
    for label,stem in PATCH_MAP.items():
        parts=sorted(root.glob(stem+'.part*.b64'))
        print(f'{label}: parts={[p.name for p in parts]}')
        try:
            enc=''.join(p.read_text(encoding='ascii').strip() for p in parts)
            print(f'{label}: b64_chars={len(enc)} mod4={len(enc)%4}')
            raw=base64.b64decode(enc, validate=True)
            print(f'{label}: decoded={len(raw)} head={raw[:8].hex()}')
            dec=zlib.decompress(raw)
            obj=json.loads(dec.decode('utf-8'))
            print(f'{label}: PASS path={obj.get("path")} operations={len(obj.get("operations",[]))}')
        except Exception as e:
            bad.append((label,repr(e)))
            print(f'{label}: FAIL {e!r}')
    if bad:
        print('BAD_ASSETS='+json.dumps(bad))
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
