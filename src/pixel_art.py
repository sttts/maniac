"""Procedural pixel art generators for all scene backgrounds at 320x200."""
import pygame


# Shared palette (Maniac Mansion inspired)
DARK_BLUE = (25, 25, 60)
MED_BLUE = (40, 40, 90)
LIGHT_BLUE = (60, 65, 120)
WALL_BLUE = (35, 35, 80)
FLOOR_BROWN = (80, 55, 35)
FLOOR_DARK = (60, 40, 25)
WOOD_BROWN = (100, 65, 40)
WOOD_DARK = (70, 45, 25)
DOOR_BROWN = (90, 60, 35)
COUCH_PURPLE = (90, 50, 100)
COUCH_DARK = (65, 35, 75)
LAMP_YELLOW = (220, 200, 100)
LAMP_GLOW = (180, 170, 80)
WINDOW_CYAN = (60, 90, 120)
DESK_BROWN = (110, 75, 45)
MONITOR_GRAY = (100, 100, 110)
MONITOR_DARK = (60, 60, 70)
SCREEN_BLACK = (5, 5, 15)
GREEN_LED = (50, 200, 50)
RED_LED = (200, 50, 50)
CRT_BEZEL = (70, 70, 80)
PCB_GREEN = (30, 80, 30)
PCB_DARK = (20, 60, 20)
COPPER = (180, 130, 60)
SOLDER = (160, 160, 170)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAIR_COLOR = (70, 50, 35)
STAIR_DARK = (50, 35, 22)
RAILING = (80, 60, 40)
CARPET = (90, 30, 30)
BOOKSHELF = (85, 55, 30)
BOOK_COLORS = [
    (180, 50, 50), (50, 120, 180), (50, 150, 50),
    (180, 180, 50), (150, 80, 50), (100, 50, 150),
]


def draw_living_room(surface):
    """Scene 1: Living room with stairs, couch, lamp, picture frame, door."""
    W, H = 320, 144  # scene area height

    # Floor
    pygame.draw.rect(surface, FLOOR_BROWN, (0, 105, W, H - 105))
    # Floor boards
    for y in range(107, H, 6):
        pygame.draw.line(surface, FLOOR_DARK, (0, y), (W, y))

    # Back wall
    pygame.draw.rect(surface, WALL_BLUE, (0, 0, W, 105))
    # Baseboard
    pygame.draw.rect(surface, WOOD_DARK, (0, 102, W, 4))

    # Staircase on left (going up-left)
    for i in range(8):
        sx = 5 + i * 8
        sy = 100 - i * 12
        sw = 55 - i * 4
        sh = 12
        pygame.draw.rect(surface, STAIR_COLOR, (sx, sy, sw, sh))
        pygame.draw.rect(surface, STAIR_DARK, (sx, sy, sw, 2))
    # Railing
    for i in range(8):
        rx = 55 - i * 2
        ry = 100 - i * 12
        pygame.draw.line(surface, RAILING, (rx, ry), (rx, ry - 18), 2)
    # Railing top bar
    pygame.draw.line(surface, RAILING, (55, 82), (40, 4), 2)

    # Carpet under stairs
    pygame.draw.rect(surface, CARPET, (0, 105, 60, H - 105))

    # Picture frame on wall
    pygame.draw.rect(surface, WOOD_BROWN, (130, 25, 30, 25))
    pygame.draw.rect(surface, LIGHT_BLUE, (133, 28, 24, 19))
    # Little landscape in frame
    pygame.draw.rect(surface, (80, 140, 80), (133, 38, 24, 9))
    pygame.draw.rect(surface, (100, 160, 200), (133, 28, 24, 10))

    # Lamp on table
    pygame.draw.rect(surface, WOOD_BROWN, (175, 85, 20, 20))  # table
    pygame.draw.rect(surface, WOOD_DARK, (175, 85, 20, 2))
    pygame.draw.rect(surface, LAMP_YELLOW, (181, 60, 8, 10))  # shade
    pygame.draw.rect(surface, LAMP_GLOW, (183, 70, 4, 16))    # pole
    # Glow circle
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            if dx * dx + dy * dy < 64:
                px, py = 185 + dx, 65 + dy
                if 0 <= px < W and 0 <= py < H:
                    c = surface.get_at((px, py))
                    nr = min(255, c[0] + 15)
                    ng = min(255, c[1] + 12)
                    nb = min(255, c[2] + 5)
                    surface.set_at((px, py), (nr, ng, nb))

    # Couch
    pygame.draw.rect(surface, COUCH_DARK, (195, 80, 70, 28))    # back
    pygame.draw.rect(surface, COUCH_PURPLE, (195, 88, 70, 20))  # seat
    pygame.draw.rect(surface, COUCH_DARK, (195, 88, 70, 3))     # shadow
    # Armrests
    pygame.draw.rect(surface, COUCH_DARK, (192, 85, 6, 24))
    pygame.draw.rect(surface, COUCH_DARK, (262, 85, 6, 24))
    # Cushion lines
    pygame.draw.line(surface, COUCH_DARK, (218, 90), (218, 105))
    pygame.draw.line(surface, COUCH_DARK, (242, 90), (242, 105))

    # Door on right
    pygame.draw.rect(surface, DOOR_BROWN, (285, 35, 28, 70))
    pygame.draw.rect(surface, WOOD_DARK, (285, 35, 28, 3))      # top frame
    pygame.draw.rect(surface, WOOD_DARK, (285, 35, 3, 70))      # left frame
    pygame.draw.rect(surface, WOOD_DARK, (310, 35, 3, 70))      # right frame
    # Door knob
    pygame.draw.circle(surface, LAMP_YELLOW, (305, 72), 2)
    # Door panels
    pygame.draw.rect(surface, WOOD_DARK, (290, 42, 18, 12), 1)
    pygame.draw.rect(surface, WOOD_DARK, (290, 60, 18, 15), 1)


