import math
from typing import List

import pygame
from tracker.coords import Target

WIDTH, HEIGHT = 600, 600
RADAR_RADIUS = 250
BG_COLOR = (0, 0, 0)
RADAR_COLOR = (0, 200, 0)
ISS_COLOR = (255, 255, 0)
SAT_COLOR = (0, 255, 0)
PLANE_COLOR = (0, 150, 255)
TEXT_COLOR = (230, 230, 230)

pygame.init()
_screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ORBITZ RADAR")
_font: pygame.font.Font = pygame.font.SysFont("consolas", 20)

_last_text = ("", "")


def _polar_to_cartesian(az_deg: float, el_deg: float) -> tuple[int, int]:
    el_clamped = max(0.0, min(90.0, el_deg))
    r = RADAR_RADIUS * (1.0 - el_clamped / 90.0)

    theta = math.radians(az_deg)
    cx, cy = WIDTH // 2, HEIGHT // 2

    x = cx + r * math.sin(theta)
    y = cy - r * math.cos(theta)

    return int(x), int(y)


def _draw_radar_background() -> None:
    _screen.fill(BG_COLOR)
    cx, cy = WIDTH // 2, HEIGHT // 2

    pygame.draw.circle(_screen, RADAR_COLOR, (cx, cy), RADAR_RADIUS, 1)
    pygame.draw.circle(_screen, RADAR_COLOR, (cx, cy), RADAR_RADIUS * 2 // 3, 1)
    pygame.draw.circle(_screen, RADAR_COLOR, (cx, cy), RADAR_RADIUS // 3, 1)

    pygame.draw.line(
        _screen, RADAR_COLOR,
        (cx - RADAR_RADIUS, cy), (cx + RADAR_RADIUS, cy), 1
    )
    pygame.draw.line(
        _screen, RADAR_COLOR,
        (cx, cy - RADAR_RADIUS), (cx, cy + RADAR_RADIUS), 1
    )


def draw_radar(
    targets: List[Target],
    selected_index: int | None = None,
) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    _draw_radar_background()

    for i, t in enumerate(targets):
        if t.kind == "iss":
            color = ISS_COLOR
        elif t.kind in ("sat", "satellite"):
            color = SAT_COLOR
        elif t.kind in ("plane", "aircraft"):
            color = PLANE_COLOR
        else:
            color = (180, 180, 180)

        x, y = _polar_to_cartesian(t.az, t.el)

        is_selected = selected_index is not None and i == selected_index
        radius = 8 if is_selected else 5
        pygame.draw.circle(_screen, color, (x, y), radius)
        if is_selected:
            pygame.draw.circle(_screen, (255, 255, 255), (x, y), radius + 2, 1)

    line1, line2 = _last_text
    if line1:
        surf = _font.render(line1, True, TEXT_COLOR)
        _screen.blit(surf, (10, 10))
    if line2:
        surf = _font.render(line2, True, TEXT_COLOR)
        _screen.blit(surf, (10, 35))

    pygame.display.flip()


def show_text(line1: str, line2: str = "") -> None:
    global _last_text
    _last_text = (line1, line2)
    print(f"[TEXT] {line1} | {line2}")