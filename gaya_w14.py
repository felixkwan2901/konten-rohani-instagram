"""Akun Tenang - minggu 14 (konten/tenang_w14.py), 27 Des 2026 - 2 Jan 2027: tutup tahun & Tahun Baru.
36 gaya diacak tiap hari + komik Eli + hitung mundur Tahun Baru.
BARU (terinspirasi akun Instagram kreatif, isinya buatan sendiri):
       KATAHARI (papan tebak kata 5 huruf, a la NYT Games), GRAFIK (setahun dalam satu garis, a la grafik NYT Games),
       LENGKAPI (layar pelajaran aplikasi bahasa, a la Duolingo), ULASAN (kartu ulasan film, a la Letterboxd),
       CUKIL (poster cetak cukil lino, a la The Son & Stars), TIMBUL (angka timbul di kertas, a la 36 Days of Type),
       CORET (foto + coretan spidol putih, a la Notion), PANDUAN (seri "panduan lapangan" di langit gradasi, a la Headspace),
       TUMPUK (puisi punggung buku, a la Penguin Books), PAPAN (papan inspirasi bento, a la Pinterest),
       NAPAS (Reel latihan napas, a la Calm/Headspace), KEMBANGAPI (Reel kembang api yang membentuk kata).
LAMA : CATATAN, REKAP, JAMPASIR, TOPLES, BINGO, PROGRESS, SIGNPOST, SERTIFIKAT, FLIP, JAM, RESEP, KOMPAS.
MIX  : ALKITABCAHAYA, KETIKCAHAYA, KAMUSCAHAYA (bayang jendela sore, a la Poetry Is Not A Luxury),
       STICKYLANGIT, POLAROIDLANGIT (langit gradasi), BALONKEMBANG, FLIPTAHUN, PHOTOBOOTHKEMBANG, TIKETKEMBANG
       (malam kembang api), KALENDERTAHUN (kalender sobek tanpa hiasan Natal), UNDANGANTAHUN, KONFETIMALAM (Reel).

  python3 gaya_w14.py [reels]
"""
import datetime as dt
import importlib
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cerita
import config
import gaya_w5
import gaya_w6
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import gaya_w11
import gaya_w12
import render
from gaya_w6 import cover, foto_warna, georgia, hn
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tanpa_kutip
from gaya_w9 import ayat_bawah
from gaya_w11 import konteks
from gaya_w13 import foto_redup
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w14"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2026, 12, 27)


def avenir(size, idx=0):  # 0 Bold, 2 Demi, 5 Medium, 7 Regular, 8 Heavy, 9 Heavy Italic
    return ft("/System/Library/Fonts/Avenir Next.ttc", size, idx)


def bulat(size, berat="Bold"):
    f = ImageFont.truetype("/System/Library/Fonts/SFNSRounded.ttf", size)
    f.set_variation_by_name(berat)
    return f


def spidol(size):
    return ft("Bradley Hand Bold.ttf", size)


def charter(size, idx=0):  # 0 Roman, 1 Italic, 3 Bold, 5 Black
    return ft("Charter.ttc", size, idx)


def kilau(d, x, y, r, col):
    """Bintang kilau empat sudut."""
    k = r * 0.22
    d.polygon([(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)], fill=col)


def langit(w, h, seed, atas=(70, 128, 236), bawah=(248, 178, 196)):
    """Langit gradasi biru ke merah muda dengan awan lembut dan kilau (a la Headspace)."""
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, atas, bawah).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for k in range(6):
        cx = rng.uniform(-80, w + 80)
        cy = rng.uniform(h * 0.8, h + 80) if k % 2 == 0 else rng.uniform(-60, h * 0.18)
        for _ in range(8):
            rx, ry = rng.uniform(90, 210), rng.uniform(50, 100)
            x, y = cx + rng.uniform(-200, 200), cy + rng.uniform(-40, 40)
            d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(255, 255, 255, 110))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    for _ in range(max(4, int(w * h / 110000))):
        kilau(d, rng.uniform(40, w - 40), rng.uniform(40, h - 40), rng.uniform(9, 20), (255, 255, 255, 210))
    return grain(img.convert("RGB"), 0.03)


def ledakan(d, x, y, r, col, rng, n=46):
    for k in range(n):
        a = 2 * math.pi * k / n + rng.uniform(-0.05, 0.05)
        rr = r * rng.uniform(0.72, 1.0)
        for s in np.linspace(0.3, 1, 8):
            px, py = x + math.cos(a) * rr * s, y + math.sin(a) * rr * s + 22 * s * s
            pr = 1.6 + 2.4 * s
            d.ellipse((px - pr, py - pr, px + pr, py + pr), fill=col + (int(70 + 170 * s),))


def kembang_latar(w, h, seed, n=5, zona=(0.04, 0.6)):
    """Langit malam dengan kembang api diam (malam Tahun Baru)."""
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (10, 14, 42), (40, 24, 68)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 5000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(0.8, 2.4)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(rng.uniform(50, 190))))
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    warna = [(255, 206, 90), (255, 120, 160), (120, 200, 255), (190, 150, 255), (255, 246, 220)]
    for k in range(n):
        x, y = rng.uniform(0.08, 0.92) * w, rng.uniform(*zona) * h
        ledakan(ld, x, y, rng.uniform(110, 210), warna[(k + seed) % 5], rng)
    glow = lay.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(glow)
    img.alpha_composite(glow)
    img.alpha_composite(lay)
    return grain(img.convert("RGB"), 0.03)


def cahaya(img, seed, kuat=0.34):
    """Bayang jendela sore di atas kertas: kisi jendela miring + bayang daun, cahaya hangat."""
    rng = np.random.default_rng(seed)
    w, h = img.size
    s = 4
    sw, sh = w // s, h // s
    m = Image.new("L", (sw * 2, sh * 2), 0)
    d = ImageDraw.Draw(m)
    pw, ph = sw * 0.62, sh * 0.5
    x0, y0 = sw * 0.5 - pw - 4 + rng.uniform(-20, 20), sh * 0.5 - ph * 0.4
    for cx in (0, 1):
        for cy in (0, 1):
            d.rectangle((x0 + cx * (pw + 9), y0 + cy * (ph + 9), x0 + cx * (pw + 9) + pw, y0 + cy * (ph + 9) + ph), fill=255)
    m = m.rotate(rng.uniform(-30, -20), resample=Image.BICUBIC, center=(sw, sh))
    m = m.crop((sw // 2, sh // 2, sw // 2 + sw, sh // 2 + sh))
    # ranting dan daun memotong cahaya di pojok atas
    dd = ImageDraw.Draw(m)
    bx, by = rng.uniform(sw * 0.55, sw * 0.95), -5
    for k in range(3):
        ex, ey = bx - rng.uniform(40, 110), by + rng.uniform(60, 140)
        dd.line((bx, by, ex, ey), fill=0, width=2)
        for t in np.linspace(0.2, 1, 6):
            lx, ly = bx + (ex - bx) * t, by + (ey - by) * t
            leaf = Image.new("L", (40, 40), 0)
            ImageDraw.Draw(leaf).ellipse((20 - 10, 20 - 4, 20 + 10, 20 + 4), fill=255)
            leaf = leaf.rotate(rng.uniform(0, 180), resample=Image.BICUBIC)
            m.paste(0, (int(lx - 20 + rng.uniform(-8, 8)), int(ly - 20)), leaf)
        bx, by = ex + rng.uniform(-10, 30), by + rng.uniform(10, 40)
    m = m.filter(ImageFilter.GaussianBlur(2.2)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
    a = np.asarray(m).astype(np.float32)[..., None] / 255
    base = np.asarray(img.convert("RGB")).astype(np.float32)
    teduh = base * (1 - kuat) * np.array([0.96, 0.98, 1.04])
    hangat = np.minimum(255, base * np.array([1.05, 1.0, 0.9]) + np.array([16, 8, 0]))
    return Image.fromarray(np.clip(teduh * (1 - a) + hangat * a, 0, 255).astype(np.uint8))


def goresan(d, pts, w, col, rng, jitter=1.6):
    pts = [(x + rng.normal(0, jitter), y + rng.normal(0, jitter)) for x, y in pts]
    d.line(pts, fill=col, width=int(w), joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=col)


def kurva(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in np.linspace(0, 1, n)]


def panah(d, p0, p1, p2, w, col, rng):
    pts = kurva(p0, p1, p2)
    goresan(d, pts, w, col, rng)
    (ax, ay), (bx, by) = pts[-3], pts[-1]
    a = math.atan2(by - ay, bx - ax)
    for s in (1, -1):
        goresan(d, [(bx, by), (bx - math.cos(a + s * 0.5) * w * 5, by - math.sin(a + s * 0.5) * w * 5)], w, col, rng, 0.8)


def ubin(img, box, isi, radius=28):
    """Tempel gambar/warna ke kotak bersudut bulat."""
    x0, y0, x1, y1 = [int(v) for v in box]
    tw, th = x1 - x0, y1 - y0
    tile = isi.resize((tw, th)) if isinstance(isi, Image.Image) else Image.new("RGB", (tw, th), isi)
    mask = Image.new("L", (tw * 3, th * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw * 3 - 1, th * 3 - 1), radius=radius * 3, fill=255)
    img.paste(tile.convert("RGB"), (x0, y0), mask.resize((tw, th), Image.LANCZOS))


def ayat_tengah(img, p, y0, y1, warna, warna_ref, maxw=W - 180, start=40, stop=22):
    """Ayat + referensi, ditaruh di tengah ruang kosong y0..y1."""
    d = ImageDraw.Draw(img)
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), maxw, y1 - y0 - 70, start, stop, 1.36)
    tinggi = len(lines) * size * 1.36 + 50
    y = y0 + max(0, (y1 - y0 - tinggi) / 2)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=warna, anchor="ma")
        y += size * 1.36
    d.text((W / 2, y + 12), p["ref"], font=hn(30, 1), fill=warna_ref, anchor="ma")