def draw_computer_room(surface):
    """Scene 2: Computer room with desk, CRT monitor, keyboard, mic, bookshelf."""
    W, H = 320, 144

    # Floor
    pygame.draw.rect(surface, FLOOR_BROWN, (0, 108, W, H - 108))
    for y in range(110, H, 6):
        pygame.draw.line(surface, FLOOR_DARK, (0, y), (W, y))

    # Back wall
    pygame.draw.rect(surface, DARK_BLUE, (0, 0, W, 108))
    pygame.draw.rect(surface, WOOD_DARK, (0, 105, W, 4))

    # Bookshelf on left
    pygame.draw.rect(surface, BOOKSHELF, (10, 15, 60, 90))
    for shelf_y in [15, 40, 65, 90]:
        pygame.draw.rect(surface, WOOD_DARK, (10, shelf_y, 60, 3))
    # Books on shelves
    bx = 12
    for shelf in range(3):
        bx = 12
        base_y = 18 + shelf * 25
        for i in range(7):
            bw = 5 + (i % 3)
            bh = 18 + (i % 4)
            color = BOOK_COLORS[i % len(BOOK_COLORS)]
            pygame.draw.rect(surface, color, (bx, base_y + (22 - bh), bw, bh))
            bx += bw + 1

    # Desk
    pygame.draw.rect(surface, DESK_BROWN, (100, 75, 160, 8))    # desktop surface
    pygame.draw.rect(surface, WOOD_DARK, (100, 75, 160, 2))     # edge
    pygame.draw.rect(surface, WOOD_DARK, (105, 83, 8, 25))      # left leg
    pygame.draw.rect(surface, WOOD_DARK, (247, 83, 8, 25))      # right leg

    # CRT Monitor
    pygame.draw.rect(surface, MONITOR_GRAY, (150, 30, 60, 48))  # outer case
    pygame.draw.rect(surface, MONITOR_DARK, (153, 33, 54, 38))  # bezel
    pygame.draw.rect(surface, SCREEN_BLACK, (156, 36, 48, 32))  # screen
    # Monitor stand
    pygame.draw.rect(surface, MONITOR_GRAY, (170, 72, 20, 5))
    # Power LED
    pygame.draw.rect(surface, RED_LED, (200, 70, 3, 2))

    # Keyboard
    pygame.draw.rect(surface, (80, 80, 90), (155, 79, 45, 7))
    # Key rows
    for ky in range(2):
        for kx in range(10):
            pygame.draw.rect(
                surface, (100, 100, 110),
                (157 + kx * 4, 80 + ky * 3, 3, 2),
            )

    # Microphone on right side of desk
    pygame.draw.rect(surface, (50, 50, 55), (240, 55, 4, 22))   # stand
    pygame.draw.circle(surface, (80, 80, 90), (242, 52), 5)      # mic head
    pygame.draw.rect(surface, (50, 50, 55), (236, 76, 12, 3))   # base

    # Chair (simple)
    pygame.draw.rect(surface, (60, 40, 30), (160, 95, 40, 5))   # seat
    pygame.draw.rect(surface, (50, 30, 20), (175, 100, 10, 12)) # post
    pygame.draw.rect(surface, (50, 30, 20), (165, 112, 30, 3))  # base
    # Chair back
    pygame.draw.rect(surface, (60, 40, 30), (162, 80, 36, 16))
    pygame.draw.rect(surface, (70, 50, 35), (164, 82, 32, 12))

    # Window on right wall
    pygame.draw.rect(surface, WOOD_BROWN, (280, 15, 30, 40))
    pygame.draw.rect(surface, WINDOW_CYAN, (283, 18, 24, 34))
    pygame.draw.line(surface, WOOD_BROWN, (295, 18), (295, 52), 2)
    pygame.draw.line(surface, WOOD_BROWN, (283, 35), (307, 35), 2)


