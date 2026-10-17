#!/usr/bin/env bash
# Siapkan mesin cloud (Linux) untuk merender konten: ffmpeg/ffprobe, cairo, paket Python.
# Font macOS tidak ada di sini; fonta.py otomatis memakai font bebas lisensi di fonts/.
set -u
cd "$(dirname "$0")/.."
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  (sudo -n apt-get update -qq && sudo -n apt-get install -y -qq ffmpeg libcairo2) 2>/dev/null \
    || (apt-get update -qq && apt-get install -y -qq ffmpeg libcairo2) 2>/dev/null \
    || true
fi
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  # cadangan tanpa apt: biner statis ffmpeg + ffprobe dari pip
  python3 -m pip install -q static-ffmpeg && mkdir -p "$HOME/.local/bin" \
    && python3 - <<'PY'
import os, static_ffmpeg.run as r
ff, fp = r.get_or_fetch_platform_executables_else_raise()
for exe in (ff, fp):
    dst = os.path.expanduser("~/.local/bin/" + os.path.basename(exe))
    if not os.path.exists(dst):
        os.symlink(exe, dst)
PY
  export PATH="$HOME/.local/bin:$PATH"
fi
python3 -m pip install -q pillow numpy cairosvg 2>/dev/null || python3 -m pip install -q --break-system-packages pillow numpy cairosvg
python3 - <<'PY'
import shutil, config, fonta  # noqa
from PIL import ImageFont
f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 40, index=8)
print("font:", f.getname(), "| ffmpeg:", shutil.which("ffmpeg"), "| ffprobe:", shutil.which("ffprobe"))
PY
