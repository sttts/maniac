"""Procedural pixel art generators — authentic Maniac Mansion style at 320x200.

Uses dithering, careful color placement, and detailed shapes to match the
SCUMM engine look from the concept art.
"""
import math
import pygame
from src.font import draw_text, draw_text_centered

# ── Palette ──────────────────────────────────────────────────────────────────
# Walls — deep indigo/purple tones with dithering
WALL_DARK = (30, 22, 65)
WALL_MID = (42, 32, 85)
WALL_LIGHT = (55, 42, 100)
WALL_ACCENT = (48, 38, 95)

# Floor — warm brown wood
FLOOR_MAIN = (90, 55, 30)
FLOOR_LIGHT = (110, 70, 40)
FLOOR_DARK = (65, 38, 18)
FLOOR_LINE = (55, 32, 15)

# Furniture
COUCH_MAIN = (100, 50, 110)
COUCH_LIGHT = (125, 65, 135)
COUCH_DARK = (70, 35, 80)
COUCH_CUSHION = (85, 42, 95)

WOOD_MAIN = (100, 65, 35)
WOOD_LIGHT = (120, 80, 45)
WOOD_DARK = (70, 42, 20)
WOOD_SHADOW = (50, 30, 12)

LAMP_SHADE = (200, 190, 90)
LAMP_GLOW = (240, 230, 130)
LAMP_POLE = (150, 140, 60)

DOOR_MAIN = (100, 60, 30)
DOOR_LIGHT = (120, 75, 40)
DOOR_DARK = (70, 40, 18)
DOOR_FRAME = (80, 50, 25)

STAIR_MAIN = (75, 50, 30)
STAIR_LIGHT = (95, 65, 40)
STAIR_DARK = (55, 35, 18)
STAIR_RAIL = (85, 60, 35)
STAIR_RAIL_HI = (110, 80, 50)

CARPET_MAIN = (120, 35, 30)
CARPET_DARK = (90, 25, 20)

# CRT/Monitor
MON_CASE = (110, 110, 120)
MON_DARK = (75, 75, 85)
MON_BEZEL = (85, 85, 95)
SCREEN_BG = (5, 8, 18)
GREEN_LED = (60, 220, 60)
RED_LED = (220, 50, 50)
CRT_BEZEL = (70, 70, 80)

# Desk
DESK_TOP = (120, 80, 45)
DESK_FRONT = (95, 60, 32)
DESK_DARK = (70, 42, 20)

# Bookshelf
SHELF_WOOD = (85, 55, 28)
SHELF_DARK = (60, 38, 15)
BOOK_COLORS = [
    (180, 45, 45), (45, 110, 170), (45, 140, 45),
    (170, 160, 45), (160, 80, 45), (100, 50, 140),
    (45, 130, 130), (170, 100, 60),
]

# PCB/Electronics
PCB_GREEN = (25, 75, 28)
PCB_DARK = (18, 55, 20)
PCB_LIGHT = (35, 95, 38)
COPPER = (185, 135, 55)
COPPER_DARK = (140, 100, 40)
SOLDER = (170, 170, 180)
IC_BLACK = (18, 18, 22)
IC_LABEL = (35, 35, 40)
WIRE_RED = (180, 40, 35)
WIRE_YELLOW = (200, 180, 50)
WIRE_BLUE = (45, 80, 170)
CAP_BLUE = (40, 65, 170)
CAP_BROWN = (140, 95, 40)

# Switch panel
PANEL_MAIN = (175, 170, 155)
PANEL_LIGHT = (195, 190, 175)
PANEL_DARK = (140, 135, 120)
PANEL_LINE = (155, 150, 135)
SWITCH_BODY = (60, 60, 65)
SWITCH_HI = (85, 85, 92)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SKY = (50, 75, 110)


def _dither_rect(surface, x, y, w, h, c1, c2, pattern="checker"):
    """Fill a rect with dithered pattern between two colors."""
    for py in range(y, y + h):
        for px in range(x, x + w):
            if 0 <= px < surface.get_width() and 0 <= py < surface.get_height():
                if pattern == "checker":
                    use_c1 = (px + py) % 2 == 0
                elif pattern == "horizontal":
                    use_c1 = py % 2 == 0
                elif pattern == "vertical":
                    use_c1 = px % 2 == 0
                else:
                    use_c1 = (px + py) % 2 == 0
                surface.set_at((px, py), c1 if use_c1 else c2)


def _dither_gradient_v(surface, x, y, w, h, c_top, c_bot):
    """Vertical gradient using dithering (no smooth interpolation)."""
    for py in range(y, y + h):
        if h <= 1:
            t = 0
        else:
            t = (py - y) / (h - 1)
        # Two-level dither
        r1 = int(c_top[0] + (c_bot[0] - c_top[0]) * t)
        g1 = int(c_top[1] + (c_bot[1] - c_top[1]) * t)
        b1 = int(c_top[2] + (c_bot[2] - c_top[2]) * t)
        for px in range(x, x + w):
            if 0 <= px < surface.get_width() and 0 <= py < surface.get_height():
                # Add subtle noise
                offset = ((px * 7 + py * 13) % 5) - 2
                r = max(0, min(255, r1 + offset))
                g = max(0, min(255, g1 + offset))
                b = max(0, min(255, b1 + offset))
                surface.set_at((px, py), (r, g, b))


