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
MAX_PAUSE, KEEP_PAUSE = 0.22, 0.12
SPEED = 1.06                     # whole edit played 6% faster (pitch kept with atempo)
LEAD, TAIL = 0.07, 0.10          # handles kept before the first and after the last word of a span
END_HOLD = 0.35                  # extra room after the very last word (the end card follows)


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
    ("A", 121.38, 122.52),   # So aku curious.  (outro lead-in; the end card follows)
]

# Repeated or filler words dropped inside spans (take, first word start, last word end).
DROPS = [
    ("A", 20.74, 21.34),     # "product tu," in "kononnya tengah product tu, guna product tu"
    ("B", 33.56, 34.04),     # "tu sendiri" in "kajian TikTok tu sendiri"
    ("A", 39.44, 39.82),     # "sendiri" in "Asia Pasifik sendiri"
    ("A", 48.36, 48.92),     # "tu sendiri" in "authentic content tu sendiri"
    ("A", 88.76, 89.34),     # "tu sendiri" in "tunjuk produk sebenar tu sendiri"
]


def silences(take):
    """Silent stretches (>= 50 ms below -34 dB, so breaths count) of the processed voice, from ffmpeg silencedetect."""
    return json.load(open(os.path.join(TRANSCRIPTS, TAKE_FILES[take] + ".silences.json")))


SILENCES = {k: silences(k) for k in TAKE_FILES}


def energy(take):
    """10 ms loudness envelope (dB) of the processed voice."""
    return json.load(open(os.path.join(TRANSCRIPTS, TAKE_FILES[take] + ".energy.json")))["db"]


ENERGY = {k: energy(k) for k in TAKE_FILES}


def _quietest(take, t0, t1, length=0.0):
    """(start, mean dB) of the quietest window of `length` seconds inside [t0, t1]."""
    db = ENERGY[take]
    i0, i1, n = int(t0 * 100), int(t1 * 100), max(int(length * 100), 1)
    best = min(range(i0, max(i1 - n, i0) + 1), key=lambda i: sum(db[i:i + n]) / n)
    return best / 100, sum(db[best:best + n]) / n


def _drop_cut(take, prev, first, last, nxt):
    """Out and in points for removing words first..last between prev and nxt, at the quietest frames."""
    out_t, out_db = _quietest(take, prev[2] - 0.05, first[1] + 0.05)
    in_t, in_db = _quietest(take, last[2] - 0.05, nxt[1] + 0.05)
    return out_t, in_t, max(out_db, in_db)


def _span_words(take, first, last):
    return [w for w in WORDS[take] if first - 0.01 <= w[1] and w[2] <= last + 0.01]


def _clean_drops():
    """Only keep a drop when both of its cuts land below -32 dB; words said in one breath stay in."""
    ok = []
    for take, a, b in DROPS:
        ws = WORDS[take]
        idx = [i for i, w in enumerate(ws) if a - 0.01 <= w[1] and w[2] <= b + 0.01]
        prev, nxt = ws[idx[0] - 1], ws[idx[-1] + 1]
        if _drop_cut(take, prev, ws[idx[0]], ws[idx[-1]], nxt)[2] < -32:
            ok.append((take, a, b))
    return ok


DROPS = _clean_drops()


def _dropped(take, w):
    return any(k == take and a - 0.01 <= w[1] and w[2] <= b + 0.01 for k, a, b in DROPS)


def _segments(take, first, last, end_pad):
    """Cuts land in measured silence, or failing that in the quietest stretch of the gap, so no word is clipped
    even where Scribe's word times drift. Dropped words are cut out at the quietest frames on either side."""
    span = _span_words(take, first, last)
    kept = [w for w in span if not _dropped(take, w)]
    sil = SILENCES[take]
    # Span start: the end of the silence just before the first word.
    before = [x for x in sil if kept[0][1] - 0.6 <= x[1] <= kept[0][1] + 0.15]
    cur = max(before[-1][0], before[-1][1] - LEAD) if before else kept[0][1] - LEAD
    segs = []
    for prev, w in zip(kept, kept[1:]):
        skipped = [x for x in span if prev[2] <= x[1] and x[2] <= w[1] and _dropped(take, x)]
        if skipped:
            out_t, in_t, _ = _drop_cut(take, prev, skipped[0], skipped[-1], w)
            segs.append((take, cur, out_t))
            cur = in_t
        elif w[1] - prev[2] > MAX_PAUSE:
            gaps = [x for x in sil if x[1] > prev[2] - 0.15 and x[0] < w[1] + 0.15 and x[1] - x[0] >= KEEP_PAUSE + 0.06]
            if gaps:
                g0, g1 = max(gaps, key=lambda x: x[1] - x[0])
                segs.append((take, cur, g0 + KEEP_PAUSE / 2))
                cur = g1 - KEEP_PAUSE / 2
            else:
                # No clean silence (a breath, room tone): remove the quietest stretch, clear of both words.
                cut = w[1] - prev[2] - KEEP_PAUSE
                t, mean = _quietest(take, prev[2] + 0.04, w[1] - 0.04, cut)
                if mean < -32:
                    segs.append((take, cur, t))
                    cur = t + cut
    # Span end: inside the silence just after the last kept word, or before any dropped tail words.
    tail = [x for x in span if x[1] >= kept[-1][2] and _dropped(take, x)]
    after = [x for x in sil if kept[-1][2] - 0.15 <= x[0] <= kept[-1][2] + 0.6]
    if tail:
        end = _quietest(take, kept[-1][2] - 0.05, tail[0][1] + 0.05)[0]
    else:
        end = min(after[0][1], after[0][0] + end_pad) if after else kept[-1][2] + end_pad
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
CUT_LENGTH = round(sum(b - a for _, a, b in SEGMENTS), 3)      # before the speed-up
SPEECH_END = round(CUT_LENGTH / SPEED, 3)                       # output time where the talk ends
END_CARD = 3.2
DURATION = round(SPEECH_END + END_CARD, 3)


def to_out(take, t):
    """Output time of source time t (after the speed-up), or None if that moment was cut."""
    for k, a, b, o in TIMELINE:
        if k == take and a - 0.12 <= t <= b + 0.12:
            return round((o + min(max(t - a, 0), b - a)) / SPEED, 3)
    return None


def kept_words():
    """[(text, out_start, out_end)] for every word that survives the cut, in output order."""
    out = []
    for take, first, last in SPANS:
        for text, s, e in WORDS[take]:
            if first - 0.01 <= s and e <= last + 0.01 and not _dropped(take, (text, s, e)):
                os_, oe = to_out(take, s), to_out(take, e)
                if os_ is not None and oe is not None:
                    out.append((text, os_, oe))
    return out


if __name__ == "__main__":
    for row in TIMELINE:
        print(row)
    print("segments", len(SEGMENTS), "speech", SPEECH_END, "duration", DURATION, "words", len(kept_words()))
