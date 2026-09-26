#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TARGETS = [
    "scripts/inventory/inventory.scr",
    "scripts/inventory/inventorystuff.scr",
    "scripts/inventory/inventory_special.scr",
    "scripts/inventory/inventory_ranged.scr",
    "scripts/inventory/gameplay_item_sets.scr",
    "scripts/inventory/inventory_outfits.scr",
    "scripts/inventory/inventory_outfits_ft.scr",
    "scripts/inventory/outfits_visualization.def",
    "scripts/inventory/outfits_visualization_ft.def",
    "scripts/inventory/itemaffixes.scr",
    "scripts/inventory/dismantleparams.scr",
    "scripts/inventory/collectables_ft.scr",
    "scripts/player/player_variables.scr",
]

TOKENS = [
    "Vanguard",
    "Outfit",
    "Gear",
    "Armor",
    "Equipment",
    "Consumable",
    "Weapon",
    "Ammo",
    "QuickSlotsCount",
    "AmmoSlotsCount",
    "Storage",
    "Stack",
    "MaxStack",
    "MaxAmmoCountInventoryUpgrade",
    "CanDrop",
    "IsShareable",
    "Dismantle",
    "Infected",
    "Human",
    "Resistance",
    "Stamina",
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


def extract_braced_block(text: str, anchor: str) -> str | None:
    start = text.find(anchor)
    if start < 0:
        return None
    brace = text.find("{", start)
    if brace < 0:
        return None
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
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
        i += 1
    return None


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = repo / "local_baseline" / "CURRENT_RUNTIME"
    runtime_path = repo / "local_build" / "CURRENT_RUNTIME_PREP" / "CURRENT_RUNTIME.json"
    outdir = repo / "local_build" / "REMAKE_PROVEN45" / "mapping"
    outdir.mkdir(parents=True, exist_ok=True)

    if not runtime_path.exists():
        raise FileNotFoundError("Run PREPARE_CURRENT_RUNTIME.cmd first")
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))

    report: dict[str, object] = {
        "current_runtime": runtime.get("current_runtime", "unknown"),
        "policy": {
            "player_variables_mapping_only": True,
            "stash_dlc_forbidden": True,
            "inventory_versioning_forbidden": True,
            "night_sovereign_carrier_strategy": "map native Vanguard outfit items; do not invent/delete live registry entries",
            "inventory_targets": {"equipment": 34, "consumable": 34, "weapon": 68, "ammo": 42},
            "stack_target": 99999
        },
        "targets": {},
        "missing_targets": [],
        "vanguard_item_blocks": {}
    }

    texts: dict[str, str] = {}
    for rel in TARGETS:
        path = base / rel
        if not path.exists():
            report["missing_targets"].append(rel)
            continue
        text = path.read_text(encoding="latin1")
        texts[rel] = text
        hits = {}
        for token in TOKENS:
            found = snippets(text, token)
            if found:
                hits[token] = found
        report["targets"][rel] = hits

    for rel in ("scripts/inventory/inventory_outfits_ft.scr", "scripts/inventory/inventory_outfits.scr"):
        text = texts.get(rel)
        if not text:
            continue
        names = sorted(set(re.findall(r'Item\("([^"]*Vanguard[^"]*)"\)', text, flags=re.IGNORECASE)))
        for name in names:
            block = extract_braced_block(text, f'Item("{name}")')
            if block:
                report["vanguard_item_blocks"][name] = {"source": rel, "block": block}

    capacity_lines = {}
    cap_pattern = r"[^\n]*(?:QuickSlotsCount|AmmoSlotsCount|Storage\w*SlotsCount|MaxAmmoCountInventoryUpgrade|MaxStack\w*|Stack\w*)[^\n]*"
    for rel, text in texts.items():
        found = [m.group(0).strip() for m in re.finditer(cap_pattern, text, flags=re.IGNORECASE)]
        if found:
            capacity_lines[rel] = sorted(set(found))
    report["capacity_stack_lines"] = capacity_lines

    json_path = outdir / "R3_R4_MAPPING.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    txt_path = outdir / "R3_R4_MAPPING.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(f"REMAKE PROVEN45 R3/R4 MAPPING - runtime {report['current_runtime']}\n")
        f.write("OUTFIT: native Vanguard carriers. INVENTORY: mapping only until exact safe anchors are authored.\n\n")
        if report["missing_targets"]:
            f.write("===== MISSING/OPTIONAL TARGETS =====\n")
            for rel in report["missing_targets"]:
                f.write(f"- {rel}\n")
            f.write("\n")
        f.write("===== VANGUARD ITEM BLOCKS =====\n")
        for name, item in report["vanguard_item_blocks"].items():
            f.write(f"\n--- {name} [{item['source']}] ---\n{item['block']}\n")
        f.write("\n===== CAPACITY / STACK LINES =====\n")
        for rel, lines in capacity_lines.items():
            f.write(f"\n--- {rel} ---\n")
            for line in lines:
                f.write(line + "\n")
        f.write("\n===== TOKEN CONTEXT =====\n")
        for rel, hits in report["targets"].items():
            f.write(f"\n===== {rel} =====\n")
            for token, entries in hits.items():
                f.write(f"--- {token} ---\n")
                for entry in entries:
                    f.write(entry["context"] + "\n\n")

    print(f"RUNTIME={report['current_runtime']}")
    print(f"VANGUARD_ITEMS={len(report['vanguard_item_blocks'])}")
    print(f"JSON={json_path}")
    print(f"TEXT={txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
