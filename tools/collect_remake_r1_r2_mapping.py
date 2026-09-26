#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TARGETS = [
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

TOKENS = [
    "Exotic",
    "Platinum",
    "Color_Exotic",
    "Color_Platinum",
    "Weapons_Random_Exotic",
    "Weapons_Random_Platinum",
    "Human_1h",
    "Human_2h",
    "Human_Ranged",
    "Enemy_Lottery_Weapons",
]


def snippets(text: str, token: str, radius: int = 3) -> list[dict]:
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


def extract_looted_object(text: str, name: str) -> str | None:
    anchor = f'LootedObject("{name}")'
    start = text.find(anchor)
    if start < 0:
        return None
    brace = text.find("{", start)
    if brace < 0:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(brace, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = repo / "local_baseline" / "CURRENT_RUNTIME"
    runtime_report = repo / "local_build" / "CURRENT_RUNTIME_PREP" / "CURRENT_RUNTIME.json"
    outdir = repo / "local_build" / "REMAKE_PROVEN45" / "mapping"
    outdir.mkdir(parents=True, exist_ok=True)

    if not runtime_report.exists():
        raise FileNotFoundError("Run PREPARE_CURRENT_RUNTIME.cmd first")
    runtime = json.loads(runtime_report.read_text(encoding="utf-8"))

    report = {
        "current_runtime": runtime.get("current_runtime", "unknown"),
        "behavioral_baseline": "USER_HIGH_LOOT_SPECIAL45",
        "source_root": str(base),
        "targets": {},
        "human_looted_objects": {},
    }
    for rel in TARGETS:
        path = base / rel
        if not path.exists():
            raise FileNotFoundError(f"Missing current-runtime file: {path}")
        text = path.read_text(encoding="latin1")
        hits = {}
        for token in TOKENS:
            found = snippets(text, token)
            if found:
                hits[token] = found
        report["targets"][rel] = hits

    loot_path = base / "scripts/inventory/loot/lootpools_ft.loot"
    loot_text = loot_path.read_text(encoding="latin1")
    names = sorted(set(re.findall(r'LootedObject\("(Human_[^"]+)"\)', loot_text)))
    for name in names:
        block = extract_looted_object(loot_text, name)
        if block is not None:
            report["human_looted_objects"][name] = block

    json_path = outdir / "R1_R2_MAPPING.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    txt_path = outdir / "R1_R2_MAPPING.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(f"REMAKE PROVEN45 R1/R2 MAPPING - runtime {report['current_runtime']}\n\n")
        for rel, hits in report["targets"].items():
            f.write(f"===== {rel} =====\n")
            if not hits:
                f.write("(no target tokens found)\n\n")
                continue
            for token, entries in hits.items():
                f.write(f"--- {token} ---\n")
                for entry in entries:
                    f.write(entry["context"] + "\n\n")
        f.write("===== HUMAN LootedObject blocks =====\n")
        for name, block in report["human_looted_objects"].items():
            f.write(f"\n--- {name} ---\n{block}\n")

    print(f"RUNTIME={report['current_runtime']}")
    print(f"JSON={json_path}")
    print(f"TEXT={txt_path}")
    print(f"HumanLootedObjects={len(report['human_looted_objects'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
