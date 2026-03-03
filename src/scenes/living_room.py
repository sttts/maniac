"""Scene 1: Living room — cursor clicks 'Walk to', then clicks door, character walks to door (~3.5s)."""
import math
import os
import pygame
from src.pixel_art import draw_living_room, load_background


DURATION_SHORT = 2.5
DURATION_LONG = 3.5

# Door is at the far right edge of the background
DOOR_X = 314
DOOR_Y = 80

# Cat position on the red towel (right side of couch)
CAT_X = 254
CAT_Y = 71
CAT_H = 35  # target height in native pixels

# Sofa person position and animation
SOFA_X = 229
SOFA_Y = 55
SOFA_ANIM_FPS = 1.0 / 0.13  # 130ms per frame
SOFA_ANIM_START = 0.5  # start page turn after 0.5s

# Clock pendulum: pivot point below clock face, swings left/right
PENDULUM_PIVOT_X = 165
PENDULUM_PIVOT_Y = 62
PENDULUM_LENGTH = 14
PENDULUM_PERIOD = 1.5  # seconds for full swing cycle
PENDULUM_ANGLE = 0.25  # max angle in radians (~14 degrees)


def _load_sofa_frames():
    """Load sofa animation frames, cropped to union bounding box for pixel-perfect alignment."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    anim_dir = os.path.join(project_root, "assets", "sprites", "sofa_anim")

    # First pass: load raw frames and find union bounding box
    raw = []
    u_min_x, u_min_y, u_max_x, u_max_y = 9999, 9999, 0, 0
    i = 0
    while True:
        path = os.path.join(anim_dir, f"frame_{i:03d}.png")
        if not os.path.exists(path):
            break
        img = pygame.image.load(path)
        try:
            img = img.convert_alpha()
        except pygame.error:
            pass
        raw.append(img)
        w, h = img.get_size()
        for y in range(h):
            for x in range(w):
                if img.get_at((x, y))[3] > 10:
                    u_min_x = min(u_min_x, x)
                    u_min_y = min(u_min_y, y)
                    u_max_x = max(u_max_x, x)
                    u_max_y = max(u_max_y, y)
        i += 1

    if not raw or u_max_x <= u_min_x:
        return []

    # Second pass: crop all frames to the same union box
    crop_w = u_max_x - u_min_x + 1
    crop_h = u_max_y - u_min_y + 1
    frames = []
    for img in raw:
        frames.append(img.subsurface((u_min_x, u_min_y, crop_w, crop_h)))
    return frames


def _load_cat_frames():
    """Load animated cat sprite frames from assets/sprites/cat/."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    cat_dir = os.path.join(project_root, "assets", "sprites", "cat")
    frames = []
    i = 0
    while True:
        path = os.path.join(cat_dir, f"frame_{i:03d}.png")
        if not os.path.exists(path):
            break
        img = pygame.image.load(path)
        try:
            img = img.convert_alpha()
        except pygame.error:
            pass

        # Scale to target height
        w, h = img.get_size()
        scale = CAT_H / h
        new_w = max(1, int(w * scale))
        frames.append(pygame.transform.scale(img, (new_w, CAT_H)))
        i += 1
    return frames


