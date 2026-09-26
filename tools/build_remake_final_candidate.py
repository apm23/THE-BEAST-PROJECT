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

PROFILE = "REMAKE_PROVEN45_SINGLEPLAYER_CORE"
PLAN_REL = Path("config/remake_proven45_final_ops.json")
R1R2_PAK_REL = Path("local_build/REMAKE_PROVEN45/R1_R2/data2_payload.pak")
R1R2_MANIFEST_REL = Path("local_build/REMAKE_PROVEN45/R1_R2/BUILD_MANIFEST.json")
SPECIAL_MAPPING_REL = Path("local_build/REMAKE_PROVEN45/mapping/SPECIAL_INFECTED_EXOTIC_MAPPING.json")
R3R4_MAPPING_REL = Path("local_build/REMAKE_PROVEN45/mapping/R3_R4_MAPPING.json")
POOL_PATH = "scripts/inventory/loot/lootpools_ft.loot"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
        if not anchor:
            raise RuntimeError(f"{label} op#{idx}: missing anchor")
        pos = find_unique(out, anchor)
        if kind == "insert_after":
            payload = op.get("insert")
            if payload is None:
                raise RuntimeError(f"{label} op#{idx}: missing insert payload")
            pos += len(anchor)
            out = out[:pos] + payload + out[pos:]
        elif kind == "insert_before":
            payload = op.get("insert")
            if payload is None:
                raise RuntimeError(f"{label} op#{idx}: missing insert payload")
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


def load_pak(path: Path) -> dict[str, bytes]:
    if not path.exists():
        raise FileNotFoundError(path)
    files: dict[str, bytes] = {}
    with zipfile.ZipFile(path, "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Base candidate PAK failed integrity: {bad}")
        for name in z.namelist():
            if name.endswith("/"):
                continue
            files[name] = z.read(name)
    return files


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
            raise RuntimeError(f"Final PAK integrity failed: {bad}")
    return data


def verify_runtime(repo: Path) -> None:
    p = repo / "local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json"
    if not p.exists():
        raise FileNotFoundError("Missing CURRENT_RUNTIME report. Run RUN_1.71PE_CORE_PREP.cmd first.")
    r = json.loads(p.read_text(encoding="utf-8"))
    if r.get("mode") != "SPECIAL45_CORE_BYTE_COMPATIBLE":
        raise RuntimeError("Current runtime requires a dedicated 1.71PE core port before final gameplay build.")


def verify_mappings(repo: Path) -> None:
    for rel in (SPECIAL_MAPPING_REL, R3R4_MAPPING_REL):
        p = repo / rel
        if not p.exists():
            raise FileNotFoundError(f"Missing current-runtime mapping: {p}")


def path_forbidden(path: str, plan: dict) -> bool:
    low = path.lower()
    for frag in plan.get("hard_forbidden_path_fragments", []):
        if frag.lower() in low:
            return True
    return False


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description="Build final guarded 1.71PE single-player core candidate on top of R1/R2.")
    ap.add_argument("--plan", type=Path, default=repo / PLAN_REL)
    ap.add_argument("--base-pak", type=Path, default=repo / R1R2_PAK_REL)
    ap.add_argument("--base-manifest", type=Path, default=repo / R1R2_MANIFEST_REL)
    ap.add_argument("--runtime", type=Path, default=repo / "local_baseline/CURRENT_RUNTIME")
    ap.add_argument("--output", type=Path, default=repo / "local_build/REMAKE_PROVEN45_SINGLEPLAYER_CORE/data2_payload.pak")
    args = ap.parse_args()

    verify_runtime(repo)
    verify_mappings(repo)
    if not args.plan.exists():
        raise FileNotFoundError(args.plan)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != "AUTHORED_FROM_CURRENT_RUNTIME_MAPPING":
        raise RuntimeError("Final operation plan is not authorized from 1.71PE CURRENT_RUNTIME mapping.")

    if not args.base_manifest.exists():
        raise FileNotFoundError(args.base_manifest)
    base_manifest = json.loads(args.base_manifest.read_text(encoding="utf-8"))
    if base_manifest.get("profile") != "REMAKE_PROVEN45_R1_R2":
        raise RuntimeError("Unexpected base candidate profile.")
    if base_manifest.get("runtime_status") == "RUNTIME_GREEN":
        pass

    files = load_pak(args.base_pak)
    base_pak_sha = sha256(args.base_pak.read_bytes())
    before_pool_seq = lootedobject_sequence(files[POOL_PATH].decode("latin1")) if POOL_PATH in files else []

    allowed = set(plan.get("allowed_changed_files", []))
    expected = set(plan.get("expected_changed_files", []))
    ops_by_file = plan.get("file_operations", {})

    if set(ops_by_file) != expected:
        raise RuntimeError(
            f"Plan consistency failed: file_operations keys must equal expected_changed_files. "
            f"ops={sorted(ops_by_file)}, expected={sorted(expected)}"
        )
    if not expected.issubset(allowed):
        raise RuntimeError("Expected changed files are not a subset of allowed_changed_files.")

    source_before: dict[str, bytes] = {}
    base_members = set(files)

    for rel in sorted(expected):
        if path_forbidden(rel, plan):
            raise RuntimeError(f"Forbidden path requested by final plan: {rel}")
        if rel in files:
            source = files[rel]
        else:
            src = args.runtime / rel
            if not src.exists():
                raise FileNotFoundError(f"Current-runtime source file missing for final stage: {src}")
            source = src.read_bytes()
        source_before[rel] = source
        text = source.decode("latin1")
        patched = apply_ops(text, ops_by_file[rel], rel).encode("latin1")
        if patched == source:
            raise RuntimeError(f"Authored operations made no change: {rel}")
        files[rel] = patched

    changed_stage = {rel for rel in expected if files[rel] != source_before[rel]}
    if changed_stage != expected:
        raise RuntimeError(f"Final-stage changed-file guard failed: expected {sorted(expected)}, got {sorted(changed_stage)}")

    if POOL_PATH in files:
        after_pool_seq = lootedobject_sequence(files[POOL_PATH].decode("latin1"))
        if before_pool_seq and before_pool_seq != after_pool_seq:
            raise RuntimeError("LootedObject topology/name order changed in final stage. Candidate rejected.")

    # Do not carry untouched vanilla-only files into the PAK merely because they were allowed.
    for rel in list(files):
        if rel not in base_members and rel not in expected:
            del files[rel]

    data = write_pak(files, args.output)
    manifest = {
        "profile": PROFILE,
        "runtime_target": "1.71PE",
        "runtime_status": "CANDIDATE_NOT_RUNTIME_GREEN",
        "base_profile": "REMAKE_PROVEN45_R1_R2",
        "base_candidate_sha256": base_pak_sha,
        "candidate_data2_sha256": sha256(data),
        "final_stage_changed_files": sorted(changed_stage),
        "pak_members": sorted(files),
        "lootedobject_sequence_preserved": True,
        "sense_included": False,
        "coop_included": False,
        "plan_sha256": sha256(args.plan.read_bytes()),
        "test_matrix": "config/remake_singleplayer_test_matrix.json"
    }
    manifest_path = args.output.parent / "BUILD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
