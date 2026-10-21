"""Jadwal ulang post yang terlewat + posting ulang versi yang sudah dibetulkan.

17-21 Okt 2026 posting otomatis mati (config.py sempat mengimpor modul yang butuh Pillow), jadi 50 post Tenang dan
11 post Eli & Ruthie tidak tayang. Post itu diselipkan ke slot tambahan:
  Tenang : 3 slot ekstra per hari (pagi 08:15, siang 14:15, malam 20:40), jadi ±15 post sehari sampai habis.
  Eli    : 1 slot ekstra per hari (12:30 WIB).
Post yang menyebut hari tertentu (Senin, Minggu, besok, ...) dipindah ke HARI yang sama minggu berikutnya; semua post tetap
di bagian hari yang sama (pagi/siang/malam), supaya kalimat seperti "pagi ini" tetap pas.

Posting ulang ("ulang"): post yang sudah tayang dengan kesalahan (gaya MINIMAL remix Okt mengecilkan semua huruf, termasuk
"Aku" dan "Tuhan") diposting lagi dengan desain aslinya. Post lama yang salah dihapus Felix sendiri di Instagram.

Data: state/jadwal_ulang.json  {"pindah": {id: waktu_baru}, "ulang": [item post baru]}
Dipanggil dari render.build_schedule (sebelum Story dibuat) dan bisa diterapkan langsung ke output/schedule.json.
"""
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
FILE = ROOT / "state" / "jadwal_ulang.json"
EKSTRA = {"tenang": {"pagi": "08:15", "siang": "14:15", "malam": "20:40"}, "eli": {"siang": "12:30"}}
HARI_ID = r"\b(Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu|besok)\b"
HARI_EN = r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|tomorrow)\b"


def bagian(waktu):
    jam = int(waktu[11:13])
    return "pagi" if jam < 11 else "siang" if jam < 17 else "malam"


def susun(antre, akun, mulai, sudah_terisi=None):
    """antre: item urut waktu asli. Kembalikan {id: waktu_baru}. Hari yang sama untuk post yang menyebut hari."""
    slot = EKSTRA[akun]
    terisi = sudah_terisi or set()
    hasil = {}
    sisa = list(antre)
    hari = mulai
    while sisa and hari < mulai + timedelta(days=60):
        for b, jam in slot.items():
            if (hari, b) in terisi:
                continue
            for it in sisa:
                asli = datetime.fromisoformat(it["waktu"])
                b_it = bagian(it["waktu"]) if len(slot) > 1 else b
                terikat = re.search(HARI_ID if akun == "tenang" else HARI_EN, it.get("caption", ""))
                if b_it == b and (not terikat or asli.weekday() == hari.weekday()):
                    hasil[it["id"]] = f"{hari}T{jam}:00+07:00"
                    terisi.add((hari, b))
                    sisa.remove(it)
                    break
        hari += timedelta(days=1)
    if sisa:
        raise SystemExit(f"{len(sisa)} post {akun} tidak dapat slot")
    return hasil


def terapkan(items):
    """Pindahkan waktu post (dan Story-nya, +10 menit) lalu tambahkan post ulang. Item lain tidak diubah."""
    if not FILE.exists():
        return items
    data = json.loads(FILE.read_text())
    pindah = data.get("pindah", {})
    for it in items:
        if it["id"] in pindah:
            it["waktu"] = pindah[it["id"]]
        elif it["id"].startswith("story-") and it["id"][6:] in pindah:
            it["waktu"] = (datetime.fromisoformat(pindah[it["id"][6:]]) + timedelta(minutes=10)).isoformat()
    ada = {it["id"] for it in items}
    items += [dict(u) for u in data.get("ulang", []) if u["id"] not in ada]
    return items
