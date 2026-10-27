#!/usr/bin/env bash
# Builds assets/media/ for motion-test.html (not in git: regenerate from the source take).
# Needs: retouched Take A (../scripts/retouch.sh), processed voice (../scripts/voice.sh),
#        ELEVENLABS_API_KEY for the two SFX.
# Usage: ./prep-media.sh <A_retouched.mp4> <A_voice.wav>
set -euo pipefail
vid="$1"; voice="$2"; out=assets/media; mkdir -p "$out"
enc=(-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an -movflags +faststart)
# Hook H2 (flash-forward) and the opening line, Take A source times.
ffmpeg -loglevel error -y -ss 71.18 -i "$vid" -t 3.60 "${enc[@]}" "$out/hook.mp4"
ffmpeg -loglevel error -y -ss 1.72  -i "$vid" -t 7.90 "${enc[@]}" "$out/open.mp4"
# Voice: hook 71.18-74.78 then 1.72-9.62 back to back (11.5 s).
ffmpeg -loglevel error -y -i "$voice" -filter_complex \
  "[0]atrim=71.18:74.78,asetpts=PTS-STARTPTS[a];[0]atrim=1.72:9.62,asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1" \
  -c:a aac -b:a 192k "$out/voice.m4a"
sfx() {
  curl -sSf -o "$out/$1.mp3" -X POST https://api.elevenlabs.io/v1/sound-generation \
    -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
    -d "{\"text\":\"$2\",\"duration_seconds\":$3,\"prompt_influence\":0.6}"
}
sfx whoosh "short clean cinematic whoosh transition, airy swoosh, no music" 1.0
sfx type "soft quiet laptop keyboard typing, a few quick keystrokes, close mic" 1.5
