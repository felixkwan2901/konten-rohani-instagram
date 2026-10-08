"""Akun Tenang - minggu 13 (konten/tenang_w13.py), minggu Natal: 36 gaya diacak tiap hari + komik Eli.
BARU (terinspirasi gaya akun Kristen besar di Instagram, isinya buatan sendiri):
       KATAKUNCI (kalimat kecil + satu kata raksasa, a la Jesus Calling), POSTERTEBAL (huruf kondensed raksasa terpotong di tepi,
       a la Elevation/Hillsong), KARTUFOTO (kartu kertas di atas foto alam, a la Proverbs 31), ANTIK (kartu hijau tua berornamen,
       a la Daily Grace), BOTANI (cat air daun & beri, a la GraceLaced), ARTIKEL (kutipan artikel dengan garis merah, a la Desiring God),
       BOCOR (teks besar melewati tepi, a la Motivasi Percaya), BERITA (kotak judul berita, a la Jawaban), KOLASE (kolase risograf
       angka raksasa, a la GMS), ANGKA (angka statistik raksasa, hitung mundur), TITIK (Reels grid titik, a la Elevation),
       PANGGUNG (Reels lampu panggung, a la Bethel Music).
LAMA : KRANS, KONFETI, BALON, FILM, RASI, KARTUNATAL, SCROLL, PERJALANAN, TELEGRAM, UTAS, TANYA, KACAPATRI.
MIX  : SALJUEMAS, LAMPUPOHON, FLIPNATAL, KORANNATAL, STAMPNATAL, WATERCOLORMALAM, PHOTOBOOTHNATAL, TAGHIJAU, CRAYONHITAM,
       KOPIMERAH, PIXELNATAL, EMAILGELAP.

  python3 gaya_w13.py [reels]
"""
import datetime as dt
import importlib
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cerita
import config
import gaya_w5
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import gaya_w11
import gaya_w12
import render
from gaya_w6 import cover, foto_warna, georgia, hn, tambah_musik
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tanpa_kutip
from gaya_w9 import EMAS, ayat_bawah, kertas_kado
from gaya_w11 import konteks
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w13"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2026, 12, 20)


def foto_redup(scene, w, h, seed, gelap=0.4, blur=2):
    ph = cover(foto_warna(scene, w, h, seed=seed), w, h).convert("RGB").filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(ph).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True)
    a = a * 0.6 + lum * 0.4  # sedikit pudar
    return Image.fromarray(np.clip(a * (1 - gelap), 0, 255).astype(np.uint8))


def bintang_krem(w, h, seed):
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (250, 244, 232), (238, 226, 206)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for x in range(-h, w, 90):
        d.line((x, 0, x + h, h), fill=(232, 210, 196, 255), width=3)
    for _ in range(int(w * h / 30000)):
        gaya_w10.bintang5(d, rng.uniform(0, w), rng.uniform(0, h), rng.uniform(6, 12), (214, 170, 80, 255))
    return grain(img.convert("RGB"), 0.04)


def merah_salju(w, h, seed):
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (120, 18, 28), (52, 6, 12)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 7000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(1.5, 4)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(rng.uniform(80, 200))))
    return img


# ================= BARU =================

# ---------- KATAKUNCI: satu kata raksasa ----------

def katakunci_image(p, i):
    img = grain(foto_redup(p["foto"], W, H, 7300 + i, gelap=0.42), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    fs = hn(34, 10)
    y = 300
    for ln in wrap(d, bersih(p["atas"]).upper(), fs, W - 200):
        d.text((W / 2, y), ln, font=fs, fill=white, anchor="ma")
        y += 46
    kata = bersih(p["kata"]).upper()
    fk = hn(300, 9)
    while d.textlength(kata, font=fk) > W - 110:
        fk = hn(fk.size - 6, 9)
    y += 10
    d.text((W / 2, y), kata, font=fk, fill=white, anchor="ma")
    y += fk.size * 0.98
    for ln in wrap(d, bersih(p["bawah"]).upper(), fs, W - 200):
        d.text((W / 2, y), ln, font=fs, fill=white, anchor="ma")
        y += 46
    ayat_bawah(img, p, max(y + 60, 980), H - 70, (236, 236, 236), (255, 226, 160), start=30, stop=20)
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(22, 10), fill=(220, 220, 220), anchor="ma")
    return img


