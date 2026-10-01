#!/usr/bin/env python3
"""Synthesize the audio of the packs this repository was seeded with.

Every sample is computed here from sines, decaying envelopes and seeded noise; nothing is recorded or downloaded, so the output is original work dedicated to the public domain under CC0-1.0, as each pack's plugin.toml says. The tunes the melody packs play are traditional or long out of copyright. The manifests are committed beside the samples and are not written by this script.

Run it after changing a voice below, then commit the regenerated files:

    python3 scripts/generate_seed_packs.py

The output is deterministic: the same script always writes the same bytes.
"""

from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
RATE = 44_100
# Peak level of every key sample, about -3 dBFS, so the host's volume setting starts from the same loudness for each pack.
PEAK = 0.7


def silence(seconds: float, rate: int = RATE) -> list[float]:
    return [0.0] * int(seconds * rate)


def noise_burst(buffer: list[float], at: float, seed: int, decay: float, level: float, highpass: float = 0.8, lowpass: float = 1.0) -> None:
    """Seeded white noise through a one-pole high-pass (`highpass` near 1 keeps only the top) and a one-pole low-pass (`lowpass` 1 is open), under an exponential decay."""
    generator = random.Random(seed)
    start = int(at * RATE)
    end = min(len(buffer), start + int(decay * 8 * RATE))
    previous_input = previous_high = low = 0.0
    for index in range(start, end):
        t = (index - start) / RATE
        sample = generator.uniform(-1.0, 1.0)
        high = highpass * (previous_high + sample - previous_input)
        previous_input, previous_high = sample, high
        low += lowpass * (high - low)
        buffer[index] += level * low * math.exp(-t / decay)


def tone(buffer: list[float], at: float, frequency: float, partials: list[tuple[float, float, float]], attack: float = 0.002, level: float = 1.0, bend: float = 0.0, bend_time: float = 0.03) -> None:
    """A struck or plucked note: partials of (frequency ratio, amplitude, decay seconds) under a short linear attack. `bend` starts the pitch that many semitones away and glides to it over `bend_time`."""
    start = int(at * RATE)
    longest = max(decay for _, _, decay in partials)
    end = min(len(buffer), start + int(longest * 7 * RATE))
    phases = [0.0] * len(partials)
    for index in range(start, end):
        t = (index - start) / RATE
        shift = 2 ** (bend * math.exp(-t / bend_time) / 12) if bend else 1.0
        envelope = min(1.0, t / attack)
        value = 0.0
        for number, (ratio, amplitude, decay) in enumerate(partials):
            phases[number] += 2 * math.pi * frequency * ratio * shift / RATE
            value += amplitude * math.sin(phases[number]) * math.exp(-t / decay)
        buffer[index] += level * envelope * value


def finish(buffer: list[float], level: float = PEAK) -> list[int]:
    """Fade the last 8 ms to silence, normalize to `level` and quantize to 16 bits."""
    fade = int(0.008 * RATE)
    for offset in range(fade):
        buffer[len(buffer) - fade + offset] *= 1.0 - (offset + 1) / fade
    peak = max(abs(value) for value in buffer) or 1.0
    return [round(value / peak * level * 32767) for value in buffer]


def midi(note: int) -> float:
    return 440.0 * 2 ** ((note - 69) / 12)


# ---- mech-blue-switch: a clicky switch, the click jacket snapping before the key bottoms out ----


def blue(click: float, bottom: float, seed: int, seconds: float = 0.16, rattle: bool = False, level: float = 1.0) -> list[float]:
    buffer = silence(seconds)
    # The click jacket: a very short bright tick plus a ringing 4-5 kHz resonance.
    noise_burst(buffer, 0.0, seed, 0.0015, 1.0 * level, highpass=0.9)
    tone(buffer, 0.0, click, [(1.0, 0.5, 0.004), (1.5, 0.2, 0.003)], attack=0.0003, level=level)
    # Bottoming out 18 ms later: a duller knock with a short plastic body.
    noise_burst(buffer, 0.018, seed + 1, 0.004, 0.55 * level, highpass=0.6, lowpass=0.35)
    tone(buffer, 0.018, bottom, [(1.0, 0.6, 0.012), (2.7, 0.15, 0.006)], attack=0.0005, level=level)
    if rattle:
        # A stabilizer wire rattling once on the way down.
        noise_burst(buffer, 0.034, seed + 2, 0.006, 0.25 * level, highpass=0.7, lowpass=0.5)
    return buffer


def mech_blue() -> dict[str, list[int]]:
    return {
        "key.wav": finish(blue(4300, 520, 11)),
        "space.wav": finish(blue(3600, 300, 21, seconds=0.2, rattle=True)),
        "enter.wav": finish(blue(3900, 380, 31, seconds=0.2, rattle=True)),
        "backspace.wav": finish(blue(4000, 450, 41)),
        "commit.wav": finish(blue(4600, 560, 51, seconds=0.12), level=0.45),
    }


# ---- soft-thock: a lubed linear switch on a dampened board, all body and no click ----


def thock(pitch: float, seed: int, seconds: float = 0.14, depth: float = 1.0) -> list[float]:
    buffer = silence(seconds)
    noise_burst(buffer, 0.0, seed, 0.006, 0.5, highpass=0.5, lowpass=0.18)
    tone(buffer, 0.0, pitch, [(1.0, 1.0, 0.02 * depth), (1.9, 0.3, 0.01), (3.1, 0.08, 0.005)], attack=0.001)
    return buffer


def soft_thock() -> dict[str, list[int]]:
    return {
        "key.wav": finish(thock(240, 61)),
        "space.wav": finish(thock(150, 71, seconds=0.18, depth=1.6)),
        "enter.wav": finish(thock(185, 81, seconds=0.16, depth=1.3)),
        "backspace.wav": finish(thock(210, 91)),
    }


