#!/usr/bin/env python3
# Left stick = mouse pointer; A = left-click, B = right-click.
import time, threading
import evdev
from evdev import ecodes as e, UInput

pad = None
for path in evdev.list_devices():
    d = evdev.InputDevice(path)
    caps = d.capabilities()
    keys = caps.get(e.EV_KEY, [])
    axes = [c for c, _ in caps.get(e.EV_ABS, [])]
    if e.BTN_SOUTH in keys and e.ABS_X in axes:   # gamepad buttons + a stick
        pad = d
        break
if not pad:
    raise SystemExit("No gamepad with an analog stick found in /dev/input/*")
print("Using:", pad.name, pad.path, flush=True)

ai = dict(pad.capabilities()[e.EV_ABS])
xi, yi = ai[e.ABS_X], ai[e.ABS_Y]


def axis(v, info):
    mid = (info.min + info.max) / 2.0
    rng = (info.max - info.min) / 2.0
    n = (v - mid) / rng
    dz = max((info.flat or 0) / rng, 0.12)
    if abs(n) < dz:
        return 0.0
    s = (abs(n) - dz) / (1.0 - dz)
    return (1 if n > 0 else -1) * s * s


ui = UInput({e.EV_REL: [e.REL_X, e.REL_Y], e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT]},
            name="rp5-analog-mouse")
st = {"x": 0.0, "y": 0.0}
SPEED = 18


def reader():
    for ev in pad.read_loop():
        if ev.type == e.EV_ABS:
            if ev.code == e.ABS_X:
                st["x"] = axis(ev.value, xi)
            elif ev.code == e.ABS_Y:
                st["y"] = axis(ev.value, yi)
        elif ev.type == e.EV_KEY and ev.value in (0, 1):
            if ev.code == e.BTN_SOUTH:
                ui.write(e.EV_KEY, e.BTN_LEFT, ev.value)
                ui.syn()
            elif ev.code == e.BTN_EAST:
                ui.write(e.EV_KEY, e.BTN_RIGHT, ev.value)
                ui.syn()


threading.Thread(target=reader, daemon=True).start()
while True:
    dx, dy = int(st["x"] * SPEED), int(st["y"] * SPEED)
    if dx or dy:
        ui.write(e.EV_REL, e.REL_X, dx)
        ui.write(e.EV_REL, e.REL_Y, dy)
        ui.syn()
    time.sleep(1 / 60)
