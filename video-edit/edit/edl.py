"""Edit decision list for the full edit (~90 s), shared by prep.py (cuts media) and build.py (writes index.html).

Cuts are placed on ElevenLabs Scribe word boundaries (transcripts/*.scribe.json, run on the processed voice),
never inside a word. Within each kept span, any pause longer than MAX_PAUSE is shortened to KEEP_PAUSE.
Times are seconds in the source takes; output time comes from laying the segments end to end.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS = os.path.join(HERE, "..", "transcripts")
TAKE_FILES = {"A": "VID_20261027_081227", "B": "VID_20261027_081713"}
MAX_PAUSE, KEEP_PAUSE = 0.30, 0.18
LEAD, TAIL = 0.07, 0.10          # handles kept before the first and after the last word of a span
END_HOLD = 0.60                  # extra room after the very last word


def words(take):
    d = json.load(open(os.path.join(TRANSCRIPTS, TAKE_FILES[take] + ".scribe.json")))
    return [(w["text"], w["start"], w["end"]) for w in d["words"] if w["type"] == "word"]


WORDS = {k: words(k) for k in TAKE_FILES}

# Kept spans (take, first word start, last word end), in output order.
# Hook H4 is the closing question used as a cold open; the video ends on "actually trust" and loops back into it.
# Dropped for pace: "Video affiliate ke ... pun ada", "Mula-mula memang nampak impressive", "And here's something
# interesting", "Nampak tak apa yang sedang berlaku?", "AI ni memang powerful", "So, kalau korang buat content ...
# tiga tips untuk korang", "Demonstrate macam mana dia berfungsi", "Sebab at the end of the day", "So aku curious".
# E3: Take B names the year ("pada tahun 2026") in place of Take A's "pada tahun ni".
SPANS = [
    ("A", 123.00, 128.20),   # Korang sendiri masih percaya ke dengan AI generated product review ni?
    ("A", 2.26, 11.64),      # AI sekarang dah boleh buat video ... Cuba korang scroll TikTok sekarang.
    ("A", 16.86, 22.40),     # Ada yang guna AI model, AI voice ... guna produk tu.
    ("A", 25.02, 29.92),     # Tapi bila ramai sangat ... lebih kurang sama je.
    ("B", 32.32, 35.46),     # Menurut kajian TikTok tu sendiri pada tahun 2026,
    ("A", 35.76, 52.34),     # tiga daripada empat ... untuk membeli something.
    ("A", 55.44, 63.56),     # Technology is getting better ... jangan guna AI.
    ("A", 66.40, 74.96),     # Cuma kalau semua orang ... bukan lagi kelebihan utama dah.
    ("A", 84.32, 89.34),     # First, show, don't just generate. Kalau review produk, tunjuk produk sebenar tu sendiri.
    ("A", 92.68, 112.36),    # Second, share real experiences ... datang daripada diri kita sendiri.
    ("A", 114.48, 120.44),   # orang bukan sekadar nak tengok content yang cantik je. Dia nak something they can actually trust.
]


def silences(take):
    """Silent stretches (>= 60 ms below -40 dB) of the processed voice, from ffmpeg silencedetect."""
    return json.load(open(os.path.join(TRANSCRIPTS, TAKE_FILES[take] + ".silences.json")))


SILENCES = {k: silences(k) for k in TAKE_FILES}


def _segments(take, first, last, end_pad):
    """Every cut lands in a measured silence, so no word is clipped even where Scribe's word times drift."""
    ws = [w for w in WORDS[take] if first - 0.01 <= w[1] and w[2] <= last + 0.01]
    sil = SILENCES[take]
    # Span start: the end of the silence just before the first word.
    before = [x for x in sil if ws[0][1] - 0.6 <= x[1] <= ws[0][1] + 0.15]
    cur = max(before[-1][0], before[-1][1] - LEAD) if before else ws[0][1] - LEAD
    segs = []
    for (_, _, e0), (_, s1, _) in zip(ws, ws[1:]):
        if s1 - e0 <= MAX_PAUSE:
            continue
        gaps = [x for x in sil if x[1] > e0 - 0.15 and x[0] < s1 + 0.15 and x[1] - x[0] >= KEEP_PAUSE + 0.08]
        if not gaps:
            continue
        g0, g1 = max(gaps, key=lambda x: x[1] - x[0])
        segs.append((take, cur, g0 + KEEP_PAUSE / 2))
        cur = g1 - KEEP_PAUSE / 2
    # Span end: inside the silence just after the last word.
    after = [x for x in sil if ws[-1][2] - 0.15 <= x[0] <= ws[-1][2] + 0.6]
    end = min(after[0][1], after[0][0] + end_pad) if after else ws[-1][2] + end_pad
    segs.append((take, cur, end))
    return segs


def _frame(t):
    return round(round(t * 30) / 30, 4)


SEGMENTS = []
for i, (take, first, last) in enumerate(SPANS):
    pad = END_HOLD if i == len(SPANS) - 1 else TAIL
    SEGMENTS += [(k, _frame(a), _frame(b)) for k, a, b in _segments(take, first, last, pad)]


def timeline():
    """[(take, src_in, src_out, out_in)] in output order."""
    out, t = [], 0.0
    for take, a, b in SEGMENTS:
        out.append((take, a, b, round(t, 4)))
        t += b - a
    return out


TIMELINE = timeline()
DURATION = round(sum(b - a for _, a, b in SEGMENTS), 3)


def to_out(take, t):
    """Output time of source time t, or None if that moment was cut. Snaps into the nearest kept segment edge."""
    for k, a, b, o in TIMELINE:
        if k == take and a - 0.12 <= t <= b + 0.12:
            return round(o + min(max(t - a, 0), b - a), 3)
    return None


def kept_words():
    """[(text, out_start, out_end)] for every word that survives the cut, in output order."""
    out = []
    for take, first, last in SPANS:
        for text, s, e in WORDS[take]:
            if first - 0.01 <= s and e <= last + 0.01:
                os_, oe = to_out(take, s), to_out(take, e)
                if os_ is not None and oe is not None:
                    out.append((text, os_, oe))
    return out


if __name__ == "__main__":
    for row in TIMELINE:
        print(row)
    print("segments", len(SEGMENTS), "duration", DURATION, "words", len(kept_words()))
