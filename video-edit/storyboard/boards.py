"""Lays the 18 snapshot frames out as one labelled board per option (out/option-*.jpg).

Run from video-edit/storyboard after a snapshot:
  options A-C: snapshot --at 0.5,1.5,...,17.5  ->  python3 boards.py <snapdir> abc
  style D:     snapshot --at 18.5,...,29.5     ->  python3 boards.py <snapdir> d
"""
import glob
import subprocess
import sys

FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
BEATS = ["1 HOOK", "2 CONTEXT", "3 DATA", "4 THESIS", "5 TIPS", "6 CTA"]
TITLES = {"a": "OPTION A  -  EDITORIAL CLEAN", "b": "OPTION B  -  FAST TIKTOK NATIVE", "c": "OPTION C  -  REAL vs AI"}
NOTES = {
    "a": ["Cold open: stat 3 dari 4 (A 35.0s)", "Chips: affiliate / review / AI", "Stat card 9 dari 10",
          "Quote card + punch-in 110%", "Tracker 3 TIPS + tip card", "Question + komen"],
    "b": ["Cold open: Video perfect dah tak laku", "Scroll swipe + AI stamps", "Zoom 118% + red flash on 3/4",
          "Typewriter arrows", "#1 number slam", "Push-in, silent ending"],
    "c": ["Cold open: glitch, Ini real atau AI?", "Split real / AI", "Terminal stat readout",
          "Seam wipe glitch to clean", "Terminal tip card", "Clean, final question"],
}


def esc(s):
    return s.replace(":", "\\:").replace("'", "’")


def boards_abc(snapdir):
    frames = sorted(glob.glob(f"{snapdir}/frame-*.png"))
    for oi, k in enumerate("abc"):
        ins, flt = [], []
        for j in range(6):
            ins += ["-i", frames[oi * 6 + j]]
            flt.append(
                f"[{j}]scale=360:640,pad=380:740:10:60:color=0x111111,"
                f"drawtext=fontfile={FB}:text='{esc(BEATS[j])}':x=12:y=14:fontsize=22:fontcolor=0xFFD60A:expansion=none,"
                f"drawtext=fontfile={FR}:text='{esc(NOTES[k][j])}':x=12:y=706:fontsize=15:fontcolor=white:expansion=none[v{j}]"
            )
        flt.append(
            "".join(f"[v{j}]" for j in range(6))
            + f"hstack=6,pad=iw:ih+70:0:70:color=0x111111,"
            f"drawtext=fontfile={FB}:text='{esc(TITLES[k])}':x=14:y=22:fontsize=32:fontcolor=white:expansion=none[out]"
        )
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(flt),
                        "-map", "[out]", "-q:v", "3", f"out/option-{k}.jpg"], check=True)


def board_d(snapdir):
    """Style D: 12 frames (snapshot at 18.5..29.5) in two rows, labels from labels-d.txt."""
    labels = [line.split("|") for line in open("labels-d.txt").read().splitlines()]
    frames = sorted(glob.glob(f"{snapdir}/frame-*.png"))
    ins, flt = [], []
    for j, (beat, note) in enumerate(labels):
        ins += ["-i", frames[j]]
        colour = "0xE9B9C1" if "MG" in note else "0xFFFFFF"
        flt.append(
            f"[{j}]scale=360:640,pad=380:740:10:60:color=0x111111,"
            f"drawtext=fontfile={FB}:text='{esc(beat)}':x=12:y=14:fontsize=22:fontcolor={colour}:expansion=none,"
            f"drawtext=fontfile={FR}:text='{esc(note.replace('TH', 'Talking head + Kold caption').replace('MG', 'Motion-graphic b-roll'))}':x=12:y=706:fontsize=15:fontcolor=white:expansion=none[v{j}]"
        )
    flt.append("".join(f"[v{j}]" for j in range(6)) + "hstack=6[r1]")
    flt.append("".join(f"[v{j}]" for j in range(6, 12)) + "hstack=6[r2]")
    flt.append("[r1][r2]vstack,pad=iw:ih+70:0:70:color=0x111111,"
               f"drawtext=fontfile={FB}:text='{esc('STYLE D  -  KOLD CAPTIONS + EDITORIAL MOTION-GRAPHIC B-ROLL')}':x=14:y=22:fontsize=32:fontcolor=white:expansion=none[out]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(flt),
                    "-map", "[out]", "-q:v", "3", "out/style-d.jpg"], check=True)


if __name__ == "__main__":
    (board_d if sys.argv[2] == "d" else boards_abc)(sys.argv[1])