class LivingRoom:
    def __init__(self, cursor, character, ui, short=True):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.short = short
        self.duration = DURATION_SHORT if short else DURATION_LONG
        self.time = 0.0
        self.done = False
        self.bg_cache = None

        # Timing parameters
        self._start_delay = 0.1 if short else 0.2
        self._cursor_speed = 0.5 if short else 0.8

        # Animated cat
        self.cat_frames = _load_cat_frames()
        self.cat_anim_timer = 0.0
        self.cat_frame_idx = 0

        # Sofa person: frame 0 is resting, plays animation twice
        self.sofa_frames = _load_sofa_frames()
        anim_len = len(self.sofa_frames) / SOFA_ANIM_FPS if self.sofa_frames else 0
        self.sofa_anim_starts = [SOFA_ANIM_START, self.duration - 0.5 - anim_len]

        # Place character left of center, feet on floor
        self.character.x = 80.0
        self.character.y = 130.0
        self.character.state = "stand"
        self.character.facing = 1

        # Cursor starts on the verb bar (visible against black background)
        self.cursor.teleport(160, 155)
        self.cursor.visible = True

        # Event flags
        self._verb_clicked = False
        self._door_clicked = False
        self._started = False

    def _on_verb_arrive(self):
        self.ui.select_verb("Walk to")
        self.ui.set_status("Walk to")
        self._verb_clicked = True

    def _on_door_arrive(self):
        self.ui.set_status("Walk to Door")
        self._door_clicked = True
        self.character.walk_to(DOOR_X, y=self.character.y)

    def update(self, dt):
        self.time += dt
        self.cursor.update(dt)
        self.character.update(dt)
        self.ui.update(dt, self.cursor.x, self.cursor.y)

        # Cat breathing animation (200ms per frame, matching GIF)
        if self.cat_frames:
            self.cat_anim_timer += dt
            if self.cat_anim_timer >= 0.2:
                self.cat_anim_timer -= 0.2
                self.cat_frame_idx = (self.cat_frame_idx + 1) % len(self.cat_frames)

        # Step 1: cursor moves to "Walk to" verb
        if self.time >= self._start_delay and not self._started:
            self._started = True
            vx, vy = self.ui.get_verb_pos("Walk to")
            self.cursor.move_to(vx, vy, duration=self._cursor_speed, on_arrive=self._on_verb_arrive)

        # Step 2: after clicking verb, cursor moves to door in the scene
        if self._verb_clicked and not self._door_clicked and not self.cursor.is_moving():
            self.cursor.move_to(DOOR_X, DOOR_Y, duration=self._cursor_speed, on_arrive=self._on_door_arrive)

        if self.time >= self.duration:
            self.done = True

    def draw(self, surface):
        if self.bg_cache is None:
            bg = load_background("living_room.png")
            if bg:
                self.bg_cache = surface.copy()
                self.bg_cache.blit(bg, (0, 0))
            else:
                self.bg_cache = surface.copy()
                draw_living_room(self.bg_cache)
        surface.blit(self.bg_cache, (0, 0))

        # Draw swinging pendulum on the grandfather clock
        angle = math.sin(self.time * 2 * math.pi / PENDULUM_PERIOD) * PENDULUM_ANGLE
        bob_x = PENDULUM_PIVOT_X + int(math.sin(angle) * PENDULUM_LENGTH)
        bob_y = PENDULUM_PIVOT_Y + int(math.cos(angle) * PENDULUM_LENGTH)
        pygame.draw.line(surface, (180, 160, 60), (PENDULUM_PIVOT_X, PENDULUM_PIVOT_Y), (bob_x, bob_y), 1)
        pygame.draw.circle(surface, (200, 180, 60), (bob_x, bob_y), 3)

        # Draw animated cat on the couch
        if self.cat_frames:
            cat_frame = self.cat_frames[self.cat_frame_idx]
            surface.blit(cat_frame, (CAT_X, CAT_Y))

        # Draw sofa person (play animation at each scheduled start, rest on frame 0)
        if self.sofa_frames:
            frame = self.sofa_frames[0]
            for start in self.sofa_anim_starts:
                anim_t = self.time - start
                if 0 <= anim_t:
                    idx = int(anim_t * SOFA_ANIM_FPS)
                    if idx < len(self.sofa_frames):
                        frame = self.sofa_frames[idx]
                        break
            surface.blit(frame, (SOFA_X, SOFA_Y))

        self.character.draw(surface)
        self.ui.draw(surface)
        self.cursor.draw(surface)

    def get_sound_events(self, start_time):
        """Return (time, sound_array) tuples for this scene."""
        from src.sounds import generate_click_sound
        click = generate_click_sound()
        if self.short:
            return [
                (start_time + 0.4, click),   # verb click
                (start_time + 0.8, click),   # door click
            ]
        return [
            (start_time + 0.7, click),   # verb click
            (start_time + 1.2, click),   # door click
        ]