# ---------- POSTERTEBAL: huruf raksasa terpotong ----------

POSTER_WARNA = {"kuning": ((250, 206, 40), (20, 20, 24)), "biru": ((28, 78, 220), (255, 255, 255)),
                "merah": ((214, 36, 50), (255, 255, 255)), "hijau": ((18, 112, 70), (255, 255, 255))}


def postertebal_image(p, i):
    bg, fg = POSTER_WARNA.get(p["warna"], POSTER_WARNA["kuning"])
    img = grain(Image.new("RGB", (W, H), bg), 0.06).convert("RGBA")
    d = ImageDraw.Draw(img)
    lines = bersih(p["teks"]).upper().split("\n")
    size = 400
    while max(d.textlength(ln, font=hn(size, 9)) for ln in lines) > W + 70 or (len(lines) * size * 0.84 > 720 and size > 120):
        size -= 6
    f = hn(size, 9)
    lh = size * 0.84
    y = 90
    for k, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2 if tw < W - 40 else -35 + (k % 2) * 10
        d.text((x, y), ln, font=f, fill=fg)
        y += lh
    y += size * 0.24 + 30
    for ln in wrap(d, bersih(p["kecil"]), hn(36, 10), W - 140):
        d.text((70, y), ln, font=hn(36, 10), fill=fg)
        y += 46
    f2, l2, s2 = pas(d, tanpa_kutip(p["ayat"]), lambda s: hn(s, 2), W - 140, H - 120 - y - 40, 30, 20, 1.32)
    y = max(y + 40, H - 120 - len(l2) * s2 * 1.32)
    for ln in l2:
        d.text((70, y), ln, font=f2, fill=fg)
        y += s2 * 1.32
    d.text((70, y + 6), p["ref"], font=hn(28, 1), fill=fg)
    d.text((W - 70, H - 50), "@" + HANDLE, font=hn(22, 1), fill=fg, anchor="rs")
    return img


# ---------- KARTUFOTO: kartu kertas di atas foto ----------

