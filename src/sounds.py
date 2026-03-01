"""Sound generation using numpy waveform synthesis — C64 SID style."""
import os
import struct
import numpy as np

SAMPLE_RATE = 44100


def _square_wave(freq, duration, duty=0.5, volume=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = np.where((t * freq) % 1.0 < duty, volume, -volume)
    return wave


def _sawtooth_wave(freq, duration, volume=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = 2.0 * ((t * freq) % 1.0) - 1.0
    return (wave * volume).astype(np.float64)


def _noise(duration, volume=0.3):
    n = int(SAMPLE_RATE * duration)
    return np.random.uniform(-volume, volume, n)


def _sine_wave(freq, duration, volume=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t) * volume


def _envelope(wave, attack=0.01, decay=0.05, sustain_level=0.7, release=0.05):
    """Apply ADSR envelope."""
    n = len(wave)
    env = np.ones(n)
    a_samples = int(attack * SAMPLE_RATE)
    d_samples = int(decay * SAMPLE_RATE)
    r_samples = int(release * SAMPLE_RATE)

    # Attack
    if a_samples > 0:
        env[:a_samples] = np.linspace(0, 1, a_samples)
    # Decay
    d_end = a_samples + d_samples
    if d_samples > 0 and d_end <= n:
        env[a_samples:d_end] = np.linspace(1, sustain_level, d_samples)
    # Sustain
    if d_end < n - r_samples:
        env[d_end:n - r_samples] = sustain_level
    # Release
    if r_samples > 0:
        env[-r_samples:] = np.linspace(sustain_level, 0, r_samples)
    return wave * env


def _arpeggio_note(base_freq, semitones, duration, duty=0.5, volume=0.25):
    """Play an arpeggiated note (fast switching between intervals)."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = np.zeros_like(t)

    # Fast arpeggio: cycle through base and semitone offsets every ~50ms
    cycle_samples = int(0.05 * SAMPLE_RATE)
    for i, st in enumerate(semitones):
        freq = base_freq * (2 ** (st / 12.0))
        start = (i * cycle_samples) % len(t)
        end = start + cycle_samples
        if end > len(t):
            end = len(t)
        seg_t = np.linspace(0, (end - start) / SAMPLE_RATE, end - start, endpoint=False)
        wave[start:end] += np.where((seg_t * freq) % 1.0 < duty, volume, -volume)
    return wave


def generate_sid_music(duration=14.0):
    """Generate C64 SID-style 3-channel chiptune in C minor."""
    n = int(SAMPLE_RATE * duration)
    mix = np.zeros(n)

    # C minor scale frequencies
    # C3=130.81, Eb3=155.56, G3=196.00, C4=261.63
    bass_notes = [
        (130.81, 0.4), (130.81, 0.4), (155.56, 0.4), (196.00, 0.4),
        (130.81, 0.4), (174.61, 0.4), (155.56, 0.4), (116.54, 0.4),
        (130.81, 0.4), (130.81, 0.4), (155.56, 0.4), (196.00, 0.4),
        (174.61, 0.4), (155.56, 0.4), (130.81, 0.4), (130.81, 0.4),
    ]

    lead_notes = [
        (523.25, 0.2), (622.25, 0.2), (523.25, 0.2), (392.00, 0.2),
        (523.25, 0.2), (622.25, 0.2), (698.46, 0.2), (622.25, 0.2),
        (523.25, 0.2), (392.00, 0.2), (349.23, 0.2), (392.00, 0.2),
        (523.25, 0.3), (466.16, 0.2), (392.00, 0.3),
        (523.25, 0.2), (622.25, 0.2), (523.25, 0.2), (392.00, 0.2),
        (349.23, 0.2), (311.13, 0.2), (349.23, 0.2), (392.00, 0.2),
        (523.25, 0.3), (466.16, 0.3), (392.00, 0.4),
    ]

    # Bass channel (sawtooth)
    pos = 0
    while pos < n:
        for freq, dur in bass_notes:
            samples = int(dur * SAMPLE_RATE)
            if pos + samples > n:
                samples = n - pos
            if samples <= 0:
                break
            note = _sawtooth_wave(freq, dur, volume=0.15)[:samples]
            note = _envelope(note, attack=0.01, decay=0.1, sustain_level=0.6, release=0.02)
            mix[pos:pos + len(note)] += note
            pos += samples

    # Lead channel (pulse wave with arpeggio feel)
    pos = 0
    while pos < n:
        for freq, dur in lead_notes:
            samples = int(dur * SAMPLE_RATE)
            if pos + samples > n:
                samples = n - pos
            if samples <= 0:
                break
            # Pulse width modulation
            pwm_duty = 0.3 + 0.2 * np.sin(2 * np.pi * 3 * np.linspace(0, dur, samples))
            t = np.linspace(0, dur, samples, endpoint=False)
            note = np.where((t * freq) % 1.0 < pwm_duty, 0.12, -0.12)
            note = _envelope(note, attack=0.005, decay=0.05, sustain_level=0.8, release=0.02)
            mix[pos:pos + len(note)] += note
            pos += samples

    # Percussion channel (noise hits on beat)
    beat_interval = int(0.4 * SAMPLE_RATE)
    for beat_start in range(0, n, beat_interval):
        hit_len = min(int(0.05 * SAMPLE_RATE), n - beat_start)
        hit = _noise(0.05, volume=0.1)[:hit_len]
        hit = _envelope(hit, attack=0.001, decay=0.03, sustain_level=0.1, release=0.01)
        mix[beat_start:beat_start + len(hit)] += hit
        # Offbeat hi-hat
        offbeat = beat_start + beat_interval // 2
        if offbeat + hit_len <= n:
            hh = _noise(0.02, volume=0.05)[:min(int(0.02 * SAMPLE_RATE), hit_len)]
            hh = _envelope(hh, attack=0.001, decay=0.01, sustain_level=0.05, release=0.005)
            mix[offbeat:offbeat + len(hh)] += hh

    return mix


def generate_outro(duration=4.0):
    """Outro jingle — fast C64 chiptune fanfare, like a game level complete."""
    n = int(SAMPLE_RATE * duration)
    mix = np.zeros(n)

    def _add(wave, t0):
        start = int(t0 * SAMPLE_RATE)
        end = min(start + len(wave), n)
        mix[start:end] += wave[:end - start]

    # Fast ascending arpeggio run: C-Eb-G-C-Eb-G-C (staccato, 0.08s each)
    arp_freqs = [261.63, 311.13, 392.00, 523.25, 622.25, 783.99, 1046.50]
    for i, freq in enumerate(arp_freqs):
        note = _square_wave(freq, 0.08, duty=0.25, volume=0.15)
        note = _envelope(note, attack=0.003, decay=0.04, sustain_level=0.3, release=0.02)
        _add(note, i * 0.08)

    # Punchy bass hits under the arpeggio
    for t in [0.0, 0.24, 0.48]:
        bass = _sawtooth_wave(130.81, 0.12, volume=0.18)
        bass = _envelope(bass, attack=0.005, decay=0.06, sustain_level=0.3, release=0.02)
        _add(bass, t)

    # Victory phrase: short melody (da-da-da-DAAAA)
    melody = [
        (523.25, 0.12),  # C5
        (622.25, 0.12),  # Eb5
        (783.99, 0.12),  # G5
        (1046.50, 0.5),  # C6 held
    ]
    t = 0.6
    for freq, dur in melody:
        note = _square_wave(freq, dur, duty=0.3, volume=0.14)
        note = _envelope(note, attack=0.005, decay=0.05, sustain_level=0.7, release=0.05)
        _add(note, t)
        t += dur

    # Bass under the victory phrase
    bass = _sawtooth_wave(130.81, 0.8, volume=0.15)
    bass = _envelope(bass, attack=0.01, decay=0.2, sustain_level=0.4, release=0.1)
    _add(bass, 0.6)

    # Noise hit on the final note for impact
    hit = _noise(0.08, volume=0.15)
    hit = _envelope(hit, attack=0.001, decay=0.04, sustain_level=0.0, release=0.02)
    _add(hit, 0.96)

    # Quick echo of final note (quieter, delayed)
    echo = _square_wave(1046.50, 0.3, duty=0.25, volume=0.06)
    echo = _envelope(echo, attack=0.005, decay=0.1, sustain_level=0.3, release=0.1)
    _add(echo, 1.6)

    # Silence after ~2s
    return mix


def generate_mac_bong():
    """Load Macintosh Quadra startup chime from WAV file."""
    import wave
    wav_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds", "mac_startup.wav")
    w = wave.open(wav_path, "r")
    raw = w.readframes(w.getnframes())
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32767.0

    # Resample from 22254 Hz to 44100 Hz
    src_rate = w.getframerate()
    w.close()
    if src_rate != SAMPLE_RATE:
        ratio = SAMPLE_RATE / src_rate
        new_len = int(len(samples) * ratio)
        x_old = np.linspace(0, 1, len(samples))
        x_new = np.linspace(0, 1, new_len)
        samples = np.interp(x_new, x_old, samples)

    return samples * 1.0


def generate_apple2_beep():
    """Load Apple II startup beep from WAV file."""
    import wave
    wav_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds", "apple2_startup.wav")
    w = wave.open(wav_path, "r")
    raw = w.readframes(w.getnframes())
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32767.0

    # Resample if needed
    src_rate = w.getframerate()
    w.close()
    if src_rate != SAMPLE_RATE:
        ratio = SAMPLE_RATE / src_rate
        new_len = int(len(samples) * ratio)
        x_old = np.linspace(0, 1, len(samples))
        x_new = np.linspace(0, 1, new_len)
        samples = np.interp(x_new, x_old, samples)

    return samples * 0.6


def generate_click_sound():
    """Short click for mouse cursor actions."""
    return _envelope(_noise(0.03, volume=0.3), attack=0.001, decay=0.02, sustain_level=0.0, release=0.005)


def generate_boot_beep():
    """PC speaker beep on boot."""
    return _envelope(_square_wave(1000, 0.15, volume=0.25), attack=0.005, decay=0.05, sustain_level=0.2, release=0.02)


def generate_disk_drive(duration=1.5):
    """C64 1541 floppy drive sound — loud mechanical stepper motor grinding."""
    n = int(SAMPLE_RATE * duration)
    mix = np.zeros(n)

    # Motor spin — low rumble
    mix += _sine_wave(95, duration, volume=0.15)[:n]
    mix += _sine_wave(190, duration, volume=0.08)[:n]
    # Motor wobble
    t = np.linspace(0, duration, n, endpoint=False)
    mix += np.sin(2 * np.pi * 300 * t + 3 * np.sin(2 * np.pi * 6 * t)) * 0.06

    # Stepper motor head seeks — the iconic grinding bursts
    # Pattern: groups of rapid steps with pauses (like the 1541 seeking tracks)
    step_times = []
    pos = 0.05
    while pos < duration - 0.1:
        # Burst of 4-8 rapid steps
        burst_len = np.random.randint(4, 9)
        for j in range(burst_len):
            step_times.append(pos)
            pos += 0.018 + np.random.uniform(0, 0.008)
        # Pause between bursts
        pos += 0.08 + np.random.uniform(0, 0.06)

    for st in step_times:
        idx = int(st * SAMPLE_RATE)
        # Each step is a sharp mechanical click/thunk
        step_dur = 0.012
        step_n = int(step_dur * SAMPLE_RATE)
        if idx + step_n > n:
            break
        # Noise burst with resonant frequency (stepper motor)
        step = _noise(step_dur, volume=0.5)
        # Add metallic ring at ~800Hz
        step += _square_wave(800, step_dur, duty=0.3, volume=0.25)[:len(step)]
        step = _envelope(step, attack=0.0005, decay=0.005, sustain_level=0.1, release=0.003)
        mix[idx:idx + len(step)] += step

    # Overall envelope — fade in motor, fade out at end
    env = np.ones(n)
    fade_in = min(int(0.05 * SAMPLE_RATE), n)
    env[:fade_in] = np.linspace(0, 1, fade_in)
    fade_out = min(int(0.1 * SAMPLE_RATE), n)
    env[-fade_out:] = np.linspace(1, 0, fade_out)
    mix *= env

    return mix


def generate_flight_hum(duration=2.0):
    """Low filtered engine noise for flight sim."""
    raw = _noise(duration, volume=0.08)
    # Simple low-pass: moving average
    kernel_size = 20
    kernel = np.ones(kernel_size) / kernel_size
    filtered = np.convolve(raw, kernel, mode='same')
    # Add engine tone
    filtered += _sine_wave(80, duration, volume=0.04)[:len(filtered)]
    return filtered


def generate_keypress():
    """Mechanical keyboard keypress sound."""
    return _envelope(_noise(0.04, volume=0.2), attack=0.001, decay=0.02, sustain_level=0.0, release=0.01)


def mix_timeline(events, total_duration):
    """Mix sound events into a single audio track.

    events: list of (time_seconds, numpy_array) tuples
    """
    n = int(SAMPLE_RATE * total_duration)
    mix = np.zeros(n)
    for t, wave in events:
        start = int(t * SAMPLE_RATE)
        end = start + len(wave)
        if end > n:
            wave = wave[:n - start]
            end = n
        if start < n:
            mix[start:start + len(wave)] += wave
    return mix


def save_wav(filename, data):
    """Save numpy float array as 16-bit WAV."""
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    # Normalize to prevent clipping
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data / peak * 0.85

    # Convert to 16-bit PCM
    pcm = (data * 32767).astype(np.int16)

    # Write WAV file
    with open(filename, "wb") as f:
        n_samples = len(pcm)
        data_size = n_samples * 2
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))           # chunk size
        f.write(struct.pack("<H", 1))            # PCM format
        f.write(struct.pack("<H", 1))            # mono
        f.write(struct.pack("<I", SAMPLE_RATE))  # sample rate
        f.write(struct.pack("<I", SAMPLE_RATE * 2))  # byte rate
        f.write(struct.pack("<H", 2))            # block align
        f.write(struct.pack("<H", 16))           # bits per sample
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(pcm.tobytes())