# ================= BARU =================

# ---------- KATAHARI: papan tebak kata 5 huruf ----------

HIJAU_K, KUNING_K, ABU_K, KOSONG_K = (106, 170, 100), (201, 180, 88), (120, 124, 126), (211, 214, 218)


def warna_tebakan(tebak, kata):
    hasil = [ABU_K] * 5
    sisa = {}
    for k in range(5):
        if tebak[k] == kata[k]:
            hasil[k] = HIJAU_K
        else:
            sisa[kata[k]] = sisa.get(kata[k], 0) + 1
    for k in range(5):
        if hasil[k] != HIJAU_K and sisa.get(tebak[k], 0) > 0:
            hasil[k] = KUNING_K
            sisa[tebak[k]] -= 1
    return hasil


def katahari_image(p, i):
    img = grain(Image.new("RGB", (W, H), (255, 255, 255)), 0.015).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 62), ("KATA HARI INI  ·  " + p.get("_tanggal", "")).upper(), font=hn(24, 10), fill=(120, 124, 126), anchor="ma")
    fj = ft("Georgia Bold.ttf", 54)
    while d.textlength(bersih(p["judul"]), font=fj) > W - 140:
        fj = ft("Georgia Bold.ttf", fj.size - 2)
    d.text((W / 2, 104), bersih(p["judul"]), font=fj, fill=(18, 18, 19), anchor="ma")
    d.line((60, 192, W - 60, 192), fill=KOSONG_K, width=2)
    rows = [t.upper() for t in p["tebakan"]] + [p["kata"].upper()]
    ts, gap = 116, 11
    x0, y0 = (W - (5 * ts + 4 * gap)) / 2, 222
    fl = hn(66, 1)
    for r in range(6):
        y = y0 + r * (ts + gap)
        for k in range(5):
            x = x0 + k * (ts + gap)
            if r < len(rows):
                col = warna_tebakan(rows[r], rows[-1])[k]
                d.rectangle((x, y, x + ts, y + ts), fill=col)
                d.text((x + ts / 2, y + ts / 2 + 2), rows[r][k], font=fl, fill="white", anchor="mm")
            else:
                d.rectangle((x, y, x + ts - 1, y + ts - 1), outline=KOSONG_K, width=3)
    y = y0 + 6 * (ts + gap) + 22
    for ln in wrap(d, bersih(p["teks"]), georgia(34, True), W - 200):
        d.text((W / 2, y), ln, font=georgia(34, True), fill=(60, 60, 64), anchor="ma")
        y += 46
    ayat_tengah(img, p, y + 10, H - 70, (40, 40, 44), (83, 141, 78), start=36)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=hn(22, 10), fill=(150, 150, 154), anchor="ma")
    return img


# ---------- GRAFIK: setahun dalam satu garis ----------

def catmull(pts, n=18):
    pts = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for k in range(1, len(pts) - 2):
        p0, p1, p2, p3 = [np.array(v, np.float32) for v in pts[k - 1:k + 3]]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    out.append(tuple(pts[-2]))
    return out


def grafik_image(p, i):
    img = Image.new("RGB", (W, H), (252, 251, 247))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 54):
        d.line((x, 0, x, H), fill=(240, 238, 232), width=1)
    for y in range(0, H, 54):
        d.line((0, y, W, y), fill=(240, 238, 232), width=1)
    img = grain(img, 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    merah, tinta, emas = (220, 78, 58), (28, 28, 32), (206, 152, 40)
    d.text((80, 70), "GRAFIK TAHUN INI", font=hn(24, 1), fill=merah)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: hn(s, 1), W - 160, 140, 56, 38, 1.12)
    y = 108
    for ln in lines:
        d.text((80, y), ln, font=f, fill=tinta)
        y += size * 1.12
    x0, x1 = 110, W - 90
    ytop, ybot = y + 80, y + 700
    d.line((x0, ybot, x1, ybot), fill=tinta, width=3)
    d.line((x0, ytop - 10, x0, ybot), fill=tinta, width=3)
    d.text((x0 - 14, ytop - 4), "naik", font=hn(20, 10), fill=(140, 140, 140), anchor="ra")
    d.text((x0 - 14, ybot - 26), "turun", font=hn(20, 10), fill=(140, 140, 140), anchor="ra")
    titik = p["titik"]
    xs = np.linspace(x0 + 50, x1 - 40, len(titik))
    ys = [ybot - 30 - v / 100 * (ybot - ytop - 150) for _, v in titik]
    gy = ytop + 34  # garis lurus kasih setia
    lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.line((x0 * 2, gy * 2, x1 * 2, gy * 2), fill=emas + (255,), width=16)
    curve = catmull(list(zip(xs, ys)))
    ld.line([(a * 2, b * 2) for a, b in curve], fill=tinta + (255,), width=10, joint="curve")
    for x, yy in zip(xs, ys):
        ld.ellipse((x * 2 - 18, yy * 2 - 18, x * 2 + 18, yy * 2 + 18), fill=(255, 255, 255, 255), outline=tinta + (255,), width=7)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    d.text((x1, gy - 14), bersih(p["garis"]), font=georgia(36, True), fill=(160, 112, 20), anchor="rs")
    fl = hn(30, 10)
    for k, ((lab, v), x, yy) in enumerate(zip(titik, xs, ys)):
        tetangga = [titik[j][1] for j in (k - 1, k + 1) if 0 <= j < len(titik)]
        bawah = all(v <= t for t in tetangga)
        lx = min(max(x, x0 + 90), x1 - 80)
        lines = wrap(d, bersih(lab), fl, 190)
        if bawah:
            for n, ln in enumerate(lines):
                d.text((lx, yy + 26 + n * 34), ln, font=fl, fill=tinta, anchor="ma")
        else:
            for n, ln in enumerate(reversed(lines)):
                d.text((lx, yy - 26 - n * 34), ln, font=fl, fill=tinta, anchor="md")
    d.text((xs[0], ybot + 16), "JAN", font=hn(22, 1), fill=(140, 140, 140), anchor="ma")
    d.text((xs[-1], ybot + 16), "DES", font=hn(22, 1), fill=(140, 140, 140), anchor="ma")
    ayat_tengah(img, p, ybot + 60, H - 70, (40, 40, 44), merah, start=38)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=hn(22, 10), fill=(150, 150, 150), anchor="ma")
    return img


# ---------- LENGKAPI: layar pelajaran aplikasi bahasa ----------

HIJAU_L, HIJAU_L2, ABU_L, TEKS_L = (88, 204, 2), (70, 163, 0), (229, 229, 229), (75, 75, 75)


def api_kecil(s):
    def gambar(d, k):
        for (r, col, dy) in ((s * 0.46, (255, 150, 0, 255), 0), (s * 0.28, (255, 210, 60, 255), s * 0.12)):
            cx, cy = s / 2, s * 0.52 + dy
            pts = [(cx + r * 0.95 * math.sin(t) * abs(math.sin(t / 2)) ** 1.1, cy - r * 1.05 * math.cos(t)) for t in np.linspace(0, 2 * math.pi, 60)]
            d.polygon([(x * k, y * k) for x, y in pts], fill=col)
    return sprite(s, s, gambar)


def chip(img, x, y, teks, f, h=80, kosong=False, pilih=False):
    d = ImageDraw.Draw(img)
    w = d.textlength(teks, font=f) + 64
    if kosong:
        d.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=ABU_L)
        return w
    tepi = (88, 204, 2) if pilih else ABU_L
    d.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=tepi)
    d.rounded_rectangle((x + 3, y + 3, x + w - 3, y + h - 8), radius=18, fill=(255, 255, 255) if not pilih else (240, 255, 228))
    d.text((x + w / 2, y + h / 2 - 3), teks, font=f, fill=HIJAU_L2 if pilih else TEKS_L, anchor="mm")
    return w


