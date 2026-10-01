#!/usr/bin/env python3
"""Synthesize the samples of templates/sound-keys deterministically with the standard library only, so the template ships no recorded audio and stays CC0."""

import math
import struct
import wave
from pathlib import Path

RATE = 22050
ROOT = Path(__file__).resolve().parent.parent / "templates" / "sound-keys"


def tone(frequency: float, millis: int, decay: float, noise: float = 0.0) -> list[float]:
    count = RATE * millis // 1000
    fade = max(1, RATE // 1000)
    seed = 1
    samples = []
    for index in range(count):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        hiss = (seed / 0x7FFFFFFF * 2 - 1) * noise
        value = (math.sin(2 * math.pi * frequency * index / RATE) + hiss) * math.exp(-decay * index / RATE)
        # Short linear ramps at both ends keep the sample free of clicks.
        value *= min(1.0, index / fade, (count - 1 - index) / fade)
        samples.append(value)
    return samples


def write(name: str, samples: list[float], peak: float = 0.5) -> None:
    loudest = max(abs(value) for value in samples) or 1.0
    frames = b"".join(struct.pack("<h", round(value / loudest * peak * 32767)) for value in samples)
    with wave.open(str(ROOT / name), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(frames)


def main() -> None:
    write("key.wav", tone(1800, 40, 120, noise=0.6))
    write("space.wav", tone(900, 60, 80, noise=0.5))
    write("enter.wav", tone(1200, 120, 30))
    write("backspace.wav", tone(1400, 50, 100, noise=0.4))
    write("commit.wav", tone(1568, 160, 20), peak=0.4)


if __name__ == "__main__":
    main()
