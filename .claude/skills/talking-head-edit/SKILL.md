---
name: talking-head-edit
description: Afif's house process and style for editing his talking-head social media videos (TikTok / Reels / Shorts, 1080x1920, usually Malay with English mixed in) with HyperFrames + ElevenLabs. Use whenever he asks to edit, storyboard, caption, add b-roll to, or make a cover for a talking-head / selfie video, or says "edit video", "talking head", "buat edit macam biasa", or drops new takes into video-edit/. Covers footage prep, voice clean-up, word-accurate cutting, Kold-style captions, editorial b-roll, outro, cover and QA.
---

# Talking-head edit: Afif's process and style

The reference implementation is the "Orang masih percaya ke?" edit in `video-edit/`. Copy its pieces rather than
starting from scratch: `video-edit/edit/` (edl.py, prep.py, build.py), `video-edit/scripts/`,
`video-edit/storyboard/assets/style-d.css`, `video-edit/covers/build_d.py`. The full design spec is in
[style.md](style.md); read it before writing captions, b-roll or a cover.

Talk to Afif in Malay (casual, "korang/aku" register is fine), keep code and commits in English.

## His standing preferences (from his feedback; do not regress these)

- **Style D** is the house style: Kold-style captions on the talking head + full-screen editorial motion-graphic b-roll.
- **Accent is yellow `#ffd60a`**, never red or maroon.
- **B-roll canvases alternate white and black.** Never all black.
- **B-roll content:** CC0 stock cut-outs, pure motion graphics, and AI-generated images are all fine.
  - **Never cut Afif out of his footage for b-roll.**
  - **Never use sexy or revealing imagery** (no cleavage, no tank tops). Keep people fully clothed and modest, or show no people at all.
- **Cover:** minimalist and polished. Use the real graded frame with **no background removal**. Add a Kold-style title and at most one small accent, such as a yellow spark.
  - No sticker or icon collages.
  - Keep his face at the natural frame size; don't push in.
  - Cover text is usually the hook question.
- **Grade:** HyperFrames preset `skin-soft` on top of the light retouch.
- **Voice:** run it through clarity processing every time.
- **Pacing:**
  - Remove awkward pauses and repeated or filler words.
  - Speed up slightly (1.06x) if the edit drags.
  - About 90 s is a guideline, not a hard target. Never cut meaning to hit a number.
- **Hook:**
  - A strong line from his own words, as a cold open, with the text on screen from frame 0.
  - He picks it from options. Last time he chose the closing question.
- **Ending must not hang.**
  - Keep his full closing lines. **Do not cut anything he says after "So aku curious"** or a similar sign-off.
  - Then a short end card: the question, comment bubbles, a "Komen kat bawah ↓" pill and a follow line.
- **Background music:**
  - Clearly audible under the voice: about 0.55 volume on the quiet lo-fi loop, roughly 20–23 dB under speech.
  - Lifted for the end card.
- **Always show visuals before the full edit:** storyboard board, style frames and a short motion test. He decides from pictures, not descriptions.

## Process

Raw takes come from his Google Drive "Content Video" folder. Download them with `gdown --folder <url>`; they are public.
Big media stays out of git, in the scratchpad or `/tmp`.

1. **Notes and transcripts.**
   - Read `video-edit/NOTES.md` if it exists.
   - Compare the takes, pick a base take, and splice better lines from other takes (for example, the one that names the year).
2. **Retouch:** `scripts/retouch.sh <in.mp4> <out.mp4>`.
   - This is a denoise plus 45% bilateral skin smoothing; the mole and pores stay.
   - Then convert to constant 30 fps: `ffmpeg -i in -vf fps=30 -an -c:v libx264 -crf 14 out`. Frame-aligned cuts on a variable-frame-rate phone file drift out of sync.
3. **Voice:** `scripts/voice.sh <take.mp4> <take_voice.wav>`.
   - ElevenLabs Voice Isolator, then EQ, de-ess and 3:1 compression.
   - Two-pass loudnorm to −14 LUFS, with a −1.5 dBTP limiter.
