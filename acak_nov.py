"""Acak urutan jam post Tenang 1-28 November (minggu 6-9) supaya grid Instagram tidak membentuk kolom yang sama tiap hari.

Minggu 6-9 memakai 12 template yang sama dengan urutan sama setiap hari; karena 12 post = 4 baris x 3 kolom,
tiap template selalu jatuh di kolom yang sama. Di sini jam tayangnya diputar di dalam kelompok waktu yang setara:
  pagi  : pagi 06:00, pagi3 07:30, pagi2 09:00, siang0 10:30  -> diputar (hari % 4)
  siang : siang 12:00 <-> sore2 16:30                          -> ditukar di hari ganjil (kecuali minggu 8: menu makan siang)
  malam : petang 18:00, malam 21:00, larut 22:30              -> diputar (hari % 3)
Reels (siang2, malam0) dan hitung mundur (sore) tetap. Gambar yang menampilkan jam (layar kunci, jam tangan,
catatan, struk, pop-up) digambar ulang dengan jam barunya. Isi dan caption tidak berubah.

Dipanggil dari render.build_schedule: items = acak_nov.acak(items)
"""
import importlib
import json

import config
import gaya_w6
import gaya_w7
import gaya_w9
from render import ROOT, save

MODS = {"tenang_w6": "tenang_w6", "tenang_w7": "tenang_w7", "tenang_w8": "tenang_w8", "tenang_w9": "tenang_w9"}
PAGI = ["pagi", "pagi3", "pagi2", "siang0"]
SIANG = ["siang", "sore2"]
MALAM = ["petang", "malam", "larut"]


def jam(slot):
    return config.AKUN["tenang"]["jam"][slot]


def gambar_ulang(mod, fmt, idx, p, slot_baru):
    """Template yang menampilkan jam: gambar ulang dengan jam slot barunya. -> path relatif atau None."""
    j = jam(slot_baru)
    if fmt == "LAYAR":
        return save(gaya_w6.layar_image(dict(p, jam=j), idx), f"{mod}/layar{idx + 1}.jpg")
    if fmt == "CATATAN":
        return save(gaya_w7.catatan_image(dict(p, _jam=j.replace(":", ".")), idx), f"{mod}/catatan{idx + 1}.jpg")
    if fmt == "STRUK":
        return save(gaya_w7.struk_image(dict(p, _jam=j), idx), f"{mod}/struk{idx + 1}.jpg")
    if fmt == "POPUP":
        return save(gaya_w7.popup_image(dict(p, _jam=j.replace(":", ".")), idx), f"{mod}/popup{idx + 1}.jpg")
    if fmt == "JAM":
        return save(gaya_w9.jam_image(dict(p, _jam=j.replace(":", ".")), idx), f"{mod}/jam{idx + 1}.jpg")
    return None


def acak(items):
    posted = set(json.loads((ROOT / "state/posted.json").read_text()))
    mods = {m: importlib.import_module(f"konten.{m}") for m in MODS if (ROOT / f"konten/{m}.py").exists()}
    for it in items:
        if it["akun"] != "tenang" or it["id"].startswith("story") or it["id"] in posted:
            continue
        mod, hari, slot = it["id"].rsplit("-", 2)
        if mod not in mods:
            continue
        d = int(hari)
        baru = slot
        if slot in PAGI:
            baru = PAGI[(PAGI.index(slot) + d) % len(PAGI)]
        elif slot in SIANG and d % 2 == 1 and mod != "tenang_w8":
            baru = SIANG[1 - SIANG.index(slot)]
        elif slot in MALAM:
            baru = MALAM[(MALAM.index(slot) + d) % len(MALAM)]
        if baru == slot:
            continue
        it["waktu"] = it["waktu"][:11] + jam(baru) + it["waktu"][16:]
        fmt, idx = mods[mod].JADWAL[d][slot]
        if fmt in ("LAYAR", "CATATAN", "STRUK", "POPUP", "JAM"):
            rel = gambar_ulang(mod, fmt, idx, getattr(mods[mod], fmt)[idx], baru)
            if rel:
                it["files"] = [rel]
    return items
