"""Writes index.html for the full Style D edit from the EDL (edl.py) and the Scribe word times.

- Talking head: base.mp4 (cut by prep.py), alternating 100% / 107% punch-in on every jump cut.
- Kold captions: phrases of up to 4 words, one emphasis word per phrase in a large face, shown word by word.
- B-roll: eight full-screen motion-graphic inserts, alternating black and white canvases, timed to the spoken words.
Run from video-edit/edit:  python3 build.py
"""
import re

from edl import DURATION, END_CARD, SPEECH_END, TIMELINE, kept_words, to_out

STAR_PATH = "M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z"
NUMBERS = {"tiga": "3", "empat": "4", "sembilan": "9", "sepuluh": "10"}
KEEP_CASE = {"ai": "AI", "tiktok": "TikTok", "asia": "Asia", "pasifik": "Pacific"}
# Emphasis priority: the first of these found in a phrase gets the big face.
EMPHASIS = ["authenticity", "authentic", "perfect", "real", "trust", "percaya", "skip", "show", "tool", "identity",
            "sama", "cantik", "experiences", "limitation", "personaliti", "kelebihan", "better", "generated", "generate",
            "valuable", "bagus", "diri", "review", "model", "voice", "powerful", "sebenar", "2026", "ai"]
STYLES = ["kserif i", "kit", "kserif", "kbig"]


def O(take, t):
    v = to_out(take, t)
    assert v is not None, (take, t)
    return v


# ---------------------------------------------------------------- b-roll (source times -> output times)

def typed(text, t0, t1, top, extra=""):
    return f'<div class="ov eyebrow typed" style="top:{top}px{extra}" data-text="{text}" data-t0="{t0}" data-t1="{t1}"></div>'


def star(pos):
    return f'<svg class="star" viewBox="0 0 100 100" style="{pos}"><path d="{STAR_PATH}"/></svg>'


def w(text, t):
    return f'<span class="wd" data-in="{t}">{text}</span>'


def mk(html, light):
    return re.sub(r'(<span class="wd"[^>]*>)(.*?)(</span>)', r'\1<span class="mk">\2</span>\3', html) if light else html


PERSON = ('<svg class="pop off" data-in="{t}"{on} viewBox="0 0 100 140"><circle cx="50" cy="34" r="24"/>'
          '<path d="M8 140 C8 96 28 74 50 74 C72 74 92 96 92 140 Z"/></svg>')


def ai_card(i, t=None):
    attrs = f' class="aicard pop" data-in="{t}"' if t is not None else ' class="aicard"'
    return (f'<div{attrs}><svg viewBox="0 0 100 140"><circle cx="50" cy="34" r="24"/><path d="M8 140 C8 96 28 74 50 74 C72 74 92 96 92 140 Z"/></svg>'
            f'<i></i><i class="s"></i>{"<b>AI</b>" if i in (0, 4, 8) else ""}</div>')


