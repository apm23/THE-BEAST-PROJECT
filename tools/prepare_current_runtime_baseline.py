#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

CORE_SPECIAL45_INPUTS = {
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/loot/lootpools_ft.loot",
    "scripts/inventory/loot/lootsets_ft.loot",
}

MAPPING_INPUTS = {
    "scripts/inventory/inventory_gen.scr",
    "scripts/inventory/inventory_weapondefintions_ft.scr",
    "scripts/inventory/itemaffixes.scr",
    "scripts/inventory/loot/color_sets.loot",
    "scripts/inventory/loot/weaponprobpresets.scr",
    "scripts/inventory/loot/weaponscolorpresets.scr",
    "scripts/inventory/loot/weaponsetpresets.scr",
    "scripts/inventory/inventory_outfits.scr",
    "scripts/inventory/inventory_outfits_ft.scr",
    "scripts/inventory/outfits_visualization.def",
    "scripts/inventory/outfits_visualization_ft.def",
    "scripts/inventory/dismantleparams.scr",
    "scripts/inventory/inventory_charms.scr",
    "scripts/inventory/collectables_ft.scr",
    "scripts/player/player_variables.scr",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    compat_path = repo / "local_build" / "COMPAT_1.71PE_VS_1.71E" / "compatibility.json"
    pe = repo / "local_baseline" / "1.71PE"
    active = repo / "local_baseline" / "CURRENT_RUNTIME"
    outdir = repo / "local_build" / "CURRENT_RUNTIME_PREP"
    outdir.mkdir(parents=True, exist_ok=True)

    if not compat_path.exists():
        raise FileNotFoundError("Run CHECK_1.71PE_COMPATIBILITY.cmd first")
    if not pe.exists():
        raise FileNotFoundError(pe)

    compat = json.loads(compat_path.read_text(encoding="utf-8"))
    by_path = {r["path"]: r for r in compat["files"]}

    core_bad = [p for p in sorted(CORE_SPECIAL45_INPUTS) if by_path.get(p, {}).get("status") != "IDENTICAL"]
    mapping_changed = [
        p for p in sorted(MAPPING_INPUTS)
        if p in by_path and by_path.get(p, {}).get("status") != "IDENTICAL"
    ]

    mode = "SPECIAL45_CORE_BYTE_COMPATIBLE" if not core_bad else "PORT_REQUIRED_BEFORE_GAMEPLAY_BUILD"

    if active.exists():
        shutil.rmtree(active)
    active.mkdir(parents=True, exist_ok=True)

    copied = []
    for src in sorted(p for p in pe.rglob("*") if p.is_file()):
        rel_path = src.relative_to(pe)
        if rel_path.name.startswith("_") and rel_path.suffix.lower() == ".json":
            continue
        dst = active / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append({
            "path": rel_path.as_posix(),
            "sha256": sha256_file(dst),
            "size": dst.stat().st_size,
        })

    mapping_present = sorted(p for p in MAPPING_INPUTS if (active / p).exists())
    mapping_missing_optional = sorted(p for p in MAPPING_INPUTS if not (active / p).exists())

    report = {
        "current_runtime": "1.71PE",
        "behavioral_baseline": "USER_HIGH_LOOT_SPECIAL45",
        "mode": mode,
        "core_special45_inputs": sorted(CORE_SPECIAL45_INPUTS),
        "core_non_identical": core_bad,
        "mapping_inputs_changed_with_historical_comparison": mapping_changed,
        "mapping_inputs_present": mapping_present,
        "mapping_inputs_missing_optional": mapping_missing_optional,
        "active_baseline": str(active),
        "copied_files": len(copied),
        "rules": [
            "Never patch current runtime unless this report says SPECIAL45_CORE_BYTE_COMPATIBLE or a dedicated 1.71PE port has been authored.",
            "Extra current-runtime mapping files are copied locally but do not alter the historical 58-file compatibility contract.",
            "player_variables/stash_dlc/versioning remain mapping-only or forbidden unless separately proven safe.",
            "LootedObject topology stays frozen.",
            "Sense and CO-OP remain deferred for the single-player core phase."
        ]
    }

    (outdir / "CURRENT_RUNTIME.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        f"MODE={mode}",
        "CURRENT_RUNTIME=1.71PE",
        f"CORE_NON_IDENTICAL={len(core_bad)}",
        f"COPIED_FILES={len(copied)}",
        f"MAPPING_PRESENT={len(mapping_present)}",
        f"MAPPING_OPTIONAL_MISSING={len(mapping_missing_optional)}",
        "",
    ]
    if core_bad:
        lines += ["CORE FILES REQUIRING PORT:"] + [f"- {x}" for x in core_bad]
    else:
        lines += ["SPECIAL45 core inputs are byte-compatible."]
    if mapping_missing_optional:
        lines += ["", "OPTIONAL/EXTRA MAPPING FILES NOT PRESENT:"] + [f"- {x}" for x in mapping_missing_optional]
    (outdir / "CURRENT_RUNTIME.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 2 if core_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