# ---- kalimba: each key class plucks a different tine of a pentatonic kalimba ----

KALIMBA = [(1.0, 1.0, 0.45), (2.0, 0.08, 0.12), (5.4, 0.18, 0.05), (8.9, 0.05, 0.02)]


def tine(note: int, seconds: float = 0.9) -> list[float]:
    buffer = silence(seconds)
    noise_burst(buffer, 0.0, note, 0.0015, 0.12, highpass=0.85)
    tone(buffer, 0.0, midi(note), KALIMBA, attack=0.0015)
    return buffer


def kalimba() -> dict[str, list[int]]:
    # C major pentatonic around C5; the commit sound is a soft C-E-G arpeggio.
    chord = silence(1.2)
    for offset, note in enumerate((72, 76, 79)):
        tone(chord, offset * 0.06, midi(note), KALIMBA, attack=0.0015, level=0.8)
    return {
        "key.wav": finish(tine(76)),
        "space.wav": finish(tine(67)),
        "enter.wav": finish(tine(72)),
        "backspace.wav": finish(tine(69)),
        "commit.wav": finish(chord, level=0.5),
    }


# ---- melody samples: one note each; the packs' semitones play the tune ----


def guzheng() -> list[int]:
    """A plucked silk string on C5, starting a little sharp the way a pressed guzheng string settles."""
    buffer = silence(1.2)
    tone(buffer, 0.0, midi(72), [(1.0, 1.0, 0.5), (2.0, 0.45, 0.25), (3.0, 0.25, 0.12), (4.0, 0.12, 0.07)], attack=0.002, bend=0.35, bend_time=0.05)
    noise_burst(buffer, 0.0, 101, 0.002, 0.1, highpass=0.8)
    return finish(buffer)


def piano() -> list[int]:
    """A soft upright-piano-like note on A4: slightly stretched partials, the upper ones dying first."""
    buffer = silence(1.4)
    tone(buffer, 0.0, midi(69), [(1.0, 1.0, 0.7), (2.002, 0.5, 0.35), (3.006, 0.22, 0.18), (4.012, 0.1, 0.1), (5.02, 0.05, 0.06)], attack=0.003)
    noise_burst(buffer, 0.0, 111, 0.003, 0.06, highpass=0.6, lowpass=0.3)
    return finish(buffer)


def xylophone() -> list[int]:
    """A toy xylophone bar on C5: a bright, quickly fading strike with the bar's characteristic fourth partial."""
    buffer = silence(0.8)
    tone(buffer, 0.0, midi(72), [(1.0, 1.0, 0.22), (3.93, 0.35, 0.05), (9.2, 0.1, 0.015)], attack=0.001)
    noise_burst(buffer, 0.0, 121, 0.002, 0.15, highpass=0.75)
    return finish(buffer)


# ---- rain-ambience: steady rain with scattered close drops, looping seamlessly ----

MUSIC_RATE = 22_050


def rain() -> list[int]:
    seconds = 40.0
    total = int(seconds * MUSIC_RATE)
    generator = random.Random(2026)
    # Steady rain: brown-ish noise (white noise through two low-passes) plus a quieter hiss band.
    body = [0.0] * total
    low1 = low2 = previous_input = previous_high = 0.0
    for index in range(total):
        white = generator.uniform(-1.0, 1.0)
        low1 += 0.12 * (white - low1)
        low2 += 0.12 * (low1 - low2)
        high = 0.9 * (previous_high + white - previous_input)
        previous_input, previous_high = white, high
        # A slow swell so the rain breathes instead of sounding like static.
        swell = 0.85 + 0.15 * math.sin(2 * math.pi * index / total * 3)
        body[index] = swell * (1.6 * low2 + 0.08 * high)
    # Close drops: short downward-gliding plinks at random times and pitches.
    for _ in range(int(seconds * 7)):
        at = generator.uniform(0.0, seconds - 0.1)
        start_hz = generator.uniform(1800, 3800)
        level = generator.uniform(0.04, 0.16)
        start = int(at * MUSIC_RATE)
        phase = 0.0
        for offset in range(int(0.04 * MUSIC_RATE)):
            t = offset / MUSIC_RATE
            frequency = start_hz * (1.0 - 0.45 * min(1.0, t / 0.02))
            phase += 2 * math.pi * frequency / MUSIC_RATE
            body[start + offset] += level * math.sin(phase) * math.exp(-t / 0.008)
    # Loop seam: crossfade the last two seconds into the first two, then drop the tail, so the end runs into the start.
    seam = int(2.0 * MUSIC_RATE)
    looped = body[: total - seam]
    for offset in range(seam):
        mix = offset / seam
        looped[offset] = body[offset] * mix + body[total - seam + offset] * (1.0 - mix)
    peak = max(abs(value) for value in looped) or 1.0
    # Background music sits well below the key sounds.
    return [round(value / peak * 0.45 * 32767) for value in looped]


def write(path: Path, samples: list[int], rate: int = RATE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(struct.pack(f"<{len(samples)}h", *samples))


def main() -> int:
    for pack, files in (("mech-blue-switch", mech_blue()), ("soft-thock", soft_thock()), ("kalimba", kalimba())):
        for name, samples in files.items():
            write(PACKS / pack / name, samples)
    write(PACKS / "jasmine-flower/tone.wav", guzheng())
    write(PACKS / "fur-elise/tone.wav", piano())
    write(PACKS / "two-tigers/tone.wav", xylophone())
    write(PACKS / "rain-ambience/rain.wav", rain(), MUSIC_RATE)
    for path in sorted(PACKS.glob("*/*.wav")):
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