def broll():
    """[(id, start, end, light, html)]"""
    S = "assets/stock/"
    out = []

    a, b = O("A", 6.88) - 0.05, O("A", 9.52) + 0.06
    out.append(("b1", a, b, False,
                star("right:-150px;top:-170px") + typed("Tapi persoalannya,", O("A", 6.88), O("A", 8.0), 250)
                + f'<div class="ov mgbig" style="top:310px">{w("orang", O("A", 8.38))}<br>{w("masih", O("A", 8.62))}</div>'
                + f'<img class="stock rise" data-in="{a + 0.1:.3f}" src="{S}statue.png" alt="" style="left:330px;top:560px;height:1240px" />'
                + f'<div class="ov mgbig" style="top:910px;z-index:3">{w("percaya", O("A", 8.86))}<br>{w("ke?", O("A", 9.22))}</div>'))

    a, b = O("A", 10.14) - 0.05, O("A", 11.64) + 0.12
    out.append(("b2", a, b, True,
                typed("Cuba korang scroll TikTok sekarang,", O("A", 10.14), O("A", 11.5), 250)
                + f'<div class="feed scroll" data-t0="{a:.3f}" data-t1="{b:.3f}" style="left:300px;top:330px;transform:rotate(-6deg) scale(0.8);transform-origin:50% 0">'
                + '<div class="track">'
                + "".join(f'<div class="card"><img src="{S}{img}.png" alt="" /><span class="tag">{tag}</span></div>'
                          for img, tag in (("bags", "#affiliate"), ("mic", "#productreview"), ("record", "#iklan"), ("bags", "#review")))
                + '</div><div class="ui"><i></i><i></i><i></i></div></div>'))

    a, b = O("A", 16.86) - 0.05, O("A", 18.98) + 0.01
    wave = "".join(f'<b style="height:{h}px"></b>' for h in (30, 70, 110, 60, 96, 120, 54, 88, 40, 104, 66, 28, 80, 112, 48))
    out.append(("b3", a, b, False,
                typed("Ada yang guna", O("A", 16.86), O("A", 17.32), 250)
                + f'<div class="ov mgbig" style="top:300px">{w("AI", O("A", 17.38))} {w("model,", O("A", 17.64))}</div>'
                + f'<div class="aiphone pop" data-in="{O("A", 17.38):.3f}" style="left:440px;top:470px;width:400px">{ai_card(0)}</div>'
                + f'<div class="aibadge pop" data-in="{O("A", 17.64):.3f}" style="left:380px;top:520px">AI GENERATED</div>'
                + f'<div class="wave pop" data-in="{O("A", 18.34):.3f}" style="left:64px;top:1060px">{wave}</div>'
                + f'<div class="ov mgmid" style="top:1190px;z-index:3">{w("AI", O("A", 18.34))} {w("voice.", O("A", 18.68))}</div>'))

    a, b = O("A", 27.48) - 0.05, O("A", 29.92) + 0.06
    out.append(("b4", a, b, True,
                typed("Lama-lama semuanya nampak", O("A", 27.48), O("A", 28.54), 250)
                + '<div class="grid9" style="left:64px;top:320px;width:600px">'
                + "".join(ai_card(i, round(a + 0.05 + i * 0.09, 3)) for i in range(9)) + '</div>'
                + f'<div class="ov mgbig" style="top:1110px;z-index:3">{w("sama", O("A", 29.26))} {w("je.", O("A", 29.72))}</div>'))

    a, b = O("B", 32.32) - 0.05, O("A", 44.64) + 0.06
    # Four grey people from the start of the insert; three turn yellow on "pengguna".
    people = "".join(PERSON.format(t=round(a + 0.3 + i * 0.1, 3), on=f' data-on="{O("A", 36.88) + i * 0.15:.3f}"' if i < 3 else "")
                     for i in range(4))
    out.append(("b5", a, b, True,
                star("left:-200px;bottom:-200px") + typed("Menurut kajian TikTok 2026,", O("B", 32.32), O("B", 35.46), 250)
                + f'<div class="ov mgbig" style="top:300px;font-size:210px">{w("3", O("A", 35.76))} {w("dari", O("A", 36.2))} {w("4", O("A", 36.48))}</div>'
                + f'<div class="people" style="left:90px;top:620px;width:780px">{people}</div>'
                + f'<div class="ov mgmid" style="top:1080px">{w("skip", O("A", 40.32))} {w("content", O("A", 40.7))}</div>'
                + f'<div class="ov mgsmall wd" data-in="{O("A", 41.42):.3f}" style="top:1200px">yang nampak terlalu polished atau AI.</div>'))

    a, b = O("A", 45.22) - 0.05, O("A", 52.34) + 0.06
    dots = "".join(f'<i class="pop{" off" if i == 9 else ""}" data-in="{round(O("A", 45.4) + i * 0.08, 3)}"></i>' for i in range(10))
    out.append(("b6", a, b, False,
                typed("dan 9 daripada 10 kata", O("A", 45.22), O("A", 46.9), 250)
                + f'<div class="ov mgbig" style="top:300px;font-size:150px">{w("authentic", O("A", 47.52))}</div>'
                + f'<div class="dots" style="left:90px;top:520px;width:500px">{dots}</div>'
                + f'<img class="stock rise" data-in="{O("A", 49.72):.3f}" src="{S}bags.png" alt="" style="left:420px;top:760px;width:560px" />'
                + f'<div class="ov mgsmall wd" data-in="{O("A", 48.98):.3f}" style="top:1230px">content pengaruh keputusan membeli.</div>'))

    a, b = O("A", 84.32) - 0.05, O("A", 88.70) + 0.06
    out.append(("b7", a, b, True,
                star("right:-150px;top:-170px") + typed("First,", O("A", 84.32), O("A", 84.56), 250)
                + f'<div class="ov mgbig" style="top:300px;font-size:230px">{w("show,", O("A", 84.98))}</div>'
                + f'<div class="ov mgsmall wd" data-in="{O("A", 85.56):.3f}" style="top:540px;font-size:44px">don\'t just generate.</div>'
                + f'<img class="stock rise" data-in="{a + 0.1:.3f}" src="{S}record.png" alt="" style="left:-60px;top:660px;width:1100px" />'
                + f'<div class="ov mgmid" style="top:1150px;z-index:3;font-size:68px">{w("tunjuk", O("A", 87.74))} {w("produk", O("A", 88.08))} {w("sebenar.", O("A", 88.38))}</div>'))

    a, b = O("A", 101.18) - 0.05, O("A", 105.34) + 0.06
    out.append(("b8", a, b, False,
                f'<img class="stock drop" data-in="{a + 0.05:.3f}" src="{S}claw.png" alt="" style="left:470px;top:-120px;height:1180px" />'
                + typed("Third, use AI as a", O("A", 101.18), O("A", 103.14), 760)
                + f'<div class="ov mgbig" style="top:820px;font-size:220px;z-index:3">{w("tool,", O("A", 103.2))}</div>'
                + f'<div class="ov mgmid soft" style="top:1030px">{w("not", O("A", 103.7))} {w("your", O("A", 104.0))}</div>'
                + f'<div class="ov mgmid" style="top:1116px">{w("identity.", O("A", 104.68))}</div>'
                + '<div class="ov barcode" style="left:64px;top:1250px;width:220px;height:48px"></div>'))
    # Outro end card on the music after "So aku curious.": the question, then the call to action.
    a, b = SPEECH_END - 0.02, DURATION
    out.append(("end", a, b, False,
                star("right:-150px;top:-170px") + typed("jadi, korang", a + 0.15, a + 0.6, 250)
                + f'<div class="ov mgbig" style="top:310px;font-size:150px">{w("masih", a + 0.55)}<br>{w("percaya?", a + 0.75)}</div>'
                + f'<div class="ov mgmid wd" data-in="{a + 1.0:.3f}" style="top:620px;color:#fff;font-size:84px">AI-generated<br>product review.</div>'
                + "".join(f'<div class="bubble pop" data-in="{a + 1.2 + i * 0.18:.3f}" style="left:{x}px;top:{y}px;width:{wd}px"><i></i><b></b><b class="s"></b></div>'
                          for i, (x, y, wd) in enumerate(((64, 830, 560), (300, 930, 600), (120, 1030, 520))))
                + f'<div class="cta pop" data-in="{a + 1.75:.3f}" style="left:64px;top:1150px">Komen kat bawah &#8595;</div>'
                + f'<div class="ov mgsmall wd" data-in="{a + 2.0:.3f}" style="top:1262px;color:rgba(255,255,255,0.8)">Follow untuk tips content yang real.</div>'))
    return [(i, round(a, 3), round(b, 3), light, mk(html, light)) for i, a, b, light, html in out]


