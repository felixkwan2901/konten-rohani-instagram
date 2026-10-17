"""Render SATU minggu Tenang lalu gabungkan ke output/schedule.json, tanpa merender ulang minggu lain.
Dipakai agen cloud mingguan (lihat CLOUD.md); di Mac juga bisa.

  python3 minggu.py tenang_w15            # ambil modul gaya & hari mulai dari config.MINGGU_TENANG
  python3 minggu.py tenang_w15 --cek      # hanya cek ID/tanggal, tidak merender
"""
import importlib
import json
import sys
from datetime import date, timedelta

import config
import render
from konten import tenang
from render import OUT


def pratinjau(rows, name, tw=216):
    """Seperti render.contact_sheet, tapi Reels (.mp4) diambil frame-nya di detik 1.5."""
    import subprocess
    from io import BytesIO

    from PIL import Image
    th = int(tw * render.H / render.W)
    sheet = Image.new("RGB", (max(len(r) for r in rows) * (tw + 8) + 8, len(rows) * (th + 8) + 8), "#DDDDDD")
    for r, row in enumerate(rows):
        for c, rel in enumerate(row):
            if rel.endswith(".mp4"):
                png = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", "1.5", "-i", str(OUT / rel), "-frames:v", "1",
                                      "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
                im = Image.open(BytesIO(png)).convert("RGB")
                im = im.crop((0, (im.height - im.width * render.H // render.W) // 2, im.width,
                              (im.height + im.width * render.H // render.W) // 2))
            else:
                im = Image.open(OUT / rel).convert("RGB")
            sheet.paste(im.resize((tw, th)), (8 + c * (tw + 8), 8 + r * (th + 8)))
    sheet.save(OUT / name, "JPEG", quality=88)


def main():
    mod = sys.argv[1]
    cocok = [m for m in config.MINGGU_TENANG if m[0] == mod]
    if not cocok:
        raise SystemExit(f"{mod} belum ada di config.MINGGU_TENANG")
    _, gaya, mulai = cocok[0]
    start = date.fromisoformat(config.START_DATE)
    at = lambda day, hhmm: f"{start + timedelta(days=day)}T{hhmm}:00+07:00"  # noqa: E731
    print(f"{mod} ({gaya}): {start + timedelta(days=mulai):%a %d %b %Y} - {start + timedelta(days=mulai + 6):%a %d %b %Y}")
    if "--cek" in sys.argv:
        return
    g = importlib.import_module(gaya)
    if hasattr(g, "render_reels") and "--tanpa-reels" not in sys.argv:  # Reels dirender dulu supaya ikut terjadwal
        g.render_reels(mod)
    baru = []
    for (hari, slot), (files, caption) in g.render_week(mod).items():
        baru.append({"id": f"{mod}-{hari}-{slot}", "akun": "tenang", "waktu": at(mulai + hari - 1, config.AKUN["tenang"]["jam"][slot]),
                     "files": files, "caption": caption + "\n.\n.\n" + tenang.TAGS})
    if config.STORY_OTOMATIS:
        baru = render.add_stories(baru)
    jadwal = json.loads((OUT / "schedule.json").read_text())
    jadwal = [it for it in jadwal if not it["id"].startswith((f"{mod}-", f"story-{mod}-"))]
    jadwal = sorted(jadwal + baru, key=lambda x: x["waktu"])
    (OUT / "schedule.json").write_text(json.dumps(jadwal, ensure_ascii=False, indent=2))
    # lembar pratinjau: halaman pertama tiap post, satu baris per hari
    per_hari = {}
    for it in baru:
        if not it.get("story"):
            per_hari.setdefault(it["waktu"][:10], []).append(it["files"][0])
    pratinjau([v for _, v in sorted(per_hari.items())], f"preview_{mod}.jpg")
    print(f"{len([b for b in baru if not b.get('story')])} post + {len([b for b in baru if b.get('story')])} story -> "
          f"output/schedule.json ({len(jadwal)} total). Pratinjau: output/preview_{mod}.jpg")


if __name__ == "__main__":
    main()
