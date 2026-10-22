"""Akun Tenang - minggu 17 (konten/tenang_w17.py), 17 - 23 Jan 2027: Yesus memanggil murid-murid; mengikut, panggilan,
pekerjaan sehari-hari. 36 gaya diacak tiap hari + komik Eli.
BARU (benda kerja & benda laut sehari-hari, isinya buatan sendiri):
       JARING (jala ikan berpelampung di air danau yang dalam), PERAHU (diagram melipat perahu kertas 6 langkah),
       BENDERA (bendera isyarat Kode Isyarat Internasional mengeja kata, mis. IKUT), PERKAKAS (papan bayangan perkakas
       tukang kayu, satu alat "sedang dipakai"), PLANG (papan seng tulisan tangan di pinggir jalan),
       CONGKLAK (papan congklak, menabur satu biji demi satu), ALUR (diagram alur murid tulisan tangan di kertas grafik),
       LOWONGAN (selebaran "DICARI" dengan sobekan nomor), UPAH (amplop upah kertas kraft, semua dibayar sama),
       BEKAL (bekal lima roti dua ikan dilihat dari atas),
       DOMINO (Reel domino bernama berjatuhan sampai "kamu"), RADIO (Reel radio mencari frekuensi di tengah gangguan).
LAMA : VENN, PERJALANAN, WATERCOLOR, KOPI, BOTANI, ARTIKEL, KARTUFOTO, KATAKUNCI, ULASAN, TITIK, JAMPASIR, NAPAS.
MIX  : STICKYKAYU, RESEPKAYU, TELEGRAMKAYU, PHOTOBOOTHKAYU (papan kayu meja tukang kayu / lambung perahu + serbuk gergaji),
       POLAROIDDANAU, TIKETDANAU, BALONDANAU, FLIPDANAU, MAJALAHDANAU (danau Galilea subuh: air biru-abu, kabut, bukit),
       KAMUSSENJA, KETIKSENJA, EMAILSENJA (efek cahaya keemasan sore + vinyet lembut).
KOMIK = komik Eli & Yesus.

  python3 gaya_w17.py [reels]
"""
import datetime as dt
import importlib
import math
import re
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cerita
import config
import gaya_w5
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import gaya_w11
import gaya_w12
import gaya_w13
import gaya_w14
import render
from gaya_w6 import hn
from gaya_w7 import bayangan, bersih, comp, ease, fade, gradasi, sprite, tanpa_kutip
from gaya_w11 import konteks
from gaya_w14 import kilau, kurva
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w17"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2027, 1, 17)
SUP = "/System/Library/Fonts/Supplemental/"
SYS = "/System/Library/Fonts/"

# Skema konten gaya BARU (batas = jumlah karakter maksimum). Semua item juga punya ayat, ref, caption.
SKEMA = {
    "JARING": "judul ≤24, lokasi ≤26, ayat ≤130",
    "PERAHU": "judul ≤20, langkah[6] ≤18, penutup ≤36, ayat ≤150",
    "BENDERA": "kata 3-6 huruf A-Z (dieja dengan bendera Kode Isyarat Internasional), arti ≤24, ayat ≤140",
    "PERKAKAS": "judul ≤20, alat[5-6] ≤10 (nama alat: palu, gergaji, pahat, siku, serut, palu kayu, obeng, meteran, "
                "waterpas, kikir, kuas, bor, tang), kosong = indeks alat yang sedang dipakai, label_kosong ≤14, ayat ≤170",
    "PLANG": "judul ≤14, baris[2] ≤28, arah ≤10, ayat ≤170",
    "CONGKLAK": "judul ≤24, isi[16] angka 0-9 (7 lubang baris atas kiri→kanan, 7 lubang baris bawah kiri→kanan, "
                "lumbung kiri, lumbung kanan), ayat ≤170",
    "ALUR": "mulai ≤30, tanya ≤12, ya[2] ≤22, tidak ≤22, akhir ≤16, ayat ≤160",
    "LOWONGAN": "judul ≤10, sub ≤26, syarat[4] ≤32 ('Label: isi'), tab ≤18, robek = daftar indeks tab 0-7 yang sudah "
                "disobek (satu tab di sebelahnya otomatis setengah sobek), ayat ≤170",
    "UPAH": "judul ≤30, baris[5] = [jam ≤5, nama ≤12, upah ≤10] (baris terakhir dicap), cap ≤8, ayat ≤180",
    "BEKAL": "catatan ≤24, baris ≤56, ayat ≤140",
    "DOMINO": "nama[10-14] ≤10 (yang terakhir = domino merah, mis. 'kamu'), judul ≤30, ayat ≤160 (Reels)",
    "RADIO": "frekuensi ≤6 (mis. '103.10', 88-108), gangguan[4] ≤12, lcd ≤18, ayat ≤150 (Reels)",
}


# ================= HURUF & ALAT BANTU =================

@lru_cache(maxsize=None)
def fnt(path, size, idx=0):
    return ImageFont.truetype(path if path.startswith("/") else SUP + path, max(8, int(round(size))), index=idx)


def din(s):
    return fnt("DIN Condensed Bold.ttf", s)


def futura(s, idx=0):  # 0 Medium, 2 Bold, 4 Condensed ExtraBold
    return fnt("Futura.ttc", s, idx)


def iowan(s, idx=0):  # 0 Roman, 1 Bold, 2 Italic, 3 Bold Italic
    return fnt("Iowan Old Style.ttc", s, idx)


def charter(s, idx=0):  # 0 Roman, 1 Italic, 3 Bold, 5 Black
    return fnt("Charter.ttc", s, idx)


def helv(s, idx=0):  # 0 Regular, 1 Bold, 7 Light, 10 Medium
    return fnt(SYS + "HelveticaNeue.ttc", s, idx)


def avenir(s, idx=0):  # 0 Bold, 2 Demi, 5 Medium, 7 Regular, 8 Heavy
    return fnt(SYS + "Avenir Next.ttc", s, idx)


def coret(s):
    return fnt(SYS + "Noteworthy.ttc", s, 1)


def menlo(s, idx=0):
    return fnt(SYS + "Menlo.ttc", s, idx)


def kurir(s, tebal=False):
    return fnt("Courier New Bold.ttf" if tebal else "Courier New.ttf", s)


def mesin(s, idx=0):  # American Typewriter: 0 Regular, 2 Bold, 3 Semibold
    return fnt("AmericanTypewriter.ttc", s, idx)


def bradley(s):
    return fnt("Bradley Hand Bold.ttf", s)


def rockwell(s, idx=2):
    return fnt("Rockwell.ttc", s, idx)


def impact(s):
    return fnt("Impact.ttf", s)


def ablack(s):
    return fnt("Arial Black.ttf", s)


def kuas(s):
    return fnt("SignPainter.ttc", s, 1)


@lru_cache(maxsize=None)
def rounded(s, berat="Bold"):
    f = ImageFont.truetype(SYS + "SFNSRounded.ttf", int(s))
    f.set_variation_by_name(berat)
    return f


def kredit(d, xy, warna, anchor="ma", size=22, font=None):
    d.text(xy, "@" + HANDLE, font=font or helv(size, 10), fill=warna, anchor=anchor)


def muat(d, teks, font_fn, maxw, start, stop=12):
    """Huruf terbesar (≤ start) supaya teks satu baris ≤ maxw."""
    size = start
    while size > stop and d.textlength(teks, font=font_fn(size)) > maxw:
        size -= 1
    return font_fn(size)


def susun(d, teks, font_fn, maxw, maxh, start, stop, lh=1.3, maks_baris=None):
    """Seperti pas(), tapi setiap baris dijamin ≤ maxw (kata panjang ikut mengecilkan huruf)."""
    for size in range(int(start), int(stop) - 1, -1):
        f = font_fn(size)
        lines = wrap(d, teks, f, maxw)
        if (len(lines) * size * lh <= maxh and all(d.textlength(ln, font=f) <= maxw for ln in lines)
                and (maks_baris is None or len(lines) <= maks_baris)):
            return f, lines, size
    return f, lines, size


def seimbang(d, lines, f):
    """Dua baris dibuat kira-kira sama panjang (hindari satu kata yatim di baris kedua)."""
    if len(lines) != 2:
        return lines
    kata = " ".join(lines).split()
    terbaik = min(range(1, len(kata)), key=lambda k: max(d.textlength(" ".join(kata[:k]), font=f), d.textlength(" ".join(kata[k:]), font=f)))
    return [" ".join(kata[:terbaik]), " ".join(kata[terbaik:])]