BROLL = broll()


def in_broll(t, margin=0.0):
    return any(a - margin <= t <= b + margin for _, a, b, _, _ in BROLL)


# ---------------------------------------------------------------- Kold captions

def display(word, nxt):
    core = re.sub(r"[^\w'-]", "", word).lower()
    punct = word[len(word.rstrip(".,?!")):]
    if core in NUMBERS:
        return NUMBERS[core] + punct
    if core == "product" and (nxt or "").lower().strip(".,?!") != "review":
        return "produk" + punct
    if core in KEEP_CASE:
        return KEEP_CASE[core] + punct
    return word.lower()


def phrases():
    ws = [(display(t, ws_next), s, e) for (t, s, e), ws_next in
          zip(kept_words(), [x[0] for x in kept_words()[1:]] + [None])]
    groups, cur = [], []
    for i, (t, s, e) in enumerate(ws):
        if in_broll(s):
            if cur:
                groups.append(cur)
                cur = []
            continue
        if cur and (s - cur[-1][2] > 0.45 or len(cur) == 5):
            groups.append(cur)
            cur = []
        cur.append((t, s, e))
        if t[-1] in ".?!" or (t[-1] == "," and len(cur) >= 2):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    # Fold one-word fragments into a neighbour: a sentence tail joins the phrase before it,
    # a lead-in like "second," joins the phrase after it.
    merged = []
    for g in groups:
        if merged and len(g) == 1 and len(merged[-1]) <= 5 and g[0][1] - merged[-1][-1][2] < 0.35 \
                and merged[-1][-1][0][-1] not in ".?!":
            merged[-1] = merged[-1] + g
        else:
            merged.append(g)
    out = []
    for g in merged:
        if out and len(out[-1]) == 1 and len(g) <= 4 and g[0][1] - out[-1][-1][2] < 0.7 and out[-1][-1][0][-1] not in ".?!":
            out[-1] = out[-1] + g
        else:
            out.append(g)
    return out


