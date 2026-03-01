"""Scene 1: Living room — cursor clicks 'Walk to', then clicks door, character walks to door (~2.5s)."""
from src.pixel_art import draw_living_room, load_background


DURATION = 2.5

# Door is at the right edge of the background
DOOR_X = 300
DOOR_Y = 80


class LivingRoom:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.bg_cache = None

        # Place character left of center, feet on floor
        self.character.x = 80.0
        self.character.y = 130.0
        self.character.state = "stand"
        self.character.facing = 1

        # Cursor starts visible in the middle of the scene
        self.cursor.teleport(160, 90)
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

        # Step 1: cursor moves to "Walk to" verb (slow enough to see)
        if self.time >= 0.2 and not self._started:
            self._started = True
            vx, vy = self.ui.get_verb_pos("Walk to")
            self.cursor.move_to(vx, vy, duration=0.5, on_arrive=self._on_verb_arrive)

        # Step 2: after clicking verb, cursor moves to door in the scene
        if self._verb_clicked and not self._door_clicked and not self.cursor.is_moving():
            self.cursor.move_to(DOOR_X, DOOR_Y, duration=0.5, on_arrive=self._on_door_arrive)

        if self.time >= DURATION:
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
        self.character.draw(surface)
        self.ui.draw(surface)
        self.cursor.draw(surface)

    def get_sound_events(self, start_time):
        """Return (time, sound_array) tuples for this scene."""
        from src.sounds import generate_click_sound
        click = generate_click_sound()
        return [
            (start_time + 0.7, click),   # verb click
            (start_time + 1.2, click),   # door click
        ]
