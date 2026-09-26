#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PROFILE = "REMAKE_PROVEN45_SINGLEPLAYER_CORE"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    root = Path.cwd()
    package_manifest = root / "PACKAGE_MANIFEST.json"
    results_path = root / "RUNTIME_TEST_RESULTS.json"
    matrix_path = root / "TEST_MATRIX.json"
    pak = root / "data2_payload.pak"

    for p in (package_manifest, results_path, matrix_path, pak):
        if not p.exists():
            raise FileNotFoundError(p)

    pm = load(package_manifest)
    results = load(results_path)
    matrix = load(matrix_path)

    if pm.get("profile") != PROFILE or results.get("profile") != PROFILE or matrix.get("profile") != PROFILE:
        raise RuntimeError("Profile mismatch; refusing runtime-green finalization")
    if pm.get("runtime_target") != "1.71PE" or results.get("runtime_target") != "1.71PE":
        raise RuntimeError("Runtime target mismatch")
    if results.get("runtime_status") != "RUNTIME_GREEN":
        raise RuntimeError("Test gate has not promoted this candidate")
    if results.get("hard_fail_events"):
        raise RuntimeError("Hard-fail history exists; refusing GREEN certificate")

    required = [t["id"] for t in matrix.get("tests", [])]
    if required != [f"T{i:02d}" for i in range(1, 16)]:
        raise RuntimeError("Unexpected runtime test matrix; expected T01-T15")
    missing = [tid for tid in required if results.get("tests", {}).get(tid, {}).get("result") != "PASS"]
    if missing:
        raise RuntimeError(f"Runtime tests not all PASS: {missing}")

    actual_hash = sha256_file(pak)
    expected_hash = pm.get("data2_sha256")
    if actual_hash != expected_hash:
        raise RuntimeError("data2 payload hash changed after test package creation")

    source = pm.get("source_manifest", {})
    if source.get("foundation_sha256") != "190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657":
        raise RuntimeError("Canonical SPECIAL45 foundation declaration missing")
    if source.get("sense_included") is not False or source.get("coop_included") is not False:
        raise RuntimeError("Deferred Sense/CO-OP unexpectedly present")

    now = datetime.now(timezone.utc).isoformat()
    certificate = {
        "profile": PROFILE,
        "runtime_target": "1.71PE",
        "runtime_status": "RUNTIME_GREEN",
        "data2_sha256": actual_hash,
        "special45_foundation_sha256": source["foundation_sha256"],
        "tests_passed": required,
        "hard_fail_count": 0,
        "sense_included": False,
        "coop_included": False,
        "promoted_at": results.get("promoted_at"),
        "certificate_created_at": now,
        "note": "GREEN applies only to this exact data2 hash on the tested 1.71PE runtime and test scope. New Game/NG+ remain separate unless explicitly tested."
    }
    dump(root / "RUNTIME_GREEN_CERTIFICATE.json", certificate)

    pm["runtime_status"] = "RUNTIME_GREEN"
    pm["runtime_green_certificate"] = "RUNTIME_GREEN_CERTIFICATE.json"
    pm["runtime_green_data2_sha256"] = actual_hash
    pm["runtime_green_at"] = now
    dump(package_manifest, pm)

    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
