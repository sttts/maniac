# Maniac Stefan — Scene Script

YouTube channel intro, SCUMM adventure game style (Maniac Mansion 1987).

Two versions: **intro** (~15s, short) and **channel** (~25s, full).

**Resolution:** 320x200 native, scaled 4x to 1280x800, centered on 1280x720 (16:9).

**UI:** Authentic Maniac Mansion layout — black background, 4-column green verb grid (Push/Pull/Give, Open/Close/Read, Walk to/Pick up/What is, Turn on/Turn off/Use), pink/magenta inventory items, crosshair cursor (23x23, 1px arms), white status line.

**Inventory:** Screwdriver, iPhone, Keys, Invoice, Rubber Duck

## Scene 1: Living Room (channel 3.5s / intro 2.5s)

**Background:** `living_room.png` — Staircase left, grandfather clock with animated pendulum, green lamp, blue couch with sleeping cat (animated sprite, 10 frames), painting, door right.

**Channel version:**

| Time | Action |
|------|--------|
| 0.0s | Stefan stands left of center, crosshair cursor visible on verb bar |
| 0.2s | Cursor moves to **"Walk to"** verb (0.8s) |
| 0.7s | Click — verb highlights, status: "Walk to" |
| 0.7s | Cursor moves to door (far right, x=314) (0.8s) |
| 1.2s | Click — status: "Walk to Door" |
| 1.2s | Stefan walks right toward door |
| ~3.3s | Stefan reaches door |
| 3.5s | Scene ends |

**Intro version:** faster cursor (0.5s moves), less initial delay (0.1s), scene ends before character reaches door.

**Animated overlays:**
- Clock pendulum: swings inside dark window (pivot y=62, length 14, 1.5s period)
- Cat: breathing animation on red towel on couch (200ms per frame)

---

## Scene 2: Computer Room (channel 5.0s / intro 3.5s)

**Background:** `computer_room.png` — Filing cabinet, desk with CRT monitor, keyboard, microphone, Kubernetes/Unity poster with spider web, Half-Life lambda picture, side table with model airplane.

**Animated overlays:**
- 3D printer on left side of desk (16 frames, 130ms, sprite sheet)
- Spider descends from web on silk thread (y=30→60, 6 px/s)

**Channel version:**

| Time | Action |
|------|--------|
| 0.0s | Stefan enters bottom-left, cursor visible |
| 0.15s | Cursor moves to **"Walk to"** verb (0.6s) |
| 0.45s | Click — status: "Walk to" |
| 0.45s | Cursor moves to chair area (0.6s) |
| 0.75s | Click — status: "Walk to Chair" |
| 0.75s | Stefan walks NE to waypoint, then N to desk |
| ~1.5s | Stefan arrives at chair, sits down |
| 1.5s | Cursor moves to **"Use"** verb (0.6s) |
| 1.8s | Click — status: "Use" |
| 1.8s | Cursor moves to microphone on desk (0.6s) |
| 2.1s | Click — status: "Use Microphone" |
| 2.1s | Cursor moves to **"Turn on"** verb (0.6s) |
| 2.4s | Click — status: "Turn on" |
| 2.4s | Cursor moves to computer monitor (0.6s) |
| 2.7s | Click — status: "Turn on Computer" |
| 5.0s | Scene ends |

**Intro version:** faster cursor (0.45s moves), skips Use Microphone interaction — goes directly from sitting to "Turn on" verb.

---

## Scene 3: Switch Close-Up (1.5s)

**Background:** Procedural — Close-up of computer power toggle switch. Same in both versions.

| Time | Action |
|------|--------|
| 0.0s | Close-up of switch, cursor visible |
| 0.1s | Cursor moves to **"Turn on"** verb |
| 0.35s | Click — status: "Turn on" |
| 0.35s | Cursor moves to switch |
| 0.6s | Click — status: "Turn on Computer" |
| 0.6s | Switch flips to ON, green LED lights up |
| 1.5s | Scene ends |

---

## Scene 4: DOS Boot (channel 2.0s / intro 1.5s)

**Background:** Procedural DOS screen (black with white/green text).

| Time | Action |
|------|--------|
| 0.0s | Black screen, cursor hidden |
| 0.2s | C64 1541 floppy drive sound starts |
| 0.3s | "MS-DOS" appears |
| 0.6s | "(C)Copyright Microsoft Corp" |
| 0.9s | "1981-1990 ver 5.00A" |
| 1.2s | "C:\> _" with blinking cursor |

---

## Scene 5: Flight Simulator (2.0s) — channel only

**Background:** DOS screen → procedural flight sim (top-down, blue ocean, green islands, plane).

| Time | Action |
|------|--------|
| 0.0s | DOS boot text visible, typing starts after "C:\> " |
| 0.0-0.54s | "FLIGHT.EXE" types out char by char (0.06s per char) |
| 0.8s | Game starts — top-down flight sim |
| 0.8-2.0s | Auto-scrolling forward (islands scroll down, plane centered) |
| 2.0s | Scene ends |

---

## Scene 6: YouTube Studio (channel 5.0s / intro 2.5s)

**Background:** ESC key → DOS prompt → Windows-style desktop with YouTube Studio window → REC screen.

**Channel version:**

| Time | Action |
|------|--------|
| 0.0s | Cursor hidden |
| 0.1s | ESC key shown (3D button graphic on black) |
| 0.5s | DOS prompt, types "win" |
| 1.3s | Desktop appears (teal, YouTube Studio window, taskbar) |
| 1.6s | Cursor visible, moves to **"Use"** verb |
| 2.1s | Click — status: "Use" |
| 2.1s | Cursor moves to YouTube Studio window title |
| 2.5s | Click — status: "Use YouTube Studio" |
| 2.9s | Cursor moves to RECORD button |
| 3.3s | Click — status: "Use Record Button" |
| 3.3s | REC screen with blinking red dot and VU meters |
| 5.0s | Scene ends |

**Intro version:** no ESC key, starts at DOS prompt typing "win", cursor goes directly to Record button (skips Use verb and YouTube Studio click), no recording screen.

**Desktop details:** My Computer icon, Recycle Bin, YouTube Studio window (red bar, "Stefan's Channel", Views: 1,337, Subs: 42, red RECORD button), Windows taskbar with Start button.

---

## Scene 7: CRT Inside View (channel 6.0s / intro 3.5s)

**Background:** `crt_inside.png` — Stefan seen through CRT monitor from inside, circuit board edges visible.

| Time | Action |
|------|--------|
| 0.0s | Zoom-out from center (2x → 1x over 0.8s) |
| 0.0s | Cursor hidden |
| ~1.2-1.8s | Anamorphic lens flare sparkle on right glasses corner |
| ongoing | White recording circle blinks at top-right (1Hz) |
| ongoing | Mirrored recording timer at bottom-right |

**Sparkle timing:** channel starts at 1.8s (0.9s duration), intro starts at 1.2s (0.7s duration).

---

## Technical Details

**Pipeline:** Pygame-ce renders 320x200 frames → PNG sequence → ffmpeg → MP4 (libx264, yuv420p, 30fps)

**Audio:** numpy waveform synthesis — SID-style 3-channel chiptune (C minor), click SFX, keypress sounds, C64 floppy drive, flight engine hum. Mixed to single WAV track.

**Total Duration:** channel 3.5 + 5.0 + 1.5 + 2.0 + 2.0 + 5.0 + 6.0 = **25.0s** / intro 2.5 + 3.5 + 1.5 + 1.5 + 2.5 + 3.5 = **15.0s**
