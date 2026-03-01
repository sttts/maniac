"""SCUMM verb bar and inventory UI — authentic Maniac Mansion style."""
import pygame
from src.font import draw_text, draw_text_centered, text_width, CHAR_H

# Layout at 320x200 native resolution (matching real Maniac Mansion)
SCENE_H = 136       # playable scene area
STATUS_Y = 136      # one-line status text
VERB_AREA_TOP = 146 # verb grid starts here
VERB_AREA_H = 28    # 3 rows * ~9px
INV_AREA_TOP = 176  # inventory below verbs
INV_AREA_H = 24
UI_TOP = STATUS_Y   # where the UI begins

# Verb grid: 3 columns x 3 rows (matching Maniac Mansion layout)
VERBS = [
    "Walk to",  "Pick up",  "Use",
    "Open",     "Look at",  "Turn on",
    "Close",    "Give",     "Push",
]

INVENTORY = ["Key", "Blank Tape", "Can of Pepsi"]

# Authentic Maniac Mansion colors
COL_UI_BG = (16, 16, 60)          # dark blue UI background
COL_VERB = (0, 200, 0)            # green verbs (MM used bright green)
COL_VERB_HI = (255, 255, 85)     # highlighted verb (bright yellow)
COL_VERB_CLICK = (255, 255, 255) # click flash white
COL_INV_BG = (16, 16, 60)        # inventory background
COL_INV_TEXT = (0, 200, 0)       # inventory text green
COL_INV_BORDER = (80, 80, 120)   # subtle border between items
COL_STATUS = (255, 255, 255)     # status line white

# Verb positions: col_x offsets for 3 columns
VERB_COL_X = [6, 110, 216]
VERB_ROW_H = 9


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
        col = idx % 3
        row = idx // 3
        x = VERB_COL_X[col] + text_width(verb) // 2
        y = VERB_AREA_TOP + row * VERB_ROW_H + CHAR_H // 2
        return (x, y)

    def get_inventory_pos(self, item):
        if item not in INVENTORY:
            return (160, INV_AREA_TOP + 10)
        idx = INVENTORY.index(item)
        slot_w = 320 // len(INVENTORY)
        x = idx * slot_w + slot_w // 2
        y = INV_AREA_TOP + 10
        return (x, y)

    def update(self, dt, cursor_x, cursor_y):
        if self.click_timer > 0:
            self.click_timer -= dt
            if self.click_timer <= 0:
                self.click_flash = None

        # Verb hover detection
        self.highlight_verb = None
        if VERB_AREA_TOP <= cursor_y < VERB_AREA_TOP + VERB_AREA_H:
            for verb in VERBS:
                vx, vy = self.get_verb_pos(verb)
                hw = text_width(verb) // 2 + 4
                if abs(cursor_x - vx) < hw and abs(cursor_y - vy) < 5:
                    self.highlight_verb = verb
                    break

    def draw(self, surface):
        # Dark blue background for entire UI area
        pygame.draw.rect(surface, COL_UI_BG, (0, UI_TOP, 320, 200 - UI_TOP))

        # Thin separator line between scene and UI
        pygame.draw.line(surface, (40, 40, 100), (0, UI_TOP), (319, UI_TOP))

        # Status line (centered, one line above verbs)
        if self.status_text:
            draw_text_centered(surface, 160, STATUS_Y + 2, self.status_text, COL_STATUS)

        # Verb grid
        for i, verb in enumerate(VERBS):
            col = i % 3
            row = i // 3
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

        # Inventory area border
        pygame.draw.line(surface, COL_INV_BORDER, (0, INV_AREA_TOP - 1), (319, INV_AREA_TOP - 1))

        # Inventory slots
        slot_w = 320 // len(INVENTORY)
        for i, item in enumerate(INVENTORY):
            x = i * slot_w + 4
            y = INV_AREA_TOP + 4
            draw_text(surface, x, y, item, COL_INV_TEXT)

            # Slot divider
            if i > 0:
                dx = i * slot_w
                pygame.draw.line(surface, COL_INV_BORDER, (dx, INV_AREA_TOP), (dx, 199))
