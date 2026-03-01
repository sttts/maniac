"""Scene 2: Computer room — Walk to Chair, sit, Use Microphone, Turn on Computer (~2.5s)."""
from src.pixel_art import draw_computer_room, load_background


DURATION = 3.5

# Chair position in computer room background (in front of desk)
CHAIR_X = 130
CHAIR_Y = 120

# Microphone is on the desk near the monitor
MIC_X = 155
MIC_Y = 60

# Computer monitor position
MONITOR_X = 145
MONITOR_Y = 48


class ComputerRoom:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.bg_cache = None

        # Character enters from bottom-left (came through door)
        self.character.x = 40.0
        self.character.y = 130.0
        self.character.state = "stand"
        self.character.facing = 1

        # Cursor starts visible in center of scene
        self.cursor.teleport(160, 90)
        self.cursor.visible = True

        # Phase tracking
        self._phase = "start"  # start → walk_to_click → walking → sat → use_click → mic_click → turnon_click

    def _on_walkto_verb(self):
        self.ui.select_verb("Walk to")
        self.ui.set_status("Walk to")
        self._phase = "walk_to_chair"

    def _on_chair_click(self):
        self.ui.set_status("Walk to Chair")
        self._phase = "walking"
        # Walk north-east then north to the chair
        self.character.walk_to(CHAIR_X, y=CHAIR_Y, on_arrive=self._on_chair_arrive)

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

        if self.cursor.is_moving():
            pass  # wait for cursor to finish

        # Step 1: cursor moves to "Walk to"
        elif self._phase == "start" and self.time >= 0.15:
            vx, vy = self.ui.get_verb_pos("Walk to")
            self.cursor.move_to(vx, vy, duration=0.3, on_arrive=self._on_walkto_verb)
            self._phase = "moving_to_verb"

        # Step 2: cursor clicks on the chair area
        elif self._phase == "walk_to_chair":
            self.cursor.move_to(CHAIR_X, CHAIR_Y, duration=0.3, on_arrive=self._on_chair_click)
            self._phase = "moving_to_chair"

        # Step 3: after sitting, cursor moves to "Use"
        elif self._phase == "sat":
            vx, vy = self.ui.get_verb_pos("Use")
            self.cursor.move_to(vx, vy, duration=0.3, on_arrive=self._on_use_verb)
            self._phase = "moving_to_use"

        # Step 4: cursor clicks on microphone
        elif self._phase == "use_mic":
            self.cursor.move_to(MIC_X, MIC_Y, duration=0.3, on_arrive=self._on_mic_click)
            self._phase = "moving_to_mic"

        # Step 5: cursor moves to "Turn on"
        elif self._phase == "turnon":
            vx, vy = self.ui.get_verb_pos("Turn on")
            self.cursor.move_to(vx, vy, duration=0.25, on_arrive=self._on_turnon_verb)
            self._phase = "moving_to_turnon"

        # Step 6: cursor clicks on computer monitor
        elif self._phase == "turnon_computer":
            self.cursor.move_to(MONITOR_X, MONITOR_Y, duration=0.25, on_arrive=self._on_computer_click)
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
