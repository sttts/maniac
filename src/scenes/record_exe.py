"""Scene 6: ESC → DOS → RECORD.EXE — exits flight sim, types RECORD.EXE, shows REC screen (~2s)."""
import pygame
from src.pixel_art import draw_dos_screen, draw_rec_screen


DURATION = 2.0


class RecordExeScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.phase = "esc"  # esc → typing → rec
        self.typed_chars = 0
        self.command = "RECORD.EXE"
        self.cursor.visible = False

    def update(self, dt):
        self.time += dt

        if self.phase == "esc" and self.time > 0.3:
            self.phase = "typing"

        if self.phase == "typing":
            typing_time = self.time - 0.3
            self.typed_chars = min(len(self.command), int(typing_time / 0.06))
            if self.typed_chars >= len(self.command) and self.time > 1.2:
                self.phase = "rec"

        if self.time >= DURATION:
            self.done = True
            self.cursor.visible = True

    def draw(self, surface):
        if self.phase == "esc":
            # Show ESC key press overlay on black screen
            surface.fill((0, 0, 0))
            font = pygame.font.SysFont("monospace", 12, bold=True)
            # ESC key box
            pygame.draw.rect(surface, (60, 60, 70), (135, 55, 50, 30))
            pygame.draw.rect(surface, (90, 90, 100), (137, 57, 46, 26))
            esc_text = font.render("ESC", False, (200, 200, 200))
            surface.blit(esc_text, (145, 62))

        elif self.phase == "typing":
            typed = self.command[:self.typed_chars]
            lines = ["C:\\>" + typed]
            cursor_on = int(self.time * 4) % 2 == 0
            draw_dos_screen(surface, lines, cursor_visible=cursor_on)

        else:
            rec_blink = int(self.time * 3) % 2 == 0
            draw_rec_screen(surface, rec_blink=rec_blink)

    def get_sound_events(self, start_time):
        from src.sounds import generate_keypress, generate_click_sound
        events = []
        # ESC keypress
        events.append((start_time + 0.1, generate_keypress()))
        # Typing RECORD.EXE
        for i in range(len(self.command)):
            events.append((start_time + 0.3 + i * 0.06, generate_keypress()))
        # Enter key
        events.append((start_time + 1.15, generate_click_sound()))
        return events
