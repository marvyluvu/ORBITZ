import math
from typing import List
import pygame
import pygame.gfxdraw
from tracker.coords import Target

WIDTH, HEIGHT = 600, 600
RADAR_RADIUS = 250

BG_COLOR = (0, 0, 0)
RADAR_COLOR = (0, 200, 0)
ISS_COLOR = (255, 200, 0)
SAT_COLOR = (0, 255, 0)
PLANE_COLOR = (0, 150, 255)
TEXT_MAIN_COLOR = (255, 255, 255)
TEXT_INFO_COLOR = (200, 200, 200)
SELECT_RING_COLOR = (255, 255, 255)

pygame.init()
_screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ORBITZ RADAR")

pygame.font.init()
_font_main: pygame.font.Font = pygame.font.SysFont("consolas", 20)
_font_info: pygame.font.Font = pygame.font.SysFont("consolas", 18)

_last_text = ("", "")
_SWEEP_ANGLE = 0.0
_SWEEP_SPEED = 0.8  # degrees per frame


def _polar_to_cartesian(az_deg: float, el_deg: float) -> tuple[int, int]:
    el_clamped = max(0.0, min(90.0, el_deg))
    r = RADAR_RADIUS * (1.0 - el_clamped / 90.0)

    theta = math.radians(az_deg)
    cx, cy = WIDTH // 2, HEIGHT // 2

    x = cx + r * math.sin(theta)
    y = cy - r * math.cos(theta)

    return int(x), int(y)


def _draw_radar_background() -> None:
    cx, cy = WIDTH // 2, HEIGHT // 2
    _screen.fill(BG_COLOR)

    # text
    line1, line2 = _last_text
    if line1:
        surf = _font_main.render(line1, True, TEXT_MAIN_COLOR)
        _screen.blit(surf, (10, 10))
    if line2:
        surf = _font_info.render(line2, True, TEXT_INFO_COLOR)
        _screen.blit(surf, (10, 35))

    # radar rings
    for frac in (1.0, 2.0 / 3.0, 1.0 / 3.0):
        radius = int(RADAR_RADIUS * frac)
        pygame.gfxdraw.aacircle(_screen, cx, cy, radius, RADAR_COLOR)
        pygame.gfxdraw.circle(_screen, cx, cy, radius, RADAR_COLOR)

    # crosshairs
    pygame.draw.aaline(
        _screen, RADAR_COLOR,
        (cx - RADAR_RADIUS, cy), (cx + RADAR_RADIUS, cy)
    )
    pygame.draw.aaline(
        _screen, RADAR_COLOR,
        (cx, cy - RADAR_RADIUS), (cx, cy + RADAR_RADIUS)
    )


def draw_radar(
    targets: List[Target],
    selected_index: int | None = None,
) -> None:
    global _SWEEP_ANGLE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    _draw_radar_background()

    cx, cy = WIDTH // 2, HEIGHT // 2

    # draw targets
    for i, t in enumerate(targets):
        if t.kind == "iss":
            color = ISS_COLOR
            base_radius = 6
        elif t.kind in ("sat", "satellite"):
            color = SAT_COLOR
            base_radius = 5
        elif t.kind in ("plane", "aircraft"):
            color = PLANE_COLOR
            base_radius = 5
        else:
            color = (180, 180, 180)
            base_radius = 5

        x, y = _polar_to_cartesian(t.az, t.el)
        is_selected = selected_index is not None and i == selected_index

        if is_selected:
            pygame.gfxdraw.filled_circle(_screen, x, y, base_radius + 2, color)
            pygame.gfxdraw.aacircle(_screen, x, y, base_radius + 4, SELECT_RING_COLOR)
            pygame.gfxdraw.circle(_screen, x, y, base_radius + 4, SELECT_RING_COLOR)

            if hasattr(t, "heading"):
                angle = math.radians(t.heading)
                line_len = 12
                x2 = x + int(math.sin(angle) * line_len)
                y2 = y - int(math.cos(angle) * line_len)
                pygame.draw.aaline(_screen, SELECT_RING_COLOR, (x, y), (x2, y2))
        else:
            pygame.gfxdraw.filled_circle(_screen, x, y, base_radius, color)
            pygame.gfxdraw.aacircle(_screen, x, y, base_radius, color)

    # sweep line
    angle_rad = math.radians(_SWEEP_ANGLE)
    x2 = cx + int(math.sin(angle_rad) * RADAR_RADIUS)
    y2 = cy - int(math.cos(angle_rad) * RADAR_RADIUS)
    pygame.draw.aaline(_screen, (0, 80, 0), (cx, cy), (x2, y2))
    _SWEEP_ANGLE = (_SWEEP_ANGLE + _SWEEP_SPEED) % 360.0

    pygame.display.flip()


def show_text(line1: str, line2: str = "") -> None:
    global _last_text
    _last_text = (line1, line2)
    print(f"[TEXT] {line1} | {line2}")