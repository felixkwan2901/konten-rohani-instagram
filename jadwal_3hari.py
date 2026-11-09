"""Tenang: mulai 10 Nov 2026 hanya 3 post per hari (06:00, 12:00, 20:00 WIB), permintaan Felix karena reach turun.

Aturan:
- Post musiman (Natal/Adven, Tahun Baru, Januari, November) tetap dekat tanggal aslinya, maksimal
  bergeser 6 hari. Post hari peringatan (Hari Pahlawan, Hari HAM, ...) dan post bertanggal (hitung mundur "44 hari lagi",
  "Senin 14 Desember") hanya boleh di tanggal aslinya. Prioritas per hari: jarak ke tanggal asli, hitung mundur (seri harian, jangan bolong), post bertanggal,
  Reels, lalu jam. Post musiman yang lewat jendelanya disimpan sebagai cadangan (tidak dijadwalkan), mis. untuk tahun depan.
- Post umum (tidak terikat musim) dimundurkan berurutan untuk mengisi slot kosong, 3 per hari.
  Post yang menyebut hari (Senin, besok, ...) dipasang di hari yang sama, dan post yang menyebut waktu ("pagi ini",
  "Kamis siang", "Catatan malam") tetap di bagian hari aslinya (pagi 06:00 / siang 12:00 / malam 20:00).

Hasilnya disimpan di state/jadwal_3hari.json  {"waktu": {id: waktu_baru}, "cadangan": [id, ...]}
dan diterapkan oleh render.build_schedule dan minggu.py, supaya render ulang tidak membatalkannya.

  python3 jadwal_3hari.py      # susun ulang dari output/schedule.json sekarang (pakai waktu_asli), lalu terapkan
  Post minggu baru yang ditambahkan nanti: jalankan ini lagi setelah minggu.py supaya ikut aturan 3/hari.
"""
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
FILE = ROOT / "state" / "jadwal_3hari.json"
MULAI = date(2026, 11, 10)
WIB = timezone(timedelta(hours=7))
JAM = {"pagi": "06:00", "siang": "12:00", "malam": "20:00"}
MUSIM = {
    "hitungmundur": r"\b\d+ hari lagi\b",  # tayang tepat di tanggal aslinya
    "peringatan": r"\bHari (Kebaikan Sedunia|Anak Sedunia|Pahlawan|Hak Asasi Manusia|HAM|Guru|Ibu)\b|\bhari ke-\d+\b|\bMinggu ke-\d+\b",
    "natal": r"\b(Natal|Adven|Advent|Betlehem|palungan|kandang|gembala-gembala|Imanuel|malam kudus|Kristus Raja|kado|Desember)\b",
    "tahunbaru": r"\b(Tahun Baru|tahun baru|31 Desember|1 Januari|akhir tahun|tutup tahun|malam pergantian)\b",
    "januari": r"\b(Januari|Epifania|orang majus|Pembaptisan Tuhan|Pekan Doa|2027)\b",
    "november": r"\b(November|Oktober)\b",
}
TEPAT_RE = (r"\b\d+ hari lagi\b|\bhari ke-\d+\b|\bMinggu ke-\d+\b"  # hanya boleh tayang di tanggal aslinya
            r"|\b(Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu),? \d{1,2} (Oktober|November|Desember|Januari)\b"
            r"|\bHari ini\b[^.\n]{0,40}(\b\d{1,2} (November|Desember|Januari)\b|\bHari [A-Z])")
HARI_RE = r"\b(Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu|besok)\b"
WAKTU_RE = {"pagi": r"\bpagi (ini|hari)\b|\bselamat pagi\b", "siang": r"\b(siang|sore) (ini|hari)\b",
            "malam": r"\bmalam (ini|hari)\b|\bselamat malam\b|\bsebelum tidur\b|\bmalam Minggu\b"}


def asli(it):
    """Waktu asli post (sebelum aturan 3/hari), supaya menyusun ulang tidak menggeser yang sudah digeser."""
    return it.get("waktu_asli", it["waktu"])


def musim(it):
    for k, p in MUSIM.items():
        if re.search(p, it.get("caption", "")):
            return k
    return None


def bagian(waktu):
    jam = int(waktu[11:13])
    return "pagi" if jam < 11 else "siang" if jam < 17 else "malam"


def bagian_wajib(it):
    """Bagian hari yang harus dijaga kalau caption menyebut waktu ('pagi ini', 'Kamis siang', 'Catatan malam'):
    tetap di bagian hari aslinya. None kalau bebas."""
    judul = it.get("caption", "").split("\n")[0]
    if re.search(r"\b(pagi|siang|sore|malam)\b", judul) or any(re.search(p, it.get("caption", "")) for p in WAKTU_RE.values()):
        return bagian(asli(it))
    return None


