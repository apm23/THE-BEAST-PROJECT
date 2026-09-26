#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import build_user_special45_payload as special45

PROFILE = "REMAKE_PROVEN45_R1_R2"
POOL_PATH = "scripts/inventory/loot/lootpools_ft.loot"
SETS_PATH = "scripts/inventory/loot/lootsets_ft.loot"
MAPPING_REL = Path("local_build/REMAKE_PROVEN45/mapping/R1_R2_MAPPING.json")
PLAN_REL = Path("config/remake_proven45_r1_r2_ops.json")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reconstruct_special45(baseline: Path, patch_dir: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path, stem in special45.PATCH_MAP.items():
        base_path = baseline / Path(path)
        if not base_path.exists():
            raise FileNotFoundError(f"Missing current-runtime baseline file: {base_path}")
        spec = special45.load_patch(patch_dir, stem)
        files[path] = special45.apply_patch(base_path.read_bytes(), spec)

    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(path, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    got = sha256(bio.getvalue())
    if got != special45.CANONICAL_DATA2_SHA256:
        raise RuntimeError(
            "PROVEN45 guard failed on CURRENT_RUNTIME: "
            f"expected canonical {special45.CANONICAL_DATA2_SHA256}, got {got}. "
            "A dedicated 1.71PE port is required before this builder may run."
        )
    return files


def find_unique(text: str, anchor: str) -> int:
    first = text.find(anchor)
    if first < 0:
        raise RuntimeError(f"Anchor not found: {anchor}")
    if text.find(anchor, first + len(anchor)) >= 0:
        raise RuntimeError(f"Anchor not unique: {anchor}")
    return first


def apply_ops(text: str, ops: list[dict], label: str) -> str:
    out = text
    for idx, op in enumerate(ops, 1):
        kind = op.get("op")
        anchor = op.get("anchor", "")
        payload = op.get("insert", "")
        if not anchor:
            raise RuntimeError(f"{label} op#{idx}: missing anchor")
        pos = find_unique(out, anchor)
        if kind == "insert_after":
            pos += len(anchor)
            out = out[:pos] + payload + out[pos:]
        elif kind == "insert_before":
            out = out[:pos] + payload + out[pos:]
        elif kind == "replace_exact":
            replacement = op.get("replacement")
            if replacement is None:
                raise RuntimeError(f"{label} op#{idx}: missing replacement")
            out = out[:pos] + replacement + out[pos + len(anchor):]
        else:
            raise RuntimeError(f"{label} op#{idx}: unsupported op {kind!r}")
    return out


def lootedobject_sequence(text: str) -> list[str]:
    return re.findall(r'LootedObject\("([^"]+)"\)', text)


def verify_mapping(repo: Path, plan: dict) -> None:
    mapping_path = repo / MAPPING_REL
    if not mapping_path.exists():
        raise FileNotFoundError(
            f"Missing mapping report: {mapping_path}. Run tools/RUN_1.71PE_CORE_PREP.cmd first."
        )
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    human = mapping.get("human_looted_objects", {})
    for name in plan.get("required_human_looted_objects", []):
        if name not in human:
            raise RuntimeError(f"Required human LootedObject missing from current-runtime mapping: {name}")

    token_hits = mapping.get("targets", {})
    required_tokens = plan.get("required_mapping_tokens", [])
    flattened = set()
    for hits in token_hits.values():
        flattened.update(hits.keys())
    for token in required_tokens:
        if token not in flattened:
            raise RuntimeError(f"Required native mapping token not proven on CURRENT_RUNTIME: {token}")


def verify_current_runtime_mode(repo: Path) -> None:
    p = repo / "local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json"
    if not p.exists():
        raise FileNotFoundError("Missing CURRENT_RUNTIME report. Run RUN_1.71PE_CORE_PREP.cmd first.")
    report = json.loads(p.read_text(encoding="utf-8"))
    if report.get("mode") != "SPECIAL45_CORE_BYTE_COMPATIBLE":
        raise RuntimeError("CURRENT_RUNTIME is not byte-compatible with SPECIAL45 core; dedicated 1.71PE port required.")


def write_pak(files: dict[str, bytes], out_path: Path) -> bytes:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files):
            info = zipfile.ZipInfo(path, date_time=special45.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0x01800000
            info.create_system = 3
            z.writestr(info, files[path], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = bio.getvalue()
    out_path.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"PAK integrity failed: {bad}")
    return data


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description="Build guarded R1/R2 remake candidate on CURRENT_RUNTIME while preserving canonical PROVEN45.")
    ap.add_argument("--baseline", type=Path, default=repo / "local_baseline/CURRENT_RUNTIME")
    ap.add_argument("--patch-dir", type=Path, default=repo / "patches/runtime/USER_HIGH_LOOT_SPECIAL45_1.71E")
    ap.add_argument("--plan", type=Path, default=repo / PLAN_REL)
    ap.add_argument("--output", type=Path, default=repo / "local_build/REMAKE_PROVEN45/R1_R2/data2_payload.pak")
    args = ap.parse_args()

    verify_current_runtime_mode(repo)
    if not args.plan.exists():
        raise FileNotFoundError(f"Missing authored operation plan: {args.plan}")
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != "AUTHORED_FROM_CURRENT_RUNTIME_MAPPING":
        raise RuntimeError("R1/R2 operation plan is not authorized; author exact ops from 1.71PE CURRENT_RUNTIME mapping first.")

    verify_mapping(repo, plan)
    files = reconstruct_special45(args.baseline, args.patch_dir)
    before = {p: sha256(b) for p, b in files.items()}
    before_loot_seq = lootedobject_sequence(files[POOL_PATH].decode("latin1"))

    allowed = set(plan.get("allowed_changed_files", []))
    for rel, ops in plan.get("file_operations", {}).items():
        if rel not in files:
            raise RuntimeError(f"Plan tries to edit file outside PROVEN45 payload: {rel}")
        if rel not in allowed:
            raise RuntimeError(f"Plan tries to edit unapproved file: {rel}")
        text = files[rel].decode("latin1")
        files[rel] = apply_ops(text, ops, rel).encode("latin1")

    changed = [p for p, b in files.items() if sha256(b) != before[p]]
    if set(changed) != allowed:
        raise RuntimeError(f"Changed-file guard failed: expected {sorted(allowed)}, got {sorted(changed)}")

    after_loot_seq = lootedobject_sequence(files[POOL_PATH].decode("latin1"))
    if before_loot_seq != after_loot_seq:
        raise RuntimeError("LootedObject topology/name order changed. Candidate rejected before packaging.")

    data = write_pak(files, args.output)
    manifest = {
        "profile": PROFILE,
        "runtime_target": "1.71PE",
        "runtime_status": "CANDIDATE_NOT_RUNTIME_GREEN",
        "derived_from_data2_sha256": special45.CANONICAL_DATA2_SHA256,
        "candidate_data2_sha256": sha256(data),
        "changed_files": changed,
        "lootedobject_sequence_preserved": True,
        "mapping_required": True,
        "plan_sha256": sha256(args.plan.read_bytes()),
    }
    manifest_path = args.output.parent / "BUILD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
