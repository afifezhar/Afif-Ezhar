"""Fails if any cut in an edit list lands in speech (loudness above the threshold at the cut point).

Usage (from video-edit/):
  python3 scripts/check_cuts.py edit A=/path/A_voice.wav B=/path/B_voice.wav [--threshold -30]
The edit directory must hold an edl.py exposing SEGMENTS = [(take, src_in, src_out), ...].
"""
import subprocess
import sys

import numpy as np

edit_dir, rest = sys.argv[1], sys.argv[2:]
threshold = -30.0
if "--threshold" in rest:
    i = rest.index("--threshold")
    threshold = float(rest[i + 1])
    rest = rest[:i] + rest[i + 2:]
voices = dict(arg.split("=", 1) for arg in rest)

sys.path.insert(0, edit_dir)
from edl import SEGMENTS  # noqa: E402


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


audio = {take: load(path) for take, path in voices.items()}


def db(x, t):
    i = int(t * 16000)
    w = x[max(i - 240, 0):i + 240]
    return float(20 * np.log10(np.sqrt((w ** 2).mean()) + 1e-9))


loud = [(k, a, b, round(db(audio[k], a), 1), round(db(audio[k], b), 1))
        for k, a, b in SEGMENTS if db(audio[k], a) > threshold or db(audio[k], b) > threshold]
print(f"{len(SEGMENTS) * 2} cut points, {len(loud)} in speech (> {threshold} dB)")
for row in loud:
    print("  ", row)
sys.exit(1 if loud else 0)
