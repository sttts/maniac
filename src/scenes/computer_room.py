"""Scene 2: Computer room — character enters, walks to desk, sits, cursor clicks Use → Microphone (~2s)."""
from src.pixel_art import draw_computer_room, load_background


DURATION = 2.0
DESK_X = 175


class ComputerRoom:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.bg_cache = None

        # Character enters from left
        self.character.x = 10.0
        self.character.y = 134.0
        self.character.state = "walk"
        self.character.facing = 1
        self.character.walk_to(DESK_X, on_arrive=self._on_desk_arrive)

        self.cursor.teleport(160, 60)
        self._sat_down = False
        self._use_clicked = False

    def _on_desk_arrive(self):
        self.character.sit()
        self._sat_down = True

    def _on_use_arrive(self):
        self.ui.select_verb("Use")
        self.ui.set_status("Use")
        self._use_clicked = True

    def _on_mic_arrive(self):
        self.ui.set_status("Use Microphone")

    def update(self, dt):
        self.time += dt
        self.cursor.update(dt)
        self.character.update(dt)
        self.ui.update(dt, self.cursor.x, self.cursor.y)

        # After sitting, move cursor to "Use" verb
        if self._sat_down and not self._use_clicked and not self.cursor.is_moving():
            vx, vy = self.ui.get_verb_pos("Use")
            self.cursor.move_to(vx, vy, duration=0.25, on_arrive=self._on_use_arrive)

        # After clicking Use, move cursor to microphone
        if self._use_clicked and not self.cursor.is_moving() and self.ui.status_text == "Use":
            self.cursor.move_to(242, 52, duration=0.25, on_arrive=self._on_mic_arrive)

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
            (start_time + 1.1, click),  # Use click
            (start_time + 1.5, click),  # Microphone click
        ]
