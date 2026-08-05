#!/bin/bash
# Produce web-sized clips that PRESERVE projection metadata.
#
#   --disableSpatialConversion  keeps the spatial/immersive format intact
#   --disableMetadataFilter     keeps the ProjectionKind extension in the output
#
# Without both flags avconvert strips the projection metadata and the renderer
# silently falls back to flat video. Verify every output with tools/projcheck.py.

set -euo pipefail
cd "$(dirname "$0")/.."

SRC=media
OUT=assets
mkdir -p "$OUT"

# name | source | preset | start | duration
CLIPS=(
    "equirect360.mov|$SRC/demo_360.mov|Preset1920x1080|1|8"
    "equirect180.mov|$SRC/mono_180.mov|Preset1920x1080|2|8"
    "widefov.mp4|$SRC/wfov_stable.mp4|Preset1920x1080|2|8"
)

for entry in "${CLIPS[@]}"; do
    IFS='|' read -r name src preset start dur <<< "$entry"
    if [ ! -f "$src" ]; then
        echo "[SKIP] $name — missing source $src"
        continue
    fi
    echo "[..] $name  <- $(basename "$src")"
    avconvert --source "$src" --output "$OUT/$name" \
        --preset "$preset" --start "$start" --duration "$dur" \
        --disableSpatialConversion --disableMetadataFilter \
        --replace >/dev/null 2>&1
    echo "[OK] $name  $(du -h "$OUT/$name" | cut -f1)"
done

echo
echo "=== verifying projection metadata survived ==="
python3 tools/projcheck.py "$OUT"/*.mov "$OUT"/*.mp4