def susun(items, posted, sekarang=None):
    sekarang = (sekarang or datetime.now(timezone.utc)).astimezone(WIB)
    hari = max(MULAI, sekarang.date())
    sisa = sorted([it for it in items if it["akun"] == "tenang" and not it.get("story") and it["id"] not in posted
                   and datetime.fromisoformat(it["waktu"]) > sekarang], key=asli)
    musiman = {}  # tanggal asli -> post musiman
    umum = []
    for it in sisa:
        if musim(it):
            musiman.setdefault(date.fromisoformat(asli(it)[:10]), []).append(it)
        else:
            umum.append(it)
    waktu, cadangan = {}, []
    akhir_musim = max(musiman) if musiman else hari
    pool = []  # post musiman yang belum terjadwal (asli sebelum hari mulai = cadangan)
    for d in sorted(musiman):
        if d < hari:
            cadangan += [it["id"] for it in musiman[d]]
        else:
            pool += musiman[d]
    antre = list(umum)
    batas = hari + timedelta(days=600)
    JARAK = 6  # post musiman boleh bergeser maksimal 6 hari dari tanggal aslinya

    def jarak(it):  # hari peringatan & post bertanggal hanya di harinya sendiri
        return 0 if musim(it) == "peringatan" or re.search(TEPAT_RE, it["caption"]) else JARAK

    def cocok(it, b, hari):
        hari_disebut = re.search(HARI_RE, it.get("caption", ""))
        wajib = bagian_wajib(it)
        return ((not hari_disebut or date.fromisoformat(asli(it)[:10]).weekday() == hari.weekday())
                and (not wajib or wajib == b))

    while (antre or pool or hari <= akhir_musim) and hari < batas:
        bebas = {b: j for b, j in JAM.items()  # hari pertama: hanya slot yang belum lewat
                 if datetime.fromisoformat(f"{hari}T{j}:00+07:00") > sekarang + timedelta(minutes=10)}
        # 1. post musiman: tanggal sendiri dulu (hitung mundur hanya di tanggalnya), lalu tetangga <= 6 hari
        def kunci(it):
            return (abs((date.fromisoformat(asli(it)[:10]) - hari).days), (0 if musim(it) == "hitungmundur" else 1 if re.search(TEPAT_RE, it["caption"])
                     else 2 if re.search(MUSIM["peringatan"], it["caption"].split("\n")[0])  # judulnya menyebut hari itu
                     else 3 if jarak(it) == 0 else 4),
                    0 if bagian_wajib(it) else 1,  # yang terikat bagian hari dipasang dulu
                    0 if it["files"][0].endswith(".mp4") else 1, asli(it))
        calon = sorted([it for it in pool if abs((date.fromisoformat(asli(it)[:10]) - hari).days) <= jarak(it)], key=kunci)
        for it in calon:
            if not bebas:
                break
            asli_b = bagian(asli(it))
            urut = [asli_b] + [b for b in bebas if b != asli_b]
            b = next((b for b in urut if b in bebas and cocok(it, b, hari)
                      and (b == asli_b or not bagian_wajib(it))), None)
            if b:
                waktu[it["id"]] = f"{hari}T{bebas.pop(b)}:00+07:00"
                pool.remove(it)
        # post musiman yang sudah lewat jendelanya -> cadangan
        for it in [it for it in pool if (hari - date.fromisoformat(asli(it)[:10])).days >= jarak(it)]:
            cadangan.append(it["id"])
            pool.remove(it)
        # 2. slot kosong diisi post umum (hari & bagian hari dijaga)
        for b in list(bebas):
            for it in antre:
                if cocok(it, b, hari):
                    waktu[it["id"]] = f"{hari}T{bebas.pop(b)}:00+07:00"
                    antre.remove(it)
                    break
        hari += timedelta(days=1)
    cadangan += [it["id"] for it in pool]
    cadangan += [it["id"] for it in antre]
    return {"catatan": "Tenang 3 post/hari mulai 10 Nov 2026 (lihat jadwal_3hari.py)", "waktu": waktu, "cadangan": cadangan}


def terapkan(items):
    """Pakai waktu baru untuk post Tenang (Story ikut +10 menit); post cadangan dan Story-nya dikeluarkan dari jadwal."""
    if not FILE.exists():
        return items
    data = json.loads(FILE.read_text())
    waktu, cadangan = data.get("waktu", {}), set(data.get("cadangan", []))
    hasil = []
    for it in items:
        pid = it["id"][6:] if it["id"].startswith("story-") else it["id"]
        if pid in cadangan:
            continue
        if pid in waktu:
            it.setdefault("waktu_asli", it["waktu"])
            t = datetime.fromisoformat(waktu[pid])
            it["waktu"] = (t + timedelta(minutes=10)).isoformat() if it["id"].startswith("story-") else t.isoformat()
        hasil.append(it)
    return hasil


if __name__ == "__main__":
    out = ROOT / "output" / "schedule.json"
    items = json.loads(out.read_text())
    posted = json.loads((ROOT / "state" / "posted.json").read_text())
    data = susun(items, posted)
    if FILE.exists():  # cadangan lama tetap cadangan (sudah tidak ada di schedule.json, jadi tidak terlihat oleh susun)
        lama = json.loads(FILE.read_text())
        data["cadangan"] += [c for c in lama.get("cadangan", []) if c not in posted and c not in data["cadangan"]
                             and c not in data["waktu"]]
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    items = sorted(terapkan(items), key=lambda x: x["waktu"])
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    hari = sorted({v[:10] for v in data["waktu"].values()})
    print(f"{len(data['waktu'])} post dijadwalkan ulang ({hari[0]} s.d. {hari[-1]}), {len(data['cadangan'])} cadangan")
