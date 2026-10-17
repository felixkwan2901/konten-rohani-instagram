"""Unduh font pengganti (lisensi OFL/Apache dari Google Fonts) untuk dipakai di mesin cloud (Linux) yang tidak punya font macOS.
Peta macOS -> pengganti ada di fonta.py (PETA). Jalankan sekali; hasilnya di fonts/*.ttf dan ikut di-commit.

  python3 fonts/ambil_font.py
"""
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fonta import PETA, nama_file  # noqa: E402

DIR = Path(__file__).resolve().parent


def ambil(keluarga, berat, miring):
    tujuan = DIR / nama_file(keluarga, berat, miring)
    if tujuan.exists():
        return tujuan
    for b, m in ((berat, miring), (berat, 0), (400, miring), (400, 0)):  # kalau gaya persis tidak ada, pakai yang terdekat
        q = urllib.parse.quote(keluarga) + (f":ital,wght@{m},{b}" if m else f":wght@{b}")
        req = urllib.request.Request(f"https://fonts.googleapis.com/css2?family={q}", headers={"User-Agent": "curl/8"})
        try:
            css = urllib.request.urlopen(req, timeout=30).read().decode()
        except Exception:
            continue
        url = re.search(r"url\((https://[^)]+\.ttf)\)", css)
        if url:
            tujuan.write_bytes(urllib.request.urlopen(url.group(1), timeout=60).read())
            if (b, m) != (berat, miring):
                print(f"  {keluarga} {berat}{'i' if miring else ''} tidak ada -> pakai {b}{'i' if m else ''}")
            return tujuan
    raise SystemExit(f"gagal mengambil {keluarga} {berat} {miring}")


if __name__ == "__main__":
    perlu = sorted({v for wajah in PETA.values() for v in wajah.values()})
    for keluarga, berat, miring in perlu:
        p = ambil(keluarga, berat, miring)
        print(f"{p.name:40s} {p.stat().st_size // 1024} KB")
