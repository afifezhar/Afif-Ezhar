"""Writes the three storyboard option compositions (6 style frames each) and index.html.

Run from video-edit/storyboard:  python3 build.py
Then grade with `hyperframes media-treatment` (see ../STORYBOARD.md) and snapshot.
"""

F = "../assets/frames/"


def plate(src, cls=""):
    return f'<img class="plate {cls}" src="{F}{src}" alt="" />'


# Each beat: (label, source time in Take A, scene HTML)
OPTIONS = {
    "a": [
        ("Hook", "35.0", plate("f_36_0.jpg", "zoom-110") + '<div class="shade"></div>'
         '<div class="ov cardA" style="top:800px"><div class="eyebrow">KAJIAN TIKTOK · ASIA PACIFIC 2026</div>'
         '<div class="num"><em>3</em> dari <em>4</em></div><div class="body">orang skip content yang nampak terlalu polished atau AI</div></div>'
         '<div class="ov capA">3 daripada 4 pengguna <span class="k">skip</span></div>'),
        ("Context", "16.3", plate("f_20_0.jpg") + '<div class="shade"></div>'
         '<div class="ov chipsA"><span>Affiliate</span><span>Product review</span><span class="on">AI model · AI voice</span></div>'
         '<div class="ov capA">Ada yang guna <span class="k">AI model</span>, AI voice</div>'),
        ("Data", "44.2", plate("f_47_0.jpg") + '<div class="shade"></div>'
         '<div class="ov cardA" style="top:800px"><div class="eyebrow">KAJIAN TIKTOK 2026</div>'
         '<div class="num"><em>9</em> dari <em>10</em></div><div class="body">kata authentic content pengaruh keputusan beli</div></div>'
         '<div class="ov capA"><span class="k">Authentic content</span> mempengaruhi keputusan</div>'),
        ("Thesis", "54.9", plate("f_58_0.jpg", "zoom-110") + '<div class="shade"></div>'
         '<div class="ov quoteA"><span class="small">Technology is getting better.</span>But <span class="k">authenticity</span> is becoming more valuable.</div>'
         '<div class="ov capA">But <span class="k">authenticity</span> is becoming more valuable</div>'),
        ("Tips", "83.6", plate("f_85_0.jpg") + '<div class="shade"></div>'
         '<div class="ov trackerA">3 TIPS &nbsp;<b>●</b> ○ ○</div>'
         '<div class="ov cardA" style="top:820px"><div class="eyebrow">TIP 01</div><div class="body" style="font-size:56px">Show, don\'t just generate</div></div>'
         '<div class="ov capA">First, <span class="k">show</span>. Don\'t just generate</div>'),
        ("CTA", "122.2", plate("f_125_0.jpg", "zoom-110") + '<div class="shade"></div>'
         '<div class="ov titleA" style="top:820px">Korang masih<br><span class="k">percaya ke?</span></div>'
         '<div class="ov capA">Komen kat bawah ↓</div>'),
    ],
    "b": [
        ("Hook", "71.2", plate("f_72_3.jpg", "zoom-118") + '<div class="shade"></div>'
         '<div class="ov hugeB" style="top:760px;font-size:150px">Video perfect<br><span class="k">dah tak laku.</span></div>'
         '<div class="ov capB" style="font-size:88px">Bukan lagi <span class="k">kelebihan</span></div>'),
        ("Context", "9.7", plate("f_20_0.jpg", "zoom-110") + '<div class="blurband"></div><div class="shade"></div>'
         '<div class="ov stampB" style="left:90px;top:820px;font-size:110px">AI model</div>'
         '<div class="ov stampB y" style="left:380px;top:980px;font-size:90px;transform:rotate(4deg)">AI voice</div>'
         '<div class="ov capB">Sama <span class="k">je</span></div>'),
        ("Data", "35.0", plate("f_36_0.jpg", "zoom-118") + '<div class="flash"></div><div class="shade"></div>'
         '<div class="ov hugeB k" style="top:720px;font-size:300px">3/4</div>'
         '<div class="ov stampB" style="left:500px;top:820px;font-size:120px">Skip!</div>'
         '<div class="ov capB">Terus <span class="k">skip</span></div>'),
        ("Thesis", "54.9", plate("f_58_0.jpg") + '<div class="shade"></div>'
         '<div class="ov hugeB" style="top:780px;font-size:96px">Technology <span class="arrowB">↑</span><br><span class="k">Authenticity <span class="arrowB">↑↑</span></span></div>'
         '<div class="ov capB">More <span class="k">valuable</span></div>'),
        ("Tips", "83.6", plate("f_85_0.jpg", "zoom-118") + '<div class="shade"></div>'
         '<div class="ov hugeB k" style="top:740px;font-size:260px">#1</div>'
         '<div class="ov hugeB" style="top:990px;font-size:130px;left:64px">Show.</div>'
         '<div class="ov capB" style="font-size:84px">Don\'t just <span class="k">generate</span></div>'),
        ("CTA", "122.2", plate("f_125_0.jpg", "zoom-110") + '<div class="shade"></div>'
         '<div class="ov hugeB" style="top:800px;font-size:130px">Korang<br><span class="k">percaya ke?</span></div>'
         '<div class="ov capB" style="font-size:84px">Komen <span class="k">↓</span></div>'),
    ],
    "c": [
        ("Hook", "1.7", plate("f_3_0.jpg") + plate("f_3_0_ai.jpg", "ai") + '<div class="shade"></div>'
         '<div class="ov tagC ai" style="left:700px;top:250px">AI?</div>'
         '<div class="ov headC" style="top:800px;font-size:150px">Ini real<br><span class="k">atau AI?</span></div>'
         '<div class="ov capC"><span>AI sekarang dah boleh buat video yang nampak <em>real</em></span></div>'),
        ("Context", "16.3", plate("f_20_0.jpg") + plate("f_20_0_ai.jpg", "ai split-r") + '<div class="seam"></div><div class="shade"></div>'
         '<div class="ov tagC real" style="left:64px;top:250px">REAL</div><div class="ov tagC ai" style="left:610px;top:250px">AI</div>'
         '<div class="ov capC"><span>Ada yang guna <em>AI model</em>, <em>AI voice</em></span></div>'),
        ("Data", "35.0", plate("f_36_0.jpg") + '<div class="shade"></div>'
         '<div class="ov termC"><span class="dim">$ tiktok-study --region apac</span><br>&gt; 3/4 skip polished / AI content<br>&gt; 9/10 trust authentic content<br><span class="dim">&gt; src: TikTok 2026</span></div>'
         '<div class="ov capC"><span>3 daripada 4 pengguna <em>skip</em></span></div>'),
        ("Thesis", "56.8", plate("f_58_0.jpg") + plate("f_58_0_ai.jpg", "ai split-r") + '<div class="seam"></div><div class="shade"></div>'
         '<div class="ov headC" style="top:800px;font-size:110px">Technology ↑<br><span class="k">Authenticity ↑↑</span></div>'
         '<div class="ov capC"><span>But <em>authenticity</em> is becoming more valuable</span></div>'),
        ("Tips", "83.6", plate("f_85_0.jpg") + '<div class="shade"></div>'
         '<div class="ov termC" style="top:820px;font-size:46px"><span class="dim">// tip 01</span><br>SHOW, don\'t just generate<span class="dim">_</span></div>'
         '<div class="ov capC"><span>Tunjuk <em>produk sebenar</em> tu sendiri</span></div>'),
        ("CTA", "122.2", plate("f_125_0.jpg") + '<div class="shade"></div>'
         '<div class="ov headC" style="top:820px;font-size:130px">Korang masih<br><span class="k">percaya?</span></div>'
         '<div class="ov capC"><span>Dengan AI generated product review ni?</span></div>'),
    ],
}

