"""Scene 6: DOS prompt → Desktop → YouTube Studio — click Record."""
import pygame
from src.pixel_art import draw_dos_screen, draw_rec_screen
from src.font import draw_text, draw_text_centered


DURATION_SHORT = 2.5
DURATION_LONG = 5.0

WIN_COMMAND = "win"


def _draw_desktop(surface):
    """Draw a retro desktop with YouTube Studio window."""
    # Desktop background — teal/cyan like classic Windows
    surface.fill((0, 128, 128))

    # Desktop icons (left column)
    icon_color = (255, 255, 255)

    # My Computer icon
    pygame.draw.rect(surface, (180, 180, 190), (10, 8, 16, 12))
    pygame.draw.rect(surface, (60, 60, 200), (12, 10, 12, 8))
    draw_text(surface, 8, 22, "My Computer", icon_color)

    # Recycle Bin
    pygame.draw.rect(surface, (180, 180, 180), (10, 38, 14, 16))
    pygame.draw.rect(surface, (160, 160, 160), (12, 36, 10, 4))
    draw_text(surface, 6, 56, "Recycle Bin", icon_color)

    # YouTube Studio window — centered, large
    win_x, win_y = 60, 16
    win_w, win_h = 200, 104

    # Window frame
    pygame.draw.rect(surface, (200, 200, 200), (win_x, win_y, win_w, win_h))
    pygame.draw.rect(surface, (0, 0, 128), (win_x, win_y, win_w, 12))
    draw_text(surface, win_x + 3, win_y + 3, "YouTube Studio", (255, 255, 255))

    # Close/minimize/maximize buttons
    bx = win_x + win_w - 11
    pygame.draw.rect(surface, (192, 192, 192), (bx, win_y + 1, 10, 10))
    draw_text(surface, bx + 2, win_y + 2, "X", (0, 0, 0))

    # YouTube Studio content area
    cx, cy = win_x + 2, win_y + 14
    cw, ch = win_w - 4, win_h - 16
    pygame.draw.rect(surface, (255, 255, 255), (cx, cy, cw, ch))

    # Channel dashboard area
    pygame.draw.rect(surface, (245, 245, 245), (cx + 2, cy + 4, cw - 4, ch - 6))

    # Channel name
    draw_text(surface, cx + 6, cy + 8, "Stefan's Channel", (30, 30, 30))

    # Stats boxes
    draw_text(surface, cx + 6, cy + 20, "Views: 1,337", (80, 80, 80))
    draw_text(surface, cx + 6, cy + 30, "Subs: 42", (80, 80, 80))

    # Big red RECORD / GO LIVE button
    btn_x = cx + cw // 2 - 35
    btn_y = cy + 48
    pygame.draw.rect(surface, (204, 0, 0), (btn_x, btn_y, 70, 20))
    pygame.draw.rect(surface, (255, 0, 0), (btn_x + 1, btn_y + 1, 68, 18))
    draw_text(surface, btn_x + 10, btn_y + 7, "RECORD", (255, 255, 255))

    # Taskbar at bottom
    pygame.draw.rect(surface, (192, 192, 192), (0, 126, 320, 10))
    pygame.draw.rect(surface, (128, 128, 128), (0, 126, 320, 1))

    # Start button
    pygame.draw.rect(surface, (192, 192, 192), (2, 127, 36, 8))
    draw_text(surface, 4, 128, "Start", (0, 0, 0))

    return btn_x, btn_y


# Record button position (returned by _draw_desktop)
REC_BTN_X = 155
REC_BTN_Y = 94