def emphasis_index(g):
    found = [(EMPHASIS.index(k), -i, i) for i, (t, _, _) in enumerate(g)
             for k in [re.sub(r"[^\w]", "", t).lower()] if k in EMPHASIS]
    # A big word reads better after a small lead-in, unless the opening word is the point of the video.
    lead_ok = found if found and min(found)[0] < 3 else ([f for f in found if f[2] > 0] or found)
    if lead_ok:
        return min(lead_ok)[2]
    return max(range(len(g)), key=lambda i: (len(g[i][0]), i))


def phrase_html(n, g):
    k = emphasis_index(g)
    style = STYLES[n % len(STYLES)]
    if len(re.sub(r"[^\w]", "", g[k][0])) > 11 and style.startswith("kserif"):
        style = "kit"
    span = lambda items: " ".join(f'<span class="w" data-in="{s:.3f}">{t}</span>' for t, s, _ in items)
    lines = []
    if g[:k]:
        lines.append(f'<div class="ks">{span(g[:k])}</div>')
    lines.append(f'<div class="{style}">{span([g[k]])}</div>')
    if g[k + 1:]:
        lines.append(f'<div class="ks">{span(g[k + 1:])}</div>')
    return "".join(lines)


PHRASES = phrases()


def caption_blocks():
    blocks = []
    for n, g in enumerate(PHRASES):
        show = g[0][1] - 0.04
        hide = PHRASES[n + 1][0][1] - 0.06 if n + 1 < len(PHRASES) else SPEECH_END
        hide = min(hide, g[-1][2] + 1.2)
        for _, a, _, _, _ in BROLL:          # never run into a b-roll
            if show < a < hide:
                hide = a - 0.02
        blocks.append(f'      <div id="k{n}" class="ov kold" data-show="{show:.3f}" data-hide="{hide:.3f}">{phrase_html(n, g)}</div>')
    return "\n".join(blocks)


# ---------------------------------------------------------------- page

cuts = [o for _, _, _, o in TIMELINE[1:]]
broll_html = "\n".join(
    f'      <div id="{i}" class="mg{" light" if light else ""} clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="1">{html}</div>'
    for i, a, b, light, html in BROLL)
stars = "\n".join(
    f'      <svg id="s-{i}" class="tstar{" ink" if light else ""}" viewBox="0 0 100 100"><path d="{STAR_PATH}"/></svg>'
    for i, a, b, light, html in BROLL)
whooshes = "\n".join(
    f'      <audio id="sw-{i}" src="assets/media/whoosh.mp3" data-start="{max(a - 0.3, 0):.3f}" data-duration="1" data-volume="0.5" data-track-index="{4 + n % 2}"></audio>'
    for n, (i, a, b, light, html) in enumerate(BROLL))
typing = "\n".join(
    f'      <audio id="st-{i}" src="assets/media/type.mp3" data-start="{a + 0.05:.3f}" data-duration="1.5" data-volume="0.25" data-track-index="{6 + n % 2}"></audio>'
    for n, (i, a, b, light, html) in enumerate(BROLL))
