"""Remix tampilan post Tenang 13-31 Oktober (minggu 3-5 + slot tambahan) yang belum terposting.

Masalah: minggu-minggu awal itu hanya memakai ~6 template per hari (buku x4, meme x3, skrip x2, ...), jadi grid terlihat sama.
Solusi: isi, ayat, dan caption TIDAK diubah (sudah dicek), hanya gambarnya digambar ulang dengan template lain dari
pustaka gaya (minggu 6-13) sehingga dalam satu hari tidak ada template yang terulang. Carousel, Reels, komik tetap.

Dipanggil dari render.build_schedule: items = remix_okt.remix(items)
"""
import datetime as dt
import importlib
import json
import re

import cek_ayat
import gaya_w6
import gaya_w7
import gaya_w8
import gaya_w10
import gaya_w11
import gaya_w12
import gaya_w13
from gaya_w7 import bersih
from render import OUT, ROOT, save

MULAI = "2026-10-13"
SELESAI = "2026-10-31"
MODS = ("tenang_w3", "tenang_w4", "tenang_w5", "tenang_extra")
KODE = {"T": "RELATABLE", "K": "KINETIK", "F": "DUMP", "V": "DULU"}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = {10: "Oktober", 11: "November"}
SCENE = {"panggung": "kabut", "lilin": "bintang", "jendela": "fajar", "kabut": "kabut", "bintang": "bintang", "laut": "laut",
         "fajar": "fajar", "hujan": "kabut", "pagi": "fajar", "malam": "bintang"}

# template tujuan per jenis isi (urutan dirotasi per hari supaya tiap hari berbeda)
CALON = {
    "BUKU": ["DOA", "KETIK", "STICKY", "LILIN", "HPJADUL", "LAYAR", "TOPLES", "ANTIK", "KETIKLILIN", "TOPLESMALAM", "LILINJENDELA"],
    "MEME": ["BOCOR", "WATERCOLOR", "MINIMAL", "LAYAR", "HPJADUL", "LILIN", "WATERCOLORMALAM", "KARTUFOTO"],
    "SKRIP": ["LETTER", "POSTERTEBAL", "LETTERPUTIH", "KACAPATRI", "WATERCOLOR", "MINIMAL"],
    "RELATABLE": ["T", "HPJADUL", "STICKY"],
    "BESAR": ["POSTERTEBAL", "BOCOR", "KARTUFOTO", "LETTER", "ANTIK", "MINIMAL", "WATERCOLOR", "BOTANI"],
    "KUTIPAN": ["ANTIK", "KARTUFOTO", "BOTANI", "WATERCOLORMALAM", "MINIMAL", "BOCOR"],
    "KERTAS": ["KARTUFOTO", "LILIN", "WATERCOLOR", "BOTANI", "LILINJENDELA", "MINIMAL"],
}


def keluarga(nama):
    """Varian satu template dihitung sama (lilin = lilin jendela, ketik = ketik lilin, dst.)."""
    nama = nama.upper()
    for akhiran in ("JENDELA", "MALAM", "LILIN", "PUTIH"):
        if nama.endswith(akhiran) and nama != akhiran:
            return nama[: -len(akhiran)]
    return nama


def tanpa_markup(s):
    return re.sub(r"[\*\[\]_]", "", s)


def ayat_dari(caption):
    pairs = cek_ayat.pairs_from(caption, "c")
    return (pairs[0][0], pairs[0][1].strip(" .")) if pairs else ("", "")


def potong(teks, n):
    teks = bersih(teks)
    if len(teks) <= n:
        return teks
    return teks[:n].rsplit(" ", 1)[0] + "…"


def baris_pendek(teks, lebar, maks):
    """Pecah teks jadi baris <= lebar huruf (untuk papan huruf / poster)."""
    out, cur = [], ""
    for w in bersih(teks).upper().split():
        if len(w) > lebar:
            return None
        if len(cur) + len(w) + (1 if cur else 0) <= lebar:
            cur = f"{cur} {w}".strip()
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    return out if len(out) <= maks else None


