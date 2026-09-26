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

CORE_SPECIAL45_INPUTS = [
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/loot/lootpools_ft.loot",
    "scripts/inventory/loot/lootsets_ft.loot",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    baseline = repo / "local_baseline" / "CURRENT_RUNTIME"
    manifest_path = repo / "config" / "baseline_1.71E_manifest.json"
    feature_path = repo / "config" / "remake_proven45_features.json"
    plan_path = repo / "config" / "remake_proven45_patch_plan.json"
    runtime_report_path = repo / "local_build" / "CURRENT_RUNTIME_PREP" / "CURRENT_RUNTIME.json"

    for required in (manifest_path, feature_path, plan_path, runtime_report_path):
        if not required.exists():
            raise FileNotFoundError(required)
    if not baseline.exists():
        raise FileNotFoundError("CURRENT_RUNTIME baseline missing. Run RUN_1.71PE_CORE_PREP.cmd first.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    features = json.loads(feature_path.read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    runtime = json.loads(runtime_report_path.read_text(encoding="utf-8"))
    manifest_by_path = {entry["path"]: entry for entry in manifest["files"]}

    if features["global_loot_policy"] != "immutable_proven45_foundation_no_new_global_root_override":
        raise RuntimeError("Remake policy drift: PROVEN45 is no longer marked immutable")
    if plan["base_payload_sha256"] != special45.CANONICAL_DATA2_SHA256:
        raise RuntimeError("Patch-plan base hash does not match canonical SPECIAL45")
    if runtime.get("current_runtime") != "1.71PE":
        raise RuntimeError(f"Unexpected CURRENT_RUNTIME: {runtime.get('current_runtime')!r}")
    if runtime.get("mode") != "SPECIAL45_CORE_BYTE_COMPATIBLE":
        raise RuntimeError("CURRENT_RUNTIME is not SPECIAL45-core byte-compatible; dedicated 1.71PE port required.")

    missing = []
    for rel in REQUIRED_MAPPING_FILES:
        if not (baseline / rel).exists():
            missing.append(rel)

    core_mismatched = []
    for rel in CORE_SPECIAL45_INPUTS:
        entry = manifest_by_path.get(rel)
        if not entry:
            raise RuntimeError(f"Core file absent from captured manifest: {rel}")
        p = baseline / rel
        if not p.exists():
            if rel not in missing:
                missing.append(rel)
            continue
        data = p.read_bytes()
        actual = sha256(data)
        if actual != entry["sha256"] or len(data) != entry["size"]:
            core_mismatched.append({
                "path": rel,
                "expected_sha256": entry["sha256"],
                "actual_sha256": actual,
                "expected_size": entry["size"],
                "actual_size": len(data),
            })

    status = {
        "profile": "REMAKE_PROVEN45_STAGE0",
        "runtime_target": "1.71PE",
        "current_runtime_mode": runtime.get("mode"),
        "canonical_special45_sha256": special45.CANONICAL_DATA2_SHA256,
        "required_mapping_files": REQUIRED_MAPPING_FILES,
        "missing": missing,
        "core_mismatched": core_mismatched,
        "ready_for_patch_authoring": not missing and not core_mismatched,
        "note": "Only the three canonical SPECIAL45 core inputs must remain byte-identical; changed mapping-only files are intentionally remapped from CURRENT_RUNTIME."
    }

    out = repo / "local_build" / "REMAKE_PROVEN45" / "STAGE0_STATUS.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))

    if missing:
        print("\nCURRENT_RUNTIME is incomplete. Re-run tools/RUN_1.71PE_CORE_PREP.cmd.")
        return 2
    if core_mismatched:
        print("\nCore mismatch. Stop: dedicated 1.71PE SPECIAL45 port required before gameplay authoring.")
        return 3

    print("\nSTAGE0 PASS: 1.71PE CURRENT_RUNTIME is ready; canonical PROVEN45 core remains guarded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
