"""Stefan character sprite — detailed SCUMM-style pixel art, 3/4 perspective."""
import pygame

# Sprite is defined as a color-indexed pixel map for maximum control.
# 20 wide x 36 tall — larger than before for better detail.
W, H = 20, 36

# Palette indices
_ = None  # transparent
K = 0     # black (outline)
S = 1     # skin
D = 2     # skin shadow
H1 = 3    # hair main
H2 = 4    # hair highlight
B = 5     # beard
G = 6     # glasses frame
L = 7     # glasses lens
E = 8     # eye (pupil)
W1 = 9    # white of eye
C = 10    # hoodie main blue
C2 = 11   # hoodie shadow
C3 = 12   # hoodie highlight
Z = 13    # zipper/hoodie accent
T = 14    # t-shirt (visible at collar)
P = 15    # pants
P2 = 16   # pants shadow
SH = 17   # shoes
SH2 = 18  # shoes highlight
SK = 19   # skin hand

PALETTE = {
    K: (20, 15, 10),
    S: (225, 185, 145),
    D: (190, 150, 110),
    H1: (150, 135, 105),
    H2: (185, 170, 140),
    B: (160, 145, 120),
    G: (50, 40, 30),
    L: (170, 195, 215),
    E: (30, 30, 35),
    W1: (230, 230, 240),
    C: (50, 80, 170),
    C2: (30, 55, 130),
    C3: (75, 110, 200),
    Z: (90, 90, 100),
    T: (140, 145, 150),
    P: (55, 55, 75),
    P2: (40, 40, 55),
    SH: (60, 45, 30),
    SH2: (80, 60, 40),
    SK: (210, 175, 135),
}

# Standing sprite facing right (3/4 view)
# Each row is 20 pixels wide
STAND = [
    # Row 0-3: Hair/top of head
    [_,_,_,_,_,_,H1,H1,H1,H1,H1,H1,H1,_,_,_,_,_,_,_],
    [_,_,_,_,_,H1,H2,H2,H1,H1,H1,H1,H1,H1,_,_,_,_,_,_],
    [_,_,_,_,_,H1,H2,H2,H2,H1,H1,H1,H1,H1,_,_,_,_,_,_],
    [_,_,_,_,_,H1,H1,H2,H1,H1,H1,H1,H1,H1,_,_,_,_,_,_],
    # Row 4-5: Forehead + glasses
    [_,_,_,_,_,K,S,S,S,S,S,S,S,K,_,_,_,_,_,_],
    [_,_,_,_,_,K,S,S,S,S,S,S,D,K,_,_,_,_,_,_],
    # Row 6-7: Eyes with glasses
    [_,_,_,_,_,K,G,G,G,G,G,G,G,K,_,_,_,_,_,_],
    [_,_,_,_,_,K,G,W1,E,G,G,W1,E,K,_,_,_,_,_,_],
    # Row 8: Nose
    [_,_,_,_,_,K,S,S,S,S,D,S,D,K,_,_,_,_,_,_],
    # Row 9-11: Mouth and beard
    [_,_,_,_,_,K,S,B,B,B,B,B,D,K,_,_,_,_,_,_],
    [_,_,_,_,_,_,K,B,B,B,B,B,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,B,B,B,K,_,_,_,_,_,_,_,_],
    # Row 12: Neck
    [_,_,_,_,_,_,_,_,S,S,S,_,_,_,_,_,_,_,_,_],
    # Row 13: Collar (t-shirt visible)
    [_,_,_,_,_,_,C2,T,T,T,T,T,C2,_,_,_,_,_,_,_],
    # Row 14-20: Hoodie body
    [_,_,_,_,_,C2,C,C,C3,Z,Z,C3,C,C,C2,_,_,_,_,_],
    [_,_,_,_,C2,C,C,C,C3,Z,Z,C3,C,C,C,C2,_,_,_,_],
    [_,_,_,_,C2,C,C,C,C,Z,Z,C,C,C,C,C2,_,_,_,_],
    [_,_,_,C2,C2,C,C,C,C,Z,Z,C,C,C,C,C2,C2,_,_,_],
    [_,_,_,C2,C2,C,C,C,C,C,C,C,C,C,C,C2,C2,_,_,_],
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,C2,_,_,_,_],
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,C2,_,_,_,_],
    # Row 21-22: Hoodie bottom + hands
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,C2,_,_,_,_],
    [_,_,_,SK,SK,C2,C,C,C,C,C,C,C,C,C2,SK,SK,_,_,_],
    # Row 23-27: Pants
    [_,_,_,_,_,_,P,P,P,P,P,P,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P,P,P,P,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P,P2,P,P,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P,P2,P,P,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P,_,_,P,P,P,_,_,_,_,_,_],
    # Row 28-30: Lower legs
    [_,_,_,_,_,_,P,P,P2,_,_,P2,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P2,_,_,P2,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P2,P,P2,_,_,P2,P,P2,_,_,_,_,_,_],
    # Row 31-33: Shoes
    [_,_,_,_,_,SH,SH,SH2,SH,_,_,SH,SH2,SH,SH,_,_,_,_,_],
    [_,_,_,_,_,SH,SH,SH2,SH,_,_,SH,SH2,SH,SH,_,_,_,_,_],
    [_,_,_,_,_,SH,SH,SH,SH,_,_,SH,SH,SH,SH,_,_,_,_,_],
    # Row 34-35: padding
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

