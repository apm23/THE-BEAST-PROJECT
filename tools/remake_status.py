#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def exists(p: Path) -> bool:
    return p.exists()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    checks = {
        "compatibility_report": repo / "local_build" / "COMPAT_1.71PE_VS_1.71E" / "compatibility.json",
        "current_runtime_report": repo / "local_build" / "CURRENT_RUNTIME_PREP" / "CURRENT_RUNTIME.json",
        "r1_r2_mapping": repo / "local_build" / "REMAKE_PROVEN45" / "mapping" / "R1_R2_MAPPING.json",
        "special_mapping": repo / "local_build" / "REMAKE_PROVEN45" / "mapping" / "SPECIAL_INFECTED_EXOTIC_MAPPING.json",
        "r3_r4_mapping": repo / "local_build" / "REMAKE_PROVEN45" / "mapping" / "R3_R4_MAPPING.json",
        "r1_r2_candidate": repo / "local_build" / "REMAKE_PROVEN45" / "R1_R2" / "data2_payload.pak",
        "r1_r2_manifest": repo / "local_build" / "REMAKE_PROVEN45" / "R1_R2" / "BUILD_MANIFEST.json",
        "final_candidate": repo / "local_build" / "REMAKE_PROVEN45_SINGLEPLAYER_CORE" / "data2_payload.pak",
        "final_manifest": repo / "local_build" / "REMAKE_PROVEN45_SINGLEPLAYER_CORE" / "BUILD_MANIFEST.json",
        "package": repo / "local_build" / "DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip",
    }

    report: dict[str, object] = {
        "runtime_target": "1.71PE",
        "branch_profile": "REMAKE_PROVEN45_SINGLEPLAYER_CORE",
        "checks": {k: {"exists": exists(v), "path": str(v)} for k, v in checks.items()},
    }

    runtime_mode = None
    if checks["current_runtime_report"].exists():
        runtime = json.loads(checks["current_runtime_report"].read_text(encoding="utf-8"))
        runtime_mode = runtime.get("mode")
    report["runtime_mode"] = runtime_mode

    if not checks["compatibility_report"].exists() or not checks["current_runtime_report"].exists():
        next_action = "RUN tools/RUN_1.71PE_CORE_PREP.cmd"
        state = "NEEDS_LOCAL_PREP"
    elif runtime_mode == "PORT_REQUIRED_BEFORE_GAMEPLAY_BUILD":
        next_action = "Author dedicated 1.71PE port from generated port plan; do not build gameplay candidate yet."
        state = "PORT_REQUIRED"
    elif not all(checks[k].exists() for k in ("r1_r2_mapping", "special_mapping", "r3_r4_mapping")):
        next_action = "Re-run tools/RUN_1.71PE_CORE_PREP.cmd to collect all current-runtime mappings."
        state = "MAPPING_INCOMPLETE"
    elif not checks["r1_r2_candidate"].exists():
        next_action = "Author/validate R1-R2 operations from current-runtime mapping, then run BUILD_REMAKE_PROVEN45_R1_R2.cmd."
        state = "READY_FOR_R1_R2_AUTHORING"
    elif not checks["final_candidate"].exists():
        next_action = "Author final-stage operations for special-infected/outfit/inventory-stack and run BUILD_REMAKE_PROVEN45_FINAL.cmd."
        state = "READY_FOR_FINAL_AUTHORING"
    elif not checks["package"].exists():
        next_action = "Run PACKAGE_REMAKE_CANDIDATE.cmd."
        state = "READY_TO_PACKAGE"
    else:
        next_action = "Execute config/remake_singleplayer_test_matrix.json in game; candidate is not runtime-green until all hard gates pass."
        state = "READY_FOR_RUNTIME_TEST"

    report["state"] = state
    report["next_action"] = next_action

    outdir = repo / "local_build" / "REMAKE_STATUS"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    text = [f"STATE={state}", f"RUNTIME_MODE={runtime_mode}", f"NEXT={next_action}", ""]
    for name, item in report["checks"].items():
        text.append(f"{name}={'YES' if item['exists'] else 'NO'} :: {item['path']}")
    (outdir / "status.txt").write_text("\n".join(text) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
