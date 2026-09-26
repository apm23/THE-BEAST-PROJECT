#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CRITICAL = {
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/loot/lootpools_ft.loot",
    "scripts/inventory/loot/lootsets_ft.loot",
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
    old_manifest = repo / "config" / "baseline_1.71E_manifest.json"
    new_base = repo / "local_baseline" / "1.71PE"
    outdir = repo / "local_build" / "COMPAT_1.71PE_VS_1.71E"
    outdir.mkdir(parents=True, exist_ok=True)

    if not old_manifest.exists():
        raise FileNotFoundError(old_manifest)
    if not new_base.exists():
        raise FileNotFoundError(
            f"Missing extracted 1.71PE baseline: {new_base}. Extract target files there first."
        )

    manifest = json.loads(old_manifest.read_text(encoding="utf-8"))
    rows = []
    identical = changed = missing = 0

    for entry in manifest["files"]:
        rel = entry["path"]
        p = new_base / rel
        row = {
            "path": rel,
            "critical": rel in CRITICAL,
            "old_sha256": entry["sha256"],
            "old_size": entry["size"],
        }
        if not p.exists():
            row["status"] = "MISSING"
            missing += 1
        else:
            new_hash = sha256_file(p)
            new_size = p.stat().st_size
            row["new_sha256"] = new_hash
            row["new_size"] = new_size
            if new_hash == entry["sha256"] and new_size == entry["size"]:
                row["status"] = "IDENTICAL"
                identical += 1
            else:
                row["status"] = "CHANGED"
                changed += 1
        rows.append(row)

    critical_changed = [r for r in rows if r["critical"] and r["status"] != "IDENTICAL"]
    verdict = "COMPATIBLE_FOR_EXISTING_PATCHES" if not critical_changed and missing == 0 else "NEW_BASELINE_REQUIRED"

    report = {
        "old_baseline": "1.71E",
        "new_baseline": "1.71PE",
        "verdict": verdict,
        "counts": {"identical": identical, "changed": changed, "missing": missing},
        "critical_non_identical": critical_changed,
        "files": rows,
    }

    (outdir / "compatibility.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (outdir / "compatibility.txt").open("w", encoding="utf-8") as f:
        f.write(f"VERDICT: {verdict}\n")
        f.write(f"IDENTICAL={identical} CHANGED={changed} MISSING={missing}\n\n")
        if critical_changed:
            f.write("CRITICAL NON-IDENTICAL:\n")
            for r in critical_changed:
                f.write(f"- {r['status']}: {r['path']}\n")
        else:
            f.write("All critical patch inputs are byte-identical to 1.71E.\n")

    print(json.dumps({
        "verdict": verdict,
        "identical": identical,
        "changed": changed,
        "missing": missing,
        "critical_non_identical": len(critical_changed),
        "report": str(outdir / "compatibility.txt"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
