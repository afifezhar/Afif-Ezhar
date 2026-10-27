# Talking-head edit — working notes

Source: Google Drive folder `1yr56pDBWE4xn-pbbCp2xgzCjZVu2EonE` ("Content Video")

| Take | File | Length | Format |
| --- | --- | --- | --- |
| A | `VID_20261027_081227.mp4` | 2:11 | 1920×1080 stored, rotation 90° → plays 1080×1920, ~29.9 fps, AAC 48 kHz |
| B | `VID_20261027_081713.mp4` | 2:10 | same |

Both are selfie takes in a car, same script. Face sits in the upper third, black shirt.

## Transcripts

Whisper large-v3 (faster-whisper, int8, CPU), language `ms`, with timestamps for every word:
`transcripts/*.txt` (lines) and `transcripts/*.words.json` (words).

Whisper slips to fix in captions: "AI genetik" → "AI generated", "efresif" → "impressive",
"selipun" → "pun", "sure don't just generate" → "show, don't just generate".

## Take comparison

- **Take A** is cleaner and more fluent ("Show / Don't just generate" lands well, ending
  "They can actually trust"). It says "pada tahun ni".
- **Take B** names the year ("pada tahun 2026"), but has filler ("apa semua") and a weaker ending.
- Plan: build on Take A, and splice in lines from B only where they read better.

## Script beats (Take A timings)

1. Hook 0:01–0:09: "AI sekarang dah boleh buat video yang nampak real… orang masih percaya ke?"
2. Context 0:09–0:29: scroll TikTok, affiliate videos with AI models and voices, everything starts to look the same
3. Data 0:29–0:54: TikTok study, 3 of 4 APAC users skip over-polished or AI content; 9 of 10 say authentic content drives buying
4. Thesis 0:54–1:14: "Technology is getting better, but authenticity is becoming more valuable"; not anti-AI
5. Tips 1:14–1:52: (1) Show, don't just generate (2) Share real experiences (3) Use AI as a tool, not your entire identity
6. CTA 1:52–2:08: "Orang nak something they can actually trust… korang masih percaya ke dengan AI generated product review?"

## Toolchain

- HyperFrames `0.8.206` (`npx hyperframes`). Run `npx hyperframes browser ensure` once.
  Vendor GSAP locally if `cdn.jsdelivr.net` is not reachable.
- ElevenLabs (SFX, music, Scribe) reads `ELEVENLABS_API_KEY` from the environment.
- Output: 1080×1920. All text inside y 168–1330 px, and kept clear of the right-hand action rail.
