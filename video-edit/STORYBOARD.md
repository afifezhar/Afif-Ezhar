# Storyboard options — "Orang masih percaya ke?"

Base: **Take A** (`VID_20261027_081227.mp4`), 1080×1920. Timings below are Take A source times.
Pick **one storyboard (A / B / C)**, **one hook (H1 / H2 / H3)** and **one cover (1–4)**, and I'll build the full HyperFrames edit.

**Visual boards** (HyperFrames style frames from the retouched, graded footage, one frame per beat):

| Option | Board |
| --- | --- |
| A · Editorial Clean | `storyboard/out/option-a.jpg` |
| B · Fast TikTok Native | `storyboard/out/option-b.jpg` |
| C · Real vs AI | `storyboard/out/option-c.jpg` |

Source: `storyboard/build.py` → `storyboard/compositions/option-*.html`; boards by `storyboard/boards.py`.

## Hook options (opening 0–4 s)

Rules for every hook: the hook text is on screen from **frame 0** (no intro, no logo), the first spoken word lands within 0.2 s, and the cover uses the same line so the post and the opening match.

| # | Hook | Spoken (Take A, word-timed) | On-screen from frame 0 | Then | Default for |
| --- | --- | --- | --- | --- | --- |
| **H1** | Stat shock (cold open) | "3 daripada 4" (35.04–36.62) + "skip content yang nampak terlalu polished" (39.56–42.26), ~4.3 s | **3 DARI 4** orang skip content AI | Jump to "AI sekarang dah boleh…" (1.72) | A |
| **H2** | Contrarian statement (cold open) | "Video yang perfect bukan lagi kelebihan utama dah" (71.18–74.78), 3.6 s | **VIDEO PERFECT DAH TAK LAKU.** | Jump to "AI sekarang dah boleh…" (1.72) | B |
| **H3** | Glitch question | "AI sekarang dah boleh buat video yang nampak real" (1.72–5.22), face glitched until "real" | **INI REAL ATAU AI?** | Snaps clean, carries on | C |

H1 and H2 are flash-forwards: the line plays again in its place later (about +4 s runtime). Recommendation: **H2**. It is the shortest, it's a claim people want to argue with (good for comments), and it pairs with Cover 1.

## Edits common to all three options

| # | Change | Source | Why |
| --- | --- | --- | --- |
| E1 | Trim head: start at 1.60 (or the hook clip above) | A | Cut the dead air before "AI sekarang" |
| E2 | Cut gaps > 0.35 s (9.32–9.68, 54.20–54.90, 89.00–89.50) | A | Tighter pacing, ~3 s saved |
| E3 | Replace "Menurut kajian TikTok sendiri pada tahun ni" (A 31.64–35.04) with "…pada tahun 2026" | **B 31.86–35.18** | Names the year; same car/shirt, so it reads as a jump cut |
| E4 | Cut "They can add to it" (A 118.52–119.48) so the line reads "Dia nak something… actually trust" | A | Whisper and ear both trip on it; the ending lands cleaner |
| E5 | Trim tail after "…product review ni?" (A ~127.9) + 0.4 s hold | A | End on the question |

Estimated runtime: **~2:01** (H3) or **~2:05** (H1 / H2). Captions use the fixes in `NOTES.md` ("AI generated", "impressive", "show, don't just generate").

## Voice clarity — applies to every option

`scripts/voice.sh` (output replaces the camera audio in the edit):
1. **ElevenLabs Voice Isolator** removes car and room noise.
2. Then a cleanup chain: high-pass at 80 Hz, a gentle expander so pauses stay quiet, −2.5 dB at 250 Hz to remove mud, +3 dB presence at 3.5 kHz, +1.5 dB air shelf, a de-esser, and 3:1 compression.
3. Two-pass loudnorm, then a limiter.