NAMES = {"a": "Editorial Clean", "b": "Fast TikTok Native", "c": "Real vs AI"}

for key, beats in OPTIONS.items():
    scenes = "\n".join(
        f'      <!-- {i + 1}. {label} (Take A {t}s) -->\n'
        f'      <section id="{key}{i + 1}" class="scene clip" data-start="{i}" data-duration="1" data-beat="{label}">{html}</section>'
        for i, (label, t, html) in enumerate(beats)
    )
    doc = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="../assets/sb.css" />
  </head>
  <body>
    <!-- Option {key.upper()}: {NAMES[key]} — one style frame per beat -->
    <div id="root" data-composition-id="option-{key}" data-start="0" data-duration="{len(beats)}" data-width="1080" data-height="1920">
{scenes}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["option-{key}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(f"compositions/option-{key}.html", "w").write(doc)

mounts = "\n".join(
    f'      <div id="option-{k}" class="clip" data-composition-id="option-{k}" data-composition-src="compositions/option-{k}.html" '
    f'data-start="{i * 6}" data-duration="6" data-track-index="0"></div>'
    for i, k in enumerate(OPTIONS)
)
open("index.html", "w").write(f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/sb.css" />
  </head>
  <body>
    <!-- Storyboard style frames: option A 0-6s, B 6-12s, C 12-18s, one beat per second -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="18" data-width="1080" data-height="1920">
{mounts}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""")