def kartufoto_image(p, i):
    img = foto_warna(p["foto"], W, H, seed=7400 + i).convert("RGB").filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    cw, chh = 780, 1010
    rng = np.random.default_rng(7400 + i)
    c = np.zeros((chh, cw, 3), np.float32) + np.array([248, 244, 234])
    c *= (0.97 + 0.04 * render.fbm2d(chh, cw, rng, ((30, 1.0), (160, 0.5))))[..., None]
    card = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(card)
    ink, aksen = (60, 54, 46), (150, 120, 80)
    judul = bersih(p["judul"])
    if "*" in judul:
        sebelum, kata, sesudah = judul.split("*", 2)
    else:
        sebelum, kata, sesudah = judul, "", ""
    y = 90
    for teks, font, col in ((sebelum.strip(), georgia(56), ink), (kata.strip(), ft("SnellRoundhand.ttc", 96, 2), aksen), (sesudah.strip(), georgia(56), ink)):
        if not teks:
            continue
        for ln in wrap(d, teks, font, cw - 120):
            d.text((cw / 2, y), ln, font=font, fill=col, anchor="ma")
            y += font.size * (1.1 if font.size > 80 else 1.2)
    y += 30
    d.line((cw / 2 - 50, y, cw / 2 + 50, y), fill=(200, 186, 160), width=2)
    y += 40
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), cw - 140, chh - 110 - y, 34, 22, 1.4)
    for ln in lines:
        d.text((cw / 2, y), ln, font=f, fill=(90, 82, 72), anchor="ma")
        y += size * 1.4
    d.text((cw / 2, y + 12), p["ref"].upper(), font=hn(24, 10), fill=aksen, anchor="ma")
    d.text((cw / 2, chh - 50), HANDLE, font=hn(20, 10), fill=(170, 160, 150), anchor="ma")
    bayangan(img, card, ((W - cw) // 2, (H - chh) // 2), blur=26, geser=(0, 18), kuat=0.35)
    return img


# ---------- ANTIK: kartu hijau tua berornamen ----------

def ornamen_sudut(d, x, y, sx, sy, col):
    for r in (40, 26):
        d.arc((x - r if sx > 0 else x - r, y - r, x + r, y + r), 0 if sx > 0 else 90, 360, fill=col, width=2)
    d.line((x, y, x + sx * 120, y), fill=col, width=2)
    d.line((x, y, x, y + sy * 120), fill=col, width=2)
    d.ellipse((x + sx * 124 - 4, y - 4, x + sx * 124 + 4, y + 4), fill=col)
    d.ellipse((x - 4, y + sy * 124 - 4, x + 4, y + sy * 124 + 4), fill=col)


def antik_image(p, i):
    rng = np.random.default_rng(7500 + i)
    a = np.zeros((H, W, 3), np.float32) + np.array([26, 56, 42])
    a *= (0.8 + 0.35 * render.fbm2d(H, W, rng, ((5, 1.0), (40, 0.5), (200, 0.3))))[..., None]
    img = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.06).convert("RGBA")
    d = ImageDraw.Draw(img)
    emas, krem = (206, 172, 102), (240, 230, 206)
    d.rectangle((50, 50, W - 50, H - 50), outline=emas, width=3)
    d.rectangle((64, 64, W - 64, H - 64), outline=emas, width=1)
    for x, y, sx, sy in ((100, 100, 1, 1), (W - 100, 100, -1, 1), (100, H - 100, 1, -1), (W - 100, H - 100, -1, -1)):
        ornamen_sudut(d, x, y, sx, sy, emas)
    y = 230
    d.text((W / 2, y), " ".join(bersih(p["atas"]).upper()), font=hn(26, 10), fill=emas, anchor="ma")
    y += 70
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: ft("BigCaslon.ttf", s), W - 260, 260, 76, 44, 1.15)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=krem, anchor="ma")
        y += size * 1.15
    y += 30
    d.polygon([(W / 2, y - 12), (W / 2 + 12, y), (W / 2, y + 12), (W / 2 - 12, y)], fill=emas)
    d.line((W / 2 - 140, y, W / 2 - 24, y), fill=emas, width=2)
    d.line((W / 2 + 24, y, W / 2 + 140, y), fill=emas, width=2)
    y += 60
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 300, H - 260 - y, 40, 26, 1.45)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=krem, anchor="ma")
        y += size * 1.45
    d.text((W / 2, y + 24), " ".join(p["ref"].upper()), font=hn(24, 10), fill=emas, anchor="ma")
    d.text((W / 2, H - 150), HANDLE, font=hn(20, 10), fill=(150, 160, 140), anchor="ma")
    return img


# ---------- BOTANI: cat air daun & beri ----------

def ranting(lay, x0, y0, ang, panjang, rng, warna):
    d = ImageDraw.Draw(lay)
    pts = []
    for t in np.linspace(0, 1, 30):
        a = ang + 0.5 * math.sin(t * 2.4)
        pts.append((x0 + math.cos(a) * panjang * t, y0 + math.sin(a) * panjang * t))
    d.line(pts, fill=(110, 96, 70, 200), width=4)
    for k, (x, y) in enumerate(pts[4::3]):
        for s in (-1, 1):
            a = ang + s * 0.9 + rng.uniform(-0.2, 0.2)
            L = rng.uniform(40, 70)
            cx, cy = x + math.cos(a) * L / 2, y + math.sin(a) * L / 2
            leaf = Image.new("RGBA", (int(L * 1.2), int(L * 0.6)), (0, 0, 0, 0))
            ImageDraw.Draw(leaf).ellipse((0, 0, leaf.width, leaf.height), fill=warna[k % len(warna)] + (150,))
            leaf = leaf.rotate(-math.degrees(a), expand=True, resample=Image.BICUBIC)
            comp(lay, leaf, (cx - leaf.width / 2, cy - leaf.height / 2))
    ex, ey = pts[-1]
    for _ in range(5):
        bx, by = ex + rng.uniform(-30, 30), ey + rng.uniform(-30, 30)
        d.ellipse((bx - 11, by - 11, bx + 11, by + 11), fill=(190, 40, 50, 200))