def renggang(d, xy, teks, f, fill, jarak=2.0, anchor="la"):
    """Teks dengan spasi huruf. anchor: la / ma / ra (kiri / tengah / kanan)."""
    lebar = sum(d.textlength(c, font=f) for c in teks) + jarak * max(0, len(teks) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= lebar / 2
    elif anchor[0] == "r":
        x -= lebar
    for c in teks:
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(c, font=f) + jarak
    return lebar


def lebar_renggang(d, teks, f, jarak):
    return sum(d.textlength(c, font=f) for c in teks) + jarak * max(0, len(teks) - 1)


def ayat_blok(d, p, x0, x1, y0, y1, font_fn, warna, warna_ref, ref_font, start=36, stop=22, lh=1.36, rata="tengah",
              vtengah=True, ref_gap=14, ref_teks=None):
    """Ayat + referensi di kotak (x0..x1, y0..y1). Mengembalikan y bawah."""
    teks = bersih(p["ayat"])
    rh = ref_font.size * 1.15 + ref_gap
    f, lines, size = susun(d, teks, font_fn, x1 - x0, y1 - y0 - rh, start, stop, lh)
    tinggi = len(lines) * size * lh + rh
    y = y0 + (max(0, (y1 - y0 - tinggi) / 2) if vtengah else 0)
    x, anc = ((x0 + x1) / 2, "ma") if rata == "tengah" else (x0, "la")
    for ln in lines:
        d.text((x, y), ln, font=f, fill=warna, anchor=anc)
        y += size * lh
    d.text((x, y + ref_gap), ref_teks or p["ref"], font=ref_font, fill=warna_ref, anchor=anc)
    return y + rh


def teks_bayang(img, xy, teks, f, fill, anchor="ma", blur=4, kuat=170, geser=(0, 2)):
    """Teks kecil dengan bayang lembut supaya terbaca di latar ramai."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((xy[0] + geser[0], xy[1] + geser[1]), teks, font=f, fill=(0, 0, 0, kuat), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, teks, font=f, fill=fill, anchor=anchor)


def potong(pts, L):
    """Polyline tanpa L piksel terakhir."""
    out = [tuple(q) for q in pts]
    while len(out) >= 2 and L > 0:
        (ax, ay), (bx, by) = out[-2], out[-1]
        seg = math.hypot(bx - ax, by - ay)
        if seg > L:
            t = (seg - L) / seg
            out[-1] = (ax + (bx - ax) * t, ay + (by - ay) * t)
            return out
        L -= seg
        out.pop()
    return out


def kepala(d, tip, ang, L, col, lebar=0.95):
    """Kepala panah segitiga (poligon), ujung di tip, menghadap sudut ang."""
    bx, by = tip[0] - math.cos(ang) * L, tip[1] - math.sin(ang) * L
    hx, hy = -math.sin(ang) * L * lebar / 2, math.cos(ang) * L * lebar / 2
    d.polygon([tuple(tip), (bx + hx, by + hy), (bx - hx, by - hy)], fill=col)


def putus(d, pts, col, w, pola=(14, 9)):
    """Garis putus-putus sepanjang polyline. pola = panjang nyala/mati bergantian (mis. (12, 6, 2, 6) = strip-titik)."""
    k, sisa = 0, pola[0]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        seg = math.hypot(bx - ax, by - ay)
        pos = 0.0
        while seg > 0 and pos < seg - 1e-6:
            step = min(sisa, seg - pos)
            if k % 2 == 0:
                t0, t1 = pos / seg, (pos + step) / seg
                d.line((ax + (bx - ax) * t0, ay + (by - ay) * t0, ax + (bx - ax) * t1, ay + (by - ay) * t1), fill=col, width=int(w))
            pos += step
            sisa -= step
            if sisa <= 1e-6:
                k = (k + 1) % len(pola)
                sisa = pola[k]


def panah(d, pts, col, w, L=None, pola=None, lebar=0.95):
    """Panah polyline: badan (utuh atau putus-putus) + kepala poligon."""
    L = L or max(10, w * 4.2)
    tip = pts[-1]
    back = potong(pts, L)[-1]
    ang = math.atan2(tip[1] - back[1], tip[0] - back[0])
    body = potong(pts, L * 0.75)
    if len(body) >= 2:
        if pola:
            putus(d, body, col, w, pola)
        else:
            d.line(body, fill=col, width=int(w), joint="curve")
    kepala(d, tip, ang, L, col, lebar)


def campur(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def lapis_warna(img, mask, col, alpha=1.0, pos=(0, 0)):
    """Tempel warna rata memakai mask L."""
    lay = Image.new("RGBA", mask.size, tuple(col[:3]) + (255,))
    lay.putalpha(mask.point(lambda v: int(v * alpha)) if alpha < 1 else mask)
    comp(img, lay, pos)


def kertas_tekstur(w, h, warna, seed, kuat=0.04, serat=0.0):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (1 - kuat + 2 * kuat * render.fbm2d(h, w, rng, ((3, 1.0), (24, 0.5), (120, 0.3))))[..., None]
    if serat:
        n = rng.random((h, max(2, w // 3))).astype(np.float32)
        n = np.asarray(Image.fromarray(n).resize((w, h), Image.BICUBIC))
        a *= (1 - serat / 2 + serat * n)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# ================= LATAR & EFEK MINGGU INI =================

def kayu_latar(w, h, seed):
    """Papan kayu meja kerja tukang kayu / lambung perahu: bilah mendatar, serat hangat, mata kayu, paku, serbuk gergaji."""
    rng = np.random.default_rng(seed)
    arr = np.zeros((h, w, 3), np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    warna = [(166, 110, 66), (150, 98, 58), (176, 120, 74), (142, 92, 54), (160, 106, 62)]
    y0, k = -int(rng.uniform(0, 120)), 0
    batas = []
    while y0 < h:
        tinggi = int(rng.uniform(150, 230))
        y1 = min(h, y0 + tinggi)
        a, b = max(0, y0), y1
        if b > a:
            sub_y, sub_x = yy[a:b], xx[a:b]
            warp = render.fbm2d(b - a, w, rng, ((2, 1.0), (7, 0.5))) * 46
            fase = (sub_y - y0) * 0.22 + warp
            for _ in range(int(rng.integers(0, 3))):  # mata kayu membelokkan serat
                cx, cy = rng.uniform(0, w), rng.uniform(y0 + 30, y0 + tinggi - 30)
                rx, ry = rng.uniform(40, 90), rng.uniform(14, 26)
                g = np.exp(-(((sub_x - cx) / rx) ** 2 + ((sub_y - cy) / ry) ** 2))
                fase += g * 9
                inti = np.exp(-(((sub_x - cx) / (rx * 0.18)) ** 2 + ((sub_y - cy) / (ry * 0.5)) ** 2))
                fase += inti * 4
            serat = (0.5 + 0.5 * np.sin(fase)) ** 5
            halus = render.fbm2d(b - a, w, rng, ((3, 1.0), (40, 0.4), (200, 0.3)))
            col = np.array(warna[k % len(warna)], np.float32) * rng.uniform(0.94, 1.06)
            arr[a:b] = col * (0.86 + 0.18 * halus[..., None]) * (1 - 0.16 * serat[..., None])
            arr[a:b] *= (1 + 0.05 * np.sin(sub_x / w * math.pi * rng.uniform(1, 3) + rng.uniform(0, 6)))[..., None]
        batas.append(y1)
        y0, k = y1, k + 1
    for yb in batas[:-1]:  # sambungan antar bilah
        if 0 < yb < h:
            arr[max(0, yb - 3):yb] *= 0.42
            arr[yb:min(h, yb + 2)] *= 1.12
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for xb in (w * 0.14, w * 0.86):  # paku di atas balok penyangga
        for yb in [0] + batas[:-1]:
            for dy in (34, -34):
                y = yb + dy
                if (dy > 0 and yb == 0) or 0 < y < h:
                    x = xb + rng.uniform(-6, 6)
                    if y < 6 or y > h - 6:
                        continue
                    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(70, 52, 40, 255))
                    d.ellipse((x - 6, y - 6, x + 5, y + 5), fill=(118, 104, 92, 255))
                    d.ellipse((x - 4, y - 5, x, y - 1), fill=(170, 160, 150, 255))
    # serbuk gergaji di dua sudut + serutan kayu melingkar
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    sudut = [(0, h), (w, h), (0, 0), (w, 0)]
    for cx, cy in [sudut[j] for j in rng.permutation(4)[:2]]:
        for _ in range(int(w * h / 900)):
            r = abs(rng.normal(0, 150))
            a = rng.uniform(0, 2 * math.pi)
            x, y = cx + math.cos(a) * r * 1.4, cy + math.sin(a) * r
            s = rng.uniform(0.8, 2.6)
            ld.ellipse((x - s, y - s * 0.7, x + s, y + s * 0.7), fill=(236, 206, 160, int(rng.uniform(90, 220))))
        for _ in range(2):
            x, y = cx + (1 if cx == 0 else -1) * rng.uniform(40, 150), cy + (-1 if cy == h else 1) * rng.uniform(30, 120)
            r0 = rng.uniform(16, 26)
            pts = [(x + (r0 - t * 2.2) * math.cos(t), y + (r0 - t * 2.2) * 0.62 * math.sin(t)) for t in np.linspace(0, 6.5, 40)]
            ld.line(pts, fill=(226, 190, 134, 230), width=7, joint="curve")
            ld.line(pts, fill=(246, 222, 178, 240), width=3, joint="curve")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    vin = 1 - 0.22 * (((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h / 2) / (h * 0.75)) ** 2)
    a *= vin[..., None]
    return grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.04)


def danau_latar(w, h, seed, horizon=0.42, perahu=True):
    """Danau Galilea subuh: langit pucat (biru tua di zenit), bukit berlapis, kabut tipis, air tenang biru-abu."""
    rng = np.random.default_rng(seed)
    hz = int(h * horizon)
    y = np.arange(h, dtype=np.float32)[:, None]
    t = np.clip(y / max(1, hz), 0, 1)
    langit = np.array([62, 82, 112], np.float32) * (1 - t[..., None] ** 0.9) + np.array([226, 220, 214], np.float32) * t[..., None] ** 0.9
    langit = langit + np.array([18, 6, -6], np.float32) * np.clip((t[..., None] - 0.7) / 0.3, 0, 1)
    tw = np.clip((y - hz) / max(1, h - hz), 0, 1)
    air = np.array([132, 146, 162], np.float32) * (1 - tw[..., None] ** 0.55) + np.array([34, 52, 74], np.float32) * tw[..., None] ** 0.55
    arr = np.where((y < hz)[..., None], langit, air)
    arr = np.broadcast_to(arr, (h, w, 3)).copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sx = w * rng.uniform(0.62, 0.8)
    glow = np.exp(-(((xx - sx) / (w * 0.32)) ** 2 + ((yy - hz) / (h * 0.16)) ** 2))
    arr += (glow * (yy < hz))[..., None] * np.array([40, 22, 4])
    # pantulan cahaya di air: garis-garis mendatar terputus di bawah titik cahaya
    pant = np.exp(-((xx - sx) / (w * 0.07 + (yy - hz).clip(0) * 0.12)) ** 2) * (yy > hz) * np.exp(-(yy - hz).clip(0) / (h * 0.3))
    pita = (np.sin(yy * 0.9 + render.fbm2d(h, w, rng, ((6, 1.0),)) * 12) > 0.35).astype(np.float32)
    arr += (pant * pita)[..., None] * np.array([60, 46, 30])
    # riak: garis terang tipis yang makin renggang ke bawah
    n = render.fbm2d(h, w, rng, ((4, 1.0), (16, 0.5)))
    riak = np.sin((yy - hz).clip(0) ** 0.62 * 7 + n * 6)
    pecah = np.asarray(Image.fromarray(rng.random((max(2, h // 3), 20)).astype(np.float32)).resize((w, h), Image.BICUBIC))
    kilat = (riak > 0.9) * (pecah > 0.58) * (yy > hz + 4)
    arr += kilat[..., None] * np.array([22, 26, 30]) * (1 - tw[..., None] * 0.55)
    arr -= ((riak < -0.92) * (pecah < 0.4) * (yy > hz + 4))[..., None] * np.array([10, 10, 8])
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    # bukit berlapis di seberang danau
    for lap, (col, tinggi, kab) in enumerate((((150, 152, 170), 130, 0.55), ((112, 118, 140), 80, 0.35))):
        xs = np.linspace(-20, w + 20, 80)
        prof = render.fbm2d(2, 80, rng, ((3, 1.0), (9, 0.4)))[0]
        ys = hz - (0.35 + 0.65 * prof) * tinggi * (1.25 if lap == 0 else 1.0)
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([(-20, hz + 1)] + list(zip(xs, ys)) + [(w + 20, hz + 1)], fill=col + (255,))
        img.alpha_composite(lay)
        kabut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kabut)
        for _ in range(7):
            cx, cy = rng.uniform(0, w), hz - rng.uniform(0, tinggi * 0.6)
            rx, ry = rng.uniform(140, 320), rng.uniform(10, 22)
            kd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(236, 230, 226, int(170 * kab)))
        img.alpha_composite(kabut.filter(ImageFilter.GaussianBlur(14)))
    # pantulan bukit (gelap tipis) + kabut di permukaan air
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle((0, hz, w, hz + 26), fill=(96, 104, 126, 120))
    for _ in range(6):
        cx, cy = rng.uniform(0, w), hz + rng.uniform(4, 60)
        rx, ry = rng.uniform(180, 420), rng.uniform(8, 16)
        ld.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(232, 228, 226, 90))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    if perahu:  # perahu nelayan kecil di kejauhan
        px, py = w * rng.uniform(0.16, 0.3), hz + 18
        d.polygon([(px - 34, py), (px + 34, py), (px + 24, py + 9), (px - 26, py + 9)], fill=(40, 46, 62, 255))
        d.line((px - 4, py, px - 4, py - 46), fill=(40, 46, 62, 255), width=3)
        d.polygon([(px - 2, py - 44), (px + 22, py - 6), (px - 2, py - 6)], fill=(70, 76, 94, 255))
        d.line((px - 30, py + 13, px + 30, py + 13), fill=(96, 110, 130), width=2)
    for _ in range(3):  # burung kecil
        bx, by, s = rng.uniform(w * 0.1, w * 0.9), rng.uniform(h * 0.05, hz * 0.6), rng.uniform(7, 12)
        d.line([(bx - s, by - s * 0.3), (bx - s * 0.4, by - s * 0.55), (bx, by)], fill=(70, 80, 100), width=2, joint="curve")
        d.line([(bx, by), (bx + s * 0.4, by - s * 0.55), (bx + s, by - s * 0.3)], fill=(70, 80, 100), width=2, joint="curve")
    return grain(img.convert("RGB"), 0.03)


def senja(img, seed, kuat=1.0):
    """EFEK cahaya keemasan sore (golden hour): sinar hangat rendah dari samping, kilau lembut, vinyet lembut."""
    rng = np.random.default_rng(seed)
    w, h = img.size
    base = np.asarray(img.convert("RGB")).astype(np.float32) / 255
    out = base * np.array([1.03, 0.975, 0.86]) + np.array([0.035, 0.016, 0.0])
    kanan = rng.random() < 0.5
    sx, sy = (1.08 * w if kanan else -0.08 * w), h * rng.uniform(0.18, 0.36)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dist = np.sqrt(((xx - sx) / w) ** 2 + ((yy - sy) / h * 0.8) ** 2)
    sinar = np.exp(-(dist / 0.62) ** 2) * 0.55 * kuat
    pita = np.exp(-(((yy - sy) - (xx - sx) * (0.18 if kanan else -0.18)) / (h * 0.22)) ** 2)  # berkas datar sedikit miring
    sinar += pita * np.exp(-dist / 0.9) * 0.16 * kuat
    col = np.array([1.0, 0.66, 0.30])
    lum0 = base @ np.array([0.299, 0.587, 0.114])
    bobot = (0.12 + 0.88 * np.clip(lum0, 0, 1) ** 1.5)[..., None]  # bagian gelap (tulisan) hampir tidak ikut terangkat
    out = 1 - (1 - out) * (1 - sinar[..., None] * col * bobot)
    lum = out @ np.array([0.299, 0.587, 0.114])
    terang = Image.fromarray((np.clip(lum - 0.78, 0, 1) * 4 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
    out += (np.asarray(terang, np.float32) / 255)[..., None] * np.array([0.10, 0.07, 0.03]) * kuat
    r2 = ((xx - w / 2) / (w * 0.62)) ** 2 + ((yy - h / 2) / (h * 0.62)) ** 2
    vin = np.clip(1 - 0.34 * np.clip(r2 - 0.35, 0, None) ** 1.1, 0.55, 1)
    out = out * vin[..., None] ** np.array([0.9, 1.0, 1.25])
    return grain(Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)), 0.025)


# ================= BARU =================

# ---------- JARING: jala ikan di air dalam ----------

def air_dalam(w, h, seed, atas=(16, 58, 92), bawah=(8, 30, 52)):
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(atas, np.float32) * (1 - y) + np.array(bawah, np.float32) * y
    arr = np.broadcast_to(arr, (h, w, 3)).copy()
    m = Image.new("L", (w // 4, h // 4), 0)
    md = ImageDraw.Draw(m)
    for _ in range(8):  # berkas cahaya dari permukaan
        x = rng.uniform(-0.1, 1.1) * w / 4
        lb = rng.uniform(5, 18)
        mr = rng.uniform(-50, 20)
        md.polygon([(x - lb, 0), (x + lb, 0), (x + mr + lb * 2.4, h / 4), (x + mr - lb * 0.3, h / 4)], fill=int(rng.uniform(50, 120)))
    m = m.filter(ImageFilter.GaussianBlur(7)).resize((w, h), Image.BICUBIC)
    sinar = np.asarray(m, np.float32)[..., None] / 255 * np.clip(1.1 - y * 1.5, 0, 1)
    arr += sinar * np.array([50, 100, 130]) * 0.5
    n = render.fbm2d(h, w, rng, ((7, 1.0), (22, 0.6)))
    caus = np.clip(1 - np.abs(n - 0.5) * 10, 0, 1) ** 2 * np.clip(0.42 - y[..., 0] * 1.1, 0, 1)
    arr += caus[..., None] * np.array([60, 110, 140]) * 0.55
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(150):
        px, py, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(0.6, 1.8)
        d.ellipse((px - r, py - r, px + r, py + r), fill=(170, 210, 235, int(rng.uniform(40, 140))))
    img.alpha_composite(lay)
    return img


def ikan_perak(L, rng):
    """Ikan kecil perak (RGBA), menghadap ke kiri."""
    h = int(L * 0.44)
    k = 3

    def gambar(d, k):
        atas = [(L * (0.03 + 0.72 * t), h * 0.52 - h * 0.40 * math.sin(math.pi * t ** 0.75)) for t in np.linspace(0, 1, 30)]
        bawah = [(L * (0.03 + 0.72 * t), h * 0.52 + h * 0.33 * math.sin(math.pi * t ** 0.75)) for t in np.linspace(1, 0, 30)]
        ekor = [(L * 0.70, h * 0.52), (L * 0.99, h * 0.08), (L * 0.91, h * 0.52), (L * 0.99, h * 0.94)]
        d.polygon([(x * k, y * k) for x, y in ekor], fill=(128, 146, 164, 255))
        sirip = [(L * 0.36, h * 0.16), (L * 0.52, h * 0.0), (L * 0.56, h * 0.16)]
        d.polygon([(x * k, y * k) for x, y in sirip], fill=(120, 138, 156, 255))
        d.polygon([(x * k, y * k) for x, y in atas + bawah], fill=(200, 210, 220, 255))
    spr = sprite(L, h, gambar, k=k)
    a = np.asarray(spr).astype(np.float32)
    yy = np.linspace(0, 1, h)[:, None]
    shade = 0.58 + 0.62 * np.clip(yy * 1.3, 0, 1)
    kil = np.exp(-((yy - 0.42) / 0.08) ** 2) * 0.25
    a[..., :3] = np.clip(a[..., :3] * shade[..., None] + kil[..., None] * 255, 0, 255)
    spr = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(spr)
    d.line([(L * 0.2, h * 0.5), (L * 0.68, h * 0.54)], fill=(150, 166, 182, 255), width=1)
    d.arc((L * 0.13, h * 0.2, L * 0.27, h * 0.84), 300, 60, fill=(120, 136, 150, 255), width=2)
    d.ellipse((L * 0.08, h * 0.36, L * 0.14, h * 0.48), fill=(20, 26, 34, 255))
    d.ellipse((L * 0.095, h * 0.37, L * 0.11, h * 0.40), fill=(255, 255, 255, 255))
    return spr


def jaring_image(p, i):
    rng = np.random.default_rng(17100 + i)
    img = air_dalam(W, H, 17100 + i)
    d = ImageDraw.Draw(img)
    X0 = 80
    lokasi = bersih(p["lokasi"]).upper()
    fl = din(32)
    while lebar_renggang(d, lokasi, fl, 3) > W - 2 * X0 - 60 and fl.size > 18:
        fl = din(fl.size - 1)
    y = 122
    d.line((X0, y + 12, X0 + 38, y + 12), fill=(240, 140, 60), width=4)
    renggang(d, (X0 + 54, y), lokasi, fl, (164, 206, 232), 3)
    y += 56
    f, lines, size = susun(d, bersih(p["judul"]), lambda s: avenir(s, 8), W - 2 * X0, 2 * 72 * 1.06, 72, 46, 1.06)
    lines = seimbang(d, lines, f)
    for ln in lines:
        d.text((X0, y), ln, font=f, fill=(255, 255, 255))
        y += size * 1.06
    y += 26
    f, lines, size = susun(d, bersih(p["ayat"]), charter, W - 2 * X0, 250, 36, 26, 1.42)
    for ln in lines:
        d.text((X0, y), ln, font=f, fill=(222, 236, 246))
        y += size * 1.42
    renggang(d, (X0, y + 16), p["ref"].upper(), din(30), (246, 164, 92), 2)
    teks_bawah = y + 16 + 30
    # jala: tali atas berpelampung, mata jala belah ketupat, melengkung ke bawah
    top = max(teks_bawah + 110, 560)
    var = i % 3
    A = (-70.0, top + (30, -6, 14)[var])
    B = (W + 70.0, top + (-6, 34, 14)[var])
    C = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2 + (34, 30, 48)[var])
    NU, NV = 26, 24
    Ldalam = H - top + 160
    jit = rng.uniform(-3, 3, (NU + 1, NV + 1, 2))
    fase = rng.uniform(0, 6)

    def tali(u):
        return ((1 - u) ** 2 * A[0] + 2 * u * (1 - u) * C[0] + u * u * B[0], (1 - u) ** 2 * A[1] + 2 * u * (1 - u) * C[1] + u * u * B[1])

    pusat = W * (0.5 + (var - 1) * 0.1)

    def simpul(a, b):
        u, v = a / NU, b / NV
        x, y_ = tali(u)
        x += (pusat - x) * 0.4 * v ** 1.5 + 34 * v * math.sin(math.pi * u * 2 + fase)
        y_ += Ldalam * v ** 1.12 + 150 * math.sin(math.pi * u) * v ** 1.3
        if b > 0 and float(a).is_integer() and float(b).is_integer():
            x, y_ = x + jit[int(a), int(b), 0], y_ + jit[int(a), int(b), 1]
        return x, y_
    # ikan dulu (jala menyilang di atasnya)
    n_ikan = int(rng.integers(6, 9))
    for k_ in range(n_ikan):
        u = 0.14 + 0.72 * (k_ + rng.uniform(0.2, 0.8)) / n_ikan
        ty = rng.uniform(max(top + 300, H - 420), H - 190)
        lo, hi = 0.0, 1.0
        for _ in range(30):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if simpul(u * NU, m * NV)[1] < ty else (lo, m)
        x, y_ = simpul(u * NU, lo * NV)
        L = int(rng.uniform(96, 140))
        ik = ikan_perak(L, rng)
        if rng.random() < 0.5:
            ik = ik.transpose(Image.FLIP_LEFT_RIGHT)
        ik = ik.rotate(rng.uniform(-28, 28), expand=True, resample=Image.BICUBIC)
        bayangan(img, ik, (x - ik.width / 2, y_ - ik.height / 2), blur=6, geser=(3, 5), kuat=0.35)
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    seg = []
    for a in range(NU + 1):
        for b in range(NV):
            if (a + b) % 2:
                continue
            for da in (1, -1):
                if 0 <= a + da <= NU:
                    seg.append((simpul(a, b), simpul(a + da, b + 1)))
    for (p0, p1) in seg:
        ld.line((p0[0] * S + 4, p0[1] * S + 6, p1[0] * S + 4, p1[1] * S + 6), fill=(4, 16, 30, 150), width=3 * S)
    for (p0, p1) in seg:
        ld.line((p0[0] * S, p0[1] * S, p1[0] * S, p1[1] * S), fill=(214, 190, 140, 255), width=3 * S)
    for a in range(NU + 1):
        for b in range(1, NV + 1):
            if (a + b) % 2 == 0:
                x, y_ = simpul(a, b)
                ld.ellipse((x * S - 4 * S, y_ * S - 4 * S, x * S + 4 * S, y_ * S + 4 * S), fill=(176, 150, 104, 255))
                ld.ellipse((x * S - 2.4 * S, y_ * S - 3 * S, x * S + 1 * S, y_ * S), fill=(232, 212, 168, 255))
    tp = [tali(u) for u in np.linspace(0, 1, 90)]
    ld.line([(x * S + 4, y_ * S + 8) for x, y_ in tp], fill=(4, 16, 30, 170), width=8 * S, joint="curve")
    ld.line([(x * S, y_ * S) for x, y_ in tp], fill=(204, 178, 126, 255), width=8 * S, joint="curve")
    for u in np.linspace(0, 1, 140):  # pilinan tali
        x, y_ = tali(u)
        ld.line((x * S - 5, y_ * S - 7, x * S + 5, y_ * S + 7), fill=(150, 124, 84, 255), width=3)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # pelampung jingga
    pel = sprite(64, 40, lambda dd, k: (dd.ellipse((2 * k, 2 * k, 62 * k, 38 * k), fill=(240, 120, 40, 255)),
                                         dd.rectangle((28 * k, 2 * k, 36 * k, 38 * k), fill=(250, 236, 214, 255)),
                                         dd.ellipse((10 * k, 7 * k, 30 * k, 16 * k), fill=(255, 196, 140, 255))), k=3)
    n_pel = 9
    for k_ in range(n_pel):
        u = (k_ + 0.5) / n_pel
        x, y_ = tali(u)
        x2, y2 = tali(min(1, u + 0.01))
        ang = math.degrees(math.atan2(y2 - y_, x2 - x))
        sp = pel.rotate(-ang, expand=True, resample=Image.BICUBIC)
        bayangan(img, sp, (x - sp.width / 2, y_ - sp.height / 2 + 2), blur=5, geser=(3, 6), kuat=0.5)
    teks_bayang(img, (W / 2, H - 46), "@" + HANDLE, helv(22, 10), (206, 224, 238), blur=5, kuat=230)
    return img


# ---------- PERAHU: diagram melipat perahu kertas ----------

BIRU_P, BIRU_P2, BIRU_P3 = (150, 200, 235, 255), (118, 176, 222, 255), (196, 226, 246, 255)
PUTIH_P, TINTA_P, MERAH_P = (255, 255, 255, 255), (30, 30, 30, 255), (220, 70, 50, 255)
LEMBAH, GUNUNG = (10, 7), (13, 5, 3, 5)  # lipat lembah: putus-putus; lipat gunung: strip-titik


def _garis_tutup(d, pts, S, w=2.4):
    q = [(x * S, y * S) for x, y in pts]
    d.line(q + [q[0]], fill=TINTA_P, width=int(w * S), joint="curve")


def _poli(d, pts, S, fill, garis=True):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)
    if garis:
        _garis_tutup(d, pts, S)


def _lipat(d, a, b, S, pola=LEMBAH, col=TINTA_P, w=2.0):
    putus(d, [(a[0] * S, a[1] * S), (b[0] * S, b[1] * S)], col, w * S, tuple(v * S for v in pola))


def _panah_lengkung(d, p0, c, p1, S, w=3.0, col=MERAH_P):
    panah(d, [(x * S, y * S) for x, y in kurva(p0, c, p1, 30)], col, w * S, L=14 * S)


KERTAS_P = [(BIRU_P, BIRU_P2, BIRU_P3), ((244, 186, 120, 255), (226, 158, 92, 255), (250, 214, 170, 255)),
            ((160, 206, 170, 255), (128, 182, 142, 255), (200, 230, 206, 255))]


def perahu_langkah(n, w, h, warna=0):
    """Satu sel diagram (RGBA w x h) untuk langkah n (1-6). warna: 0 biru, 1 jingga, 2 hijau (sisi depan kertas)."""
    BIRU_P, BIRU_P2, BIRU_P3 = KERTAS_P[warna % 3]

    def gambar(d, S):
        cx, cy = w / 2, h / 2
        if n == 1:  # kertas tegak, lipat dua (atas ke bawah)
            sh = h * 0.8
            sw = sh / 1.414
            x0, y0 = cx - sw / 2 - 18, cy - sh / 2
            _poli(d, [(x0, y0), (x0 + sw, y0), (x0 + sw, y0 + sh), (x0, y0 + sh)], S, BIRU_P)
            _poli(d, [(x0 + sw - 30, y0 + sh), (x0 + sw, y0 + sh - 30), (x0 + sw, y0 + sh)], S, PUTIH_P)  # sudut tersingkap
            _lipat(d, (x0 - 8, y0 + sh / 2), (x0 + sw + 8, y0 + sh / 2), S)
            _panah_lengkung(d, (x0 + sw * 0.72, y0 + 10), (x0 + sw + 74, y0 + sh * 0.5), (x0 + sw * 0.72, y0 + sh - 12), S)
        elif n in (2, 3):
            rw = w * 0.74
            rh = rw / 1.414
            x0, y0 = cx - rw / 2, cy - rh / 2 + 14
            yb = y0 + rw / 2
            if n == 2:  # lipatan; sudut atas ke garis tengah
                _poli(d, [(x0, y0), (x0 + rw, y0), (x0 + rw, y0 + rh), (x0, y0 + rh)], S, PUTIH_P)
                _lipat(d, (cx, y0 - 10), (cx, y0 + rh + 10), S, GUNUNG, w=1.6)
                _lipat(d, (cx, y0), (x0, yb), S)
                _lipat(d, (cx, y0), (x0 + rw, yb), S)
                _panah_lengkung(d, (x0 + 6, y0 - 6), (x0 + rw * 0.18, y0 - 62), (cx - 14, yb - 26), S)
                _panah_lengkung(d, (x0 + rw - 6, y0 - 6), (x0 + rw * 0.82, y0 - 62), (cx + 14, yb - 26), S)
            else:  # topi: tepi bawah dilipat ke atas
                _poli(d, [(x0, yb), (x0 + rw, yb), (x0 + rw, y0 + rh), (x0, y0 + rh)], S, PUTIH_P)
                _poli(d, [(cx, y0), (x0, yb), (cx, yb)], S, BIRU_P)
                _poli(d, [(cx, y0), (x0 + rw, yb), (cx, yb)], S, BIRU_P2)
                _lipat(d, (x0 - 10, yb - 1), (x0 + rw + 10, yb - 1), S)
                _panah_lengkung(d, (x0 + rw * 0.8, y0 + rh - 4), (x0 + rw + 58, yb + 6), (x0 + rw * 0.8, yb - 34), S)
        elif n in (4, 5):
            hd = min(w, h) * 0.37
            dcx, dcy = cx, cy + 6
            if n == 4:  # buka topi jadi belah ketupat
                tw = hd * 1.5
                putus(d, [((dcx - tw) * S, (dcy + hd * 0.45) * S), (dcx * S, (dcy - hd * 0.95) * S),
                          ((dcx + tw) * S, (dcy + hd * 0.45) * S)], (160, 160, 160, 255), 1.6 * S, (5 * S, 5 * S))
            _poli(d, [(dcx, dcy - hd), (dcx + hd, dcy), (dcx, dcy + hd), (dcx - hd, dcy)], S, BIRU_P)
            if n == 4:
                _poli(d, [(dcx - hd * 0.5, dcy + hd * 0.5), (dcx, dcy), (dcx + hd * 0.5, dcy + hd * 0.5), (dcx, dcy + hd)], S, BIRU_P3)
                d.line(((dcx * S, (dcy - hd) * S), (dcx * S, (dcy + hd) * S)), fill=TINTA_P, width=int(1.6 * S))
                for s_ in (-1, 1):
                    panah(d, [((dcx + s_ * (hd + 58)) * S, dcy * S), ((dcx + s_ * (hd + 12)) * S, dcy * S)], MERAH_P, 3 * S, L=14 * S)
            else:  # ujung bawah ke atas
                _poli(d, [(dcx - hd, dcy), (dcx + hd, dcy), (dcx, dcy + hd)], S, PUTIH_P)
                _lipat(d, (dcx - hd - 10, dcy), (dcx + hd + 10, dcy), S)
                _panah_lengkung(d, (dcx + 8, dcy + hd - 14), (dcx + hd + 30, dcy + 10), (dcx + 12, dcy - hd + 22), S)
        else:  # perahu jadi
            yt = cy + h * 0.06
            lb, sb = w * 0.40, w * 0.2
            yb = yt + h * 0.22
            _poli(d, [(cx, yt - h * 0.42), (cx + sb, yt), (cx - sb, yt)], S, PUTIH_P)
            d.line(((cx * S, (yt - h * 0.42) * S), (cx * S, yt * S)), fill=TINTA_P, width=int(1.5 * S))
            _poli(d, [(cx - lb, yt), (cx + lb, yt), (cx + lb * 0.56, yb), (cx - lb * 0.56, yb)], S, BIRU_P)
            _poli(d, [(cx - lb, yt), (cx - lb * 0.56, yb), (cx - lb * 0.72, yt + 4)], S, BIRU_P2, garis=False)
            _poli(d, [(cx + lb, yt), (cx + lb * 0.56, yb), (cx + lb * 0.72, yt + 4)], S, BIRU_P2, garis=False)
            _garis_tutup(d, [(cx - lb, yt), (cx + lb, yt), (cx + lb * 0.56, yb), (cx - lb * 0.56, yb)], S)
            _lipat(d, (cx - lb * 0.72, yt + 4), (cx - lb * 0.56, yb), S, w=1.4)
            _lipat(d, (cx + lb * 0.72, yt + 4), (cx + lb * 0.56, yb), S, w=1.4)
            for k_ in range(3):
                yy = yb + 12 + k_ * 11
                pts = [((cx - lb * 0.9 + t * lb * 1.8) * S, (yy + 3 * math.sin(t * 14 + k_)) * S) for t in np.linspace(0, 1, 30)]
                d.line(pts, fill=(120, 180, 225, 255), width=int(2 * S), joint="curve")
            for s_ in (-1, 1):
                panah(d, [((cx + s_ * (lb - 30)) * S, (yt - 18) * S), ((cx + s_ * (lb + 14)) * S, (yt - 18) * S)], MERAH_P, 3 * S, L=13 * S)
            kilau(d, (cx + sb + 40) * S, (yt - h * 0.3) * S, 11 * S, (240, 180, 40, 255))
            kilau(d, (cx - sb - 46) * S, (yt - h * 0.22) * S, 7 * S, (240, 180, 40, 255))
    return sprite(w, h, gambar, k=3)


def perahu_image(p, i):
    img = kertas_tekstur(W, H, (250, 250, 248), 17200 + i, 0.015).convert("RGBA")
    d = ImageDraw.Draw(img)
    tinta, abu, merah = (30, 30, 30), (128, 128, 124), (220, 70, 50)
    X0 = 80
    renggang(d, (X0, 66), "PANDUAN LIPAT  ·  6 LANGKAH", futura(22, 0), abu, 3)
    renggang(d, (W - X0, 66), "1 LEMBAR KERTAS", futura(22, 0), abu, 3, anchor="ra")
    f = muat(d, bersih(p["judul"]), lambda s: futura(s, 2), W - 2 * X0, 66, 40)
    d.text((X0, 100), bersih(p["judul"]), font=f, fill=tinta)
    d.line((X0, 190, W - X0, 190), fill=tinta, width=3)
    gap = 30
    cw = (W - 2 * X0 - 2 * gap) / 3
    dh, rowh = 236, 334
    for n in range(6):
        r, c = divmod(n, 3)
        x = X0 + c * (cw + gap)
        y = 212 + r * rowh
        sel = perahu_langkah(n + 1, int(cw), dh, i)
        comp(img, sel, (x, y + 22))
        d = ImageDraw.Draw(img)
        d.text((x + 2, y), str(n + 1), font=futura(42, 2), fill=merah if n == 5 else tinta)
        lab = bersih(p["langkah"][n])
        fl, lines, size = susun(d, lab, lambda s: futura(s, 0), cw - 10, 2 * 30 * 1.15, 27, 18, 1.15, maks_baris=2)
        yy = y + dh + 30
        for ln in lines:
            d.text((x + cw / 2, yy), ln, font=fl, fill=tinta, anchor="ma")
            yy += size * 1.15
        if c < 2:
            d.line((x + cw + gap / 2, y + 8, x + cw + gap / 2, y + rowh - 30), fill=(222, 222, 216), width=2)
    d.line((X0, 212 + rowh - 14, W - X0, 212 + rowh - 14), fill=(222, 222, 216), width=2)
    y = 212 + 2 * rowh
    d.line((X0, y - 6, W - X0, y - 6), fill=tinta, width=3)
    # penutup + keterangan garis
    f, lines, size = susun(d, bersih(p["penutup"]), lambda s: iowan(s, 2), W - 2 * X0, 2 * 46 * 1.15, 46, 30, 1.15)
    lines = seimbang(d, lines, f)
    y += 26
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=tinta, anchor="ma")
        y += size * 1.15
    y += 14
    ayat_blok(d, p, X0 + 20, W - X0 - 20, y, H - 128, charter, (52, 52, 50), merah, futura(26, 2), start=34, stop=24, lh=1.38)
    # legenda lipatan
    ly = H - 86
    putus(d, [(X0, ly), (X0 + 56, ly)], tinta, 2, LEMBAH)
    d.text((X0 + 66, ly), "lipat lembah", font=futura(19, 0), fill=abu, anchor="lm")
    x2 = X0 + 66 + d.textlength("lipat lembah", font=futura(19, 0)) + 30
    putus(d, [(x2, ly), (x2 + 56, ly)], tinta, 2, GUNUNG)
    d.text((x2 + 66, ly), "lipat gunung", font=futura(19, 0), fill=abu, anchor="lm")
    kredit(d, (W - X0, ly), abu, anchor="rm", size=20)
    return img


# ---------- BENDERA: bendera isyarat Kode Isyarat Internasional ----------

ICS = {"M": (206, 32, 44), "P": (252, 252, 250), "B": (22, 60, 158), "K": (252, 204, 30), "H": (26, 26, 28)}


def pola_bendera(huruf, w, h):
    """Bendera huruf ICS (International Code of Signals) -> daftar (poligon/elips, warna). x: 0 = tiang (hoist)."""
    R, P, B, Y, K = ICS["M"], ICS["P"], ICS["B"], ICS["K"], ICS["H"]

    def kotak(x0, y0, x1, y1, c):
        return ("poly", [(x0 * w, y0 * h), (x1 * w, y0 * h), (x1 * w, y1 * h), (x0 * w, y1 * h)], c)

    def pita(p0, p1, tebal, c):  # pita lurus (untuk silang & salib serong), digambar melebihi tepi
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        nx, ny = -(y1 - y0) / L * tebal / 2, (x1 - x0) / L * tebal / 2
        ex, ey = (x1 - x0) / L * w, (y1 - y0) / L * w
        return ("poly", [(x0 - ex + nx, y0 - ey + ny), (x1 + ex + nx, y1 + ey + ny), (x1 + ex - nx, y1 + ey - ny), (x0 - ex - nx, y0 - ey - ny)], c)
    t = h * 0.2
    if huruf == "Y":  # garis serong kuning-merah arah "/", sudut kiri atas & kanan bawah merah
        out = [kotak(0, 0, 1, 1, Y)]
        for c in range(0, 21, 4):  # pita merah di sekitar u + v = c/10, lebar 2/10
            a0, a1 = (c - 1) / 10, (c + 1) / 10
            out.append(("poly", [((a0 + 2) * w, -2 * h), ((a1 + 2) * w, -2 * h), ((a1 - 2) * w, 2 * h), ((a0 - 2) * w, 2 * h)], R))
        return out
    s = {
        "A": [kotak(0, 0, .5, 1, P), kotak(.5, 0, 1, 1, B)],
        "B": [kotak(0, 0, 1, 1, R)],
        "C": [kotak(0, k / 5, 1, (k + 1) / 5, c) for k, c in enumerate((B, P, R, P, B))],
        "D": [kotak(0, 0, 1, .25, Y), kotak(0, .25, 1, .75, B), kotak(0, .75, 1, 1, Y)],
        "E": [kotak(0, 0, 1, .5, B), kotak(0, .5, 1, 1, R)],
        "F": [kotak(0, 0, 1, 1, P), ("poly", [(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)], R)],
        "G": [kotak(k / 6, 0, (k + 1) / 6, 1, (Y, B)[k % 2]) for k in range(6)],
        "H": [kotak(0, 0, .5, 1, P), kotak(.5, 0, 1, 1, R)],
        "I": [kotak(0, 0, 1, 1, Y), ("ell", (w / 2 - h * .25, h * .25, w / 2 + h * .25, h * .75), K)],
        "J": [kotak(0, 0, 1, 1 / 3, B), kotak(0, 1 / 3, 1, 2 / 3, P), kotak(0, 2 / 3, 1, 1, B)],
        "K": [kotak(0, 0, .5, 1, Y), kotak(.5, 0, 1, 1, B)],
        "L": [kotak(0, 0, .5, .5, Y), kotak(.5, 0, 1, .5, K), kotak(0, .5, .5, 1, K), kotak(.5, .5, 1, 1, Y)],
        "M": [kotak(0, 0, 1, 1, B), pita((0, 0), (w, h), t, P), pita((0, h), (w, 0), t, P)],
        "N": [kotak(c / 4, r / 4, (c + 1) / 4, (r + 1) / 4, (B, P)[(r + c) % 2]) for r in range(4) for c in range(4)],
        "O": [("poly", [(0, 0), (w, 0), (w, h)], R), ("poly", [(0, 0), (0, h), (w, h)], Y)],
        "P": [kotak(0, 0, 1, 1, B), kotak(1 / 3, 1 / 3, 2 / 3, 2 / 3, P)],
        "Q": [kotak(0, 0, 1, 1, Y)],
        "R": [kotak(0, 0, 1, 1, R), kotak(0, .4, 1, .6, Y), ("poly", [(w / 2 - t / 2, 0), (w / 2 + t / 2, 0), (w / 2 + t / 2, h), (w / 2 - t / 2, h)], Y)],
        "S": [kotak(0, 0, 1, 1, P), kotak(1 / 3, 1 / 3, 2 / 3, 2 / 3, B)],
        "T": [kotak(0, 0, 1 / 3, 1, R), kotak(1 / 3, 0, 2 / 3, 1, P), kotak(2 / 3, 0, 1, 1, B)],
        "U": [kotak(0, 0, .5, .5, R), kotak(.5, 0, 1, .5, P), kotak(0, .5, .5, 1, P), kotak(.5, .5, 1, 1, R)],
        "V": [kotak(0, 0, 1, 1, P), pita((0, 0), (w, h), t, R), pita((0, h), (w, 0), t, R)],
        "W": [kotak(0, 0, 1, 1, B), kotak(1 / 6, 1 / 6, 5 / 6, 5 / 6, P), kotak(2 / 6, 2 / 6, 4 / 6, 4 / 6, R)],
        "X": [kotak(0, 0, 1, 1, P), kotak(0, .4, 1, .6, B), ("poly", [(w / 2 - t / 2, 0), (w / 2 + t / 2, 0), (w / 2 + t / 2, h), (w / 2 - t / 2, h)], B)],
        "Z": [("poly", [(0, 0), (w, 0), (w / 2, h / 2)], Y), ("poly", [(w, 0), (w, h), (w / 2, h / 2)], B),
              ("poly", [(0, h), (w, h), (w / 2, h / 2)], R), ("poly", [(0, 0), (0, h), (w / 2, h / 2)], K)],
    }
    return s[huruf]


def bendera_sprite(huruf, fw, fh, k=3):
    """Sprite bendera datar (RGBA). A dan B berbentuk ekor walet."""
    big = Image.new("RGBA", (fw * k, fh * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for jenis, geo, col in pola_bendera(huruf, fw * k, fh * k):
        if jenis == "poly":
            d.polygon(geo, fill=col + (255,))
        else:
            d.ellipse(geo, fill=col + (255,))
    mask = Image.new("L", big.size, 0)
    md = ImageDraw.Draw(mask)
    W_, H_ = fw * k, fh * k
    if huruf in "AB":
        md.polygon([(0, 0), (W_, 0), (W_ * 0.74, H_ / 2), (W_, H_), (0, H_)], fill=255)
    else:
        md.rectangle((0, 0, W_, H_), fill=255)
    big.putalpha(mask)
    return big.resize((fw, fh), Image.LANCZOS)


def kibar(spr, fase, amp=7.0, lam=46.0):
    """Bendera berkibar: tiap kolom digeser naik-turun (makin jauh dari tiang makin besar) + bayangan lipatan."""
    a = np.asarray(spr).astype(np.float32)
    h, w = a.shape[:2]
    pad = int(amp * 2 + 4)
    out = np.zeros((h + 2 * pad, w, 4), np.float32)
    for x in range(w):
        u = x / max(1, w - 1)
        dy = amp * (u ** 0.9) * math.sin(x / lam * 2 + fase)
        y0 = pad + dy
        iy = int(math.floor(y0))
        fr = y0 - iy
        col = a[:, x, :]
        sh = 1 - 0.13 * math.cos(x / lam * 2 + fase) * (0.3 + 0.7 * u)
        col = col.copy()
        col[:, :3] *= sh
        out[iy:iy + h, x, :] += col * (1 - fr)
        out[iy + 1:iy + 1 + h, x, :] += col * fr
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), pad


def bendera_image(p, i):
    rng = np.random.default_rng(17300 + i)
    img = gradasi(W, H, (170, 214, 240), (236, 246, 252)).convert("RGBA")
    awan = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    ad = ImageDraw.Draw(awan)
    for _ in range(5):
        cx, cy = rng.uniform(-50, W + 50), rng.uniform(0.04, 0.7) * H
        for _ in range(6):
            rx, ry = rng.uniform(70, 160), rng.uniform(26, 50)
            x, y = cx + rng.uniform(-140, 140), cy + rng.uniform(-20, 20)
            ad.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(255, 255, 255, 110))
    img.alpha_composite(awan.filter(ImageFilter.GaussianBlur(22)))
    img = grain(img.convert("RGB"), 0.025).convert("RGBA")
    d = ImageDraw.Draw(img)
    navy = (24, 44, 86)
    renggang(d, (W / 2, 70), "KODE ISYARAT INTERNASIONAL", avenir(24, 2), (60, 96, 140), 4, anchor="ma")
    for _ in range(3):  # camar
        bx, by, s_ = rng.uniform(W * 0.55, W * 0.9), rng.uniform(120, 170), rng.uniform(10, 16)
        d.line([(bx - s_, by - s_ * 0.2), (bx - s_ * 0.45, by - s_ * 0.6), (bx, by)], fill=(70, 96, 130), width=3, joint="curve")
        d.line([(bx, by), (bx + s_ * 0.45, by - s_ * 0.6), (bx + s_, by - s_ * 0.2)], fill=(70, 96, 130), width=3, joint="curve")
    kata = re.sub("[^A-Z]", "", bersih(p["kata"]).upper())[:6] or "IKUT"
    n = len(kata)
    gap = 34 if n <= 4 else 20
    fw = int(min(200, (W - 2 * 64 - (n - 1) * gap) / n))
    fh = int(fw / 1.2)
    x_start = (W - (n * fw + (n - 1) * gap)) / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # semua isi digambar di sini lalu digeser supaya seimbang
    A, B = (-40.0, 40.0), (W + 40.0, 126.0)
    C = (W / 2, 144.0)

    def tali(u):
        return ((1 - u) ** 2 * A[0] + 2 * u * (1 - u) * C[0] + u * u * B[0], (1 - u) ** 2 * A[1] + 2 * u * (1 - u) * C[1] + u * u * B[1])

    def tali_y(x):
        lo, hi = 0.0, 1.0
        for _ in range(30):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if tali(m)[0] < x else (lo, m)
        return tali(lo)[1]
    tali_col = (120, 100, 80)
    ld = ImageDraw.Draw(lay)
    ld.line([tali(u) for u in np.linspace(0, 1, 80)], fill=tali_col + (255,), width=4, joint="curve")
    y_huruf = 0
    posisi = []
    for k, hrf in enumerate(kata):
        xh = x_start + k * (fw + gap)
        yr = tali_y(xh)
        yt = yr + 34
        spr, pad = kibar(bendera_sprite(hrf, fw, fh), fase=rng.uniform(0, 6) + k * 1.3, amp=max(4.0, fw * 0.035))
        tepi = spr.getchannel("A").filter(ImageFilter.MaxFilter(3))
        garis = Image.new("RGBA", spr.size, (40, 40, 50, 0))
        garis.putalpha(tepi.point(lambda v: int(v * 0.55)))
        garis.alpha_composite(spr)
        bayangan(lay, garis, (xh, yt - pad), blur=8, geser=(5, 8), kuat=0.22)
        ld = ImageDraw.Draw(lay)
        ld.line((xh, yr, xh, yt + fh + 16), fill=tali_col + (255,), width=3)
        for yy in (yt + 2, yt + fh - 2):
            ld.ellipse((xh - 6, yy - 6, xh + 6, yy + 6), outline=(90, 80, 70, 255), width=3)
        ld.ellipse((xh - 5, yr - 5, xh + 5, yr + 5), fill=(90, 80, 70, 255))
        posisi.append((xh, yt))
        y_huruf = max(y_huruf, yt + fh + 30)
    fhuruf = din(int(min(76, fw * 0.44)))
    for k, hrf in enumerate(kata):
        xh, yt = posisi[k]
        ld.text((xh + fw / 2, yt + fh + 30), hrf, font=fhuruf, fill=navy + (255,), anchor="ma")
    y = y_huruf + fhuruf.size + 46
    # kartu dekoder
    cw = 880
    eq_kiri = "  ·  ".join(kata) + "  =  "
    fe = avenir(54, 0)
    while ld.textlength(eq_kiri + kata, font=fe) > cw - 100:
        fe = avenir(fe.size - 2, 0)
    arti = bersih(p["arti"])
    fa = muat(ld, arti, lambda s: charter(s, 1), cw - 100, 46, 26)
    ch = int(64 + fe.size * 1.2 + 20 + fa.size * 1.3 + 40)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=26, fill=(255, 255, 255, 245))
    renggang(cd, (cw / 2, 26), "ARTINYA", avenir(20, 2), (130, 146, 166), 5, anchor="ma")
    x = cw / 2 - ld.textlength(eq_kiri + kata, font=fe) / 2
    ye = 60
    cd.text((x, ye), eq_kiri, font=fe, fill=(70, 84, 104))
    cd.text((x + ld.textlength(eq_kiri, font=fe), ye), kata, font=fe, fill=ICS["B"])
    cd.text((cw / 2, ye + fe.size * 1.2 + 20), arti, font=fa, fill=navy, anchor="ma")
    bayangan(lay, card, ((W - cw) / 2, y), blur=16, geser=(0, 10), kuat=0.16)
    ld = ImageDraw.Draw(lay)
    bawah = ayat_blok(ld, p, 100, W - 100, y + ch + 56, y + ch + 56 + 360, charter, navy + (255,), ICS["M"] + (255,), avenir(28, 0),
                      start=38, stop=26, lh=1.38, vtengah=False)
    geser = max(0, min(200, ((H - 96) - bawah - 136) / 2))
    img.alpha_composite(lay, (0, int(136 + geser)))
    kredit(ImageDraw.Draw(img), (W / 2, H - 50), (90, 120, 150))
    return img


# ---------- PERKAKAS: papan bayangan perkakas tukang kayu ----------

def _pk(pts, w, h, S):
    return [(x * w * S, y * h * S) for x, y in pts]


def alat_palu(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.42 * w * S, 0.15 * h * S, 0.58 * w * S, 0.99 * h * S), radius=0.08 * w * S, fill=255)
    ds.polygon(_pk([(0.08, 0.035), (0.38, 0.035), (0.42, 0.055), (0.64, 0.055), (0.80, 0.07), (0.94, 0.15), (0.98, 0.25),
                    (0.86, 0.19), (0.70, 0.165), (0.42, 0.165), (0.38, 0.185), (0.08, 0.185)], w, h, S), fill=255)


def alat_gergaji(dk, ds, w, h, S, m=None):
    ds.polygon(_pk([(0.30, 0.25), (0.74, 0.25), (0.62, 0.985), (0.44, 0.985)], w, h, S), fill=255)
    for k in range(26):  # gigi gergaji di sisi kiri
        t0, t1 = 0.27 + k * 0.0276, 0.27 + (k + 1) * 0.0276
        x0, x1 = 0.30 + (0.44 - 0.30) * (t0 - 0.25) / 0.735, 0.30 + (0.44 - 0.30) * (t1 - 0.25) / 0.735
        ds.polygon(_pk([(x0, t0), (x1 - 0.06, (t0 + t1) / 2), (x1, t1)], w, h, S), fill=255)
    dk.polygon(_pk([(0.22, 0.02), (0.80, 0.02), (0.86, 0.12), (0.78, 0.29), (0.24, 0.29), (0.16, 0.12)], w, h, S), fill=255)
    dk.ellipse((0.34 * w * S, 0.08 * h * S, 0.68 * w * S, 0.19 * h * S), fill=0)
    ds.ellipse((0.34 * w * S, 0.08 * h * S, 0.68 * w * S, 0.19 * h * S), fill=0)


def alat_pahat(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.28 * w * S, 0.0, 0.72 * w * S, 0.46 * h * S), radius=0.18 * w * S, fill=255)
    ds.rectangle((0.30 * w * S, 0.44 * h * S, 0.70 * w * S, 0.50 * h * S), fill=255)
    ds.polygon(_pk([(0.38, 0.5), (0.62, 0.5), (0.62, 0.93), (0.66, 1.0), (0.38, 1.0)], w, h, S), fill=255)


def alat_siku(dk, ds, w, h, S, m=None):
    dk.rectangle((0.04 * w * S, 0.0, 0.26 * w * S, 0.62 * h * S), fill=255)
    ds.rectangle((0.26 * w * S, 0.0, 0.98 * w * S, 0.11 * h * S), fill=255)


def alat_serut(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.02 * w * S, 0.42 * h * S, 0.98 * w * S, 0.86 * h * S), radius=0.08 * h * S, fill=255)
    dk.ellipse((0.10 * w * S, 0.18 * h * S, 0.26 * w * S, 0.50 * h * S), fill=255)
    dk.polygon(_pk([(0.60, 0.44), (0.66, 0.06), (0.86, 0.06), (0.92, 0.44)], w, h, S), fill=255)
    dk.ellipse((0.70 * w * S, 0.16 * h * S, 0.82 * w * S, 0.34 * h * S), fill=0)
    ds.polygon(_pk([(0.40, 0.44), (0.47, 0.0), (0.56, 0.0), (0.51, 0.44)], w, h, S), fill=255)


def alat_ganden(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.04 * w * S, 0.0, 0.96 * w * S, 0.30 * h * S), radius=0.05 * w * S, fill=255)
    dk.rounded_rectangle((0.40 * w * S, 0.28 * h * S, 0.60 * w * S, 1.0 * h * S), radius=0.08 * w * S, fill=255)


def alat_obeng(dk, ds, w, h, S, m=None):
    m["merah"].rounded_rectangle((0.16 * w * S, 0.0, 0.84 * w * S, 0.42 * h * S), radius=0.3 * w * S, fill=255)
    ds.rectangle((0.42 * w * S, 0.40 * h * S, 0.58 * w * S, 0.94 * h * S), fill=255)
    ds.polygon(_pk([(0.42, 0.94), (0.58, 0.94), (0.54, 1.0), (0.46, 1.0)], w, h, S), fill=255)


def alat_meteran(dk, ds, w, h, S, m=None):  # meteran gulung: rumah kuning, pita berskala
    m["cat"].rounded_rectangle((0.06 * w * S, 0.0, 0.94 * w * S, 0.44 * h * S), radius=0.2 * w * S, fill=255)
    m["gelap"].ellipse((0.26 * w * S, 0.08 * h * S, 0.74 * w * S, 0.32 * h * S), fill=255)
    m["cat"].ellipse((0.42 * w * S, 0.16 * h * S, 0.58 * w * S, 0.24 * h * S), fill=255)
    m["pita"].rectangle((0.36 * w * S, 0.40 * h * S, 0.64 * w * S, 0.95 * h * S), fill=255)
    for k in range(14):
        y = (0.44 + k * 0.036) * h * S
        m["gelap"].line((0.36 * w * S, y, (0.50 if k % 2 else 0.58) * w * S, y), fill=255, width=max(1, int(0.8 * S)))
    ds.rectangle((0.32 * w * S, 0.94 * h * S, 0.68 * w * S, 1.0 * h * S), fill=255)


def alat_waterpas(dk, ds, w, h, S, m=None):
    ds.rounded_rectangle((0.0, 0.25 * h * S, 1.0 * w * S, 0.75 * h * S), radius=0.06 * h * S, fill=255)
    for x0, x1 in ((0.42, 0.58), (0.08, 0.16), (0.84, 0.92)):
        m["gelap"].rounded_rectangle((x0 * w * S, 0.34 * h * S, x1 * w * S, 0.66 * h * S), radius=0.1 * h * S, fill=255)
        m["kaca"].rounded_rectangle(((x0 + 0.01) * w * S, 0.39 * h * S, (x1 - 0.01) * w * S, 0.61 * h * S), radius=0.08 * h * S, fill=255)


def alat_kikir(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.30 * w * S, 0.0, 0.70 * w * S, 0.34 * h * S), radius=0.16 * w * S, fill=255)
    ds.polygon(_pk([(0.36, 0.34), (0.64, 0.34), (0.58, 0.99), (0.42, 0.99)], w, h, S), fill=255)


def alat_kuas(dk, ds, w, h, S, m=None):
    dk.rounded_rectangle((0.38 * w * S, 0.0, 0.62 * w * S, 0.5 * h * S), radius=0.1 * w * S, fill=255)
    dk.ellipse((0.42 * w * S, 0.04 * h * S, 0.58 * w * S, 0.1 * h * S), fill=0)
    ds.rectangle((0.22 * w * S, 0.5 * h * S, 0.78 * w * S, 0.64 * h * S), fill=255)
    m["gelap"].polygon(_pk([(0.22, 0.64), (0.78, 0.64), (0.82, 1.0), (0.18, 1.0)], w, h, S), fill=255)


def alat_bor(dk, ds, w, h, S, m=None):
    ds.line(_pk([(0.5, 0.05), (0.5, 0.25), (0.2, 0.35), (0.2, 0.62), (0.5, 0.72), (0.5, 0.98)], w, h, S), fill=255, width=int(0.07 * w * S), joint="curve")
    dk.ellipse((0.36 * w * S, 0.0, 0.64 * w * S, 0.1 * h * S), fill=255)
    dk.rounded_rectangle((0.08 * w * S, 0.40 * h * S, 0.32 * w * S, 0.56 * h * S), radius=0.06 * w * S, fill=255)


def alat_tang(dk, ds, w, h, S, m=None):
    ds.polygon(_pk([(0.42, 0.0), (0.5, 0.0), (0.52, 0.34), (0.40, 0.34)], w, h, S), fill=255)
    ds.polygon(_pk([(0.5, 0.0), (0.58, 0.0), (0.60, 0.34), (0.48, 0.34)], w, h, S), fill=255)
    ds.ellipse((0.40 * w * S, 0.30 * h * S, 0.60 * w * S, 0.42 * h * S), fill=255)
    m["merah"].polygon(_pk([(0.42, 0.40), (0.48, 0.40), (0.30, 1.0), (0.18, 0.98)], w, h, S), fill=255)
    m["merah"].polygon(_pk([(0.52, 0.40), (0.58, 0.40), (0.82, 0.98), (0.70, 1.0)], w, h, S), fill=255)


# (fungsi, lebar, tinggi) ukuran asli dalam piksel
ALAT = {"palu": (alat_palu, 150, 280), "gergaji": (alat_gergaji, 190, 290), "pahat": (alat_pahat, 84, 270),
        "siku": (alat_siku, 230, 250), "serut": (alat_serut, 270, 150), "ganden": (alat_ganden, 170, 270),
        "obeng": (alat_obeng, 70, 270), "meteran": (alat_meteran, 120, 270), "waterpas": (alat_waterpas, 280, 70),
        "kikir": (alat_kikir, 70, 280), "kuas": (alat_kuas, 90, 250), "bor": (alat_bor, 160, 280), "tang": (alat_tang, 150, 270)}
KUNCI_ALAT = [("PALU KAYU", "ganden"), ("GANDEN", "ganden"), ("PALU", "palu"), ("GERGAJI", "gergaji"), ("PAHAT", "pahat"),
              ("SIKU", "siku"), ("SERUT", "serut"), ("KETAM", "serut"), ("OBENG", "obeng"), ("METER", "meteran"),
              ("PENGGARIS", "meteran"), ("MISTAR", "meteran"), ("WATERPAS", "waterpas"), ("KIKIR", "kikir"), ("AMPLAS", "kikir"),
              ("KUAS", "kuas"), ("BOR", "bor"), ("TANG", "tang")]
URUT_CADANGAN = ["palu", "gergaji", "pahat", "siku", "serut", "ganden"]


def jenis_alat(nama, k):
    besar = nama.upper()
    for kunci, jenis in KUNCI_ALAT:
        if kunci in besar:
            return jenis
    return URUT_CADANGAN[k % len(URUT_CADANGAN)]


BAHAN = ("baja", "kayu", "merah", "cat", "pita", "gelap", "kaca")  # urutan tumpuk (yang belakang di atas)


def render_alat(jenis, maxw, maxh, rng):
    """-> (tool RGBA, mask L gabungan) diskalakan muat di maxw x maxh."""
    fn, bw, bh = ALAT[jenis]
    s = min(maxw / bw, maxh / bh, 1.25)
    w, h = int(bw * s), int(bh * s)
    S = 3
    kanvas = {b: Image.new("L", (w * S, h * S), 0) for b in BAHAN}
    gambar = {b: ImageDraw.Draw(kanvas[b]) for b in BAHAN}
    fn(gambar["kayu"], gambar["baja"], w, h, S, gambar)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = xx if h >= w else yy
    serat = (0.5 + 0.5 * np.sin(u * 0.55 + 4 * render.fbm2d(h, w, rng, ((2, 1.0), (6, 0.5))) * 3)) ** 3
    kayu = np.array([190, 140, 90], np.float32) * (0.97 - 0.12 * serat)[..., None]
    kayu *= (0.9 + 0.14 * render.fbm2d(h, w, rng, ((3, 1.0), (24, 0.5), (90, 0.3))))[..., None]
    kilap = np.clip(1 - np.abs((xx / max(1, w) - 0.35)) * 1.6, 0, 1)[..., None]
    warna = {
        "kayu": kayu,
        "baja": np.array([170, 176, 184], np.float32) * (0.82 + 0.3 * kilap),
        "merah": np.array([200, 64, 52], np.float32) * (0.86 + 0.24 * kilap),
        "cat": np.array([238, 190, 44], np.float32) * (0.88 + 0.18 * kilap),
        "pita": np.array([246, 214, 90], np.float32) * np.ones_like(kilap),
        "gelap": np.array([50, 46, 44], np.float32) * np.ones_like(kilap),
        "kaca": np.array([150, 214, 110], np.float32) * (0.9 + 0.2 * kilap),
    }
    P = np.zeros((h, w, 3), np.float32)
    A = np.zeros((h, w), np.float32)
    for b in BAHAN:
        ma = np.asarray(kanvas[b].resize((w, h), Image.LANCZOS), np.float32) / 255
        P = P * (1 - ma[..., None]) + warna[b] * ma[..., None]
        A = A * (1 - ma) + ma
    rgb = np.where(A[..., None] > 1e-3, P / np.maximum(A, 1e-3)[..., None], 0)
    mask = Image.fromarray((A * 255).astype(np.uint8))
    tepi = np.asarray(mask.filter(ImageFilter.MinFilter(3)), np.float32) / 255
    rgb *= (0.72 + 0.28 * tepi)[..., None]
    tool = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), A * 255]).astype(np.uint8), "RGBA")
    return tool, mask


@lru_cache(maxsize=1)
def _pasak_sprite():
    def g(d, k):
        d.ellipse((5 * k, 7 * k, 25 * k, 27 * k), fill=(40, 36, 32, 110))
        d.ellipse((3 * k, 3 * k, 21 * k, 21 * k), fill=(150, 154, 160, 255))
        d.ellipse((6 * k, 5 * k, 15 * k, 13 * k), fill=(220, 224, 228, 255))
    return sprite(30, 30, g, k=4)


def pasak(img, x, y):
    comp(img, _pasak_sprite(), (x - 12, y - 12))


def perkakas_image(p, i):
    rng = np.random.default_rng(17400 + i)
    papan = kertas_tekstur(W, H, (206, 200, 190), 17400 + i, 0.03).convert("RGBA")
    img = papan
    d = ImageDraw.Draw(img)
    oranye, lubang, hitam = (240, 120, 40), (120, 114, 106), (30, 30, 30)
    grid = 40
    alat = [bersih(a) for a in p["alat"]][:6]
    kosong = int(p.get("kosong", 0)) % len(alat)
    n = len(alat)
    # tata letak: 3 kolom x 2 baris (5 alat: 3 + 2 di tengah)
    cw, chh = 300, 330
    x0s = [90, 390, 690]
    slots = []
    for k in range(n):
        r, c = divmod(k, 3)
        x = x0s[c] + (150 if (n == 5 and r == 1) else 0)
        slots.append((x, 180 + r * (chh + 12)))
    cat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    alat_lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pegs, labels, tag = [], [], None
    for k, nama in enumerate(alat):
        sx, sy = slots[k]
        tool, mask = render_alat(jenis_alat(nama, k), cw - 50, chh - 76, rng)
        tx, ty = int(sx + (cw - tool.width) / 2), int(sy + 22 + (chh - 76 - tool.height) / 2)
        pad = 12
        mpad = Image.new("L", (mask.width + 2 * pad, mask.height + 2 * pad), 0)
        mpad.paste(mask, (pad, pad))
        bay = mpad.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(0.8))
        lapis_warna(cat, bay, oranye, 0.96, (tx - pad, ty - pad))
        px = [tx + tool.width * 0.5] if tool.width < 120 else [tx + tool.width * 0.3, tx + tool.width * 0.7]
        for x in px:
            gx = round((x - 20) / grid) * grid + 20
            gy = round((ty - 6 - 20) / grid) * grid + 20
            pegs.append((gx, gy))
        if k == kosong:
            tag = (pegs[-1], tx + tool.width / 2, ty + tool.height / 2)
        else:
            sh = Image.new("RGBA", (tool.width + 40, tool.height + 40), (0, 0, 0, 0))
            sh.paste((0, 0, 0, 255), (20, 20), mask.point(lambda v: int(v * 0.45)))
            comp(alat_lay, sh.filter(ImageFilter.GaussianBlur(6)), (tx - 20 + 6, ty - 20 + 9))
            comp(alat_lay, tool, (tx, ty))
        labels.append((sx + cw / 2, sy + chh - 34, nama.upper()))
    img.alpha_composite(cat)
    d = ImageDraw.Draw(img)
    for gy in range(20, H, grid):  # lubang papan
        for gx in range(20, W, grid):
            d.ellipse((gx - 5, gy - 5, gx + 5, gy + 5), fill=lubang)
            d.arc((gx - 5, gy - 5, gx + 5, gy + 5), 20, 160, fill=(226, 220, 210), width=1)
    img.alpha_composite(alat_lay)
    d = ImageDraw.Draw(img)
    for gx, gy in pegs:
        pasak(img, gx, gy)
    fl = helv(22, 1)
    for x, y, t in labels:  # pelat nama kecil (seperti label tempel) di bawah tiap tempat
        f = fl
        while lebar_renggang(d, t, f, 3) > 240 and f.size > 14:
            f = helv(f.size - 1, 1)
        lw = lebar_renggang(d, t, f, 3)
        d.rounded_rectangle((x - lw / 2 - 16, y - 9, x + lw / 2 + 16, y + f.size + 9), radius=5, fill=(34, 32, 30))
        renggang(d, (x, y), t, f, (246, 240, 228), 3, anchor="ma")
    if tag:
        (gx, gy), cx, cy = tag
        lab = bersih(p.get("label_kosong", "sedang dipakai"))
        ft_ = muat(d, lab, coret, 220, 30, 18)
        tw = int(d.textlength(lab, font=ft_) + 46)
        kartu = Image.new("RGBA", (tw, 64), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kartu)
        kd.rounded_rectangle((0, 0, tw - 1, 63), radius=8, fill=(250, 246, 234, 255), outline=(180, 170, 150, 255), width=2)
        kd.ellipse((12, 26, 22, 36), outline=(150, 140, 120, 255), width=2)
        kd.text((tw / 2 + 8, 32), lab, font=ft_, fill=(30, 30, 30, 255), anchor="mm")
        kartu = kartu.rotate(-5, expand=True, resample=Image.BICUBIC)
        kx, ky = cx - kartu.width / 2, cy - kartu.height / 2 + 10
        d.line((gx, gy, kx + 22, ky + kartu.height / 2 - 4), fill=(120, 100, 80), width=2)
        bayangan(img, kartu, (kx, ky), blur=6, geser=(3, 6), kuat=0.3)
        d = ImageDraw.Draw(img)
        pasak(img, gx, gy)
    # papan nama hitam di atas
    d.rounded_rectangle((70, 52, W - 70, 146), radius=6, fill=hitam)
    judul = bersih(p["judul"]).upper()
    fj = din(70)
    while lebar_renggang(d, judul, fj, 8) > W - 260 and fj.size > 36:
        fj = din(fj.size - 2)
    renggang(d, (W / 2, 104), judul, fj, (255, 255, 255), 8, anchor="mm")
    for x in (98, W - 98):
        d.ellipse((x - 9, 90, x + 9, 108), fill=(90, 90, 92))
        d.line((x - 6, 99, x + 6, 99), fill=(40, 40, 40), width=2)
    # kartu ayat tergantung tali pada satu pasak
    cwid = 860
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rf = din(30)
    f, lines, size = susun(probe, bersih(p["ayat"]), charter, cwid - 110, 300, 33, 24, 1.36)
    ch = int(len(lines) * size * 1.36 + rf.size + 84)
    label_bawah = max(y for _, y, _ in labels) + 40
    gy_peg = round((label_bawah + max(30, (H - 60 - label_bawah - ch - 66) / 2) - 20) / grid) * grid + 20
    peg = (round((W / 2 - 20) / grid) * grid + 20, gy_peg)
    ytop = min(H - 60 - ch, peg[1] + 66)
    kartu = Image.new("RGBA", (cwid, ch), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kartu)
    kd.rectangle((0, 0, cwid - 1, ch - 1), fill=(250, 246, 236, 255))
    kd.rectangle((0, 0, cwid - 1, 10), fill=oranye + (255,))
    y = 40
    for ln in lines:
        kd.text((cwid / 2, y), ln, font=f, fill=(40, 36, 32), anchor="ma")
        y += size * 1.36
    renggang(kd, (cwid / 2, y + 10), p["ref"].upper(), rf, (200, 92, 30), 2, anchor="ma")
    lubang_k = [(60, 34), (cwid - 60, 34)]
    for hx, hy in lubang_k:
        kd.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=(226, 214, 190, 255))
        kd.ellipse((hx - 5, hy - 5, hx + 5, hy + 5), fill=(120, 114, 106, 255))
    kx = (W - cwid) / 2
    bayangan(img, kartu, (kx, ytop), blur=14, geser=(4, 10), kuat=0.35)
    d = ImageDraw.Draw(img)
    for hx, hy in lubang_k:
        d.line((peg[0], peg[1], kx + hx, ytop + hy), fill=(110, 92, 72), width=3)
    pasak(img, *peg)
    fk = helv(20, 10)
    tw = d.textlength("@" + HANDLE, font=fk)
    d.rounded_rectangle((W / 2 - tw / 2 - 14, H - 50, W / 2 + tw / 2 + 14, H - 18), radius=5, fill=(34, 32, 30))
    kredit(d, (W / 2, H - 34), (236, 230, 220), anchor="mm", size=20)
    return img


# ---------- PLANG: papan seng tulisan tangan ----------

def huruf_pelukis(teks, f, jitter, rng, track=0):
    """Mask L huruf satu per satu dengan miring acak kecil (±jitter derajat). -> (mask, lebar, tinggi)."""
    probe = ImageDraw.Draw(Image.new("L", (10, 10)))
    lebar = int(sum(probe.textlength(c, font=f) for c in teks) + track * (len(teks) - 1) + 40)
    asc, desc = f.getmetrics()
    tinggi = asc + desc + 30
    m = Image.new("L", (lebar, tinggi), 0)
    x = 20
    for c in teks:
        cw = probe.textlength(c, font=f)
        if c.strip():
            g = Image.new("L", (int(cw + 40), tinggi), 0)
            ImageDraw.Draw(g).text((20, 15), c, font=f, fill=255)
            g = g.rotate(rng.uniform(-jitter, jitter), resample=Image.BICUBIC, center=(20 + cw / 2, tinggi / 2))
            m.paste(255, (int(x - 20), int(rng.uniform(-2, 2))), g)
        x += cw + track
    return m, lebar, tinggi


def plang_image(p, i):
    rng = np.random.default_rng(17500 + i)
    # latar pinggir jalan: langit, semak tropis, tanah
    img = gradasi(W, H, (166, 208, 228), (232, 232, 216)).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle((0, 760, W, 1130), fill=(66, 112, 66, 255))
    for _ in range(46):  # semak & pohon pisang samar di belakang
        x, y = rng.uniform(-60, W + 60), rng.uniform(660, 1000)
        r = rng.uniform(60, 150)
        ld.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=campur((54, 100, 62), (112, 152, 84), rng.random()) + (255,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    tanah = kertas_tekstur(W, H - 1120, (196, 178, 146), 17510 + i, 0.08)
    img.paste(tanah, (0, 1120))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 1120, W, 1128), fill=(170, 150, 118))
    for xc in (250, 830):  # tiang kayu
        tiang = kertas_tekstur(48, H - 300, (122, 86, 58), 17520 + xc, 0.12, serat=0.3)
        img.paste(tiang, (xc - 24, 300))
        d.line((xc + 22, 300, xc + 22, H), fill=(84, 58, 40), width=4)
    rumput = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rumput)
    for gx0 in [250, 830] + list(rng.uniform(0, W, 6)):  # rumpun rumput
        for _ in range(16):
            gx = gx0 + rng.normal(0, 26)
            gy = H - rng.uniform(70, 110)
            tinggi, condong = rng.uniform(40, 90), rng.uniform(-26, 26)
            rd.polygon([(gx - 4, gy), (gx + 4, gy), (gx + condong, gy - tinggi)], fill=campur((70, 112, 56), (120, 156, 76), rng.random()) + (255,))
    img.alpha_composite(rumput)
    # tata letak tulisan dulu, supaya tinggi papan seng pas dengan isinya
    zw = W - 140
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    judul = bersih(p["judul"]).upper()
    fsize = 150
    while True:
        mj, lw, lh = huruf_pelukis(judul, rockwell(fsize), 1.5, np.random.default_rng(17530 + i), track=4)
        if lw <= zw - 110 or fsize <= 60:
            break
        fsize -= 4
    jx, jy = int((zw - lw) / 2), 34
    y = jy + lh + 4
    baris_pos = []
    for k, teks in enumerate(p["baris"][:2]):
        t = bersih(teks)
        fb = muat(probe, t, kuas, zw - 120, 78 if k == 0 else 72, 36)
        baris_pos.append((t, fb, y))
        y += fb.size * 0.98
    arah = bersih(p["arah"])
    fa = muat(probe, arah, ablack, 260, 44, 22)
    aw = max(250, int(probe.textlength(arah, font=fa) + 120))
    ah = 96
    ay = y + 26 + ah / 2
    zh = int(ay + ah / 2 + 54)
    rf = rockwell(32)
    yw = W - 300
    f, lines, size = susun(probe, bersih(p["ayat"]), charter, yw - 100, 330, 34, 24, 1.36)
    yh = int(len(lines) * size * 1.36 + rf.size + 110)
    total = zh + 46 + yh
    zx, zy = 70, int(max(56, min(190, (1230 - total) / 2)))
    # papan seng biru muda bergelombang
    xs = np.arange(zw, dtype=np.float32)[None, :]
    korug = (0.9 + 0.1 * np.sin(0.16 * xs)) * np.ones((zh, 1), np.float32)
    n = rng.random((zh, max(2, zw // 40))).astype(np.float32)
    sapu = np.asarray(Image.fromarray(n).resize((zw, zh), Image.BICUBIC), np.float32)
    cat = np.zeros((zh, zw, 3), np.float32) + np.array([120, 190, 210], np.float32)
    cat *= (0.95 + 0.07 * sapu)[..., None]
    seng = np.zeros_like(cat) + np.array([168, 174, 178], np.float32)
    kelupas = render.fbm2d(zh, zw, rng, ((5, 1.0), (24, 0.6), (90, 0.3)))
    yy, xx = np.mgrid[0:zh, 0:zw].astype(np.float32)
    tepi = np.minimum(np.minimum(xx, zw - xx), np.minimum(yy, zh - yy))
    dekat = np.exp(-tepi / 40)
    kl = np.clip((kelupas + 0.3 * dekat - 0.74) * 9, 0, 1)
    arr = cat * (1 - kl[..., None]) + seng * kl[..., None]
    karat_n = np.asarray(Image.fromarray((render.fbm2d(zh, zw, rng, ((14, 1.0), (40, 0.5))) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
    karat = np.clip((karat_n + 0.42 * dekat - 0.8) * 7, 0, 1)
    paku = [(26, 26), (zw - 26, 26), (26, zh - 26), (zw - 26, zh - 26), (180, 26), (zw - 180, zh - 26), (zw - 180, 26), (180, zh - 26)]
    for (px_, py_) in paku:  # karat meleleh di bawah paku
        lele = np.exp(-((xx - px_) / 6) ** 2) * np.clip(1 - (yy - py_) / rng.uniform(60, 150), 0, 1) * (yy > py_)
        karat = np.maximum(karat, lele * 0.85)
    arr = arr * (1 - karat[..., None] * 0.85) + np.array([150, 80, 40], np.float32) * karat[..., None] * 0.85
    # tulisan cat
    huruf = Image.new("RGBA", (zw, zh), (0, 0, 0, 0))
    luar = mj.filter(ImageFilter.MaxFilter(7))
    bay = Image.new("L", (zw, zh), 0)
    bay.paste(luar, (jx + 9, jy + 9))
    lapis_warna(huruf, bay, (210, 50, 40))
    ol = Image.new("L", (zw, zh), 0)
    ol.paste(luar, (jx, jy))
    lapis_warna(huruf, ol, (24, 24, 24))
    isi = Image.new("L", (zw, zh), 0)
    isi.paste(mj, (jx, jy))
    lapis_warna(huruf, isi, (250, 248, 240))
    hd = ImageDraw.Draw(huruf)
    for k, (t, fb, yb) in enumerate(baris_pos):
        warna = ((24, 24, 24), (196, 40, 32))[k]
        hd.text((zw / 2 + 2, yb + 2), t, font=fb, fill=(250, 248, 240, 160), anchor="ma")
        hd.text((zw / 2, yb), t, font=fb, fill=warna + (255,), anchor="ma")
    # panah dicat + jarak (menunjuk ke kiri kalau tulisannya "kiri")
    kiri = "KIRI" in arah.upper()
    ax0, ax1 = (70, 70 + aw) if kiri else (zw - 70 - aw, zw - 70)
    mp = Image.new("L", (zw, zh), 0)
    bentuk = [(0, -0.3), (aw - 70, -0.3), (aw - 70, -0.5), (aw, 0), (aw - 70, 0.5), (aw - 70, 0.3), (0, 0.3)]
    ImageDraw.Draw(mp).polygon([((ax1 - x) if kiri else (ax0 + x), ay + v * ah) for x, v in bentuk], fill=255)
    lapis_warna(huruf, mp.filter(ImageFilter.MaxFilter(7)), (24, 24, 24))
    lapis_warna(huruf, mp, (210, 50, 40))
    hd = ImageDraw.Draw(huruf)
    hd.text(((ax1 - (aw - 70) / 2 - 6) if kiri else (ax0 + (aw - 70) / 2 + 6), ay + 2), arah, font=fa, fill=(250, 248, 240, 255), anchor="mm")
    # gergaji kecil dicat di sisi lain panah
    ik = Image.new("L", (zw, zh), 0)
    idr = ImageDraw.Draw(ik)
    bx, by = 80, ay
    idr.polygon([(bx + 64, by - 24), (bx + 230, by - 12), (bx + 230, by + 4), (bx + 64, by + 20)], fill=255)
    for k in range(16):
        x = bx + 70 + k * 10
        idr.polygon([(x, by + 19 - k * 0.9), (x + 5, by + 28 - k * 0.9), (x + 10, by + 18 - k * 0.9)], fill=255)
    idr.polygon([(bx + 4, by - 30), (bx + 50, by - 36), (bx + 72, by - 24), (bx + 72, by + 22), (bx + 40, by + 34), (bx + 8, by + 26), (bx + 18, by)], fill=255)
    idr.ellipse((bx + 26, by - 18, bx + 56, by + 14), fill=0)
    if kiri:
        ik = ik.transpose(Image.FLIP_LEFT_RIGHT)
    if (not kiri and ax0 > bx + 250) or (kiri and ax1 < zw - bx - 250):
        lapis_warna(huruf, ik, (24, 24, 24), 0.92)
    ha = np.asarray(huruf).astype(np.float32)
    a_h = ha[..., 3:] / 255 * (0.88 + 0.12 * sapu[..., None])
    arr = arr * (1 - a_h) + ha[..., :3] * a_h
    arr *= korug[..., None]
    zimg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    zd = ImageDraw.Draw(zimg)
    for (px_, py_) in paku:
        zd.ellipse((px_ - 7, py_ - 7, px_ + 7, py_ + 7), fill=(70, 66, 62))
        zd.ellipse((px_ - 4, py_ - 5, px_ + 2, py_ + 1), fill=(170, 166, 160))
    zimg = zimg.rotate(-0.8, expand=True, resample=Image.BICUBIC)
    bayangan(img, zimg, (zx - (zimg.width - zw) / 2, zy - (zimg.height - zh) / 2), blur=14, geser=(6, 12), kuat=0.45)
    # papan kuning berisi ayat
    yx, yy0 = 150, zy + zh + 46
    pk = np.zeros((yh, yw, 3), np.float32) + np.array([246, 206, 60], np.float32)
    nn = rng.random((yh, max(2, yw // 30))).astype(np.float32)
    pk *= (0.93 + 0.09 * np.asarray(Image.fromarray(nn).resize((yw, yh), Image.BICUBIC), np.float32))[..., None]
    kb = Image.fromarray(np.clip(pk, 0, 255).astype(np.uint8)).convert("RGBA")
    kd = ImageDraw.Draw(kb)
    kd.rectangle((14, 14, yw - 15, yh - 15), outline=(24, 24, 24, 255), width=4)
    y = 50
    for ln in lines:
        kd.text((yw / 2, y), ln, font=f, fill=(20, 20, 20), anchor="ma")
        y += size * 1.36
    kd.text((yw / 2, y + 12), p["ref"].upper(), font=rf, fill=(196, 40, 32), anchor="ma")
    for (px_, py_) in [(30, 30), (yw - 30, 30), (30, yh - 30), (yw - 30, yh - 30)]:
        kd.ellipse((px_ - 6, py_ - 6, px_ + 6, py_ + 6), fill=(70, 66, 62))
    kb = kb.rotate(0.6, expand=True, resample=Image.BICUBIC)
    bayangan(img, kb, (yx, yy0), blur=12, geser=(5, 10), kuat=0.4)
    d = ImageDraw.Draw(img)
    kredit(d, (W / 2, H - 40), (70, 58, 44))
    return img


# ---------- CONGKLAK: papan congklak ----------

def kurangi(a, b):
    return Image.fromarray(np.clip(np.asarray(a, np.int16) - np.asarray(b, np.int16), 0, 255).astype(np.uint8))


def lubang_sprite(rx, ry):
    """Lubang cekung (RGBA): dinding atas gelap (bayang), dasar bawah lebih terang, bibir bawah berkilau."""
    w, h = int(rx * 2 + 12), int(ry * 2 + 12)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = (xx - w / 2) / rx, (yy - h / 2) / ry
    r = np.sqrt(u * u + v * v)
    di_dalam = np.clip((1 - r) * min(rx, ry) * 0.6, 0, 1)
    dasar = np.array([112, 72, 42], np.float32)
    terang = np.clip(0.38 + 0.62 * (v * 0.55 + 0.45) * (1 - r ** 3) + 0.25 * np.clip(v, 0, 1) * r ** 4, 0.25, 1.15)
    rgb = dasar * terang[..., None]
    rgb *= (1 - 0.45 * np.clip(-v, 0, 1)[..., None] * (r ** 2)[..., None])
    bibir = np.clip(1 - np.abs(r - 1.0) * min(rx, ry) / 2.5, 0, 1)
    kil = bibir * np.clip(v, 0, 1) ** 1.5
    gelap = bibir * np.clip(-v, 0, 1)
    rgb = rgb * (1 - gelap[..., None] * 0.5) + kil[..., None] * np.array([210, 160, 110]) * 0.6
    a = np.clip(di_dalam + bibir * 0.9, 0, 1)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8), "RGBA")


def kerang(L, rng):
    """Kerang cowrie kecil (RGBA), dilihat dari sisi bercelah."""
    h = int(L * 0.7)

    def gambar(d, k):
        d.ellipse((1 * k, 1 * k, (L - 1) * k, (h - 1) * k), fill=(236, 226, 204, 255))
        d.ellipse((L * 0.12 * k, h * 0.08 * k, L * 0.7 * k, h * 0.5 * k), fill=(250, 246, 234, 255))
        d.line([(L * 0.12 * k, h * 0.56 * k), (L * 0.5 * k, h * 0.5 * k), (L * 0.88 * k, h * 0.56 * k)], fill=(140, 118, 96, 255),
               width=max(1, int(L * 0.07 * k)), joint="curve")
        for t in np.linspace(0.2, 0.8, 7):
            x = L * t * k
            d.line((x, h * 0.42 * k, x, h * 0.64 * k), fill=(166, 144, 120, 255), width=max(1, int(L * 0.035 * k)))
    spr = sprite(L, h, gambar, k=4)
    a = np.asarray(spr).astype(np.float32)
    yy = np.linspace(0, 1, h)[:, None]
    a[..., :3] *= (1.05 - 0.2 * yy)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def isi_lubang(img, cx, cy, r, n, rng, L=30):
    pos = []
    for _ in range(int(n)):
        for _try in range(80):
            a, rr = rng.uniform(0, 2 * math.pi), r * math.sqrt(rng.random())
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.9
            if all(math.hypot(x - qx, y - qy) > L * 0.5 for qx, qy in pos):
                break
        pos.append((x, y))
        k = kerang(int(L * rng.uniform(0.92, 1.08)), rng).rotate(rng.uniform(0, 180), expand=True, resample=Image.BICUBIC)
        bayangan(img, k, (x - k.width / 2, y - k.height / 2), blur=2, geser=(1, 3), kuat=0.6)


def congklak_image(p, i):
    rng = np.random.default_rng(17600 + i)
    kain = kertas_tekstur(W, H, (232, 222, 200), 17600 + i, 0.03)
    a = np.asarray(kain).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    a *= (1 - 0.03 * ((xx // 3 + yy // 3) % 2))[..., None]  # anyaman linen
    tepi_kain = (np.minimum(yy, H - 1 - yy) < 26) | (np.minimum(xx, W - 1 - xx) < 26)
    a[tepi_kain] *= np.array([0.86, 0.78, 0.72])  # pinggiran kain
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    merah, tinta = (190, 74, 44), (70, 50, 36)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rf = iowan(32, 3)
    _, vl, vs = susun(probe, bersih(p["ayat"]), charter, W - 200, 330 - rf.size - 20, 40, 26, 1.4)
    tinggi_ayat = len(vl) * vs * 1.4 + rf.size + 20
    renggang(d, (W / 2, 76), "CONGKLAK  ·  DAKON", avenir(22, 2), (150, 120, 90), 5, anchor="ma")
    f = muat(d, bersih(p["judul"]), lambda s: iowan(s, 2), W - 160, 60, 34)
    d.text((W / 2, 110), bersih(p["judul"]), font=f, fill=tinta, anchor="ma")
    a_, b_ = 478, 172
    cy = int(max(470, min(560, (H - 120 - tinggi_ayat - 90 - b_ + 470) / 2)))
    cx = W / 2
    # papan berbentuk perahu: badan superelips, ujung meruncing dengan kepala ukiran
    pts = []
    for t in np.linspace(0, 2 * math.pi, 400, endpoint=False):
        c, s_ = math.cos(t), math.sin(t)
        x = a_ * math.copysign(abs(c) ** 0.5, c)
        y = b_ * math.copysign(abs(s_) ** 0.5, s_) * (1 - 0.18 * abs(c) ** 4)
        pts.append((cx + x, cy + y))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(pts, fill=255)
    for sgn in (-1, 1):
        md.polygon([(cx + sgn * (a_ - 40), cy - 70), (cx + sgn * (a_ + 30), cy), (cx + sgn * (a_ - 40), cy + 70)], fill=255)
        md.ellipse((cx + sgn * (a_ + 22) - 22, cy - 22, cx + sgn * (a_ + 22) + 22, cy + 22), fill=255)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.paste((60, 40, 20, 255), (0, 0), mask.point(lambda v: int(v * 0.5)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (10, 22))
    fase = (yy - cy) * 0.3 + 7 * render.fbm2d(H, W, rng, ((3, 1.0), (9, 0.4)))
    serat = (0.5 + 0.5 * np.sin(fase)) ** 4
    kayu = np.array([166, 108, 62], np.float32) * (1 - serat[..., None] * 0.2)
    kayu = kayu * (0.9 + 0.14 * render.fbm2d(H, W, rng, ((4, 1.0), (40, 0.4))))[..., None]
    m_np = np.asarray(mask.filter(ImageFilter.GaussianBlur(12)), np.float32) / 255
    kayu *= (0.7 + 0.34 * m_np)[..., None]
    terang = np.asarray(mask.filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
    kayu += (np.clip(terang - np.roll(terang, 6, axis=0), 0, 1) * 80)[..., None]
    kotak = (int(cx - a_ - 60), int(cy - b_ - 20), int(cx + a_ + 60), int(cy + b_ + 20))
    alur = mask.crop(kotak).resize(((kotak[2] - kotak[0]) // 2, (kotak[3] - kotak[1]) // 2)).filter(ImageFilter.MinFilter(19))
    garis = kurangi(alur, alur.filter(ImageFilter.MinFilter(3))).resize((kotak[2] - kotak[0], kotak[3] - kotak[1]), Image.BILINEAR)
    garis_alur = np.zeros((H, W), np.float32)
    garis_alur[kotak[1]:kotak[3], kotak[0]:kotak[2]] = np.asarray(garis, np.float32) / 255
    kayu *= (1 - 0.35 * garis_alur)[..., None]  # alur ukiran di sepanjang tepi
    papan = Image.fromarray(np.dstack([np.clip(kayu, 0, 255), np.asarray(mask)]).astype(np.uint8), "RGBA")
    img.alpha_composite(papan)
    d = ImageDraw.Draw(img)
    for sgn in (-1, 1):  # kepala ukiran di ujung
        ex = cx + sgn * (a_ + 22)
        d.ellipse((ex - 14, cy - 14, ex + 14, cy + 14), outline=(110, 66, 34), width=3)
        d.arc((ex - 8, cy - 8, ex + 8, cy + 8), 0, 270, fill=(110, 66, 34), width=3)
    isi = [max(0, min(9, int(v))) for v in list(p["isi"]) + [0] * 16][:16]
    sp, r = 94, 40
    xs = [cx + (k - 3) * sp for k in range(7)]
    rows = [cy - 74, cy + 74]
    lub = lubang_sprite(r, r * 0.92)
    lumbung = lubang_sprite(58, 116)
    lx = [cx - 3 * sp - r - 26 - 58, cx + 3 * sp + r + 26 + 58]
    for x in lx:
        comp(img, lumbung, (x - lumbung.width / 2, cy - lumbung.height / 2))
    for ry in rows:
        for x in xs:
            comp(img, lub, (x - lub.width / 2, ry - lub.height / 2))
    for k in range(7):
        isi_lubang(img, xs[k], rows[0], r * 0.5, isi[k], rng)
        isi_lubang(img, xs[k], rows[1], r * 0.5, isi[7 + k], rng)
    for j, x in enumerate(lx):
        isi_lubang(img, x, cy, 30, isi[14 + j], rng, L=32)
    # jalur menabur: lengkung titik-titik di atas papan, satu biji tiap lubang, angka "1" di puncak tiap lompatan
    calon = [1, 3, 2, 0][i % 3:] + [1, 3, 2, 0][:i % 3]  # mulai dari lubang baris atas yang berisi paling banyak
    mulai = max(calon, key=lambda k: (isi[k], -calon.index(k)))
    langkah = min(4, 6 - mulai)
    puncak = cy - b_ - 54
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for k in range(langkah):
        x0_, x1_ = xs[mulai + k], xs[mulai + k + 1]
        pts_ = kurva((x0_ + 6, rows[0] - 26), ((x0_ + x1_) / 2, 2 * puncak - (rows[0] - 30)), (x1_ - 4, rows[0] - 30), 34)
        pts_ = [(x * S, y * S) for x, y in pts_]
        if k == langkah - 1:
            panah(ld, pts_, merah + (255,), 4 * S, L=17 * S, pola=(4 * S, 8 * S))
        else:
            putus(ld, pts_, merah + (255,), 4 * S, (4 * S, 8 * S))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    fc = bradley(34)
    for k in range(langkah):
        x0_, x1_ = xs[mulai + k], xs[mulai + k + 1]
        d.text(((x0_ + x1_) / 2, puncak - 14), "1", font=fc, fill=merah, anchor="ms")
    d.text((xs[mulai] - 30, puncak - 14), "ambil", font=bradley(26), fill=tinta, anchor="rs")
    xa = xs[mulai + langkah]
    kr = kerang(32, rng).rotate(30, expand=True, resample=Image.BICUBIC)
    bayangan(img, kr, (xa - kr.width / 2 + 10, rows[0] - 100), blur=6, geser=(4, 40), kuat=0.3)
    yb = cy + b_ + 40
    for (x, y, rot) in [(110, yb - 30, 20), (W - 150, yb - 46, -40), (W - 214, yb - 6, 70)]:  # kerang lepas di kain
        k_ = kerang(30, rng).rotate(rot, expand=True, resample=Image.BICUBIC)
        bayangan(img, k_, (x, y), blur=2, geser=(1, 3), kuat=0.5)
    d = ImageDraw.Draw(img)
    ayat_blok(d, p, 100, W - 100, yb + 30, H - 90, charter, (60, 44, 32), merah, rf, start=40, stop=26, lh=1.4)
    kredit(d, (W / 2, H - 58), (150, 130, 108))
    return img


# ---------- ALUR: diagram alur tulisan tangan ----------

def goyang(pts, rng, amp=1.6, tutup=True):
    """Titik-titik garis dengan getar halus seperti digambar tangan."""
    n = len(pts)
    noise = np.cumsum(rng.normal(0, amp * 0.35, (n, 2)), axis=0)
    noise -= np.linspace(0, 1, n)[:, None] * noise[-1]
    noise = np.clip(noise, -amp * 2, amp * 2)
    return [(x + noise[k, 0], y + noise[k, 1]) for k, (x, y) in enumerate(pts)]


def oval_pts(cx, cy, rx, ry, n=90):
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi * 1.04, n)]


def kotak_pts(x0, y0, x1, y1, r=18, n=14):
    pts = []
    for (cx_, cy_, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for t in np.linspace(a0, a0 + 90, n):
            pts.append((cx_ + r * math.cos(math.radians(t)), cy_ + r * math.sin(math.radians(t))))
    return pts + pts[:2]


def garis_isi(a, b, n=20):
    return [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for t in np.linspace(0, 1, n)]


def alur_image(p, i):
    rng = np.random.default_rng(17700 + i)
    img = Image.new("RGB", (W, H), (238, 242, 246))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 30):
        d.line((x, 0, x, H), fill=(214, 224, 234) if x % 150 else (196, 210, 226), width=1)
    for y in range(0, H, 30):
        d.line((0, y, W, y), fill=(214, 224, 234) if y % 150 else (196, 210, 226), width=1)
    img = grain(img, 0.02).convert("RGBA")
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    tinta, hijau, merah = (30, 30, 30, 255), (40, 160, 90, 255), (220, 70, 50, 255)

    def gar(pts, col=tinta, w=4, tutup=False):
        q = goyang(pts, rng)
        ld.line([(x * S, y * S) for x, y in q], fill=col, width=int(w * S), joint="curve")

    def pan(pts, col=tinta, w=4):
        q = goyang(pts, rng, 1.2)
        panah(ld, [(x * S, y * S) for x, y in q], col, w * S, L=18 * S, lebar=1.0)

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    cx = 400
    # mulai (oval)
    mulai = bersih(p["mulai"])
    fm, lm, sm = susun(probe, mulai, coret, 560, 2 * 44 * 1.15, 42, 26, 1.15, maks_baris=2)
    mw = max(d.textlength(ln, font=fm) for ln in lm)
    rx, ry = max(170, mw / 2 + 56), max(52, len(lm) * sm * 1.15 / 2 + 26)
    y_m = 66 + ry
    gar(oval_pts(cx, y_m, rx, ry))
    # tanya (belah ketupat)
    yq = y_m + ry + 76 + 104
    qw, qh = 160, 104
    gar([(cx, yq - qh), (cx + qw, yq), (cx, yq + qh), (cx - qw, yq), (cx, yq - qh), (cx + 8, yq - qh + 5)])
    pan(garis_isi((cx, y_m + ry + 8), (cx, yq - qh - 8)))
    # tidak / belum (kanan) lalu kembali
    tx0, tx1 = 680, 1004
    ft_, lt, st = susun(probe, bersih(p["tidak"]), coret, tx1 - tx0 - 44, 3 * 34 * 1.12, 34, 22, 1.12)
    th = len(lt) * st * 1.12 + 46
    gar(kotak_pts(tx0, yq - th / 2, tx1, yq + th / 2))
    pan(garis_isi((cx + qw + 8, yq), (tx0 - 10, yq)), merah)
    tb = yq - th / 2
    pan(kurva(((tx0 + tx1) / 2, tb - 8), ((tx0 + tx1) / 2 - 60, yq - qh - 130), (cx + 40, yq - qh - 4 + 22), 30), merah, 3.6)
    # ya (bawah)
    yy = yq + qh
    kotak_ya = []
    for k, teks in enumerate(p["ya"][:2]):
        fy, ly, sy = susun(probe, bersih(teks), coret, 520, 2 * 36 * 1.12, 36, 24, 1.12, maks_baris=2)
        wbox = max(260, max(d.textlength(ln, font=fy) for ln in ly) + 70)
        hbox = len(ly) * sy * 1.12 + 40
        top = yy + 88
        pan(garis_isi((cx, yy + 8), (cx, top - 8)), hijau if k == 0 else tinta)
        gar(kotak_pts(cx - wbox / 2, top, cx + wbox / 2, top + hbox))
        kotak_ya.append((fy, ly, sy, top, hbox, wbox))
        yy = top + hbox
    # akhir (oval)
    akhir = bersih(p["akhir"])
    fa = muat(probe, akhir, coret, 380, 40, 24)
    arx = max(150, d.textlength(akhir, font=fa) / 2 + 60)
    ya_ = yy + 88 + 50
    pan(garis_isi((cx, yy + 8), (cx, ya_ - 50 - 8)))
    gar(oval_pts(cx, ya_, arx, 50))
    gar(oval_pts(cx, ya_, arx + 9, 59), w=2.4)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # stabilo di kotak ya kedua
    fy, ly, sy, top, hbox, wbox = kotak_ya[1]
    st_ = Image.new("RGBA", (int(wbox - 20), int(hbox - 18)), (255, 232, 90, 150))
    st_ = st_.rotate(-2, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(st_, (int(cx - st_.width / 2), int(top + hbox / 2 - st_.height / 2)))
    d = ImageDraw.Draw(img)
    tc = (30, 30, 30)

    def tengah(x, yc, lines, f, size, lh):  # baris-baris teks di tengah bentuk (pakai pusat tinggi huruf kecil)
        for k, ln in enumerate(lines):
            d.text((x, yc + (k - (len(lines) - 1) / 2) * size * lh + size * 0.06), ln, font=f, fill=tc, anchor="mm")
    tengah(cx, y_m, lm, fm, sm, 1.15)
    tanya = bersih(p["tanya"])
    fq = muat(d, tanya, coret, qw * 1.15, 42, 22)
    tengah(cx, yq, [tanya], fq, fq.size, 1)
    tengah((tx0 + tx1) / 2, yq, lt, ft_, st, 1.12)
    for fy, ly, sy, top, hbox, wbox in kotak_ya:
        tengah(cx, top + hbox / 2, ly, fy, sy, 1.12)
    tengah(cx, ya_, [akhir], fa, fa.size, 1)
    fl = coret(32)
    d.text(((cx + qw + tx0) / 2, yq - 14), "Belum", font=fl, fill=merah[:3], anchor="md")
    d.text((cx + 22, yq + qh + 40), "Ya", font=fl, fill=hijau[:3], anchor="lm")
    # coretan kecil di ruang kanan: ikan / perahu / jejak kaki (berganti tiap item)
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    biru_p = (60, 90, 140, 255)
    fx, fy_ = 840, (yq + qh + ya_) / 2 + 30
    if i % 3 == 0:
        badan = [(fx - 70 + 140 * t, fy_ - 34 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 20)] + \
                [(fx + 70 - 140 * t, fy_ + 30 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 20)]
        gar(badan, biru_p, 3.4)
        gar([(fx + 68, fy_), (fx + 110, fy_ - 30), (fx + 104, fy_), (fx + 110, fy_ + 30), (fx + 68, fy_)], biru_p, 3.4)
        ld.ellipse(((fx - 44) * S, (fy_ - 8) * S, (fx - 34) * S, (fy_ + 2) * S), fill=biru_p)
        for k in range(3):
            gar(oval_pts(fx - 100 - k * 26, fy_ - 40 - k * 30, 7 + k * 2, 7 + k * 2, 30), biru_p, 2.4)
    elif i % 3 == 1:
        gar([(fx - 100, fy_), (fx + 100, fy_), (fx + 70, fy_ + 46), (fx - 70, fy_ + 46), (fx - 100, fy_)], biru_p, 3.4)
        gar([(fx - 6, fy_), (fx - 6, fy_ - 130)], biru_p, 3.4)
        gar([(fx, fy_ - 124), (fx + 74, fy_ - 20), (fx, fy_ - 20)], biru_p, 3.4)
        for k in range(2):
            gar([(fx - 130 + t * 260, fy_ + 66 + k * 18 + 5 * math.sin(t * 14 + k)) for t in np.linspace(0, 1, 30)], biru_p, 2.6)
    else:
        for k, (dx, dy) in enumerate(((-60, 70), (10, 10), (-40, -60), (30, -120))):
            px_, py_ = fx + dx, fy_ + dy
            gar(oval_pts(px_, py_, 16, 26, 40), biru_p, 3)
            for j in range(4):
                gar(oval_pts(px_ - 12 + j * 8, py_ - 36 - (j % 2) * 3, 4, 5, 16), biru_p, 2.4)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    ytop = ya_ + 50 + 42
    d.line((80, ytop - 18, W - 80, ytop - 18), fill=(150, 160, 176), width=2)
    ayat_blok(d, p, 90, W - 90, ytop, H - 84, charter, (34, 36, 40), merah[:3], coret(30), start=34, stop=24, lh=1.38)
    kredit(d, (W / 2, H - 50), (120, 130, 146))
    return img


# ---------- LOWONGAN: selebaran dengan sobekan ----------

def gabus(w, h, seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array([196, 150, 100], np.float32)
    a *= (0.86 + 0.24 * render.fbm2d(h, w, rng, ((6, 1.0), (40, 0.6), (200, 0.5))))[..., None]
    bint = rng.random((h, w))
    a[bint < 0.05] = a[bint < 0.05] * 0.72
    a[(bint > 0.05) & (bint < 0.07)] *= 1.15
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))
    return grain(img, 0.08)


def pin(img, x, y, col=(220, 40, 40)):
    sh = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((22, 28, 62, 60), fill=(0, 0, 0, 120))
    comp(img, sh.filter(ImageFilter.GaussianBlur(5)), (x - 32, y - 30))

    def g(d, k):
        d.ellipse((4 * k, 4 * k, 40 * k, 40 * k), fill=tuple(int(c * 0.7) for c in col) + (255,))
        d.ellipse((7 * k, 4 * k, 39 * k, 36 * k), fill=col + (255,))
        d.ellipse((13 * k, 9 * k, 25 * k, 19 * k), fill=(255, 220, 220, 255))
    comp(img, sprite(44, 44, g, k=4), (x - 22, y - 22))


def lowongan_image(p, i):
    rng = np.random.default_rng(17800 + i)
    img = gabus(W, H, 17800 + i).convert("RGBA")
    # kertas lama di belakang
    for k in range(5):
        sw, sh_ = int(rng.uniform(220, 380)), int(rng.uniform(200, 340))
        col = [(238, 232, 210), (232, 214, 214), (214, 226, 236), (240, 236, 200), (226, 232, 214)][k]
        sc = Image.new("RGBA", (sw, sh_), col + (255,))
        sd = ImageDraw.Draw(sc)
        for yy in range(30, sh_ - 20, 26):
            sd.rectangle((24, yy, int(sw * rng.uniform(0.4, 0.9)), yy + 8), fill=campur(col, (150, 146, 140), 0.4))
        tor = [(x, sh_ - 6 + rng.uniform(-6, 6)) for x in np.linspace(0, sw, 16)]
        sd.polygon([(0, sh_)] + tor + [(sw, sh_)], fill=(0, 0, 0, 0))
        sc = sc.rotate(rng.uniform(-10, 10), expand=True, resample=Image.BICUBIC)
        x, y = [(-60, 40), (W - 260, -30), (-80, H - 330), (W - 300, H - 280), (W - 210, 520)][k]
        bayangan(img, sc, (x, y), blur=8, geser=(3, 6), kuat=0.3)
        pin(img, int(x + sc.width / 2), int(y + 26), [(60, 120, 220), (240, 180, 40), (40, 160, 90), (200, 80, 160), (60, 120, 220)][k])
    fw, fh = 860, 1150
    fl = Image.new("RGBA", (fw, fh), (250, 250, 246, 255))
    d = ImageDraw.Draw(fl)
    hitam = (24, 24, 24)
    X = 64
    judul = bersih(p["judul"]).upper()
    fj = muat(d, judul, impact, fw - 2 * X, 160, 70)
    d.text((X - 4, 54), judul, font=fj, fill=hitam)
    y = 54 + fj.size * 1.1
    sub = bersih(p["sub"]).upper()
    fs = muat(d, sub, lambda s: helv(s, 1), fw - 2 * X, 44, 24)
    d.text((X, y), sub, font=fs, fill=hitam)
    y += fs.size * 1.3 + 14
    d.rectangle((X, y, fw - X, y + 6), fill=hitam)
    y += 34
    fr, fb = helv(33, 0), helv(33, 1)
    for s_ in p["syarat"][:4]:
        t = bersih(s_)
        lab, _, isi_ = t.partition(":")
        d.rectangle((X, y + 9, X + 14, y + 23), fill=hitam)
        x = X + 32
        if isi_:
            words = [(lab + ":", fb)] + [(w_, fr) for w_ in isi_.split()]
        else:
            words = [(w_, fr) for w_ in t.split()]
        sp = d.textlength(" ", font=fr)
        for w_, f_ in words:
            wl = d.textlength(w_, font=f_)
            if x + wl > fw - X:
                x = X + 32
                y += 44
            d.text((x, y), w_, font=f_, fill=hitam)
            x += wl + sp
        y += 58
    y += 4
    d.line((X, y, fw - X, y), fill=(200, 200, 196), width=2)
    y += 22
    tab_h = 246
    y_tab = fh - tab_h
    rf = helv(27, 1)
    fv, vl, vs = susun(d, bersih(p["ayat"]), lambda s: charter(s, 1), fw - 2 * X - 30, y_tab - 40 - y - rf.size - 16, 36, 22, 1.38)
    tinggi = len(vl) * vs * 1.38 + rf.size + 16
    yv = y + max(0, (y_tab - 30 - y - tinggi) / 2)
    d.rectangle((X, yv + 4, X + 6, yv + tinggi - 4), fill=(220, 40, 40))
    for ln in vl:
        d.text((X + 30, yv), ln, font=fv, fill=(60, 60, 64))
        yv += vs * 1.38
    d.text((X + 30, yv + 16), p["ref"], font=rf, fill=(196, 40, 32))
    kredit(d, (fw - X, 30), (150, 150, 146), anchor="ra", size=20)
    # sobekan
    n_tab = 8
    tw = (fw - 2) / n_tab
    for k in range(1, n_tab):
        putus(d, [(k * tw, y_tab), (k * tw, fh)], (150, 150, 146), 2, (7, 6))
    putus(d, [(0, y_tab), (fw, y_tab)], (150, 150, 146), 2, (7, 6))
    ftab = kurir(21, True)
    tab = bersih(p["tab"])
    while d.textlength(tab, font=ftab) > tab_h - 30 and ftab.size > 14:
        ftab = kurir(ftab.size - 1, True)
    ts = Image.new("RGBA", (int(tab_h), int(tw)), (0, 0, 0, 0))
    ImageDraw.Draw(ts).text((tab_h / 2, tw / 2), tab, font=ftab, fill=hitam + (255,), anchor="mm")
    ts = ts.rotate(90, expand=True)
    for k in range(n_tab):
        comp(fl, ts, (k * tw, y_tab))
    robek = sorted({int(v) % n_tab for v in p.get("robek", [])})
    setengah = None
    for k in robek:
        for j in (k + 1, k - 1):
            if 0 <= j < n_tab and j not in robek:
                setengah = j
                break
        if setengah is not None:
            break
    alpha = fl.getchannel("A")
    ad = ImageDraw.Draw(alpha)
    for k in robek + ([setengah] if setengah is not None else []):
        x0, x1 = k * tw - (1 if k else 0), (k + 1) * tw + 2
        ys = y_tab + (16 if k in robek else 0)
        tepi = [(x, ys + rng.uniform(-5, 5)) for x in np.linspace(x0, x1, 9)]
        ad.polygon(tepi + [(x1, fh), (x0, fh)], fill=0)
    potongan = None
    if setengah is not None:
        k = setengah
        potongan = fl.crop((int(k * tw + 2), int(y_tab + 4), int((k + 1) * tw - 1), fh)).copy()
        pa = np.asarray(potongan).astype(np.float32)
        pa[..., 3] = 255
        g = np.linspace(1.0, 0.8, pa.shape[1])[None, :, None]
        pa[..., :3] *= g
        potongan = Image.fromarray(np.clip(pa, 0, 255).astype(np.uint8))
        pd = ImageDraw.Draw(potongan)
        pd.line((0, 0, potongan.width, 0), fill=(150, 150, 146, 255), width=2)
    fl.putalpha(alpha)
    if potongan is not None:
        k = setengah
        pr = potongan.rotate(-16, expand=True, resample=Image.BICUBIC, center=(potongan.width / 2, 0))
        bayangan(fl, pr, (k * tw - 6, y_tab + 4), blur=6, geser=(6, 8), kuat=0.35)
    fl = fl.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    fx, fy = (W - fl.width) / 2, 92
    bayangan(img, fl, (fx, fy), blur=16, geser=(6, 12), kuat=0.45)
    pin(img, int(W / 2), int(fy + 34))
    return img


# ---------- UPAH: amplop upah kertas kraft ----------

def upah_image(p, i):
    rng = np.random.default_rng(17900 + i)
    meja = np.zeros((H, W, 3), np.float32) + np.array([58, 50, 44], np.float32)
    meja *= (0.8 + 0.35 * render.fbm2d(H, W, rng, ((3, 1.0), (30, 0.4), (160, 0.3))))[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    meja *= (1.15 - 0.45 * np.hypot((xx - W * 0.45) / W, (yy - H * 0.4) / H))[..., None]
    img = Image.fromarray(np.clip(meja, 0, 255).astype(np.uint8)).convert("RGBA")
    ew, eh = 820, 880
    ex, ey = (W - ew) // 2, H - eh - 76
    kraft = [(196, 160, 112), (204, 170, 122), (186, 150, 104)][i % 3]

    def kertas_kraft(w, h, seed, gelap=1.0):
        r2 = np.random.default_rng(seed)
        a = np.zeros((h, w, 3), np.float32) + np.array(kraft, np.float32) * gelap
        a *= (0.92 + 0.12 * render.fbm2d(h, w, r2, ((4, 1.0), (40, 0.5), (200, 0.4))))[..., None]
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
        serat = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dd = ImageDraw.Draw(serat)
        for _ in range(int(400 * w * h / (820 * 880))):
            x, y = r2.uniform(0, w), r2.uniform(0, h)
            ang, L = r2.uniform(0, math.pi), r2.uniform(5, 16)
            col = (150, 114, 70, 34) if r2.random() < 0.6 else (226, 196, 150, 40)
            dd.line((x, y, x + math.cos(ang) * L, y + math.sin(ang) * L), fill=col, width=1)
        im.alpha_composite(serat)
        return im
    # bagian belakang + tutup terbuka
    belakang = kertas_kraft(ew, 120, 17910 + i, 0.8)
    comp(img, belakang, (ex, ey - 30))
    tutup = Image.new("RGBA", (ew, 260), (0, 0, 0, 0))
    tm = Image.new("L", (ew, 260), 0)
    ImageDraw.Draw(tm).polygon([(0, 259), (ew, 259), (ew / 2 + 40, 6), (ew / 2, 0), (ew / 2 - 40, 6)], fill=255)
    tk = kertas_kraft(ew, 260, 17920 + i, 0.94)
    lem = Image.new("RGBA", (ew, 260), (0, 0, 0, 0))  # pita lem di tepi tutup
    ImageDraw.Draw(lem).line([(30, 252), (ew / 2, 14), (ew - 30, 252)], fill=(160, 124, 80, 90), width=16, joint="curve")
    tk.alpha_composite(lem)
    tutup.paste(tk, (0, 0), tm)
    bayangan(img, tutup, (ex, ey - 30 - 258), blur=10, geser=(0, -4), kuat=0.3)
    # koin mengintip
    koin = sprite(150, 150, lambda d_, k: (d_.ellipse((2 * k, 2 * k, 148 * k, 148 * k), fill=(176, 144, 70, 255)),
                                          d_.ellipse((10 * k, 10 * k, 140 * k, 140 * k), fill=(204, 172, 92, 255)),
                                          d_.ellipse((16 * k, 16 * k, 134 * k, 134 * k), outline=(170, 138, 64, 255), width=2 * k)), k=3)
    kd = ImageDraw.Draw(koin)
    for (gx, gy) in [(75, 48), (62, 62), (88, 62), (50, 76), (75, 76), (100, 76), (62, 90), (88, 90), (75, 104)]:
        kd.ellipse((gx - 9, gy - 9, gx + 9, gy + 9), fill=(222, 192, 110, 255), outline=(160, 128, 58, 255), width=2)
    kd.line((75, 40, 82, 24, 96, 20), fill=(160, 128, 58, 255), width=3, joint="curve")
    kil_ = Image.new("RGBA", koin.size, (0, 0, 0, 0))
    ImageDraw.Draw(kil_).ellipse((30, 28, 70, 50), fill=(250, 230, 170, 120))
    koin.alpha_composite(kil_)
    koin = koin.rotate(14, resample=Image.BICUBIC)
    bayangan(img, koin, (ex + (ew - 300, 120, ew / 2 - 40)[i % 3], ey - 96), blur=8, geser=(4, 6), kuat=0.5)
    depan = kertas_kraft(ew, eh, 17930 + i)
    dd = ImageDraw.Draw(depan)
    tinta = (50, 36, 24)
    X = 56
    judul = bersih(p["judul"]).upper()
    fj = din(54)
    while lebar_renggang(dd, judul, fj, 3) > ew - 2 * X and fj.size > 28:
        fj = din(fj.size - 1)
    y = 56
    renggang(dd, (ew / 2, y), judul, fj, tinta, 3, anchor="ma")
    y += fj.size + 18
    dd.line((X, y, ew - X, y), fill=tinta, width=3)
    dd.line((X, y + 6, ew - X, y + 6), fill=tinta, width=1)
    y += 26
    kol = [X, X + 150, X + 420, X + 580, ew - X]
    for k, lab in enumerate(("MULAI", "NAMA", "UPAH", "PARAF")):
        renggang(dd, (kol[k] + 10, y), lab, din(28), tinta, 2)
    y += 44
    dd.line((X, y, ew - X, y), fill=tinta, width=2)
    fr = kurir(36, True)
    baris = p["baris"][:5]
    y_atas = y
    for k, (jam, nama, upah) in enumerate(baris):
        yr = y + 14
        for c, t in enumerate((bersih(jam), bersih(nama), bersih(upah))):
            ff = fr
            while dd.textlength(t, font=ff) > kol[c + 1] - kol[c] - 20 and ff.size > 18:
                ff = kurir(ff.size - 1, True)
            dd.text((kol[c] + 10, yr + 2 + (fr.size - ff.size) * 0.6), t, font=ff, fill=tinta)
        if k < len(baris) - 1:  # paraf tangan
            px0, pyc = kol[3] + 22, y + 33
            pts = [(px0 + t * 80, pyc + 10 * math.sin(t * 15 + k) * (1 - t * 0.6) - t * 6) for t in np.linspace(0, 1, 40)]
            dd.line(pts, fill=(56, 50, 90), width=3, joint="curve")
            dd.line((px0 + 6, pyc + 14, px0 + 86, pyc + 8), fill=(56, 50, 90), width=2)
        y += 66
        putus(dd, [(X, y), (ew - X, y)], (120, 92, 62), 2, (6, 5))
    y_cap = y - 66
    for xk in kol[1:-1]:
        dd.line((xk, y_atas - 44, xk, y), fill=(120, 92, 62), width=1)
    y += 30
    rf = din(30)
    f, lines, size = susun(dd, bersih(p["ayat"]), mesin, ew - 2 * X - 20, eh - y - 70 - rf.size, 40, 22, 1.4)
    for ln in lines:
        dd.text((X + 10, y), ln, font=f, fill=(60, 44, 30))
        y += size * 1.4
    renggang(dd, (ew - X - 10, y + 12), p["ref"].upper(), rf, (150, 40, 30), 2, anchor="ra")
    # cap merah
    cap = bersih(p["cap"]).upper()
    fc = din(60)
    while dd.textlength(cap, font=fc) > 128 and fc.size > 26:
        fc = din(fc.size - 1)
    cw_ = int(dd.textlength(cap, font=fc) + 44)
    st = Image.new("RGBA", (cw_, 92), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    merah = (200, 40, 40)
    sd.rounded_rectangle((3, 3, cw_ - 4, 88), radius=9, outline=merah + (255,), width=5)
    sd.rounded_rectangle((11, 11, cw_ - 12, 80), radius=5, outline=merah + (255,), width=2)
    sd.text((cw_ / 2, 49), cap, font=fc, fill=merah + (255,), anchor="mm")
    st = st.rotate(-8, expand=True, resample=Image.BICUBIC)
    sa = np.asarray(st).astype(np.float32)
    nz = render.fbm2d(sa.shape[0], sa.shape[1], rng, ((6, 1.0), (24, 0.6)))
    sa[..., 3] *= (nz > 0.24) * 0.9
    sa[..., 3] *= (rng.random(nz.shape) > 0.06)
    st = Image.fromarray(np.clip(sa, 0, 255).astype(np.uint8))
    # cap ditimpa seperti tinta (multiply) di baris terakhir supaya tulisan di bawahnya tetap terbaca
    sx = int(min(ew - 14 - st.width, (kol[3] + kol[4]) / 2 - st.width / 2 + 8))
    sy = int(y_cap + 33 - st.height / 2)
    reg = np.asarray(depan.crop((sx, sy, sx + st.width, sy + st.height))).astype(np.float32)
    sa = np.asarray(st).astype(np.float32)
    al = sa[..., 3:4] / 255 * 0.9
    reg[..., :3] = reg[..., :3] * (1 - al + al * sa[..., :3] / 255 * 1.08)
    depan.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8)), (sx, sy))
    sh = Image.new("RGBA", (ew + 60, eh + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((30, 30, ew + 30, eh + 30), fill=(0, 0, 0, 130))
    comp(img, sh.filter(ImageFilter.GaussianBlur(16)), (ex - 30 + 8, ey - 30 + 14))
    comp(img, depan, (ex, ey))
    d = ImageDraw.Draw(img)
    kredit(d, (W / 2, H - 46), (196, 184, 170))
    return img


# ---------- BEKAL: lima roti dua ikan ----------

def roti(r, rng):
    w, h = int(r * 2.1), int(r * 2.0)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = (xx - w / 2) / (r * 1.02), (yy - h / 2) / r
    r2 = u * u + v * v
    a = np.clip((1 - r2) * r * 0.6, 0, 1)
    t = np.clip(np.sqrt(r2), 0, 1)
    lt = np.clip(0.55 - 0.45 * (u * 0.6 + v * 0.8), 0, 1)
    tengah = np.array([238, 200, 130], np.float32)
    tepi = np.array([200, 140, 66], np.float32)
    rgb = tengah * (1 - t[..., None] ** 1.6) + tepi * t[..., None] ** 1.6
    rgb *= (0.86 + 0.26 * lt)[..., None]
    rgb *= (0.94 + 0.1 * render.fbm2d(h, w, rng, ((6, 1.0), (24, 0.5))))[..., None]
    img = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(img)
    rot = rng.uniform(-0.5, 0.5)
    for k in (-1, 0, 1):  # tiga goresan
        cx, cy = w / 2 + k * r * 0.42, h / 2
        pts = []
        for t_ in np.linspace(-0.6, 0.6, 16):
            x, y = cx + r * 0.16 * math.sin(t_ * 2.4), cy + t_ * r * 1.05
            pts.append((w / 2 + (x - w / 2) * math.cos(rot) - (y - h / 2) * math.sin(rot), h / 2 + (x - w / 2) * math.sin(rot) + (y - h / 2) * math.cos(rot)))
        d.line(pts, fill=(150, 96, 44, 255), width=4, joint="curve")
        d.line([(x + 2, y + 1) for x, y in pts], fill=(248, 222, 166, 255), width=2, joint="curve")
    tp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(tp)
    for _ in range(40):  # taburan tepung
        x, y = w / 2 + rng.normal(0, r * 0.35), h / 2 + rng.normal(0, r * 0.35)
        s = rng.uniform(0.8, 2)
        td.ellipse((x - s, y - s, x + s, y + s), fill=(255, 250, 236, int(rng.uniform(60, 160))))
    tp.putalpha(Image.fromarray(np.minimum(np.asarray(tp.getchannel("A")), np.asarray(img.getchannel("A")))))
    img.alpha_composite(tp)
    return img


def ikan_bakar(L, rng):
    h = int(L * 0.33)
    m = Image.new("L", (L * 3, h * 3), 0)
    md = ImageDraw.Draw(m)
    badan = [(L * 3 * (0.04 + 0.70 * t), h * 3 * (0.5 - 0.42 * math.sin(math.pi * t ** 0.8))) for t in np.linspace(0, 1, 30)] + \
            [(L * 3 * (0.04 + 0.70 * t), h * 3 * (0.5 + 0.38 * math.sin(math.pi * t ** 0.8))) for t in np.linspace(1, 0, 30)]
    md.polygon(badan, fill=255)
    md.polygon([(L * 3 * 0.70, h * 1.5), (L * 3 * 0.97, h * 3 * 0.12), (L * 3 * 0.91, h * 1.5), (L * 3 * 0.97, h * 3 * 0.88)], fill=255)
    m = m.resize((L, h), Image.LANCZOS)
    yy = np.mgrid[0:h, 0:L][0].astype(np.float32)
    v = (yy - h / 2) / (h / 2)
    rgb = np.array([150, 140, 120], np.float32) * (1.05 - 0.25 * np.abs(v) ** 2)[..., None]
    rgb = rgb * (0.9 + 0.15 * render.fbm2d(h, L, rng, ((5, 1.0), (20, 0.5))))[..., None]
    gm = Image.new("L", (L, h), 0)  # bekas panggangan: pita serong lembut
    gd = ImageDraw.Draw(gm)
    for k in range(6):
        x0 = L * (0.16 + k * 0.1) + rng.uniform(-4, 4)
        gd.line((x0, h * 0.05, x0 + h * 0.55, h * 0.95), fill=int(rng.uniform(170, 230)), width=max(3, int(L * 0.018)))
    gm = np.asarray(gm.filter(ImageFilter.GaussianBlur(1.6)), np.float32)[..., None] / 255
    rgb = rgb * (1 - gm * 0.75) + np.array([70, 50, 40]) * gm * 0.75
    rgb += (np.exp(-((v + 0.35) / 0.18) ** 2) * 30)[..., None]
    img = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.asarray(m)]).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(img)
    d.arc((L * 0.12, h * 0.18, L * 0.26, h * 0.86), 290, 70, fill=(90, 70, 56, 255), width=3)
    d.ellipse((L * 0.07, h * 0.36, L * 0.12, h * 0.5), fill=(240, 236, 226, 255))
    d.ellipse((L * 0.085, h * 0.39, L * 0.11, h * 0.47), fill=(30, 26, 24, 255))
    return img


def bekal_image(p, i):
    rng = np.random.default_rng(18000 + i)
    linen = kertas_tekstur(W, H, (232, 226, 214), 18000 + i, 0.03, serat=0.04)
    a = np.asarray(linen).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    garis = ((xx % 48) < 10) | ((yy % 48) < 10)
    a[garis] = a[garis] * 0.955
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    # serbet merah di bawah sudut kotak
    sv = Image.new("RGBA", (460, 460), (180, 70, 50, 255))
    sd = ImageDraw.Draw(sv)
    for k in range(0, 460, 6):
        sd.line((k, 0, k, 460), fill=(172, 66, 47), width=1)
    for k in range(0, 460, 26):
        for e in (18, 442):
            sd.polygon([(k + 13, e - 8), (k + 21, e), (k + 13, e + 8), (k + 5, e)], fill=(246, 230, 214, 255))
            sd.polygon([(e - 8, k + 13), (e, k + 21), (e + 8, k + 13), (e, k + 5)], fill=(246, 230, 214, 255))
    sv = sv.rotate(28 + 8 * (i % 2), expand=True, resample=Image.BICUBIC)
    nap_x = (-250, W - 380, -250)[i % 3]
    bayangan(img, sv, (nap_x, -200), blur=10, geser=(4, 8), kuat=0.3)
    # kotak kayu
    bw, bh = 900, 540
    kotak = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    kayu = np.zeros((bh, bw, 3), np.float32) + np.array([176, 124, 80], np.float32)
    ky = np.mgrid[0:bh, 0:bw][0].astype(np.float32)
    kayu *= (0.86 + 0.14 * (0.5 + 0.5 * np.sin(ky * 0.25 + 6 * render.fbm2d(bh, bw, rng, ((3, 1.0), (8, 0.4))))) ** 3)[..., None]
    kayu *= (0.92 + 0.1 * render.fbm2d(bh, bw, rng, ((4, 1.0), (30, 0.5))))[..., None]
    km = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(km).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=28, fill=255)
    kotak.paste(Image.fromarray(np.clip(kayu, 0, 255).astype(np.uint8)), (0, 0), km)
    rim, div = 30, int(bw * 0.58)
    inner = [(rim, rim, div - 10, bh - rim), (div + 10, rim, bw - rim, bh - rim)]
    kd = ImageDraw.Draw(kotak)
    for x0, y0, x1, y1 in inner:
        kd.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=(150, 104, 66, 255))
        bay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bay)
        bd.rounded_rectangle((x0, y0, x1, y1), radius=14, outline=(40, 24, 12, 170), width=16)
        bm = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(bm).rounded_rectangle((x0, y0, x1, y1), radius=14, fill=255)
        bay = bay.filter(ImageFilter.GaussianBlur(9))
        bay.putalpha(Image.fromarray(np.minimum(np.asarray(bay.getchannel("A")), np.asarray(bm))))
        kotak.alpha_composite(bay)
    kd = ImageDraw.Draw(kotak)
    kd.rounded_rectangle((2, 2, bw - 3, bh - 3), radius=28, outline=(214, 170, 120, 255), width=3)
    # lima roti
    x0, y0, x1, y1 = inner[0]
    ccx, ccy = (x0 + x1) / 2, (y0 + y1) / 2
    r = 84
    for (dx, dy) in [(-118, -100), (118, -100), (0, 0), (-118, 100), (118, 100)]:
        rt = roti(r * rng.uniform(0.96, 1.04), rng).rotate(rng.uniform(0, 360), resample=Image.BICUBIC)
        sh = Image.new("RGBA", rt.size, (0, 0, 0, 0))
        sh.paste((40, 20, 0, 255), (0, 0), rt.getchannel("A").point(lambda v: int(v * 0.4)))
        comp(kotak, sh.filter(ImageFilter.GaussianBlur(6)), (ccx + dx - rt.width / 2 + 5, ccy + dy - rt.height / 2 + 8))
        comp(kotak, rt, (ccx + dx - rt.width / 2 + rng.uniform(-6, 6), ccy + dy - rt.height / 2 + rng.uniform(-6, 6)))
    # dua ikan
    x0, y0, x1, y1 = inner[1]
    ccx = (x0 + x1) / 2
    for k, dx in enumerate((-80, 80)):
        ik = ikan_bakar(430, rng)
        ik = ik.rotate(90 if k == 0 else -90, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", ik.size, (0, 0, 0, 0))
        sh.paste((40, 20, 0, 255), (0, 0), ik.getchannel("A").point(lambda v: int(v * 0.4)))
        comp(kotak, sh.filter(ImageFilter.GaussianBlur(6)), (ccx + dx - ik.width / 2 + 5, (y0 + y1) / 2 - ik.height / 2 + 8))
        comp(kotak, ik, (ccx + dx - ik.width / 2, (y0 + y1) / 2 - ik.height / 2))
    kd = ImageDraw.Draw(kotak)
    for (lx, ly, ang) in [(ccx - 6, y0 + 40, 0.4), (ccx + 4, y1 - 46, -0.6)]:  # daun herba
        for s_ in (-1, 1):
            ex, ey = lx + math.cos(ang + s_ * 0.9) * 26, ly + math.sin(ang + s_ * 0.9) * 26
            kd.ellipse((ex - 11, ey - 6, ex + 11, ey + 6), fill=(92, 140, 70, 255))
        kd.line((lx - 20, ly + 10, lx + 20, ly - 10), fill=(70, 110, 50, 255), width=2)
    kotak = kotak.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    bx, by = (W - kotak.width) / 2, 96
    bayangan(img, kotak, (bx, by), blur=22, geser=(8, 18), kuat=0.45)
    # catatan kecil terlipat
    catatan = bersih(p["catatan"])
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fc = muat(probe, catatan, bradley, 380, 34, 20)
    nw, nh = int(probe.textlength(catatan, font=fc) + 70), 96
    note = Image.new("RGBA", (nw, nh), (252, 248, 236, 255))
    nd = ImageDraw.Draw(note)
    nd.line((0, nh * 0.32, nw, nh * 0.32), fill=(220, 210, 190, 255), width=2)
    nd.rectangle((0, 0, nw, nh * 0.32), fill=(244, 238, 222, 255))
    nd.text((nw / 2, nh * 0.64), catatan, font=fc, fill=(40, 50, 90, 255), anchor="mm")
    note = note.rotate(4, expand=True, resample=Image.BICUBIC)
    nx = min(W - 74 - note.width, bx + kotak.width - note.width * 0.7)
    bayangan(img, note, (nx, by + kotak.height - 70), blur=8, geser=(3, 7), kuat=0.35)
    d = ImageDraw.Draw(img)
    y = by + kotak.height + 64
    f, lines, size = susun(d, bersih(p["baris"]), lambda s: iowan(s, 2), W - 180, 2 * 44 * 1.2, 44, 30, 1.2)
    lines = seimbang(d, lines, f)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(70, 46, 30), anchor="ma")
        y += size * 1.2
    d.line((W / 2 - 40, y + 18, W / 2 + 40, y + 18), fill=(180, 70, 50), width=3)
    ayat_blok(d, p, 100, W - 100, y + 40, H - 86, charter, (64, 50, 40), (180, 70, 50), iowan(30, 3), start=34, stop=24, lh=1.38)
    kredit(d, (W / 2, H - 50), (150, 136, 118))
    return img


# ---------- DOMINO (Reels): satu panggilan menjatuhkan yang lain ----------

def _sudut_kontak(Pk, Pn, Wd, Hd, phi):
    """Sudut jatuh maksimum domino k (pivot Pk di pojok kanan bawah, sumbu y ke atas) sebelum menyentuh
    domino berikut (pivot Pn) yang sedang miring phi radian."""
    bl = (Pn[0] - Wd * math.cos(phi), Pn[1] + Wd * math.sin(phi))  # pojok kiri bawah domino berikut
    arah = (math.sin(phi), math.cos(phi))  # arah muka kiri ke atas
    nrm = (math.cos(phi), -math.sin(phi))  # normal ke dalam domino berikut

    def jarak(th):  # (kedalaman pojok kanan atas domino k ke dalam muka kiri, posisi sepanjang muka)
        c = (Pk[0] + Hd * math.sin(th), Pk[1] + Hd * math.cos(th))
        v = (c[0] - bl[0], c[1] - bl[1])
        return v[0] * nrm[0] + v[1] * nrm[1], v[0] * arah[0] + v[1] * arah[1]
    hasil = math.pi / 2
    if jarak(math.pi / 2)[0] > 0:  # (1) pojok kanan atas k menyentuh muka kiri domino berikut
        lo, hi = 0.0, math.pi / 2
        for _ in range(40):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if jarak(m)[0] < 0 else (lo, m)
        if 0 <= jarak(lo)[1] <= Hd + 1:
            hasil = lo
    # (2) pojok kiri atas domino berikut menyentuh muka kanan domino k
    T = (Pn[0] - Wd * math.cos(phi) + Hd * math.sin(phi), Pn[1] + Wd * math.sin(phi) + Hd * math.cos(phi))
    dx, dy = T[0] - Pk[0], T[1] - Pk[1]
    if math.hypot(dx, dy) <= Hd and dy > 0:
        hasil = min(hasil, math.atan2(dx, dy))
    return max(0.0, hasil)


def domino_reel(p, idx, mod=MOD, seconds=12):
    rel = f"reels/{mod}/domino{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    nama = [bersih(n) for n in p["nama"]][:14]
    N = len(nama)
    Wd, Hd, sp = 58, 300, 100
    X0 = 160
    xs = [X0 + k * sp for k in range(N)]
    piv = [(x + Wd, 0.0) for x in xs]
    bel_x = piv[-1][0] + 222
    bel_h = 26 + 128  # puncak tombol bel
    dunia = (-300, bel_x + 200)
    FLOOR = 1340
    navy, merah, krem = (30, 40, 90), (230, 70, 50), (246, 238, 220)
    bg = kertas_tekstur(RW, RH, (246, 240, 228), 18100 + idx, 0.02).convert("RGBA")
    # sprite domino (dunia: 1 px = 1 unit pada zoom 1)
    K = 2
    spr = []
    for k, nm in enumerate(nama):
        col = merah if k == N - 1 else navy
        s_ = Image.new("RGBA", (Wd * K, Hd * K), (0, 0, 0, 0))
        sd = ImageDraw.Draw(s_)
        sd.rounded_rectangle((0, 0, Wd * K - 1, Hd * K - 1), radius=9 * K, fill=col + (255,))
        sd.rounded_rectangle((3 * K, 3 * K, Wd * K - 4 * K, Hd * K * 0.5), radius=8 * K, fill=tuple(min(255, c + 16) for c in col) + (255,))
        for yy in (16, Hd - 16):
            sd.ellipse(((Wd / 2 - 5) * K, (yy - 5) * K, (Wd / 2 + 5) * K, (yy + 5) * K), fill=krem + (255,))
        f = futura(40 * K, 2)
        while (sd.textlength(nm, font=f) > (Hd - 76) * K) and f.size > 18 * K:
            f = futura(f.size - K, 2)
        t = Image.new("RGBA", (Hd * K, Wd * K), (0, 0, 0, 0))
        ImageDraw.Draw(t).text((Hd * K / 2, Wd * K / 2 + 2 * K), nm, font=f, fill=krem + (255,), anchor="mm")
        s_.alpha_composite(t.rotate(90, expand=True))
        spr.append(s_.resize((Wd * 2, Hd * 2), Image.LANCZOS))  # simpan 2x untuk zoom
    T0, T1 = 2.6, 8.6
    dtk = (T1 - T0) / N
    th_c = math.asin((sp - Wd) / Hd)
    th_bel = math.atan2(bel_x - piv[-1][0], bel_h)
    t_bel = None

    def bebas(k, t):
        if t < T0 + k * dtk:
            return 0.0
        u = (t - (T0 + k * dtk)) / dtk
        return min(math.pi / 2, th_c * u * u)

    def sudut_semua(t):
        th = [0.0] * N
        th[-1] = min(bebas(N - 1, t), th_bel)
        for k in range(N - 2, -1, -1):
            th[k] = min(bebas(k, t), _sudut_kontak(piv[k], piv[k + 1], Wd, Hd, th[k + 1]))
        return th
    # waktu domino terakhir menyentuh bel
    for n in range(int(seconds * FPS * 4)):
        t = n / (FPS * 4)
        if bebas(N - 1, t) >= th_bel:
            t_bel = t
            break
    t_bel = t_bel or 9.0
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fj, lj, sj = susun(probe, bersih(p["judul"]), lambda s: rounded(s, "Bold"), RW - 200, 2 * 68 * 1.12, 68, 40, 1.12)
    lj = seimbang(probe, lj, fj)
    judul = Image.new("RGBA", (RW, int(len(lj) * sj * 1.12 + 20)), (0, 0, 0, 0))
    jd = ImageDraw.Draw(judul)
    for k, ln in enumerate(lj):
        jd.text((RW / 2, k * sj * 1.12), ln, font=fj, fill=navy + (255,), anchor="ma")
    fv, vl, vs = susun(probe, tanpa_kutip(p["ayat"]), lambda s: iowan(s, 2), RW - 180, 380, 54, 32, 1.32)
    ayat = Image.new("RGBA", (RW, int(len(vl) * vs * 1.34 + 70)), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=fv, fill=(50, 44, 40, 255), anchor="ma")
        y += vs * 1.32
    ad.text((RW / 2, y + 16), p["ref"], font=rounded(38, "Bold"), fill=merah + (255,), anchor="ma")
    y_judul = 440
    y_ayat = y_judul + judul.height + 40
    z0 = 0.8
    cx_awal = -280 + (RW / 2 - 50) / z0  # landasan di tepi kiri, deretan domino berlanjut ke kanan

    def kamera(t):
        depan = xs[min(N - 1, max(0, int((t - T0) / dtk)))] + Wd
        cx_semua = cx_awal
        if t < 2.3:
            return cx_semua, z0
        z1 = 1.0
        if t < 3.4:
            u = ease((t - 2.3) / 1.1)
            cx_ = cx_semua + (max(xs[0] + 300, min(depan, dunia[1] - 540)) - cx_semua) * u
            return cx_, z0 + (z1 - z0) * u
        if t < t_bel + 0.3:
            target = max(xs[0] + 300, min(depan + 120, dunia[1] - 540))
            return target, z1
        u = ease((t - t_bel - 0.3) / 1.4)
        a = max(xs[0] + 300, min(xs[-1] + 120 + 120, dunia[1] - 540))
        return a + (bel_x - 200 - a) * u * 0.4, z1 - 0.12 * u
    # haluskan kamera
    cam = []
    prev = None
    for n in range(seconds * FPS):
        c, z = kamera(n / FPS)
        if prev is not None:
            c = prev[0] + (c - prev[0]) * 0.12
            z = prev[1] + (z - prev[1]) * 0.18
        prev = (c, z)
        cam.append(prev)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        cxw, z = cam[n]

        def S(x, y):
            return ((x - cxw) * z + RW / 2, FLOOR - y * z)
        frame = bg.copy()
        d = ImageDraw.Draw(frame)
        d.rectangle((0, FLOOR, RW, RH), fill=(226, 216, 196, 255))
        d.line((0, FLOOR, RW, FLOOR), fill=(200, 190, 170), width=4)
        # landasan miring + bola
        r0, r1 = (-280, 330), (xs[0] - 40, 214)
        q0, q1 = S(*r0), S(*r1)
        d.line((q0, q1), fill=(176, 140, 100), width=max(2, int(12 * z)))
        tiang = S(r0[0] + 30, 0)
        d.line((S(r0[0] + 30, r0[1] - 10), tiang), fill=(160, 126, 90), width=max(2, int(10 * z)))
        br = 34
        if t < 2.0:
            bu = 0.0
        else:
            bu = min(1.0, ((t - 2.0) / 0.6) ** 2)
        if t <= 2.6:
            bxw = r0[0] + 40 + (r1[0] + 30 - (r0[0] + 40)) * bu
            byw = r0[1] + (r1[1] - r0[1]) * (bxw - r0[0]) / (r1[0] - r0[0]) + br + 4
        else:
            u = min(1.0, (t - 2.6) / 0.5)
            bxw = r1[0] + 30 - 26 * math.sin(u * math.pi * 0.5)
            byw = r1[1] + br + 4
        bc = S(bxw, byw)
        rr = br * z
        d.ellipse((bc[0] - rr, bc[1] - rr, bc[0] + rr, bc[1] + rr), fill=(250, 200, 40))
        d.ellipse((bc[0] - rr * 0.5, bc[1] - rr * 0.6, bc[0] - rr * 0.05, bc[1] - rr * 0.2), fill=(255, 236, 170))
        # bel meja
        bxs = S(bel_x, 0)
        bw_ = 150 * z
        d.rounded_rectangle((bxs[0] - bw_ / 2, bxs[1] - 26 * z, bxs[0] + bw_ / 2, bxs[1]), radius=6 * z, fill=(110, 76, 50))
        kubah = S(bel_x, 26)
        goyang_ = math.sin((t - t_bel) * 40) * 3 * z * max(0, 1 - (t - t_bel) / 0.8) if t >= t_bel else 0
        kx_ = kubah[0] + goyang_
        d.pieslice((kx_ - 66 * z, kubah[1] - 90 * z, kx_ + 66 * z, kubah[1] + 90 * z), 180, 360, fill=(226, 184, 70))
        d.pieslice((kx_ - 46 * z, kubah[1] - 76 * z, kx_ + 20 * z, kubah[1] + 40 * z), 200, 290, fill=(250, 226, 150))
        d.rectangle((kx_ - 66 * z, kubah[1] - 3 * z, kx_ + 66 * z, kubah[1] + 2 * z), fill=(180, 140, 50))
        d.rectangle((kx_ - 5 * z, kubah[1] - 140 * z, kx_ + 5 * z, kubah[1] - 88 * z), fill=(120, 120, 126))
        tekan = 6 * z if t_bel <= t < t_bel + 0.25 else 0
        d.ellipse((kx_ - 20 * z, kubah[1] - 128 * z + tekan, kx_ + 20 * z, kubah[1] - 112 * z + tekan), fill=(150, 150, 156))
        if t >= t_bel:  # kilat + gelombang bunyi
            u = (t - t_bel)
            if u < 1.2:
                kil = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
                kd = ImageDraw.Draw(kil)
                for j in range(3):
                    rr = (60 + j * 46 + u * 160) * z
                    a = int(220 * max(0, 1 - u / 1.2))
                    kd.arc((kubah[0] - rr, kubah[1] - 60 * z - rr, kubah[0] + rr, kubah[1] - 60 * z + rr), 200, 340, fill=(240, 160, 40, a), width=max(2, int(6 * z)))
                g = int(140 * max(0, 1 - u / 0.5))
                kd.ellipse((kubah[0] - 150 * z, kubah[1] - 220 * z, kubah[0] + 150 * z, kubah[1] + 60 * z), fill=(255, 236, 170, g))
                frame.alpha_composite(kil.filter(ImageFilter.GaussianBlur(3)))
        # domino
        th = sudut_semua(t)
        for k in range(N):
            muncul = t - k * 0.05
            if muncul <= 0:
                continue
            sy = 1.0
            if muncul < 0.45:
                u = muncul / 0.45
                sy = max(0.02, 1 + 0.1 * math.sin(u * math.pi) - (1 - ease(u)) * 1.0)
            dw, dh_ = max(2, int(Wd * z)), max(2, int(Hd * z * sy))
            im = spr[k].resize((dw, dh_), Image.BILINEAR)
            ang = math.degrees(th[k])
            pvx, pvy = S(*piv[k])
            if ang > 0.05:
                big = Image.new("RGBA", (dw * 2 + 2 * dh_, dh_ * 2 + 2), (0, 0, 0, 0))
                ox, oy = dh_ + dw, dh_
                big.alpha_composite(im, (ox - dw, oy - dh_))
                big = big.rotate(-ang, resample=Image.BICUBIC, center=(ox, oy))
                comp(frame, big, (pvx - ox, pvy - oy))
            else:
                comp(frame, im, (pvx - dw, pvy - dh_))
        if t >= 1.0:
            frame.alpha_composite(fade(judul, ease((t - 1.0) / 0.7)), (0, y_judul))
        if t >= 9.6:
            frame.alpha_composite(fade(ayat, ease((t - 9.6) / 0.9)), (0, y_ayat))
        kredit(ImageDraw.Draw(frame), (RW / 2, 1500), (150, 140, 126), size=28)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- RADIO (Reels): mencari frekuensi ----------

def radio_reel(p, idx, mod=MOD, seconds=13):
    rel = f"reels/{mod}/radio{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(18200 + idx)
    try:
        frek = float(str(p["frekuensi"]).replace(",", "."))
    except ValueError:
        frek = 103.1
    frek = min(108.0, max(88.0, frek))
    gangguan = [bersih(g).upper() for g in p["gangguan"]][:4]
    lcd_akhir = bersih(p["lcd"]).upper()
    bg = gradasi(RW, RH, (232, 226, 214), (214, 206, 192)).convert("RGBA")
    bg = grain(bg.convert("RGB"), 0.03).convert("RGBA")
    # panel radio (dicache)
    bx0, by0, bx1, by1 = 70, 444, RW - 70, 1172
    panel = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    sh = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((bx0 + 6, by0 + 20, bx1 + 6, by1 + 24), radius=48, fill=(0, 0, 0, 120))
    panel.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    body = kertas_tekstur(bx1 - bx0, by1 - by0, (40, 40, 42), 18210 + idx, 0.06).convert("RGBA")
    bm = Image.new("L", body.size, 0)
    ImageDraw.Draw(bm).rounded_rectangle((0, 0, body.width - 1, body.height - 1), radius=44, fill=255)
    body.putalpha(bm)
    panel.alpha_composite(body, (bx0, by0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((bx0, by0, bx1, by1), radius=44, outline=(78, 78, 82), width=3)
    # jendela dial
    dx0, dy0, dx1, dy1 = bx0 + 50, by0 + 54, bx1 - 50, by0 + 214
    pd.rounded_rectangle((dx0 - 10, dy0 - 10, dx1 + 10, dy1 + 10), radius=18, fill=(20, 20, 22))
    pd.rounded_rectangle((dx0, dy0, dx1, dy1), radius=12, fill=(236, 228, 206))
    sx0, sx1 = dx0 + 66, dx1 - 74

    def fx(f_):
        return sx0 + (f_ - 88) / 20 * (sx1 - sx0)
    for k in range(0, 41):
        f_ = 88 + k * 0.5
        x = fx(f_)
        L = 30 if k % 4 == 0 else 16
        pd.line((x, dy1 - 18 - L, x, dy1 - 18), fill=(60, 54, 46), width=3 if k % 4 == 0 else 2)
        if k % 4 == 0:
            pd.text((x, dy0 + 22), f"{int(f_)}", font=din(40), fill=(40, 36, 32), anchor="ma")
    pd.text((dx0 + 16, dy1 - 22), "FM", font=din(26), fill=(255, 110, 30), anchor="ls")
    pd.text((dx1 - 16, dy1 - 22), "MHz", font=din(26), fill=(120, 110, 96), anchor="rs")
    # kisi speaker
    gx0, gy0, gs = bx0 + 56, dy1 + 52, 384
    grid_pts = []
    for r_ in range(18):
        for c_ in range(18):
            x, y = gx0 + 13 + c_ * 21.5, gy0 + 13 + r_ * 21.5
            if math.hypot(x - (gx0 + gs / 2), y - (gy0 + gs / 2)) < gs / 2 - 4:
                grid_pts.append((x, y))
                pd.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(18, 18, 20))
                pd.arc((x - 6, y - 6, x + 6, y + 6), 20, 160, fill=(80, 80, 84), width=1)
    pd.ellipse((gx0 - 6, gy0 - 6, gx0 + gs + 6, gy0 + gs + 6), outline=(70, 70, 74), width=3)
    # LCD, jendela gelombang, bar sinyal, kenop
    lx0, ly0, lx1, ly1 = gx0 + gs + 46, dy1 + 52, bx1 - 56, dy1 + 52 + 112
    pd.rounded_rectangle((lx0 - 8, ly0 - 8, lx1 + 8, ly1 + 8), radius=14, fill=(14, 14, 16))
    pd.rounded_rectangle((lx0, ly0, lx1, ly1), radius=8, fill=(20, 30, 24))
    wx0, wy0, wx1, wy1 = lx0, ly1 + 30, lx1, ly1 + 30 + 132
    pd.rounded_rectangle((wx0 - 8, wy0 - 8, wx1 + 8, wy1 + 8), radius=14, fill=(14, 14, 16))
    pd.rounded_rectangle((wx0, wy0, wx1, wy1), radius=8, fill=(12, 22, 18))
    for gxx in range(int(wx0) + 20, int(wx1), 30):
        pd.line((gxx, wy0 + 4, gxx, wy1 - 4), fill=(24, 44, 34), width=1)
    pd.line((wx0 + 4, (wy0 + wy1) / 2, wx1 - 4, (wy0 + wy1) / 2), fill=(30, 56, 42), width=1)
    kx, ky, kr = lx0 + 78, wy1 + 92, 66
    pd.ellipse((kx - kr - 8, ky - kr - 8, kx + kr + 8, ky + kr + 8), fill=(22, 22, 24))
    for k in range(48):
        a = 2 * math.pi * k / 48
        pd.line((kx + math.cos(a) * (kr - 2), ky + math.sin(a) * (kr - 2), kx + math.cos(a) * (kr + 6), ky + math.sin(a) * (kr + 6)), fill=(70, 70, 74), width=3)
    pd.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=(58, 58, 62))
    pd.ellipse((kx - kr * 0.7, ky - kr * 0.7, kx + kr * 0.7, ky + kr * 0.7), fill=(48, 48, 52))
    bar_x0, bar_y1 = lx0 + 196, wy1 + 126
    for k in range(5):
        pd.rectangle((bar_x0 + k * 30, bar_y1 - 24 - k * 18, bar_x0 + k * 30 + 18, bar_y1), outline=(90, 90, 94), width=2)
    pd.text((bar_x0 + 150, bar_y1), "SINYAL", font=din(22), fill=(130, 130, 134), anchor="ls")
    pd.text((bx0 + 60, by1 - 30), "@" + HANDLE.upper(), font=din(26), fill=(170, 170, 174), anchor="ls")
    pd.ellipse((bx1 - 70, by1 - 50, bx1 - 54, by1 - 34), fill=(255, 110, 30))
    pd.text((bx1 - 84, by1 - 30), "TUNER FM 88-108", font=din(22), fill=(130, 130, 134), anchor="rs")
    bg.alpha_composite(panel)
    # ayat
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fv, vl, vs = susun(probe, tanpa_kutip(p["ayat"]), lambda s: charter(s, 1), RW - 180, 300, 46, 30, 1.32)
    ayat = Image.new("RGBA", (RW, int(len(vl) * vs * 1.32 + 70)), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=fv, fill=(40, 38, 36, 255), anchor="ma")
        y += vs * 1.32
    ad.text((RW / 2, y + 14), p["ref"].upper(), font=din(38), fill=(220, 90, 20, 255), anchor="ma")
    y_ayat = by1 + 56
    # lintasan jarum
    if frek >= 97:
        henti = list(np.linspace(89.6, frek - 2.6, 4))
    else:
        henti = list(np.linspace(min(107, frek + 2.6), 106.6, 4))[::-1]
    henti = [h_ + rng.uniform(-0.3, 0.3) for h_ in henti]
    seg = [(0.0, 1.0, 88.4, 88.4)]
    t = 1.0
    f_prev = 88.4
    for h_ in henti:
        seg.append((t, t + 0.5, f_prev, h_))
        seg.append((t + 0.5, t + 1.25, h_, h_))
        t += 1.25
        f_prev = h_
    jeda = [(1.0 + 0.5 + k * 1.25, 1.0 + 1.25 + k * 1.25) for k in range(4)]

    def frek_t(t):
        if t >= 6.0:
            u = min(1.0, (t - 6.0) / 1.4)
            c1, c3 = 1.70158, 2.70158
            e = 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2
            return f_prev + (frek - f_prev) * e
        for t0, t1, a, b in seg:
            if t0 <= t < t1:
                return a + (b - a) * ease((t - t0) / (t1 - t0))
        return f_prev
    fl_ = menlo(40, 1)
    fs_ = menlo(26, 0)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        if t < 0.8:
            a = ease(t / 0.8)
            frame = Image.blend(Image.new("RGBA", (RW, RH), (230, 224, 212, 255)), frame, a)
        d = ImageDraw.Draw(frame)
        f_ = min(108.15, max(87.85, frek_t(t)))
        k_sin = ease((t - 6.4) / 1.4)
        stasiun = None
        for j, (a_, b_) in enumerate(jeda):
            if a_ <= t < b_ and j < len(gangguan):
                stasiun = j
        # jarum
        x = fx(f_)
        d.rectangle((x - 3, dy0 + 4, x + 3, dy1 - 4), fill=(255, 110, 30))
        d.polygon([(x - 10, dy0 + 2), (x + 10, dy0 + 2), (x, dy0 + 16)], fill=(255, 110, 30))
        # kenop berputar
        ang = -math.pi / 2 + (f_ - 88) / 20 * 2 * math.pi * 0.85
        d.line((kx + math.cos(ang) * kr * 0.2, ky + math.sin(ang) * kr * 0.2, kx + math.cos(ang) * kr * 0.62, ky + math.sin(ang) * kr * 0.62), fill=(255, 110, 30), width=7)
        # LCD
        hijau = (120, 255, 170)
        if t < 1.0 or (stasiun is None and t < 6.6):
            teks1 = "MENCARI" + "." * (1 + int(t * 3) % 3)
        elif stasiun is not None:
            teks1 = gangguan[stasiun]
        else:
            teks1 = lcd_akhir if t >= 7.2 else "MENCARI..."
        fl = fl_
        while d.textlength(teks1, font=fl) > lx1 - lx0 - 30 and fl.size > 18:
            fl = menlo(fl.size - 2, 1)
        d.text((lx0 + 16, ly0 + 16), teks1, font=fl, fill=hijau)
        d.text((lx0 + 16, ly1 - 16), f"{f_:6.2f} MHz", font=fs_, fill=(90, 190, 130), anchor="ls")
        # gelombang
        pts = []
        amp_n = (1 - k_sin) * (1.0 if stasiun is not None or t < 1 else 0.55)
        for xx_ in range(int(wx0) + 6, int(wx1) - 6, 3):
            u = (xx_ - wx0) / (wx1 - wx0)
            nz = rng.normal(0, 1) * 34 * amp_n
            sn = math.sin(u * 2 * math.pi * 3 + t * 6) * 52 * k_sin
            yv = (wy0 + wy1) / 2 + max(-66, min(66, nz + sn))
            pts.append((xx_, yv))
        d.line(pts, fill=hijau + ((255,) if k_sin > 0.5 else (230,)), width=3, joint="curve")
        # bar sinyal
        level = 5 * k_sin if t >= 6.4 else (rng.integers(1, 3) if stasiun is not None else (1 if int(t * 6) % 2 else 0))
        for k in range(5):
            if k < level:
                d.rectangle((bar_x0 + k * 30 + 3, bar_y1 - 24 - k * 18 + 3, bar_x0 + k * 30 + 15, bar_y1 - 3), fill=hijau if t >= 6.4 else (255, 110, 30))
        # label stasiun di atas dial
        if stasiun is not None:
            a_, b_ = jeda[stasiun]
            al = min(1.0, (t - a_) / 0.15, (b_ - t) / 0.15)
            lab = gangguan[stasiun]
            fl2 = din(40)
            tw = d.textlength(lab, font=fl2) + 44
            lxp = min(max(x - tw / 2, 80), RW - 80 - tw)
            tag = Image.new("RGBA", (int(tw), 64), (0, 0, 0, 0))
            tg = ImageDraw.Draw(tag)
            tg.rounded_rectangle((0, 0, tw - 1, 56), radius=14, fill=(30, 30, 32, 235))
            tg.text((tw / 2, 30), lab, font=fl2, fill=(255, 140, 70, 255), anchor="mm")
            frame.alpha_composite(fade(tag, al), (int(lxp), int(dy0 - 100)))
        # bintik statis
        statis = (1 - k_sin) * (0.6 if stasiun is not None else 0.25) if t < 7.8 else 0
        if statis > 0.01:
            m = (rng.random((RH // 6, RW // 6)) < 0.06 * statis).astype(np.uint8) * int(110 * statis + 40)
            sp_ = Image.fromarray(m).resize((RW, RH), Image.NEAREST)
            lay = Image.new("RGBA", (RW, RH), (255, 255, 255, 0))
            lay.putalpha(sp_)
            frame.alpha_composite(lay)
        # kisi berdenyut + ayat
        if t >= 8.0:
            u = t - 8.0
            lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ccx, ccy = gx0 + gs / 2, gy0 + gs / 2
            for (px_, py_) in grid_pts:
                r_ = math.hypot(px_ - ccx, py_ - ccy)
                v = 0.5 + 0.5 * math.sin(u * 3.2 - r_ / 26)
                if v > 0.55:
                    rr = 4 + 2 * v
                    ld.ellipse((px_ - rr, py_ - rr, px_ + rr, py_ + rr), fill=(255, 140, 70, int(120 * (v - 0.55) / 0.45 * min(1, u))))
            frame.alpha_composite(lay)
            frame.alpha_composite(fade(ayat, ease((t - 8.0) / 0.9)), (0, int(y_ayat + 16 * (1 - ease((t - 8.0) / 0.9)))))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def sticky_kayu(p, i):
    img = gaya_w8.sticky_image(p, i, latar=kayu_latar(W, H, 18300 + i))
    teks_bayang(img, (300, H - 64), "@" + HANDLE, hn(22, 10), (240, 226, 206), anchor="ma", blur=3, kuat=150)
    return img


def majalah_danau(p, i):
    """Sampul majalah di danau subuh; baris edisi & tanggal barcode diganti ke Januari 2027."""
    latar = danau_latar(W, H, 18330 + i, horizon=0.52)
    img = gaya_w10.majalah_image(p, i, latar=latar).convert("RGB")
    a = np.asarray(latar).astype(np.float32)[28:70]
    yy = np.linspace(0, 1, H)[28:70, None, None]
    a *= 1 - 0.55 * np.clip((0.3 - yy) / 0.3, 0, 1)
    img.paste(grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05), (0, 28))
    d = ImageDraw.Draw(img)
    bulan = " ".join(p.get("_tanggal", "17 Januari 2027").split()[1:]).upper()
    d.text((W / 2, 40), f"{bersih(p.get('edisi', 'EDISI JANUARI')).upper()}  ·  {bulan}  ·  @{HANDLE.upper()}", font=hn(22, 1), fill=(255, 255, 255), anchor="ma")
    d.rectangle((W - 226, H - 82, W - 64, H - 60), fill=(255, 255, 255))
    d.text((W - 145, H - 72), p.get("_tgl_struk", "17/01/2027").replace("/", "-"), font=hn(16, 10), fill=(20, 20, 20), anchor="mm")
    return img


SIMPLE = {
    # baru
    "JARING": jaring_image, "PERAHU": perahu_image, "BENDERA": bendera_image, "PERKAKAS": perkakas_image,
    "PLANG": plang_image, "CONGKLAK": congklak_image, "ALUR": alur_image, "LOWONGAN": lowongan_image,
    "UPAH": upah_image, "BEKAL": bekal_image,
    # lama
    "VENN": gaya_w12.venn_image, "PERJALANAN": gaya_w12.perjalanan_image, "WATERCOLOR": gaya_w12.watercolor_image,
    "KOPI": gaya_w12.kopi_image, "BOTANI": gaya_w13.botani_image, "ARTIKEL": gaya_w13.artikel_image,
    "KARTUFOTO": gaya_w13.kartufoto_image, "KATAKUNCI": gaya_w13.katakunci_image, "ULASAN": gaya_w14.ulasan_image,
    # mix: latar kayu / danau, efek senja
    "STICKYKAYU": sticky_kayu,
    "POLAROIDDANAU": lambda p, i: gaya_w7.polaroid_image(p, i, latar=danau_latar(W, H, 18310 + i, horizon=0.5)),
    "TIKETDANAU": lambda p, i: gaya_w7.tiket_image(p, i, latar=danau_latar(W, H, 18320 + i, horizon=0.56)),
    "RESEPKAYU": lambda p, i: gaya_w9.resep_image(p, i, latar=kayu_latar(W, H, 18340 + i)),
    "BALONDANAU": lambda p, i: gaya_w12.balon_image(p, i, latar=danau_latar(W, H, 18350 + i, horizon=0.38)),
    "TELEGRAMKAYU": lambda p, i: gaya_w10.telegram_image(p, i, latar=kayu_latar(W, H, 18360 + i)),
    "KAMUSSENJA": lambda p, i: senja(gaya_w7.kamus_image(p, i), 18370 + i),
    "PHOTOBOOTHKAYU": lambda p, i: gaya_w11.photobooth_image(p, i, latar=kayu_latar(W, H, 18380 + i)),
    "FLIPDANAU": lambda p, i: gaya_w11.flipclock_image(p, i, latar=danau_latar(W, H, 18390 + i, horizon=0.44, perahu=False)),
    "MAJALAHDANAU": majalah_danau,
    "KETIKSENJA": lambda p, i: senja(gaya_w7.ketik_image(p, i), 18400 + i),
    "EMAILSENJA": lambda p, i: senja(gaya_w12.email_image(p, i), 18410 + i),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {}
REELS = {"DOMINO": (domino_reel, "domino"), "RADIO": (radio_reel, "radio"),
         "TITIK": (gaya_w13.titik_reel, "titik"), "JAMPASIR": (gaya_w10.jampasir_reel, "jampasir"),
         "NAPAS": (gaya_w14.napas_reel, "napas")}


def render_week(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            p = getattr(t, fmt)[idx]
            if fmt in SIMPLE:
                out[(hari, slot)] = ([save(SIMPLE[fmt](konteks(p, hari, slot, MULAI), idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt in MULTI:
                out[(hari, slot)] = (MULTI[fmt](konteks(p, hari, slot, MULAI), idx, mod), p["caption"])
            elif fmt in REELS:
                rel = f"reels/{mod}/{REELS[fmt][1]}{idx + 1}.mp4"
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], p["caption"])
    return out


def render_reels(mod=MOD):
    gaya_w11.render_reels(mod, REELS, MULAI)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
