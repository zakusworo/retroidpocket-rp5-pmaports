#!/bin/sh
# Force the Retroid Pocket 5 internal panel to upright landscape + 1.75 scale.
# The panel is portrait-mounted; phoc.ini "rotate" is overridden by the DRM
# panel-orientation and the phrog greeter resets a single transform, so we
# re-apply via wlr-randr a few times. Runs from XDG autostart in both the user
# session and the greeter (logs per-user to avoid greetd/user ownership clashes).
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
LOG="$XDG_RUNTIME_DIR/rp5-orient.log"

for i in $(seq 1 60); do
    WD=$(ls "$XDG_RUNTIME_DIR" 2>/dev/null | grep -m1 '^wayland-[0-9]*$')
    [ -n "$WD" ] && break
    sleep 0.5
done
export WAYLAND_DISPLAY="$WD"

n=0
while [ "$n" -lt 7 ]; do
    echo "$(date) user=$(id -un) WD=$WAYLAND_DISPLAY try=$n" >> "$LOG" 2>/dev/null || true
    wlr-randr --output DSI-1 --transform 90 --scale 1.75 >> "$LOG" 2>&1 || \
        wlr-randr --output DSI-1 --transform 90 --scale 1.75 2>/dev/null || true
    n=$((n + 1))
    sleep 2
done