def lengkapi_image(p, i):
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    d.line((70, 70, 104, 104), fill=(175, 175, 175), width=7)
    d.line((70, 104, 104, 70), fill=(175, 175, 175), width=7)
    d.rounded_rectangle((140, 74, W - 210, 102), radius=14, fill=ABU_L)
    d.rounded_rectangle((140, 74, 140 + (W - 350) * 0.82, 102), radius=14, fill=HIJAU_L)
    d.rounded_rectangle((156, 80, 140 + (W - 350) * 0.82 - 16, 86), radius=3, fill=(140, 224, 80))
    comp(img, api_kecil(56), (W - 190, 60))
    d.text((W - 128, 89), str(p["streak"]), font=bulat(40, "Heavy"), fill=(255, 150, 0), anchor="lm")
    d.text((70, 166), bersih(p["perintah"]), font=bulat(60, "Heavy"), fill=(60, 60, 60))
    # kalimat dengan kotak jawaban terisi
    fk = bulat(48, "Semibold")
    jawab = bersih(p["jawaban"])
    token = []
    for w in bersih(p["kalimat"]).split():
        m = re.match(r"^(.*?)___(.*)$", w)
        if m:
            if m.group(1):
                token.append(("kata", m.group(1)))
            token.append(("jawab", jawab))
            if m.group(2):
                token.append(("kata", m.group(2)))
        else:
            token.append(("kata", w))
    sp = d.textlength(" ", font=fk)
    lebar = lambda t: d.textlength(t[1], font=fk) + (64 if t[0] == "jawab" else 0)
    baris, cur, cw = [], [], 0
    for t in token:
        tw = lebar(t)
        tempel = t[0] == "kata" and cur and cur[-1][0] == "jawab" and not t[1][0].isalnum()
        if cur and not tempel and cw + sp + tw > W - 140:
            baris.append(cur)
            cur, cw = [], 0
        cur.append(t)
        cw += tw + (0 if tempel else sp)
    baris.append(cur)
    y = 280
    for b in baris:
        x = 70
        for k, t in enumerate(b):
            if k and not (t[0] == "kata" and b[k - 1][0] == "jawab" and not t[1][0].isalnum()):
                x += sp
            if t[0] == "jawab":
                x += chip(img, x, y - 10, t[1], fk, h=84, pilih=True)
            else:
                d.text((x, y + 30), t[1], font=fk, fill=TEKS_L, anchor="lm")
                x += d.textlength(t[1], font=fk)
        d.line((70, y + 86, W - 70, y + 86), fill=ABU_L, width=3)
        y += 100
    # bank kata
    y += 40
    fc = bulat(44, "Semibold")
    ws = [d.textlength(bersih(w), font=fc) + 64 for w in p["pilihan"]]
    while sum(ws) + 20 * (len(ws) - 1) > W - 110 and fc.size > 30:  # usahakan bank kata satu baris
        fc = bulat(fc.size - 2, "Semibold")
        ws = [d.textlength(bersih(w), font=fc) + 64 for w in p["pilihan"]]
    rows, cur = [], []
    for k, w in enumerate(ws):
        if cur and sum(ws[j] for j in cur) + 20 * len(cur) + w > W - 100:
            rows.append(cur)
            cur = []
        cur.append(k)
    rows.append(cur)
    for r in rows:
        tot = sum(ws[k] for k in r) + 20 * (len(r) - 1)
        x = (W - tot) / 2
        for k in r:
            w = bersih(p["pilihan"][k])
            chip(img, x, y, w, fc, h=88, kosong=w.lower() == jawab.lower())
            x += ws[k] + 20
        y += 108
    # panel benar
    yb = min(max(y + 30, 800), 920)
    d.rectangle((0, yb, W, H), fill=(215, 255, 184))
    d.ellipse((60, yb + 28, 124, yb + 92), fill=(255, 255, 255))
    d.line((76, yb + 60, 88, yb + 74, 110, yb + 46), fill=HIJAU_L2, width=9, joint="curve")
    d.text((146, yb + 60), bersih(p["pujian"]), font=bulat(52, "Heavy"), fill=HIJAU_L2, anchor="lm")
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), W - 160, (H - 214) - (yb + 112) - 46, 36, 24, 1.32)
    yy = yb + 112
    for ln in lines:
        d.text((80, yy), ln, font=f, fill=(58, 110, 20))
        yy += size * 1.32
    d.text((80, yy + 6), p["ref"].upper(), font=bulat(30, "Heavy"), fill=HIJAU_L2)
    d.rounded_rectangle((60, H - 186, W - 60, H - 92), radius=22, fill=HIJAU_L2)
    d.rounded_rectangle((60, H - 192, W - 60, H - 100), radius=22, fill=HIJAU_L)
    d.text((W / 2, H - 146), "LANJUTKAN", font=bulat(40, "Heavy"), fill="white", anchor="mm")
    d.text((W / 2, H - 50), "@" + HANDLE, font=bulat(24, "Semibold"), fill=(110, 160, 70), anchor="ma")
    return img


# ---------- ULASAN: kartu ulasan film ----------

def bintang_poly(cx, cy, r):
    return [(cx + (r if k % 2 == 0 else r * 0.45) * math.sin(math.pi * k / 5), cy - (r if k % 2 == 0 else r * 0.45) * math.cos(math.pi * k / 5)) for k in range(10)]


def ulasan_image(p, i):
    bg, abu, putih, hijau = (20, 24, 28), (153, 170, 187), (226, 232, 238), (64, 188, 96)
    img = grain(Image.new("RGB", (W, H), bg), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((70, 66), "ULASAN", font=hn(24, 1), fill=abu)
    d.text((W - 70, 66), "@" + HANDLE, font=hn(22, 10), fill=(100, 114, 128), anchor="ra")
    av = gradasi(80, 80, (250, 180, 90), (220, 90, 120))
    ubin(img, (70, 132, 150, 212), av, radius=40)
    d.text((110, 172), bersih(p["pengulas"])[:1].upper(), font=hn(40, 1), fill="white", anchor="mm")
    d.text((172, 172), "Ulasan oleh ", font=hn(30, 0), fill=abu, anchor="lm")
    d.text((172 + d.textlength("Ulasan oleh ", font=hn(30, 0)), 172), bersih(p["pengulas"]), font=hn(30, 1), fill=putih, anchor="lm")
    # poster
    px0, py0, pw, ph = W - 70 - 236, 252, 236, 354
    scene = ["fajar", "bintang", "kabut", "laut"][i % 4]
    poster = cover(foto_warna(scene, 480, 720, seed=9100 + i), pw, ph).convert("RGBA")
    pd = ImageDraw.Draw(poster)
    pd.rectangle((0, ph - 120, pw, ph), fill=(0, 0, 0, 90))
    for k, ln in enumerate(wrap(pd, bersih(p["judul"]).upper(), hn(26, 1), pw - 30)[:3]):
        pd.text((pw / 2, ph - 104 + k * 30), ln, font=hn(26, 1), fill="white", anchor="ma")
    bayangan(img, poster, (px0, py0), blur=10, geser=(0, 8), kuat=0.5)
    d = ImageDraw.Draw(img)
    d.rectangle((px0 - 1, py0 - 1, px0 + pw, py0 + ph), outline=(68, 85, 102), width=2)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: ft("Georgia Bold.ttf", s), W - 140 - pw - 60, 230, 72, 46, 1.1)
    y = 262
    for ln in lines:
        d.text((70, y), ln, font=f, fill="white")
        y += size * 1.1
    d.text((70, y + 6), bersih(p["tahun"]), font=hn(34, 0), fill=abu)
    y += 72
    bint = float(p["bintang"])
    lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for k in range(5):
        cx = (70 + 26 + k * 58) * 2
        poly = bintang_poly(cx, (y + 26) * 2, 52)
        if bint >= k + 1:
            ld.polygon(poly, fill=hijau + (255,))
        elif bint >= k + 0.5:
            half = Image.new("RGBA", lay.size, (0, 0, 0, 0))
            ImageDraw.Draw(half).polygon(poly, fill=hijau + (255,))
            lay.alpha_composite(half.crop((0, 0, cx, lay.height)), (0, 0))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    y = max(y + 90, py0 + ph + 50)
    fr = hn(40, 0)
    for ln in wrap(d, bersih(p["ulasan"]), fr, W - 140):
        d.text((70, y), ln, font=fr, fill=putih)
        y += 56
    y += 18
    hx, hy = 82, y + 16
    d.polygon([(hx - 12, hy - 4), (hx, hy + 12), (hx + 12, hy - 4)], fill=(255, 128, 0))
    d.ellipse((hx - 13, hy - 12, hx + 1, hy + 2), fill=(255, 128, 0))
    d.ellipse((hx - 1, hy - 12, hx + 13, hy + 2), fill=(255, 128, 0))
    d.text((106, y + 16), f"{p['suka']:,} suka".replace(",", "."), font=hn(28, 0), fill=abu, anchor="lm")
    y += 76
    d.line((70, y, W - 70, y), fill=(44, 52, 60), width=2)
    ayat_tengah(img, p, y + 20, H - 50, (200, 210, 220), hijau, start=36)
    return img


# ---------- CUKIL: poster cetak cukil lino ----------

def kertas_cukil(w, h, seed):
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), np.float32) + np.array([231, 228, 220])
    base *= (0.96 + 0.06 * render.fbm2d(h, w, rng, ((3, 1.0), (40, 0.5), (200, 0.3))))[..., None]
    return grain(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), 0.05)


def tinta(mask, seed, kasar=0.5):
    """Mask L -> alpha tinta cetak: tepi kasar + bintik kertas yang tidak kena tinta."""
    rng = np.random.default_rng(seed)
    a = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255
    h, w = a.shape
    n = render.fbm2d(h, w, rng, ((2, 1.0), (6, 0.5)))
    a = np.clip((a - 0.5 + (n - 0.5) * 0.35 * kasar) * 6 + 0.5, 0, 1)
    bintik = rng.random((h, w)) < 0.012
    a[bintik] *= 0.25
    a *= 0.86 + 0.14 * render.fbm2d(h, w, rng, ((20, 1.0), (80, 0.6)))
    return a


