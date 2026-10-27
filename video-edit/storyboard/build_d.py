"""Writes compositions/style-d.html: 12 style frames for Style D
(Kold-style captions on the talking head + white editorial motion-graphic b-roll with CC0 stock).

Run from video-edit/storyboard:  python3 build_d.py
"""

F = "../assets/frames/"
S = "../assets/stock/"
STAR = ('<svg class="star" viewBox="0 0 100 100" style="{pos}"><path fill="#0b0b0b" '
        'd="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z"/></svg>')


def th(src, kold, zoom=""):
    """Talking-head frame with a Kold caption block."""
    return f'<img class="plate {zoom}" src="{F}{src}" alt="" /><div class="fade"></div><div class="ov kold">{kold}</div>'


def stock(name, style):
    return f'<img class="stock" src="{S}{name}.png" alt="" style="{style}" />'


# (beat, Take A time, kind, html)
FRAMES = [
    ("1 HOOK", "71.2", "TH", th("f_72_3.jpg", '<div class="ks">Video yang</div><div class="kserif">perfect</div>', "zoom-110")),
    ("2 OPEN", "3.6", "TH", th("f_3_0.jpg", '<div class="ks">buat video yang</div><div class="kit">nampak real,</div>')),
    ("3 B-ROLL", "6.1", "MG", '<div class="mg">'
     + STAR.format(pos="right:-150px;top:-170px")
     + '<div class="ov eyebrow" style="top:250px">Tapi persoalannya,</div>'
     + '<div class="ov mgbig" style="top:310px">orang<br>masih</div>'
     + stock("statue", "left:330px;top:560px;height:1240px")
     + '<div class="ov mgbig" style="top:1000px;z-index:3">percaya<br>ke?</div></div>'),
    ("4 B-ROLL", "16.3", "MG", '<div class="mg">'
     + '<div class="ov eyebrow" style="top:250px">Ada yang guna</div>'
     + '<div class="ov mgbig" style="top:300px">AI model,</div>'
     + stock("mannequin", "left:90px;top:540px;height:620px")
     + stock("mic", "left:470px;top:700px;height:400px")
     + '<div class="ov mgmid" style="top:1170px;z-index:3">AI voice.</div>'
     + '<div class="ov barcode" style="left:600px;top:1240px"></div></div>'),
    ("5 TALK", "27.0", "TH", th("f_20_0.jpg", '<div class="ks">lama-lama semuanya nampak</div><div class="kserif i">sama je.</div>')),
    ("6 B-ROLL", "35.0", "MG", '<div class="mg">'
     + STAR.format(pos="left:-200px;bottom:-200px")
     + '<div class="ov eyebrow" style="top:250px">Menurut kajian TikTok 2026,</div>'
     + '<div class="ov mgbig" style="top:300px;font-size:210px">3 dari 4</div>'
     + stock("phone", "left:120px;top:560px;width:900px")
     + '<div class="ov mgmid" style="top:1180px;z-index:3;text-align:right">skip.</div>'
     + '<div class="ov swipe" style="left:640px;top:880px">↑</div></div>'),
    ("7 B-ROLL", "44.2", "MG", '<div class="mg dark">'
     + '<div class="glow" style="left:-120px;top:1100px;width:700px;height:500px"></div>'
     + '<div class="glow" style="right:-160px;top:200px;width:520px;height:420px"></div>'
     + '<div class="ov eyebrow center" style="top:330px">dan 9 daripada 10 kata</div>'
     + '<div class="ov mgbig center" style="top:400px;font-size:150px">authentic</div>'
     + '<div class="ov mgsmall center" style="top:560px">content pengaruh keputusan untuk membeli</div>'
     + stock("bags", "left:150px;top:720px;width:760px;filter:drop-shadow(0 0 40px rgba(224,56,77,0.35))") + '</div>'),
    ("8 THESIS", "56.8", "TH", th("f_58_0.jpg", '<div class="ks">but</div><div class="kserif">authenticity</div><div class="ks">is becoming more valuable.</div>', "zoom-110")),
    ("9 B-ROLL", "83.6", "MG", '<div class="mg">'
     + STAR.format(pos="right:-150px;top:-170px")
     + '<div class="ov eyebrow" style="top:250px">First,</div>'
     + '<div class="ov mgbig" style="top:300px;font-size:230px">show,</div>'
     + stock("record", "left:-60px;top:660px;width:1100px")
     + '<div class="ov mgsmall" style="top:520px;font-size:44px">don\'t just generate.</div></div>'),
    ("10 TALK", "91.4", "TH", th("f_47_0.jpg", '<div class="ks">second,</div><div class="kit">share real</div><div class="kserif i">experiences.</div>')),
    ("11 B-ROLL", "100.2", "MG", '<div class="mg">'
     + stock("claw", "left:470px;top:-120px;height:1180px")
     + '<div class="ov eyebrow" style="top:760px">Third, use AI as a</div>'
     + '<div class="ov mgbig" style="top:820px;font-size:220px;z-index:3">tool,</div>'
     + '<div class="ov mgmid" style="top:1030px;color:var(--blush)">not your</div>'
     + '<div class="ov mgmid" style="top:1116px">identity.</div>'
     + '<div class="ov barcode" style="left:64px;top:1250px;width:220px;height:48px"></div></div>'),
    ("12 CTA", "122.2", "TH", th("f_125_0.jpg", '<div class="ks">korang masih</div><div class="kserif i">percaya ke?</div>', "zoom-110")),
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
    <!-- Style D: Kold captions on talking head + editorial motion-graphic b-roll (CC0 stock). One frame per second. -->
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
