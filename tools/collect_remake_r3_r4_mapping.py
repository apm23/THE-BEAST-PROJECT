#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

TARGETS = [
    "scripts/inventory/inventory.scr",
    "scripts/inventory/inventorystuff.scr",
    "scripts/inventory/inventory_special.scr",
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/gameplay_item_sets.scr",
]

TOKENS = [
    "Outfit",
    "outfit",
    "Equipment",
    "Consumable",
    "Weapon",
    "Ammo",
    "Stack",
    "MaxStack",
    "Inventory",
    "Slots",
    "Capacity",
]


def snippets(text: str, token: str, radius: int = 4) -> list[dict]:
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if token.lower() in line.lower():
            a = max(0, i - radius)
            b = min(len(lines), i + radius + 1)
            out.append({
                "line": i + 1,
                "context": "\n".join(f"{j+1}: {lines[j]}" for j in range(a, b)),
            })
    return out


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = repo / "local_baseline" / "1.71E"
    outdir = repo / "local_build" / "REMAKE_PROVEN45" / "mapping"
    outdir.mkdir(parents=True, exist_ok=True)

    report = {"targets": {}}
    for rel in TARGETS:
        path = base / rel
        if not path.exists():
            raise FileNotFoundError(f"Missing baseline file: {path}")
        text = path.read_text(encoding="latin1")
        hits = {}
        for token in TOKENS:
            found = snippets(text, token)
            if found:
                hits[token] = found
        report["targets"][rel] = hits

    json_path = outdir / "R3_R4_MAPPING.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    txt_path = outdir / "R3_R4_MAPPING.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write("REMAKE PROVEN45 R3/R4 MAPPING - OUTFIT + INVENTORY/STACK\n\n")
        for rel, hits in report["targets"].items():
            f.write(f"===== {rel} =====\n")
            if not hits:
                f.write("(no target tokens found)\n\n")
                continue
            for token, entries in hits.items():
                f.write(f"--- {token} ---\n")
                for entry in entries:
                    f.write(entry["context"] + "\n\n")

    print(f"JSON={json_path}")
    print(f"TEXT={txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
