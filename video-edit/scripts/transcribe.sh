#!/usr/bin/env bash
# Word times, silence map and loudness envelope for one processed take; the edit list (edit/edl.py) cuts on these.
#   <name>.scribe.json    ElevenLabs Scribe words (more accurate word times than Whisper on this footage)
#   <name>.silences.json  [[start, end], ...] stretches >= 50 ms below -34 dB (breaths count as silence)
#   <name>.energy.json    {"hop": 0.01, "db": [...]} 10 ms loudness envelope, for picking the quietest cut point
# Usage: ELEVENLABS_API_KEY=... scripts/transcribe.sh <take_voice.wav> <out_dir> <name> [language_code, default msa]
set -euo pipefail
voice="$1"; out="$2"; name="$3"; lang="${4:-msa}"
mkdir -p "$out"; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

ffmpeg -loglevel error -y -i "$voice" -c:a libmp3lame -b:a 128k "$tmp/v.mp3"
curl -sSf -o "$out/$name.scribe.json" -X POST https://api.elevenlabs.io/v1/speech-to-text \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -F model_id=scribe_v1 -F language_code="$lang" \
  -F timestamps_granularity=word -F tag_audio_events=false -F file=@"$tmp/v.mp3"

ffmpeg -hide_banner -nostats -i "$voice" -af silencedetect=noise=-34dB:d=0.05 -f null - 2>&1 \
  | grep -oE "silence_(start|end): [0-9.]+" | paste - - \
  | awk 'BEGIN{printf "["} {if(NR>1)printf ","; printf "[%s,%s]", $2,$4} END{print "]"}' > "$out/$name.silences.json"

python3 - "$voice" "$out/$name.energy.json" <<'EOF'
import json, subprocess, sys
import numpy as np
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
n = len(x) // 160
db = np.round(20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)).astype(int).clip(-99, 0)
json.dump({"hop": 0.01, "db": db.tolist()}, open(sys.argv[2], "w"), separators=(",", ":"))
EOF
echo "wrote $out/$name.{scribe,silences,energy}.json"
