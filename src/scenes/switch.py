"""Scene 3: Switch close-up — cursor clicks 'Turn on', hand flips switch, LED lights up (~1.5s)."""
from src.pixel_art import draw_switch_closeup, draw_switch_on


DURATION = 1.5


class SwitchScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.switch_on = False

        self.cursor.teleport(160, 60)
        self.ui.selected_verb = None
        self.ui.set_status("")

        self._verb_clicked = False
        self._switch_clicked = False

    def _on_verb_arrive(self):
        self.ui.select_verb("Turn on")
        self.ui.set_status("Turn on")
        self._verb_clicked = True

    def _on_switch_arrive(self):
        self.ui.set_status("Turn on Computer")
        self._switch_clicked = True
        self.switch_on = True

    def update(self, dt):
        self.time += dt
        self.cursor.update(dt)
        self.ui.update(dt, self.cursor.x, self.cursor.y)

        # Move cursor to "Turn on" verb
        if self.time >= 0.1 and not self._verb_clicked and not self.cursor.is_moving():
            vx, vy = self.ui.get_verb_pos("Turn on")
            self.cursor.move_to(vx, vy, duration=0.25, on_arrive=self._on_verb_arrive)

        # Move cursor to switch
        if self._verb_clicked and not self._switch_clicked and not self.cursor.is_moving():
            self.cursor.move_to(160, 72, duration=0.25, on_arrive=self._on_switch_arrive)

        if self.time >= DURATION:
            self.done = True

    def draw(self, surface):
        if self.switch_on:
            draw_switch_on(surface)
        else:
            draw_switch_closeup(surface)
        self.ui.draw(surface)
        self.cursor.draw(surface)

    def get_sound_events(self, start_time):
        from src.sounds import generate_click_sound, generate_boot_beep
        click = generate_click_sound()
        return [
            (start_time + 0.35, click),       # Turn on click
            (start_time + 0.75, click),        # switch click
            (start_time + 0.8, generate_boot_beep()),  # power beep
        ]
