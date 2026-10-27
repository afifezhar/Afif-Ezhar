#!/usr/bin/env bash
# Light retouch for the talking-head footage, applied before the HyperFrames grade.
#   hqdn3d     : low-light phone noise
#   bilateral  : edge-preserving skin smoothing, blended at 45% so pores and stubble stay
#   unsharp    : small amount back on eyes/hair edges
# Usage: scripts/retouch.sh <in.mp4> <out.mp4>          (video)
#        scripts/retouch.sh <in.mp4> <out.jpg> <seconds> (one still, for covers)
set -euo pipefail
RETOUCH="hqdn3d=2:1.5:4:3,split[a][b];[b]bilateral=sigmaS=6:sigmaR=0.08[s];[a][s]blend=all_mode=normal:all_opacity=0.45,unsharp=5:5:0.35"
in="$1"; out="$2"
if [[ $# -ge 3 ]]; then
  ffmpeg -loglevel error -y -ss "$3" -i "$in" -frames:v 1 -filter_complex "$RETOUCH" -q:v 2 "$out"
else
  ffmpeg -loglevel error -stats -y -i "$in" -filter_complex "$RETOUCH" \
    -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -c:a copy -movflags +faststart "$out"
fi
