# SP1 PROVEN SENSE LOCK — 2026-10-01

This is a durable addendum to `MASTER_STATE_SP1.md` for the native Survivor Sense branch.

## GREEN / runtime-proven

The following behavior was explicitly confirmed in-game by the user:

- Ordinary Biters become visible through walls using the **native Survivor Sense/XRay renderer**.
- Resting / sleeping Biters are also picked up by the same Sense path.
- The working mechanism is an **empty-key hostility fallback** in `ai/survivor_sense_hostility_presets.scr`.
- The proven fallback shape is:

```scr
SurvivorSenseHostilityPresets("")
{
    GenericNonHostile("");
    ScriptedNonHostile("");
    GenericHostile("Preset_red_FT");
    ScriptedHostile("Preset_red_FT");
}
```

- This route requires no custom overlay, no W2S, no Lua runtime hook, no DLL patch, and no live AI-field transplant.
- The native game handles tracking, animation, and through-wall rendering once the fallback resolves to a valid hostile Sense preset.

## Important runtime interpretation

Earlier N1.3 runtime snapshots proved ordinary Biters were already present in the native Survivor Sense candidate vector, while their runtime `m_SurvivorSensePreset` resolved to an empty/default form. The empty-key hostility fallback is therefore the first route that was both technically consistent with the runtime observations and explicitly confirmed working in-game.

## DO NOT regress to failed live-hook branches

The following branches caused force closes or were disproven and should not be retried as the default route:

- runtime preset-handle transplant into `AI+0x25C8`;
- N1.5 / N1.5.1 predicate-submit CALL wrappers;
- N1.6 transient register preset bridge;
- broad raw-memory camera scans;
- V42–V45 raw native state transplant.

## Current V2 status

A later V2 experiment adds a dedicated cyan Biter preset plus near-zero smoothing and longer persistence/distance settings. The user has **not yet completed verification of requested functions #3 and #4** (fade-in minimization and long-distance / turn-away persistence), so those two must remain **UNPROVEN / TEST-PENDING** and must not be promoted to GREEN yet.

The safe GREEN baseline remains the small empty-key hostility fallback above, including sleeping/resting Biter support.

## Continuation rule

When resuming SP1 Sense work, preserve this proven baseline first. Any future color, fade, duration, or distance changes must be layered on top and independently verified without sacrificing the working empty-key fallback.
