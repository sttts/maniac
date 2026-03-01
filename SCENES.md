# Maniac Stefan — Scene Script

YouTube channel intro, ~18.5 seconds, SCUMM adventure game style (Maniac Mansion 1987).

**UI:** Authentic Maniac Mansion layout — black background, 4-column green verb grid, pink/magenta inventory items, white arrow cursor, white status line.

**Inventory:** Screwdriver, iPhone, Keys, Invoice, Rubber Duck

## Scene 1: Living Room (3.0s)

**Background:** `living_room.png` — Staircase left, grandfather clock, green lamp, blue couch with cat, door right.

| Time | Action |
|------|--------|
| 0.0s | Stefan stands left of center, arrow cursor visible mid-screen |
| 0.2s | Cursor moves to **"Walk to"** verb |
| 0.7s | Click — verb highlights, status: "Walk to" |
| 0.7s | Cursor moves to door (right side) |
| 1.2s | Click — status: "Walk to Door" |
| 1.2s | Stefan walks right toward door |
| ~2.8s | Stefan reaches door |
| 3.0s | Scene ends |

**Sounds:** Click at 0.7s (verb), click at 1.2s (door)

---

## Scene 2: Computer Room (4.0s)

**Background:** `computer_room.png` — Desk with CRT, keyboard, 3D printer, Kubernetes poster, lambda picture, model airplane, spider web.

| Time | Action |
|------|--------|
| 0.0s | Stefan enters bottom-left, cursor visible |
| 0.15s | Cursor moves to **"Walk to"** verb |
| 0.45s | Click — status: "Walk to" |
| 0.45s | Cursor moves to chair area |
| 0.75s | Click — status: "Walk to Chair" |
| 0.75s | Stefan walks NE diagonally to waypoint, then N to desk |
| ~1.5s | Stefan arrives at chair, sits down |
| 1.5s | Cursor moves to **"Use"** verb |
| 1.8s | Click — status: "Use" |
| 1.8s | Cursor moves to microphone on desk |
| 2.1s | Click — status: "Use Microphone" |
| 2.1s | Cursor moves to **"Turn on"** verb |
| 2.4s | Click — status: "Turn on" |
| 2.4s | Cursor moves to computer monitor |
| 2.7s | Click — status: "Turn on Computer" |
| 4.0s | Scene ends |

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
| 0.2s | C64 1541 floppy drive sound starts (loud mechanical grinding) |
| 0.3s | "MS-DOS" appears |
| 0.6s | "(C)Copyright Microsoft Corp" |
| 0.9s | "1981-1990 ver 5.00A" |
| 1.2s | "C:\>_" with blinking cursor |
| 2.0s | Scene ends |

**Sounds:** Boot beep at 0.0s, C64 1541 floppy drive sound at 0.2s

---

## Scene 5: Flight Simulator (2.0s)

**Background:** DOS screen → procedural flight sim (top-down, blue ocean, green islands, plane).

| Time | Action |
|------|--------|
| 0.0s | DOS prompt, cursor hidden, typing starts |
| 0.0-0.54s | "FLIGHT.EXE" types out char by char (0.06s per char, keypress sounds) |
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

## Scene 7: CRT Inside View (2.0s)

**Background:** Procedural — Circuit boards on sides, CRT opening, Stefan waving.

| Time | Action |
|------|--------|
| 0.0s | Zoom-out from center (2x → 1x over 0.8s) |
| 0.0s | Cursor hidden |
| 0.0-2.0s | Stefan waving at camera, YouTube overlay "0:00/30:03" |
| 2.0s | Scene ends |

**Sounds:** Music continues

---

## Status

### Implemented
- [x] SCUMM UI matching original Maniac Mansion (4-col verbs, arrow cursor, black bg)
- [x] C64 1541 floppy drive sound (loud mechanical stepper motor grinding)
- [x] SID-style chiptune music (3-channel, C minor)
- [x] Desktop/YouTube Studio scene with SCUMM interactions
- [x] Character-by-character terminal typing with keypress sounds
- [x] Two-phase character walk (NE diagonal, then N) in computer room

### Missing Backgrounds (currently procedural)
- [ ] `switch_closeup.png`
- [ ] `crt_inside.png`

### Total Duration
3.0 + 4.0 + 1.5 + 2.0 + 2.0 + 4.0 + 2.0 = **18.5s**
