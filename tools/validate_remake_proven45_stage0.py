#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import build_user_special45_payload as special45

REQUIRED_MAPPING_FILES = [
    "enums/item_color.def",
    "scripts/inventory/inventory_gen.scr",
    "scripts/inventory/inventory_weapondefintions_ft.scr",
    "scripts/inventory/itemaffixes.scr",
    "scripts/inventory/loot/color_sets.loot",
    "scripts/inventory/loot/lootpools_ft.loot",
    "scripts/inventory/loot/lootsets_ft.loot",
    "scripts/inventory/loot/weaponprobpresets.scr",
    "scripts/inventory/loot/weaponscolorpresets.scr",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    here = Path(__file__).resolve()
    repo = here.parents[1]
    baseline = repo / "local_baseline" / "1.71E"
    manifest_path = repo / "config" / "baseline_1.71E_manifest.json"
    feature_path = repo / "config" / "remake_proven45_features.json"
    plan_path = repo / "config" / "remake_proven45_patch_plan.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    features = json.loads(feature_path.read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    manifest_by_path = {entry["path"]: entry for entry in manifest["files"]}

    if features["global_loot_policy"] != "immutable_proven45_foundation_no_new_global_root_override":
        raise RuntimeError("Remake policy drift: PROVEN45 is no longer marked immutable")
    if plan["base_payload_sha256"] != special45.CANONICAL_DATA2_SHA256:
        raise RuntimeError("Patch-plan base hash does not match canonical SPECIAL45")

    missing = []
    mismatched = []
    for rel in REQUIRED_MAPPING_FILES:
        entry = manifest_by_path.get(rel)
        if not entry:
            raise RuntimeError(f"Required mapping file is absent from captured manifest: {rel}")
        path = baseline / rel
        if not path.exists():
            missing.append(rel)
            continue
        data = path.read_bytes()
        actual = sha256(data)
        if actual != entry["sha256"] or len(data) != entry["size"]:
            mismatched.append({
                "path": rel,
                "expected_sha256": entry["sha256"],
                "actual_sha256": actual,
                "expected_size": entry["size"],
                "actual_size": len(data),
            })

    status = {
        "profile": "REMAKE_PROVEN45_STAGE0",
        "canonical_special45_sha256": special45.CANONICAL_DATA2_SHA256,
        "required_mapping_files": REQUIRED_MAPPING_FILES,
        "missing": missing,
        "mismatched": mismatched,
        "ready_for_patch_authoring": not missing and not mismatched,
        "note": "This validator never edits the canonical SPECIAL45 payload or any local game file."
    }

    out = repo / "local_build" / "REMAKE_PROVEN45" / "STAGE0_STATUS.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))

    if missing:
        print("\nRun tools/extract_targeted_baseline_1.71E.ps1 to regenerate the owned local 1.71E baseline.")
        return 2
    if mismatched:
        print("\nBaseline mismatch. Stop: do not author or build remake patches against this install.")
        return 3

    print("\nSTAGE0 PASS: exact 1.71E mapping inputs are present; PROVEN45 remains the immutable base.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