broll_times = [[i, a, b] for i, a, b, _, _ in BROLL]

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/style-d.css" />
    <style>
      .kold {{ opacity: 0; }}
      .kold .w, .wd, .pop, .rise, .drop {{ opacity: 0; }}
      .wd {{ display: inline-block; }}
      .typed .c {{ opacity: 0; }}
      .feed .track {{ position: relative; }}
      .tstar {{ position: absolute; right: -150px; top: -170px; width: 520px; height: 520px; z-index: 20; opacity: 0; }}
      .tstar path {{ fill: #ffd60a; }}
      .tstar.ink path {{ fill: #0b0b0b; }}
      .bubble {{ position: absolute; z-index: 2; height: 84px; border-radius: 42px; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,0.4); }}
      .bubble i {{ position: absolute; left: 14px; top: 14px; width: 56px; height: 56px; border-radius: 50%; background: #d6d6d6; }}
      .bubble b {{ position: absolute; left: 88px; top: 22px; width: 55%; height: 14px; border-radius: 7px; background: #cfcfcf; }}
      .bubble b.s {{ top: 48px; width: 35%; background: #e4e4e4; }}
      .cta {{ position: absolute; z-index: 3; font: 800 54px/1 "Inter", sans-serif; color: #111; background: #ffd60a; padding: 22px 34px; border-radius: 999px; }}
    </style>
  </head>
  <body>
    <!-- Full edit, Style D ({DURATION} s). Generated by build.py from edl.py; do not edit by hand. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
      <video id="base" class="plate clip" src="assets/media/base.mp4" muted data-start="0" data-duration="{SPEECH_END}" data-track-index="0"></video>
      <div id="fade" class="fade"></div>

{caption_blocks()}

{broll_html}
{stars}

      <audio id="a-voice" src="assets/media/voice.m4a" data-start="0" data-duration="{SPEECH_END}" data-track-index="2"></audio>
      <audio id="a-music" src="assets/media/music.m4a" data-start="0" data-duration="{DURATION}" data-volume="0.55" data-track-index="3"></audio>
{whooshes}
{typing}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});

      // Punch-in alternates on every jump cut so the cuts read as intentional.
      const cuts = {cuts};
      cuts.forEach((t, i) => tl.set("#base", {{ scale: i % 2 ? 1 : 1.07, transformOrigin: "50% 30%" }}, t));

      // Kold captions: phrase on, each word on its spoken time, phrase off.
      document.querySelectorAll(".kold").forEach((k) => {{
        tl.set(k, {{ opacity: 1 }}, +k.dataset.show);
        k.querySelectorAll(".w").forEach((w) =>
          tl.fromTo(w, {{ opacity: 0, y: 22, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.16, ease: "power2.out", immediateRender: false }}, +w.dataset.in));
        tl.to(k, {{ opacity: 0, duration: 0.08 }}, +k.dataset.hide);
      }});

      // B-roll: typed eyebrows, words sliding in, objects rising, icons popping.
      document.querySelectorAll(".typed").forEach((e) => {{
        const text = e.dataset.text, t0 = +e.dataset.t0, t1 = +e.dataset.t1;
        for (const ch of text) {{ const s = document.createElement("span"); s.className = "c"; s.textContent = ch; e.appendChild(s); }}
        e.querySelectorAll(".c").forEach((c, i) => tl.set(c, {{ opacity: 1 }}, t0 + i * ((t1 - t0) / text.length)));
      }});
      document.querySelectorAll(".wd").forEach((e) =>
        tl.fromTo(e, {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.22, ease: "power3.out", immediateRender: false }}, +e.dataset.in));
      document.querySelectorAll(".rise").forEach((e) =>
        tl.fromTo(e, {{ opacity: 0, y: 260 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out", immediateRender: false }}, +e.dataset.in));
      document.querySelectorAll(".drop").forEach((e) =>
        tl.fromTo(e, {{ opacity: 0, y: -300 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: false }}, +e.dataset.in));
      document.querySelectorAll(".pop").forEach((e) =>
        tl.fromTo(e, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, +e.dataset.in));
      document.querySelectorAll("[data-on]").forEach((e) =>
        tl.set(e.querySelectorAll("path, circle"), {{ fill: "#ffd60a" }}, +e.dataset.on));
      document.querySelectorAll(".scroll").forEach((e) =>
        tl.fromTo(e.querySelector(".track"), {{ y: 0 }}, {{ y: -880, duration: +e.dataset.t1 - +e.dataset.t0, ease: "power1.inOut", immediateRender: false }}, +e.dataset.t0));
      document.querySelectorAll(".wave b").forEach((b, i) =>
        tl.fromTo(b, {{ scaleY: 0.3 }}, {{ scaleY: 1, duration: 0.22, repeat: 7, yoyo: true, ease: "sine.inOut", immediateRender: false }}, {BROLL[2][1]} + (i % 5) * 0.05));

      // Star wipe into every b-roll: grows from the corner to cover the frame, then settles as a corner ornament.
      {broll_times}.forEach(([id, a, b]) => {{
        const s = "#s-" + id;
        tl.set(s, {{ opacity: 1 }}, a - 0.24);
        tl.fromTo(s, {{ scale: 0, rotation: -120, transformOrigin: "50% 50%" }}, {{ scale: 38, rotation: 0, duration: 0.24, ease: "power3.in", immediateRender: false }}, a - 0.24);
        tl.to(s, {{ scale: 1, rotation: 20, duration: 0.45, ease: "power3.out" }}, a);
        tl.set(s, {{ opacity: 0 }}, b);
      }});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)
print("duration", DURATION, "phrases", len(PHRASES), "b-roll", [(i, a, round(b - a, 2)) for i, a, b, _, _ in BROLL])
