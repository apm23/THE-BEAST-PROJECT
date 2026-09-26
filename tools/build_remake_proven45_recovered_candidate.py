#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import zlib
import zipfile
from pathlib import Path

import build_user_special45_payload as special45

PROFILE = "REMAKE_PROVEN45_SINGLEPLAYER_CORE"
LEGACY_DIR = Path("patches/runtime/REMAKE_PROVEN45_G1_LEGACY")
POOL_PATH = "scripts/inventory/loot/lootpools_ft.loot"
LOOTSET_PATH = "scripts/inventory/loot/lootsets_ft.loot"
RANGED_PATH = "scripts/inventory/inventory_ranged.scr"
OUTFIT_PATH = "scripts/inventory/inventory_outfits_ft.scr"
AFFIX_PATH = "scripts/inventory/itemaffixes.scr"
CHARM_PATH = "scripts/inventory/inventory_charms.scr"
PLAYER_VARS = "scripts/player/player_variables.scr"
COMMON_SKILLS = "scripts/skills/common_skills.xml"

LINEAGE = {
    "special45": "190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657",
    "stack99999": "77e7ff5630167af4f733bda7e754ab0eb8f90c0491e75403caaeb64077a44155",
    "weapon68": "8b1587ce0741295e98598a2ea6e22fe67102a6b34644cacd14f7558ea09dde18",
    "g1_preflight": "6ee08e9d867a9a72b1968b557256747ac701c511f7580b0605f4cd3906e2b5c5",
    "night_sovereign": "047a44416f7ab8a1bb736cf2aac374a0cb36b96a0ff775ed05ff8ad2e73e4521",
}

INV_VALUES = {
    "MaxEquipmentSlotsCount": "34",
    "EquipmentSlotsCount": "34",
    "MaxConsumableSlotsCount": "34",
    "ConsumableSlotsCount": "34",
    "MaxQuickSlotsCount": "68",
    "QuickSlotsCount": "68",
    "MaxAmmoSlotsCount": "42",
    "AmmoSlotsCount": "42",
    "InventoryUpgradeEnabled": "true",
    "InventoryCraftPartMaxStackCount": "99999",
    "InventoryConsumableMaxStackCount": "99999",
    "InventoryThrowableMaxStackCount": "99999",
}

