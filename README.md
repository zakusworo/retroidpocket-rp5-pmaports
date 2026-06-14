# postmarketOS port of Retroid Pocket 5 (`retroidpocket-rp5`)

pmaports packages for the **Retroid Pocket 5** (Qualcomm SM8250 / Snapdragon 865),
running postmarketOS with the **phosh** UI on a downstream-ish (near-mainline) kernel.

Based on [aa13q's port](https://gitlab.postmarketos.org/aa13q/pmaports) with
additional fixes (see below). Staging mirror while the postmarketOS GitLab
contribution is pending.

## Packages

| Package | What it is |
|---|---|
| `device/testing/device-retroidpocket-rp5` | Device package + `-kernel-downstream`, `-nonfree-firmware`, `-phosh` subpackages |
| `device/testing/linux-retroidpocket-rp5` | Downstream kernel (6.17.0) with the SM8250 + RP5 patch series and config |

## Fixes / additions in this fork

- **Fan**: temperature-governed cooling-maps (`0021-…fan-cooling-maps.patch`); the
  fancontrol daemon is no longer force-started (thermal governor handles it).
- **Charging icon**: charger online-detection + fuel-gauge live status read
  (`0022`, `0023`) — battery now reports *Charging* instead of *Discharging*.
- **HDMI-out (USB-C DP Alt Mode)**: `CONFIG_TYPEC_DP_ALTMODE=y` so the kernel can
  enter DP alt mode and drive an external display.
- **phosh tweaks** (`-phosh` subpackage): upright-landscape orientation via a
  wlr-randr autostart, 1.75 display scale, on-screen keyboard kept available
  (dconf lock), and a **gamepad-as-mouse** daemon (left stick → pointer,
  A = left-click, B = right-click) since phosh/Wayland ignores the gamepad.
- **Audio**: lowered the too-hot speaker gain (UCM `WSA_RX0/1` 120 → 84) that was
  clipping/distorting.
- Dropped the obsolete `0101-mdss-core-reset.patch` (already in the kernel tag).

## Build / install

Drop the packages into a pmaports clone and build with pmbootstrap:

```sh
cp -r device/testing/* <pmaports>/device/testing/
pmbootstrap config device retroidpocket-rp5
pmbootstrap config kernel downstream
pmbootstrap config ui phosh
pmbootstrap install --password <pw>
```

Flash the resulting image to a MicroSD, hold **Vol+** at power-on, and pick the SD
boot entry. Android on UFS is untouched.

## Credits

- Original port: **aa13q** (Alexey Andreyev) and the postmarketOS community.
- UCM config: Teguh Sobirin.
- Kernel patch sources credited in `device/testing/linux-retroidpocket-rp5/AUTHORS.md`.
