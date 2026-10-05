"""Konten gaya child.ink dari folder Eli (Eli kecil + Yesus) untuk akun Tenang, 3x seminggu.
Dirender ulang dengan handle @diam.dan.percaya ke output/tenang_eli/ (gambar & carousel) dan output/reels/tenang_eli/.

  render_item(("pot",))          -> carousel cerita "Pot Eli" (5 video slide)
  render_item(("payung",))       -> Reels "Payung"
  render_item(("edukasi", i))    -> carousel "Eli Belajar" ke-i dari konten/eli_variasi.py
  render_item(("saran", i))      -> carousel "Tips dari Eli" ke-i
"""
import re
import shutil

import cerita
import config
import render
from render import OUT

FOLDER = "tenang_eli"


def _tanpa_tag(caption):
    """Buang tagar & sebutan akun Eli; render.py menambahkan tagar akun Tenang."""
    return re.split(r"\n\.\n\.\n", caption)[0].strip()


class handle_tenang:
    """Sementara pakai handle Tenang di semua gambar Eli/cerita."""
    def __enter__(self):
        self.old = config.AKUN["eli"]["handle"], cerita.HANDLE
        config.AKUN["eli"]["handle"] = config.AKUN["tenang"]["handle"]
        cerita.HANDLE = "@" + config.AKUN["tenang"]["handle"].upper()

    def __exit__(self, *a):
        config.AKUN["eli"]["handle"], cerita.HANDLE = self.old


def render_item(item):
    """-> (files relatif ke output/, caption tanpa tagar)"""
    kind = item[0]
    (OUT / FOLDER).mkdir(parents=True, exist_ok=True)
    if kind == "pot":
        files = [f"{FOLDER}/pot_{n}.mp4" for n in range(1, 6)]
        if not all((OUT / f).exists() for f in files):
            with handle_tenang():
                cerita.carousel_pot(video=True)
            for n, f in enumerate(files, 1):
                shutil.copy(cerita.OUT / f"carousel_pot_{n}.mp4", OUT / f)
        return files, _tanpa_tag(cerita.CAPTION_POT)
    if kind == "payung":
        rel = f"reels/{FOLDER}/payung.mp4"
        if not (OUT / rel).exists():
            import musik
            with handle_tenang():
                src = cerita.reel_payung()
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src if str(src).startswith("/") else cerita.OUT / "reel_payung.mp4", OUT / rel)
            wav, _ = musik.lagu_unik(rel, musik.durasi(OUT / rel) + 1, set())
            musik.pasang(rel, str(wav))
        return [rel], _tanpa_tag((cerita.OUT / "reel_payung_caption.txt").read_text())
    from konten import eli_variasi as ev
    i = item[1]
    with handle_tenang():
        if kind == "edukasi":
            return render.eli_edukasi(ev.EDUKASI[i], i, FOLDER), ev.EDUKASI[i]["caption"]
        return render.eli_saran(ev.SARAN[i], i, FOLDER), ev.SARAN[i]["caption"]
