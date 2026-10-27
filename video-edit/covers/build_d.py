"""Writes the three Style D cover options (compositions/cover-d1..3.html) for hook H4
("Korang sendiri masih percaya ke dengan AI generated product review ni?") and mounts them in index.html at 4-7 s.

Run from video-edit/covers:  python3 build_d.py   (then grade img.plate / .photo img with skin-soft)
"""
import re

FRAME = "../assets/frames/A_8_2.jpg"
STAR = ('<svg class="star" viewBox="0 0 100 100" style="{pos}"><path '
        'd="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z"/></svg>')

LOCAL = """
.c-fade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.55) 62%, rgba(0,0,0,0.85) 100%); }
.cover-kold { bottom: 640px; }
.cover-kold .ks { font-size: 78px; }
.cover-kold .kserif { font-size: 240px; line-height: 0.8; }
.cover-kold .kit { font-size: 132px; color: var(--accent); }
.panel { position: absolute; left: 0; right: 0; top: 1000px; bottom: 0; background: linear-gradient(180deg, rgba(11,11,11,0) 0, #0b0b0b 90px); }
.half { position: absolute; left: 0; top: 0; width: 1080px; height: 1100px; }
.photo { position: absolute; z-index: 2; padding: 18px 18px 70px; background: #fff; box-shadow: 24px 34px 60px rgba(0,0,0,0.25); }
.photo img { display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; }
.real { position: absolute; z-index: 3; font: 800 34px/1 "Inter", sans-serif; letter-spacing: 0.04em; color: #111; background: var(--accent); padding: 14px 20px; border-radius: 10px; transform: rotate(6deg); }
"""

COVERS = {
    "d1": ("Talking head + Kold caption",
           f'<img class="plate" src="{FRAME}" alt="" /><div class="c-fade"></div>'
           '<div class="ov kold cover-kold"><div class="ks">korang masih</div><div class="kserif i">percaya</div>'
           '<div class="kit">AI review?</div></div>'),
    "d2": ("Face on top, black b-roll panel",
           '<img class="plate half" src="../assets/frames/A_8_2_top.jpg" alt="" /><div class="panel"></div>'
           + STAR.format(pos="right:-170px;top:1000px;width:420px;height:420px")
           + '<div class="ov eyebrow" style="top:1010px;color:#fff">AI generated product review,</div>'
           + '<div class="ov mgbig" style="top:1060px;font-size:118px">korang masih<br>percaya?</div>'),
    "d3": ("White canvas, real photo + yellow marker",
           '<div class="mg light">'
           + STAR.format(pos="right:-150px;top:-170px")
           + '<div class="ov eyebrow" style="top:250px">AI generated product review,</div>'
           + f'<div class="photo" style="left:200px;top:330px;width:620px;height:740px;transform:rotate(-4deg)"><img src="../assets/frames/A_8_2_photo.jpg" alt="" /></div>'
           + '<div class="real" style="left:650px;top:360px">100% REAL</div>'
           + '<div class="ov mgbig" style="top:1080px;font-size:124px;z-index:3"><span class="mk">korang masih</span><br><span class="mk">percaya?</span></div>'
           + '</div>'),
}

for key, (label, body) in COVERS.items():
    open(f"compositions/cover-{key}.html", "w").write(f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="../assets/style-d.css" />
    <style>{LOCAL}</style>
  </head>
  <body>
    <!-- Style D cover {key.upper()}: {label} (hook H4) -->
    <div id="root" data-composition-id="cover-{key}" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <section id="c{key}" class="scene">{body}</section>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["cover-{key}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")

idx = open("index.html").read()
idx = re.sub(r'\n\s*<!-- Style D cover[^\n]*\n\s*<div id="cover-d[^\n]*', "", idx)
mounts = "".join(
    f'\n      <!-- Style D cover {k.upper()} -->\n      <div id="cover-{k}" class="clip" data-composition-id="cover-{k}" '
    f'data-composition-src="compositions/cover-{k}.html" data-start="{4 + i}" data-duration="1" data-track-index="0"></div>'
    for i, k in enumerate(COVERS)
)
idx = idx.replace("\n    </div>\n    <script>", mounts + "\n    </div>\n    <script>", 1)
idx = re.sub(r'(data-composition-id="main" data-start="0" data-duration=")\d+(")', rf"\g<1>{4 + len(COVERS)}\2", idx)
open("index.html", "w").write(idx)