def isi_dari(jenis, p):
    """Teks utama + judul dari item lama."""
    if jenis == "BUKU":
        return p["judul"], " ".join(p["baris"])
    if jenis == "MEME":
        return "", p["teks"]
    if jenis == "SKRIP":
        return p.get("dari", ""), p["teks"]
    if jenis == "RELATABLE":
        return p.get("atas", ""), p["teks"]
    if jenis == "KUTIPAN":
        return p.get("sumber", ""), tanpa_markup(p["teks"])
    return "", tanpa_markup(p["teks"])


def adaptasi(target, jenis, p, caption, waktu, i):
    """-> PIL image atau None kalau isi tidak cocok untuk template itu."""
    judul, teks = isi_dari(jenis, p)
    ayat, ref = ayat_dari(caption)
    if not ref and target not in ("T",):
        ref = p.get("ref", "")
    if not ayat and target in ("KETIK", "LILIN", "STICKY", "TOPLES", "ANTIK", "BOCOR", "WATERCOLOR", "KARTUFOTO", "BOTANI",
                               "KACAPATRI", "KETIKLILIN", "TOPLESMALAM", "LILINJENDELA", "WATERCOLORMALAM", "POSTERTEBAL"):
        return None
    tgl = dt.datetime.fromisoformat(waktu)
    hari = f"{HARI[tgl.weekday()]}, {tgl.day} {BULAN[tgl.month]}"
    scene = SCENE.get(p.get("foto", ""), ("fajar", "laut", "kabut", "bintang")[i % 4])
    B = {"ayat": ayat, "ref": ref}
    if target == "DOA":
        kal = bersih(teks).split(", ")
        isi = ", ".join(kal[:-1] + [f"[{kal[-1]}]"]) if len(kal) > 1 else f"[{bersih(teks)}]"
        return gaya_w6.doa_image({"judul": bersih(judul or "Doa hari ini").upper(), "isi": isi}, i)
    if target in ("KETIK", "KETIKLILIN"):
        q = dict(B, tanggal=f"{hari.split(',')[0]} {'malam' if tgl.hour >= 18 else 'pagi' if tgl.hour < 11 else 'siang'}, {tgl.day} Okt",
                 isi=(bersih(judul) + ". " if judul and jenis == "BUKU" else "") + bersih(teks))
        return (gaya_w10.ketiklilin_image if target == "KETIKLILIN" else gaya_w7.ketik_image)(q, i)
    if target in ("LILIN", "LILINJENDELA"):
        return gaya_w8.lilin_image(dict(B, teks=potong(teks, 140)), i, jendela=target == "LILINJENDELA")
    if target == "STICKY":
        kal = [k.strip() for k in re.split(r"(?<=[,.!?])\s+", bersih(teks)) if k.strip()]
        if len(kal) < 3:
            kal = (kal + [bersih(judul) or "Tuhan dekat."] * 3)[:3]
        cat = [potong(kal[0], 60), potong(kal[1], 60), potong(" ".join(kal[2:]), 60)]
        return gaya_w8.sticky_image(dict(B, catatan=cat), i)
    if target == "HPJADUL":
        pengirim = {"BUKU": "Doa", "RELATABLE": bersih(judul)[:16] or "Teman", "MEME": "Catatan doa"}.get(jenis, "Pengingat")
        return gaya_w11.hpjadul_image(dict(B, pengirim=pengirim, pesan=potong(teks, 140)), i)
    if target == "LAYAR":
        return gaya_w6.layar_image({"jam": waktu[11:16], "hari": hari, "pengirim": "Doa" if jenis == "BUKU" else "Pengingat",
                                    "pesan": potong(teks, 130), "ref": ref, "foto": scene if scene in ("fajar", "laut") else "fajar"}, i)
    if target in ("TOPLES", "TOPLESMALAM"):
        return gaya_w10.toples_image(dict(B, label=potong(judul or "toples doa", 20).lower(), catatan=potong(teks, 90)), i, malam=target == "TOPLESMALAM")
    if target == "ANTIK":
        return gaya_w13.antik_image(dict(B, atas=potong(judul or "Pengingat", 24), judul=potong(teks, 90)), i)
    if target == "BOCOR":
        kata = [w for w in bersih(teks).split() if len(w) > 3]
        tebal = " ".join(bersih(teks).split()[-3:]) if len(kata) < 2 else kata[len(kata) // 2]
        return gaya_w13.bocor_image(dict(B, teks=potong(teks, 120), tebal=tebal, foto=scene), i)
    if target in ("WATERCOLOR", "WATERCOLORMALAM"):
        return gaya_w12.watercolor_image(dict(B, teks=potong(teks, 100)), i, malam=target == "WATERCOLORMALAM")
    if target == "MINIMAL":
        return gaya_w6.minimal_image({"teks": bersih(teks).lower() if jenis != "KUTIPAN" else bersih(teks)}, i)
    if target in ("LETTER", "LETTERPUTIH"):
        bar = baris_pendek(teks, 16, 4)
        if not bar:
            return None
        if jenis == "SKRIP" and judul and len(bar) < 5:
            bar.append(bersih(judul).upper().replace("—", "-")[:16])
        return gaya_w8.letter_image({"teks": "\n".join(bar), "ref": ref or "", "ayat": ayat}, i, putih=target == "LETTERPUTIH")
    if target == "POSTERTEBAL":
        bar = baris_pendek(teks, 12, 4)
        if not bar:
            return None
        kecil = (bersih(judul) + "  ·  " if jenis == "SKRIP" and judul else "") + "Diam dan percaya."
        return gaya_w13.postertebal_image(dict(B, teks="\n".join(bar), kecil=kecil, warna=("kuning", "biru", "merah", "hijau")[i % 4]), i)
    if target == "KACAPATRI":
        return gaya_w11.kacapatri_image(dict(B, judul=potong(teks, 40), motif=("salib", "bintang", "merpati", "lilin")[i % 4]), i)
    if target == "KARTUFOTO":
        kata = bersih(teks).split()
        if len(kata) > 9:
            return None
        k = max(range(len(kata)), key=lambda j: len(kata[j].strip(".,!?")))
        kata[k] = f"*{kata[k].strip('.,!?')}*"
        return gaya_w13.kartufoto_image(dict(B, judul=" ".join(kata), foto=scene), i)
    if target == "BOTANI":
        return gaya_w13.botani_image(dict(B, judul=potong(judul or teks, 24)), i)
    return None


def remix(items):
    posted = set(json.loads((ROOT / "state/posted.json").read_text()))
    mods = {m: importlib.import_module(f"konten.{m}") for m in MODS if (ROOT / f"konten/{m}.py").exists()}
    per_hari = {}
    for it in items:
        if it["akun"] != "tenang" or it["id"].startswith("story"):
            continue
        d = it["waktu"][:10]
        if MULAI <= d <= SELESAI:
            per_hari.setdefault(d, []).append(it)
    for n_hari, (d, daftar) in enumerate(sorted(per_hari.items())):
        daftar.sort(key=lambda x: x["waktu"])
        dipakai, kandidat = set(), []
        for it in daftar:
            mod, hari, slot = it["id"].rsplit("-", 2)
            f0 = it["files"][0]
            jenis = None
            if mod in mods and not f0.endswith(".mp4") and it["id"] not in posted:
                fmt, idx = mods[mod].JADWAL[int(hari)][slot]
                nama = KODE.get(fmt, fmt)
                if nama in CALON and len(it["files"]) == 1:
                    jenis, p = nama, getattr(mods[mod], nama)[idx]
            if jenis:
                kandidat.append((it, jenis, p))
            else:  # template yang dipertahankan (carousel, Reels, komik, atau yang sudah tayang)
                dipakai.add(re.sub(r"\d+(_\d+)?\.(jpg|mp4)$", "", f0.split("/")[-1]))
        for k, (it, jenis, p) in enumerate(kandidat):
            calon = CALON[jenis]
            geser = (n_hari * 3 + k) % len(calon)
            for target in calon[geser:] + calon[:geser]:
                if keluarga(target) in {keluarga(x) for x in dipakai}:
                    continue
                if target == "T":  # relatable boleh tetap kalau belum ada di hari itu
                    if "relatable" in dipakai:
                        continue
                    dipakai.add("relatable")
                    break
                img = adaptasi(target, jenis, p, it["caption"], it["waktu"], n_hari * 12 + k)
                if img is None:
                    continue
                it["files"] = [save(img, f"tenang_remix/{it['id']}.jpg")]
                dipakai.add(target)
                break
    return items


if __name__ == "__main__":
    import render
    render.build_schedule.__globals__  # noqa: B018  (pastikan modul termuat)
    print("Jalankan lewat render.py")
