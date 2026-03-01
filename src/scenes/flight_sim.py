"""Scene 5: Flight simulator — DOS types FLIGHT.EXE, retro top-down flight game auto-plays (~2s)."""
import pygame
from src.pixel_art import draw_dos_screen, draw_flight_sim


DURATION = 2.0


class FlightSimScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.phase = "typing"  # typing → game
        self.typed_chars = 0
        self.command = "FLIGHT.EXE"
        self.scroll_y = 0.0
        self.cursor.visible = False

    def update(self, dt):
        self.time += dt

        if self.phase == "typing":
            # Type command characters
            self.typed_chars = min(len(self.command), int(self.time / 0.06))
            if self.typed_chars >= len(self.command) and self.time > 0.8:
                self.phase = "game"

        elif self.phase == "game":
            self.scroll_y += dt * 60  # scroll speed

        if self.time >= DURATION:
            self.done = True
            self.cursor.visible = True

    def draw(self, surface):
        if self.phase == "typing":
            typed = self.command[:self.typed_chars]
            lines = ["C:\\>" + typed]
            cursor_on = int(self.time * 4) % 2 == 0
            draw_dos_screen(surface, lines, cursor_visible=cursor_on)
        else:
            draw_flight_sim(surface, scroll_y=self.scroll_y)

    def get_sound_events(self, start_time):
        from src.sounds import generate_keypress, generate_flight_hum
        events = []
        # Typing sounds
        for i in range(len(self.command)):
            events.append((start_time + i * 0.06, generate_keypress()))
        # Flight sim engine hum
        events.append((start_time + 0.8, generate_flight_hum(1.2)))
        return events
