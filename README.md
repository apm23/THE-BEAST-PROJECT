# THE BEAST PROJECT

Development repository for **Dying Light: The Beast** gameplay-mod research and reproducible patch tooling.

## Active branch state — `remake-proven45`

- Current runtime target: **VER. 1.71PE**.
- Global loot foundation: canonical **USER HIGH LOOT SPECIAL45 / PROVEN45**.
- Current scope: **single-player core first**.
- Sense and one-sided CO-OP: **DEFERRED**.
- Legendary Core / Ascension: **CANCELLED for this remake**.
- Repository stores project-authored patches/specs/tooling only; extracted proprietary game archives and user saves stay local.

## Authority for this branch

Read in this order:

1. `REMAKE_MASTER_STATE.md` — current authority for `remake-proven45`.
2. `PROJECT_CONTRACT.md`.
3. `FEATURE_SPEC.md`.
4. `config/remake_singleplayer_test_matrix.json`.
5. Historical `MASTER_STATE.md` only for proven lineage/history that does not conflict with `REMAKE_MASTER_STATE.md`.

## One-command local pipeline

On the Windows PC containing the user's owned current DLTB install:

```text
tools\RUN_REMAKE_SINGLEPLAYER_CORE.cmd
```

It performs 1.71PE extraction/compatibility checks, reconstructs SPECIAL45 byte-exact, applies fail-closed recovered G1 transplants, builds the single-player candidate, and packages safe install/status/rollback launchers.

The resulting candidate remains **CANDIDATE_NOT_RUNTIME_GREEN** until the committed T01–T15 in-game matrix passes.

## Safety

Do not commit full extracted vanilla files, game PAKs from the installation, saves, or local install paths. Do not revive blacklisted aggressive LootedObject or item-registry experiments. See `REMAKE_MASTER_STATE.md` and `.gitignore`.
