import pygame

# SCUMM UI layout constants (at 320x200 native resolution)
UI_TOP = 144        # verb area starts here
VERB_AREA_TOP = 144
VERB_AREA_H = 32
INV_AREA_TOP = 176  # inventory area
INV_AREA_H = 24
SCENE_H = 144       # playable scene area height

# Verb list matching Maniac Mansion layout
VERBS = [
    "Walk to", "Pick up", "Use",
    "Open",    "Look at", "Turn on",
    "Close",   "Give",    "Push",
]

# Inventory items
INVENTORY = ["Key", "Blank Tape", "Can of Pepsi"]

# Colors
COL_BG = (0, 0, 0)
COL_VERB = (120, 180, 120)       # green text
COL_VERB_HI = (255, 255, 100)    # highlighted yellow
COL_VERB_CLICK = (255, 255, 255) # click flash white
COL_INV = (100, 160, 200)        # inventory blue
COL_STATUS = (255, 255, 255)     # status line


def _get_font():
    """Get a small pixel font for the UI."""
    return pygame.font.SysFont("monospace", 8, bold=False)


class ScummUI:
    def __init__(self):
        self.font = None
        self.selected_verb = None   # currently selected verb text
        self.highlight_verb = None  # verb under cursor
        self.click_flash = None     # verb being click-flashed
        self.click_timer = 0.0
        self.status_text = ""       # top status line e.g. "Walk to Door"

    def _ensure_font(self):
        if self.font is None:
            self.font = _get_font()

    def select_verb(self, verb):
        """Set the selected/active verb."""
        self.selected_verb = verb
        self.click_flash = verb
        self.click_timer = 0.15

    def set_status(self, text):
        self.status_text = text

    def get_verb_pos(self, verb):
        """Return center position (x, y) of a verb in native coords."""
        if verb not in VERBS:
            return (160, VERB_AREA_TOP + 16)
        idx = VERBS.index(verb)
        col = idx % 3
        row = idx // 3
        x = 10 + col * 107 + 50
        y = VERB_AREA_TOP + 2 + row * 10 + 4
        return (x, y)

    def get_inventory_pos(self, item):
        """Return center position of an inventory item."""
        if item not in INVENTORY:
            return (160, INV_AREA_TOP + 12)
        idx = INVENTORY.index(item)
        x = 10 + idx * 100 + 40
        y = INV_AREA_TOP + 12
        return (x, y)

    def update(self, dt, cursor_x, cursor_y):
        """Update hover state and click flash timer."""
        if self.click_timer > 0:
            self.click_timer -= dt
            if self.click_timer <= 0:
                self.click_flash = None

        # Check verb hover
        self.highlight_verb = None
        if VERB_AREA_TOP <= cursor_y < VERB_AREA_TOP + VERB_AREA_H:
            for verb in VERBS:
                vx, vy = self.get_verb_pos(verb)
                if abs(cursor_x - vx) < 45 and abs(cursor_y - vy) < 6:
                    self.highlight_verb = verb
                    break

    def draw(self, surface):
        self._ensure_font()

        # Black background for UI area
        pygame.draw.rect(
            surface, COL_BG, (0, UI_TOP, 320, 200 - UI_TOP)
        )

        # Draw verbs in grid
        for i, verb in enumerate(VERBS):
            col = i % 3
            row = i // 3
            x = 10 + col * 107
            y = VERB_AREA_TOP + 2 + row * 10

            # Pick color based on state
            if verb == self.click_flash and self.click_timer > 0:
                color = COL_VERB_CLICK
            elif verb == self.selected_verb:
                color = COL_VERB_HI
            elif verb == self.highlight_verb:
                color = COL_VERB_HI
            else:
                color = COL_VERB

            text_surf = self.font.render(verb, False, color)
            surface.blit(text_surf, (x, y))

        # Draw inventory items
        for i, item in enumerate(INVENTORY):
            x = 10 + i * 100
            y = INV_AREA_TOP + 4
            text_surf = self.font.render(item, False, COL_INV)
            surface.blit(text_surf, (x, y))

        # Status line at top of UI area
        if self.status_text:
            status_surf = self.font.render(self.status_text, False, COL_STATUS)
            sw = status_surf.get_width()
            surface.blit(status_surf, ((320 - sw) // 2, UI_TOP - 10))
