# USER HIGH LOOT SPECIAL45 — exact 1.71E patch source

This directory stores the **project-authored delta data only** needed to rebuild the canonical USER HIGH LOOT SPECIAL45 `data2_payload.pak` from an owned, verified Dying Light: The Beast 1.71E install.

It intentionally does **not** contain complete vanilla game files.

Builder:

`tools/build_user_special45_payload.py`

Expected baseline files and captured 1.71E hashes:

- `scripts/inventory/inventory_ranged.scr`
  - baseline SHA-256 `610622dae7450d36a873ea630dbf9fac2757e359fa4d159b23305a0590b82b20`
  - final SHA-256 `8bf5e4d097972ed9075f6105efe4e5fb533d44ecd5f3dd39cc44fb5bd210f745`
- `scripts/inventory/loot/lootpools_ft.loot`
  - baseline SHA-256 `fac968e396e185888f20cdfc20543f4a492d10f21f5dde0c8f8b2c9c054a9f98`
  - final SHA-256 `46fe4e2c3c63e68fda99c80c1982689cbd874f16c1c173e2fa6643501be8635e`
- `scripts/inventory/loot/lootsets_ft.loot`
  - baseline SHA-256 `9addc1fbfb35b56c8be9928307208b12f3f0672cf303affdba661a4193d6410a`
  - final SHA-256 `b6f2f78ab4a2c0dcf1a1feddd2129de4c60eedb4900c894e628c91292669c308`

Canonical rebuilt `data2_payload.pak` SHA-256:

`190d7cb172fffe09b227f9b2fdb9b596dea5bf1e2d239fe804c377c45e392657`

The patch specs are compressed/base64 JSON edit instructions. The builder:

1. verifies the local vanilla baseline SHA-256 + size;
2. applies only the stored project delta operations;
3. verifies each final patched file hash + size;
4. creates the three-entry PAK with fixed ZIP metadata;
5. requires the exact canonical final PAK SHA-256 above.

The reconstruction was tested locally against the original canonical payload and produced **byte-for-byte identical output**.

Typical flow from repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\extract_targeted_baseline_1.71E.ps1
python .\tools\build_user_special45_payload.py --prepare-switcher
```

Or use:

`tools\BOOTSTRAP_1.71E_USER_SPECIAL45.cmd`
