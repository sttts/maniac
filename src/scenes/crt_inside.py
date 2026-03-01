"""Scene 7: CRT inside view — zoom out from REC, Stefan waving, YouTube overlay (~2s)."""
import pygame
from src.pixel_art import draw_crt_inside


DURATION = 2.0


class CrtInsideScene:
    def __init__(self, cursor, character, ui):
        self.cursor = cursor
        self.character = character
        self.ui = ui
        self.time = 0.0
        self.done = False
        self.cursor.visible = False

        # Get the wave frame from character
        self.wave_frame = self.character.wave_frame

    def update(self, dt):
        self.time += dt
        if self.time >= DURATION:
            self.done = True

    def draw(self, surface):
        # Zoom-out effect: start zoomed in on center, scale out
        progress = min(1.0, self.time / 0.8)  # zoom completes in 0.8s
        zoom = 2.0 - progress  # 2.0 → 1.0

        # Draw full CRT scene to a temp surface
        temp = pygame.Surface((320, 144))
        draw_crt_inside(temp, stefan_wave_frame=self.wave_frame)

        if zoom > 1.01:
            # Zoom in on center region
            zw = int(320 / zoom)
            zh = int(144 / zoom)
            zx = (320 - zw) // 2
            zy = (144 - zh) // 2
            cropped = temp.subsurface(pygame.Rect(zx, zy, zw, zh))
            scaled = pygame.transform.scale(cropped, (320, 144))
            surface.blit(scaled, (0, 0))
        else:
            surface.blit(temp, (0, 0))

    def get_sound_events(self, start_time):
        return []  # music continues, no extra SFX needed
