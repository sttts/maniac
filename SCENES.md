# Maniac Stefan — Scene Script

YouTube channel intro, ~15 seconds, SCUMM adventure game style.

## Scene 1: Living Room (2.5s)

**Background:** `living_room.png` — Staircase left, grandfather clock, green lamp, blue couch with cat, door right.

| Time | Action |
|------|--------|
| 0.0s | Stefan stands left of center, cursor visible mid-screen |
| 0.2s | Cursor moves to **"Walk to"** verb |
| 0.7s | Click — verb highlights, status: "Walk to" |
| 0.7s | Cursor moves to door (right side) |
| 1.2s | Click — status: "Walk to Door" |
| 1.2s | Stefan walks right toward door |
| 2.5s | Scene ends |

**Sounds:** Click at 0.7s (verb), click at 1.2s (door)

---

## Scene 2: Computer Room (3.5s)

**Background:** `computer_room.png` — Desk with CRT, keyboard, 3D printer, Kubernetes poster, lambda picture, model airplane, spider web.

| Time | Action |
|------|--------|
| 0.0s | Stefan enters bottom-left, cursor visible |
| 0.15s | Cursor moves to **"Walk to"** verb |
| 0.45s | Click — status: "Walk to" |
| 0.45s | Cursor moves to chair area |
| 0.75s | Click — status: "Walk to Chair", Stefan walks north-east to desk |
| ~1.3s | Stefan arrives, sits down |
| 1.3s | Cursor moves to **"Use"** verb |
| 1.6s | Click — status: "Use" |
| 1.6s | Cursor moves to microphone on desk |
| 1.9s | Click — status: "Use Microphone" |
| 1.9s | Cursor moves to **"Turn on"** verb |
| 2.15s | Click — status: "Turn on" |
| 2.15s | Cursor moves to computer monitor |
| 2.4s | Click — status: "Turn on Computer" |
| 3.5s | Scene ends |

**Sounds:** Clicks at 0.45s, 0.75s, 1.4s, 1.7s, 2.0s, 2.25s

---

## Scene 3: Switch Close-Up (1.5s)

**Background:** `switch_closeup.png` (procedural) — Close-up of computer power toggle switch.

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
**Status:** Needs PixelLab background

---

## Scene 4: DOS Boot (2.0s)

**Background:** Procedural DOS screen (black with white/green text).

| Time | Action |
|------|--------|
| 0.0s | Black screen, cursor hidden |
| 0.0s | Boot beep sound |
| 0.2s | Floppy drive sound starts |
| 0.3s | "MS-DOS" appears |
| 0.6s | "(C)Copyright Microsoft Corp" |
| 0.9s | "1981-1990 ver 5.00A" |
| 1.2s | "C:\>_" with blinking cursor |
| 2.0s | Scene ends, cursor shown |

**Sounds:** Boot beep at 0.0s, C64 floppy drive sound at 0.2s (LOUD)
**TODO:** Make floppy drive sound louder and more C64/1541-like

---

## Scene 5: Flight Simulator (2.0s)

**Background:** DOS screen → procedural flight sim (top-down, blue ocean, green islands, plane).

| Time | Action |
|------|--------|
| 0.0s | DOS prompt, cursor hidden, typing starts |
| 0.0-0.54s | "FLIGHT.EXE" types out (0.06s per char) |
| 0.8s | Game starts — top-down flight sim |
| 0.8s | Engine hum sound starts |
| 0.8-2.0s | Auto-scrolling forward (islands move down, plane centered) |
| 2.0s | Scene ends |

**Sounds:** Keypress per character, flight engine hum (1.2s)

---

## Scene 6: ESC → RECORD.EXE (2.0s)

**Background:** Black → DOS screen → REC screen (procedural).

| Time | Action |
|------|--------|
| 0.0s | Cursor hidden |
| 0.1s | ESC key shown (3D button graphic) |
| 0.3s | DOS prompt appears |
| 0.3-0.9s | "RECORD.EXE" types out |
| 1.15s | Enter key sound |
| 1.2s | REC screen with blinking red dot and VU meters |
| 2.0s | Scene ends, cursor shown |

**Sounds:** ESC keypress at 0.1s, typing keypresses, enter sound at 1.15s
**TODO:** Replace with Desktop/YouTube Studio scene?

---

## Scene 7: CRT Inside View (2.0s)

**Background:** `crt_inside.png` (procedural) — Circuit boards on sides, CRT opening, Stefan waving.

| Time | Action |
|------|--------|
| 0.0s | Zoom-out from center (2x → 1x over 0.8s) |
| 0.0s | Cursor hidden |
| 0.0-2.0s | Stefan waving at camera, YouTube overlay "0:00/30:03" |
| 2.0s | Scene ends |

**Sounds:** Music continues
**Status:** Needs PixelLab background

---

## Planned Changes

### New: Desktop/YouTube Studio Scene (after ESC, before or replacing RECORD.EXE)
- Desktop background with YouTube Studio open
- Cursor clicks **"Use"** → **"YouTube Studio"**
- Record button appears, cursor clicks it
- Transition to REC/recording state
- Needs background asset

### Audio Improvements
- [ ] C64 floppy drive sound (1541-style) — loud, mechanical grinding during DOS boot
- [ ] Current SID music continues throughout

### Missing Backgrounds (need PixelLab or manual creation)
- [ ] `switch_closeup.png` — currently procedural
- [ ] `crt_inside.png` — currently procedural
- [ ] Desktop/YouTube Studio background — new scene

### Total Duration
Current: 2.5 + 3.5 + 1.5 + 2.0 + 2.0 + 2.0 + 2.0 = **15.5s**
With YouTube Studio scene: ~17-18s
