#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

import build_user_special45_payload as special45

PROFILE = "USER_SPECIAL45_BITER_RESOURCE_PARITY"
POOL_PATH = "scripts/inventory/loot/lootpools_ft.loot"
SETS_PATH = "scripts/inventory/loot/lootsets_ft.loot"
COMMON_ANCHOR = "sub Biter_CommonResources(float weight = 1.0, int min_amount = 1, int max_amount = 1, float prob = 1.0)"
RESOURCES_ANCHOR = "sub Biter_Resources(float weight = 1.0, int min_amount = 1, int max_amount = 1, float prob = 1.0)"

# Main loose/pickup crafting resources. Keep firearm-specific scrap excluded.
# Every listed resource gets the same internal selection weight as Scrap.
RESOURCE_ITEMS = [
    ("Craft_Scrap", 40, 55),
    ("Craft_Rags", 33, 50),
    ("Craft_Wiring", 33, 50),
    ("Craft_Container", 33, 50),
    ("Craft_Resin", 33, 50),
    ("Craft_Blades", 33, 50),
    ("Craft_Weights", 33, 50),
    ("Craft_Feathers", 33, 50),
    ("Craft_Leather", 33, 50),
    ("Craft_Electrical_Parts", 33, 50),
    ("Craft_Pigments", 33, 50),
    ("Craft_Battery", 33, 50),
    ("Craft_Cleaning_Supplies", 33, 50),
    ("Craft_Oxidizer", 33, 50),
    ("Craft_Alcohol", 33, 50),
    ("Craft_Fuel_Can_FT", 33, 50),
]
RESOURCE_WEIGHT = 5.0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def newline_style(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def find_braced_block(text: str, anchor: str) -> tuple[int, int, str]:
    start = text.find(anchor)
    if start < 0:
        raise RuntimeError(f"Anchor not found: {anchor}")
    if text.find(anchor, start + len(anchor)) >= 0:
        raise RuntimeError(f"Anchor is not unique: {anchor}")

    brace = text.find("{", start + len(anchor))
    if brace < 0:
        raise RuntimeError(f"Opening brace not found for: {anchor}")

    depth = 0
    in_string = False
    escape = False
    line_comment = False
    block_comment = False
    i = brace

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if line_comment:
            if ch == "\n":
                line_comment = False
            i += 1
            continue

        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == "/" and nxt == "/":
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start, i + 1, text[start:i + 1]
        i += 1

    raise RuntimeError(f"Unclosed block: {anchor}")


def resource_lines(nl: str, indent: str) -> str:
    return "".join(
        f'{indent}        ItemCount("{name}", {minimum}, {maximum}, {RESOURCE_WEIGHT:.1f});{nl}'
        for name, minimum, maximum in RESOURCE_ITEMS
    )


def make_common_block(nl: str, indent: str) -> str:
    return (
        COMMON_ANCHOR + nl
        + indent + "{" + nl
        + indent + "    Set(Other, weight, min_amount, max_amount, prob)" + nl
        + indent + "    {" + nl
        + indent + '        ItemCount("Cash_Cash", 2, 5, 3.0);' + nl
        + nl
        + indent + "        // THE-BEAST-PROJECT: SPECIAL45 Biter resource parity candidate." + nl
        + indent + "        // Craft-resource chance is equalized to Scrap without changing Biter corpse routing." + nl
        + resource_lines(nl, indent)
        + indent + "    }" + nl
        + indent + "}"
    )


def make_resources_block(nl: str, indent: str) -> str:
    return (
        RESOURCES_ANCHOR + nl
        + indent + "{" + nl
        + indent + "    Set(Other, weight, min_amount, max_amount, prob)" + nl
        + indent + "    {" + nl
        + indent + "        // THE-BEAST-PROJECT: SPECIAL45 Biter resource parity candidate." + nl
        + indent + "        // Same craft-resource set and weight as Biter_CommonResources." + nl
        + resource_lines(nl, indent)
        + nl
        + indent + "        // Preserve existing low-weight plant extras." + nl
        + indent + '        Item("Plant_Poppy", 0.5);' + nl
        + indent + '        Item("Plant_Cordyceps", 0.5);' + nl
        + indent + "    }" + nl
        + indent + "}"
    )


def replace_named_block(text: str, anchor: str, replacement_factory) -> str:
    start, end, _ = find_braced_block(text, anchor)
    line_start = text.rfind("\n", 0, start) + 1
    indent = text[line_start:start]
    nl = newline_style(text)
    replacement = replacement_factory(nl, indent)
    return text[:start] + replacement + text[end:]


def patch_biter_subpools(text: str) -> str:
    before_braces = (text.count("{"), text.count("}"))

    text = replace_named_block(text, COMMON_ANCHOR, make_common_block)
    text = replace_named_block(text, RESOURCES_ANCHOR, make_resources_block)

    after_braces = (text.count("{"), text.count("}"))
    if before_braces != after_braces:
        raise RuntimeError(f"Brace count changed: {before_braces} -> {after_braces}")

    return text


def verify_frozen_biter_routes(lootpools_text: str) -> None:
    # Guardrails live in lootpools_ft.loot; we never mutate this file.
    biter_anchor = 'LootedObject("Biter")'
    _, _, biter_block = find_braced_block(lootpools_text, biter_anchor)
    expected_routes = [
        "use Biter_CommonResources (weight = 20.0, min_amount = 0, max_amount = 2);",
        "use Biter_Resources (weight = 10.0, min_amount = 0, max_amount = 1);",
        "use Biter_CommonResources (weight = 23.0, min_amount = 0, max_amount = 1);",
        "use Biter_Resources (weight = 11.0, min_amount = 0, max_amount = 1);",
    ]
    for route in expected_routes:
        if route not in biter_block:
            raise RuntimeError(f"Frozen Biter route guard failed: {route}")


def reconstruct_special45(baseline: Path, patch_dir: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path, stem in special45.PATCH_MAP.items():
        base_path = baseline / Path(path)
        if not base_path.exists():
            raise FileNotFoundError(
                f"Missing baseline file: {base_path}. "
                "Run tools/extract_targeted_baseline_1.71E.ps1 first."
            )
        spec = special45.load_patch(patch_dir, stem)
        if spec["path"] != path:
            raise RuntimeError(f"Patch path mismatch: {stem}")
        files[path] = special45.apply_patch(base_path.read_bytes(), spec)

    # Prove the starting point is the exact canonical SPECIAL45 file set.
    canonical_bio = io.BytesIO()
    with zipfile.ZipFile(canonical_bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(path, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    canonical_hash = sha256(canonical_bio.getvalue())
    if canonical_hash != special45.CANONICAL_DATA2_SHA256:
        raise RuntimeError(
            "SPECIAL45 reconstruction mismatch before candidate patch: "
            f"expected {special45.CANONICAL_DATA2_SHA256}, got {canonical_hash}"
        )
    return files


def write_candidate_pak(files: dict[str, bytes], out_path: Path) -> bytes:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(path, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = bio.getvalue()
    out_path.write_bytes(data)

    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Candidate PAK integrity failed: {bad}")
    return data


def main() -> int:
    here = Path(__file__).resolve()
    repo = here.parents[1]

    ap = argparse.ArgumentParser(
        description=(
            "Build a SPECIAL45-derived DLTB 1.71E candidate where ordinary Biter "
            "crafting resources have the same internal weight as Scrap."
        )
    )
    ap.add_argument(
        "--baseline",
        type=Path,
        default=repo / "local_baseline" / "1.71E",
    )
    ap.add_argument(
        "--patch-dir",
        type=Path,
        default=repo / "patches" / "runtime" / "USER_HIGH_LOOT_SPECIAL45_1.71E",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=repo / "local_build" / PROFILE / "data2_payload.pak",
    )
    args = ap.parse_args()

    files = reconstruct_special45(args.baseline, args.patch_dir)

    original_hashes = {path: sha256(data) for path, data in files.items()}

    # lootpools_ft.loot contains LootedObject("Biter") routing and stays byte-identical.
    verify_frozen_biter_routes(files[POOL_PATH].decode("latin1"))

    # lootsets_ft.loot contains the two resource sub-pools we intentionally rebalance.
    original_sets = files[SETS_PATH]
    patched_text = patch_biter_subpools(original_sets.decode("latin1"))
    files[SETS_PATH] = patched_text.encode("latin1")

    # Only lootsets_ft.loot may differ from canonical SPECIAL45.
    for path, data in files.items():
        if path == SETS_PATH:
            if data == original_sets:
                raise RuntimeError("Candidate patch made no change to lootsets_ft.loot")
        elif sha256(data) != original_hashes[path]:
            raise RuntimeError(f"Unexpected canonical file change: {path}")

    candidate_data = write_candidate_pak(files, args.output)
    candidate_hash = sha256(candidate_data)

    manifest = {
        "profile": PROFILE,
        "runtime_status": "CANDIDATE_NOT_RUNTIME_GREEN",
        "game": "Dying Light: The Beast 1.71E",
        "derived_from_data2_sha256": special45.CANONICAL_DATA2_SHA256,
        "candidate_data2_sha256": candidate_hash,
        "changed_file": SETS_PATH,
        "verified_unchanged_route_file": POOL_PATH,
        "frozen_outer_biter_routing": True,
        "resource_weight": RESOURCE_WEIGHT,
        "resource_quantities": {
            "Craft_Scrap": [40, 55],
            "non_scrap": [33, 50],
        },
        "resources": [name for name, _, _ in RESOURCE_ITEMS],
        "notes": [
            "Both Biter_CommonResources and Biter_Resources use the same craft-resource set.",
            "Each listed craft resource has weight 5.0, equal to Scrap.",
            "Electrical Parts and Pigments are added as normal pickup-resource types.",
            "Firearm-specific scrap remains excluded.",
            "Cash remains only in Biter_CommonResources.",
            "Plant_Poppy and Plant_Cordyceps remain low-weight extras only in Biter_Resources.",
            "lootpools_ft.loot remains byte-identical to canonical SPECIAL45.",
            "No LootedObject(Biter) route/topology edit is performed.",
            "Canonical SPECIAL45 source and hash remain unchanged for rollback.",
        ],
        "file_sha256": {path: sha256(data) for path, data in files.items()},
    }

    manifest_path = args.output.parent / "BUILD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(json.dumps(manifest, indent=2))
    print(f"PAK={args.output}")
    print(f"MANIFEST={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
