from typing import List
from tracker.coords import Target

def draw_radar(targets: List[Target]) -> None:
    print("\n=== RADAR FRAME ===")
    if not targets:
        print("No Targets set.")
        return

    for t in targets:
        vis ="V" if t.visible else "-"
        print(
            f"[{t.kind[:1].upper()}] {t.name:10s}"
            f"az={t.az:6.1f}  el={t.el:5.1f} "
            f"lat={t.lat:7.3f} lon={t.lon:7.3f} {vis}"
    
        )
def show_text(line1: str, line2: str = "") -> None:
    print(f"[TEXT] {line1} | {line2}")