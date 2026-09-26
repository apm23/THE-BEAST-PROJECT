#!/usr/bin/env python3
from __future__ import annotations

import json
import traceback
from pathlib import Path

import build_remake_proven45_recovered_candidate as b


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    runtime = repo / "local_baseline/CURRENT_RUNTIME"
    legacy = repo / b.LEGACY_DIR
    outdir = repo / "local_build/REMAKE_PROVEN45_DIAGNOSTIC"
    outdir.mkdir(parents=True, exist_ok=True)
    port_txt = repo / "local_build/PORT_1.71PE_PLAN/PORT_PLAN.txt"

    result = {
        "runtime": "1.71PE",
        "status": "FAILED",
        "stage": None,
        "detail": None,
        "checks": [],
    }

    def run(stage, fn):
        result["stage"] = stage
        try:
            fn()
            result["checks"].append({"stage": stage, "result": "PASS"})
        except Exception as e:
            result["checks"].append({"stage": stage, "result": "FAIL", "error": f"{type(e).__name__}: {e}"})
            result["detail"] = f"{type(e).__name__}: {e}"
            raise

    state = {}
    try:
        run("runtime_report", lambda: b.load_runtime_report(repo))

        def special45():
            state["files"] = b.build_special45_files(repo, runtime)
            state["before_looted"] = b.lootedobject_sequence(state["files"][b.POOL_PATH])
        run("special45_foundation", special45)

        def ranged():
            spec = b.load_transplant(legacy, "inventory_ranged")
            state["files"][b.RANGED_PATH] = b.apply_context_spec(state["files"][b.RANGED_PATH], spec)
        run("transplant_inventory_ranged", ranged)

        def pools():
            spec = b.load_transplant(legacy, "lootpools_g1")
            state["files"][b.POOL_PATH] = b.apply_context_spec(state["files"][b.POOL_PATH], spec)
        run("transplant_lootpools_g1", pools)

        for rel, stem, stage in (
            (b.OUTFIT_PATH, "outfits_ft", "transplant_outfits_ft"),
            (b.AFFIX_PATH, "itemaffixes", "transplant_itemaffixes"),
            (b.CHARM_PATH, "charms", "transplant_charms"),
        ):
            def apply_one(rel=rel, stem=stem):
                src = runtime / rel
                if not src.exists():
                    raise FileNotFoundError(src)
                spec = b.load_transplant(legacy, stem)
                state["files"][rel] = b.apply_context_spec(src.read_bytes(), spec)
            run(stage, apply_one)

        def lootsets():
            block = b.normalized(b.load_block(legacy, "lootsets_append.b64")).strip("\n")
            text = b.normalized(state["files"][b.LOOTSET_PATH].decode("latin1"))
            if block not in text:
                text = text.rstrip() + "\n\n" + block + "\n"
            if text.count(block) != 1:
                raise RuntimeError(f"lootsets custom block count={text.count(block)}")
            state["files"][b.LOOTSET_PATH] = text.encode("latin1")
        run("append_lootsets_block", lootsets)

        run("patch_player_variables", lambda: state["files"].__setitem__(b.PLAYER_VARS, b.patch_player_variables((runtime / b.PLAYER_VARS).read_bytes())))
        run("patch_common_skills", lambda: state["files"].__setitem__(b.COMMON_SKILLS, b.patch_common_skills((runtime / b.COMMON_SKILLS).read_bytes())))

        def topology():
            after = b.lootedobject_sequence(state["files"][b.POOL_PATH])
            if state["before_looted"] != after:
                raise RuntimeError("LootedObject outer topology/name order changed")
        run("lootedobject_topology", topology)

        result["status"] = "ALL_DIAGNOSTIC_STAGES_PASS"
        result["stage"] = "complete"
        result["detail"] = None
    except Exception:
        result["traceback"] = traceback.format_exc()

    json_path = outdir / "BUILD_FAILURE.json"
    txt_path = outdir / "BUILD_FAILURE.txt"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    lines = [
        "REMAKE PROVEN45 RECOVERED TRANSPLANT DIAGNOSTIC",
        f"STATUS={result['status']}",
        f"STAGE={result.get('stage')}",
        f"DETAIL={result.get('detail')}",
        "",
    ]
    for c in result["checks"]:
        line = f"[{c['result']}] {c['stage']}"
        if c.get("error"):
            line += f" :: {c['error']}"
        lines.append(line)
    txt = "\n".join(lines) + "\n"
    txt_path.write_text(txt, encoding="utf-8")

    port_txt.parent.mkdir(parents=True, exist_ok=True)
    with port_txt.open("a", encoding="utf-8") as f:
        f.write("\n\n[BUILD_TRANSPLANT_DIAGNOSTIC]\n")
        f.write(txt)

    print(txt)
    return 0 if result["status"] == "ALL_DIAGNOSTIC_STAGES_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
