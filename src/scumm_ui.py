"""SCUMM verb bar and inventory UI — matching original Maniac Mansion (1987)."""
import pygame
from src.font import draw_text, draw_text_centered, text_width, CHAR_H

# Layout at 320x200 native resolution
SCENE_H = 136        # playable scene area height
STATUS_Y = 137       # status text line (above verbs)
VERB_AREA_TOP = 146  # verb grid starts here
VERB_AREA_H = 28     # 4 rows * ~7px
INV_AREA_TOP = 174   # inventory below verbs
INV_AREA_H = 26
UI_TOP = SCENE_H     # where the UI background begins

# Original Maniac Mansion verb layout: 4 columns x 4 rows
# (some slots empty in last row)
VERBS = [
    # col 0        col 1        col 2        col 3
    "Push",       "Open",      "Walk to",   "Turn on",
    "Pull",       "Close",     "Pick up",   "Turn off",
    "Give",       "Read",      "What is",   "Use",
    "",           "",          "",          "",
]

# Only non-empty verbs for lookup
VERB_LIST = [v for v in VERBS if v]

INVENTORY = [
    "screwdriver", "iPhone", "keys",
    "invoice", "rubber duck",
]

# Authentic Maniac Mansion colors
COL_UI_BG = (0, 0, 0)                # black background
COL_VERB = (0, 220, 0)               # bright green verbs
COL_VERB_HI = (255, 255, 85)         # highlighted verb (bright yellow)
COL_VERB_CLICK = (255, 255, 255)     # click flash white
COL_STATUS = (255, 255, 255)         # status line white
COL_INV = (200, 80, 200)             # pink/magenta inventory text

# 4-column layout positions
VERB_COL_X = [4, 76, 156, 240]
VERB_ROW_H = 8
N_COLS = 4
N_ROWS = 4


class ScummUI:
    def __init__(self):
        self.selected_verb = None
        self.highlight_verb = None
        self.click_flash = None
        self.click_timer = 0.0
        self.status_text = ""

    def select_verb(self, verb):
        self.selected_verb = verb
        self.click_flash = verb
        self.click_timer = 0.15

    def set_status(self, text):
        self.status_text = text

    def get_verb_pos(self, verb):
        """Return center (x, y) of a verb label in native coords."""
        if verb not in VERBS:
            return (160, VERB_AREA_TOP + 14)
        idx = VERBS.index(verb)
        col = idx % N_COLS
        row = idx // N_COLS
        x = VERB_COL_X[col] + text_width(verb) // 2
        y = VERB_AREA_TOP + row * VERB_ROW_H + CHAR_H // 2
        return (x, y)

    def get_inventory_pos(self, item):
        if item not in INVENTORY:
            return (160, INV_AREA_TOP + 8)
        idx = INVENTORY.index(item)
        # Two rows of 3 items
        col = idx % 3
        row = idx // 3
        slot_w = 320 // 3
        x = col * slot_w + slot_w // 2
        y = INV_AREA_TOP + row * 9 + 4
        return (x, y)

    def update(self, dt, cursor_x, cursor_y):
        if self.click_timer > 0:
            self.click_timer -= dt
            if self.click_timer <= 0:
                self.click_flash = None

        # Verb hover detection
        self.highlight_verb = None
        if VERB_AREA_TOP <= cursor_y < VERB_AREA_TOP + VERB_AREA_H:
            for verb in VERB_LIST:
                vx, vy = self.get_verb_pos(verb)
                hw = text_width(verb) // 2 + 4
                if abs(cursor_x - vx) < hw and abs(cursor_y - vy) < 5:
                    self.highlight_verb = verb
                    break

    def draw(self, surface):
        # Black background for entire UI area
        pygame.draw.rect(surface, COL_UI_BG, (0, UI_TOP, 320, 200 - UI_TOP))

        # Status line (centered, above verb grid)
        if self.status_text:
            draw_text_centered(surface, 160, STATUS_Y, self.status_text, COL_STATUS)

        # Verb grid: 4 columns x 4 rows
        for i, verb in enumerate(VERBS):
            if not verb:
                continue
            col = i % N_COLS
            row = i // N_COLS
            x = VERB_COL_X[col]
            y = VERB_AREA_TOP + row * VERB_ROW_H

            if verb == self.click_flash and self.click_timer > 0:
                color = COL_VERB_CLICK
            elif verb == self.selected_verb:
                color = COL_VERB_HI
            elif verb == self.highlight_verb:
                color = COL_VERB_HI
            else:
                color = COL_VERB

            draw_text(surface, x, y, verb, color)

        # Inventory separator line
        pygame.draw.line(surface, (40, 40, 40), (0, INV_AREA_TOP - 1), (319, INV_AREA_TOP - 1))

        # Inventory items in pink/magenta — single row
        x_pos = 4
        for i, item in enumerate(INVENTORY):
            draw_text(surface, x_pos, INV_AREA_TOP + 2, item, COL_INV)
            x_pos += text_width(item) + 12
