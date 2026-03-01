"""Stefan character — loads PixelLab-generated sprite animations."""
import os
import pygame

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SPRITE_DIR = os.path.join(PROJECT_ROOT, "assets", "sprites", "stefan")

# Target height for character in the 320x200 scene
TARGET_H = 36


def _load_sprite(path):
    """Load a single RGBA sprite, scaled to TARGET_H."""
    img = pygame.image.load(path)
    try:
        img = img.convert_alpha()
    except pygame.error:
        pass

    # Auto-crop transparent borders
    w, h = img.get_size()
    min_x, min_y, max_x, max_y = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            if img.get_at((x, y))[3] > 10:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    if max_x <= min_x or max_y <= min_y:
        return img

    cropped = img.subsurface((min_x, min_y, max_x - min_x + 1, max_y - min_y + 1))
    cw, ch = cropped.get_size()

    # Scale to target height, preserving aspect ratio
    scale = TARGET_H / ch
    new_w = max(1, int(cw * scale))
    return pygame.transform.scale(cropped, (new_w, TARGET_H))


def _load_frames(directory):
    """Load all frame_NNN.png files from a directory, sorted."""
    frames = []
    if not os.path.isdir(directory):
        return frames
    files = sorted(f for f in os.listdir(directory) if f.startswith("frame_") and f.endswith(".png"))
    for f in files:
        frames.append(_load_sprite(os.path.join(directory, f)))
    return frames


class Character:
    def __init__(self):
        # Idle (breathing) — facing camera (south)
        idle_frames = _load_frames(os.path.join(SPRITE_DIR, "animations", "breathing-idle", "south"))
        self.idle_frames = idle_frames if idle_frames else [pygame.Surface((12, TARGET_H), pygame.SRCALPHA)]

        # Walk east (right)
        walk_frames = _load_frames(os.path.join(SPRITE_DIR, "animations", "walk", "east"))
        self.walk_frames = walk_frames if walk_frames else self.idle_frames

        # Standing rotation: east (side view, facing right)
        east_path = os.path.join(SPRITE_DIR, "rotations", "east.png")
        if os.path.exists(east_path):
            self.stand_frame = _load_sprite(east_path)
        else:
            self.stand_frame = self.idle_frames[0]

        # South facing (front) for idle
        south_path = os.path.join(SPRITE_DIR, "rotations", "south.png")
        if os.path.exists(south_path):
            self.front_frame = _load_sprite(south_path)
        else:
            self.front_frame = self.idle_frames[0]

        # Sit and wave: use front frame as base (we don't have specific frames)
        self.sit_frame = self.front_frame
        self.wave_frame = self.front_frame

        # State
        self.x = 40.0
        self.y = 125.0
        self.state = "stand"
        self.facing = 1       # 1=right, -1=left
        self.walk_speed = 50.0
        self.anim_timer = 0.0
        self.anim_frame = 0
        self.idle_timer = 0.0
        self.idle_frame = 0

        self._target_x = None
        self._on_arrive = None

    def walk_to(self, x, on_arrive=None):
        self._target_x = float(x)
        self._on_arrive = on_arrive
        self.state = "walk"
        self.facing = 1 if x > self.x else -1

    def sit(self):
        self.state = "sit"

    def wave(self):
        self.state = "wave"

    def is_walking(self):
        return self.state == "walk" and self._target_x is not None

    def update(self, dt):
        # Idle breathing animation
        self.idle_timer += dt
        if self.idle_timer >= 0.2:
            self.idle_timer = 0
            self.idle_frame = (self.idle_frame + 1) % len(self.idle_frames)

        if self.state == "walk" and self._target_x is not None:
            # Walk animation
            self.anim_timer += dt
            if self.anim_timer >= 0.1:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(self.walk_frames)

            dx = self._target_x - self.x
            move = self.walk_speed * dt
            if abs(dx) <= move:
                self.x = self._target_x
                self._target_x = None
                self.state = "stand"
                self.anim_frame = 0
                if self._on_arrive:
                    cb = self._on_arrive
                    self._on_arrive = None
                    cb()
            else:
                self.x += move if dx > 0 else -move

    def draw(self, surface):
        if self.state == "walk":
            frame = self.walk_frames[self.anim_frame % len(self.walk_frames)]
        elif self.state == "sit":
            frame = self.sit_frame
        elif self.state == "wave":
            frame = self.wave_frame
        elif self.state == "stand":
            frame = self.stand_frame
        else:
            frame = self.idle_frames[self.idle_frame]

        if self.facing < 0:
            frame = pygame.transform.flip(frame, True, False)

        # Feet anchored at (self.x, self.y)
        draw_x = int(self.x) - frame.get_width() // 2
        draw_y = int(self.y) - frame.get_height()
        surface.blit(frame, (draw_x, draw_y))
