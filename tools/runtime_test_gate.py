#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

PROFILE = "REMAKE_PROVEN45_SINGLEPLAYER_CORE"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_state(matrix: dict, path: Path) -> dict:
    if path.exists():
        state = load_json(path)
        if state.get("profile") != PROFILE:
            raise RuntimeError("Runtime test state belongs to another profile")
        return state
    state = {
        "profile": PROFILE,
        "runtime_target": matrix["runtime_target"],
        "runtime_status": "CANDIDATE_NOT_RUNTIME_GREEN",
        "created_at": utcnow(),
        "updated_at": utcnow(),
        "tests": {
            t["id"]: {
                "name": t["name"],
                "expect": t["expect"],
                "result": "PENDING",
                "note": "",
                "updated_at": None,
            }
            for t in matrix["tests"]
        },
        "hard_fail_events": [],
        "deferred": matrix.get("deferred", []),
    }
    save_json(path, state)
    return state


def summary(state: dict) -> dict:
    vals = list(state["tests"].values())
    counts = {k: sum(1 for v in vals if v["result"] == k) for k in ("PASS", "FAIL", "PENDING")}
    all_pass = counts["PASS"] == len(vals) and counts["FAIL"] == 0 and counts["PENDING"] == 0
    clean = not state.get("hard_fail_events")
    promotable = all_pass and clean
    return {"counts": counts, "hard_fail_count": len(state.get("hard_fail_events", [])), "promotable": promotable}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["init", "pass", "fail", "hard-fail", "status", "promote", "reset"])
    ap.add_argument("test_id", nargs="?")
    ap.add_argument("--note", default="")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    matrix_path = root / "TEST_MATRIX.json"
    if not matrix_path.exists():
        repo_matrix = root / "config/remake_singleplayer_test_matrix.json"
        matrix_path = repo_matrix if repo_matrix.exists() else matrix_path
    if not matrix_path.exists():
        raise FileNotFoundError("TEST_MATRIX.json / config/remake_singleplayer_test_matrix.json not found")
    matrix = load_json(matrix_path)
    if matrix.get("profile") != PROFILE:
        raise RuntimeError("Unexpected test matrix profile")

    state_path = root / "RUNTIME_TEST_RESULTS.json"
    if args.action == "reset":
        if state_path.exists():
            state_path.unlink()
        state = ensure_state(matrix, state_path)
        print(json.dumps(summary(state), indent=2))
        return 0

    state = ensure_state(matrix, state_path)

    if args.action in ("pass", "fail"):
        if not args.test_id or args.test_id not in state["tests"]:
            raise RuntimeError("Valid test_id required (T01..T15)")
        rec = state["tests"][args.test_id]
        rec["result"] = args.action.upper()
        rec["note"] = args.note
        rec["updated_at"] = utcnow()
        if args.action == "fail":
            state["runtime_status"] = "CANDIDATE_NOT_RUNTIME_GREEN"

    elif args.action == "hard-fail":
        if not args.note:
            raise RuntimeError("--note is required for hard-fail")
        state.setdefault("hard_fail_events", []).append({"at": utcnow(), "note": args.note})
        state["runtime_status"] = "CANDIDATE_NOT_RUNTIME_GREEN"

    elif args.action == "promote":
        s = summary(state)
        if not s["promotable"]:
            raise RuntimeError(f"Cannot promote: {s}")
        state["runtime_status"] = "RUNTIME_GREEN"
        state["promoted_at"] = utcnow()

    state["updated_at"] = utcnow()
    save_json(state_path, state)
    s = summary(state)
    print(json.dumps({"runtime_status": state["runtime_status"], **s}, indent=2))

    if args.action == "status":
        for tid, rec in state["tests"].items():
            print(f"{tid} {rec['result']:7} {rec['name']}" + (f" -- {rec['note']}" if rec['note'] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
