import time

from drivers import display_mock as display
from drivers import inputs_mock as inputs
from drivers import alerts_mock as alerts

from tracker.planes import get_planes_bbox
from tracker.sats import get_iss, get_next_iss_rise_minutes, get_visible_sat_targets
from tracker.coords import Target
import threading

MODE_PLANES = 0
MODE_SATS = 1

REFRESH_SECONDS = 10.0
FRAME_DELAY = 0.02

PASS_REFRESH_SECONDS = 60.0

targets_lock = threading.Lock()
shared_targets: list[Target] = []
shared_line2 = "starting..."
shared_mode = MODE_PLANES

def updater_thread():
    global shared_targets, shared_line2, shared_mode

    last_refresh = 0.0
    next_pass_minutes = None
    last_pass_check = 0.0
    last_mode = shared_mode

    while True:
        now = time.time()
        mode = shared_mode

        # if mode changed, force immediate refresh
        if mode != last_mode:
            last_mode = mode
            last_refresh = 0.0  # so next block runs right away

        if now - last_refresh >= REFRESH_SECONDS:
            last_refresh = now
            if mode == MODE_PLANES:
                try:
                    new_targets = get_planes_bbox()
                    line2 = f"{len(new_targets)} planes" if new_targets else "No planes"
                except Exception as e:
                    new_targets = []
                    line2 = f"Planes error: {e}"

                with targets_lock:
                    shared_targets = new_targets
                    shared_line2 = line2

            else:
                if now - last_pass_check >= PASS_REFRESH_SECONDS:
                    try:
                        next_pass_minutes = get_next_iss_rise_minutes()
                    except Exception:
                        next_pass_minutes = None
                    last_pass_check = now

                mins = next_pass_minutes
                if mins is not None:
                    line2 = f"next pass in {mins:.0f} min"
                else:
                    line2 = "No pass in 24h"

                new_targets = []
                try:
                    iss = get_iss()
                    new_targets.append(iss)
                except Exception:
                    pass

                try:
                    sats = get_visible_sat_targets(min_el_deg=10.0)
                    new_targets.extend(sats)
                except Exception:
                    pass

                with targets_lock:
                    shared_targets = new_targets
                    shared_line2 = line2

        time.sleep(0.1)
        
def main():
    global shared_mode, shared_targets, shared_line2



    mode = MODE_PLANES
    shared_mode = mode
    display.show_text("ORBITZ MOCK CODE", "STARTING...")

    worker = threading.Thread(target=updater_thread, daemon=True)
    worker.start()

    try:
        _ = get_iss()
    except Exception as e:
        display.show_text("ISS init error", str(e))

    targets: list[Target] = []
    selected_index = 0

    while True:
        now = time.time()

        with targets_lock:
            targets = list(shared_targets)
            line2 = shared_line2

        buttons = inputs.read_buttons()
        if buttons.get("quit"):
            display.show_text("Goodbye", "")
            break

        if buttons.get("mode"):
            mode = MODE_SATS if mode == MODE_PLANES else MODE_PLANES
            shared_mode = mode
            selected_index = 0

            with targets_lock:
                shared_targets = []
                shared_line2 = "Loading..."
            targets = []
            line2 = "Loading..."


        if buttons.get("next") and targets:
            selected_index = (selected_index + 1) % len(targets)

        if buttons.get("prev") and targets:
            selected_index = (selected_index - 1) % len(targets)

        if mode == MODE_PLANES:
            display.show_text("Mode: PLANES", line2)
        else:
            display.show_text("Mode: SATS/ISS", line2)

        if targets:
            selected_index %= len(targets)
            t = targets[selected_index]
            if t.kind in ("sat", "iss"):
                info = f"{t.name} az={t.az:.0f} el={t.el:.0f}"
            else:
                info = f"{t.name} hdg={t.heading:.0f} spd={t.speed:.0f}"
            line1, _ = display._last_text
            display.show_text(line1, info)

        display.draw_radar(targets, selected_index=selected_index)
        time.sleep(FRAME_DELAY)

if __name__ == "__main__":
    main()