def draw_switch_closeup(surface):
    """Scene 3: Close-up of computer power switch."""
    W, H = 320, 144

    # Beige computer case panel
    pygame.draw.rect(surface, (180, 175, 160), (0, 0, W, H))
    # Panel texture lines
    for y in range(0, H, 3):
        pygame.draw.line(surface, (170, 165, 150), (0, y), (W, y))

    # Ventilation slots on left
    for i in range(8):
        y = 20 + i * 12
        pygame.draw.rect(surface, (120, 115, 100), (20, y, 50, 4))

    # Switch recess
    pygame.draw.rect(surface, (130, 125, 110), (130, 30, 60, 84))
    pygame.draw.rect(surface, (110, 105, 90), (130, 30, 60, 3))
    pygame.draw.rect(surface, (150, 145, 130), (130, 111, 60, 3))

    # "ON" label
    font = pygame.font.SysFont("monospace", 10, bold=True)
    label = font.render("ON", False, (60, 55, 45))
    surface.blit(label, (148, 35))

    # The switch itself (toggle, currently off — will animate to on)
    pygame.draw.rect(surface, (60, 60, 65), (145, 55, 30, 50))   # switch track
    pygame.draw.rect(surface, (80, 80, 85), (148, 75, 24, 28))   # switch handle (down = off)
    pygame.draw.rect(surface, (90, 90, 95), (148, 75, 24, 3))    # highlight

    # LED indicator (off)
    pygame.draw.circle(surface, (30, 50, 30), (210, 72), 5)
    pygame.draw.circle(surface, (20, 35, 20), (210, 72), 3)


def draw_switch_on(surface):
    """Scene 3 variant: switch flipped ON with green LED."""
    W, H = 320, 144

    # Same base panel
    draw_switch_closeup(surface)

    # Override switch handle position (up = on)
    pygame.draw.rect(surface, (60, 60, 65), (145, 55, 30, 50))
    pygame.draw.rect(surface, (90, 90, 100), (148, 57, 24, 28))  # handle up
    pygame.draw.rect(surface, (100, 100, 110), (148, 57, 24, 3))

    # Green LED (on)
    pygame.draw.circle(surface, GREEN_LED, (210, 72), 5)
    # LED glow
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            if dx * dx + dy * dy < 50:
                px, py = 210 + dx, 72 + dy
                if 0 <= px < W and 0 <= py < H:
                    c = surface.get_at((px, py))
                    ng = min(255, c[1] + 30)
                    surface.set_at((px, py), (c[0], ng, c[2]))