# Walk frame 2: left foot forward, right foot back
WALK_LEFT_FWD = list(STAND[:27])  # copy upper body
WALK_LEFT_FWD += [
    # Left leg forward, right leg back
    [_,_,_,_,_,P,P,P,P2,_,_,_,P2,P,P,_,_,_,_,_],
    [_,_,_,_,P,P,P,P2,_,_,_,_,_,P2,P,_,_,_,_,_],
    [_,_,_,_,P,P,P,P2,_,_,_,_,_,P2,P,P,_,_,_,_],
    [_,_,_,SH,SH,SH2,SH,SH,_,_,_,_,_,SH,SH2,SH,_,_,_,_],
    [_,_,_,SH,SH,SH,SH,SH,_,_,_,_,_,SH,SH,SH,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

# Walk frame 3: right foot forward, left foot back (mirror of frame 2)
WALK_RIGHT_FWD = list(STAND[:27])
WALK_RIGHT_FWD += [
    [_,_,_,_,_,_,P,P,P2,_,_,P,P,P,P,_,_,_,_,_],
    [_,_,_,_,_,_,P2,P,_,_,_,_,P,P,P,P,_,_,_,_],
    [_,_,_,_,_,P,P2,P,_,_,_,_,P,P,P,P,_,_,_,_],
    [_,_,_,_,SH,SH2,SH,SH,_,_,_,SH,SH,SH2,SH,SH,_,_,_,_],
    [_,_,_,_,SH,SH,SH,SH,_,_,_,SH,SH,SH,SH,SH,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

# Sitting sprite (upper body same, legs bent forward)
SITTING = list(STAND[:23])  # up to hands
SITTING += [
    # Seated: legs extend forward
    [_,_,_,_,_,_,P,P,P,P,P,P,P,P,_,_,_,_,_,_],
    [_,_,_,_,_,_,P,P,P,P,P,P,P,P,P,_,_,_,_,_],
    [_,_,_,_,_,_,_,P,P,P,P,P,P,P,P,P,_,_,_,_],
    [_,_,_,_,_,_,_,_,P2,P,P,P2,P,P,P,P,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,SH,SH,SH2,SH,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,SH,SH,SH,SH,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

# Waving sprite (right arm raised)
WAVING = [
    # Row 0-3: Hair (same)
    STAND[0], STAND[1], STAND[2], STAND[3],
    # Row 4-12: Face (same)
    STAND[4], STAND[5], STAND[6], STAND[7], STAND[8],
    STAND[9], STAND[10], STAND[11], STAND[12],
    # Row 13: collar
    STAND[13],
    # Row 14-22: body with raised right arm
    [_,_,_,_,_,C2,C,C,C3,Z,Z,C3,C,C,C2,C2,_,_,_,_],
    [_,_,_,_,C2,C,C,C,C3,Z,Z,C3,C,C,C,_,C2,_,_,_],
    [_,_,_,_,C2,C,C,C,C,Z,Z,C,C,C,C,_,_,C2,_,_],
    [_,_,_,C2,C2,C,C,C,C,Z,Z,C,C,C,C,_,_,C3,_,_],
    [_,_,_,C2,C2,C,C,C,C,C,C,C,C,C,C,_,_,SK,_,_],
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,_,SK,SK,_,_],
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,C2,_,_,_,_],
    [_,_,_,_,C2,C,C,C,C,C,C,C,C,C,C,C2,_,_,_,_],
    [_,_,_,SK,SK,C2,C,C,C,C,C,C,C,C,C2,_,_,_,_,_],
    # Row 23+: pants/shoes same as standing
    STAND[23], STAND[24], STAND[25], STAND[26], STAND[27],
    STAND[28], STAND[29], STAND[30], STAND[31], STAND[32],
    STAND[33], STAND[34], STAND[35],
]


def _render_sprite(pixel_data):
    """Convert a pixel data grid to a pygame surface."""
    sprite_h = len(pixel_data)
    sprite_w = 20
    s = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for y, row in enumerate(pixel_data):
        for x, idx in enumerate(row):
            if idx is not None and idx in PALETTE:
                s.set_at((x, y), PALETTE[idx])
    return s


class Character:
    def __init__(self):
        self.stand_frame = _render_sprite(STAND)
        self.walk_frames = [
            self.stand_frame,
            _render_sprite(WALK_LEFT_FWD),
            self.stand_frame,
            _render_sprite(WALK_RIGHT_FWD),
        ]
        self.sit_frame = _render_sprite(SITTING)
        self.wave_frame = _render_sprite(WAVING)

        # State
        self.x = 40.0
        self.y = 125.0
        self.state = "stand"
        self.facing = 1       # 1=right, -1=left
        self.walk_speed = 50.0
        self.anim_timer = 0.0
        self.anim_frame = 0

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
        if self.state == "walk" and self._target_x is not None:
            self.anim_timer += dt
            if self.anim_timer >= 0.12:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 4

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

        if self.facing < 0:
            frame = pygame.transform.flip(frame, True, False)

        # Feet anchored at (self.x, self.y)
        draw_x = int(self.x) - frame.get_width() // 2
        draw_y = int(self.y) - frame.get_height()
        surface.blit(frame, (draw_x, draw_y))
