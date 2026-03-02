"""Scene 7: CRT inside view — Stefan seen through CRT, recording dot blinking."""
import math
import os
import pygame
from src.font import draw_text


DURATION_SHORT = 3.5
DURATION_LONG = 6.0

# Sparkle on right glasses corner (viewer's right = image right)
SPARKLE_POS = (195, 65)
SPARKLE_DELAY_SHORT = 1.2
SPARKLE_DELAY_LONG = 1.8
SPARKLE_DURATION_SHORT = 0.7
SPARKLE_DURATION_LONG = 0.9
SPARKLE_H_MAX = 40     # horizontal ray max length
SPARKLE_V_MAX = 10     # vertical ray max length

# Face overlay position and size (head center in 320x200 scene)
FACE_CENTER_X = 166
FACE_CENTER_Y = 80
FACE_H = 122  # target height to match background head

# Face animation timing (seconds after zoom completes at 0.8s)
SMILE_TIME_SHORT = 1.0   # end of serious face cycle
SMILE_TIME_LONG = 2.0
BLINK_TIME_SHORT = 1.4   # blink after smile
BLINK_TIME_LONG = 2.0
BLINK_DURATION = 0.3      # how long the blink lasts

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BG_PATH = os.path.join(PROJECT_ROOT, "assets", "backgrounds", "crt_inside.png")
FACE_DIR = os.path.join(PROJECT_ROOT, "assets", "sprites", "face")


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


def _load_face_frames():
    """Load face animation frames, auto-crop, make transparent, add CRT scanlines."""
    frames = []
    i = 0
    while True:
        path = os.path.join(FACE_DIR, f"frame_{i:03d}.png")
        if not os.path.exists(path):
            break
        img = pygame.image.load(path)
        try:
            img = img.convert_alpha()
        except pygame.error:
            pass

        # Make light background transparent with wide soft edge
        w, h = img.get_size()
        for y in range(h):
            for x in range(w):
                r, g, b, a = img.get_at((x, y))
                brightness = (r + g + b) / 3
                if brightness > 210:
                    img.set_at((x, y), (r, g, b, 0))
                elif brightness > 170:
                    fade = int(255 * (210 - brightness) / 40)
                    img.set_at((x, y), (r, g, b, fade))

        # Auto-crop transparent borders
        min_x, min_y, max_x, max_y = w, h, 0, 0
        for y in range(h):
            for x in range(w):
                if img.get_at((x, y))[3] > 10:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        if max_x <= min_x or max_y <= min_y:
            frames.append(img)
            i += 1
            continue

        cropped = img.subsurface((min_x, min_y, max_x - min_x + 1, max_y - min_y + 1))
        cw, ch = cropped.get_size()

        # Use original cropped size (no scaling)
        scaled = cropped.copy()
        new_w = cw
        fy_top = FACE_CENTER_Y - ch // 2

        # CRT scanlines: darken every other row to match background
        for sy in range(ch):
            if (fy_top + sy) % 2 == 1:
                for sx in range(new_w):
                    r, g, b, a = scaled.get_at((sx, sy))
                    if a > 0:
                        scaled.set_at((sx, sy), (int(r * 0.65), int(g * 0.65), int(b * 0.65), a))

        # Feather edges: soften alpha where face meets transparent background
        result = scaled.copy()
        for sy in range(ch):
            for sx in range(new_w):
                r, g, b, a = result.get_at((sx, sy))
                if a > 0:
                    clear = 0
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = sx + dx, sy + dy
                        if 0 <= nx < new_w and 0 <= ny < ch:
                            if scaled.get_at((nx, ny))[3] < 30:
                                clear += 1
                        else:
                            clear += 1
                    if clear >= 2:
                        result.set_at((sx, sy), (r, g, b, a // 3))

        frames.append(result)
        i += 1
    return frames


class CrtInsideScene:
    def __init__(self, cursor, character, ui, short=True):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.short = short
        self.duration = DURATION_SHORT if short else DURATION_LONG
        self.sparkle_delay = SPARKLE_DELAY_SHORT if short else SPARKLE_DELAY_LONG
        self.sparkle_duration = SPARKLE_DURATION_SHORT if short else SPARKLE_DURATION_LONG
        self.smile_time = SMILE_TIME_SHORT if short else SMILE_TIME_LONG
        self.blink_time = BLINK_TIME_SHORT if short else BLINK_TIME_LONG
        self.time = 0.0
        self.done = False
        self.cursor.visible = False
        self.bg = _load_crt_bg()
        self.face_frames = _load_face_frames()

        # Separate serious (0-2) and blink (3-4) frames
        self.serious_frames = self.face_frames[:3] if len(self.face_frames) >= 3 else self.face_frames
        self.blink_frames = self.face_frames[3:] if len(self.face_frames) > 3 else []

    def update(self, dt):
        self.time += dt
        if self.time >= self.duration:
            self.done = True

    def _get_face_overlay(self):
        """Return the face frame to overlay, or None for the background smile."""
        t = self.time

        # Before smile: show serious face with subtle animation
        if t < self.smile_time and self.serious_frames:
            # Cycle through serious frames (0.5s per frame, no repeat)
            idx = min(int(t / 0.5), len(self.serious_frames) - 1)
            return self.serious_frames[idx]

        # Blink: brief eye close
        if self.blink_frames and self.blink_time <= t < self.blink_time + BLINK_DURATION:
            blink_t = t - self.blink_time
            # Quick close-open: frame 0 for first half, frame 1 (or 0) for second half
            if blink_t < BLINK_DURATION / 2:
                return self.blink_frames[0]
            elif len(self.blink_frames) > 1:
                return self.blink_frames[1]
            return self.blink_frames[0]

        # Default: show frame 002 (serious resting face)
        if len(self.serious_frames) >= 3:
            return self.serious_frames[2]
        return self.serious_frames[-1] if self.serious_frames else None

    def draw(self, surface):
        if self.bg is None:
            surface.fill((0, 0, 0))
            return

        # Composite overlays onto a working copy so they zoom with the image
        frame = self.bg.copy()

        # Face animation overlay (convert frame to support alpha blending)
        face = self._get_face_overlay()
        if face is not None:
            fx = FACE_CENTER_X - face.get_width() // 2
            fy = FACE_CENTER_Y - face.get_height() // 2
            # Need a temporary SRCALPHA surface for proper alpha compositing
            tmp = pygame.Surface((320, 200), pygame.SRCALPHA)
            tmp.blit(frame, (0, 0))
            tmp.blit(face, (fx, fy))
            frame = tmp

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
        sparkle_t = self.time - self.sparkle_delay
        if 0 < sparkle_t < self.sparkle_duration:
            phase = sparkle_t / self.sparkle_duration
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
