"""Synthesize the 15s music bed + sound design for the Holiday Encore promo."""
import sys, wave
import numpy as np

SR = 48000
DUR = 15.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
mixL = np.zeros(N); mixR = np.zeros(N)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mixL[i:i + len(sig)] += sig * l * 1.414
    mixR[i:i + len(sig)] += sig * r * 1.414


def tt(d): return np.arange(int(d * SR)) / SR


def env(d, a=0.005, r=None):
    t = tt(d); r = r or d
    return np.minimum(1, t / a) * np.exp(-t / (r / 5))


def stft_filter(x, lo, hi):
    """Time-varying band-pass: lo/hi are functions of normalized time 0..1 -> Hz."""
    n, hop = 2048, 512
    win = np.hanning(n)
    pad = np.concatenate([np.zeros(n), x, np.zeros(n)])
    out = np.zeros_like(pad); norm = np.zeros_like(pad)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    frames = range(0, len(pad) - n, hop)
    total = max(1, len(pad) - n)
    for s in frames:
        u = min(max((s - n) / max(1, len(x)), 0), 1)
        l, h = lo(u), hi(u)
        mask = 1 / (1 + ((freqs - (l + h) / 2) / ((h - l) / 2 + 1)) ** 4)
        spec = np.fft.rfft(pad[s:s + n] * win) * mask
        out[s:s + n] += np.fft.irfft(spec) * win
        norm[s:s + n] += win ** 2
    out = out / np.maximum(norm, 1e-6)
    return out[n:n + len(x)]


def lowpass(x, fc):
    spec = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(spec / (1 + (f / fc) ** 4), len(x))


def reverb(x, secs=2.2, wet=0.3):
    ir = rng.standard_normal(int(secs * SR)) * np.exp(-np.arange(int(secs * SR)) / SR * 6.9 / secs)
    ir = lowpass(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + len(ir)
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[: len(x)]
    return x * (1 - wet) + y * wet * 0.6


def note(m): return 440 * 2 ** ((m - 69) / 12)

# ---------------- SFX ----------------
def tick(f=3200, d=0.06):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 90) + rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.3

def whoosh(d=0.6, up=True):
    x = rng.standard_normal(int(d * SR))
    lo = (lambda u: 200 + 3000 * u) if up else (lambda u: 3200 - 3000 * u)
    y = stft_filter(x, lo, lambda u: lo(u) * 2.2 + 400)
    shape = np.sin(np.pi * np.linspace(0, 1, len(y))) ** 2
    return y * shape / (np.abs(y).max() + 1e-9)

def riser(d):
    t = tt(d); u = t / d
    x = stft_filter(rng.standard_normal(len(t)), lambda u: 300 + 6000 * u ** 2, lambda u: 900 + 9000 * u ** 2)
    x /= np.abs(x).max()
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * u ** 2) / SR) * 0.25
    return (x * 0.7 + tone) * u ** 2.5

def impact(d=2.5):
    t = tt(d)
    boom = np.sin(2 * np.pi * np.cumsum(30 + 90 * np.exp(-t * 18)) / SR) * np.exp(-t * 2.2)
    crack = lowpass(rng.standard_normal(len(t)), 5000) * np.exp(-t * 30) * 0.6
    return reverb(boom + crack, 2.5, 0.35)

def pop(f=900):
    t = tt(0.12)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-t * 60))) / SR) * np.exp(-t * 40)

def chime(m=84):
    t = tt(1.6); s = sum(np.sin(2 * np.pi * note(m) * k * t) * np.exp(-t * (2 + k)) / k for k in (1, 2, 3, 4.2))
    return reverb(s, 2.0, 0.4)

# ---------------- Music (150 bpm, beat grid from 1.3s) ----------------
BEAT = 0.4; T0 = 1.3
def kick():
    t = tt(0.45); return np.sin(2 * np.pi * np.cumsum(45 + 140 * np.exp(-t * 35)) / SR) * np.exp(-t * 7)
def clap():
    t = tt(0.3); x = stft_filter(rng.standard_normal(len(t)), lambda u: 900, lambda u: 4000)
    return x / np.abs(x).max() * np.exp(-t * 18)
def hat():
    t = tt(0.08); x = stft_filter(rng.standard_normal(len(t)), lambda u: 7000, lambda u: 16000)
    return x / np.abs(x).max() * np.exp(-t * 60)
K, C, H = kick(), clap(), hat()

def pad(notes, d):
    t = tt(d); s = np.zeros(len(t))
    for m in notes:
        for det in (-0.12, 0, 0.12):
            ph = (note(m + det) * t) % 1
            s += 2 * ph - 1
    s = lowpass(s, 1800) / (len(notes) * 3)
    a = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.3)
    return s * a

