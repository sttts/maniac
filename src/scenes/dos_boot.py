"""Scene 4: DOS boot — CRT shows MS-DOS booting line by line, C:\\>_ prompt (~2s)."""
from src.pixel_art import draw_dos_screen


DURATION = 2.0

BOOT_LINES = [
    "MS-DOS",
    "",
    "(C)Copyright Microsoft Corp",
    "1981-1990 ver 5.00A",
    "",
    "C:\\> _",
]


class DosBootScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.visible_lines = []
        self.cursor.visible = False

    def update(self, dt):
        self.time += dt

        # Reveal lines over time
        lines_to_show = int(self.time / 0.3) + 1
        self.visible_lines = BOOT_LINES[:min(lines_to_show, len(BOOT_LINES))]

        if self.time >= DURATION:
            self.done = True
            self.cursor.visible = True

    def draw(self, surface):
        # Cursor blink every 0.5s
        cursor_on = int(self.time * 2) % 2 == 0
        draw_dos_screen(surface, self.visible_lines, cursor_visible=cursor_on)

    def get_sound_events(self, start_time):
        from src.sounds import generate_disk_drive, generate_apple2_beep
        return [
            (start_time + 0.2, generate_disk_drive(1.5)),
            (start_time + 1.5, generate_apple2_beep()),  # when C:\> appears
        ]