SKILL_EFFECTS = (
    "EquipmentSlotsCount",
    "ConsumableSlotsCount",
    "QuickSlotsCount",
    "AmmoSlotsCount",
    "InventoryCraftPartMaxStackCount",
    "InventoryConsumableMaxStackCount",
    "InventoryThrowableMaxStackCount",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_runtime_report(repo: Path) -> dict:
    p = repo / "local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json"
    if not p.exists():
        raise FileNotFoundError("Run tools/RUN_1.71PE_CORE_PREP.cmd first")
    report = json.loads(p.read_text(encoding="utf-8"))
    if report.get("current_runtime") != "1.71PE":
        raise RuntimeError(f"Unexpected CURRENT_RUNTIME: {report.get('current_runtime')!r}")
    if report.get("mode") != "SPECIAL45_CORE_BYTE_COMPATIBLE":
        raise RuntimeError("1.71PE SPECIAL45 core is not byte-compatible. Dedicated port required; refusing transplant.")
    return report


def load_transplant(path: Path, stem: str) -> dict:
    parts = sorted(path.glob(stem + ".part*.b64"))
    if not parts:
        single = path / (stem + ".b64")
        if not single.exists():
            raise FileNotFoundError(single)
        parts = [single]
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    raw = zlib.decompress(base64.b64decode(encoded))
    return json.loads(raw.decode("utf-8"))


def load_block(path: Path, name: str) -> str:
    encoded = (path / name).read_text(encoding="ascii").strip()
    return zlib.decompress(base64.b64decode(encoded)).decode("latin1")


def normalized(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def apply_context_spec(data: bytes, spec: dict) -> bytes:
    # Exact historical base: preserve exact bytes and require historical target hash.
    if sha256(data) == spec.get("base_sha256"):
        text = data.decode("latin1")
        for i, op in enumerate(spec["ops"], 1):
            needle = op["before"] + op["old"] + op["after"]
            if text.count(needle) != 1:
                raise RuntimeError(f"{spec['path']} exact op#{i}: context count={text.count(needle)}")
            repl = op["before"] + op["new"] + op["after"]
            text = text.replace(needle, repl, 1)
        out = text.encode("latin1")
        if sha256(out) != spec.get("target_sha256"):
            raise RuntimeError(f"Historical target hash mismatch after exact transplant: {spec['path']}")
        return out

    # Current runtime differs: use normalized unique context only; never guess.
    text = normalized(data.decode("latin1"))
    for i, op in enumerate(spec["ops"], 1):
        before = normalized(op["before"])
        old = normalized(op["old"])
        after = normalized(op["after"])
        new = normalized(op["new"])
        needle = before + old + after
        already = before + new + after
        if text.count(already) == 1:
            continue
        count = text.count(needle)
        if count != 1:
            raise RuntimeError(f"{spec['path']} current-runtime op#{i}: unique context required, got {count}")
        text = text.replace(needle, before + new + after, 1)
    return text.encode("latin1")


def patch_player_variables(data: bytes) -> bytes:
    text = data.decode("latin1")
    original = text
    for name, value in INV_VALUES.items():
        pat = re.compile(rf'(Param\("{re.escape(name)}",\s*")[^"]+("\);)')
        matches = list(pat.finditer(text))
        if len(matches) != 1:
            raise RuntimeError(f"player_variables: expected one {name}, got {len(matches)}")
        text = pat.sub(rf'\g<1>{value}\g<2>', text, count=1)
    if text == original:
        raise RuntimeError("player_variables narrow patch made no change")
    for name, value in INV_VALUES.items():
        if not re.search(rf'Param\("{re.escape(name)}",\s*"{re.escape(value)}"\);', text):
            raise RuntimeError(f"player_variables verification failed: {name}={value}")
    return text.encode("latin1")


def patch_common_skills(data: bytes) -> bytes:
    text = data.decode("latin1")
    for skill in ("InventoryUpgrade_1", "InventoryUpgrade_2"):
        pat = re.compile(rf'(<skill id="{skill}"\b.*?</skill>)', re.S)
        m = pat.search(text)
        if not m:
            raise RuntimeError(f"common_skills: missing {skill}")
        block = m.group(1)
        new_block = block
        for effect in SKILL_EFFECTS:
            ep = re.compile(rf'(<effect id="{re.escape(effect)}" change=")[^"]+("\s*/>)')
            hits = list(ep.finditer(new_block))
            if len(hits) != 1:
                raise RuntimeError(f"common_skills {skill}: expected one {effect}, got {len(hits)}")
            new_block = ep.sub(r'\g<1>0\g<2>', new_block, count=1)
        text = text[:m.start()] + new_block + text[m.end():]
    return text.encode("latin1")


def lootedobject_sequence(data: bytes) -> list[str]:
    return re.findall(r'LootedObject\("([^"]+)"\)', data.decode("latin1"))


def build_special45_files(repo: Path, runtime: Path) -> dict[str, bytes]:
    patch_dir = repo / "patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E"
    files: dict[str, bytes] = {}
    for rel, stem in special45.PATCH_MAP.items():
        src = runtime / rel
        if not src.exists():
            raise FileNotFoundError(src)
        spec = special45.load_patch(patch_dir, stem)
        files[rel] = special45.apply_patch(src.read_bytes(), spec)
    # Prove the foundation itself is still exactly canonical before adding anything.
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(files):
            info = zipfile.ZipInfo(rel, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[rel], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    if sha256(bio.getvalue()) != special45.CANONICAL_DATA2_SHA256:
        raise RuntimeError("SPECIAL45 canonical foundation hash drifted; refusing remake build")
    return files


def write_pak(files: dict[str, bytes], out: Path) -> bytes:
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(files):
            info = zipfile.ZipInfo(rel, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[rel], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = bio.getvalue()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Candidate PAK integrity failure: {bad}")
    return data


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    runtime = repo / "local_baseline/CURRENT_RUNTIME"
    legacy = repo / LEGACY_DIR
    report = load_runtime_report(repo)
    if not runtime.exists():
        raise FileNotFoundError(runtime)

    files = build_special45_files(repo, runtime)
    before_looted = lootedobject_sequence(files[POOL_PATH])

    for rel, stem in (
        (RANGED_PATH, "inventory_ranged"),
        (POOL_PATH, "lootpools_g1"),
    ):
        spec = load_transplant(legacy, stem)
        if spec.get("path") != rel:
            raise RuntimeError(f"Transplant path mismatch for {stem}: {spec.get('path')}")
        files[rel] = apply_context_spec(files[rel], spec)

    for rel, stem in (
        (OUTFIT_PATH, "outfits_ft"),
        (AFFIX_PATH, "itemaffixes"),
        (CHARM_PATH, "charms"),
    ):
        src = runtime / rel
        if not src.exists():
            raise FileNotFoundError(src)
        spec = load_transplant(legacy, stem)
        if spec.get("path") != rel:
            raise RuntimeError(f"Transplant path mismatch for {stem}: {spec.get('path')}")
        files[rel] = apply_context_spec(src.read_bytes(), spec)

    block = normalized(load_block(legacy, "lootsets_append.b64")).strip("\n")
    lootsets = normalized(files[LOOTSET_PATH].decode("latin1"))
    if block not in lootsets:
        lootsets = lootsets.rstrip() + "\n\n" + block + "\n"
    if lootsets.count(block) != 1:
        raise RuntimeError("G1 lootsets append block must occur exactly once")
    files[LOOTSET_PATH] = lootsets.encode("latin1")

    pv = runtime / PLAYER_VARS
    cs = runtime / COMMON_SKILLS
    if not pv.exists() or not cs.exists():
        raise FileNotFoundError("Missing player_variables/common_skills CURRENT_RUNTIME extraction")
    files[PLAYER_VARS] = patch_player_variables(pv.read_bytes())
    files[COMMON_SKILLS] = patch_common_skills(cs.read_bytes())

    after_looted = lootedobject_sequence(files[POOL_PATH])
    if before_looted != after_looted:
        raise RuntimeError("LootedObject outer topology/name order changed; candidate rejected")

    # Required semantic proofs.
    checks = {
        "native_exotic_route": b"DLTB_G1_Firearm_ExoticNative" in files[LOOTSET_PATH] and b"ColorSet_ExoticOnly" in files[POOL_PATH],
        "night_sovereign": b"Night_Sovereign" in files[OUTFIT_PATH] and b"Night_Sovereign" in files[AFFIX_PATH],
        "sigil": b"charm_Night_Sovereign" in files[CHARM_PATH],
        "weapon_drop_share": b"CanDrop(true)" in files[RANGED_PATH] and b"IsShareable(true)" in files[RANGED_PATH],
        "inventory_68": b'Param("QuickSlotsCount", "68")' in files[PLAYER_VARS],
        "stack_99999": b'Param("InventoryCraftPartMaxStackCount", "99999")' in files[PLAYER_VARS],
        "sense_deferred": True,
        "coop_deferred": True,
        "lootedobject_sequence_preserved": before_looted == after_looted,
    }
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise RuntimeError(f"Semantic guard failed: {failed}")

    out = repo / "local_build/REMAKE_PROVEN45_SINGLEPLAYER_CORE/data2_payload.pak"
    data = write_pak(files, out)
    manifest = {
        "profile": PROFILE,
        "runtime_target": "1.71PE",
        "runtime_status": "CANDIDATE_NOT_RUNTIME_GREEN",
        "foundation": "USER_HIGH_LOOT_SPECIAL45_BYTE_EXACT",
        "foundation_sha256": special45.CANONICAL_DATA2_SHA256,
        "candidate_data2_sha256": sha256(data),
        "current_runtime_mode": report.get("mode"),
        "recovered_lineage": LINEAGE,
        "pak_members": sorted(files),
        "semantic_checks": checks,
        "inventory_targets": {"equipment": 34, "consumable": 34, "weapon": 68, "ammo": 42},
        "stack_target": 99999,
        "sense_included": False,
        "coop_included": False,
        "notes": [
            "Global loot foundation remains canonical SPECIAL45; no Global Root V1 override is used.",
            "Recovered G1 changes are context-transplanted and fail closed on ambiguous current-runtime context.",
            "player_variables/common_skills are narrowed to proven inventory/stack semantics only.",
            "Runtime GREEN requires in-game smoke tests on 1.71PE."
        ],
    }
    mpath = out.parent / "BUILD_MANIFEST.json"
    mpath.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