def botani_image(p, i):
    rng = np.random.default_rng(7600 + i)
    a = np.zeros((H, W, 3), np.float32) + np.array([250, 246, 238])
    a -= render.fbm2d(H, W, rng, ((80, 1.0), (300, 0.5)))[..., None] * 8
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hijau = [(120, 150, 110), (90, 130, 100), (150, 170, 120), (100, 140, 130)]
    for x0, y0, ang in ((-20, 80, 0.4), (W + 20, 120, math.pi - 0.5), (-20, H - 140, -0.5), (W + 20, H - 100, math.pi + 0.45)):
        ranting(lay, x0, y0, ang, 360, rng, hijau)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))
    d = ImageDraw.Draw(img)
    fj = ft("SnellRoundhand.ttc", 92, 2)
    while d.textlength(bersih(p["judul"]), font=fj) > W - 260:
        fj = ft("SnellRoundhand.ttc", fj.size - 4, 2)
    d.text((W / 2, 300), bersih(p["judul"]), font=fj, fill=(90, 110, 80), anchor="ma")
    y = 300 + fj.size * 1.4
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: ft("Iowan Old Style.ttc", s, 2), W - 300, 620, 46, 28, 1.42)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(70, 66, 56), anchor="ma")
        y += size * 1.42
    d.text((W / 2, y + 26), p["ref"].upper(), font=hn(26, 10), fill=(150, 60, 60), anchor="ma")
    d.text((W / 2, H - 70), HANDLE, font=hn(20, 10), fill=(150, 150, 140), anchor="ma")
    return img


# ---------- ARTIKEL: kutipan artikel ----------

def artikel_image(p, i):
    img = grain(Image.new("RGB", (W, H), (252, 251, 248)), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    merah = (200, 40, 40)
    d.rectangle((80, 110, 200, 122), fill=merah)
    d.text((80, 150), "RENUNGAN", font=hn(24, 1), fill=merah)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: ft("Georgia Bold.ttf", s), W - 160, 330, 74, 44, 1.14)
    y = 200
    for ln in lines:
        d.text((80, y), ln, font=f, fill=(24, 24, 26))
        y += size * 1.14
    y += 30
    f2, l2, s2 = pas(d, bersih(p["kutipan"]), georgia, W - 160, 400, 36, 26, 1.48)
    for ln in l2:
        d.text((80, y), ln, font=f2, fill=(80, 80, 84))
        y += s2 * 1.48
    y += 18
    d.text((80, y), "— " + bersih(p["penulis"]).upper(), font=hn(24, 10), fill=(140, 140, 146))
    y += 70
    d.rectangle((80, y, 86, H - 150), fill=merah)
    ayat_bawah(img, p, y + 10, H - 170, (60, 60, 64), merah, maxw=W - 240, start=32, stop=22)
    d.text((W - 80, H - 70), "@" + HANDLE, font=hn(22, 10), fill=(160, 160, 166), anchor="rs")
    return img


# ---------- BOCOR: teks besar melewati tepi ----------

def bocor_image(p, i):
    img = grain(foto_redup(p["foto"], W, H, 7700 + i, gelap=0.55), 0.06).convert("RGBA")
    d = ImageDraw.Draw(img)
    teks = bersih(p["teks"])
    tebal = bersih(p.get("tebal", ""))
    words = teks.split()
    mark = [False] * len(words)
    tw = tebal.split()
    for s in range(len(words) - len(tw) + 1):
        if tw and [w.strip(".,!?") for w in words[s:s + len(tw)]] == [w.strip(".,!?") for w in tw]:
            for k in range(s, s + len(tw)):
                mark[k] = True
            break
    size = 112
    f = hn(size, 1)
    lines, cur, curm = [], [], []
    for w, m in zip(words, mark):
        trial = " ".join(cur + [w])
        if d.textlength(trial, font=f) > W + 20 and cur:
            lines.append(list(zip(cur, curm)))
            cur, curm = [w], [m]
        else:
            cur.append(w)
            curm.append(m)
    lines.append(list(zip(cur, curm)))
    while len(lines) * size * 1.02 > 760 and size > 70:
        size -= 6
        f = hn(size, 1)
        lines, cur, curm = [], [], []
        for w, m in zip(words, mark):
            trial = " ".join(cur + [w])
            if d.textlength(trial, font=f) > W + 20 and cur:
                lines.append(list(zip(cur, curm)))
                cur, curm = [w], [m]
            else:
                cur.append(w)
                curm.append(m)
        lines.append(list(zip(cur, curm)))
    y = 160
    sp = d.textlength(" ", font=f)
    for k, ln in enumerate(lines):
        x = -18 if k % 2 == 0 else -4
        for w, m in ln:
            col = (255, 214, 90) if m else (255, 255, 255)
            if m:
                d.rectangle((x, y + size * 0.9, x + d.textlength(w, font=f), y + size * 1.0), fill=(255, 214, 90))
            d.text((x, y), w, font=f, fill=col)
            x += d.textlength(w, font=f) + sp
        y += size * 1.02
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle((0, max(y + 40, 960), W, H), fill=(0, 0, 0, 120))
    img.alpha_composite(band)
    ayat_bawah(img, p, max(y + 80, 1000), H - 70, (236, 236, 236), (255, 214, 90), start=30, stop=20)
    ImageDraw.Draw(img).text((W - 50, H - 30), "@" + HANDLE, font=hn(22, 10), fill=(220, 220, 220), anchor="rs")
    return img


