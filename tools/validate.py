#!/usr/bin/env python3
"""Static validation for project-authored configuration.

This does not validate proprietary game definitions. It protects the repository
from impossible probability ranges, malformed Ascension progression, and
accidental target-version drift.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "balance.json"
EXPECTED_GAME_VERSION = "1.71E"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def check_probability(name: str, value: object) -> None:
    if isinstance(value, (int, float)):
        if not 0 <= float(value) <= 1:
            fail(f"{name} must be between 0 and 1, got {value}")
        return

    if isinstance(value, dict) and set(value) == {"min", "max"}:
        lo = value["min"]
        hi = value["max"]
        if not isinstance(lo, (int, float)) or not isinstance(hi, (int, float)):
            fail(f"{name} range must be numeric")
        if not 0 <= float(lo) <= float(hi) <= 1:
            fail(f"{name} range must satisfy 0 <= min <= max <= 1, got {value}")
        return

    fail(f"{name} must be a probability or {{min,max}} range, got {value!r}")


def main() -> None:
    with CONFIG.open("r", encoding="utf-8") as fh:
        cfg = json.load(fh)

    if cfg.get("schema_version") != 1:
        fail("unsupported schema_version")

    if cfg.get("target_game_version") != EXPECTED_GAME_VERSION:
        fail(
            f"target_game_version must remain {EXPECTED_GAME_VERSION} until MASTER_STATE explicitly changes"
        )

    rarity = cfg.get("rarity", {})
    check_probability(
        "rarity.legendary_per_generated_weapon",
        rarity.get("legendary_per_generated_weapon"),
    )

    for name, value in cfg.get("weapon_drop_targets", {}).items():
        check_probability(f"weapon_drop_targets.{name}", value)

    for name, value in cfg.get("legendary_core_drop_targets", {}).items():
        check_probability(f"legendary_core_drop_targets.{name}", value)

    costs = cfg.get("legendary_core_costs", {})
    expected_cost_order = [
        "rare_or_epic_to_legendary",
        "legendary_to_l1",
        "l1_to_l2",
        "l2_to_l3",
        "l3_to_l4",
        "l4_to_l5",
    ]
    for key in expected_cost_order:
        value = costs.get(key)
        if not isinstance(value, int) or value <= 0:
            fail(f"legendary_core_costs.{key} must be a positive integer")

    stages = cfg.get("ascension_cumulative_targets", {})
    expected_stages = ["l1", "l2", "l3", "l4", "l5"]
    previous = {"damage": -1.0, "durability": -1.0, "attack_speed_ceiling": -1.0}

    for stage in expected_stages:
        values = stages.get(stage)
        if not isinstance(values, dict):
            fail(f"missing ascension stage {stage}")

        for stat in previous:
            value = values.get(stat)
            if not isinstance(value, (int, float)) or value < 0:
                fail(f"ascension_cumulative_targets.{stage}.{stat} must be >= 0")
            if value < previous[stat]:
                fail(f"{stat} must be cumulative/non-decreasing at {stage}")
            previous[stat] = float(value)

    if stages["l5"]["attack_speed_ceiling"] > 0.10:
        fail("L+5 attack-speed ceiling must not exceed 10% without explicit contract change")

    print("Validation OK")
    print(f"Target game: {cfg['target_game_version']}")
    print(f"Legendary roll: {cfg['rarity']['legendary_per_generated_weapon']:.0%}")


if __name__ == "__main__":
    main()