class RecordExeScene:
    def __init__(self, cursor, character, ui, short=True):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.short = short
        self.duration = DURATION_SHORT if short else DURATION_LONG
        self.time = 0.0
        self.done = False
        self.cursor.visible = False
        self.bg_cache = None
        self._phase_started = False
        self._phase_delay = 0.0

        # Phase timing depends on version
        if short:
            self.dos_prompt_end = 0.5
            self.phase = "dos_prompt"
        else:
            self.esc_end = 0.5
            self.dos_prompt_end = 1.3
            self.phase = "esc"

        self.desktop_start = self.dos_prompt_end

        # DOS prompt typing state
        self.dos_typed_chars = 0

    def _on_use_verb(self):
        self.ui.select_verb("Use")
        self.ui.set_status("Use")
        self.phase = "yt_click"
        self._phase_started = False
        self._phase_delay = self.time + 0.3

    def _on_yt_click(self):
        self.ui.set_status("Use YouTube Studio")
        self.phase = "rec_click"
        self._phase_started = False
        self._phase_delay = self.time + 0.4

    def _on_rec_click(self):
        self.ui.set_status("Use Record Button")
        self.phase = "recording" if not self.short else "done"

    def update(self, dt):
        self.time += dt
        self.cursor.update(dt)
        self.ui.update(dt, self.cursor.x, self.cursor.y)

        # Long only: ESC key shown briefly
        if self.phase == "esc" and self.time > self.esc_end:
            self.phase = "dos_prompt"

        # Phase: DOS prompt typing "win"
        if self.phase == "dos_prompt":
            dos_time = self.time if self.short else self.time - self.esc_end
            self.dos_typed_chars = min(len(WIN_COMMAND), int(dos_time / 0.08))
            if self.time > self.dos_prompt_end:
                self.phase = "desktop"
                self.cursor.visible = True
                self.cursor.teleport(160, 70)
                self._phase_delay = self.time + (0.2 if self.short else 0.3)

        # Short: cursor goes directly to Record button
        # Long: cursor goes to "Use" verb first
        if self.phase == "desktop" and not self._phase_started and not self.cursor.is_moving():
            if self.time >= self._phase_delay:
                self._phase_started = True
                if self.short:
                    self.phase = "rec_click"
                    self.cursor.move_to(REC_BTN_X, REC_BTN_Y, duration=0.4, on_arrive=self._on_rec_click)
                else:
                    vx, vy = self.ui.get_verb_pos("Use")
                    self.cursor.move_to(vx, vy, duration=0.5, on_arrive=self._on_use_verb)

        # Long only: cursor clicks on YouTube Studio window title
        if self.phase == "yt_click" and not self._phase_started and not self.cursor.is_moving():
            if self.time >= self._phase_delay:
                self._phase_started = True
                self.cursor.move_to(155, 35, duration=0.5, on_arrive=self._on_yt_click)

        # Long only: cursor clicks Record button
        if self.phase == "rec_click" and not self._phase_started and not self.cursor.is_moving():
            if self.time >= self._phase_delay:
                self._phase_started = True
                self.cursor.move_to(REC_BTN_X, REC_BTN_Y, duration=0.4, on_arrive=self._on_rec_click)

        if self.time >= self.duration:
            self.done = True

    def draw(self, surface):
        # Long only: ESC key press overlay
        if self.phase == "esc":
            surface.fill((0, 0, 0))
            pygame.draw.rect(surface, (50, 50, 58), (130, 50, 60, 36))
            pygame.draw.rect(surface, (80, 80, 90), (132, 52, 56, 32))
            pygame.draw.rect(surface, (95, 95, 105), (132, 52, 56, 3))
            pygame.draw.rect(surface, (65, 65, 72), (132, 81, 56, 3))
            draw_text_centered(surface, 160, 63, "ESC", (200, 200, 200))

        elif self.phase == "dos_prompt":
            # DOS prompt typing "win"
            typed = WIN_COMMAND[:self.dos_typed_chars]
            lines = [
                "MS-DOS",
                "",
                "(C)Copyright Microsoft Corp",
                "1981-1990 ver 5.00A",
                "",
                "C:\\> " + typed,
            ]
            cursor_on = int(self.time * 4) % 2 == 0
            draw_dos_screen(surface, lines, cursor_visible=cursor_on)

        elif self.phase == "recording":
            # Long only: REC screen with blinking dot
            rec_blink = int(self.time * 3) % 2 == 0
            draw_rec_screen(surface, rec_blink=rec_blink)

        else:
            # Desktop with YouTube Studio
            if self.bg_cache is None:
                self.bg_cache = surface.copy()
                _draw_desktop(self.bg_cache)
            surface.blit(self.bg_cache, (0, 0))
            self.ui.draw(surface)
            self.cursor.draw(surface)
            return

        # Non-desktop phases: draw cursor but no UI
        if self.phase != "recording":
            self.cursor.draw(surface)

    def get_sound_events(self, start_time):
        from src.sounds import generate_keypress, generate_click_sound, generate_mac_bong
        events = []

        if not self.short:
            # ESC keypress
            events.append((start_time + 0.1, generate_keypress()))

        # DOS "win" typing
        typing_start = 0.0 if self.short else self.esc_end
        for i in range(len(WIN_COMMAND)):
            events.append((start_time + typing_start + i * 0.08, generate_keypress()))

        # Enter key
        events.append((start_time + typing_start + len(WIN_COMMAND) * 0.08, generate_keypress()))

        # Mac Classic startup bong when desktop appears
        events.append((start_time + self.desktop_start, generate_mac_bong()))

        if self.short:
            # Record button click only
            events.append((start_time + self.desktop_start + 0.6, generate_click_sound()))
        else:
            # Use verb click, YouTube Studio click, Record button click
            events.append((start_time + self.desktop_start + 0.8, generate_click_sound()))
            events.append((start_time + self.desktop_start + 1.6, generate_click_sound()))
            events.append((start_time + self.desktop_start + 2.4, generate_click_sound()))
        return events