| Take A | Integrated | True peak | Noise in pauses vs speech |
| --- | --- | --- | --- |
| Before | −24.7 LUFS | — | −60.7 dB vs −25.6 dB |
| After | **−14.5 LUFS** (TikTok/Reels/Shorts level) | **−1.2 dBFS** | **−65.7 dB** vs −14.9 dB |

A/B listen: `samples/voice-before-after.m4a`. It plays the hook before processing (gain-matched), then 0.6 s of silence, then the same hook after.

## Colour grade + light retouch — applies to every option

1. **Retouch** (`scripts/retouch.sh`, ffmpeg, before HyperFrames): `hqdn3d` denoise for the low-light phone noise, edge-preserving `bilateral` skin smoothing blended at 45% (pores, stubble and the mole stay), a small `unsharp` back on eyes and hair. Before/after: `covers/out/retouch-before-after.jpg`.
2. **Grade** (`grade.json`): HyperFrames preset **`skin-soft`** (your pick). Applied with `hyperframes media-treatment` on every footage plate. Option C adds its glitch treatment on top of this base, only on the "AI" moments. Earlier candidates are in `covers/out/grade-compare.jpg`.

## Safe zone (TikTok + Reels + Shorts) — applies to every option

Spec: `safe-zone.json`. Footage runs full-bleed. **Every caption, motion graphic and b-roll card stays inside the content box.**

| Zone | Pixels (1080×1920) | Used for |
| --- | --- | --- |
| Content box | x 64–900, y 220–1330 | All overlays: title cards, stat cards, tip cards, chips, b-roll inserts |
| Caption band | x 64–900, bottom-anchored at y 1310 | Running captions. They grow upward when a line wraps, so they never fall into the UI |
| Reserved top | y < 220 | Status bar, For You / Following tabs, Reels camera icon |
| Reserved right | x > 900 | Like / comment / share / audio rail |
| Reserved bottom | y > 1330 | Username, post caption, audio ticker, Shorts subscribe bar |
| Cover grid crop (3:4) | y 240–1680 | Cover headline must also fit here for the profile grid |

- B-roll and motion-graphic inserts are cards inside the content box (max 836 px wide). A full-screen b-roll cut is fine, but any text on it follows the same box.
- `scripts/check-safe-zone.mjs covers/compositions storyboard/compositions` measures every overlay element and fails on any overflow. It caught several real overflows while these were built (a headline running into the action rail, captions wrapping into the bottom UI), and all 4 covers and 18 style frames now pass. The edit composition will go through the same check. `covers/out/safe-zone-preview.jpg` shows the zones (red = reserved, green = content box, cyan = 3:4 grid crop).

---

## Option A — "Editorial Clean" (credible, calm) · board `storyboard/out/option-a.jpg`

Look: white Inter captions, 2–3 words at a time, key word in yellow `#FFD60A`. Data sits on off-white paper cards. Soft lo-fi bed. Default hook **H1**, cover **2** or **1**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Hook (H1) | 35.0 → 1.6–9.3 | Stat card from frame 0, 110% punch-in | **3 dari 4** orang skip content AI | Soft riser into the downbeat |
| Context | 9.7–29.7 | Chips stack in on "affiliate / produk review / AI model, AI voice" | `Affiliate` `Product review` `AI model · AI voice` | Light whoosh per chip |
| Data | 29.7–54.2 | Paper stat cards: 3/4, then 9/10 | **9 dari 10** — authentic content pengaruh keputusan beli · `Kajian TikTok 2026` | Tick on each number |
| Thesis | 54.9–74.8 | Quote card + 110% punch-in | Technology is getting better. / But **authenticity** is becoming more valuable. | Music dips −6 dB |
| Tips | 74.8–112.0 | "3 TIPS ● ○ ○" tracker top-left + one tip card per tip | **01** Show, don't just generate · **02** Share real experiences · **03** AI as a tool | Soft pop per tip |
| CTA | 112.0–128.3 | Title + punch-in, hold 0.4 s | **Korang masih percaya ke?** + "Komen kat bawah ↓" | Music resolves |