chords = [[53, 57, 60, 64], [55, 59, 62, 64], [57, 60, 64, 67], [52, 55, 60, 64]]  # Fmaj7 G6 Am7 C/E
roots = [41, 43, 45, 40]
bar = BEAT * 4
music = np.zeros(N); drums = np.zeros(N); bass = np.zeros(N)

def put(buf, sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: buf[i:i + len(sig[: N - i])] += sig[: N - i] * g

for b in range(9):  # 9 bars from 1.3s -> 15.7s
    ts = T0 + b * bar
    put(music, pad(chords[b % 4], bar + 0.3), ts, 0.5)
    # sub bass, gated 8ths
    tb = tt(bar); f = note(roots[b % 4])
    gate = 0.35 + 0.65 * (((tb / (BEAT / 2)) % 1) < 0.7)
    if ts < 12.1: put(bass, np.sin(2 * np.pi * f * tb) * gate * 0.6 + np.sin(4 * np.pi * f * tb) * 0.1, ts)
    # pluck arpeggio 16ths
    for k in range(16):
        tn = ts + k * BEAT / 4
        m = chords[b % 4][[0, 1, 2, 3, 2, 1, 3, 2][k % 8]] + 24
        tp = tt(0.25)
        put(music, np.sin(2 * np.pi * note(m) * tp) * np.exp(-tp * 18) * (0.18 if tn > 3.2 else 0.08), tn)

beats = np.arange(T0, 15, BEAT)
for i, tb in enumerate(beats):
    if tb >= 12.1: break               # drop out before the end impact
    if tb < 3.2 and i % 2: continue    # sparse intro
    put(drums, K, tb, 0.9)
    if tb >= 3.2 and i % 2 == 1: put(drums, C, tb, 0.35)
    if tb >= 3.2:
        put(drums, H, tb + BEAT / 2, 0.18)

# sidechain: duck pad + bass on each kick
duck = np.ones(N)
for tb in beats:
    if tb >= 12.1: break
    i = int(tb * SR); L = int(0.3 * SR)
    seg = 1 - 0.6 * np.exp(-np.arange(L) / SR * 14)
    duck[i:i + L] = np.minimum(duck[i:i + L], seg[: N - i])
music *= duck; bass *= duck

# intro: soft pad swell under the type
intro = pad([57, 60, 64, 69], 1.6) * np.linspace(0, 1, int(1.6 * SR)) ** 2
put(music, intro, 0, 0.35)
music = reverb(music, 2.4, 0.35)
fade = np.ones(N); fs = int(13.6 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
for buf, g in ((music, 0.8), (drums, 0.7), (bass, 0.75)):
    mixL += buf * fade * g; mixR += buf * fade * g

# ---------------- SFX placement ----------------
for i, t in enumerate((0.1, 0.35, 0.7, 0.95)): add(tick(2600 + i * 300), t, 0.25, [-.3, .3, -.2, .2][i])
add(riser(1.4), 0.05, 0.35)
add(whoosh(0.5), 1.2, 0.35)
add(impact(), 1.45, 0.9)
for i, t in enumerate((3.3, 4.1, 4.9, 5.7)):
    add(whoosh(0.45, i % 2 == 0), t - 0.2, 0.4, [-.5, .5, -.5, .5][i])
    add(tick(1800, 0.08), t + 0.15, 0.25)
add(whoosh(0.7), 6.2, 0.4); add(impact(1.5), 6.6, 0.45)
for i in range(7): add(pop(700 + i * 90), 6.8 + i * 0.1, 0.35, (-0.6 + i * 0.2))
add(whoosh(0.5, False), 8.2, 0.4); add(impact(1.8), 8.5, 0.4)
for i in range(11): add(tick(1500 + i * 180, 0.04), 8.7 + 0.8 * (1 - (1 - i / 10) ** 0.5), 0.3)
add(chime(88), 9.45, 0.3)
add(whoosh(0.5), 10.2, 0.4)
sw = tt(1.1); add(np.sin(2 * np.pi * np.cumsum(400 + 800 * sw / 1.1) / SR) * np.sin(np.pi * sw / 1.1) * 0.25, 10.7, 0.5)
add(pop(1200), 10.7, 0.3, -0.7); add(chime(91), 11.6, 0.3, 0.7)
add(riser(0.9), 11.45, 0.35); add(whoosh(0.4), 12.1, 0.4)
add(impact(2.6), 12.4, 1.0)
add(chime(81), 12.45, 0.25)
add(pop(1000), 13.45, 0.35)

mix = np.stack([mixL, mixR], 1)
mix = np.tanh(mix * 1.1) ; mix /= np.abs(mix).max() / 0.89
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok')
