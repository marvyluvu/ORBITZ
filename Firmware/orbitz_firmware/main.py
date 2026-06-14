import time

from drivers import display_mock as display
from drivers import inputs_mock as inputs
from drivers import alerts_mock as alerts

from tracker.planes import get_planes_bbox
from tracker.sats import get_iss, get_next_iss_rise_minutes

MODE_PLANES = 0
MODE_ISS = 1

def main():
    mode = MODE_PLANES

    display.show_text("ORBITZ MOCK CODE", "STARTING...")

    while True:
        buttons = inputs.read_buttons()
        if buttons["quit"]:
            display.show_text("Goodbye", "")
            break

        if buttons["mode"]:
           

            mode = MODE_ISS if mode == MODE_PLANES else MODE_PLANES

        if mode == MODE_PLANES:
            display.show_text("Mode: PLANES", "")
            try:
                planes = get_planes_bbox()
            except Exception as e:
                display.show_text("Plane error", str(e))
                planes = []

            display.draw_radar(planes)
            alerts.set_strip("blue", "blink" if planes else "off")

        else:  
            mins = get_next_iss_rise_minutes()
            if mins is not None: 
                line2 = f"next pass in {mins:.0f} min"
            else:
                line2 = " No pass in 24h"
            
            display.show_text("Mode: ISS", line2)

            try:
                iss = get_iss()
                targets = [iss]
            except Exception as e:
                display.show_text("ISS error", str(e))
                targets = []

            display.draw_radar(targets)
            alerts.set_strip(
                "green",
                "blink" if targets and targets[0].visible else "off",
            )

        time.sleep(5)

if __name__ == "__main__":
    main()