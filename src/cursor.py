"""Maniac Mansion crosshair cursor — small + with hollow center."""
import pygame


def _make_cursor_surface():
    """Create the original Maniac Mansion crosshair cursor.

    Bitmap pattern matching the SCUMM crosshair: thin + with hollow center,
    black outline for visibility on any background.
    """
    # B=black, W=white, .=transparent
    # 23x23 with center at (11,11), hollow center, 1px-wide arms
    pattern = [
        "...........B...........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        ".BBBBBBBBBBWBBBBBBBBBB.",
        "BWWWWWWWWWW.WWWWWWWWWWB",
        ".BBBBBBBBBBWBBBBBBBBBB.",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "..........BWB..........",
        "...........B...........",
    ]
    h = len(pattern)
    w = len(pattern[0])
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            if ch == "W":
                s.set_at((x, y), (255, 255, 255, 255))
            elif ch == "B":
                s.set_at((x, y), (0, 0, 0, 255))
    return s


def _ease_in_out(t):
    """Smooth easing function for cursor movement."""
    return t * t * (3 - 2 * t)


class Cursor:
    def __init__(self):
        self.surface = _make_cursor_surface()
        self.x = 160.0
        self.y = 60.0
        self.visible = True

        # Movement animation state
        self._moving = False
        self._start_x = 0.0
        self._start_y = 0.0
        self._end_x = 0.0
        self._end_y = 0.0
        self._move_time = 0.0
        self._move_duration = 0.0
        self._on_arrive = None

    def move_to(self, x, y, duration=0.4, on_arrive=None):
        """Start animated movement to target position."""
        self._moving = True
        self._start_x = self.x
        self._start_y = self.y
        self._end_x = float(x)
        self._end_y = float(y)
        self._move_time = 0.0
        self._move_duration = duration
        self._on_arrive = on_arrive

    def teleport(self, x, y):
        """Instantly move cursor."""
        self.x = float(x)
        self.y = float(y)
        self._moving = False

    def is_moving(self):
        return self._moving

    def update(self, dt):
        if not self._moving:
            return
        self._move_time += dt
        t = min(1.0, self._move_time / self._move_duration)
        eased = _ease_in_out(t)
        self.x = self._start_x + (self._end_x - self._start_x) * eased
        self.y = self._start_y + (self._end_y - self._start_y) * eased
        if t >= 1.0:
            self._moving = False
            if self._on_arrive:
                self._on_arrive()
                self._on_arrive = None

    def draw(self, surface):
        if self.visible:
            # Center the crosshair on (self.x, self.y)
            cx = int(self.x) - self.surface.get_width() // 2
            cy = int(self.y) - self.surface.get_height() // 2
            surface.blit(self.surface, (cx, cy))
