"""Writes compositions/style-d.html: 14 style frames for Style D
(Kold-style captions on the talking head + editorial b-roll that alternates white and black canvases,
mixing CC0 stock cut-outs with pure motion graphics; yellow accent).

Run from video-edit/storyboard:  python3 build_d.py
"""
import re

F = "../assets/frames/"
S = "../assets/stock/"
STAR = ('<svg class="star" viewBox="0 0 100 100" style="{pos}"><path '
        'd="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z"/></svg>')
PERSON = ('<svg class="{cls}" viewBox="0 0 100 140"><circle cx="50" cy="34" r="24"/>'
          '<path d="M8 140 C8 96 28 74 50 74 C72 74 92 96 92 140 Z"/></svg>')


def th(src, kold, zoom=""):
    """Talking-head frame with a Kold caption block."""
    return f'<img class="plate {zoom}" src="{F}{src}" alt="" /><div class="fade"></div><div class="ov kold">{kold}</div>'


def stock(name, style):
    return f'<img class="stock" src="{S}{name}.png" alt="" style="{style}" />'


def mg(theme, inner):
    """theme: 'dark' = yellow on black, 'light' = black on white with yellow marker on headline words."""
    if theme == "light":
        inner = re.sub(r'(<div class="ov (?:mgbig|mgmid)[^"]*"[^>]*>)(.*?)(</div>)',
                       lambda m: m.group(1) + re.sub(r'([^<>]+)(?=<br>|$)', r'<span class="mk">\1</span>', m.group(2)) + m.group(3),
                       inner)
        return f'<div class="mg light">{inner}</div>'
    return f'<div class="mg">{inner}</div>'


def feed_card(img, tag):
    return f'<div class="card"><img src="{S}{img}.png" alt="" /><span class="tag">{tag}</span></div>'


def ai_card(i):
    return (f'<div class="aicard"><svg viewBox="0 0 100 140"><circle cx="50" cy="34" r="24"/>'
            f'<path d="M8 140 C8 96 28 74 50 74 C72 74 92 96 92 140 Z"/></svg><i></i><i class="s"></i>'
            f'{"<b>AI</b>" if i in (0, 4, 8) else ""}</div>')


WAVE = "".join(f'<b style="height:{h}px"></b>' for h in (30, 70, 110, 60, 96, 120, 54, 88, 40, 104, 66, 28, 80, 112, 48))