# ---------- BERITA: kotak judul berita ----------

def berita_image(p, i):
    ph = cover(foto_warna(p["foto"], W, 900, seed=7800 + i), W, 820).convert("RGBA")
    img = Image.new("RGBA", (W, H), (16, 34, 84, 255))
    img.paste(ph, (0, 0))
    d = ImageDraw.Draw(img)
    navy, kuning = (16, 34, 84), (255, 206, 50)
    lab = bersih(p["label"]).upper()
    tw = d.textlength(lab, font=hn(28, 1))
    d.rounded_rectangle((60, 60, 60 + tw + 48, 112), radius=10, fill=(40, 110, 230))
    d.text((84, 86), lab, font=hn(28, 1), fill="white", anchor="lm")
    d.rounded_rectangle((W - 260, 60, W - 60, 112), radius=26, fill=(255, 255, 255, 230))
    d.text((W - 160, 86), "Tenang", font=hn(30, 1), fill=navy, anchor="mm")
    judul = bersih(p["judul"])
    f = hn(66, 1)
    words = judul.split()
    while True:
        lines, cur = [], []
        for w in words:
            if d.textlength(" ".join(cur + [w]).replace("*", ""), font=f) > W - 180 and cur:
                lines.append(cur)
                cur = [w]
            else:
                cur.append(w)
        lines.append(cur)
        if len(lines) * f.size * 1.2 < 330 or f.size < 40:
            break
        f = hn(f.size - 4, 1)
    bh = int(len(lines) * f.size * 1.2 + 70)
    by = 820 - bh + 120
    d.rounded_rectangle((50, by, W - 50, by + bh), radius=16, fill=navy)
    y = by + 36
    sp = d.textlength(" ", font=f)
    for ln in lines:
        x = 90
        for w in ln:
            hl = w.startswith("*") or w.endswith("*")
            w_ = w.replace("*", "")
            ww = d.textlength(w_, font=f)
            if hl:
                d.rectangle((x - 8, y - 4, x + ww + 8, y + f.size * 1.08), fill=kuning)
            d.text((x, y), w_, font=f, fill=navy if hl else (255, 255, 255))
            x += ww + sp
        y += f.size * 1.2
    y = by + bh + 34
    for ln in wrap(d, bersih(p["sub"]), hn(34, 0), W - 140):
        d.text((70, y), ln, font=hn(34, 0), fill=(220, 228, 246))
        y += 44
    ayat_bawah(img, p, y + 36, H - 70, (236, 240, 250), kuning, start=30, stop=20)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(170, 186, 220), anchor="ma")
    return img


# ---------- KOLASE: kolase risograf ----------

def halftone_warna(w, h, col, rng, kerapatan=0.5):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, h, 10):
        for x in range(0, w, 10):
            r = 4.2 * kerapatan + rng.uniform(-0.6, 0.6)
            d.ellipse((x + 5 - r, y + 5 - r, x + 5 + r, y + 5 + r), fill=col + (220,))
    return lay