4. **Word times:** `scripts/transcribe.sh <take_voice.wav> transcripts <TakeName>` writes three files:
   - Scribe word times
   - a silence map
   - a 10 ms loudness envelope

   **Cut on Scribe times, not Whisper.** Whisper drifted up to 0.8 s here.
5. **Storyboard first.**
   - Hook options (word-timed, from his own lines) and the beat list, written into `STORYBOARD.md`.
   - Style frames rendered in HyperFrames, then a labelled board (`storyboard/build_d.py`, `boards.py`).
   - Send him the board and wait for his pick.
6. **Motion test.** Render about 12 s (hook, opening line, one star wipe, one b-roll) with the real voice and music (`motion-test/build.py`). Send it.
7. **Edit list** (`edit/edl.py`):
   - `SPANS` are the kept sentences in output order (the hook first). `DROPS` are repeated or filler words.
   - Pauses over 0.22 s become 0.12 s. Every cut lands in measured silence, or failing that in the quietest stretch.
   - A drop is kept only if both of its cut points are below −32 dB. Words said in one breath stay in.
   - `SPEED = 1.06`.
8. **Media:** `edit/prep.py` cuts the base video and voice, then builds the music loop with crossfades and the end-card lift.
   - ElevenLabs Music needs a paid plan. On the free plan, generate a 22 s seamless loop with the Sound Effects API (`loop: true`) and chain it.
   - Whoosh and typing sound effects also come from the Sound Effects API.
9. **Composition:** `edit/build.py` writes `index.html`.
   - Captions are auto-grouped into phrases, with one emphasis word chosen by priority.
   - Plan b-roll from the script: one insert per idea, alternating canvases, words timed to speech.
   - Add the star wipes, the end card, and a 100%/107% punch-in on every jump cut.
   - Grade the base video with `npx hyperframes media-treatment --selector "#base" --grading '{"preset":"skin-soft","intensity":1}' --apply`.
10. **QA before rendering** (all must pass):
    - `npx hyperframes lint`: 0 errors. Warnings about the Studio timeline are fine.
    - `node scripts/check-safe-zone.mjs <dirs>` (`NODE_PATH=$(npm root -g)`).
    - `python3 scripts/check_cuts.py edit A=... B=...`: 0 cut points in speech.
    - Picture and voice durations equal to within 1 frame.
    - Snapshot about 20 moments with `npx hyperframes snapshot --at ...` and look at them: no orphan caption words, nothing covering the face, b-roll text readable.
11. **Render:** `npx hyperframes render -o renders/final.mp4 -f 30`.
    - It takes about 17 s per second of video (about 25 min for 90 s), so run it in the background.
    - Check loudness (target −14 LUFS, peak below −1 dBFS) and the music level on the end card.
    - Music can be remixed onto a finished render with ffmpeg `amix` without re-rendering.
12. **Deliver:**
    - Compress with `-crf 20` into `video-edit/final/` and send it with SendUserFile, plus the cover JPG.
    - MP4s are gitignored; commit the code and push.
    - Say plainly what was verified, and that the audio still needs his ears: the container can't play sound.

## Gotchas found the hard way

- HyperFrames media treatments render `<img>` and `<video>` through their own pipeline. `object-position` is ignored and translucent PNG mattes look boxed. Pre-crop frames with ffmpeg instead.
- Sub-compositions must use `id="root"` and must not style their root by class. Mount them with `data-composition-src`; that is a lint error otherwise.
- Separate projects (covers, storyboard, motion test, edit) each need their own folder: one root `index.html` per project.
- Class names clash across shared CSS. The cover project's `.hl` broke the yellow marker, which is now `.mk`.
- Inline caption spans measure taller than their line box. Bottom-anchor captions with headroom, and let the safe-zone checker decide.
- Canva `generate-image` only returns a 450 px preview. Full resolution needs a saved Canva design and export, so **ask Afif first**: he declined once. Weave (Figma) needs his Figma account linked.
- The safe zone is x 64–900, y 220–1330 (`video-edit/safe-zone.json`). Cover headlines must also fit the 3:4 grid crop, y 240–1680.
