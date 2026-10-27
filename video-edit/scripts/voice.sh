#!/usr/bin/env bash
# Voice clarity for the talking-head takes.
#   1. ElevenLabs Voice Isolator (removes car/room noise, keeps the voice)
#   2. high-pass 80 Hz, gentle expander for pauses, -2.5 dB mud cut at 250 Hz,
#      +3 dB presence at 3.5 kHz, +1.5 dB air shelf, de-esser, 3:1 compression
#   3. two-pass loudnorm to -14 LUFS, then limiter at -1.5 dBTP (TikTok/Reels/Shorts level)
# Usage: ELEVENLABS_API_KEY=... scripts/voice.sh <in.mp4> <out.wav>
set -euo pipefail
in="$1"; out="$2"; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
ffmpeg -loglevel error -y -i "$in" -vn -ac 1 -ar 48000 -c:a pcm_s16le "$tmp/raw.wav"
curl -sSf -o "$tmp/iso.mp3" -X POST https://api.elevenlabs.io/v1/audio-isolation \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -F "audio=@$tmp/raw.wav"
PRE="highpass=f=80,agate=threshold=0.006:ratio=2.5:range=0.12:attack=5:release=180,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=3,highshelf=f=10000:g=1.5,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3"
m="$(ffmpeg -hide_banner -nostats -i "$tmp/iso.mp3" -af "$PRE,loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')"
g() { python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])" <<<"$m"; }
ffmpeg -loglevel error -y -i "$tmp/iso.mp3" -af "$PRE,loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,volume=1.3dB,alimiter=limit=0.84:attack=3:release=50:level=false" \
  -ar 48000 -c:a pcm_s16le "$out"
