"""Entry point — runs the full scene sequence, captures frames, exports MP4."""
import os
import sys
import time

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
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
from src.sounds import generate_sid_music, generate_outro, mix_timeline, save_wav, SAMPLE_RATE


def _reinit_scene(scene, cursor, character, ui, short):
    """Re-init a scene, passing short= only if supported (FlightSimScene doesn't take it)."""
    if isinstance(scene, FlightSimScene):
        scene.__init__(cursor, character, ui)
    else:
        scene.__init__(cursor, character, ui, short=short)


def build_scenes(cursor, character, ui, short=True):
    """Create the scene sequence in order."""
    scenes = [
        LivingRoom(cursor, character, ui, short=short),
        ComputerRoom(cursor, character, ui, short=short),
        SwitchScene(cursor, character, ui, short=short),
        DosBootScene(cursor, character, ui, short=short),
    ]
    # Long version includes flight simulator
    if not short:
        scenes.append(FlightSimScene(cursor, character, ui))
    scenes.append(RecordExeScene(cursor, character, ui, short=short))
    scenes.append(CrtInsideScene(cursor, character, ui, short=short))
    return scenes


def get_durations(short=True):
    """Get scene durations for the given version."""
    from src.scenes import living_room, computer_room, dos_boot
    from src.scenes import flight_sim, record_exe, crt_inside
    durations = [
        living_room.DURATION_SHORT if short else living_room.DURATION_LONG,
        computer_room.DURATION_SHORT if short else computer_room.DURATION_LONG,
        1.5,  # switch (same for both)
        dos_boot.DURATION_SHORT if short else dos_boot.DURATION_LONG,
    ]
    if not short:
        durations.append(flight_sim.DURATION)
    durations.append(record_exe.DURATION_SHORT if short else record_exe.DURATION_LONG)
    durations.append(crt_inside.DURATION_SHORT if short else crt_inside.DURATION_LONG)
    return durations


def collect_sound_events(scenes, durations):
    """Gather all sound events from scenes with correct timing offsets."""
    events = []
    scene_start = 0.0
    for scene, dur in zip(scenes, durations):
        events.extend(scene.get_sound_events(scene_start))
        scene_start += dur
    return events, scene_start


def generate_audio(scenes, durations, total_duration, output_dir):
    """Generate and save the full audio track."""
    print("  Generating audio...")

    # Collect SFX events
    sfx_events, _ = collect_sound_events(scenes, durations)

    # CRT scene is always last; get its duration
    crt_duration = durations[-1]
    outro_start = total_duration - crt_duration
    music = generate_sid_music(total_duration)

    # Fade music out over 2s leading into the CRT scene
    fade_start = int((outro_start - 1.0) * SAMPLE_RATE)
    fade_end = int((outro_start + 1.0) * SAMPLE_RATE)
    fade_len = fade_end - fade_start
    if fade_start > 0 and fade_end <= len(music):
        music[fade_start:fade_end] *= np.linspace(1, 0, fade_len)
        music[fade_end:] = 0
    sfx_events.append((0.0, music))

    # Outro jingle during CRT scene
    outro = generate_outro(crt_duration)
    sfx_events.append((outro_start + 0.5, outro))

    # Mix everything
    mixed = mix_timeline(sfx_events, total_duration)

    # Save
    audio_path = os.path.join(output_dir, "audio.wav")
    save_wav(audio_path, mixed)
    return audio_path


def render_version(renderer, output_dir, short=True, preview=False):
    """Render one version of the video."""
    label = "intro" if short else "channel"
    output_path = os.path.join(output_dir, f"{label}.mp4")
    print(f"Rendering {label} version...")

    durations = get_durations(short=short)
    total_duration = sum(durations)
    print(f"  Duration: {total_duration}s ({int(total_duration * FPS)} frames)")

    # Generate audio (needs scenes for sound events)
    cursor = Cursor()
    character = Character()
    ui = ScummUI()
    temp_scenes = build_scenes(cursor, character, ui, short=short)
    audio_path = generate_audio(temp_scenes, durations, total_duration, output_dir)

    # Re-create scenes for rendering (fresh state)
    cursor = Cursor()
    character = Character()
    ui = ScummUI()
    scenes = build_scenes(cursor, character, ui, short=short)

    # Re-init first scene so shared state is correct after all constructors ran
    _reinit_scene(scenes[0], cursor, character, ui, short)

    # Render frames
    dt = 1.0 / FPS
    frame_num = 0
    scene_idx = 0
    clock = pygame.time.Clock()

    print("  Rendering frames...")
    while scene_idx < len(scenes):
        current_scene = scenes[scene_idx]

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
                _reinit_scene(scenes[scene_idx], cursor, character, ui, short)

        if frame_num % 30 == 0:
            print(f"    Frame {frame_num}/{int(total_duration * FPS)}")

    print(f"  Rendered {frame_num} frames")

    # Export video
    renderer.export_video(audio_path, output_path)

    # Cleanup
    renderer.cleanup_frames()
    os.remove(audio_path)
    print(f"  Exported: {output_path}")


def run(preview=False, versions=None):
    """Run the full sequence."""
    if versions is None:
        versions = ["intro", "channel"]

    project_root = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    renderer = Renderer(preview=preview)

    for version in versions:
        short = version == "intro"
        render_version(renderer, output_dir, short=short, preview=preview)

    renderer.quit()
    print("Done!")


if __name__ == "__main__":
    preview = "--preview" in sys.argv

    # Determine which versions to render
    if "--intro" in sys.argv:
        versions = ["intro"]
    elif "--channel" in sys.argv:
        versions = ["channel"]
    else:
        versions = ["intro", "channel"]

    run(preview=preview, versions=versions)
