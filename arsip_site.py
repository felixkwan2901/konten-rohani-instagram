"""Bangun arsip web @diam.dan.percaya dari folder output/tenang* dan output/reels/tenang.

  python3 arsip_site.py       # tulis thumbs/, full/, reels/ dan collections.js ke situs

Hasilnya masuk ke repo GitHub Pages (kwanfelix.me/diam.dan.percaya). File yang sudah
ada dan lebih baru dari sumbernya dilewati, jadi menjalankan ulang cepat.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT = ROOT / "output"
SITE = Path.home() / "felixkwan2901.github.io" / "diam.dan.percaya"

# (folder sumber, folder di situs, nama tampil). Urutan = urutan posting; nama tampil = nomor saja.
COLLECTIONS = [
    ("tenang", "tenang", "01"),
    ("tenang_keren", "tenang-keren", "02"),
    ("tenang_w2", "tenang-w2", "03"),
    ("tenang_keren2", "tenang-keren2", "04"),
    ("tenang_minggu2", "tenang-minggu2", "05"),
]
REELS = ("reels/tenang", "reels", "Reels")
SLOTS = {"pagi": 0, "siang": 1, "sore": 2, "petang": 3, "malam": 4}
BEST_PER_FOLDER = 6  # how many picks per folder appear on the "Semua" sphere


def mark_best(items, stems):
    """Pick the cover slides (…_1) spread evenly over the folder; those are the post hooks."""
    covers = [i for i, st in enumerate(stems) if st.endswith("_1")] or list(range(len(items)))
    n = min(BEST_PER_FOLDER, len(covers))
    for k in range(n):
        items[covers[k * len(covers) // n]]["best"] = True


def order(path):
    m = re.match(r"hari(\d+)_([a-z]+)_(\d+)$", path.stem)
    if m:
        return (0, int(m.group(1)), SLOTS.get(m.group(2), 9), int(m.group(3)), "")
    parts = re.split(r"(\d+)", path.stem)
    return (1, 0, 0, 0, [int(p) if p.isdigit() else p for p in parts])


def stale(src, dst):
    return not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime


def sips(src, dst, size, quality):
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["sips", "-Z", str(size), "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
                    str(src), "--out", str(dst)], check=True, capture_output=True)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def main():
    data = []
    for folder, cid, name in COLLECTIONS:
        items, stems = [], []
        for src in sorted((OUTPUT / folder).glob("*.jpg"), key=order):
            thumb = SITE / "thumbs" / cid / src.name
            mini = SITE / "mini" / cid / src.name
            if stale(src, mini):
                sips(src, mini, 300, 72)  # small copy for sphere cards, light on phone GPU memory
            full = SITE / "full" / cid / src.name
            if stale(src, thumb):
                sips(src, thumb, 640, 78)
            if stale(src, full):
                full.parent.mkdir(parents=True, exist_ok=True)
                ffmpeg("-i", str(src), "-q:v", "6", str(full))  # ~30% of the original, no visible loss
            items.append({"m": f"mini/{cid}/{src.name}", "t": f"thumbs/{cid}/{src.name}",
                          "f": f"full/{cid}/{src.name}", "ar": 0.8})
            stems.append(src.stem)
        mark_best(items, stems)
        data.append({"id": name, "name": name, "items": items})
        print(f"{name} ({folder}): {len(items)}")

    folder, cid, name = REELS
    items = []
    for src in sorted((OUTPUT / folder).glob("*.mp4"), key=order):
        video = SITE / "reels" / src.name
        poster = SITE / "thumbs" / cid / (src.stem + ".jpg")
        if stale(src, video):
            video.parent.mkdir(parents=True, exist_ok=True)
            ffmpeg("-i", str(src), "-map", "0:v:0", "-map", "0:a?", "-vf", "scale=720:-2",
                   "-c:v", "libx264", "-crf", "27", "-preset", "slow", "-pix_fmt", "yuv420p",
                   "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(video))
        if stale(src, poster):
            poster.parent.mkdir(parents=True, exist_ok=True)
            ffmpeg("-ss", "1", "-i", str(src), "-frames:v", "1", "-vf", "scale=512:-2", "-q:v", "4", str(poster))
        mini = SITE / "mini" / cid / (src.stem + ".jpg")
        if stale(poster, mini):
            sips(poster, mini, 300, 72)
        items.append({"m": f"mini/{cid}/{src.stem}.jpg", "t": f"thumbs/{cid}/{src.stem}.jpg",
                      "f": f"thumbs/{cid}/{src.stem}.jpg", "v": f"reels/{src.name}", "ar": 9 / 16})
    for k in range(min(BEST_PER_FOLDER, len(items))):
        items[k * len(items) // min(BEST_PER_FOLDER, len(items))]["best"] = True
    data.append({"id": "reels", "name": name, "items": items})
    print(f"{name}: {len(items)}")

    js = "window.COLLECTIONS = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (SITE / "collections.js").write_text(js)
    # Cache-bust: GitHub Pages caches for 10 minutes, so point index.html at this exact version.
    version = hashlib.md5(js.encode()).hexdigest()[:8]
    page = SITE / "index.html"
    page.write_text(re.sub(r"collections\.js\?v=\w+", f"collections.js?v={version}", page.read_text()))
    print("ditulis ke", SITE)


if __name__ == "__main__":
    main()