def pahat(d, pts, S, w=5):
    d.line([(x * S, y * S) for x, y in pts], fill=0, width=int(w * S), joint="curve")


def ikon_cukil(nama, bw, bh, S, rng):
    """-> dict warna -> mask L (ukuran bw*S x bh*S). Garis 'pahat' = goresan putih di tinta hitam."""
    hitam, merah, kunyit, biru = [Image.new("L", (bw * S, bh * S), 0) for _ in range(4)]
    dh, dm, dk, db = [ImageDraw.Draw(m) for m in (hitam, merah, kunyit, biru)]
    P = lambda pts: [(x * S, y * S) for x, y in pts]
    E = lambda cx, cy, rx, ry: (S * (cx - rx), S * (cy - ry), S * (cx + rx), S * (cy + ry))

    def bukit(d, puncak_x, puncak_y, lebar, alas):
        xs = np.linspace(puncak_x - lebar, puncak_x + lebar, 40)
        ys = [alas - (alas - puncak_y) * (math.cos((x - puncak_x) / lebar * math.pi / 2) ** 1.6) for x in xs]
        d.polygon(P([(xs[0], alas)] + list(zip(xs, ys)) + [(xs[-1], alas)]), fill=255)
        return xs, ys

    def arsir_bukit(xs, ys, alas, jarak=24):
        for off in range(jarak, int(alas - min(ys)), jarak):
            seg = [(x, y + off) for x, y in zip(xs, ys) if y + off < alas - 6]
            if len(seg) > 3:
                k0 = int(rng.integers(0, max(1, len(seg) // 4)))
                pahat(dh, seg[k0:len(seg) - int(rng.integers(0, max(1, len(seg) // 4)))], S, 4)

    if nama == "matahari":
        cx, cy = bw / 2, bh * 0.62
        dm.ellipse(E(cx, cy, 170, 170), fill=255)
        for k in range(15):
            a = math.pi + math.pi * (k + 0.5) / 15
            dk.polygon(P([(cx + math.cos(a - 0.05) * 200, cy + math.sin(a - 0.05) * 200), (cx + math.cos(a) * 320, cy + math.sin(a) * 320),
                          (cx + math.cos(a + 0.05) * 200, cy + math.sin(a + 0.05) * 200)]), fill=255)
        xs, ys = bukit(dh, bw * 0.28, bh * 0.5, bw * 0.5, bh)
        arsir_bukit(xs, ys, bh)
        xs2, ys2 = bukit(dh, bw * 0.78, bh * 0.6, bw * 0.45, bh)
        dh.line(P(list(zip(xs2, ys2))), fill=0, width=int(6 * S))
        arsir_bukit(xs2, ys2, bh, 28)
    elif nama == "pintu":
        dh.rectangle((0, 0, bw * S, bh * S), fill=255)
        ax0, ax1, atop, abot = bw * 0.36, bw * 0.64, bh * 0.16, bh * 0.86
        r = (ax1 - ax0) / 2
        dh.rectangle(P([(ax0, atop + r), (ax1, abot)]), fill=0)
        dh.pieslice(E(bw / 2, atop + r, r, r), 180, 360, fill=0)
        dk.rectangle(P([(ax0, atop + r), (ax1, abot)]), fill=255)
        dk.pieslice(E(bw / 2, atop + r, r, r), 180, 360, fill=255)
        dk.polygon(P([(ax0, abot), (ax1, abot), (bw * 0.92, bh), (bw * 0.08, bh)]), fill=255)
        dh.polygon(P([(ax0, abot), (ax1, abot), (bw * 0.92, bh), (bw * 0.08, bh)]), fill=0)
        dm.polygon(P([(ax1, atop + r * 0.6), (ax1 + 90, atop + r * 0.2), (ax1 + 90, abot + 30), (ax1, abot)]), fill=255)
        dh.polygon(P([(ax1, atop + r * 0.6), (ax1 + 90, atop + r * 0.2), (ax1 + 90, abot + 30), (ax1, abot)]), fill=0)
        for y in range(18, int(bh * 0.86), 36):  # bata
            pahat(dh, [(0, y), (ax0 - 14, y)], S, 4)
            pahat(dh, [(ax1 + 104, y), (bw, y)], S, 4)
            for x in range(18 + (y // 36 % 2) * 40, int(bw), 80):
                if x < ax0 - 20 or x > ax1 + 110:
                    pahat(dh, [(x, y), (x, y + 36)], S, 4)
        for k in range(9):  # sinar di lantai
            t = (k + 0.5) / 9
            pahat(dh, [(ax0 + (ax1 - ax0) * t, abot + 8), (bw * 0.08 + bw * 0.84 * t, bh - 4)], S, 3)
    elif nama == "pelita":
        cx, cy = bw * 0.44, bh * 0.74
        fx, fy = cx + 250, cy - 50
        for k, rr in enumerate(range(214, 80, -34)):
            dk.ellipse(E(fx, fy - 110, rr, rr), fill=255 if k % 2 == 0 else 0)
        body = [(cx - 230, cy - 10), (cx - 120, cy - 70), (cx + 60, cy - 72), (cx + 240, cy - 50), (cx + 262, cy - 30), (cx + 150, cy + 30),
                (cx + 60, cy + 80), (cx - 120, cy + 84), (cx - 220, cy + 40)]
        dh.polygon(P(body), fill=255)
        dh.ellipse(E(cx - 250, cy + 10, 50, 44), fill=255)
        dh.ellipse(E(cx - 250, cy + 10, 24, 20), fill=0)
        dh.ellipse(E(cx - 20, cy - 70, 70, 20), fill=0)
        dh.rectangle(P([(cx - 170, cy + 84), (cx + 90, cy + 112)]), fill=255)
        for k in range(4):
            pahat(dh, kurva((cx - 160, cy + 10 + k * 18), (cx, cy + 40 + k * 14), (cx + 180, cy - 10 + k * 10)), S, 4)
        pts = [(fx + 70 * math.sin(t) * abs(math.sin(t / 2)) ** 1.2, fy - 110 - 120 * math.cos(t)) for t in np.linspace(0, 2 * math.pi, 50)]
        dm.polygon(P(pts), fill=255)
        dk.polygon(P(pts), fill=0)
        dm.polygon(P([(fx + 0.42 * (x - fx), fy - 60 + 0.42 * (y - fy + 60)) for x, y in pts]), fill=0)
        for k in range(13):
            a = -math.pi / 2 + (k - 6) * 0.26
            dh.line(P([(fx + math.cos(a) * 232, fy - 110 + math.sin(a) * 232), (fx + math.cos(a) * 272, fy - 110 + math.sin(a) * 272)]), fill=255, width=int(9 * S))
    elif nama == "jangkar":
        cx = bw / 2
        db.rectangle(P([(0, bh * 0.74), (bw, bh)]), fill=255)
        for k in range(5):
            y = bh * 0.78 + k * 26
            pts = [(x, y + 8 * math.sin(x / 34 + k)) for x in range(0, int(bw) + 10, 10)]
            db.line(P(pts), fill=0, width=int(5 * S))
        dh.ellipse(E(cx, bh * 0.1, 46, 46), fill=255)
        dh.ellipse(E(cx, bh * 0.1, 24, 24), fill=0)
        dh.rectangle(P([(cx - 20, bh * 0.15), (cx + 20, bh * 0.8)]), fill=255)
        dh.rounded_rectangle(P([(cx - 150, bh * 0.24), (cx + 150, bh * 0.29)]), radius=10 * S, fill=255)
        dh.arc(E(cx, bh * 0.52, 230, 230), 25, 155, fill=255, width=int(40 * S))
        for s_ in (1, -1):
            ex, ey = cx + s_ * 230 * math.cos(math.radians(25)), bh * 0.52 + 230 * math.sin(math.radians(25))
            dh.polygon(P([(ex - s_ * 10, ey - 70), (ex + s_ * 46, ey - 10), (ex - s_ * 40, ey + 10)]), fill=255)
        pahat(dh, [(cx - 6, bh * 0.32), (cx - 6, bh * 0.74)], S, 4)
        dm.line(P(kurva((cx - 30, bh * 0.2), (cx - 160, bh * 0.4), (cx + 10, bh * 0.46)) + kurva((cx + 10, bh * 0.46), (cx + 160, bh * 0.52), (cx - 10, bh * 0.66))),
                fill=255, width=int(16 * S), joint="curve")
    elif nama == "jalan":
        hz = bh * 0.42
        dm.ellipse(E(bw / 2, hz - 60, 92, 92), fill=255)
        for k in range(20):
            a = math.pi + math.pi * (k + 0.5) / 20
            dk.line(P([(bw / 2 + math.cos(a) * 112, hz - 60 + math.sin(a) * 112), (bw / 2 + math.cos(a) * 170, hz - 60 + math.sin(a) * 170)]), fill=255, width=int(10 * S))
        tanah = [(0, hz + 40)] + [(x, hz + 18 * math.sin(x / 120) + 10) for x in np.linspace(0, bw, 40)] + [(bw, bh), (0, bh)]
        dh.polygon(P(tanah), fill=255)
        for y in range(int(hz + 50), int(bh), 26):
            pahat(dh, [(x, y + 6 * math.sin(x / 70 + y)) for x in np.linspace(0, bw, 30)], S, 4)
        jalur = [(bw / 2 + 150 * math.sin((1 - t) * 4.0) * t, hz + 24 + (bh - hz - 24) * t) for t in np.linspace(0, 1, 60)]
        for k, (x, y) in enumerate(jalur):
            wid = 6 + 150 * (k / len(jalur)) ** 1.5
            dh.ellipse(E(x, y, wid, 8 + wid * 0.18), fill=0)
    else:  # burung
        db.ellipse(E(bw / 2, bh * 0.45, 250, 250), fill=255)
        for rr in range(236, 120, -30):
            db.arc(E(bw / 2, bh * 0.45, rr, rr), 200, 340, fill=0, width=int(4 * S))
        cx, cy = bw / 2, bh * 0.47
        db.ellipse(E(cx, cy, 120, 52), fill=0)
        db.ellipse(E(cx + 120, cy - 36, 40, 36), fill=0)
        db.polygon(P([(cx + 154, cy - 40), (cx + 196, cy - 30), (cx + 156, cy - 22)]), fill=0)
        db.polygon(P([(cx - 30, cy - 20), (cx - 160, cy - 200), (cx - 60, cy - 170), (cx + 40, cy - 30)]), fill=0)
        db.polygon(P([(cx - 110, cy + 10), (cx - 230, cy + 60), (cx - 200, cy - 10)]), fill=0)
        dh.ellipse(E(cx + 128, cy - 44, 6, 6), fill=255)
        tx, ty = cx + 186, cy - 30
        dk.line(P(kurva((tx, ty), (tx + 90, ty + 30), (tx + 170, ty + 120))), fill=255, width=int(8 * S))
        for k, t in enumerate(np.linspace(0.12, 0.95, 7)):
            lx, ly = tx + 170 * t, ty + 120 * t * t + 6
            dk.ellipse(E(lx + (20 if k % 2 else -20), ly + (8 if k % 2 else -14), 26, 12), fill=255)
        xs, ys = bukit(dh, bw * 0.3, bh * 0.82, bw * 0.45, bh)
        arsir_bukit(xs, ys, bh, 22)
        xs, ys = bukit(dh, bw * 0.8, bh * 0.86, bw * 0.4, bh)
        arsir_bukit(xs, ys, bh, 22)
    return {"hitam": hitam, "merah": merah, "kunyit": kunyit, "biru": biru}


def cukil_image(p, i):
    rng = np.random.default_rng(9200 + i)
    img = kertas_cukil(W, H, 9200 + i).convert("RGB")
    base = np.asarray(img).astype(np.float32)
    TINTA = {"hitam": (32, 30, 32), "merah": (190, 56, 42), "kunyit": (214, 158, 52), "biru": (36, 52, 92)}
    # judul
    jm = Image.new("L", (W, H), 0)
    jd = ImageDraw.Draw(jm)
    judul = bersih(p["judul"]).upper()
    fj = charter(124, 5)
    while jd.textlength(judul, font=fj) > W - 200 and fj.size > 56:
        fj = charter(fj.size - 4, 5)
    lines = [judul] if jd.textlength(judul, font=fj) <= W - 200 else wrap(jd, judul, fj, W - 200)
    y = 150
    for ln in lines:
        jd.text((W / 2, y), ln, font=fj, fill=255, anchor="ma")
        y += fj.size * 1.02
    # ilustrasi
    bw, bh, S = 820, 600, 2
    bx, by = (W - bw) // 2, int(y + 40)
    masks = ikon_cukil(p["ikon"], bw, bh, S, rng)
    lapisan = [("kunyit", (6, 4)), ("biru", (0, 0)), ("merah", (-4, 3)), ("hitam", (0, 0))]
    for nama, (ox, oy) in lapisan:
        m = masks[nama].resize((bw, bh), Image.LANCZOS)
        full = Image.new("L", (W, H), 0)
        full.paste(m, (bx + ox, by + oy))
        a = tinta(full, 9210 + i)[..., None]
        base = base * (1 - a) + np.array(TINTA[nama], np.float32) * a
    a = tinta(jm, 9220 + i, 0.3)[..., None]
    base = base * (1 - a) + np.array(TINTA["merah"], np.float32) * a
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle((44, 44, W - 44, H - 44), outline=TINTA["hitam"], width=4)
    d.rectangle((58, 58, W - 58, H - 58), outline=TINTA["hitam"], width=2)
    y = by + bh + 44
    f, vl, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), W - 240, H - 150 - y - 60, 38, 24, 1.36)
    y += max(0, (H - 140 - y - (len(vl) * size * 1.36 + 50)) / 2)
    for ln in vl:
        d.text((W / 2, y), ln, font=f, fill=(44, 40, 38), anchor="ma")
        y += size * 1.36
    d.text((W / 2, y + 14), bersih(p["ref"]).upper(), font=charter(30, 5), fill=TINTA["merah"], anchor="ma")
    d.text((W / 2, H - 100), "@" + HANDLE, font=charter(24, 0), fill=(110, 104, 98), anchor="ma")
    return img


# ---------- TIMBUL: angka timbul di kertas (hitung mundur) ----------

def timbul_image(p, i):
    rng = np.random.default_rng(9300 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array([245, 243, 238])
    base *= (0.975 + 0.035 * render.fbm2d(H, W, rng, ((4, 1.0), (60, 0.5), (300, 0.4))))[..., None]
    teks = str(p["angka"])
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    f = ft("Futura.ttc", 760, 2)
    while (md.textbbox((0, 0), teks, font=f)[2] - md.textbbox((0, 0), teks, font=f)[0]) > W - 220:
        f = ft("Futura.ttc", f.size - 20, 2)
    md.text((W / 2, 400), teks, font=f, fill=255, anchor="mm")
    hm = np.asarray(m.filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    hm2 = np.asarray(m.filter(ImageFilter.GaussianBlur(4))).astype(np.float32) / 255
    gy, gx = np.gradient(hm * 0.7 + hm2 * 0.3)
    sinar = (gx + gy) * 9.0
    bayang = np.asarray(m.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255
    bayang = np.roll(np.roll(bayang, 14, axis=0), 10, axis=1)
    rel = np.clip(1 + sinar, 0.55, 1.35)[..., None]
    out = base * rel * (1 - 0.1 * np.clip(bayang - hm, 0, 1))[..., None]
    img = grain(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 0.025).convert("RGBA")
    d = ImageDraw.Draw(img)
    label = "   ".join(" ".join(w) for w in bersih(p["label"]).upper().split())
    d.text((W / 2, 770), label, font=hn(40, 1), fill=(70, 66, 62), anchor="ma")
    d.text((W / 2, 832), bersih(p["sublabel"]), font=georgia(48, True), fill=(176, 130, 60), anchor="ma")
    d.text((W / 2, 912), bersih(p["tanggal"]).upper(), font=hn(24, 10), fill=(150, 144, 136), anchor="ma")
    y = 956
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 220):
        d.text((W / 2, y), ln, font=georgia(34), fill=(60, 56, 52), anchor="ma")
        y += 46
    ayat_tengah(img, p, y + 10, H - 64, (80, 74, 68), (176, 130, 60), start=34)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=hn(22, 10), fill=(160, 154, 146), anchor="ma")
    return img


# ---------- CORET: foto dengan coretan spidol putih ----------

def coret_image(p, i):
    rng = np.random.default_rng(9400 + i)
    img = grain(foto_redup(p["foto"], W, H, 9400 + i, gelap=0.5), 0.05).convert("RGBA")
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(int(H * 0.55), H):
        sd.line((0, y, W, y), fill=(0, 0, 0, int(170 * max(0.0, (y - H * 0.55) / (H * 0.45)) ** 1.3)))
    img.alpha_composite(shade)
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    putih = (255, 255, 255, 240)
    fm = spidol(86 * S)
    lines = wrap(ld, bersih(p["teks"]), fm, (W - 300) * S)
    cy = 430
    tinggi = len(lines) * 96
    y = cy - tinggi / 2
    for ln in lines:
        ld.text((W / 2 * S, y * S), ln, font=fm, fill=putih, anchor="ma")
        y += 96
    lebar = max(ld.textlength(ln, font=fm) for ln in lines) / S
    rx, ry = lebar / 2 + 70, tinggi / 2 + 60
    putaran = [(W / 2 + rx * math.cos(t) * (1 + 0.03 * math.sin(3 * t)), cy + 40 + ry * math.sin(t)) for t in np.linspace(-0.4, 2 * math.pi + 0.25, 70)]
    goresan(ld, [(x * S, y_ * S) for x, y_ in putaran], 6 * S, putih, rng, 1.2 * S)
    goresan(ld, [(x * S, (y + 10 + 6 * math.sin(x / 24)) * S) for x in np.linspace(W / 2 - lebar / 2, W / 2 + lebar / 2 - 30, 30)], 5 * S, putih, rng, S)
    fn = spidol(44 * S)
    tempat = [((96, 120), "la", ((300, 150), (W / 2 - rx * 0.6, cy - ry - 4))),
              ((W - 90, 214), "ra", ((W - 170, 290), (W / 2 + rx * 0.85, cy - ry * 0.35))),
              ((110, 720), "la", ((150, 640), (W / 2 - rx * 0.7, cy + ry * 0.95)))]
    for (pos, anchor, (ctrl, end)), note in zip(tempat, p["catatan"]):
        ld.text((pos[0] * S, pos[1] * S), bersih(note), font=fn, fill=putih, anchor=anchor)
        bw_ = ld.textlength(bersih(note), font=fn) / S
        sx = pos[0] + (bw_ / 2 if anchor == "la" else -bw_ / 2)
        panah(ld, (sx * S, (pos[1] + 62) * S), (ctrl[0] * S, (ctrl[1] + 30) * S), (end[0] * S, end[1] * S), 4 * S, putih, rng)
    for x, y_, r in ((W - 150, 640, 22), (180, 300, 14), (W - 260, 110, 16)):
        for a in range(4):
            ang = a * math.pi / 4
            goresan(ld, [((x - math.cos(ang) * r) * S, (y_ - math.sin(ang) * r) * S), ((x + math.cos(ang) * r) * S, (y_ + math.sin(ang) * r) * S)], 4 * S, putih, rng, 0.6)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    ayat_tengah(img, p, 840, H - 70, (255, 255, 255), (255, 222, 150), start=40)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=hn(22, 10), fill=(220, 220, 220), anchor="ma")
    return img


# ---------- PANDUAN: seri panduan lapangan ----------

def panduan_image(p, i):
    pal = [((72, 120, 236), (250, 176, 196)), ((96, 150, 240), (255, 196, 150)), ((120, 110, 230), (246, 170, 210))][i % 3]
    img = langit(W, H, 9500 + i, *pal).convert("RGBA")
    d = ImageDraw.Draw(img)
    fs = avenir(96, 8)
    seri = bersih(p["seri"]).upper()
    while d.textlength(seri, font=fs) > W - 140:
        fs = avenir(fs.size - 4, 8)
    d.text((W / 2, 90), seri, font=fs, fill="white", anchor="ma")
    fu, fi = avenir(72, 8), avenir(72, 9)
    a, b = "untuk ", bersih(p["untuk"]) + ":"
    while d.textlength(a, font=fu) + d.textlength(b, font=fi) > W - 140:
        fu, fi = avenir(fu.size - 4, 8), avenir(fi.size - 4, 9)
    x = W / 2 - (d.textlength(a, font=fu) + d.textlength(b, font=fi)) / 2
    yb = 90 + fs.size * 1.12
    d.text((x, yb), a, font=fu, fill="white")
    d.text((x + d.textlength(a, font=fu), yb), b, font=fi, fill="white")
    # kartu bertisolasi
    cw = 720
    ft_, tl, ts = pas(d, bersih(p["topik"]), lambda s: avenir(s, 0), cw - 100, 200, 58, 40, 1.15)
    ch = int(len(tl) * ts * 1.15 + 110)
    card = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    cd = ImageDraw.Draw(card)
    yy = (ch - len(tl) * ts * 1.15) / 2
    for ln in tl:
        cd.text((cw / 2, yy), ln, font=ft_, fill=(36, 40, 80), anchor="ma")
        yy += ts * 1.15
    card = card.rotate(-2.5, expand=True, resample=Image.BICUBIC)
    cy0 = int(yb + fu.size * 1.5)
    bayangan(img, card, ((W - card.width) // 2, cy0), blur=14, geser=(0, 10), kuat=0.22)
    tape = Image.new("RGBA", (190, 54), (255, 214, 70, 230)).rotate(4, expand=True, resample=Image.BICUBIC)
    comp(img, tape, (W / 2 - 95, cy0 - 26))
    d = ImageDraw.Draw(img)
    y = cy0 + card.height + 44
    fl = avenir(36, 2)
    for k, st in enumerate(p["langkah"]):
        lines = wrap(d, bersih(st), fl, W - 300)
        h_ = len(lines) * 46 + 36
        d.rounded_rectangle((90, y, W - 90, y + h_), radius=h_ // 2 if len(lines) == 1 else 34, fill=(255, 255, 255, 255))
        d.ellipse((112, y + h_ / 2 - 28, 168, y + h_ / 2 + 28), fill=pal[0])
        d.text((140, y + h_ / 2), str(k + 1), font=avenir(32, 0), fill="white", anchor="mm")
        for n, ln in enumerate(lines):
            d.text((194, y + 18 + n * 46), ln, font=fl, fill=(40, 44, 80))
        y += h_ + 16
    ayat_tengah(img, p, y + 10, H - 66, (255, 255, 255), (36, 40, 90), start=38)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=avenir(22, 5), fill=(255, 255, 255), anchor="ma")
    return img


# ---------- TUMPUK: puisi punggung buku ----------

FONT_BUKU = [lambda s: ft("Futura.ttc", s, 2), lambda s: ft("Didot.ttc", s, 2), lambda s: ft("Georgia Bold.ttf", s),
             lambda s: ft("GillSans.ttc", s, 6), lambda s: ft("AmericanTypewriter.ttc", s, 2), lambda s: avenir(s, 8),
             lambda s: ft("Baskerville.ttc", s, 1)]
WARNA_BUKU = [((222, 98, 44), (250, 238, 220)), ((244, 236, 218), (40, 44, 60)), ((32, 52, 92), (240, 214, 150)),
              ((92, 128, 92), (248, 242, 226)), ((150, 36, 48), (246, 228, 200)), ((232, 184, 60), (40, 34, 30)),
              ((70, 150, 170), (252, 248, 236))]


def buku(w, h, judul, warna, f_fn, rng):
    b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    isi, teks = warna
    arr = np.zeros((h, w, 3), np.float32) + np.array(isi, np.float32)
    yy = np.linspace(-1, 1, h)[:, None]
    arr *= (1.06 - 0.22 * yy ** 2)[..., None]
    arr *= (0.97 + 0.05 * rng.random((h, w)))[..., None]
    sp = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=8, fill=255)
    b.paste(sp, (0, 0), mask)
    d = ImageDraw.Draw(b)
    for x in (34, 44, w - 44, w - 34):
        d.line((x, 6, x, h - 6), fill=teks + (150,), width=2)
    f = f_fn(int(h * 0.42))
    while d.textlength(judul, font=f) > w - 210 and f.size > 18:
        f = f_fn(f.size - 2)
    d.text((w / 2 - 20, h / 2), judul, font=f, fill=teks + (255,), anchor="mm")
    d.ellipse((w - 108, h / 2 - 16, w - 76, h / 2 + 16), outline=teks + (255,), width=3)
    d.ellipse((w - 97, h / 2 - 5, w - 87, h / 2 + 5), fill=teks + (255,))
    return b


def tumpuk_image(p, i):
    rng = np.random.default_rng(9600 + i)
    meja = 950
    dinding = gradasi(W, meja, (238, 230, 216), (222, 208, 190))
    kayu = np.zeros((H - meja, W, 3), np.float32) + np.array([138, 92, 60])
    kayu *= (0.85 + 0.2 * render.fbm2d(H - meja, W, rng, ((1, 1.0), (12, 0.6), (90, 0.3))))[..., None]
    for k in range(0, H - meja, 9):
        kayu[k:k + 2] *= 0.94
    img = Image.new("RGB", (W, H))
    img.paste(dinding, (0, 0))
    img.paste(Image.fromarray(np.clip(kayu, 0, 255).astype(np.uint8)), (0, meja))
    img = grain(img, 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle((0, meja, W, meja + 6), fill=(110, 72, 46))
    d.text((W / 2, 92), "puisi punggung buku", font=georgia(46, True), fill=(110, 90, 70), anchor="ma")
    d.text((W / 2, 158), "D I B A C A   D A R I   A T A S   K E   B A W A H", font=hn(22, 10), fill=(150, 130, 110), anchor="ma")
    judul = [bersih(t) for t in p["buku"]]
    hs = [int(rng.uniform(96, 124)) for _ in judul]
    y = meja - sum(hs) + 4
    urut = rng.permutation(len(WARNA_BUKU))
    for k, (t, h_) in enumerate(zip(judul, hs)):
        w_ = int(rng.uniform(660, 880))
        b = buku(w_, h_, t, WARNA_BUKU[urut[k % len(urut)]], FONT_BUKU[(k + i * 2) % len(FONT_BUKU)], rng)
        b = b.rotate(rng.uniform(-1.2, 1.2), expand=True, resample=Image.BICUBIC)
        bayangan(img, b, (W / 2 - b.width / 2 + rng.uniform(-36, 36), y - (b.height - h_) / 2), blur=8, geser=(0, 6), kuat=0.35)
        y += h_
    ayat_tengah(img, p, meja + 30, H - 60, (250, 240, 226), (250, 210, 140), start=38)
    ImageDraw.Draw(img).text((W / 2, H - 42), "@" + HANDLE, font=hn(22, 10), fill=(230, 210, 190), anchor="ma")
    return img


# ---------- PAPAN: papan inspirasi bento ----------

PASTEL = [(214, 226, 200), (250, 230, 170), (246, 206, 200), (200, 220, 240), (232, 176, 140)]


def papan_image(p, i):
    img = grain(Image.new("RGB", (W, H), (244, 241, 236)), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((54, 58), "PAPAN INSPIRASI", font=hn(22, 1), fill=(160, 140, 120))
    fj = ft("Georgia Bold.ttf", 56)
    while d.textlength(bersih(p["judul"]), font=fj) > W - 110:
        fj = ft("Georgia Bold.ttf", fj.size - 2)
    d.text((54, 92), bersih(p["judul"]), font=fj, fill=(40, 36, 32))
    g = 18
    kotak = [bersih(k) for k in p["kotak"]]
    foto = p["foto"]
    L, R, T = 50, W - 50, 196
    tiles = {"f1": (L, T, 560, T + 380), "k1": (560 + g, T, R, T + 181), "k2": (560 + g, T + 199, R, T + 380),
             "ayat": (L, T + 398, 700, T + 838), "f2": (700 + g, T + 398, R, T + 838),
             "k3": (L, T + 856, 360, H - 50), "k4": (360 + g, T + 856, 700, H - 50), "k5": (700 + g, T + 856, R, H - 50)}
    for key, sc in (("f1", foto[0]), ("f2", foto[1])):
        x0, y0, x1, y1 = tiles[key]
        ubin(img, tiles[key], cover(foto_warna(sc, 800, 800, seed=9700 + i * 2 + (key == "f2")), int(x1 - x0), int(y1 - y0)))
    rng = np.random.default_rng(9700 + i)
    warna = [PASTEL[k] for k in rng.permutation(5)]
    for k, key in enumerate(("k1", "k2", "k3", "k4", "k5")):
        x0, y0, x1, y1 = tiles[key]
        ubin(img, tiles[key], warna[k])
        d = ImageDraw.Draw(img)
        d.text((x0 + 26, y0 + 22), f"0{k + 1}", font=hn(22, 1), fill=(90, 80, 70))
        f = avenir(52, 8)
        lines = wrap(d, kotak[k], f, x1 - x0 - 52)
        while (len(lines) > 2 or len(lines) * f.size * 1.1 > y1 - y0 - 80) and f.size > 26:
            f = avenir(f.size - 2, 8)
            lines = wrap(d, kotak[k], f, x1 - x0 - 52)
        yy = y1 - 26 - len(lines) * f.size * 1.08
        for ln in lines:
            d.text((x0 + 26, yy), ln, font=f, fill=(44, 38, 34))
            yy += f.size * 1.08
    x0, y0, x1, y1 = tiles["ayat"]
    ubin(img, tiles["ayat"], (255, 252, 246))
    d = ImageDraw.Draw(img)
    d.text((x0 + 36, y0 + 28), "“", font=ft("Georgia Bold.ttf", 110), fill=(232, 176, 140))
    f, vl, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), x1 - x0 - 80, y1 - y0 - 200, 38, 24, 1.34)
    yy = y0 + 130
    for ln in vl:
        d.text((x0 + 40, yy), ln, font=f, fill=(56, 48, 42))
        yy += size * 1.34
    d.text((x0 + 40, yy + 12), p["ref"], font=hn(28, 1), fill=(196, 112, 80))
    d.text((x1 - 26, y1 - 24), "@" + HANDLE, font=hn(20, 10), fill=(170, 160, 150), anchor="rs")
    return img


# ---------- NAPAS (Reels): latihan napas ----------

def napas_reel(p, idx, mod=MOD, seconds=24):
    rel = f"reels/{mod}/napas{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    pal = [((44, 66, 128), (156, 128, 196)), ((32, 86, 100), (176, 152, 196))][idx % 2]
    rng = np.random.default_rng(9750 + idx)
    bg = gradasi(RW, RH, *pal).convert("RGBA")
    awan = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    ad_ = ImageDraw.Draw(awan)
    for _ in range(14):
        x, y, r = rng.uniform(0, RW), rng.uniform(0, RH), rng.uniform(160, 380)
        ad_.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 16))
    bg.alpha_composite(awan.filter(ImageFilter.GaussianBlur(80)))
    bg = grain(bg.convert("RGB"), 0.03).convert("RGBA")
    R = 470
    glow = Image.new("RGBA", (R * 2 + 200, R * 2 + 200), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    c = R + 100
    gd.ellipse((c - R, c - R, c + R, c + R), fill=(255, 255, 255, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((c - R * 0.86, c - R * 0.86, c + R * 0.86, c + R * 0.86), fill=(255, 255, 255, 60))
    for k, rr in enumerate((0.93, 1.0, 1.08)):
        gd.ellipse((c - R * rr, c - R * rr, c + R * rr, c + R * rr), outline=(255, 255, 255, 140 - 40 * k), width=3)
    cache = {}

    def teks(a, b, n=None):
        key = (a, b, n)
        if key not in cache:
            t = Image.new("RGBA", (RW, 360), (0, 0, 0, 0))
            td = ImageDraw.Draw(t)
            td.text((RW / 2, 40), a, font=bulat(76, "Bold"), fill=(255, 255, 255, 255), anchor="ma")
            td.text((RW / 2, 150), bersih(b), font=georgia(44, True), fill=(240, 236, 255, 235), anchor="ma")
            if n is not None:
                td.text((RW / 2, 240), str(n), font=bulat(56, "Semibold"), fill=(255, 255, 255, 170), anchor="ma")
            cache[key] = t
        return cache[key]
    judul = Image.new("RGBA", (RW, 200), (0, 0, 0, 0))
    jd = ImageDraw.Draw(judul)
    for k, ln in enumerate(wrap(jd, bersih(p["judul"]), georgia(56, True), RW - 200)[:2]):
        jd.text((RW / 2, k * 70), ln, font=georgia(56, True), fill=(255, 255, 255, 240), anchor="ma")
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 520, 46, 28, 1.38)
    ayat = Image.new("RGBA", (RW, 760), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(255, 255, 255, 255), anchor="ma")
        y += vs * 1.38
    ad.text((RW / 2, y + 20), p["ref"], font=bulat(38, "Bold"), fill=(255, 226, 160, 255), anchor="ma")
    tarik, hembus = bersih(p["tarik"]), bersih(p["hembus"])
    fase = [(1.0, 5.0, "in"), (5.0, 6.0, "tahan"), (6.0, 10.0, "out"), (10.0, 14.0, "in"), (14.0, 15.0, "tahan"), (15.0, 19.0, "out")]
    cx, cy = RW / 2, 900
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        s, txt, alpha = 0.62, teks("Tarik napas", tarik), 1.0
        for t0, t1, kind in fase:
            if t0 <= t < t1:
                u = (t - t0) / (t1 - t0)
                hit = int(math.ceil((t1 - t)))
                if kind == "in":
                    s, txt = 0.45 + 0.55 * ease(u), teks("Tarik napas", tarik, hit)
                elif kind == "out":
                    s, txt = 1.0 - 0.55 * ease(u), teks("Hembuskan", hembus, hit)
                else:
                    s, txt = 1.0, teks("Tahan", "sebentar saja")
        if t >= 19:
            u = ease((t - 19) / 1.2)
            s, alpha = 0.45 - 0.15 * u, 1 - 0.6 * u
            txt = fade(txt, 1 - u) if t < 20.2 else None
        gs = glow.resize((int(glow.width * s), int(glow.height * s)), Image.BILINEAR)
        frame.alpha_composite(fade(gs, alpha), (int(cx - gs.width / 2), int(cy - gs.height / 2)))
        frame.alpha_composite(judul, (0, 230))
        if txt is not None:
            frame.alpha_composite(txt, (0, int(cy - 130)))
        if t >= 19.6:
            frame.alpha_composite(fade(ayat, ease((t - 19.6) / 1.0)), (0, 700))
        ImageDraw.Draw(frame).text((RW / 2, RH - 150), "@" + HANDLE, font=bulat(30, "Semibold"), fill=(255, 255, 255, 180), anchor="ma")
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- KEMBANGAPI (Reels): kembang api yang membentuk kata ----------

def kembangapi_reel(p, idx, mod=MOD, seconds=13):
    rel = f"reels/{mod}/kembangapi{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(9800 + idx)
    bg = gradasi(RW, RH, (8, 10, 32), (34, 20, 58)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    for _ in range(420):
        x, y, r = rng.uniform(0, RW), rng.uniform(0, RH * 0.8), rng.uniform(0.8, 2.4)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(rng.uniform(40, 180))))
    x = 0
    while x < RW:  # siluet kota
        bw_, bh_ = rng.uniform(60, 150), rng.uniform(120, 420)
        d.rectangle((x, RH - bh_, x + bw_, RH), fill=(10, 10, 22, 255))
        for wy in range(int(RH - bh_ + 20), RH - 20, 34):
            for wx in range(int(x + 12), int(x + bw_ - 12), 26):
                if rng.random() < 0.3:
                    d.rectangle((wx, wy, wx + 10, wy + 14), fill=(250, 210, 120, 160))
        x += bw_ + rng.uniform(4, 20)
    bg = grain(bg.convert("RGB"), 0.03).convert("RGBA")
    # titik huruf
    lines = [ln.strip() for ln in bersih(p["teks"]).upper().split("\n") if ln.strip()]
    m = Image.new("L", (RW, 900), 0)
    md = ImageDraw.Draw(m)
    fs = 330
    f = hn(fs, 9)
    while max(md.textlength(ln, font=f) for ln in lines) > RW - 140 or len(lines) * fs * 1.0 > 860:
        fs -= 10
        f = hn(fs, 9)
    y = 450 - len(lines) * fs * 1.0 / 2
    for ln in lines:
        md.text((RW / 2, y), ln, font=f, fill=255, anchor="ma")
        y += fs * 1.0
    ys, xs = np.nonzero(np.asarray(m)[::6, ::6] > 128)
    tgt = np.stack([xs * 6, ys * 6 + 160], 1).astype(np.float32)
    tgt = tgt[rng.permutation(len(tgt))][:2400]
    N = len(tgt)
    pusat = np.array([RW / 2, 560.0])
    tunda = rng.uniform(0, 0.25, N)
    kerlip = rng.uniform(0, 2 * math.pi, N)
    warna_bg = [(255, 120, 160), (120, 200, 255), (190, 150, 255), (255, 206, 90), (140, 240, 190)]
    ledak = [(0.7, 0.25, 0.3), (1.6, 0.75, 0.22), (2.5, 0.4, 0.18), (3.0, 0.8, 0.35), (6.8, 0.2, 0.2), (8.2, 0.82, 0.24), (9.6, 0.5, 0.15), (11.0, 0.25, 0.3)]
    ledak = [(t0, x * RW, y * RH + 120, warna_bg[k % 5], rng.uniform(220, 320), rng.uniform(0, 1, 80)) for k, (t0, x, y) in enumerate(ledak)]
    kecil = Image.new("RGBA", (RW, 200), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kecil)
    for k, ln in enumerate(wrap(kd, bersih(p["kecil"]), georgia(46, True), RW - 200)[:2]):
        kd.text((RW / 2, k * 60), ln, font=georgia(46, True), fill=(255, 244, 226, 255), anchor="ma")
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fv, vl, vsz = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 240, 400, 38, 24, 1.36)
    ayat = Image.new("RGBA", (RW, int(len(vl) * vsz * 1.36 + 170)), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    ad.rounded_rectangle((70, 0, RW - 70, ayat.height), radius=30, fill=(10, 10, 30, 170))
    yy = 34
    for ln in vl:
        ad.text((RW / 2, yy), ln, font=fv, fill=(246, 240, 255), anchor="ma")
        yy += vsz * 1.36
    ad.text((RW / 2, yy + 10), p["ref"], font=hn(32, 1), fill=(255, 206, 90), anchor="ma")
    ad.text((RW / 2, yy + 60), "@" + HANDLE, font=hn(24, 10), fill=(170, 166, 200), anchor="ma")
    TB = 4.2  # saat ledakan besar di tengah

    def gambar(t, sampul=False):
        frame = bg.copy()
        lay = Image.new("RGBA", (RW // 2, RH // 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for t0, x0, y0, col, r, arah in ledak:
            if sampul:
                dt_ = 0.9 if t0 in (1.6, 3.0) else -1
            else:
                dt_ = t - t0
            if -0.8 < dt_ < 0:  # roket naik
                u = 1 + dt_ / 0.8
                ry = RH - (RH - y0) * ease(u)
                for s in range(6):
                    ld.ellipse(((x0 - 3) / 2, (ry + s * 14 - 3) / 2, (x0 + 3) / 2, (ry + s * 14 + 3) / 2), fill=(255, 230, 180, 220 - s * 35))
            elif 0 <= dt_ < 2.4:
                a = max(0.0, 1 - dt_ / 2.4) ** 0.8
                for k in range(80):
                    ang = 2 * math.pi * k / 80 + arah[k] * 0.08
                    for j, lag in enumerate((0.0, 0.07, 0.14)):  # ekor
                        tt = max(0.0, dt_ - lag)
                        rr = r * (1 - math.exp(-3.0 * tt)) * (0.75 + 0.25 * arah[k])
                        px, py = x0 + math.cos(ang) * rr, y0 + math.sin(ang) * rr + 70 * tt * tt
                        pr = 4.2 - j * 1.2
                        ld.ellipse(((px - pr) / 2, (py - pr) / 2, (px + pr) / 2, (py + pr) / 2), fill=col + (int(255 * a * (1 - j * 0.3)),))
        if sampul or t >= TB - 0.8:
            if not sampul and t < TB:
                u = 1 + (t - TB) / 0.8
                ry = RH - (RH - pusat[1]) * ease(u)
                for s in range(8):
                    ld.ellipse(((RW / 2 - 4) / 2, (ry + s * 16 - 4) / 2, (RW / 2 + 4) / 2, (ry + s * 16 + 4) / 2), fill=(255, 240, 200, 230 - s * 28))
            else:
                u = 1.0 if sampul else np.clip((t - TB - tunda) / 1.1, 0, 1)
                e = 1 - (1 - u) ** 3
                pos = pusat + (tgt - pusat) * e[..., None] if not sampul else tgt
                tw = 0.75 + 0.25 * np.sin(kerlip + t * 7)
                for k in range(N):
                    px, py = pos[k]
                    pr = 2.4
                    c = (255, int(200 + 40 * tw[k]), int(110 + 60 * tw[k]))
                    ld.ellipse(((px - pr) / 2, (py - pr) / 2, (px + pr) / 2, (py + pr) / 2), fill=c + (255,))
        big = lay.resize((RW, RH), Image.BILINEAR)
        frame.alpha_composite(big.filter(ImageFilter.GaussianBlur(9)))
        frame.alpha_composite(big.filter(ImageFilter.GaussianBlur(3)))
        frame.alpha_composite(big)
        if sampul or t >= 6.0:
            frame.alpha_composite(kecil if sampul else fade(kecil, ease((t - 6.0) / 0.8)), (0, 1110))
        if not sampul and t >= 7.0:
            frame.alpha_composite(fade(ayat, ease((t - 7.0) / 0.8)), (0, RH - 240 - ayat.height))
        return frame

    sampul = gambar(0, sampul=True)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = sampul if t < 0.5 else gambar(t - 0.5)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def kop_kalender(p):
    bulan = p["tanggal"].split()[-1]
    return f"{bulan.upper()} {2027 if bulan == 'Januari' else 2026}"


SIMPLE = {
    # baru
    "KATAHARI": katahari_image, "GRAFIK": grafik_image, "LENGKAPI": lengkapi_image, "ULASAN": ulasan_image,
    "CUKIL": cukil_image, "TIMBUL": timbul_image, "CORET": coret_image, "PANDUAN": panduan_image,
    "TUMPUK": tumpuk_image, "PAPAN": papan_image,
    # lama
    "CATATAN": gaya_w7.catatan_image, "REKAP": gaya_w11.rekap_image, "TOPLES": gaya_w10.toples_image,
    "BINGO": gaya_w12.bingo_image, "SIGNPOST": gaya_w11.signpost_image, "SERTIFIKAT": gaya_w9.sertifikat_image,
    "JAM": gaya_w9.jam_image, "RESEP": gaya_w9.resep_image, "KOMPAS": gaya_w10.kompas_image,
    # mix
    "ALKITABCAHAYA": lambda p, i: cahaya(gaya_w6.alkitab_image(p, i), 9900 + i),
    "KETIKCAHAYA": lambda p, i: cahaya(gaya_w7.ketik_image(p, i), 9910 + i),
    "KAMUSCAHAYA": lambda p, i: cahaya(gaya_w7.kamus_image(p, i), 9920 + i),
    "STICKYLANGIT": lambda p, i: gaya_w8.sticky_image(p, i, latar=langit(W, H, 9930 + i)),
    "POLAROIDLANGIT": lambda p, i: gaya_w7.polaroid_image(p, i, latar=langit(W, H, 9940 + i, (110, 160, 236), (252, 210, 180))),
    "BALONKEMBANG": lambda p, i: gaya_w12.balon_image(p, i, latar=kembang_latar(W, H, 9950 + i, zona=(0.03, 0.3))),
    "FLIPTAHUN": lambda p, i: gaya_w11.flipclock_image(p, i, latar=kembang_latar(W, H, 9960 + i, n=4, zona=(0.13, 0.36))),
    "PHOTOBOOTHKEMBANG": lambda p, i: gaya_w11.photobooth_image(p, i, latar=kembang_latar(W, H, 9970 + i)),
    "TIKETKEMBANG": lambda p, i: gaya_w7.tiket_image(p, i, latar=kembang_latar(W, H, 9980 + i)),
    "KALENDERTAHUN": lambda p, i: gaya_w7.kalender_image(dict(p, _kop=kop_kalender(p)), i, hias=False),
    "UNDANGANTAHUN": lambda p, i: gaya_w9.undangan_image(p, i, warna=[(28, 36, 72), (64, 30, 60)][i % 2]),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {}
REELS = {"NAPAS": (napas_reel, "napas"), "KEMBANGAPI": (kembangapi_reel, "kembangapi"),
         "JAMPASIR": (gaya_w10.jampasir_reel, "jampasir"), "PROGRESS": (gaya_w9.progress_reel, "progress"),
         "FLIP": (gaya_w8.flip_reel, "flip"),
         "KONFETIMALAM": (lambda p, i, mod: gaya_w12.konfeti_reel(p, i, mod, malam=True), "konfeti")}


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
