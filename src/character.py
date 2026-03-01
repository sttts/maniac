import pygame

# Stefan sprite: ~16x30 pixels, 3/4 perspective SCUMM style
# Blue hoodie, glasses, light brown/gray hair, beard

# Color palette
SKIN = (220, 180, 140)
SKIN_SHADE = (190, 150, 110)
HAIR = (160, 140, 110)
HAIR_LIGHT = (190, 175, 150)
BEARD = (150, 135, 115)
HOODIE = (50, 80, 160)
HOODIE_SHADE = (35, 60, 130)
HOODIE_LIGHT = (70, 110, 190)
PANTS = (60, 60, 80)
SHOES = (50, 40, 30)
GLASSES = (60, 50, 40)
GLASSES_LENS = (180, 200, 220)
EYE = (40, 40, 40)
T = (0, 0, 0, 0)  # transparent


def _draw_stefan_base(s, foot_offset=0):
    """Draw Stefan's base sprite on a 16x30 surface."""
    s.fill((0, 0, 0, 0))
    W, H = 16, 30

    # Hair (top of head)
    for x in range(5, 11):
        s.set_at((x, 0), HAIR)
    for x in range(4, 12):
        s.set_at((x, 1), HAIR)
    for x in range(4, 12):
        s.set_at((x, 2), HAIR_LIGHT if x in (6, 7, 8) else HAIR)

    # Face
    for y in range(3, 9):
        for x in range(4, 12):
            s.set_at((x, y), SKIN)
    # Side shading
    for y in range(3, 9):
        s.set_at((4, y), SKIN_SHADE)
        s.set_at((11, y), SKIN_SHADE)

    # Glasses
    for x in range(5, 11):
        s.set_at((x, 4), GLASSES)
    s.set_at((5, 5), GLASSES_LENS)
    s.set_at((6, 5), GLASSES_LENS)
    s.set_at((9, 5), GLASSES_LENS)
    s.set_at((10, 5), GLASSES_LENS)
    s.set_at((7, 5), GLASSES)  # bridge

    # Eyes
    s.set_at((6, 5), EYE)
    s.set_at((9, 5), EYE)

    # Beard
    for y in range(7, 10):
        for x in range(5, 11):
            s.set_at((x, y), BEARD)
    # Chin
    for x in range(6, 10):
        s.set_at((x, 10), BEARD)

    # Hoodie body
    for y in range(10, 21):
        for x in range(3, 13):
            shade = HOODIE_SHADE if x <= 4 or x >= 12 else HOODIE
            if x in (7, 8) and y < 14:
                shade = HOODIE_LIGHT  # zipper highlight
            s.set_at((x, y), shade)

    # Arms
    for y in range(11, 19):
        s.set_at((2, y), HOODIE_SHADE)
        s.set_at((13, y), HOODIE_SHADE)
    # Hands
    s.set_at((2, 19), SKIN)
    s.set_at((13, 19), SKIN)

    # Pants
    for y in range(21, 26):
        for x in range(4, 12):
            s.set_at((x, y), PANTS)

    # Legs/shoes with walk offset
    left_foot_y = 26 + foot_offset
    right_foot_y = 26 - foot_offset

    # Left leg
    for y in range(26, min(30, max(26, left_foot_y + 2))):
        for x in range(4, 8):
            if y < 28:
                s.set_at((x, y), PANTS)
            else:
                s.set_at((x, y), SHOES)
    # Right leg
    for y in range(26, min(30, max(26, right_foot_y + 2))):
        for x in range(8, 12):
            if y < 28:
                s.set_at((x, y), PANTS)
            else:
                s.set_at((x, y), SHOES)

    # Ensure shoes are visible
    for x in range(4, 8):
        s.set_at((x, 28), SHOES)
        s.set_at((x, 29), SHOES)
    for x in range(8, 12):
        s.set_at((x, 28), SHOES)
        s.set_at((x, 29), SHOES)


def _draw_stefan_sitting(s):
    """Draw Stefan sitting (legs bent, lower body shortened)."""
    s.fill((0, 0, 0, 0))

    # Same upper body as standing
    _draw_stefan_base(s)

    # Override lower body for sitting pose: clear legs
    for y in range(21, 30):
        for x in range(0, 16):
            s.set_at((x, y), (0, 0, 0, 0))

    # Seated pants (bent legs going forward)
    for y in range(21, 25):
        for x in range(4, 13):
            s.set_at((x, y), PANTS)
    # Feet pointing down
    for x in range(10, 14):
        s.set_at((x, 25), SHOES)
        s.set_at((x, 26), SHOES)


def _draw_stefan_waving(s):
    """Draw Stefan with right arm raised waving."""
    _draw_stefan_base(s)

    # Override right arm — raise it up
    for y in range(11, 19):
        s.set_at((13, y), (0, 0, 0, 0))

    # Raised arm
    for y in range(4, 11):
        s.set_at((14, y), HOODIE)
    s.set_at((14, 3), SKIN)  # hand
    s.set_at((15, 3), SKIN)
    s.set_at((15, 4), SKIN)


class Character:
    def __init__(self):
        # Generate walk cycle frames
        self.walk_frames = []
        offsets = [0, 1, 0, -1]
        for off in offsets:
            frame = pygame.Surface((16, 30), pygame.SRCALPHA)
            _draw_stefan_base(frame, foot_offset=off)
            self.walk_frames.append(frame)

        # Standing frame
        self.stand_frame = self.walk_frames[0]

        # Sitting frame
        self.sit_frame = pygame.Surface((16, 30), pygame.SRCALPHA)
        _draw_stefan_sitting(self.sit_frame)

        # Waving frame
        self.wave_frame = pygame.Surface((16, 30), pygame.SRCALPHA)
        _draw_stefan_waving(self.wave_frame)

        # State
        self.x = 40.0
        self.y = 110.0     # feet position (bottom of sprite)
        self.state = "stand"  # stand, walk, sit, wave
        self.facing = 1     # 1 = right, -1 = left
        self.walk_speed = 50.0  # pixels per second
        self.anim_timer = 0.0
        self.anim_frame = 0

        # Walk target
        self._target_x = None
        self._on_arrive = None

    def walk_to(self, x, on_arrive=None):
        """Start walking to x position."""
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
        if self.state == "walk" and self._target_x is not None:
            # Animate walk cycle
            self.anim_timer += dt
            if self.anim_timer >= 0.15:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 4

            # Move toward target
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
            frame = self.walk_frames[self.anim_frame]
        elif self.state == "sit":
            frame = self.sit_frame
        elif self.state == "wave":
            frame = self.wave_frame
        else:
            frame = self.stand_frame

        # Flip if facing left
        if self.facing < 0:
            frame = pygame.transform.flip(frame, True, False)

        # Draw with feet at (self.x, self.y)
        draw_x = int(self.x) - frame.get_width() // 2
        draw_y = int(self.y) - frame.get_height()
        surface.blit(frame, (draw_x, draw_y))