def draw_living_room(surface):
    """Scene 1: Living room with stairs, couch, lamp, picture, door."""
    W = 320
    SH = 136  # scene height

    # Wall background — dithered gradient for depth
    _dither_gradient_v(surface, 0, 0, W, 100, WALL_DARK, WALL_MID)
    # Wall band (lighter accent strip like in Maniac Mansion)
    _dither_rect(surface, 0, 40, W, 3, WALL_LIGHT, WALL_ACCENT)

    # Baseboard
    pygame.draw.rect(surface, WOOD_DARK, (0, 98, W, 4))
    pygame.draw.rect(surface, WOOD_LIGHT, (0, 98, W, 1))

    # Floor with wood planks
    for y in range(102, SH):
        for x in range(W):
            # Wood grain pattern
            grain = ((x * 3 + y * 7) % 11)
            if grain < 3:
                surface.set_at((x, y), FLOOR_DARK)
            elif grain < 8:
                surface.set_at((x, y), FLOOR_MAIN)
            else:
                surface.set_at((x, y), FLOOR_LIGHT)
    # Plank lines
    for y in range(104, SH, 5):
        pygame.draw.line(surface, FLOOR_LINE, (0, y), (W - 1, y))

    # ── Staircase (left side, going up-left) ──
    stair_count = 9
    for i in range(stair_count):
        sx = 8 + i * 6
        sy = 96 - i * 10
        sw = 58 - i * 3

        # Step tread
        pygame.draw.rect(surface, STAIR_LIGHT, (sx, sy, sw, 3))
        pygame.draw.rect(surface, STAIR_MAIN, (sx, sy + 3, sw, 7))
        # Step front face shadow
        pygame.draw.rect(surface, STAIR_DARK, (sx, sy + 8, sw, 2))

    # Railing — diagonal line with balusters
    rail_x1, rail_y1 = 62, 96
    rail_x2, rail_y2 = 48, 8
    pygame.draw.line(surface, STAIR_RAIL_HI, (rail_x1, rail_y1), (rail_x2, rail_y2), 1)
    pygame.draw.line(surface, STAIR_RAIL, (rail_x1 + 1, rail_y1), (rail_x2 + 1, rail_y2), 1)
    # Balusters
    for i in range(stair_count):
        bx = 60 - i * 2
        by_top = 95 - i * 10
        by_bot = by_top + 8
        pygame.draw.line(surface, STAIR_RAIL, (bx, by_top - 3), (bx, by_bot))

    # Carpet under stairs
    _dither_rect(surface, 0, 102, 55, SH - 102, CARPET_MAIN, CARPET_DARK, "checker")

    # ── Iceland picture on wall ──
    fx, fy = 135, 18
    pygame.draw.rect(surface, WOOD_LIGHT, (fx - 1, fy - 1, 34, 28))
    pygame.draw.rect(surface, WOOD_DARK, (fx, fy, 32, 26))
    # Iceland landscape: sky, mountains, water
    pygame.draw.rect(surface, (70, 100, 160), (fx + 2, fy + 2, 28, 8))   # sky
    # Mountain peaks
    for mx, mh in [(fx + 6, 5), (fx + 14, 7), (fx + 22, 4)]:
        for dy in range(mh):
            hw = mh - dy
            for ddx in range(-hw, hw + 1):
                px = mx + ddx
                py = fy + 10 - dy
                if fx + 2 <= px < fx + 30 and fy + 2 <= py < fy + 26:
                    surface.set_at((px, py), (55, 55, 70))
    # Snow caps
    surface.set_at((fx + 14, fy + 3), WHITE)
    surface.set_at((fx + 13, fy + 4), (220, 220, 230))
    surface.set_at((fx + 15, fy + 4), (220, 220, 230))
    surface.set_at((fx + 6, fy + 5), (220, 220, 230))
    # Water reflection
    pygame.draw.rect(surface, (50, 80, 130), (fx + 2, fy + 14, 28, 6))
    # Green aurora hint in sky
    for ax in range(fx + 4, fx + 28, 3):
        surface.set_at((ax, fy + 3), (50, 180, 80))
        surface.set_at((ax + 1, fy + 4), (40, 150, 70))

    # ── Lamp on side table ──
    lx, ly = 182, 52
    # Table
    pygame.draw.rect(surface, WOOD_LIGHT, (175, 88, 22, 3))
    pygame.draw.rect(surface, WOOD_MAIN, (175, 91, 22, 2))
    pygame.draw.rect(surface, WOOD_DARK, (178, 93, 4, 9))
    pygame.draw.rect(surface, WOOD_DARK, (192, 93, 4, 9))
    # Lamp shade (trapezoid shape)
    for row in range(8):
        half_w = 4 + row
        shade_y = ly + row
        for px in range(lx - half_w, lx + half_w + 1):
            # Dithered glow
            if (px + shade_y) % 2 == 0:
                surface.set_at((px, shade_y), LAMP_SHADE)
            else:
                surface.set_at((px, shade_y), LAMP_GLOW)
    # Pole
    pygame.draw.line(surface, LAMP_POLE, (lx, ly + 8), (lx, 88), 1)
    # Warm glow on surrounding wall
    for dy in range(-14, 15):
        for dx in range(-14, 15):
            dist_sq = dx * dx + dy * dy
            if dist_sq < 180:
                px = lx + dx
                py = ly + 4 + dy
                if 0 <= px < W and 0 <= py < 100:
                    c = surface.get_at((px, py))
                    intensity = max(0, 18 - dist_sq // 10)
                    nr = min(255, c[0] + intensity * 2)
                    ng = min(255, c[1] + intensity)
                    nb = min(255, c[2])
                    surface.set_at((px, py), (nr, ng, nb))

    # ── Couch ──
    cx, cy = 205, 78
    cw, ch = 72, 24
    # Back rest
    pygame.draw.rect(surface, COUCH_DARK, (cx, cy, cw, 12))
    _dither_rect(surface, cx + 2, cy + 2, cw - 4, 8, COUCH_MAIN, COUCH_DARK, "horizontal")
    # Seat
    pygame.draw.rect(surface, COUCH_MAIN, (cx, cy + 12, cw, 10))
    pygame.draw.rect(surface, COUCH_LIGHT, (cx + 2, cy + 13, cw - 4, 2))
    # Cushion dividers
    pygame.draw.line(surface, COUCH_DARK, (cx + 24, cy + 13), (cx + 24, cy + 20))
    pygame.draw.line(surface, COUCH_DARK, (cx + 48, cy + 13), (cx + 48, cy + 20))
    # Armrests
    pygame.draw.rect(surface, COUCH_DARK, (cx - 4, cy + 6, 6, 18))
    pygame.draw.rect(surface, COUCH_MAIN, (cx - 3, cy + 7, 4, 4))
    pygame.draw.rect(surface, COUCH_DARK, (cx + cw - 2, cy + 6, 6, 18))
    pygame.draw.rect(surface, COUCH_MAIN, (cx + cw - 1, cy + 7, 4, 4))
    # Shadow under couch
    _dither_rect(surface, cx - 2, cy + ch, cw + 4, 2, FLOOR_DARK, FLOOR_LINE)

    # ── Door on right ──
    dx, dy = 288, 28
    dw, dh = 26, 72
    # Door frame
    pygame.draw.rect(surface, DOOR_FRAME, (dx - 2, dy - 2, dw + 4, dh + 4))
    # Door panels
    pygame.draw.rect(surface, DOOR_MAIN, (dx, dy, dw, dh))
    # Panel insets
    pygame.draw.rect(surface, DOOR_DARK, (dx + 3, dy + 4, 20, 14))
    pygame.draw.rect(surface, DOOR_LIGHT, (dx + 4, dy + 5, 18, 12))
    pygame.draw.rect(surface, DOOR_DARK, (dx + 3, dy + 24, 20, 20))
    pygame.draw.rect(surface, DOOR_LIGHT, (dx + 4, dy + 25, 18, 18))
    # Door knob
    pygame.draw.circle(surface, (200, 180, 80), (dx + 21, dy + 38), 2)
    surface.set_at((dx + 22, dy + 37), (230, 210, 110))
    # Door frame shadow
    pygame.draw.rect(surface, WOOD_SHADOW, (dx - 2, dy - 2, 2, dh + 4))

    # ── Kubernetes logo carpet on floor ──
    # Simplified helm/ship's wheel shape at ~24x24 px
    kx, ky = 120, 108
    kr = 10
    # Carpet background (blue circle)
    for dy in range(-kr - 2, kr + 3):
        for ddx in range(-kr - 2, kr + 3):
            if ddx * ddx + dy * dy <= (kr + 2) * (kr + 2):
                px, py = kx + ddx, ky + dy
                if 0 <= px < W and 102 <= py < SH:
                    surface.set_at((px, py), (40, 60, 140))
    # White helm circle
    for angle_step in range(60):
        a = angle_step * math.pi * 2 / 60
        px = int(kx + kr * math.cos(a))
        py = int(ky + kr * math.sin(a))
        if 0 <= px < W and 0 <= py < SH:
            surface.set_at((px, py), (180, 200, 230))
    # Spokes (7 spokes like Kubernetes logo)
    for spoke in range(7):
        a = spoke * math.pi * 2 / 7
        for r in range(3, kr):
            px = int(kx + r * math.cos(a))
            py = int(ky + r * math.sin(a))
            if 0 <= px < W and 102 <= py < SH:
                surface.set_at((px, py), (180, 200, 230))
    # Center dot
    pygame.draw.circle(surface, (180, 200, 230), (kx, ky), 2)


def draw_computer_room(surface):
    """Scene 2: Computer room with desk, CRT, keyboard, mic, bookshelf."""
    W = 320
    SH = 136

    # Walls
    _dither_gradient_v(surface, 0, 0, W, 100, WALL_DARK, WALL_MID)
    _dither_rect(surface, 0, 38, W, 2, WALL_LIGHT, WALL_ACCENT)

    # Baseboard
    pygame.draw.rect(surface, WOOD_DARK, (0, 98, W, 4))
    pygame.draw.rect(surface, WOOD_LIGHT, (0, 98, W, 1))

    # Floor
    for y in range(102, SH):
        for x in range(W):
            grain = ((x * 3 + y * 7) % 11)
            if grain < 3:
                surface.set_at((x, y), FLOOR_DARK)
            elif grain < 8:
                surface.set_at((x, y), FLOOR_MAIN)
            else:
                surface.set_at((x, y), FLOOR_LIGHT)
    for y in range(104, SH, 5):
        pygame.draw.line(surface, FLOOR_LINE, (0, y), (W - 1, y))

    # ── Bookshelf on left ──
    bx, by = 8, 10
    bw, bh = 62, 88
    pygame.draw.rect(surface, SHELF_WOOD, (bx, by, bw, bh))
    pygame.draw.rect(surface, SHELF_DARK, (bx, by, bw, 2))
    pygame.draw.rect(surface, SHELF_DARK, (bx, by, 2, bh))
    # Shelves (4 levels)
    shelf_ys = [by + 2, by + 24, by + 46, by + 68]
    for sy in shelf_ys:
        pygame.draw.rect(surface, SHELF_DARK, (bx, sy, bw, 3))
        pygame.draw.rect(surface, WOOD_LIGHT, (bx + 1, sy, bw - 2, 1))
    # Books on each shelf
    for si, sy in enumerate(shelf_ys):
        book_x = bx + 3
        for bi in range(8):
            bk_w = 4 + (bi * 3 + si * 5) % 4
            bk_h = 16 + (bi * 7 + si * 3) % 5
            bk_color = BOOK_COLORS[(bi + si * 3) % len(BOOK_COLORS)]
            bk_y = sy + 3
            pygame.draw.rect(surface, bk_color, (book_x, bk_y + (20 - bk_h), bk_w, bk_h))
            # Spine highlight
            surface.set_at((book_x, bk_y + (20 - bk_h)), (
                min(255, bk_color[0] + 40),
                min(255, bk_color[1] + 40),
                min(255, bk_color[2] + 40),
            ))
            book_x += bk_w + 1
            if book_x > bx + bw - 6:
                break

    # ── Desk ──
    dx, dy = 95, 74
    dw = 170
    # Desktop surface
    pygame.draw.rect(surface, DESK_TOP, (dx, dy, dw, 4))
    pygame.draw.rect(surface, WOOD_LIGHT, (dx, dy, dw, 1))
    # Desk front panel
    pygame.draw.rect(surface, DESK_FRONT, (dx, dy + 4, dw, 20))
    pygame.draw.rect(surface, DESK_DARK, (dx, dy + 4, dw, 2))
    # Legs
    pygame.draw.rect(surface, DESK_DARK, (dx + 4, dy + 24, 6, 12))
    pygame.draw.rect(surface, DESK_DARK, (dx + dw - 10, dy + 24, 6, 12))
    # Drawer handle
    pygame.draw.rect(surface, (140, 120, 70), (dx + 70, dy + 10, 30, 2))

    # ── CRT Monitor ──
    mx, my = 148, 22
    mw, mh = 65, 52
    # Outer casing
    pygame.draw.rect(surface, MON_CASE, (mx, my, mw, mh))
    pygame.draw.rect(surface, MON_DARK, (mx, my, mw, 2))
    pygame.draw.rect(surface, MON_DARK, (mx, my, 2, mh))
    # Screen bezel
    pygame.draw.rect(surface, MON_BEZEL, (mx + 4, my + 4, mw - 8, mh - 12))
    # Screen
    pygame.draw.rect(surface, SCREEN_BG, (mx + 6, my + 6, mw - 12, mh - 16))
    # Scanlines on screen
    for sy in range(my + 6, my + mh - 10, 2):
        pygame.draw.line(surface, (10, 14, 28), (mx + 6, sy), (mx + mw - 7, sy))
    # Monitor stand
    pygame.draw.rect(surface, MON_DARK, (mx + 20, my + mh, 25, 4))
    pygame.draw.rect(surface, MON_CASE, (mx + 15, my + mh + 3, 35, 2))
    # Power LED
    pygame.draw.rect(surface, GREEN_LED, (mx + mw - 10, my + mh - 6, 3, 2))
    # Monitor label
    surface.set_at((mx + 8, my + mh - 6), (120, 120, 130))
    surface.set_at((mx + 10, my + mh - 6), (120, 120, 130))

    # ── Keyboard ──
    kx, ky = 155, 78
    pygame.draw.rect(surface, (85, 85, 95), (kx, ky, 50, 8))
    pygame.draw.rect(surface, (95, 95, 105), (kx + 1, ky + 1, 48, 1))
    for row in range(3):
        for col in range(11):
            pygame.draw.rect(surface, (105, 105, 115),
                             (kx + 2 + col * 4, ky + 2 + row * 2, 3, 1))

    # ── Microphone on right side ──
    mic_x = 245
    # Mic stand
    pygame.draw.line(surface, (55, 55, 60), (mic_x, 50), (mic_x, 76), 1)
    pygame.draw.line(surface, (65, 65, 70), (mic_x + 1, 50), (mic_x + 1, 76), 1)
    # Mic head (round)
    pygame.draw.circle(surface, (90, 90, 100), (mic_x, 46), 5)
    pygame.draw.circle(surface, (110, 110, 120), (mic_x, 46), 3)
    # Mesh dots
    for dots in [(mic_x - 1, 45), (mic_x + 1, 45), (mic_x, 44), (mic_x, 47)]:
        surface.set_at(dots, (70, 70, 80))
    # Base
    pygame.draw.rect(surface, (55, 55, 60), (mic_x - 6, 76, 14, 3))

    # ── Chair ──
    chair_x = 165
    # Seat
    pygame.draw.rect(surface, (65, 42, 25), (chair_x - 5, 95, 42, 5))
    pygame.draw.rect(surface, (80, 55, 32), (chair_x - 3, 95, 38, 2))
    # Back
    pygame.draw.rect(surface, (65, 42, 25), (chair_x - 2, 78, 36, 17))
    _dither_rect(surface, chair_x, 80, 32, 13, (75, 50, 30), (65, 42, 25))
    # Post
    pygame.draw.rect(surface, (50, 32, 18), (chair_x + 14, 100, 4, 10))
    # Wheels
    pygame.draw.rect(surface, (40, 40, 45), (chair_x + 2, 110, 28, 3))
    for wx in [chair_x + 4, chair_x + 15, chair_x + 26]:
        pygame.draw.circle(surface, (35, 35, 40), (wx, 113), 2)

    # ── Window on right wall ──
    wx, wy = 282, 14
    pygame.draw.rect(surface, WOOD_MAIN, (wx - 2, wy - 2, 32, 42))
    pygame.draw.rect(surface, WINDOW_SKY, (wx, wy, 28, 38))
    pygame.draw.line(surface, WOOD_MAIN, (wx + 14, wy), (wx + 14, wy + 38), 2)
    pygame.draw.line(surface, WOOD_MAIN, (wx, wy + 19), (wx + 28, wy + 19), 2)
    # Stars
    for star_pos in [(wx + 5, wy + 5), (wx + 22, wy + 8), (wx + 10, wy + 15)]:
        surface.set_at(star_pos, (200, 200, 220))

    # ── Lambda calculus picture on wall (above bookshelf) ──
    lx, ly = 85, 14
    pygame.draw.rect(surface, WOOD_LIGHT, (lx - 1, ly - 1, 22, 20))
    pygame.draw.rect(surface, (20, 20, 40), (lx, ly, 20, 18))
    # Lambda (λ) symbol in white — pixel art
    lam_pixels = [
        (3, 2), (4, 2),
        (4, 3), (5, 3),
        (5, 4), (6, 4),
        (6, 5), (7, 5),
        (7, 6), (8, 6),
        (8, 7), (9, 7), (10, 7),
        (7, 7), (6, 8), (11, 8),
        (5, 9), (12, 9),
        (4, 10), (13, 10),
        (3, 11), (14, 11),
        (2, 12), (15, 12),
    ]
    for px, py in lam_pixels:
        surface.set_at((lx + px, ly + py + 2), (200, 200, 240))

    # ── Model plane on a small keyboard stand ──
    # Stand (small shelf/bracket on right side of desk)
    stand_x, stand_y = 270, 58
    pygame.draw.rect(surface, (90, 90, 100), (stand_x, stand_y, 20, 3))  # shelf
    pygame.draw.rect(surface, (70, 70, 78), (stand_x + 8, stand_y + 3, 4, 14))  # post
    pygame.draw.rect(surface, (80, 80, 88), (stand_x + 4, stand_y + 17, 12, 2))  # base
    # Model plane on top
    px, py = stand_x + 10, stand_y - 2
    # Wings
    pygame.draw.line(surface, (180, 180, 200), (px - 8, py), (px + 8, py))
    # Fuselage
    pygame.draw.line(surface, (200, 200, 220), (px, py - 3), (px, py + 3))
    pygame.draw.line(surface, (190, 190, 210), (px + 1, py - 2), (px + 1, py + 2))
    # Tail
    pygame.draw.line(surface, (180, 180, 200), (px - 3, py + 3), (px + 3, py + 3))
    # Cockpit
    surface.set_at((px, py - 3), (80, 130, 200))


def draw_switch_closeup(surface):
    """Scene 3: Close-up of computer power switch — off state."""
    W = 320
    SH = 136

    # Beige computer case panel with texture
    for y in range(SH):
        for x in range(W):
            noise = ((x * 7 + y * 13) % 5) - 2
            r = max(0, min(255, PANEL_MAIN[0] + noise))
            g = max(0, min(255, PANEL_MAIN[1] + noise))
            b = max(0, min(255, PANEL_MAIN[2] + noise))
            surface.set_at((x, y), (r, g, b))

    # Horizontal panel lines (like a PC case)
    for y in range(8, SH, 12):
        pygame.draw.line(surface, PANEL_LINE, (0, y), (W - 1, y))
        pygame.draw.line(surface, PANEL_LIGHT, (0, y + 1), (W - 1, y + 1))

    # Ventilation slots on left
    for i in range(8):
        vy = 16 + i * 14
        pygame.draw.rect(surface, PANEL_DARK, (18, vy, 55, 5))
        pygame.draw.rect(surface, (100, 95, 80), (20, vy + 1, 51, 3))

    # Switch recess (indented area)
    rx, ry = 125, 18
    rw, rh = 70, 100
    pygame.draw.rect(surface, PANEL_DARK, (rx, ry, rw, rh))
    pygame.draw.rect(surface, PANEL_LIGHT, (rx + 1, ry + rh - 1, rw - 1, 1))
    pygame.draw.rect(surface, PANEL_LIGHT, (rx + rw - 1, ry + 1, 1, rh - 1))
    # Inner surface
    pygame.draw.rect(surface, (150, 145, 130), (rx + 3, ry + 3, rw - 6, rh - 6))

    # "ON" label
    draw_text(surface, rx + 22, ry + 8, "ON", (60, 55, 40))

    # OFF label below switch
    draw_text(surface, rx + 20, ry + rh - 16, "OFF", (60, 55, 40))

    # Switch track
    sx, sy = rx + 18, ry + 25
    sw, sh = 34, 55
    pygame.draw.rect(surface, SWITCH_BODY, (sx, sy, sw, sh))
    pygame.draw.rect(surface, (45, 45, 50), (sx, sy, sw, 2))
    pygame.draw.rect(surface, (75, 75, 82), (sx, sy + sh - 2, sw, 2))

    # Switch handle (DOWN = OFF position)
    pygame.draw.rect(surface, (100, 100, 110), (sx + 4, sy + 28, sw - 8, 24))
    pygame.draw.rect(surface, SWITCH_HI, (sx + 4, sy + 28, sw - 8, 3))
    pygame.draw.rect(surface, (70, 70, 78), (sx + 4, sy + 49, sw - 8, 3))
    # Grip lines
    for gy in range(sy + 34, sy + 48, 3):
        pygame.draw.line(surface, (80, 80, 88), (sx + 6, gy), (sx + sw - 7, gy))

    # LED indicator (off — dark green)
    led_x, led_y = 220, 65
    pygame.draw.circle(surface, (25, 50, 25), (led_x, led_y), 5)
    pygame.draw.circle(surface, (20, 38, 20), (led_x, led_y), 3)
    draw_text(surface, led_x - 10, led_y + 8, "PWR", (80, 75, 60))


def draw_switch_on(surface):
    """Scene 3 variant: switch flipped ON with green LED."""
    # Draw base first
    draw_switch_closeup(surface)

    # Override switch position to UP
    rx, ry = 125, 18
    sx, sy = rx + 18, ry + 25
    sw, sh = 34, 55
    pygame.draw.rect(surface, SWITCH_BODY, (sx, sy, sw, sh))
    pygame.draw.rect(surface, (45, 45, 50), (sx, sy, sw, 2))
    # Handle UP
    pygame.draw.rect(surface, (110, 110, 120), (sx + 4, sy + 3, sw - 8, 24))
    pygame.draw.rect(surface, SWITCH_HI, (sx + 4, sy + 3, sw - 8, 3))
    pygame.draw.rect(surface, (75, 75, 82), (sx + 4, sy + 24, sw - 8, 3))
    for gy in range(sy + 9, sy + 23, 3):
        pygame.draw.line(surface, (85, 85, 95), (sx + 6, gy), (sx + sw - 7, gy))

    # Green LED (on) with glow
    led_x, led_y = 220, 65
    # Glow
    for dy in range(-10, 11):
        for dx in range(-10, 11):
            dist_sq = dx * dx + dy * dy
            if dist_sq < 90:
                px, py = led_x + dx, led_y + dy
                if 0 <= px < 320 and 0 <= py < 136:
                    c = surface.get_at((px, py))
                    intensity = max(0, 25 - dist_sq // 3)
                    ng = min(255, c[1] + intensity * 3)
                    surface.set_at((px, py), (c[0], ng, c[2]))
    pygame.draw.circle(surface, GREEN_LED, (led_x, led_y), 5)
    pygame.draw.circle(surface, (100, 255, 100), (led_x, led_y), 3)
    surface.set_at((led_x - 1, led_y - 1), (180, 255, 180))


def _draw_crt_frame(surface, text_lines=None, cursor_visible=True, scanlines=True):
    """Shared CRT monitor full-screen view for DOS/flight/record scenes."""
    W = 320
    SH = 136

    # Monitor outer casing
    pygame.draw.rect(surface, MON_DARK, (0, 0, W, SH))
    # Bezel
    pygame.draw.rect(surface, CRT_BEZEL, (8, 4, W - 16, SH - 8))
    # Screen area
    screen_rect = pygame.Rect(14, 10, W - 28, SH - 20)
    pygame.draw.rect(surface, SCREEN_BG, screen_rect)

    # CRT curvature hint: slightly lighter edges
    for y in range(screen_rect.top, screen_rect.bottom):
        for edge_x in [screen_rect.left, screen_rect.left + 1,
                        screen_rect.right - 1, screen_rect.right - 2]:
            if 0 <= edge_x < W:
                surface.set_at((edge_x, y), (8, 12, 25))

    # Scanlines
    if scanlines:
        for y in range(screen_rect.top, screen_rect.bottom, 2):
            pygame.draw.line(surface, (8, 12, 25),
                             (screen_rect.left, y), (screen_rect.right - 1, y))

    # Monitor brand badge at bottom
    pygame.draw.rect(surface, (50, 50, 55), (130, SH - 8, 60, 6))
    draw_text_centered(surface, 160, SH - 7, "VGA", (80, 80, 85))

    return screen_rect


def draw_dos_screen(surface, text_lines, cursor_visible=True):
    """Scene 4: MS-DOS boot screen."""
    screen_rect = _draw_crt_frame(surface)

    ty = screen_rect.top + 4
    for line in text_lines:
        if line.startswith("MS-DOS"):
            # Colorful MS-DOS logo — each letter a different color
            colors = [
                (255, 50, 50), (255, 150, 50), (255, 255, 50),
                (50, 255, 50), (50, 150, 255), (150, 50, 255),
            ]
            tx = screen_rect.left + 4
            for i, ch in enumerate(line):
                draw_text(surface, tx, ty, ch, colors[i % len(colors)])
                tx += 6
        elif line == "":
            pass
        else:
            draw_text(surface, screen_rect.left + 4, ty, line, (200, 200, 200))
        ty += 10

    # Blinking cursor block
    if cursor_visible and text_lines:
        last = text_lines[-1]
        cx = screen_rect.left + 4 + len(last) * 6
        cy = ty - 10
        pygame.draw.rect(surface, (200, 200, 200), (cx, cy, 5, 7))


def draw_flight_sim(surface, scroll_y=0):
    """Scene 5: Top-down retro flight sim inside CRT."""
    screen_rect = _draw_crt_frame(surface, scanlines=False)

    # Game surface
    gw = screen_rect.width
    gh = screen_rect.height
    game = pygame.Surface((gw, gh))

    # Deep blue water
    for y in range(gh):
        for x in range(gw):
            wy = (y + int(scroll_y)) % 200
            wave = ((x + wy * 3) % 12)
            if wave < 2:
                game.set_at((x, y), (25, 65, 150))
            elif wave < 4:
                game.set_at((x, y), (20, 55, 135))
            else:
                game.set_at((x, y), (18, 50, 125))

    # Islands
    islands = [
        (50, 30, 28, 16), (160, 70, 38, 20), (240, 15, 22, 14),
        (90, 120, 32, 18), (30, 170, 24, 14), (190, 160, 30, 16),
        (130, 220, 35, 18), (270, 250, 22, 12),
    ]
    for ix, iy, iw, ih in islands:
        draw_y = (iy - int(scroll_y)) % 300 - 80
        if -ih <= draw_y <= gh:
            # Island base
            pygame.draw.ellipse(game, (60, 140, 45), (ix - iw // 2, draw_y, iw, ih))
            # Beach ring
            pygame.draw.ellipse(game, (180, 165, 95), (ix - iw // 2, draw_y, iw, ih), 1)
            # Center vegetation
            cix = ix - iw // 2 + iw // 3
            ciy = draw_y + ih // 3
            if ih > 14:
                pygame.draw.rect(game, (40, 100, 35), (cix, ciy, iw // 3, ih // 3))

    # Plane sprite (facing up)
    px, py = gw // 2, gh // 2 - 5
    # Shadow
    pygame.draw.ellipse(game, (15, 40, 100), (px - 5, py + 8, 10, 4))
    # Wings
    pygame.draw.rect(game, (190, 190, 200), (px - 12, py - 1, 24, 3))
    # Fuselage
    pygame.draw.rect(game, (210, 210, 220), (px - 2, py - 8, 4, 14))
    # Tail
    pygame.draw.rect(game, (190, 190, 200), (px - 5, py + 4, 10, 2))
    # Cockpit
    pygame.draw.rect(game, (80, 140, 200), (px - 1, py - 7, 2, 3))
    # Engine glow
    game.set_at((px, py + 6), (255, 200, 50))
    game.set_at((px - 1, py + 6), (255, 150, 30))

    surface.blit(game, screen_rect.topleft)

    # HUD
    draw_text(surface, screen_rect.left + 4, screen_rect.top + 2,
              "SCORE: 1337", (200, 200, 50))
    draw_text(surface, screen_rect.right - 60, screen_rect.top + 2,
              "ALT: 5000", (200, 200, 50))


def draw_rec_screen(surface, rec_blink=True):
    """Scene 6 ending: Recording screen."""
    screen_rect = _draw_crt_frame(surface)

    # "Recording..." text centered
    draw_text_centered(surface, 160, screen_rect.top + 30,
                       "Recording...", (200, 200, 200))

    # Large REC indicator
    if rec_blink:
        pygame.draw.circle(surface, (255, 30, 30),
                           (screen_rect.centerx - 20, screen_rect.top + 55), 6)
    draw_text(surface, screen_rect.centerx - 8, screen_rect.top + 50,
              "REC", (255, 30, 30))

    # VU meter bars
    bar_x = screen_rect.left + 60
    for i in range(10):
        bh = 4 + ((i * 7 + 3) % 18)
        if i < 6:
            color = (50, 200, 50)
        elif i < 8:
            color = (200, 200, 50)
        else:
            color = (200, 50, 50)
        pygame.draw.rect(surface, color,
                         (bar_x + i * 18, screen_rect.bottom - 20 - bh, 12, bh))
        pygame.draw.rect(surface, (0, 0, 0),
                         (bar_x + i * 18, screen_rect.bottom - 20 - bh, 12, bh), 1)


def draw_crt_inside(surface, stefan_wave_frame=None):
    """Scene 7: Inside-CRT perspective — circuit boards around, Stefan on screen."""
    W = 320
    SH = 136

    surface.fill(BLACK)

    # PCBs on all sides
    _draw_pcb_detailed(surface, 0, 0, 65, SH)        # left
    _draw_pcb_detailed(surface, 255, 0, 65, SH)       # right
    _draw_pcb_detailed(surface, 65, 110, 190, 26)      # bottom

    # CRT screen frame (rounded effect via corners)
    frame_rect = pygame.Rect(68, 5, 184, 103)
    pygame.draw.rect(surface, CRT_BEZEL, frame_rect)
    # Round corners by filling with black
    for corner in [(68, 5), (251, 5), (68, 107), (251, 107)]:
        pygame.draw.rect(surface, BLACK, (corner[0], corner[1], 3, 3))
    # Inner screen
    inner = frame_rect.inflate(-8, -8)
    pygame.draw.rect(surface, (40, 40, 75), inner)

    # Stefan waving inside the screen
    if stefan_wave_frame:
        big = pygame.transform.scale(stefan_wave_frame, (56, 100))
        sx = inner.centerx - 28
        sy = inner.bottom - 102
        surface.blit(big, (sx, sy))

    # YouTube-style overlay
    # Timecode bottom-right
    draw_text(surface, inner.right - 72, inner.bottom - 10,
              "0:00 / 30:03", WHITE)
    # REC dot top-left
    pygame.draw.circle(surface, (255, 30, 30),
                       (inner.left + 8, inner.bottom - 7), 3)
    draw_text(surface, inner.left + 14, inner.bottom - 10, "REC", (255, 30, 30))

    # Wires connecting PCB to screen
    wire_colors = [COPPER, WIRE_RED, WIRE_YELLOW, WIRE_BLUE, COPPER_DARK]
    for i, y in enumerate(range(15, 100, 12)):
        color = wire_colors[i % len(wire_colors)]
        # Left side wires
        pygame.draw.line(surface, color, (63, y), (70, y + 2), 1)
        pygame.draw.line(surface, color, (62, y + 1), (69, y + 3), 1)
        # Right side wires
        pygame.draw.line(surface, color, (257, y), (250, y + 2), 1)
        pygame.draw.line(surface, color, (258, y + 1), (251, y + 3), 1)


def _draw_pcb_detailed(surface, x, y, w, h):
    """Draw a detailed circuit board section."""
    # Base green PCB
    for py in range(y, y + h):
        for px in range(x, x + w):
            if 0 <= px < 320 and 0 <= py < 136:
                noise = ((px * 7 + py * 11) % 7) - 3
                r = max(0, min(255, PCB_GREEN[0] + noise))
                g = max(0, min(255, PCB_GREEN[1] + noise))
                b = max(0, min(255, PCB_GREEN[2] + noise))
                surface.set_at((px, py), (r, g, b))

    # Copper traces (horizontal)
    for i in range(0, h, 5):
        trace_y = y + i + (i * 7) % 3
        if trace_y < y + h:
            trace_x = x + (i * 13) % (w - 20)
            trace_len = 8 + (i * 5) % 15
            pygame.draw.line(surface, COPPER,
                             (trace_x, trace_y),
                             (min(x + w - 1, trace_x + trace_len), trace_y))

    # Vertical traces
    for i in range(0, w, 7):
        trace_x = x + i + (i * 11) % 3
        if trace_x < x + w:
            trace_y = y + (i * 7) % (h - 15)
            trace_len = 6 + (i * 3) % 12
            pygame.draw.line(surface, COPPER_DARK,
                             (trace_x, trace_y),
                             (trace_x, min(y + h - 1, trace_y + trace_len)))

    # IC chips (large black rectangles with pin rows)
    chip_positions = []
    for i in range(3):
        cx = x + 6 + (i * 19) % (w - 16)
        cy = y + 8 + (i * 31) % (h - 18)
        if cx + 14 < x + w and cy + 10 < y + h:
            chip_positions.append((cx, cy))
            pygame.draw.rect(surface, IC_BLACK, (cx, cy, 14, 10))
            pygame.draw.rect(surface, IC_LABEL, (cx + 2, cy + 2, 10, 6))
            # Orientation dot
            surface.set_at((cx + 2, cy + 2), (50, 50, 55))
            # Pins on top and bottom
            for p in range(5):
                pin_x = cx + 2 + p * 2
                surface.set_at((pin_x, cy - 1), SOLDER)
                surface.set_at((pin_x, cy + 10), SOLDER)

    # Solder points (via holes)
    for i in range(8):
        sx = x + 3 + (i * 7) % (w - 6)
        sy = y + 3 + (i * 11) % (h - 6)
        pygame.draw.circle(surface, SOLDER, (sx, sy), 1)
        surface.set_at((sx, sy), (200, 200, 210))

    # Capacitors
    for i in range(4):
        cx = x + 4 + (i * 17) % (w - 8)
        cy = y + 5 + (i * 23) % (h - 12)
        cap_color = CAP_BLUE if i % 2 == 0 else CAP_BROWN
        pygame.draw.rect(surface, cap_color, (cx, cy, 4, 6))
        # Leads
        surface.set_at((cx + 1, cy + 6), SOLDER)
        surface.set_at((cx + 2, cy + 6), SOLDER)

    # Resistors (small colored bands)
    for i in range(3):
        rx = x + 2 + (i * 21) % (w - 10)
        ry = y + 15 + (i * 19) % (h - 18)
        pygame.draw.rect(surface, (180, 160, 120), (rx, ry, 8, 3))
        surface.set_at((rx + 2, ry + 1), (200, 50, 50))
        surface.set_at((rx + 4, ry + 1), (50, 50, 200))
        surface.set_at((rx + 6, ry + 1), (50, 180, 50))
