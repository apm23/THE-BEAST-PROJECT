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
    manifest_path = repo / "config" / "baseline_1.71E_manifest.json"
    pe = repo / "local_baseline" / "1.71PE"
    active = repo / "local_baseline" / "CURRENT_RUNTIME"
    outdir = repo / "local_build" / "CURRENT_RUNTIME_PREP"
    outdir.mkdir(parents=True, exist_ok=True)

    if not compat_path.exists():
        raise FileNotFoundError("Run CHECK_1.71PE_COMPATIBILITY.cmd first")
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)
    if not pe.exists():
        raise FileNotFoundError(pe)

    compat = json.loads(compat_path.read_text(encoding="utf-8"))
    old = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_path = {r["path"]: r for r in compat["files"]}

    core_bad = [p for p in sorted(CORE_SPECIAL45_INPUTS) if by_path.get(p, {}).get("status") != "IDENTICAL"]
    mapping_changed = [p for p in sorted(MAPPING_INPUTS) if by_path.get(p, {}).get("status") != "IDENTICAL"]

    mode = ""
    if not core_bad:
        mode = "SPECIAL45_CORE_BYTE_COMPATIBLE"
    else:
        mode = "PORT_REQUIRED_BEFORE_GAMEPLAY_BUILD"

    if active.exists():
        shutil.rmtree(active)
    active.mkdir(parents=True, exist_ok=True)

    copied = []
    for entry in old["files"]:
        rel = entry["path"]
        src = pe / rel
        if not src.exists():
            continue
        dst = active / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append({"path": rel, "sha256": sha256_file(dst), "size": dst.stat().st_size})

    report = {
        "current_runtime": "1.71PE",
        "behavioral_baseline": "USER_HIGH_LOOT_SPECIAL45",
        "mode": mode,
        "core_special45_inputs": sorted(CORE_SPECIAL45_INPUTS),
        "core_non_identical": core_bad,
        "mapping_inputs_changed": mapping_changed,
        "active_baseline": str(active),
        "copied_files": len(copied),
        "rules": [
            "Never patch current runtime unless this report says SPECIAL45_CORE_BYTE_COMPATIBLE or a dedicated 1.71PE port has been authored.",
            "Changed mapping-only files require fresh R1/R2/R3/R4 mapping even if the three canonical SPECIAL45 core inputs remain identical.",
            "LootedObject topology stays frozen.",
            "Sense and CO-OP remain deferred for the single-player core phase."
        ]
    }

    (outdir / "CURRENT_RUNTIME.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (outdir / "CURRENT_RUNTIME.txt").write_text(
        f"MODE={mode}\n"
        f"CURRENT_RUNTIME=1.71PE\n"
        f"CORE_NON_IDENTICAL={len(core_bad)}\n"
        f"MAPPING_INPUTS_CHANGED={len(mapping_changed)}\n"
        + ("\nCORE FILES REQUIRING PORT:\n" + "\n".join(f"- {x}" for x in core_bad) + "\n" if core_bad else "\nSPECIAL45 core inputs are byte-compatible.\n")
        + ("\nMAPPING FILES CHANGED:\n" + "\n".join(f"- {x}" for x in mapping_changed) + "\n" if mapping_changed else "\nMapping inputs are also byte-identical.\n"),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    if core_bad:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
