# Maniac Stefan

A ~24 second YouTube channel intro styled after **Maniac Mansion** (1987) — the classic LucasArts SCUMM point-and-click adventure game.

[![Watch the intro](https://github.com/sttts/maniac/releases/download/latest/screenshot.png)](https://sttts.github.io/maniac/)

## What it does

The video shows what looks like someone playing a retro adventure game: a visible mouse cursor clicks on verbs, a character walks between rooms, sits at a computer, boots DOS, plays a flight sim, opens YouTube Studio, and hits Record — all rendered at authentic 320x200 SCUMM resolution with pixel-perfect scaling.

### Scenes

| # | Scene | Duration | Highlights |
|---|-------|----------|------------|
| 1 | Living room | 3.5s | Animated sleeping cat, swinging clock pendulum, walk to door |
| 2 | Computer room | 5.0s | 3D printer animation, spider descending from web, sit at desk |
| 3 | Switch close-up | 1.5s | Flip power switch, green LED |
| 4 | DOS boot | 2.0s | MS-DOS text boot, C64 floppy drive sound |
| 5 | Flight simulator | 2.0s | Type FLIGHT.EXE, top-down retro flight game |
| 6 | YouTube Studio | 5.0s | ESC key, DOS `C:\> win`, Windows desktop, click Record |
| 7 | CRT inside view | 5.0s | Zoom-out, recording indicator blink |

## Tech stack

- **Pygame-ce** — renders each frame at 320x200 native resolution
- **numpy/scipy** — generates all audio (SID-style chiptune music, SFX) via waveform synthesis
- **ffmpeg** — combines PNG frame sequence + WAV audio into MP4

No external assets required for audio — everything is synthesized. Background art is pixel art at native SCUMM resolution.

## Build

```bash
python -m venv .venv && source .venv/bin/activate
make install
make render    # outputs output/intro.mp4
```

Requires Python 3.10+ and ffmpeg installed (`brew install ffmpeg` on macOS).

## Preview

```bash
make preview   # opens a live Pygame window while rendering
```

## Project structure

```
src/
  main.py              # entry point — scene sequencer, frame capture, ffmpeg export
  renderer.py          # Pygame init, 4x scaling, frame capture
  pixel_art.py         # procedural pixel art + background loading
  scumm_ui.py          # SCUMM verb bar + inventory
  cursor.py            # 23x23 crosshair cursor with movement interpolation
  character.py         # Stefan sprite — walk cycle, sit animation
  sounds.py            # waveform synthesis (SID music, SFX)
  font.py              # bitmap font rendering
  scenes/              # one module per scene (living_room, computer_room, ...)
assets/
  backgrounds/         # pixel art background PNGs
  sprites/             # animated sprite frames (cat, 3D printer)
```

## License

MIT
