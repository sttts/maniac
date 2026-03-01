"""Scene 2: Computer room — Walk to Chair, sit, Use Microphone, Turn on Computer (~4s)."""
import os
import pygame
from src.pixel_art import draw_computer_room, load_background


DURATION = 5.0

# Spider descends from web on a silk thread
SPIDER_X = 204          # on the wall, right of the poster frame
SPIDER_START_Y = 30     # start: near the web
SPIDER_END_Y = 60       # end: lower on the wall
SPIDER_SPEED = 6.0      # pixels per second

# Waypoint: walk East first to be below desk (SCUMM L-shaped pathfinding)
WAYPOINT_X = 140
WAYPOINT_Y = 130

# Chair position: walk North to sit at desk (feet at desk level, not on top)
CHAIR_X = 140
CHAIR_Y = 100

# Microphone is on the desk near the monitor
MIC_X = 155
MIC_Y = 60

# Computer monitor position
MONITOR_X = 145
MONITOR_Y = 48

# 3D printer on the desk (left side of desk)
PRINTER_X = 46
PRINTER_Y = 44
PRINTER_H = 25  # target height in native pixels


def _load_printer_frames():
    """Load animated 3D printer sprite frames from assets/sprites/printer/."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    printer_dir = os.path.join(project_root, "assets", "sprites", "printer")
    frames = []
    i = 0
    while True:
        path = os.path.join(printer_dir, f"frame_{i:03d}.png")
        if not os.path.exists(path):
            break
        img = pygame.image.load(path)
        try:
            img = img.convert_alpha()
        except pygame.error:
            pass

        # Scale to target height
        w, h = img.get_size()
        scale = PRINTER_H / h
        new_w = max(1, int(w * scale))
        frames.append(pygame.transform.scale(img, (new_w, PRINTER_H)))
        i += 1
    return frames


class ComputerRoom:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.bg_cache = None

        # Animated 3D printer
        self.printer_frames = _load_printer_frames()
        self.printer_anim_timer = 0.0
        self.printer_frame_idx = 0

        # Spider descending on silk thread
        self.spider_y = float(SPIDER_START_Y)

        # Character enters from bottom-left (came through door)
        self.character.x = 40.0
        self.character.y = 130.0
        self.character.state = "stand"
        self.character.facing = 1

        # Cursor starts visible in center of scene
        self.cursor.teleport(160, 90)
        self.cursor.visible = True
        self.ui.set_status("")

        # Phase tracking
        self._phase = "start"

    def _on_walkto_verb(self):
        self.ui.select_verb("Walk to")
        self.ui.set_status("Walk to")
        self._phase = "walk_to_chair"

    def _on_chair_click(self):
        self.ui.set_status("Walk to Chair")
        self._phase = "walking_ne"
        # Phase 1: walk NE to waypoint
        self.character.walk_to(WAYPOINT_X, y=WAYPOINT_Y, on_arrive=self._on_waypoint)

    def _on_waypoint(self):
        # Phase 2: walk N to chair
        self.character.walk_to(CHAIR_X, y=CHAIR_Y, on_arrive=self._on_chair_arrive)
        self._phase = "walking_n"

    def _on_chair_arrive(self):
        self.character.sit()
        self._phase = "sat"

    def _on_use_verb(self):
        self.ui.select_verb("Use")
        self.ui.set_status("Use")
        self._phase = "use_mic"

    def _on_mic_click(self):
        self.ui.set_status("Use Microphone")
        self._phase = "turnon"

    def _on_turnon_verb(self):
        self.ui.select_verb("Turn on")
        self.ui.set_status("Turn on")
        self._phase = "turnon_computer"

    def _on_computer_click(self):
        self.ui.set_status("Turn on Computer")
        self._phase = "done_actions"

    def update(self, dt):
        self.time += dt
        self.cursor.update(dt)
        self.character.update(dt)
        self.ui.update(dt, self.cursor.x, self.cursor.y)

        # Spider descends slowly
        self.spider_y = min(SPIDER_END_Y, self.spider_y + SPIDER_SPEED * dt)

        # 3D printer animation (130ms per frame, matching GIF)
        if self.printer_frames:
            self.printer_anim_timer += dt
            if self.printer_anim_timer >= 0.13:
                self.printer_anim_timer -= 0.13
                self.printer_frame_idx = (self.printer_frame_idx + 1) % len(self.printer_frames)

        if self.cursor.is_moving():
            pass  # wait for cursor to finish

        # Step 1: cursor moves to "Walk to"
        elif self._phase == "start" and self.time >= 0.15:
            vx, vy = self.ui.get_verb_pos("Walk to")
            self.cursor.move_to(vx, vy, duration=0.6, on_arrive=self._on_walkto_verb)
            self._phase = "moving_to_verb"

        # Step 2: cursor clicks on the chair area
        elif self._phase == "walk_to_chair":
            self.cursor.move_to(CHAIR_X, CHAIR_Y, duration=0.6, on_arrive=self._on_chair_click)
            self._phase = "moving_to_chair"

        # Step 3: after sitting, cursor moves to "Use"
        elif self._phase == "sat":
            vx, vy = self.ui.get_verb_pos("Use")
            self.cursor.move_to(vx, vy, duration=0.6, on_arrive=self._on_use_verb)
            self._phase = "moving_to_use"

        # Step 4: cursor clicks on microphone
        elif self._phase == "use_mic":
            self.cursor.move_to(MIC_X, MIC_Y, duration=0.6, on_arrive=self._on_mic_click)
            self._phase = "moving_to_mic"

        # Step 5: cursor moves to "Turn on"
        elif self._phase == "turnon":
            vx, vy = self.ui.get_verb_pos("Turn on")
            self.cursor.move_to(vx, vy, duration=0.6, on_arrive=self._on_turnon_verb)
            self._phase = "moving_to_turnon"

        # Step 6: cursor clicks on computer monitor
        elif self._phase == "turnon_computer":
            self.cursor.move_to(MONITOR_X, MONITOR_Y, duration=0.6, on_arrive=self._on_computer_click)
            self._phase = "moving_to_computer"

        if self.time >= DURATION:
            self.done = True

    def draw(self, surface):
        if self.bg_cache is None:
            bg = load_background("computer_room.png")
            if bg:
                self.bg_cache = surface.copy()
                self.bg_cache.blit(bg, (0, 0))
            else:
                self.bg_cache = surface.copy()
                draw_computer_room(self.bg_cache)
        surface.blit(self.bg_cache, (0, 0))

        # Draw spider silk thread and spider
        sx = SPIDER_X
        sy = int(self.spider_y)
        pygame.draw.line(surface, (210, 210, 200), (sx, SPIDER_START_Y), (sx, sy), 1)

        # Spider: round body with 4 bent leg pairs
        dark = (25, 15, 8)
        brown = (50, 35, 18)

        # Body: round abdomen + smaller head
        pygame.draw.circle(surface, dark, (sx, sy + 3), 2)
        surface.set_at((sx, sy + 1), brown)

        # Legs: 4 pairs, bent outward like a real spider (knee-elbow shape)
        # Each leg: body → knee (outward), knee → foot (downward)
        for side in (-1, 1):
            # Front legs: up and out
            surface.set_at((sx + 2 * side, sy), dark)
            surface.set_at((sx + 3 * side, sy - 1), dark)
            # Mid-front legs: out
            surface.set_at((sx + 2 * side, sy + 2), dark)
            surface.set_at((sx + 3 * side, sy + 1), dark)
            # Mid-back legs: out and down
            surface.set_at((sx + 2 * side, sy + 3), dark)
            surface.set_at((sx + 3 * side, sy + 4), dark)
            # Back legs: down and out
            surface.set_at((sx + 2 * side, sy + 4), dark)
            surface.set_at((sx + 3 * side, sy + 5), dark)

        # Draw animated 3D printer
        if self.printer_frames:
            frame = self.printer_frames[self.printer_frame_idx]
            surface.blit(frame, (PRINTER_X, PRINTER_Y))

        self.character.draw(surface)
        self.ui.draw(surface)
        self.cursor.draw(surface)

    def get_sound_events(self, start_time):
        from src.sounds import generate_click_sound
        click = generate_click_sound()
        return [
            (start_time + 0.45, click),  # Walk to click
            (start_time + 0.75, click),  # Chair click
            (start_time + 1.4, click),   # Use click
            (start_time + 1.7, click),   # Mic click
            (start_time + 2.0, click),   # Turn on click
            (start_time + 2.25, click),  # Computer click
        ]
