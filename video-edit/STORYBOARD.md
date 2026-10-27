# Storyboard options — "Orang masih percaya ke?"

Base: **Take A** (`VID_20261027_081227.mp4`), 1080×1920. Timings below are Take A source times.
Pick one storyboard + one cover, and I'll build the full HyperFrames edit from it.

## Edits common to all three options

| # | Change | Source | Why |
| --- | --- | --- | --- |
| E1 | Trim head: start at 1.60 | A | Cut the dead air before "AI sekarang" |
| E2 | Cut gaps > 0.35 s (9.32–9.68, 54.20–54.90, 89.00–89.50) | A | Tighter pacing, ~3 s saved |
| E3 | Replace "Menurut kajian TikTok sendiri pada tahun ni" (A 31.64–35.04) with "…pada tahun 2026" | **B 31.86–35.18** | Names the year; same car/shirt, so it reads as a jump cut |
| E4 | Cut "They can add to it" (A 118.52–119.48) so the line reads "Dia nak something… actually trust" | A | Whisper and ear both trip on it; the ending lands cleaner |
| E5 | Trim tail after "…product review ni?" (A ~127.9) + 0.4 s hold | A | End on the question |

Estimated runtime after E1–E5: **~2:01**. Captions use the fixes in `NOTES.md` ("AI generated", "impressive", "show, don't just generate").

## Safe zone (TikTok + Reels + Shorts) — applies to every option

Spec: `safe-zone.json`. Footage runs full-bleed; **every caption, motion graphic and b-roll card stays inside the content box**.

| Zone | Pixels (1080×1920) | Used for |
| --- | --- | --- |
| Content box | x 64–900, y 220–1330 | All overlays: title cards, stat cards, tip cards, chips, b-roll inserts |
| Caption band | x 64–900, y 1040–1330 | Running captions (max 2 lines, bottom-anchored at y 1330) |
| Reserved top | y < 220 | Status bar, For You / Following tabs, Reels camera icon |
| Reserved right | x > 900 | Like / comment / share / audio rail |
| Reserved bottom | y > 1330 | Username, post caption, audio ticker, Shorts subscribe bar |
| Cover grid crop (3:4) | y 240–1680 | Cover headline must also fit here for the profile grid |

Rules for the edit:
- Captions sit in the caption band, over the black shirt (face stays clear, high contrast).
- B-roll / motion-graphic inserts are cards inside the content box (max 836 px wide); a full-screen b-roll cut is fine, but any text on it follows the same box.
- "Top-left tracker" (Option A), chips and `AI?` labels (Option C) start at y ≥ 220 and end at x ≤ 900.
- `covers/check-safe-zone.mjs` measures every overlay element against `safe-zone.json` and fails on any overflow; the edit composition will use the same check. `covers/out/safe-zone-preview.jpg` shows the zones (red = reserved, green = content box, cyan = 3:4 grid crop).

## Colour grade + light retouch — applies to every option

1. **Retouch** (`scripts/retouch.sh`, ffmpeg, before HyperFrames): `hqdn3d` denoise for the low-light phone noise, edge-preserving `bilateral` skin smoothing blended at 45% (pores, stubble and the mole stay), small `unsharp` back on eyes/hair. Before/after: `covers/out/retouch-before-after.jpg`.
2. **Grade** (`grade.json`, applied with `hyperframes media-treatment`): **A Natural Warm** — exposure +0.22, shadows +0.18, highlights −0.12, contrast +0.08, blacks −0.04, temperature +0.06, tint +0.02, vibrance +0.12, vignette 0.12. Lifts the under-lit face (avg luma was 63/255), warms skin, keeps the black shirt deep for captions.
   Compared against "Clean Bright", "Moody Contrast" and the built-in `skin-soft` preset in `covers/out/grade-compare.jpg`. Option C adds its glitch treatment on top of this base only on the "AI" moments.

---

## Option A — "Editorial Clean" (credible, calm)

Look: footage gets a light grade (contrast +, vignette). White Inter captions, 2–3 words at a time, the key word in yellow `#FFD60A`. Data appears as clean cards. Soft lo-fi bed.
Best cover: **Cover 1 (Soalan besar)** or **Cover 2 (3 dari 4)**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Hook | 1.6–9.3 | Full frame; 110% punch-in on "orang masih percaya ke?" | Title card top: **ORANG MASIH PERCAYA KE?** | Soft riser into downbeat at 6.1 |
| Context | 9.7–29.7 | Straight talking head; 3 small chips slide in on "affiliate / produk review / iklan branding" | Chips: `Affiliate` `Product review` `Iklan` | Light whoosh per chip |
| Data | 29.7–54.2 | Lower-half stat cards over the shirt: "3 / 4" counter, then "9 / 10" counter | **3 dari 4** skip content AI / terlalu polished · **9 dari 10** — authentic content pengaruh keputusan beli · `Sumber: kajian TikTok 2026` | Tick on each counter landing |
| Thesis | 54.9–74.8 | 115% punch-in on "authenticity is becoming more valuable" | Two-line quote card: Technology is getting better / **Authenticity** is becoming more valuable | Music dips −6 dB under the quote |
| Tips | 74.8–112.0 | Persistent "3 TIPS" tracker top-left; each tip gets a numbered card | **1** Show, don't just generate · **2** Share real experiences · **3** AI as a tool, not your identity | Soft "pop" on each number |
| CTA | 112.0–128.3 | Punch-in on the final question, hold 0.4 s | **Korang masih percaya ke?** + "Komen 👇" | Music resolves, out |