# (beat, Take A time, kind, html)
FRAMES = [
    ("1 HOOK", "122.2", "TH", th("f_125_0.jpg", '<div class="ks">dengan</div><div class="kit">AI generated</div><div class="ks">product review ni?</div>', "zoom-110")),
    ("2 OPEN", "3.6", "TH", th("f_3_0.jpg", '<div class="ks">buat video yang</div><div class="kit">nampak real,</div>')),
    ("3 B-ROLL", "6.1", "MG dark · stock", mg("dark",
        STAR.format(pos="right:-150px;top:-170px")
        + '<div class="ov eyebrow" style="top:250px">Tapi persoalannya,</div>'
        + '<div class="ov mgbig" style="top:310px">orang<br>masih</div>'
        + stock("statue", "left:330px;top:560px;height:1240px")
        + '<div class="ov mgbig" style="top:950px;z-index:3">percaya<br>ke?</div>')),
    ("4 B-ROLL", "9.7", "MG light · pure MG", mg("light",
        '<div class="ov eyebrow" style="top:250px">Cuba korang scroll TikTok sekarang,</div>'
        + '<div class="feed" style="left:300px;top:330px;transform:rotate(-6deg) scale(0.8);transform-origin:50% 0">'
        + feed_card("bags", "#affiliate") + feed_card("mic", "#productreview") + '<div class="ui"><i></i><i></i><i></i></div></div>'
        + '<div class="ov mgmid" style="top:1110px;z-index:3">affiliate, review,<br>iklan.</div>')),
    ("5 B-ROLL", "16.3", "MG dark · pure MG", mg("dark",
        '<div class="ov eyebrow" style="top:250px">Ada yang guna</div>'
        + '<div class="ov mgbig" style="top:300px">AI model,</div>'
        + '<div class="aiphone" style="left:440px;top:470px;width:400px">' + ai_card(0) + '</div>'
        + '<div class="aibadge" style="left:380px;top:520px">AI GENERATED</div>'
        + f'<div class="wave" style="left:64px;top:1060px">{WAVE}</div>'
        + '<div class="ov mgmid" style="top:1190px;z-index:3">AI voice.</div>')),
    ("6 B-ROLL", "24.0", "MG light · pure MG", mg("light",
        '<div class="ov eyebrow" style="top:250px">Lama-lama semuanya nampak</div>'
        + '<div class="grid9" style="left:64px;top:320px;width:600px">' + "".join(ai_card(i) for i in range(9)) + '</div>'
        + '<div class="ov mgbig" style="top:1110px;z-index:3">sama je.</div>')),
    ("7 B-ROLL", "35.0", "MG light · pure MG", mg("light",
        STAR.format(pos="left:-200px;bottom:-200px")
        + '<div class="ov eyebrow" style="top:250px">Menurut kajian TikTok 2026,</div>'
        + '<div class="ov mgbig" style="top:300px;font-size:210px">3 dari 4</div>'
        + '<div class="people" style="left:90px;top:620px;width:780px">'
        + PERSON.format(cls="on") * 3 + PERSON.format(cls="off") + '</div>'
        + '<div class="ov mgmid" style="top:1080px">skip content</div>'
        + '<div class="ov mgsmall" style="top:1200px">yang nampak terlalu polished atau AI.</div>')),
    ("8 B-ROLL", "44.2", "MG dark · MG + stock", mg("dark",
        '<div class="glow" style="left:420px;top:820px;width:560px;height:380px;opacity:0.6"></div>'
        + '<div class="ov eyebrow" style="top:250px">dan 9 daripada 10 kata</div>'
        + '<div class="ov mgbig" style="top:300px;font-size:150px">authentic</div>'
        + '<div class="dots" style="left:90px;top:520px;width:500px">' + "<i></i>" * 9 + '<i class="off"></i></div>'
        + stock("bags", "left:420px;top:760px;width:560px")
        + '<div class="ov mgsmall" style="top:1230px">content pengaruh keputusan membeli.</div>')),
    ("9 THESIS", "56.8", "TH", th("f_58_0.jpg", '<div class="ks">but</div><div class="kserif">authenticity</div><div class="ks">is becoming more valuable.</div>', "zoom-110")),
    ("10 TALK", "60.0", "TH", th("f_47_0.jpg", '<div class="ks">tapi aku bukan nak cakap</div><div class="kserif i">jangan guna AI.</div>')),
    ("11 B-ROLL", "83.6", "MG light · stock", mg("light",
        STAR.format(pos="right:-150px;top:-170px")
        + '<div class="ov eyebrow" style="top:250px">First,</div>'
        + '<div class="ov mgbig" style="top:300px;font-size:230px">show,</div>'
        + '<div class="ov mgsmall" style="top:540px;font-size:44px">don\'t just generate.</div>'
        + stock("record", "left:-60px;top:660px;width:1100px"))),
    ("12 TALK", "91.4", "TH", th("f_85_0.jpg", '<div class="ks">second,</div><div class="kit">share real</div><div class="kserif i">experiences.</div>')),
    ("13 B-ROLL", "100.2", "MG dark · stock", mg("dark",
        stock("claw", "left:470px;top:-120px;height:1180px")
        + '<div class="ov eyebrow" style="top:760px">Third, use AI as a</div>'
        + '<div class="ov mgbig" style="top:820px;font-size:220px;z-index:3">tool,</div>'
        + '<div class="ov mgmid soft" style="top:1030px">not your</div>'
        + '<div class="ov mgmid" style="top:1116px">identity.</div>'
        + '<div class="ov barcode" style="left:64px;top:1250px;width:220px;height:48px"></div>')),
    ("14 CTA", "122.2", "TH", th("f_125_0.jpg", '<div class="ks">korang masih</div><div class="kserif i">percaya ke?</div>', "zoom-110")),
]

scenes = "\n".join(
    f'      <!-- {label} · {kind} · Take A {t}s -->\n'
    f'      <section id="d{i + 1}" class="scene clip" data-start="{i}" data-duration="1">{html}</section>'
    for i, (label, t, kind, html) in enumerate(FRAMES)
)
open("compositions/style-d.html", "w").write(f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="../assets/style-d.css" />
  </head>
  <body>
    <!-- Style D: Kold captions on talking head + editorial b-roll (white/black, stock + pure motion graphics). One frame per second. -->
    <div id="root" data-composition-id="style-d" data-start="0" data-duration="{len(FRAMES)}" data-width="1080" data-height="1920">
{scenes}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["style-d"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
open("labels-d.txt", "w").write("\n".join(f"{l}|{k} · A {t}s" for l, t, k, _ in FRAMES) + "\n")
