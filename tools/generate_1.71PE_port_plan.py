#!/usr/bin/env python3
from __future__ import annotations

import difflib
import json
from pathlib import Path

CORE = [
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/loot/lootpools_ft.loot",
    "scripts/inventory/loot/lootsets_ft.loot",
]

MAPPING = [
    "scripts/inventory/inventory_gen.scr",
    "scripts/inventory/inventory_weapondefintions_ft.scr",
    "scripts/inventory/itemaffixes.scr",
    "scripts/inventory/loot/color_sets.loot",
    "scripts/inventory/loot/weaponprobpresets.scr",
    "scripts/inventory/loot/weaponscolorpresets.scr",
    "scripts/inventory/loot/weaponsetpresets.scr",
]


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    old = repo / "local_baseline" / "1.71E"
    new = repo / "local_baseline" / "1.71PE"
    compat_path = repo / "local_build/COMPAT_1.71PE_VS_1.71E/compatibility.json"
    out = repo / "local_build/PORT_1.71PE_PLAN"
    diffs = out / "diffs"
    diffs.mkdir(parents=True, exist_ok=True)

    if not compat_path.exists():
        raise FileNotFoundError("Run CHECK_1.71PE_COMPATIBILITY.cmd first")
    compat = json.loads(compat_path.read_text(encoding="utf-8"))
    by_path = {x["path"]: x for x in compat["files"]}

    rows = []
    for rel in CORE + MAPPING:
        status = by_path.get(rel, {}).get("status", "UNKNOWN")
        row = {
            "path": rel,
            "class": "CORE_SPECIAL45" if rel in CORE else "MAPPING",
            "compat_status": status,
            "action": "REUSE_1.71E_SEMANTICS" if status == "IDENTICAL" else "REVIEW_AND_PORT",
        }
        if status == "CHANGED":
            a = old / rel
            b = new / rel
            if a.exists() and b.exists():
                a_lines = a.read_text(encoding="latin1").splitlines(True)
                b_lines = b.read_text(encoding="latin1").splitlines(True)
                delta = "".join(difflib.unified_diff(
                    a_lines, b_lines,
                    fromfile=f"1.71E/{rel}", tofile=f"1.71PE/{rel}", n=5,
                ))
                safe_name = rel.replace("/", "__") + ".diff"
                (diffs / safe_name).write_text(delta, encoding="utf-8")
                row["diff_file"] = str(Path("diffs") / safe_name)
                row["diff_lines"] = len(delta.splitlines())
        rows.append(row)

    core_changed = [r for r in rows if r["class"] == "CORE_SPECIAL45" and r["compat_status"] != "IDENTICAL"]
    mode = "DIRECT_SPECIAL45_REUSE" if not core_changed else "DEDICATED_1.71PE_PORT_REQUIRED"

    report = {
        "source_behavioral_baseline": "USER_HIGH_LOOT_SPECIAL45_1.71E",
        "target_runtime": "1.71PE",
        "mode": mode,
        "rules": [
            "PROVEN45 behavior is the reference, not a license to copy stale files blindly.",
            "LootedObject outer topology remains frozen.",
            "Prefer porting numeric/sub-pool semantics onto 1.71PE when a core file changed.",
            "Do not touch inventory versioning or stash_dlc in this phase.",
            "player_variables/common_skills may change only through the committed narrow inventory/stack allowlist recovered from the proven lineage; unrelated parameters and Sense must remain untouched.",
            "Sense and CO-OP remain deferred.",
            "No gameplay build becomes RUNTIME_PROVEN until F corpse, attack, inventory, scene transition, and save reload pass in game."
        ],
        "files": rows,
    }
    (out / "PORT_PLAN.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (out / "PORT_PLAN.txt").open("w", encoding="utf-8") as f:
        f.write(f"MODE={mode}\nTARGET=1.71PE\nBASELINE=USER_HIGH_LOOT_SPECIAL45_1.71E\n\n")
        for r in rows:
            f.write(f"[{r['class']}] {r['compat_status']} -> {r['action']} :: {r['path']}\n")
            if "diff_file" in r:
                f.write(f"  diff={r['diff_file']} lines={r['diff_lines']}\n")

    print(f"MODE={mode}")
    print(f"CORE_CHANGED={len(core_changed)}")
    print(f"REPORT={out / 'PORT_PLAN.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