def draw_dos_screen(surface, text_lines, cursor_visible=True):
    """Scene 4: MS-DOS boot screen on CRT monitor."""
    W, H = 320, 144

    # CRT monitor frame
    pygame.draw.rect(surface, MONITOR_DARK, (0, 0, W, H))
    pygame.draw.rect(surface, CRT_BEZEL, (10, 5, 300, 134))
    pygame.draw.rect(surface, SCREEN_BLACK, (18, 12, 284, 120))

    # Scanline effect
    for y in range(12, 132, 2):
        pygame.draw.line(surface, (10, 10, 20), (18, y), (302, y))

    font = pygame.font.SysFont("monospace", 8)

    # Draw text lines
    ty = 16
    for line in text_lines:
        if line.startswith("MS-DOS"):
            # Colorful MS-DOS logo
            colors = [
                (255, 50, 50), (255, 150, 50), (255, 255, 50),
                (50, 255, 50), (50, 150, 255), (150, 50, 255),
            ]
            tx = 22
            for i, ch in enumerate(line):
                c = colors[i % len(colors)]
                cs = font.render(ch, False, c)
                surface.blit(cs, (tx, ty))
                tx += cs.get_width()
        else:
            ts = font.render(line, False, (200, 200, 200))
            surface.blit(ts, (22, ty))
        ty += 11

    # Blinking cursor
    if cursor_visible:
        pygame.draw.rect(surface, (200, 200, 200), (22 + len(text_lines[-1]) * 5 if text_lines else 22, ty - 11, 5, 8))


