"""Cuts the media for the full edit into assets/media/ (not in git; rebuild from the source takes).

Usage (from video-edit/edit):
  python3 prep.py <A_cfr30.mp4> <B_original.mp4> <A_voice.wav> <B_voice.wav> <music_loop.mp3> <whoosh.mp3> <type.mp3>

A_retouched.mp4 comes from ../scripts/retouch.sh, converted to constant 30 fps
(ffmpeg -i A_retouched.mp4 -vf fps=30 -an -c:v libx264 -crf 14 A_cfr30.mp4) so frame-aligned cuts keep sync;
the voices come from ../scripts/voice.sh.
"""
import os
import subprocess
import sys

from edl import DURATION, SEGMENTS

a_vid, b_src, a_voice, b_voice, loop, whoosh, typing = sys.argv[1:8]
OUT = "assets/media"
os.makedirs(OUT, exist_ok=True)
RETOUCH = "hqdn3d=2:1.5:4:3,split[a][b];[b]bilateral=sigmaS=6:sigmaR=0.08[s];[a][s]blend=all_mode=normal:all_opacity=0.45,unsharp=5:5:0.35"


def run(args):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], check=True)


# Take B is only used for the splice, so retouch just that stretch.
B_OFF = 31.5
run(["-ss", str(B_OFF), "-t", "5", "-i", b_src, "-filter_complex", RETOUCH + ",fps=30", "-an",
     "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", f"{OUT}/b_seg.mp4"])

# Picture: every segment trimmed from its take, joined, constant 30 fps.
vparts, aparts = [], []
for i, (take, a, b) in enumerate(SEGMENTS):
    src, off = (0, 0.0) if take == "A" else (1, B_OFF)
    vparts.append(f"[{src}:v]trim=start={a - off:.3f}:end={b - off:.3f},setpts=PTS-STARTPTS,fps=30[v{i}]")
    asrc = 2 if take == "A" else 3
    d = b - a
    aparts.append(f"[{asrc}:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.012,afade=t=out:st={max(d - 0.012, 0):.3f}:d=0.012[a{i}]")
n = len(SEGMENTS)
graph = ";".join(vparts + aparts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v];" \
        + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
run(["-i", a_vid, "-i", f"{OUT}/b_seg.mp4", "-i", a_voice, "-i", b_voice, "-filter_complex", graph,
     "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
     f"{OUT}/base.mp4",
     "-map", "[a]", "-c:a", "aac", "-b:a", "256k", f"{OUT}/voice.m4a"])

# Music: the 22 s loop chained with 1.5 s crossfades past the edit length, faded out at the end.
copies = int(DURATION // 20) + 2
chain, last = [], "[0]"
for i in range(1, copies):
    chain.append(f"{last}[{i}]acrossfade=d=1.5:c1=tri:c2=tri[m{i}]")
    last = f"[m{i}]"
chain.append(f"{last}atrim=0:{DURATION + 0.5:.2f},afade=t=in:d=0.5,afade=t=out:st={DURATION - 2.5:.2f}:d=2.5[m]")
run([x for _ in range(copies) for x in ("-i", loop)] + ["-filter_complex", ";".join(chain), "-map", "[m]",
    "-c:a", "aac", "-b:a", "192k", f"{OUT}/music.m4a"])

for src, name in ((whoosh, "whoosh.mp3"), (typing, "type.mp3")):
    run(["-i", src, "-c", "copy", f"{OUT}/{name}"])
print("duration", DURATION)
