# Hard Rock Hotel Desaru Coast — Holiday Encore Season 3 (15s promo)

`HardRock_Desaru_HolidayEncore_15s_9x16.mp4`: 1080×1920, 30 fps, H.264 + AAC, 15 s.

Offer details come from https://hotel.hardrock.com/desaru-coast/holiday-encore-2026.aspx. Photos and logo come from the hotel website.

## Rebuild
```bash
mkdir -p frames
for i in 0 1 2 3; do node tools/render.js "$PWD/promo.html" "$PWD/frames" 30 15 $i 4 & done; wait
python3 tools/sound.py audio.wav
ffmpeg -framerate 30 -i frames/f%04d.jpg -i audio.wav -c:v libx264 -crf 17 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -movflags +faststart -shortest HardRock_Desaru_HolidayEncore_15s_9x16.mp4
```
- `promo.html` holds the motion design as CSS animations on a single master timeline. `window.render(t)` seeks it to time `t`.
- `tools/render.js` captures the frames with Playwright. Its last two arguments split the work into parallel shards.
- `tools/sound.py` synthesizes the music bed (150 bpm) and the SFX (riser, impacts, whooshes, ticks, pops, chimes) with numpy.