def kolase_image(p, i):
    rng = np.random.default_rng(7900 + i)
    img = grain(Image.new("RGB", (W, H), (244, 238, 224)), 0.12).convert("RGBA")
    pink, teal, kuning, biru = (238, 80, 120), (0, 150, 150), (250, 200, 40), (40, 70, 160)
    d = ImageDraw.Draw(img)
    d.ellipse((560, 80, 1060, 580), fill=kuning)
    img.alpha_composite(halftone_warna(420, 420, pink, rng, 0.45), (40, 560))
    ph = cover(foto_warna(("bintang", "fajar")[i % 2], 700, 600, seed=7950 + i), 560, 440).convert("L").convert("RGB")
    ph = Image.fromarray((np.asarray(ph).astype(np.float32) * np.array([0.55, 0.85, 1.0]) + np.array([0, 20, 40])).clip(0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", ph.size, 0)
    pts = [(x, rng.uniform(0, 14)) for x in range(0, ph.width + 1, 20)] + [(ph.width, ph.height)] + [(0, ph.height)]
    ImageDraw.Draw(m).polygon(pts, fill=255)
    ph.putalpha(m)
    ph = ph.rotate(4, expand=True, resample=Image.BICUBIC)
    bayangan(img, ph, (440, 420), blur=10, geser=(6, 10), kuat=0.3)
    d = ImageDraw.Draw(img)
    besar = bersih(p["besar"])
    fb = hn(330, 9)
    while d.textlength(besar, font=fb) > W - 120:
        fb = hn(fb.size - 10, 9)
    d.text((70 + 10, 120 + 8), besar, font=fb, fill=teal)
    d.text((70, 120), besar, font=fb, fill=pink)
    y = 920
    d.text((70, y), bersih(p["judul"]).upper(), font=hn(56, 9), fill=biru)
    y += 70
    for ln in wrap(d, bersih(p["teks"]), hn(34, 10), W - 140):
        d.text((70, y), ln, font=hn(34, 10), fill=(50, 46, 60))
        y += 44
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 140, H - 90 - y - 50, 28, 20, 1.34)
    y += 20
    for ln in lines:
        d.text((70, y), ln, font=f, fill=(70, 66, 80))
        y += size * 1.34
    d.text((70, y + 6), p["ref"], font=hn(26, 1), fill=pink)
    d.text((W - 60, H - 40), "@" + HANDLE, font=hn(22, 1), fill=biru, anchor="rs")
    return img


# ---------- ANGKA: angka raksasa (hitung mundur) ----------

def angka_image(p, i):
    img = grain(foto_redup(p["foto"], W, H, 8000 + i, gelap=0.5, blur=4), 0.06).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 70), p["tanggal"].upper(), font=hn(28, 10), fill=(240, 230, 210), anchor="ma")
    num = str(p["angka"])
    fn_ = hn(560, 9)
    while d.textlength(num, font=fn_) > W - 120:
        fn_ = hn(fn_.size - 10, 9)
    d.text((W / 2, 520), num, font=fn_, fill=(255, 255, 255), anchor="ms")
    d.text((W / 2, 560), bersih(p.get("label", "HARI LAGI")).upper(), font=hn(56, 1), fill=(255, 255, 255), anchor="ma")
    d.text((W / 2, 636), bersih(p.get("sublabel", "menuju Natal")), font=georgia(50, True), fill=(255, 214, 140), anchor="ma")
    y = 730
    for ln in wrap(d, bersih(p["teks"]), georgia(36), W - 200):
        d.text((W / 2, y), ln, font=georgia(36), fill=(246, 240, 230), anchor="ma")
        y += 48
    ayat_bawah(img, p, y + 30, H - 70, (230, 226, 220), (255, 214, 140), start=30, stop=20)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(200, 196, 190), anchor="ma")
    return img


# ---------- TITIK (Reels): grid titik ----------

