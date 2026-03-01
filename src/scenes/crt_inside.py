"""Scene 7: CRT inside view — Stefan seen through CRT, recording dot blinking (~5s)."""
import os
import pygame


DURATION = 5.0

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BG_PATH = os.path.join(PROJECT_ROOT, "assets", "backgrounds", "crt_inside.png")


def _load_crt_bg():
    """Load CRT inside background, scaled to full 320x200."""
    if not os.path.exists(BG_PATH):
        return None
    img = pygame.image.load(BG_PATH)
    try:
        img = img.convert()
    except pygame.error:
        pass
    return pygame.transform.scale(img, (320, 200))


class CrtInsideScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.cursor.visible = False
        self.bg = _load_crt_bg()

    def update(self, dt):
        self.time += dt
        if self.time >= DURATION:
            self.done = True

    def draw(self, surface):
        if self.bg is None:
            surface.fill((0, 0, 0))
            return

        # Zoom-out effect: start zoomed in on center, scale out over 0.8s
        progress = min(1.0, self.time / 0.8)
        zoom = 2.0 - progress  # 2.0 → 1.0

        if zoom > 1.01:
            zw = int(320 / zoom)
            zh = int(200 / zoom)
            zx = (320 - zw) // 2
            zy = (200 - zh) // 2
            cropped = self.bg.subsurface(pygame.Rect(zx, zy, zw, zh))
            scaled = pygame.transform.scale(cropped, (320, 200))
            surface.blit(scaled, (0, 0))
        else:
            surface.blit(self.bg, (0, 0))

        # Blinking white recording circle at top-right of CRT screen (1s frequency)
        if int(self.time * 2) % 2 == 0:
            pygame.draw.circle(surface, (255, 255, 255), (252, 37), 5)

    def get_sound_events(self, start_time):
        return []
