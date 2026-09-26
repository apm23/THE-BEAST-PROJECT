#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    checks = {
        "compatibility_report": repo / "local_build/COMPAT_1.71PE_VS_1.71E/compatibility.json",
        "current_runtime_report": repo / "local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json",
        "r1_r2_mapping": repo / "local_build/REMAKE_PROVEN45/mapping/R1_R2_MAPPING.json",
        "special_mapping": repo / "local_build/REMAKE_PROVEN45/mapping/SPECIAL_INFECTED_EXOTIC_MAPPING.json",
        "r3_r4_mapping": repo / "local_build/REMAKE_PROVEN45/mapping/R3_R4_MAPPING.json",
        "final_candidate": repo / "local_build/REMAKE_PROVEN45_SINGLEPLAYER_CORE/data2_payload.pak",
        "final_manifest": repo / "local_build/REMAKE_PROVEN45_SINGLEPLAYER_CORE/BUILD_MANIFEST.json",
        "package": repo / "local_build/DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip",
    }
    report: dict[str, object] = {
        "runtime_target": "1.71PE",
        "branch_profile": "REMAKE_PROVEN45_SINGLEPLAYER_CORE",
        "active_builder": "tools/build_remake_proven45_recovered_candidate.py",
        "global_loot_foundation": "USER_HIGH_LOOT_SPECIAL45_BYTE_EXACT",
        "sense": "DEFERRED",
        "coop": "DEFERRED",
        "checks": {k: {"exists": p.exists(), "path": str(p)} for k, p in checks.items()},
    }

    runtime_mode = None
    if checks["current_runtime_report"].exists():
        runtime = json.loads(checks["current_runtime_report"].read_text(encoding="utf-8"))
        runtime_mode = runtime.get("mode")
    report["runtime_mode"] = runtime_mode

    if not checks["compatibility_report"].exists() or not checks["current_runtime_report"].exists():
        state = "NEEDS_LOCAL_PREP"
        next_action = "Run tools/RUN_REMAKE_SINGLEPLAYER_CORE.cmd; it performs 1.71PE prep first."
    elif runtime_mode == "PORT_REQUIRED_BEFORE_GAMEPLAY_BUILD":
        state = "PORT_REQUIRED"
        next_action = "Use generated 1.71PE port plan. Do not transplant or install a guessed gameplay PAK."
    elif runtime_mode != "SPECIAL45_CORE_BYTE_COMPATIBLE":
        state = "CURRENT_RUNTIME_NOT_AUTHORIZED"
        next_action = "Stop and inspect CURRENT_RUNTIME report."
    elif not checks["final_candidate"].exists() or not checks["final_manifest"].exists():
        state = "READY_FOR_RECOVERED_BUILD"
        next_action = "Run tools/BUILD_REMAKE_PROVEN45_RECOVERED.cmd or the one-click RUN_REMAKE_SINGLEPLAYER_CORE.cmd."
    elif not checks["package"].exists():
        state = "READY_TO_PACKAGE"
        next_action = "Run tools/PACKAGE_REMAKE_CANDIDATE.cmd."
    else:
        manifest = json.loads(checks["final_manifest"].read_text(encoding="utf-8"))
        report["candidate_data2_sha256"] = manifest.get("candidate_data2_sha256")
        report["semantic_checks"] = manifest.get("semantic_checks")
        state = "READY_FOR_RUNTIME_TEST"
        next_action = "Install candidate with package launcher and execute config/remake_singleplayer_test_matrix.json. Runtime GREEN only after all hard gates pass."

    report["state"] = state
    report["next_action"] = next_action
    outdir = repo / "local_build/REMAKE_STATUS"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        f"STATE={state}",
        f"RUNTIME_MODE={runtime_mode}",
        "FOUNDATION=USER_HIGH_LOOT_SPECIAL45_BYTE_EXACT",
        "SENSE=DEFERRED",
        "COOP=DEFERRED",
        f"NEXT={next_action}",
        "",
    ]
    for name, item in report["checks"].items():
        lines.append(f"{name}={'YES' if item['exists'] else 'NO'} :: {item['path']}")
    (outdir / "status.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