def titik_reel(p, idx, mod=MOD, seconds=11):
    rel = f"reels/{mod}/titik{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(8100 + idx)
    pitch, r = 16, 6.2
    cols, rows = RW // pitch, 62
    y0 = 230
    lines = bersih(p["teks"]).upper().split("\n")
    S = 4
    big = Image.new("L", (cols * S * 2, rows * S * 2), 0)
    gd = ImageDraw.Draw(big)
    fsize = 400
    f = hn(fsize, 9)
    while max(gd.textlength(ln, font=f) for ln in lines) > big.width - 60 or len(lines) * fsize * 1.05 > big.height - 40:
        fsize -= 10
        f = hn(fsize, 9)
    y = big.height / 2 - len(lines) * fsize * 1.05 / 2
    for ln in lines:
        gd.text((big.width / 2, y), ln, font=f, fill=255, anchor="ma")
        y += fsize * 1.05
    grid = np.asarray(big.resize((cols, rows), Image.BOX)) > 100
    urut = rng.permutation(int(grid.sum()))
    nyala_t = np.zeros(grid.shape)
    nyala_t[grid] = 1.2 + urut / max(1, grid.sum()) * 2.6
    bg = Image.new("RGBA", (RW, RH), (14, 16, 30, 255))
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fv, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 200, 380, 38, 24, 1.36)
    ayat = Image.new("RGBA", (RW, 520), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=fv, fill=(230, 232, 240), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 12), p["ref"], font=hn(32, 1), fill=(255, 206, 80), anchor="ma")
    ad.text((RW / 2, y + 66), "@" + HANDLE, font=hn(26, 10), fill=(150, 156, 180), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        d = ImageDraw.Draw(frame)
        for ry in range(rows):
            for cx_ in range(cols):
                x = cx_ * pitch + pitch / 2 + (RW - cols * pitch) / 2
                yy = y0 + ry * pitch + pitch / 2
                if grid[ry, cx_]:
                    if t < 0.6:
                        a = 1.0
                    elif t < 1.0:
                        a = 1 - (t - 0.6) / 0.4
                    else:
                        a = ease((t - nyala_t[ry, cx_]) / 0.25)
                    c = tuple(int(46 + (v - 46) * a) for v in (255, 206, 80))
                    rr = r * (0.8 + 0.25 * a)
                else:
                    c, rr = (40, 44, 64), r * 0.8
                d.ellipse((x - rr, yy - rr, x + rr, yy + rr), fill=c)
        if t >= 4.2:
            frame.alpha_composite(fade(ayat, ease((t - 4.2) / 0.7)), (0, y0 + rows * pitch + 60))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- PANGGUNG (Reels): lampu panggung ----------

def panggung_reel(p, idx, mod=MOD, seconds=12):
    rel = f"reels/{mod}/panggung{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(8200 + idx)
    kabut = render.fbm2d(RH // 4, RW // 4, rng, ((4, 1.0), (12, 0.6)))
    kabut = np.asarray(Image.fromarray((kabut * 255).astype(np.uint8)).resize((RW, RH), Image.BICUBIC)).astype(np.float32) / 255
    base = np.zeros((RH, RW, 3), np.float32) + np.array([10, 8, 22])
    warna = [np.array([120, 90, 255]), np.array([255, 120, 200]), np.array([90, 200, 255]), np.array([255, 200, 120])]
    yy, xx = np.mgrid[0:RH // 4, 0:RW // 4].astype(np.float32) * 4
    crowd = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    cd = ImageDraw.Draw(crowd)
    for k in range(26):
        x = k * 44 + rng.uniform(-10, 10)
        hgt = rng.uniform(140, 220)
        cd.ellipse((x - 26, RH - hgt - 52, x + 26, RH - hgt), fill=(4, 4, 8, 255))
        cd.rounded_rectangle((x - 40, RH - hgt - 10, x + 40, RH), radius=30, fill=(4, 4, 8, 255))
    for k in range(3):
        x = rng.uniform(200, RW - 200)
        cd.line((x, RH - 260, x + rng.uniform(-40, 40), RH - 420), fill=(4, 4, 8, 255), width=22)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    judul = Image.new("RGBA", (RW, 120), (0, 0, 0, 0))
    ImageDraw.Draw(judul).text((RW / 2, 0), bersih(p["judul"]), font=georgia(52, True), fill=(255, 236, 200), anchor="ma")
    baris = []
    for b in p["baris"]:
        f, ls, sz = pas(probe, bersih(b), lambda s: ft("Georgia Bold.ttf", s), RW - 160, 200, 64, 40, 1.15)
        lay = Image.new("RGBA", (RW, int(len(ls) * sz * 1.15 + 20)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for k, ln in enumerate(ls):
            ld.text((RW / 2, k * sz * 1.15), ln, font=f, fill=(255, 255, 255), anchor="ma")
        baris.append(lay)
    fv, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 300, 34, 24, 1.36)
    ayat = Image.new("RGBA", (RW, 420), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=fv, fill=(230, 226, 240), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 10), p["ref"], font=hn(30, 1), fill=(255, 210, 140), anchor="ma")
    ad.text((RW / 2, y + 60), "@" + HANDLE, font=hn(24, 10), fill=(160, 150, 180), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        lit = np.zeros((RH // 4, RW // 4), np.float32)
        img = base.copy()
        for k, c in enumerate(warna):
            sx = RW * (0.15 + 0.23 * k)
            ang = math.radians(90 + 22 * math.sin(t * 0.6 + k * 1.7))
            dx, dy = xx - sx, yy + 40
            proj = dx * math.cos(ang) + dy * math.sin(ang)
            perp = np.abs(-dx * math.sin(ang) + dy * math.cos(ang))
            beam = np.clip(1 - perp / (30 + proj * 0.22), 0, 1) * (proj > 0) * np.exp(-proj / 2200)
            beam_big = np.asarray(Image.fromarray((beam * 255).astype(np.uint8)).resize((RW, RH), Image.BILINEAR)).astype(np.float32) / 255
            img += (beam_big * (0.35 + 0.65 * kabut))[..., None] * c * 0.55
        frame = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
        frame.alpha_composite(crowd)
        frame.alpha_composite(judul, (0, 250))
        y = 420
        for k, lay in enumerate(baris):
            st = 0.0 if k == 0 else 1.2 + k * 1.6
            if t >= st:
                frame.alpha_composite(fade(lay, 1.0 if k == 0 else ease((t - st) / 0.6)), (0, y))
            y += lay.height + 30
        if t >= 5.2:
            frame.alpha_composite(fade(ayat, ease((t - 5.2) / 0.8)), (0, max(y + 40, 1000)))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= daftar gaya =================

SIMPLE = {
    # baru
    "KATAKUNCI": katakunci_image, "POSTERTEBAL": postertebal_image, "KARTUFOTO": kartufoto_image, "ANTIK": antik_image,
    "BOTANI": botani_image, "ARTIKEL": artikel_image, "BOCOR": bocor_image, "BERITA": berita_image, "KOLASE": kolase_image,
    "ANGKA": angka_image,
    # lama
    "BALON": gaya_w12.balon_image, "FILM": gaya_w10.film_image, "RASI": gaya_w10.rasi_image, "KARTUNATAL": gaya_w12.kartunatal_image,
    "SCROLL": gaya_w11.scroll_image, "PERJALANAN": gaya_w12.perjalanan_image, "TELEGRAM": gaya_w10.telegram_image,
    "TANYA": gaya_w10.tanya_image, "KACAPATRI": gaya_w11.kacapatri_image,
    # mix
    "FLIPNATAL": lambda p, i: gaya_w11.flipclock_image(p, i, latar=merah_salju(W, H, 8300 + i)),
    "KORANNATAL": lambda p, i: gaya_w8.koran_image(dict(p, _edisi="EDISI NATAL"), i, natal=True),
    "STAMPNATAL": lambda p, i: gaya_w12.stamp_image(p, i, latar=bintang_krem(W, H, 8400 + i)),
    "WATERCOLORMALAM": lambda p, i: gaya_w12.watercolor_image(p, i, malam=True),
    "PHOTOBOOTHNATAL": lambda p, i: gaya_w11.photobooth_image(p, i, latar=gaya_w10.bokeh(W, H, 8500 + i)),
    "TAGHIJAU": lambda p, i: gaya_w11.tag_image(p, i, kado_seed=1 + 3 * i),
    "CRAYONHITAM": lambda p, i: gaya_w12.crayon_image(p, i, hitam_=True),
    "KOPIMERAH": lambda p, i: gaya_w12.kopi_image(p, i, merah=True),
    "PIXELNATAL": lambda p, i: gaya_w11.pixel_image(p, i, natal=True),
    "EMAILGELAP": lambda p, i: gaya_w8.balik_gelap(gaya_w12.email_image(p, i)),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {"UTAS": gaya_w10.utas_files}
REELS = {"TITIK": (titik_reel, "titik"), "PANGGUNG": (panggung_reel, "panggung"), "KRANS": (gaya_w10.krans_reel, "krans"),
         "KONFETI": (gaya_w12.konfeti_reel, "konfeti"),
         "SALJUEMAS": (lambda p, i, mod: gaya_w11.salju_reel(p, i, mod, emas=True), "salju"),
         "LAMPUPOHON": (lambda p, i, mod: gaya_w12.lampu_reel(p, i, mod, pohon=True), "lampu")}


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