def draw_flight_sim(surface, scroll_y=0):
    """Scene 5: Top-down retro flight sim — blue water, green islands, plane."""
    W, H = 320, 144

    # CRT frame
    pygame.draw.rect(surface, MONITOR_DARK, (0, 0, W, H))
    pygame.draw.rect(surface, CRT_BEZEL, (10, 5, 300, 134))

    # Game area
    game_rect = pygame.Rect(18, 12, 284, 120)
    game_surf = pygame.Surface((284, 120))

    # Water
    game_surf.fill((20, 60, 140))
    # Water wave pattern
    for y in range(0, 120, 4):
        wy = (y + int(scroll_y)) % 120
        for x in range(0, 284, 8):
            offset = ((x + wy * 3) % 16) - 8
            pygame.draw.line(
                game_surf, (30, 75, 160),
                (x + offset, wy), (x + offset + 4, wy),
            )

    # Islands (fixed positions, scroll with scroll_y)
    islands = [
        (60, 40, 25, 15), (180, 80, 35, 18), (250, 20, 20, 12),
        (100, 130, 30, 16), (40, 170, 22, 13), (200, 160, 28, 14),
        (140, 220, 32, 17), (280, 250, 20, 11),
    ]
    for ix, iy, iw, ih in islands:
        draw_y = (iy - int(scroll_y)) % 280 - 60
        if -ih <= draw_y <= 120:
            # Island shape
            pygame.draw.ellipse(
                game_surf, (60, 140, 50), (ix - iw // 2, draw_y, iw, ih)
            )
            # Beach edge
            pygame.draw.ellipse(
                game_surf, (180, 170, 100),
                (ix - iw // 2 + 2, draw_y + 2, iw - 4, ih - 4), 1,
            )

    # Plane sprite (center)
    px, py = 142, 55
    # Fuselage
    pygame.draw.rect(game_surf, (200, 200, 210), (px - 2, py - 6, 4, 12))
    # Wings
    pygame.draw.rect(game_surf, (180, 180, 190), (px - 10, py - 1, 20, 3))
    # Tail
    pygame.draw.rect(game_surf, (180, 180, 190), (px - 4, py + 5, 8, 2))
    # Cockpit
    pygame.draw.rect(game_surf, (100, 150, 200), (px - 1, py - 5, 2, 3))

    surface.blit(game_surf, game_rect.topleft)

    # HUD overlay
    font = pygame.font.SysFont("monospace", 7)
    score_text = font.render("SCORE: 1337", False, (200, 200, 50))
    surface.blit(score_text, (22, 14))
    alt_text = font.render("ALT: 5000", False, (200, 200, 50))
    surface.blit(alt_text, (240, 14))


def draw_crt_inside(surface, stefan_wave_frame=None):
    """Scene 7: Inside-CRT perspective with circuit boards and Stefan waving."""
    W, H = 320, 144

    # Circuit board borders
    surface.fill(BLACK)

    # Left PCB
    _draw_pcb(surface, 0, 0, 60, H)
    # Right PCB
    _draw_pcb(surface, 260, 0, 60, H)
    # Bottom electronics
    _draw_pcb(surface, 60, 115, 200, 29)

    # CRT screen opening (rounded rectangle)
    screen_rect = pygame.Rect(65, 8, 190, 105)
    pygame.draw.rect(surface, CRT_BEZEL, screen_rect, border_radius=8)
    inner = screen_rect.inflate(-8, -8)
    pygame.draw.rect(surface, (50, 50, 80), inner, border_radius=4)

    # Stefan waving inside the screen
    if stefan_wave_frame:
        # Scale up the character for close-up
        big = pygame.transform.scale(stefan_wave_frame, (48, 90))
        sx = inner.centerx - 24
        sy = inner.bottom - 92
        surface.blit(big, (sx, sy))

    # YouTube overlay
    font = pygame.font.SysFont("monospace", 7)
    # Timecode
    tc = font.render("0:00 / 30:03", False, WHITE)
    surface.blit(tc, (inner.right - 65, inner.bottom - 12))
    # REC dot
    pygame.draw.circle(surface, (255, 30, 30), (inner.left + 10, inner.bottom - 8), 3)
    rec_text = font.render("REC", False, (255, 30, 30))
    surface.blit(rec_text, (inner.left + 16, inner.bottom - 12))

    # Wires between PCBs and screen
    for y in range(20, 110, 15):
        color = COPPER if y % 30 == 20 else (150, 40, 40)
        pygame.draw.line(surface, color, (58, y), (66, y + 3), 1)
        pygame.draw.line(surface, color, (262, y), (254, y + 3), 1)


def _draw_pcb(surface, x, y, w, h):
    """Draw a circuit board section with components."""
    pygame.draw.rect(surface, PCB_GREEN, (x, y, w, h))

    # Traces
    for i in range(0, h, 6):
        tx = x + (i * 7) % w
        pygame.draw.line(surface, PCB_DARK, (tx, y + i), (tx + 8, y + i), 1)
    for i in range(0, w, 8):
        ty = y + (i * 5) % h
        pygame.draw.line(surface, COPPER, (x + i, ty), (x + i, ty + 10), 1)

    # Solder points
    for i in range(5):
        sx = x + 5 + (i * 11) % (w - 10)
        sy = y + 5 + (i * 17) % (h - 10)
        pygame.draw.circle(surface, SOLDER, (sx, sy), 2)

    # IC chips
    for i in range(2):
        cx = x + 8 + i * (w // 2 - 5)
        cy = y + 15 + i * 30
        if cx + 14 < x + w and cy + 10 < y + h:
            pygame.draw.rect(surface, (20, 20, 25), (cx, cy, 14, 10))
            # Pins
            for p in range(4):
                pygame.draw.rect(surface, SOLDER, (cx + 2 + p * 3, cy - 1, 1, 1))
                pygame.draw.rect(surface, SOLDER, (cx + 2 + p * 3, cy + 10, 1, 1))

    # Capacitors
    for i in range(3):
        cx = x + 3 + (i * 19) % (w - 6)
        cy = y + 40 + (i * 23) % (h - 45)
        color = (50, 80, 180) if i % 2 == 0 else (180, 130, 30)
        pygame.draw.rect(surface, color, (cx, cy, 4, 6))


def draw_rec_screen(surface, rec_blink=True):
    """Scene 6 ending: Recording screen on CRT."""
    W, H = 320, 144

    # CRT frame
    pygame.draw.rect(surface, MONITOR_DARK, (0, 0, W, H))
    pygame.draw.rect(surface, CRT_BEZEL, (10, 5, 300, 134))
    pygame.draw.rect(surface, SCREEN_BLACK, (18, 12, 284, 120))

    # Scanlines
    for y in range(12, 132, 2):
        pygame.draw.line(surface, (10, 10, 20), (18, y), (302, y))

    font_big = pygame.font.SysFont("monospace", 16, bold=True)
    font_sm = pygame.font.SysFont("monospace", 8)

    # "Recording..." text
    rec_label = font_big.render("Recording...", False, (200, 200, 200))
    surface.blit(rec_label, (95, 45))

    # REC indicator
    if rec_blink:
        pygame.draw.circle(surface, (255, 30, 30), (120, 85), 6)
    rec_text = font_big.render("REC", False, (255, 30, 30))
    surface.blit(rec_text, (135, 77))

    # VU meter bars
    for i in range(8):
        bh = 5 + (i * 7) % 20
        color = (50, 200, 50) if i < 5 else (200, 200, 50) if i < 7 else (200, 50, 50)
        pygame.draw.rect(surface, color, (100 + i * 15, 105 - bh, 10, bh))