## Option B — "Fast TikTok Native" (retention first) · board `storyboard/out/option-b.jpg`

Look: every pause cut (target **~1:50**), punch-in alternates 100% / 118% every 3–5 s. Huge Anton captions with black stroke, 1–3 words. Upbeat track, SFX on every beat. Default hook **H2**, cover **1**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Hook (H2) | 71.2 → 1.6–9.3 | 118% zoom from frame 0 | **VIDEO PERFECT DAH TAK LAKU.** | Bass hit on frame 0 |
| Context | 9.7–29.7 | Scroll-swipe transition, rotated stamps | **AI MODEL** · **AI VOICE** · "SAMA JE" | Swipe whoosh, ding ×2 |
| Data | 29.7–54.2 | Zoom 118% + red flash | Giant **3/4** + red **SKIP!** stamp; then **9/10** | Impact boom per number |
| Thesis | 54.9–74.8 | 0.3 s black before the line, typewriter | TECHNOLOGY ↑ / **AUTHENTICITY ↑↑** | Music drop-out, back on "Tapi aku" |
| Tips | 74.8–112.0 | 0.2 s number slam per tip | **#1 SHOW.** · **#2 REAL** · **#3 AI = TOOL** | Slam ×3 |
| CTA | 112.0–128.3 | Push-in 100→112% | **KORANG PERCAYA KE?** + "KOMEN ↓" | Music stops on "ni?" — silent end |

## Option C — "Real vs AI" (concept edit) · board `storyboard/out/option-c.jpg`

Look: one rule — **whenever AI is mentioned, the footage glitches** (HyperFrames `digitalGlitch` + `scanlines`, ~0.4 s). **Real / authentic** moments are clean. Mono captions on black bars, key word on red. Dark synth bed. Default hook **H3**, cover **3**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Hook (H3) | 1.6–9.3 | Fully glitched from frame 0, snaps clean on "real" | **INI REAL ATAU AI?** + `AI?` tag | Glitch burst, then room tone |
| Context | 9.7–29.7 | Split screen: real left / glitched right | `REAL` / `AI` tags | Glitch ticks |
| Data | 29.7–54.2 | Clean; terminal readout card | `> 3/4 skip polished / AI content` · `> 9/10 trust authentic` · `src: TikTok 2026` | Keyboard ticks |
| Thesis | 54.9–74.8 | Seam wipe glitched → clean on "authenticity" | Technology ↑ / **Authenticity ↑↑** | Synth opens up |
| Tips | 74.8–112.0 | Terminal tip card; tips 1 and 3 start glitched and resolve clean | `// tip 01` SHOW, don't just generate | Resolve whoosh |
| CTA | 112.0–128.3 | Clean, final question | **Korang masih percaya?** | Synth cuts with a glitch tail |

---

## Cover options (rendered in HyperFrames)

Project: `covers/`. Each cover is a sub-composition (`covers/compositions/cover-N.html`), using retouched Take A frames with the `skin-soft` grade. All four pass the safe-zone check.
Stills: `covers/out/cover-1.jpg` … `cover-4.jpg`, all four on `covers/out/contact-sheet.jpg`.

| # | Hook | Frame (A) | Headline | Pairs with |
| --- | --- | --- | --- | --- |
| 1 | Contrarian | 8.2 s (skeptical look) | VIDEO PERFECT **DAH TAK LAKU?** | H2 · B (or A) |
| 2 | Stat shock | 52.6 s (smirk) | **3 DARI 4** orang terus SKIP video macam ni | H1 · A |
| 3 | Real vs AI | 8.2 s, right half glitched | INI REAL **ATAU AI?** | H3 · C |
| 4 | Tips | 53.4 s (hand up) | AFFILIATE & BUSINESS · JANGAN ~~GENERATE~~ JE. **SHOW.** + 3 tips | B |

Re-render: `cd covers && npx hyperframes snapshot --at 0.5,1.5,2.5,3.5 --no-end`.
