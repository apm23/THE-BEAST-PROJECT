#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOKENS = [
    "Viral",
    "Volatile",
    "Charger",
    "Goon",
    "Screamer",
    "Baron",
    "Chimera",
    "Demolisher",
    "Special",
    "Elite",
    "Exotic",
    "Platinum",
    "Enemy_Lottery_Weapons",
]


def extract_block(text: str, anchor: str) -> str | None:
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

    pool_path = base / "scripts/inventory/loot/lootpools_ft.loot"
    sets_path = base / "scripts/inventory/loot/lootsets_ft.loot"
    colors_path = base / "scripts/inventory/loot/color_sets.loot"
    for p in (pool_path, sets_path, colors_path):
        if not p.exists():
            raise FileNotFoundError(p)

    pool_text = pool_path.read_text(encoding="latin1")
    sets_text = sets_path.read_text(encoding="latin1")
    colors_text = colors_path.read_text(encoding="latin1")

    all_names = sorted(set(re.findall(r'LootedObject\("([^"]+)"\)', pool_text)))
    selected = []
    for name in all_names:
        low = name.lower()
        if any(t.lower() in low for t in TOKENS if t not in {"Exotic", "Platinum", "Enemy_Lottery_Weapons"}):
            selected.append(name)

    blocks = {}
    for name in selected:
        block = extract_block(pool_text, f'LootedObject("{name}")')
        if block:
            blocks[name] = block

    token_hits = {}
    for rel, text in [
        ("scripts/inventory/loot/lootpools_ft.loot", pool_text),
        ("scripts/inventory/loot/lootsets_ft.loot", sets_text),
        ("scripts/inventory/loot/color_sets.loot", colors_text),
    ]:
        lines = text.splitlines()
        rel_hits = {}
        for token in TOKENS:
            hits = []
            for i, line in enumerate(lines):
                if token.lower() in line.lower():
                    a = max(0, i - 3)
                    b = min(len(lines), i + 4)
                    hits.append({
                        "line": i + 1,
                        "context": "\n".join(f"{j+1}: {lines[j]}" for j in range(a, b)),
                    })
            if hits:
                rel_hits[token] = hits
        token_hits[rel] = rel_hits

    report = {
        "current_runtime": runtime.get("current_runtime", "unknown"),
        "behavioral_baseline": "USER_HIGH_LOOT_SPECIAL45",
        "policy": "map_only_no_outer_lootedobject_rewrite",
        "special_infected_looted_objects": blocks,
        "token_hits": token_hits,
    }

    j = outdir / "SPECIAL_INFECTED_EXOTIC_MAPPING.json"
    t = outdir / "SPECIAL_INFECTED_EXOTIC_MAPPING.txt"
    j.write_text(json.dumps(report, indent=2), encoding="utf-8")
    with t.open("w", encoding="utf-8") as f:
        f.write(f"SPECIAL INFECTED / EXOTIC MAPPING - runtime {report['current_runtime']}\n")
        f.write("POLICY: map only; do not rewrite outer LootedObject topology.\n\n")
        f.write("===== SPECIAL LootedObject BLOCKS =====\n")
        for name, block in blocks.items():
            f.write(f"\n--- {name} ---\n{block}\n")
        f.write("\n===== TOKEN HITS =====\n")
        for rel, hits in token_hits.items():
            f.write(f"\n### {rel}\n")
            for token, entries in hits.items():
                f.write(f"\n--- {token} ---\n")
                for entry in entries:
                    f.write(entry["context"] + "\n\n")

    print(f"RUNTIME={report['current_runtime']}")
    print(f"SPECIAL_OBJECTS={len(blocks)}")
    print(f"JSON={j}")
    print(f"TEXT={t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
