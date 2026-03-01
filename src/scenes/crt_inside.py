"""Scene 7: CRT inside view — Stefan seen through CRT, recording dot blinking (~5s)."""
import math
import os
import pygame
from src.font import draw_text


DURATION = 6.0

# Sparkle on right glasses corner (viewer's right = image right)
SPARKLE_POS = (195, 65)
SPARKLE_DELAY = 1.8    # start after zoom (0.8s) + 1s pause
SPARKLE_DURATION = 0.9 # one sparkle, grow then fade
SPARKLE_H_MAX = 40     # horizontal ray max length
SPARKLE_V_MAX = 10     # vertical ray max length

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

        # Composite overlays onto a working copy so they zoom with the image
        frame = self.bg.copy()

        # Blinking white recording circle (1s frequency)
        if int(self.time * 2) % 2 == 0:
            pygame.draw.circle(frame, (255, 255, 255), (252, 37), 5)

        # Recording timer (white, no background, mirrored, right-aligned)
        secs = int(self.time)
        timer_str = f"{secs // 60}:{secs % 60:02d}"
        from src.font import text_width
        tw = text_width(timer_str)
        timer_surf = pygame.Surface((tw, 8), pygame.SRCALPHA)
        draw_text(timer_surf, 0, 0, timer_str, color=(255, 255, 255))
        timer_surf = pygame.transform.flip(timer_surf, True, False)
        frame.blit(timer_surf, (260 - tw, 140))

        # Cross-shaped star burst on glasses corner (single burst)
        sparkle_t = self.time - SPARKLE_DELAY
        if 0 < sparkle_t < SPARKLE_DURATION:
            phase = sparkle_t / SPARKLE_DURATION
            intensity = 1.0 - abs(2.0 * phase - 1.0)
        else:
            intensity = 0
        rh = int(SPARKLE_H_MAX * intensity)
        rv = int(SPARKLE_V_MAX * intensity)
        if rh > 0:
            cx, cy = SPARKLE_POS
            bright = int(255 * min(1.0, intensity * 1.5))
            white = (bright, bright, bright)
            dim = (bright * 2 // 3, bright * 2 // 3, bright // 2)

            # Long horizontal streak (anamorphic lens flare)
            pygame.draw.line(frame, white, (cx - rh, cy), (cx + rh, cy), 1)

            # Glow lines above and below for thickness
            if rh > 20:
                pygame.draw.line(frame, dim, (cx - rh * 2 // 3, cy - 1), (cx + rh * 2 // 3, cy - 1), 1)
                pygame.draw.line(frame, dim, (cx - rh * 2 // 3, cy + 1), (cx + rh * 2 // 3, cy + 1), 1)

            # Short vertical ray
            pygame.draw.line(frame, white, (cx, cy - rv), (cx, cy + rv), 1)

            # Bright center dot
            pygame.draw.rect(frame, (bright, bright, bright), (cx - 1, cy - 1, 3, 3))

        # Zoom-out effect: start zoomed in on center, scale out over 0.8s
        progress = min(1.0, self.time / 0.8)
        zoom = 2.0 - progress  # 2.0 → 1.0

        if zoom > 1.01:
            zw = int(320 / zoom)
            zh = int(200 / zoom)
            zx = (320 - zw) // 2
            zy = (200 - zh) // 2
            cropped = frame.subsurface(pygame.Rect(zx, zy, zw, zh))
            scaled = pygame.transform.scale(cropped, (320, 200))
            surface.blit(scaled, (0, 0))
        else:
            surface.blit(frame, (0, 0))

    def get_sound_events(self, start_time):
        return []
