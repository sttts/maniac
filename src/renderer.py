import os
import pygame
import subprocess

# Native SCUMM resolution
NATIVE_W, NATIVE_H = 320, 200
SCALE = 4
OUTPUT_W, OUTPUT_H = NATIVE_W * SCALE, NATIVE_H * SCALE  # 1280x800
# Pad to 16:9 for YouTube
FINAL_W, FINAL_H = 1280, 720
FPS = 30


class Renderer:
    def __init__(self, preview=False):
        os.environ["SDL_VIDEODRIVER"] = "dummy" if not preview else ""
        pygame.init()
        self.preview = preview
        if preview:
            self.screen = pygame.display.set_mode((FINAL_W, FINAL_H))
            pygame.display.set_caption("Maniac Stefan")
        else:
            self.screen = pygame.Surface((FINAL_W, FINAL_H))

        # Native resolution surface — all scenes draw on this
        self.native = pygame.Surface((NATIVE_W, NATIVE_H))
        self.frames = []
        self.frame_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "output", "frames"
        )

    def begin_frame(self):
        """Clear the native surface for a new frame."""
        self.native.fill((0, 0, 0))

    def end_frame(self):
        """Scale native surface up and blit centered onto output."""
        # 4x nearest-neighbor scale
        scaled = pygame.transform.scale(self.native, (OUTPUT_W, OUTPUT_H))

        # Center on 1280x720 (black bars top/bottom: 40px each)
        self.screen.fill((0, 0, 0))
        y_offset = (FINAL_H - OUTPUT_H) // 2  # (720-800)//2 = -40
        self.screen.blit(scaled, (0, y_offset))

        if self.preview:
            pygame.display.flip()

    def capture_frame(self, frame_num):
        """Save current screen to PNG for ffmpeg."""
        os.makedirs(self.frame_dir, exist_ok=True)
        path = os.path.join(self.frame_dir, f"{frame_num:05d}.png")
        pygame.image.save(self.screen, path)

    def export_video(self, audio_path, output_path):
        """Combine PNG sequence + audio into MP4 via ffmpeg."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-r", str(FPS),
            "-i", os.path.join(self.frame_dir, "%05d.png"),
            "-i", audio_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_path,
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"Exported: {output_path}")

    def cleanup_frames(self):
        """Remove temporary frame PNGs."""
        if os.path.exists(self.frame_dir):
            for f in os.listdir(self.frame_dir):
                os.remove(os.path.join(self.frame_dir, f))
            os.rmdir(self.frame_dir)

    def quit(self):
        pygame.quit()
