#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import zipfile
from pathlib import Path

BASELINE_DEFAULT_SHA256 = "757e2f7a606eae5dce5b2f7d045b5184bc32daabcf52a5cd369bed682476e88f"
CANONICAL_SPECIAL45_SHA256 = "190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657"
EXPECTED_GLOBAL_ROOT_V1_SHA256 = "32c129265ef9f9e2eb889946f91cff7119316e110c34180bc0d4cbbe60a54b7b"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

DEFAULT_PATH = "scripts/inventory/loot/default.loot"
OLD_POOL_PATH = "scripts/inventory/loot/lootpools_ft.loot"
OLD_SET_PATH = "scripts/inventory/loot/lootsets_ft.loot"
GLOBAL_POOL_PATH = "scripts/inventory/loot/tbp_lootpools_global_v1.loot"
GLOBAL_SET_PATH = "scripts/inventory/loot/tbp_lootsets_global_v1.loot"

OLD_DEFAULT_IMPORT = b'import "lootpools_ft.loot"'
NEW_DEFAULT_IMPORT = b'import "tbp_lootpools_global_v1.loot"'
OLD_POOL_IMPORT = b'import "lootsets_ft.loot"'
NEW_POOL_IMPORT = b'import "tbp_lootsets_global_v1.loot"'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_pak(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path, "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Input PAK CRC failure at {bad}")
        return {n.replace("\\", "/"): z.read(n) for n in z.namelist()}


def write_pak(files: dict[str, bytes], order: list[str], out_path: Path) -> bytes:
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in order:
            info = zipfile.ZipInfo(path, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = bio.getvalue()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return data


def main() -> int:
    here = Path(__file__).resolve()
    repo = here.parents[1]

    ap = argparse.ArgumentParser(
        description=(
            "Build experimental SPECIAL45 GLOBAL LOOT ROOT V1. "
            "This does not change LootedObject contents; it moves the loot import root into data2 "
            "and binds it to project-owned child filenames."
        )
    )
    ap.add_argument(
        "--baseline",
        type=Path,
        default=repo / "local_baseline" / "1.71E",
        help="Verified extracted 1.71E baseline root.",
    )
    ap.add_argument(
        "--special45",
        type=Path,
        default=repo / "local_build" / "USER_HIGH_LOOT_SPECIAL45" / "data2_payload.pak",
        help="Exact canonical SPECIAL45 payload.",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=repo / "local_build" / "EXPERIMENTAL_GLOBAL_LOOT_ROOT_V1" / "data2_payload.pak",
    )
    args = ap.parse_args()

    default_path = args.baseline / Path(DEFAULT_PATH)
    if not default_path.exists():
        raise FileNotFoundError(f"Missing baseline root: {default_path}")
    default_bytes = default_path.read_bytes()
    if sha256(default_bytes) != BASELINE_DEFAULT_SHA256:
        raise RuntimeError(
            f"default.loot baseline mismatch: expected {BASELINE_DEFAULT_SHA256}, got {sha256(default_bytes)}"
        )

    if not args.special45.exists():
        raise FileNotFoundError(
            f"Missing canonical SPECIAL45 payload: {args.special45}. "
            "Run tools/build_user_special45_payload.py first."
        )
    special45_bytes = args.special45.read_bytes()
    if sha256(special45_bytes) != CANONICAL_SPECIAL45_SHA256:
        raise RuntimeError(
            f"SPECIAL45 input mismatch: expected {CANONICAL_SPECIAL45_SHA256}, got {sha256(special45_bytes)}"
        )

    src = read_pak(args.special45)
    expected_input_paths = {
        "scripts/inventory/inventory_ranged.scr",
        OLD_POOL_PATH,
        OLD_SET_PATH,
    }
    if set(src) != expected_input_paths:
        raise RuntimeError(f"Unexpected SPECIAL45 member set: {sorted(src)}")

    if default_bytes.count(OLD_DEFAULT_IMPORT) != 1:
        raise RuntimeError("default.loot import anchor count is not exactly 1.")
    root = default_bytes.replace(OLD_DEFAULT_IMPORT, NEW_DEFAULT_IMPORT)

    pool = src[OLD_POOL_PATH]
    if pool.count(OLD_POOL_IMPORT) != 1:
        raise RuntimeError("lootpools_ft.loot import anchor count is not exactly 1.")
    global_pool = pool.replace(OLD_POOL_IMPORT, NEW_POOL_IMPORT)
    global_sets = src[OLD_SET_PATH]

    if global_pool.replace(NEW_POOL_IMPORT, OLD_POOL_IMPORT) != pool:
        raise RuntimeError("Global pool changed outside the import binding.")
    if root.replace(NEW_DEFAULT_IMPORT, OLD_DEFAULT_IMPORT) != default_bytes:
        raise RuntimeError("Root default.loot changed outside the import binding.")

    root_text = root.decode("utf-8-sig")
    for name in ("default", "default_hard", "default_nightmare"):
        marker = f"sub {name}()"
        start = root_text.find(marker)
        if start < 0:
            raise RuntimeError(f"Missing root function {name}().")
        brace = root_text.find("{", start)
        end = root_text.find("}", brace)
        if brace < 0 or end < 0 or "use Loot_FT();" not in root_text[brace:end]:
            raise RuntimeError(f"{name}() no longer calls Loot_FT().")

    files = {
        "scripts/inventory/inventory_ranged.scr": src["scripts/inventory/inventory_ranged.scr"],
        DEFAULT_PATH: root,
        GLOBAL_POOL_PATH: global_pool,
        GLOBAL_SET_PATH: global_sets,
    }
    order = [
        "scripts/inventory/inventory_ranged.scr",
        DEFAULT_PATH,
        GLOBAL_POOL_PATH,
        GLOBAL_SET_PATH,
    ]

    out = write_pak(files, order, args.output)
    got = sha256(out)
    if got != EXPECTED_GLOBAL_ROOT_V1_SHA256:
        raise RuntimeError(
            f"GLOBAL ROOT V1 output mismatch: expected {EXPECTED_GLOBAL_ROOT_V1_SHA256}, got {got}"
        )

    print("GLOBAL LOOT ROOT V1 BUILD PASS")
    print(f"INPUT_SPECIAL45={CANONICAL_SPECIAL45_SHA256}")
    print(f"OUTPUT={args.output}")
    print(f"SHA256={got}")
    print("LOOTEDOBJECT_CONTENT=UNCHANGED")
    print("ROOT_BINDING=default.loot -> tbp_lootpools_global_v1.loot -> tbp_lootsets_global_v1.loot")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"BUILD FAIL: {exc}", file=sys.stderr)
        raise
