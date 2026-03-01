# Maniac Stefan — Scene Script

YouTube channel intro, ~23 seconds, SCUMM adventure game style (Maniac Mansion 1987).

**Resolution:** 320x200 native, scaled 4x to 1280x800, centered on 1280x720 (16:9).

**UI:** Authentic Maniac Mansion layout — black background, 4-column green verb grid (Push/Pull/Give, Open/Close/Read, Walk to/Pick up/What is, Turn on/Turn off/Use), pink/magenta inventory items, crosshair cursor (23x23, 1px arms), white status line.

**Inventory:** Screwdriver, iPhone, Keys, Invoice, Rubber Duck

## Scene 1: Living Room (3.5s)

**Background:** `living_room.png` — Staircase left, grandfather clock with animated pendulum, green lamp, blue couch with sleeping cat (animated sprite, 10 frames), painting, door right.

| Time | Action |
|------|--------|
| 0.0s | Stefan stands left of center, crosshair cursor visible on verb bar |
| 0.2s | Cursor moves to **"Walk to"** verb |
| 0.7s | Click — verb highlights, status: "Walk to" |
| 0.7s | Cursor moves to door (far right, x=314) |
| 1.2s | Click — status: "Walk to Door" |
| 1.2s | Stefan walks right toward door |
| ~3.3s | Stefan reaches door |
| 3.5s | Scene ends |

**Animated overlays:**
- Clock pendulum: swings inside dark window (pivot y=62, length 14, 1.5s period)
- Cat: breathing animation on red towel on couch (200ms per frame)

**Sounds:** Click at 0.7s (verb), click at 1.2s (door)

---

## Scene 2: Computer Room (5.0s)

**Background:** `computer_room.png` — Filing cabinet, desk with CRT monitor, keyboard, microphone, Kubernetes/Unity poster with spider web, Half-Life lambda picture, side table with model airplane.

**Animated overlays:**
- 3D printer on left side of desk (16 frames, 130ms, sprite sheet)
- Spider descends from web on silk thread (y=25→55, 6 px/s)

| Time | Action |
|------|--------|
| 0.0s | Stefan enters bottom-left, cursor visible |
| 0.15s | Cursor moves to **"Walk to"** verb |
| 0.45s | Click — status: "Walk to" |
| 0.45s | Cursor moves to chair area |
| 0.75s | Click — status: "Walk to Chair" |
| 0.75s | Stefan walks NE to waypoint, then N to desk |
| ~1.5s | Stefan arrives at chair, sits down |
| 1.5s | Cursor moves to **"Use"** verb |
| 1.8s | Click — status: "Use" |
| 1.8s | Cursor moves to microphone on desk |
| 2.1s | Click — status: "Use Microphone" |
| 2.1s | Cursor moves to **"Turn on"** verb |
| 2.4s | Click — status: "Turn on" |
| 2.4s | Cursor moves to computer monitor |
| 2.7s | Click — status: "Turn on Computer" |
| 5.0s | Scene ends |

**Sounds:** Clicks at 0.45s, 0.75s, 1.4s, 1.7s, 2.0s, 2.25s

---

## Scene 3: Switch Close-Up (1.5s)

**Background:** Procedural — Close-up of computer power toggle switch.

| Time | Action |
|------|--------|
| 0.0s | Close-up of switch, cursor visible |
| 0.1s | Cursor moves to **"Turn on"** verb |
| 0.35s | Click — status: "Turn on" |
| 0.35s | Cursor moves to switch |
| 0.6s | Click — status: "Turn on Computer" |
| 0.6s | Switch flips to ON, green LED lights up |
| 1.5s | Scene ends |

**Sounds:** Click at 0.35s, click at 0.75s, boot beep at 0.8s

---

## Scene 4: DOS Boot (2.0s)

**Background:** Procedural DOS screen (black with white/green text).

| Time | Action |
|------|--------|
| 0.0s | Black screen, cursor hidden |
| 0.0s | Boot beep sound |
| 0.2s | C64 1541 floppy drive sound starts |
| 0.3s | "MS-DOS" appears |
| 0.6s | "(C)Copyright Microsoft Corp" |
| 0.9s | "1981-1990 ver 5.00A" |
| 1.2s | "C:\> _" with blinking cursor |
| 2.0s | Scene ends |

**Sounds:** Boot beep at 0.0s, C64 1541 floppy drive sound at 0.2s

---

## Scene 5: Flight Simulator (2.0s)

**Background:** DOS screen → procedural flight sim (top-down, blue ocean, green islands, plane).

| Time | Action |
|------|--------|
| 0.0s | DOS boot text visible, typing starts after "C:\> " |
| 0.0-0.54s | "FLIGHT.EXE" types out char by char (0.06s per char) |
| 0.8s | Game starts — top-down flight sim |
| 0.8s | Engine hum sound starts |
| 0.8-2.0s | Auto-scrolling forward (islands scroll down, plane centered) |
| 2.0s | Scene ends |

**Sounds:** Keypress per character, flight engine hum (1.2s)

---

## Scene 6: ESC → Desktop → YouTube Studio (4.0s)

**Background:** ESC key → Windows-style desktop with YouTube Studio window → REC screen.

| Time | Action |
|------|--------|
| 0.0s | Cursor hidden |
| 0.1s | ESC key shown (3D button graphic on black) |
| 0.5s | Desktop appears (teal, YouTube Studio window, taskbar) |
| 0.8s | Cursor visible, moves to **"Use"** verb |
| 1.3s | Click — status: "Use" |
| 1.6s | Cursor moves to YouTube Studio window title |
| 2.1s | Click — status: "Use YouTube Studio" |
| 2.5s | Cursor moves to RECORD button |
| 2.9s | Click — status: "Use Record Button" |
| 2.9s | REC screen with blinking red dot and VU meters |
| 4.0s | Scene ends |

**Desktop details:** My Computer icon, Recycle Bin, YouTube Studio window (red bar, "Stefan's Channel", Views: 1,337, Subs: 42, red RECORD button), Windows taskbar with Start button.

**Sounds:** ESC keypress at 0.1s, clicks at 1.3s, 2.1s, 2.9s

---

## Scene 7: CRT Inside View (5.0s)

**Background:** `crt_inside.png` — Stefan seen through CRT monitor from inside, circuit board edges visible.

| Time | Action |
|------|--------|
| 0.0s | Zoom-out from center (2x → 1x over 0.8s) |
| 0.0s | Cursor hidden |
| 0.0-5.0s | Stefan visible through CRT screen |
| 0.0-5.0s | White recording circle blinks at top-right of screen (1Hz) |
| 5.0s | Scene ends |

**Sounds:** Music continues

---

## Technical Details

**Pipeline:** Pygame-ce renders 320x200 frames → PNG sequence → ffmpeg → MP4 (libx264, yuv420p, 30fps)

**Audio:** numpy waveform synthesis — SID-style 3-channel chiptune (C minor), click SFX, keypress sounds, C64 floppy drive, flight engine hum. Mixed to single WAV track.

**Total Duration:** 3.5 + 5.0 + 1.5 + 2.0 + 2.0 + 4.0 + 5.0 = **23.0s**
