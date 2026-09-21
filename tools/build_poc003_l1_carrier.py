from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

TARGETS = {
    "inventory_gen": Path("scripts/inventory/inventory_gen.scr"),
    "inventory": Path("scripts/inventory/inventory.scr"),
    "lootsets": Path("scripts/inventory/loot/lootsets_ft.loot"),
    "lootpools": Path("scripts/inventory/loot/lootpools_ft.loot"),
}

AXE_ANCHOR = 'Item("dlc_ft_WPN_1HS_AXE_03_opportunity_r1", CategoryType_Melee)'
SHOCK_ANCHOR = 'Item("ShockMod_Random_FT_T4_TIP", CategoryType_CraftPart)'
ENEMY_LOTTERY_ANCHOR = 'sub Enemy_Lottery_Weapons(float weight = 1.0, int min_amount = 1, int max_amount = 1, float prob = 1.0)'
BITER_ANCHOR = 'LootedObject("Biter")'


def detect_encoding_and_text(path: Path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    return raw, text, bom


def encode_like(text: str, bom: bool) -> bytes:
    raw = text.encode("utf-8")
    return (b"\xef\xbb\xbf" + raw) if bom else raw


def newline_style(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def find_braced_block(text: str, anchor: str):
    start = text.find(anchor)
    if start < 0:
        raise RuntimeError(f"Anchor not found: {anchor}")
    brace = text.find("{", start + len(anchor))
    if brace < 0:
        raise RuntimeError(f"Opening brace not found for: {anchor}")

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
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start, i + 1, text[start:i + 1]
        i += 1

    raise RuntimeError(f"Unclosed block: {anchor}")


def replace_once(s: str, old: str, new: str, label: str) -> str:
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, found {count}")
    return s.replace(old, new, 1)


def patch_inventory_gen(text: str) -> str:
    start, end, block = find_braced_block(text, AXE_ANCHOR)
    nl = newline_style(text)

    block = replace_once(
        block,
        '        Skin("opportunity");' + nl,
        ''.join([
            '        Skin("opportunity");', nl,
            '        // THE-BEAST-PROJECT POC-003: native Legendary + L+1 carrier probe', nl,
            '        Color(Color_Orange);', nl,
            '        CraftingSlots(true, true, true, true);', nl,
        ]),
        "Camp Axe color/slots",
    )
    block = replace_once(
        block,
        '        WeaponForcedAffixGroup("Slashing_1h_Affixes_Rare_ft");',
        '        WeaponForcedAffixGroup("Slashing_1h_Affixes_Legendary_ft");',
        "Camp Axe forced affix",
    )
    block = replace_once(
        block,
        '        WeaponRandomAffixGroup("Weapons_Random_Rare_ft");',
        '        WeaponRandomAffixGroup("Weapons_Random_Legendary_ft");',
        "Camp Axe random affix",
    )
    block = replace_once(
        block,
        '        DismantleResult("Dismantle_T1_Slash");',
        '        DismantleResult("Dismantle_T3_Slash");',
        "Camp Axe dismantle",
    )
    block = replace_once(
        block,
        '        XrayTriggerProbability(0.0);' + nl,
        ''.join([
            '        XrayTriggerProbability(0.0);', nl,
            '        StartupMod("ShockMod_Random_FT_T4_TIP"); // POC-003 L+1 carrier', nl,
        ]),
        "Camp Axe startup mod",
    )
    return text[:start] + block + text[end:]


def patch_inventory(text: str) -> str:
    start, end, block = find_braced_block(text, SHOCK_ANCHOR)
    nl = newline_style(text)
    block = replace_once(
        block,
        '        Effect(CraftingEffect_IncreasedDamageMul, 4);',
        ''.join([
            '        // POC-003 test-only signature: use highest already-defined native damage level.', nl,
            '        Effect(CraftingEffect_IncreasedDamageMul, 8);',
        ]),
        "Shock damage signature",
    )
    block = replace_once(
        block,
        '        Effect(CraftingEffect_IncreasedDurabilityAdd, 4);',
        ''.join([
            '        // POC-003 test-only signature: native percent durability level 3 = +18%.', nl,
            '        Effect(CraftingEffect_IncreasedDurability, 3);',
        ]),
        "Shock durability signature",
    )
    return text[:start] + block + text[end:]


def patch_lootsets(text: str) -> str:
    start, end, block = find_braced_block(text, ENEMY_LOTTERY_ANCHOR)
    nl = newline_style(text)
    line_start = text.rfind("\n", 0, start) + 1
    indent = text[line_start:start]
    replacement = (
        ENEMY_LOTTERY_ANCHOR + nl
        + indent + "{" + nl
        + indent + "    // THE-BEAST-PROJECT POC-003 deterministic test identity." + nl
        + indent + "    // Final mod restores the full pool and RNG." + nl
        + indent + "    Set(Other, weight, min_amount, max_amount, prob)" + nl
        + indent + "    {" + nl
        + indent + '        Item("dlc_ft_WPN_1HS_AXE_03_opportunity_r1", 1.0);' + nl
        + indent + "    }" + nl
        + indent + "}"
    )
    return text[:start] + replacement + text[end:]


def patch_lootpools(text: str) -> str:
    start, end, block = find_braced_block(text, BITER_ANCHOR)
    old = 'use Enemy_Lottery_Weapons (weight = 0.05, min_amount = 0, max_amount = 1);'
    count = block.count(old)
    if count != 2:
        raise RuntimeError(f"Biter weapon lottery: expected 2 matches, found {count}")
    block = block.replace(old, 'use Enemy_Lottery_Weapons (weight = 15.0, min_amount = 0, max_amount = 1);')
    return text[:start] + block + text[end:]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def brace_count(text: str):
    return text.count("{"), text.count("}")


def main():
    ap = argparse.ArgumentParser(description="Build DLTB 1.71E POC-003 L+1 carrier from user-owned extracted baseline.")
    ap.add_argument("baseline_dir", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stage = args.output_dir / "stage"
    if stage.exists():
        import shutil
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    patchers = {
        "inventory_gen": patch_inventory_gen,
        "inventory": patch_inventory,
        "lootsets": patch_lootsets,
        "lootpools": patch_lootpools,
    }
    audit = {}

    for key, rel in TARGETS.items():
        src = args.baseline_dir / rel
        if not src.exists():
            raise FileNotFoundError(src)
        raw, text, bom = detect_encoding_and_text(src)
        before_braces = brace_count(text)
        patched = patchers[key](text)
        after_braces = brace_count(patched)
        if before_braces != after_braces:
            raise RuntimeError(f"Brace count changed for {rel}: {before_braces} -> {after_braces}")
        if bom != encode_like(patched, bom).startswith(b"\xef\xbb\xbf"):
            raise RuntimeError(f"BOM preservation failure: {rel}")
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(encode_like(patched, bom))
        audit[str(rel)] = {
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "patched_sha256": sha256(dst),
            "bom": bom,
            "newline": "CRLF" if newline_style(text) == "\r\n" else "LF",
            "brace_count": list(after_braces),
        }

    pak = args.output_dir / "data2.pak"
    with zipfile.ZipFile(pak, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in TARGETS.values():
            zf.write(stage / rel, rel.as_posix())

    with zipfile.ZipFile(pak, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"PAK integrity failed: {bad}")
        names = zf.namelist()
        expected = [p.as_posix() for p in TARGETS.values()]
        if names != expected:
            raise RuntimeError(f"Unexpected PAK paths: {names}")

    manifest = {
        "poc": "POC-003_L1_CARRIER",
        "game": "Dying Light: The Beast 1.71E",
        "purpose": "Persistence probe only; not final Ascension balance.",
        "carrier": "ShockMod_Random_FT_T4_TIP",
        "test_signature": {
            "damage_effect": "CraftingEffect_IncreasedDamageMul level 8 (native level already defined)",
            "durability_effect": "CraftingEffect_IncreasedDurability level 3 (+18%)",
            "attack_speed": "unchanged",
        },
        "data2_sha256": sha256(pak),
        "files": audit,
    }
    (args.output_dir / "BUILD_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