## Option B — "Fast TikTok Native" (retention first)

Look: no grade change, every pause cut (target **~1:50**), punch-in alternates 100% / 118% every 3–5 s. Big Anton word-pop captions (one word at a time on stressed words). Upbeat track, SFX on every beat.
Best cover: **Cover 1** or **Cover 4 (Jangan generate je)**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Hook | 1.6–9.3 | Opens at 118% zoom, snap to 100% on "Tapi" | Word pops: **REAL** · **PERFECT** · then **PERCAYA KE?** shakes in | Bass hit at 1.6; record-scratch on "Tapi persoalannya" |
| Context | 9.7–29.7 | Fake TikTok scroll swipe transition (2 frames of blurred vertical slide) on "scroll TikTok" | **AI MODEL** · **AI VOICE** stamp on screen; "SAMA JE" at 27–29.7 | Swipe whoosh; "ding" ×3 |
| Data | 29.7–54.2 | Zoom 118% + red flash frame on the stat | Giant **3/4** with red **SKIP**; giant **9/10** with yellow **BELI** | Impact boom on each number |
| Thesis | 54.9–74.8 | Hard cut to black 0.3 s before "Technology is getting better" | Typewriter: TECHNOLOGY ↑ · AUTHENTICITY ↑↑ | Music drop-out, then back in on "Tapi aku bukan nak cakap" |
| Tips | 74.8–112.0 | Each tip opens with a 0.2 s number slam | **#1 SHOW** · **#2 REAL EXPERIENCE** · **#3 AI = TOOL** | Slam SFX ×3 |
| CTA | 112.0–128.3 | Slow push-in 100→112% over the final line | **KORANG PERCAYA KE?** + comment arrow | Music stop on "ni?" — silence ending |

## Option C — "Real vs AI" (concept edit)

Look: one visual rule — **every time AI is mentioned, the footage glitches** (HyperFrames `digitalGlitch` + `scanlines` treatment, ~0.4 s); **real/authentic** moments are clean and warm. Dark synth bed.
Best cover: **Cover 3 (Korang boleh beza lagi?)**.

| Beat | Time (A) | Visual | On-screen text | Audio (ElevenLabs) |
| --- | --- | --- | --- | --- |
| Cold open | 1.6–6.1 | First 1.5 s fully glitched + desaturated, label `AI?` top-right; snaps clean on "nampak perfect" | `AI?` → `REAL` label flip | Digital glitch burst, then room tone |
| Hook | 6.1–9.3 | Clean, 112% punch-in | **ORANG MASIH PERCAYA KE?** | Low synth pulse starts |
| Context | 9.7–29.7 | Glitch hits on "AI model", "AI voice"; split-screen (real left / glitched right) on "semuanya nampak sama" | `AI MODEL` `AI VOICE` in mono font | Glitch ticks on each hit |
| Data | 29.7–54.2 | Clean frame, stats as terminal-style mono readouts | `> 3/4 skip AI content` · `> 9/10 trust authentic` · `src: TikTok 2026` | Keyboard ticks |
| Thesis | 54.9–74.8 | Seam wipe: glitched → clean exactly on "authenticity" | Technology ↑ / **Authenticity** ↑↑ | Synth opens up |
| Tips | 74.8–112.0 | Tip 1 & 3 start glitched and resolve clean as he explains | `01 SHOW` `02 REAL` `03 AI = TOOL` | Glitch→clean "resolve" whoosh |
| CTA | 112.0–128.3 | Clean; final frame half-glitches on "AI generated product review ni?" | **Korang masih percaya?** | Synth cuts with a glitch tail |

---

## Cover options (rendered in HyperFrames)

Project: `covers/` — each cover is a sub-composition (`covers/compositions/cover-N.html`), frames from Take A with the retouch + Natural Warm grade above. All four pass `check-safe-zone.mjs`.
Stills: `covers/out/cover-1.jpg` … `cover-4.jpg`, all four on `covers/out/contact-sheet.jpg`.

| # | Name | Frame (A) | Headline | Fits |
| --- | --- | --- | --- | --- |
| 1 | Soalan besar | 8.2 s (skeptical look) | ORANG MASIH **PERCAYA KE?** | A, B |
| 2 | Statistik | 52.6 s (smirk, "nampak tak?") | **3 DARI 4** orang SKIP content AI | A |
| 3 | Real vs AI | 8.2 s, right half glitched | KORANG BOLEH **BEZA LAGI?** | C |
| 4 | Tips | 53.4 s (hand up) | JANGAN ~~GENERATE~~ JE. **SHOW.** + 3 tips | B |

Re-render the stills: `cd covers && npx hyperframes snapshot --at 0.5,1.5,2.5,3.5 --no-end`.
