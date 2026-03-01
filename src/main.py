"""Entry point — runs the full scene sequence, captures frames, exports MP4."""
import os
import sys
import time

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pygame

from src.renderer import Renderer, FPS, NATIVE_W, NATIVE_H
from src.cursor import Cursor
from src.character import Character
from src.scumm_ui import ScummUI
from src.scenes.living_room import LivingRoom
from src.scenes.computer_room import ComputerRoom
from src.scenes.switch import SwitchScene
from src.scenes.dos_boot import DosBootScene
from src.scenes.flight_sim import FlightSimScene
from src.scenes.record_exe import RecordExeScene
from src.scenes.crt_inside import CrtInsideScene
from src.sounds import generate_sid_music, mix_timeline, save_wav


def build_scenes(cursor, character, ui):
    """Create the scene sequence in order."""
    return [
        LivingRoom(cursor, character, ui),
        ComputerRoom(cursor, character, ui),
        SwitchScene(cursor, character, ui),
        DosBootScene(cursor, character, ui),
        FlightSimScene(cursor, character, ui),
        RecordExeScene(cursor, character, ui),
        CrtInsideScene(cursor, character, ui),
    ]


def collect_sound_events(scenes):
    """Gather all sound events from scenes with correct timing offsets."""
    events = []
    scene_start = 0.0
    durations = [s.DURATION if hasattr(s, "DURATION") else 2.0 for s in scenes]
    # Use module-level DURATION constants
    from src.scenes import living_room, computer_room, switch, dos_boot
    from src.scenes import flight_sim, record_exe, crt_inside
    dur_list = [
        living_room.DURATION, computer_room.DURATION, switch.DURATION,
        dos_boot.DURATION, flight_sim.DURATION, record_exe.DURATION,
        crt_inside.DURATION,
    ]
    for scene, dur in zip(scenes, dur_list):
        events.extend(scene.get_sound_events(scene_start))
        scene_start += dur
    return events, scene_start


def generate_audio(scenes, total_duration, output_dir):
    """Generate and save the full audio track."""
    print("Generating audio...")

    # Collect SFX events
    sfx_events, _ = collect_sound_events(scenes)

    # Generate background music
    music = generate_sid_music(total_duration)
    sfx_events.append((0.0, music))

    # Mix everything
    mixed = mix_timeline(sfx_events, total_duration)

    # Save
    audio_path = os.path.join(output_dir, "audio.wav")
    save_wav(audio_path, mixed)
    print(f"Audio saved: {audio_path}")
    return audio_path


def run(preview=False):
    """Run the full sequence."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    renderer = Renderer(preview=preview)
    cursor = Cursor()
    character = Character()
    ui = ScummUI()

    # Build all scenes upfront (they init lazily where possible)
    scenes_templates = [
        lambda: LivingRoom(cursor, character, ui),
        lambda: ComputerRoom(cursor, character, ui),
        lambda: SwitchScene(cursor, character, ui),
        lambda: DosBootScene(cursor, character, ui),
        lambda: FlightSimScene(cursor, character, ui),
        lambda: RecordExeScene(cursor, character, ui),
        lambda: CrtInsideScene(cursor, character, ui),
    ]

    from src.scenes import living_room, computer_room, switch, dos_boot
    from src.scenes import flight_sim, record_exe, crt_inside
    durations = [
        living_room.DURATION, computer_room.DURATION, switch.DURATION,
        dos_boot.DURATION, flight_sim.DURATION, record_exe.DURATION,
        crt_inside.DURATION,
    ]
    total_duration = sum(durations)
    print(f"Total duration: {total_duration}s ({int(total_duration * FPS)} frames)")

    # Generate audio first (need scenes for sound events)
    temp_scenes = [f() for f in scenes_templates]
    audio_path = generate_audio(temp_scenes, total_duration, output_dir)

    # Re-create scenes for rendering (fresh state)
    cursor = Cursor()
    character = Character()
    ui = ScummUI()
    scenes = [
        LivingRoom(cursor, character, ui),
        ComputerRoom(cursor, character, ui),
        SwitchScene(cursor, character, ui),
        DosBootScene(cursor, character, ui),
        FlightSimScene(cursor, character, ui),
        RecordExeScene(cursor, character, ui),
        CrtInsideScene(cursor, character, ui),
    ]

    # Render frames
    dt = 1.0 / FPS
    frame_num = 0
    scene_idx = 0
    current_scene = scenes[scene_idx]

    print("Rendering frames...")
    clock = pygame.time.Clock()

    while scene_idx < len(scenes):
        current_scene = scenes[scene_idx]

        # Handle pygame events (needed even in headless mode)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                renderer.quit()
                return

        current_scene.update(dt)

        renderer.begin_frame()
        current_scene.draw(renderer.native)
        renderer.end_frame()
        renderer.capture_frame(frame_num)
        frame_num += 1

        if preview:
            clock.tick(FPS)

        if current_scene.done:
            scene_idx += 1
            if scene_idx < len(scenes):
                # Re-init shared state for next scene
                scenes[scene_idx].__init__(cursor, character, ui)

        if frame_num % 30 == 0:
            print(f"  Frame {frame_num}/{int(total_duration * FPS)}")

    print(f"Rendered {frame_num} frames")

    # Export video
    output_path = os.path.join(output_dir, "intro.mp4")
    renderer.export_video(audio_path, output_path)

    # Cleanup
    renderer.cleanup_frames()
    os.remove(audio_path)
    renderer.quit()
    print("Done!")


if __name__ == "__main__":
    preview = "--preview" in sys.argv
    run(preview=preview)
