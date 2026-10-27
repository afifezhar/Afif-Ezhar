# Style D spec

Canvas 1080×1920, 30 fps. Shared CSS: `video-edit/storyboard/assets/style-d.css` (copied into each project's `assets/`).

## Talking head

- Footage: retouched, then the HyperFrames `skin-soft` grade. A soft bottom fade (`.fade`) keeps captions on the dark shirt.
- Punch-in alternates 100% / 107% (origin 50% 30%) on every jump cut.

## Kold captions (talking head only)

- Reference: https://www.pinterest.com/pin/170362798400644982/
- One phrase at a time (up to 5 words), centred in x 64–900, bottom-anchored at y 1230 (`.kold { bottom: 690px }`), at chest level so the face stays clear.
- Each phrase mixes three faces:
  - `.ks`: Inter 800, 58 px, −0.045em tracking. The small lead-in and tail lines.
  - The emphasis word, one per phrase, cycles through:
    - `.kserif i`: Playfair Display italic, 132 px
    - `.kit`: Poppins ExtraBold Italic, 96 px
    - `.kserif`: Playfair Display roman, 132 px
    - `.kbig`: Inter 900, 104 px
  - Use `.kit` when the word is longer than 11 characters.
- Emphasis priority:
  - authenticity, authentic, perfect, real, trust, percaya, skip, show, tool, identity, sama, cantik, experiences, limitation, personaliti, kelebihan, better, generated, generate, valuable, bagus, diri, review, model, voice, powerful, sebenar, the year, AI.
  - Prefer a word after a short lead-in, unless it is one of the top three.
- White text, glow `0 0 24px rgba(255,255,255,.45)` plus a soft drop shadow. No boxes, no strokes.
- Lowercase, except AI, TikTok, place names, numbers. Spoken numbers become digits (tiga → 3).
- Motion: each word on its spoken time, fade with a 22 px rise and scale 0.94 → 1 over 0.16 s. The phrase clears 60 ms before the next one.
- Captions are hidden during b-roll; the b-roll text carries the words.

## Editorial b-roll (full screen; the voice continues)

- Reference: https://www.pinterest.com/pin/1119285313673132667/
- **Alternate canvases:**
  - Black (`.mg`): yellow headline, white eyebrow, soft grey spotlight behind objects.
  - White (`.mg.light`): black headline on a yellow marker band (`.mk`).
- Eyebrow: Poppins Italic 36 px, typed letter by letter across the spoken words.
- Headline: Poppins ExtraBold Italic, 150–230 px, line-height 0.84, −0.06em. Words slide in from −60 px on their spoken time. A secondary line uses `.mgmid` (96 px) or `.mgsmall` (40 px).
- Objects:
  - CC0 stock cut-outs in high-contrast black & white with drop shadows (from wordpress.org/photos), recorded in `assets/stock/SOURCES.md`.
  - Or pure motion graphics: TikTok feed card, "AI GENERATED" creator card with a waveform, a grid of identical faceless cards, person icons, a dot grid.
  - AI images are allowed (modest only).
  - Headline words may sit behind or in front of the object for depth.
- Entrances: objects `.rise` (from +260 px) or `.drop`. Icons and cards `.pop` (scale 0.6 → 1, back-out). Stats recolour on the spoken number.
- Transition in: a four-point star grows from the top-right corner to cover the frame (0.24 s, power3.in), then settles as a corner ornament. It is yellow going into black and black going into white. Add a whoosh SFX (0.5) and typing SFX (0.25) under the eyebrow. Cut back to the talking head without a transition.
- About one insert per idea, roughly 35–45% of the runtime.

## End card (after his full closing lines)

- Black canvas, star wipe in, 3.2 s.
- Content:
  - typed "jadi, korang"
  - a yellow two-line question
  - a white sub-line
  - three comment bubbles (avatar and grey bars, no invented text)
  - a yellow pill "Komen kat bawah ↓"
  - "Follow untuk tips content yang real."
- The music lifts to carry it, then fades over the last 1.6 s.

## Cover

- The real graded frame, full bleed, no cut-out.
- Soft top vignette plus a bottom fade.
- Kold-style stacked title at chest level, using the hook question. For example: "korang / *percaya ke* (Playfair italic 186) / **AI-generated** (Poppins ExtraBold Italic 118, yellow) / product review?".
- At most one small yellow spark. Minimal and polished.

## Audio

- Voice: −14 LUFS integrated, −1.5 dBTP.
- Music: lo-fi loop at 0.55 volume, lifted for the end card.
- Final mix: about −13 to −14 LUFS, peak below −1 dBFS.
