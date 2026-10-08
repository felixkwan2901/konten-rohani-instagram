"""Akun Tenang - minggu 12 (konten/tenang_w12.py), Adven III "Sukacita": 36 gaya diacak tiap hari + komik Eli.
BARU : LAMPU (Reels lampu tumbler berkelip), KONFETI (Reels ledakan konfeti), BALON (balon angka emas, hitung mundur),
       BINGO (kartu bingo Adven), EMAIL (email terbuka), VENN (diagram Venn), STAMP (perangko besar), WATERCOLOR (cat air),
       KARTUNATAL (kartu Natal terbuka), CRAYON (gambar krayon anak), KOPI (gelas kopi), PERJALANAN (peta kuno perjalanan).
LAMA : PROGRESS, GOSOK, KALENDER, STRUK, CATATAN, KETIK, KARTUPOS, PETA, KODE, MUSEUM, SERTIFIKAT, JAM.
MIX  : SEARCHGELAP, KRANSTERANG, KALADVENMERAH, KORANSEPIA, TIKETKERETA, STICKYPASTEL, KAMUSGELAP, UNDANGANHIJAU,
       KASETPUTIH, LILINJENDELA, TELEGRAMNATAL, MAJALAHNATAL.

  python3 gaya_w12.py [reels]
"""
import datetime as dt
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
import render
from gaya_w6 import cover, foto_warna, georgia, hn
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tangan, tanpa_kutip, vintage
from gaya_w8 import kayu
from gaya_w9 import EMAS, ayat_bawah, kertas_kado
from render import OUT, W, H, grain, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w12"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2026, 12, 13)


# ================= BARU =================

# ---------- BALON: balon angka emas ----------

def balon_angka(teks, size):
    probe = ImageDraw.Draw(Image.new("L", (10, 10)))
    f = hn(size, 1)
    jarak = size * 0.1  # spasi antar-digit supaya balon tidak menempel
    tw = int(sum(probe.textlength(c, font=f) for c in teks) + jarak * (len(teks) - 1)) + 80
    th = int(size * 1.1) + 80
    m = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(m)
    x = 40
    for c in teks:
        md.text((x, 40), c, font=f, fill=255, stroke_width=int(size * 0.02), stroke_fill=255)
        x += probe.textlength(c, font=f) + jarak
    m = m.filter(ImageFilter.GaussianBlur(2))
    a = np.asarray(m).astype(np.float32) / 255
    dalam = np.asarray(m.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255
    yy = np.linspace(0, 1, th)[:, None]
    atas, bawah = np.array([255, 232, 150], np.float32), np.array([196, 132, 40], np.float32)
    rgb = atas * (1 - yy[..., None]) + bawah * yy[..., None]
    rgb = rgb * (0.78 + 0.3 * dalam[..., None])
    kilau = np.clip(1 - np.abs(yy - 0.3) / 0.08, 0, 1) * dalam ** 2  # satu garis kilau tipis mendatar di atas
    rgb += 255 * kilau[..., None] * 0.35
    tepi = np.clip(a - dalam, 0, 1)
    rgb = rgb * (1 - 0.45 * tepi[..., None])
    out = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def balon_image(p, i):
    rng = np.random.default_rng(6100 + i)
    img = grain(gradasi(W, H, (252, 238, 232), (240, 214, 214)), 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(90):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(5, 12)
        c = [(240, 120, 140), (120, 180, 230), (250, 200, 90), (140, 210, 160)][int(rng.integers(4))]
        d.ellipse((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=c)
    teks = str(p["angka"])
    b = balon_angka(teks, 400)
    b = b.rotate(-4, expand=True, resample=Image.BICUBIC)
    bx = (W - b.width) // 2
    bayangan(img, b, (bx, 70), blur=18, geser=(8, 18), kuat=0.22)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 620), bersih(p.get("label", "HARI LAGI")), font=hn(54, 1), fill=(150, 60, 70), anchor="ma")
    d.text((W / 2, 690), bersih(p.get("sublabel", "menuju Natal")), font=georgia(48, True), fill=(190, 120, 60), anchor="ma")
    d.text((W / 2, 780), p["tanggal"].upper(), font=hn(26, 10), fill=(150, 120, 120), anchor="ma")
    y = 830
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 200):
        d.text((W / 2, y), ln, font=georgia(34), fill=(80, 50, 50), anchor="ma")
        y += 46
    ayat_bawah(img, p, y + 20, H - 60, (90, 60, 60), (190, 100, 60), start=30, stop=20)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(170, 130, 130), anchor="ma")
    return img


# ---------- BINGO ----------

def bingo_image(p, i):
    rng = np.random.default_rng(6200 + i)
    img = grain(gradasi(W, H, (30, 90, 70), (16, 50, 40)), 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    cw, chh = 940, 1080
    x0, y0 = (W - cw) // 2, 50
    card = Image.new("RGBA", (cw, chh), (252, 248, 238, 255))
    cd = ImageDraw.Draw(card)
    warna = [(214, 50, 60), (40, 130, 90), (230, 170, 50), (60, 110, 190), (190, 80, 150)]
    for k, h_ in enumerate("BINGO"):
        cx = 120 + k * 175
        cd.ellipse((cx - 62, 40, cx + 62, 164), fill=warna[k])
        cd.text((cx, 102), h_, font=hn(78, 9), fill=(255, 255, 255), anchor="mm")
    cd.text((cw / 2, 190), bersih(p["judul"]), font=georgia(38, True), fill=(60, 50, 40), anchor="ma")
    gs, gx, gy0 = 270, 20, 270
    tanda = set(rng.choice([0, 1, 2, 3, 5, 6, 7, 8], 2, replace=False).tolist())
    for k, teks in enumerate(p["kotak"]):
        r, c = divmod(k, 3)
        x, y = 45 + c * (gs + gx), gy0 + r * (gs + gx) - 30
        tengah = k == 4
        cd.rounded_rectangle((x, y, x + gs, y + gs - 40), radius=18, fill=(250, 228, 160) if tengah else (255, 255, 255),
                             outline=(200, 190, 170), width=3)
        if tengah:
            gaya_w10.bintang5(cd, x + gs / 2, y + 50, 30, (220, 160, 40))
        f, lines, size = pas(cd, bersih(teks), lambda s: hn(s, 10), gs - 40, gs - (130 if tengah else 80), 32, 18, 1.2)
        yy = y + (gs - 40) / 2 - len(lines) * size * 1.2 / 2 + (24 if tengah else 0)
        for ln in lines:
            cd.text((x + gs / 2, yy), ln, font=f, fill=(50, 44, 40), anchor="ma")
            yy += size * 1.2
        if k in tanda:
            st = Image.new("RGBA", (gs, gs), (0, 0, 0, 0))
            ImageDraw.Draw(st).ellipse((40, 30, gs - 40, gs - 70), fill=(214, 50, 60, 90))
            card.alpha_composite(st, (x, y))
            cd = ImageDraw.Draw(card)
    bayangan(img, card, (x0, y0), blur=20, geser=(0, 14), kuat=0.4)
    ayat_bawah(img, p, y0 + chh + 24, H - 50, (236, 240, 230), (250, 210, 120), start=28, stop=20)
    ImageDraw.Draw(img).text((W - 40, H - 16), "@" + HANDLE, font=hn(18, 10), fill=(170, 200, 180), anchor="rs")
    return img


# ---------- EMAIL ----------

def email_image(p, i):
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    biru = (26, 115, 232)
    d.rectangle((0, 0, W, 130), fill=(246, 248, 252))
    d.line((60, 66, 40, 46, 60, 26), fill=biru, width=6)
    d.text((80, 46), "Kotak Masuk", font=hn(34, 0), fill=biru, anchor="lm")
    for k, x in enumerate((W - 220, W - 140, W - 60)):
        d.rounded_rectangle((x - 22, 30, x + 22, 64), radius=6, outline=(110, 114, 120), width=3)
    y = 170
    f, lines, size = pas(d, bersih(p["subjek"]), lambda s: hn(s, 1), W - 140, 150, 52, 34, 1.18)
    for ln in lines:
        d.text((70, y), ln, font=f, fill=(32, 33, 36))
        y += size * 1.18
    d.rounded_rectangle((70, y + 14, 210, y + 52), radius=8, fill=(232, 240, 254))
    d.text((140, y + 33), "Kotak Masuk", font=hn(20, 1), fill=biru, anchor="mm")
    y += 90
    d.ellipse((70, y, 150, y + 80), fill=[(230, 120, 80), (90, 160, 120), (130, 110, 210)][i % 3])
    d.text((110, y + 40), bersih(p["dari"])[:1].upper(), font=hn(40, 1), fill="white", anchor="mm")
    d.text((175, y + 6), bersih(p["dari"]), font=hn(32, 1), fill=(32, 33, 36))
    d.text((175, y + 46), "kepada saya", font=hn(26, 0), fill=(110, 114, 120))
    d.text((W - 70, y + 10), p.get("_jam", "07.30"), font=hn(26, 0), fill=(110, 114, 120), anchor="ra")
    y += 130
    f, lines, size = pas(d, bersih(p["isi"]), lambda s: hn(s, 0), W - 140, 430, 38, 26, 1.42)
    for ln in lines:
        d.text((70, y), ln, font=f, fill=(50, 52, 56))
        y += size * 1.42
    y += 30
    f2, l2, s2 = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 200, H - 140 - y - 60, 34, 22, 1.38)
    d.rectangle((70, y, 78, y + len(l2) * s2 * 1.38 + 50), fill=(200, 210, 230))
    for ln in l2:
        d.text((100, y), ln, font=f2, fill=(80, 84, 90))
        y += s2 * 1.38
    d.text((100, y + 8), p["ref"], font=hn(28, 1), fill=biru)
    d.line((0, H - 120, W, H - 120), fill=(232, 234, 237), width=2)
    for k, lab in enumerate(("Balas", "Teruskan")):
        x = 70 + k * 300
        d.rounded_rectangle((x, H - 96, x + 260, H - 36), radius=30, outline=(200, 204, 210), width=3)
        d.text((x + 130, H - 66), lab, font=hn(28, 10), fill=(60, 64, 70), anchor="mm")
    d.text((W - 60, H - 66), "@" + HANDLE, font=hn(20, 10), fill=(170, 174, 180), anchor="rm")
    return img


# ---------- VENN ----------

def venn_image(p, i):
    img = grain(Image.new("RGB", (W, H), (250, 246, 238)), 0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    navy = (34, 40, 70)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: hn(s, 1), W - 140, 150, 56, 36, 1.15)
    y = 80
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=navy, anchor="ma")
        y += size * 1.15
    cy, r, dx = 620, 300, 190
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for cx, col in ((W / 2 - dx, (240, 120, 110, 120)), (W / 2 + dx, (100, 160, 230, 120))):
        c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(c).ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=col[:3] + (255,), width=5)
        lay.alpha_composite(c)
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    for teks, x, mw in ((p["kiri"], W / 2 - dx - 120, 200), (p["kanan"], W / 2 + dx + 120, 200)):
        f, ls, sz = pas(d, bersih(teks), lambda s: hn(s, 1), mw, 200, 40, 26, 1.2)
        yy = cy - len(ls) * sz * 1.2 / 2
        for ln in ls:
            d.text((x, yy), ln, font=f, fill=navy, anchor="ma")
            yy += sz * 1.2
    f, ls, sz = pas(d, bersih(p["tengah"]), lambda s: hn(s, 9), 180, 220, 44, 24, 1.1)
    yy = cy - len(ls) * sz * 1.1 / 2
    for ln in ls:
        d.text((W / 2, yy), ln.upper(), font=f, fill=(255, 255, 255), anchor="ma", stroke_width=3, stroke_fill=navy)
        yy += sz * 1.1
    ayat_bawah(img, p, 980, H - 60, navy, (200, 80, 70), start=32, stop=22)
    d.text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(150, 146, 136), anchor="ma")
    return img


# ---------- STAMP: perangko besar ----------

def stamp_image(p, i, latar=None):
    rng = np.random.default_rng(6300 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array([236, 226, 204])
    base *= (0.94 + 0.08 * render.fbm2d(H, W, rng, ((5, 1.0), (50, 0.4))))[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    if latar is not None:
        img = latar.copy().convert("RGBA")
    sw, sh = 700, 860
    st = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.rectangle((0, 0, sw, sh), fill=(252, 250, 244, 255))
    for x in range(0, sw + 1, 30):
        d.ellipse((x - 11, -11, x + 11, 11), fill=(0, 0, 0, 0))
        d.ellipse((x - 11, sh - 11, x + 11, sh + 11), fill=(0, 0, 0, 0))
    for y in range(0, sh + 1, 30):
        d.ellipse((-11, y - 11, 11, y + 11), fill=(0, 0, 0, 0))
        d.ellipse((sw - 11, y - 11, sw + 11, y + 11), fill=(0, 0, 0, 0))
    gb = vintage(cover(foto_warna(p["foto"], 800, 900, seed=6350 + i), sw - 80, sh - 220))
    st.paste(gb, (40, 40))
    d = ImageDraw.Draw(st)
    merah = (170, 40, 40)
    d.rectangle((40, 40, sw - 40, sh - 180), outline=(60, 50, 40, 255), width=3)
    d.text((64, 60), bersih(p["nilai"]), font=hn(54, 9), fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=merah)
    fj = ft("BigCaslon.ttf", 54)
    while d.textlength(bersih(p["judul"]).upper(), font=fj) > sw - 100:
        fj = ft("BigCaslon.ttf", fj.size - 2)
    d.text((sw / 2, sh - 150), bersih(p["judul"]).upper(), font=fj, fill=merah, anchor="ma")
    d.text((sw / 2, sh - 80), "POS SUKACITA · 2026", font=hn(26, 1), fill=(90, 80, 70), anchor="ma")
    st = st.rotate(-3, expand=True, resample=Image.BICUBIC)
    x0, y0 = (W - st.width) // 2, 50
    bayangan(img, st, (x0, y0), blur=14, geser=(6, 12), kuat=0.35)
    cap = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # cap pos bergelombang
    cd = ImageDraw.Draw(cap)
    cd.ellipse((x0 + st.width - 240, y0 + 30, x0 + st.width + 20, y0 + 290), outline=(50, 50, 60, 150), width=6)
    cd.text((x0 + st.width - 110, y0 + 160), p.get("_tgl_titik", "13.12.2026"), font=hn(26, 1), fill=(50, 50, 60, 170), anchor="mm")
    for k in range(5):
        yy = y0 + 90 + k * 36
        cd.line([(x0 + st.width - 560 + t * 12, yy + 8 * math.sin(t * 0.8)) for t in range(28)], fill=(50, 50, 60, 130), width=5)
    img.alpha_composite(cap)
    ayat_bawah(img, p, y0 + st.height + 40, H - 60, (60, 50, 40), merah, start=32, stop=22)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(140, 120, 100), anchor="ma")
    return img


# ---------- WATERCOLOR: cat air ----------

def noda_cat(w, h, col, rng):
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    cx, cy = w / 2, h / 2
    pts = []
    for k in range(40):
        a = k * 2 * math.pi / 40
        rr = 0.42 * min(w, h) * (0.75 + 0.35 * rng.random())
        pts.append((cx + rr * math.cos(a) * w / min(w, h), cy + rr * math.sin(a) * h / min(w, h)))
    d.polygon(pts, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(14))
    a = np.asarray(m).astype(np.float32) / 255
    tepi = np.clip(a - np.asarray(m.filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255, 0, 1) * 2.5
    alpha = np.clip(a * 0.55 + tepi * 0.6, 0, 0.9)
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = alpha * 255 * (0.85 + 0.3 * render.fbm2d(h, w, rng, ((6, 1.0), (30, 0.5))))
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")


def watercolor_image(p, i, malam=False):
    rng = np.random.default_rng(6400 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array([22, 28, 52] if malam else [252, 250, 246])
    base -= render.fbm2d(H, W, rng, ((60, 1.0), (300, 0.6)))[..., None] * 10
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    pal = [[(240, 150, 160), (250, 200, 140), (170, 200, 240)], [(150, 210, 190), (250, 210, 150), (200, 170, 230)],
           [(250, 170, 130), (240, 220, 140), (150, 190, 230)]][i % 3]
    if malam:
        pal = [(214, 170, 80), (60, 130, 140), (140, 70, 110)]
    for k, col in enumerate(pal):
        w_, h_ = int(rng.uniform(420, 620)), int(rng.uniform(360, 520))
        x, y = rng.uniform(-80, W - w_ + 80), rng.uniform(60, 640)
        img.alpha_composite(noda_cat(w_, h_, col, rng), (int(max(0, x)), int(y)))
    d = ImageDraw.Draw(img)
    f, lines, size = pas(d, bersih(p["teks"]), lambda s: ft("SignPainter.ttc", s, 1), W - 180, 520, 120, 60, 1.05)
    y = 520 - len(lines) * size * 1.05 / 2 + 60
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(250, 238, 210) if malam else (60, 50, 70), anchor="ma")
        y += size * 1.05
    ayat_bawah(img, p, 960, H - 60, (220, 214, 200) if malam else (80, 70, 80), (236, 196, 110) if malam else (170, 90, 110), start=32, stop=22)
    d.text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(160, 150, 160), anchor="ma")
    return grain(img.convert("RGB"), 0.04)


# ---------- KARTUNATAL: kartu Natal terbuka ----------

def pohon(d, cx, top, h, col=(30, 110, 70)):
    for k in range(4):
        w_ = h * (0.22 + 0.13 * k)
        y = top + k * h * 0.2
        d.polygon([(cx, y), (cx + w_, y + h * 0.32), (cx - w_, y + h * 0.32)], fill=col)
    d.rectangle((cx - h * 0.05, top + h * 0.92, cx + h * 0.05, top + h * 1.05), fill=(110, 70, 40))
    gaya_w10.bintang5(d, cx, top, h * 0.08, (240, 200, 70))


def kartunatal_image(p, i):
    rng = np.random.default_rng(6500 + i)
    img = gaya_w10.bokeh(W, H, 6500 + i)
    pw, ph = 470, 760
    kiri = Image.new("RGBA", (pw, ph), (176, 30, 44, 255))
    kd = ImageDraw.Draw(kiri)
    kd.rectangle((24, 24, pw - 24, ph - 24), outline=(236, 196, 110), width=4)
    for _ in range(40):
        x, y, s = rng.uniform(40, pw - 40), rng.uniform(40, ph - 40), rng.uniform(2, 5)
        kd.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, 180))
    pohon(kd, pw / 2, 150, 340)
    f, lines, size = pas(kd, bersih(p["depan"]), lambda s: ft("SnellRoundhand.ttc", s, 2), pw - 80, 180, 64, 34, 1.1)
    y = 540
    for ln in lines:
        kd.text((pw / 2, y), ln, font=f, fill=(255, 240, 210), anchor="ma")
        y += size * 1.1
    kanan = Image.new("RGBA", (pw, ph), (252, 248, 240, 255))
    rd = ImageDraw.Draw(kanan)
    rd.rectangle((24, 24, pw - 24, ph - 24), outline=(220, 200, 170), width=2)
    f, lines, size = pas(rd, bersih(p["isi"]), tangan, pw - 90, 320, 40, 26, 1.28)
    y = 70
    for ln in lines:
        rd.text((45, y), ln, font=f, fill=(40, 50, 100))
        y += size * 1.28
    y += 20
    rd.line((45, y, pw - 45, y), fill=(220, 200, 170), width=2)
    y += 24
    f2, l2, s2 = pas(rd, bersih(p["ayat"]), lambda s: georgia(s, True), pw - 90, ph - 90 - y, 28, 18, 1.36)
    for ln in l2:
        rd.text((45, y), ln, font=f2, fill=(90, 70, 60))
        y += s2 * 1.36
    rd.text((45, y + 6), p["ref"], font=hn(24, 1), fill=(176, 30, 44))
    kartu = Image.new("RGBA", (pw * 2 + 10, ph), (0, 0, 0, 0))
    kartu.alpha_composite(kiri, (0, 0))
    kartu.alpha_composite(kanan, (pw + 10, 0))
    lipat = Image.new("RGBA", kartu.size, (0, 0, 0, 0))
    ImageDraw.Draw(lipat).rectangle((pw - 20, 0, pw + 30, ph), fill=(0, 0, 0, 60))
    kartu.alpha_composite(lipat.filter(ImageFilter.GaussianBlur(12)))
    bayangan(img, kartu, ((W - kartu.width) // 2, 230), blur=22, geser=(0, 18), kuat=0.5)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 110), "Kartu untukmu", font=georgia(52, True), fill=(250, 226, 170), anchor="ma")
    d.text((W / 2, H - 70), "@" + HANDLE, font=hn(24, 10), fill=(220, 200, 180), anchor="ma")
    return img


# ---------- CRAYON: gambar krayon anak ----------

def garis_krayon(d, pts, col, rng, w=6, ulang=4):
    for _ in range(ulang):
        q = [(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3)) for x, y in pts]
        d.line(q, fill=col + (int(rng.uniform(140, 220)),), width=w, joint="curve")


def arsir(d, box, col, rng, rapat=9):
    x0, y0, x1, y1 = box
    for k in range(int((x1 - x0 + y1 - y0) / rapat)):
        a = x0 + k * rapat
        d.line((a, y0, a - (y1 - y0), y1), fill=col + (int(rng.uniform(70, 140)),), width=4)


def crayon_image(p, i, hitam_=False):
    rng = np.random.default_rng(6600 + i)
    img = grain(Image.new("RGB", (W, H), (26, 26, 30) if hitam_ else (254, 253, 248)), 0.06).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    kuning, biru, coklat, merah, hijau, hitam = (240, 196, 40), (60, 120, 220), (150, 90, 40), (220, 60, 60), (60, 170, 80), (40, 40, 50)
    if hitam_:  # krayon di kertas hitam: warna lebih terang
        biru, coklat, merah, hijau, hitam = (120, 170, 255), (220, 160, 100), (255, 110, 110), (110, 220, 120), (236, 236, 236)
    garis_krayon(d, [(60, 860), (W - 60, 860)], hijau, rng, w=8)
    g = p["gambar"]
    gaya_w10.bintang5(d, 830, 230, 70, kuning + (170,))
    garis_krayon(d, [(830, 160), (850, 210), (900, 230), (850, 250), (830, 300), (810, 250), (760, 230), (810, 210), (830, 160)], kuning, rng)
    for k in range(5):
        garis_krayon(d, [(830, 300 + k * 10), (700 - k * 60, 760)], kuning, rng, w=3, ulang=1)
    if g in ("palungan", "keluarga"):
        garis_krayon(d, [(380, 760), (420, 850), (640, 850), (680, 760), (380, 760)], coklat, rng)
        arsir(d, (390, 770, 670, 845), coklat, rng)
        d.ellipse((480, 700, 580, 770), fill=(250, 220, 190, 200))
        garis_krayon(d, [(480, 735), (530, 700), (580, 735), (530, 770), (480, 735)], merah, rng, w=4)
    if g == "keluarga":
        for x, tinggi, col in ((240, 330, biru), (820, 360, coklat)):
            d.ellipse((x - 40, 860 - tinggi - 80, x + 40, 860 - tinggi), outline=hitam + (200,), width=6)
            garis_krayon(d, [(x, 860 - tinggi), (x, 860 - 120)], col, rng)
            garis_krayon(d, [(x - 70, 860 - tinggi + 70), (x + 70, 860 - tinggi + 70)], col, rng)
            garis_krayon(d, [(x, 860 - 120), (x - 50, 858)], col, rng)
            garis_krayon(d, [(x, 860 - 120), (x + 50, 858)], col, rng)
    if g == "malaikat":
        garis_krayon(d, [(540, 380), (430, 760), (650, 760), (540, 380)], (200, 200, 230), rng)
        arsir(d, (450, 420, 630, 750), (200, 210, 240), rng)
        d.ellipse((490, 290, 590, 390), outline=hitam + (200,), width=6)
        garis_krayon(d, [(480, 280), (600, 280)], kuning, rng)
        garis_krayon(d, [(470, 470), (300, 400), (380, 560), (470, 520)], (180, 200, 240), rng)
        garis_krayon(d, [(610, 470), (780, 400), (700, 560), (610, 520)], (180, 200, 240), rng)
    if g == "bintang":
        for x, y in ((200, 300), (380, 180), (620, 360), (200, 560)):
            gaya_w10.bintang5(d, x, y, 26, kuning + (150,))
        garis_krayon(d, [(100, 860), (300, 640), (520, 860)], coklat, rng)
        garis_krayon(d, [(450, 860), (700, 600), (980, 860)], coklat, rng)
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    fk = ft("Chalkboard.ttc", 60, 1)
    while d.textlength(bersih(p["judul"]), font=fk) > W - 120:
        fk = ft("Chalkboard.ttc", fk.size - 2, 1)
    d.text((W / 2, 50), bersih(p["judul"]), font=fk, fill=(255, 120, 120) if hitam_ else (220, 60, 60), anchor="ma")
    y = 900
    for ln in wrap(d, bersih(p["teks"]), ft("Chalkboard.ttc", 38, 0), W - 140):
        d.text((W / 2, y), ln, font=ft("Chalkboard.ttc", 38, 0), fill=(170, 200, 255) if hitam_ else (60, 80, 160), anchor="ma")
        y += 50
    ayat_bawah(img, p, y + 20, H - 60, (230, 226, 220) if hitam_ else (70, 66, 60), (255, 150, 120) if hitam_ else (200, 70, 60), start=30, stop=20)
    d.text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(170, 160, 150), anchor="ma")
    return img


# ---------- KOPI: gelas kopi ----------

def kopi_image(p, i, merah=False):
    rng = np.random.default_rng(6700 + i)
    img = kayu(W, H, rng, (170, 120, 80)).convert("RGBA")
    bok = gaya_w10.bokeh(W, 560, 6750 + i)
    img.alpha_composite(bok.filter(ImageFilter.GaussianBlur(6)), (0, 0))
    cx, top, bot = W / 2, 180, 900
    gelas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(gelas)
    g.polygon([(cx - 230, top + 70), (cx + 230, top + 70), (cx + 175, bot), (cx - 175, bot)], fill=(184, 28, 42, 255) if merah else (250, 248, 244, 255))
    g.rounded_rectangle((cx - 255, top, cx + 255, top + 80), radius=24, fill=(240, 238, 234, 255))
    g.rounded_rectangle((cx - 200, top - 40, cx + 200, top + 10), radius=20, fill=(228, 226, 222, 255))
    g.polygon([(cx - 214, top + 330), (cx + 214, top + 330), (cx + 196, top + 560), (cx - 196, top + 560)], fill=(176, 130, 86, 255))
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).polygon([(cx + 120, top + 80), (cx + 230, top + 80), (cx + 175, bot), (cx + 90, bot)], fill=(0, 0, 0, 30))
    gelas.alpha_composite(sombra)
    bayangan(img, gelas, (0, 0), blur=22, geser=(14, 18), kuat=0.35)
    d = ImageDraw.Draw(img)
    fn_ = ft("/System/Library/Fonts/MarkerFelt.ttc", 70, 1)
    while d.textlength(bersih(p["nama"]), font=fn_) > 360:
        fn_ = ft("/System/Library/Fonts/MarkerFelt.ttc", fn_.size - 4, 1)
    d.text((cx, top + 200), bersih(p["nama"]), font=fn_, fill=(255, 250, 240) if merah else (40, 40, 50), anchor="mm")
    f, lines, size = pas(d, bersih(p["pesan"]), tangan, 360, 200, 40, 24, 1.15)
    y = top + 445 - len(lines) * size * 1.15 / 2
    for ln in lines:
        d.text((cx, y), ln, font=f, fill=(60, 36, 20), anchor="ma")
        y += size * 1.15
    d.ellipse((cx - 20, top + 640, cx + 20, top + 680), outline=(196, 40, 50), width=4)
    ayat_bawah(img, p, 960, H - 60, (255, 246, 230), (255, 214, 140), start=32, stop=22)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(240, 220, 200), anchor="ma")
    return img


# ---------- PERJALANAN: peta kuno ----------

KOTA = {"Nazaret": (610, 300), "Kapernaum": (700, 230), "Kana": (640, 260), "Yerusalem": (600, 760), "Betlehem": (590, 830),
        "Yerikho": (700, 740), "Samaria": (580, 520), "Galilea": (660, 260), "Mesir": (380, 930), "Timur": (1000, 560),
        "Betania": (630, 770), "Hebron": (560, 930), "Emaus": (540, 760),
        "Padang gembala": (690, 880)}


def perjalanan_image(p, i):
    rng = np.random.default_rng(6800 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array([234, 214, 170])
    base *= (0.86 + 0.18 * render.fbm2d(H, W, rng, ((4, 1.0), (24, 0.5), (90, 0.3))))[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    laut = (150, 180, 186)
    pantai = [(0, 0), (420, 0)] + [(420 - 120 * (y / H) - 30 * math.sin(y / 90), y) for y in range(0, H, 30)] + [(0, H)]
    d.polygon(pantai, fill=laut)
    d.ellipse((700, 250, 760, 330), fill=laut)  # danau Galilea
    sungai = [(730, 330)] + [(722 + 12 * math.sin(y / 40), y) for y in range(340, 760, 20)]
    d.line(sungai, fill=laut, width=7)
    d.ellipse((700, 760, 770, 960), fill=laut)  # Laut Mati
    for k in range(9):
        y = 130 + k * 120
        d.line([(x, y + 10 * math.sin(x / 50)) for x in range(20, 380, 20)], fill=(120, 150, 160), width=2)
    awal = KOTA.get(bersih(p["dari"]), (610, 300))
    akhir = KOTA.get(bersih(p["ke"]), (590, 830))
    mid = ((awal[0] + akhir[0]) / 2 + 70, (awal[1] + akhir[1]) / 2)
    rute = [(awal[0] + (2 * (1 - t) * t) * (mid[0] - awal[0]) * 2 + t * t * (akhir[0] - awal[0]),
             awal[1] + (2 * (1 - t) * t) * (mid[1] - awal[1]) * 2 + t * t * (akhir[1] - awal[1])) for t in np.linspace(0, 1, 60)]
    for k in range(0, len(rute) - 1, 2):
        d.line((rute[k], rute[k + 1]), fill=(170, 40, 40), width=6)
    tampil = []
    for nama in [bersih(p["dari"]), bersih(p["ke"]), "Yerusalem", "Nazaret", "Betlehem", "Kapernaum", "Yerikho", "Samaria", "Hebron"]:
        if nama in KOTA and nama not in tampil and all(math.dist(KOTA[nama], KOTA[o]) > 70 for o in tampil):
            tampil.append(nama)
    for nama in tampil:
        x, y = KOTA[nama]
        if x > W - 200:
            x = W - 200
        utama = nama in (bersih(p["dari"]), bersih(p["ke"]))
        r = 12 if utama else 6
        d.ellipse((x - r, y - r, x + r, y + r), fill=(170, 40, 40) if utama else (80, 60, 40))
        d.text((x + 20, y - 16), nama, font=ft("Iowan Old Style.ttc", 30 if utama else 22, 1 if utama else 0), fill=(70, 46, 26))
    cx, cy = 900, 180  # mawar angin
    for a, L in ((0, 80), (90, 60), (180, 60), (270, 60)):
        ang = math.radians(a - 90)
        d.polygon([(cx + L * math.cos(ang), cy + L * math.sin(ang)), (cx + 12 * math.cos(ang + 1.57), cy + 12 * math.sin(ang + 1.57)),
                   (cx + 12 * math.cos(ang - 1.57), cy + 12 * math.sin(ang - 1.57))], fill=(90, 60, 40))
    d.text((cx, cy - 110), "U", font=ft("Iowan Old Style.ttc", 30, 1), fill=(90, 60, 40), anchor="mm")
    d.rounded_rectangle((60, 40, 640, 150), radius=16, fill=(244, 230, 196), outline=(120, 80, 50), width=3)
    f, ls, sz = pas(d, bersih(p["judul"]), lambda s: ft("Trattatello.ttf", s), 540, 90, 44, 24, 1.1)
    yy = 95 - len(ls) * sz * 1.1 / 2
    for ln in ls:
        d.text((350, yy), ln, font=f, fill=(110, 40, 30), anchor="ma")
        yy += sz * 1.1
    d.text((mid[0] + 30, mid[1]), bersih(p["jarak"]), font=ft("Iowan Old Style.ttc", 30, 1), fill=(170, 40, 40))
    y = 1000
    d.rounded_rectangle((60, y - 20, W - 60, H - 40), radius=20, fill=(244, 232, 204), outline=(150, 110, 70), width=2)
    for c in p["catatan"]:
        d.text((90, y), "• " + bersih(c), font=georgia(28), fill=(70, 46, 26))
        y += 40
    ayat_bawah(img, p, y + 10, H - 60, (70, 46, 26), (170, 40, 40), maxw=W - 200, start=26, stop=18)
    ImageDraw.Draw(img).text((W - 70, H - 50), "@" + HANDLE, font=hn(18, 10), fill=(140, 110, 80), anchor="ra")
    return img


# ---------- LAMPU (Reels): lampu tumbler ----------

def lampu_reel(p, idx, mod=MOD, seconds=12, pohon=False):
    rel = f"reels/{mod}/lampu{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(6900 + idx)
    bg = gradasi(RW, RH, (26, 20, 30), (10, 8, 14)).convert("RGBA")
    bulbs = []
    if pohon:  # pohon Natal dengan untaian lampu zig-zag
        bd_ = ImageDraw.Draw(bg)
        top_, bot_ = 980, 1720
        bd_.polygon([(RW / 2, top_), (RW / 2 + 420, bot_), (RW / 2 - 420, bot_)], fill=(20, 70, 40, 255))
        bd_.rectangle((RW / 2 - 40, bot_, RW / 2 + 40, bot_ + 90), fill=(90, 56, 34, 255))
        gaya_w10.bintang5(bd_, RW / 2, top_ - 10, 46, (255, 214, 90, 255))
        for k in range(6):
            y1 = top_ + 90 + k * 110
            w1 = (y1 - top_) / (bot_ - top_) * 420
            pts_ = [(RW / 2 - w1 + t * 2 * w1, y1 + 50 * t + 30 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 9)]
            bd_.line(pts_, fill=(40, 60, 40, 255), width=4)
            for x, y in pts_[1:-1]:
                bulbs.append((x, y - 26, [(255, 80, 80), (80, 220, 120), (255, 210, 80), (90, 160, 255)][len(bulbs) % 4], rng.uniform(0, 6.28)))
    for k, (y0, amp) in enumerate(() if pohon else ((150, 70), (560, 60), (1560, 70))):
        for x in range(-20, RW + 40, 70):
            y = y0 + amp * math.sin(x / 190 + k)
            bulbs.append((x, y, [(255, 80, 80), (80, 220, 120), (255, 210, 80), (90, 160, 255)][len(bulbs) % 4], rng.uniform(0, 6.28)))
    kabel = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kabel)
    for k, (y0, amp) in enumerate(() if pohon else ((150, 70), (560, 60), (1560, 70))):
        kd.line([(x, y0 + amp * math.sin(x / 190 + k)) for x in range(-20, RW + 40, 20)], fill=(40, 60, 40, 255), width=4)
    bg.alpha_composite(kabel)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    teks = Image.new("RGBA", (RW, 360), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks)
    td.text((RW / 2, 0), bersih(p["judul"]), font=georgia(62, True), fill=(255, 226, 160), anchor="ma")
    y = 100
    for ln in wrap(td, bersih(p["teks"]), georgia(40), RW - 200):
        td.text((RW / 2, y), ln, font=georgia(40), fill=(246, 238, 226), anchor="ma")
        y += 54
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 520, 40, 26, 1.38)
    ayat = Image.new("RGBA", (RW, 760), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(236, 228, 214), anchor="ma")
        y += vs * 1.38
    ad.text((RW / 2, y + 14), p["ref"], font=hn(32, 1), fill=(255, 210, 120), anchor="ma")
    ad.text((RW / 2, y + 72), "@" + HANDLE, font=hn(26, 10), fill=(170, 150, 160), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        glow = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        dot = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        dd = ImageDraw.Draw(dot)
        for x, y, c, ph in bulbs:
            a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 3.2 + ph))
            gd.ellipse((x - 34, y - 20, x + 34, y + 60), fill=c + (int(120 * a),))
            dd.ellipse((x - 11, y + 4, x + 11, y + 36), fill=tuple(int(v * (0.5 + 0.5 * a)) for v in c) + (255,))
        frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
        frame.alpha_composite(dot)
        frame.alpha_composite(teks, (0, 200 if pohon else 300))
        if t >= 1.5:
            frame.alpha_composite(fade(ayat, ease((t - 1.5) / 0.8)), (0, 540 if pohon else 720))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- KONFETI (Reels) ----------

def konfeti_reel(p, idx, mod=MOD, seconds=12):
    rel = f"reels/{mod}/konfeti{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7000 + idx)
    bg = grain(gradasi(RW, RH, (255, 236, 214), (250, 206, 196)), 0.04).convert("RGBA")
    n = 320
    ang = rng.uniform(-math.pi * 0.85, -math.pi * 0.15, n)
    sp = rng.uniform(900, 2000, n)
    vx, vy = np.cos(ang) * sp, np.sin(ang) * sp
    warna = [(240, 70, 90), (60, 160, 230), (250, 200, 50), (80, 200, 120), (180, 100, 220)]
    cols = [warna[k % 5] for k in range(n)]
    rot0, rotv = rng.uniform(0, 360, n), rng.uniform(-400, 400, n)
    ox, oy = RW / 2, 1500
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fs = hn(140, 9)
    while probe.textlength(bersih(p["seru"]).upper(), font=fs) > RW - 120 and fs.size > 60:
        fs = hn(fs.size - 6, 9)
    seru_lines = wrap(probe, bersih(p["seru"]).upper(), fs, RW - 120)
    seru = Image.new("RGBA", (RW, int(len(seru_lines) * fs.size * 1.05 + 40)), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seru)
    for k, ln in enumerate(seru_lines):
        sd.text((RW / 2, 10 + k * fs.size * 1.05), ln, font=fs, fill=(200, 40, 70), anchor="ma", stroke_width=6, stroke_fill=(255, 255, 255))
    teks = Image.new("RGBA", (RW, 300), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks)
    y = 0
    for ln in wrap(td, bersih(p["teks"]), georgia(42), RW - 200):
        td.text((RW / 2, y), ln, font=georgia(42), fill=(70, 40, 40), anchor="ma")
        y += 56
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 380, 38, 24, 1.36)
    ayat = Image.new("RGBA", (RW, 560), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    ad.rounded_rectangle((70, 0, RW - 70, len(vl) * vs * 1.36 + 140), radius=30, fill=(255, 255, 255, 200))
    y = 34
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(70, 50, 50), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 10), p["ref"], font=hn(32, 1), fill=(200, 40, 70), anchor="ma")
    ad.text((RW / 2, y + 62), "@" + HANDLE, font=hn(24, 10), fill=(150, 110, 110), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for fr in range(seconds * FPS):
        t = fr / FPS
        frame = bg.copy()
        s = 1.0 + 0.05 * math.sin(t * 5) * max(0.0, 1 - t / 2)
        sw_ = seru.resize((int(seru.width * s), int(seru.height * s)))
        frame.alpha_composite(sw_, ((RW - sw_.width) // 2, int(300 - (sw_.height - seru.height) / 2)))
        if t >= 0.8:
            frame.alpha_composite(fade(teks, ease((t - 0.8) / 0.6)), (0, 330 + seru.height + 30))
        if t >= 2.2:
            frame.alpha_composite(fade(ayat, ease((t - 2.2) / 0.7)), (0, 820))
        lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for tt, geser in ((t + 0.9, 0), (t - 5.0, n // 2)):  # sampul: konfeti sudah menyebar; ledakan kedua di tengah video
            if tt <= 0:
                continue
            drag = (1 - math.exp(-1.8 * tt)) / 1.8
            xs = ox + vx * drag
            ys = oy + vy * drag + 420 * tt * tt
            for k0 in range(n):
                k = (k0 + geser) % n
                if ys[k0] > RH + 40:
                    continue
                a = math.radians(rot0[k] + rotv[k] * tt)
                w_, h_ = 14, 26 * abs(math.cos(a * 1.3)) + 4
                ca, sa = math.cos(a), math.sin(a)
                pts = [(xs[k0] + dx * ca - dy * sa, ys[k0] + dx * sa + dy * ca) for dx, dy in ((-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2))]
                ld.polygon(pts, fill=cols[k] + (230,))
        frame.alpha_composite(lay)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def koransepia_image(p, i):
    img = gaya_w8.koran_image(dict(p, _edisi="EDISI NATAL"), i).convert("RGB")
    a = np.asarray(img).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True)
    sep = lum * np.array([1.07, 0.92, 0.72]) + np.array([12, 6, 0])
    return Image.fromarray(np.clip(sep, 0, 255).astype(np.uint8))


def pastel(w, h, seed):
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (250, 222, 230), (210, 236, 228)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(26):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(40, 120)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 40))
    return img


SIMPLE = {
    # baru
    "BALON": balon_image, "BINGO": bingo_image, "EMAIL": email_image, "VENN": venn_image, "STAMP": stamp_image,
    "WATERCOLOR": watercolor_image, "KARTUNATAL": kartunatal_image, "CRAYON": crayon_image, "KOPI": kopi_image,
    "PERJALANAN": perjalanan_image,
    # lama
    "KALENDER": gaya_w7.kalender_image, "STRUK": gaya_w7.struk_image, "CATATAN": gaya_w7.catatan_image, "KETIK": gaya_w7.ketik_image,
    "KARTUPOS": gaya_w8.kartupos_image, "PETA": gaya_w8.peta_image, "KODE": gaya_w8.kode_image, "MUSEUM": gaya_w9.museum_image,
    "SERTIFIKAT": gaya_w9.sertifikat_image, "JAM": gaya_w9.jam_image,
    # mix
    "KALADVENMERAH": lambda p, i: gaya_w10.kaladven_image(p, i, merah=True),
    "KORANSEPIA": koransepia_image,
    "TIKETKERETA": lambda p, i: gaya_w7.tiket_image(p, i, kereta=True),
    "STICKYPASTEL": lambda p, i: gaya_w8.sticky_image(p, i, latar=pastel(W, H, 7100 + i)),
    "KAMUSGELAP": lambda p, i: gaya_w7.kamus_image(p, i, gelap=True),
    "UNDANGANHIJAU": lambda p, i: gaya_w9.undangan_image(p, i, warna=(32, 92, 72)),
    "KASETPUTIH": lambda p, i: gaya_w9.kaset_image(p, i, putih=True),
    "LILINJENDELA": lambda p, i: gaya_w8.lilin_image(p, i, jendela=True),
    "TELEGRAMNATAL": lambda p, i: gaya_w10.telegram_image(p, i, latar=kertas_kado(W, H, i)),
    "MAJALAHNATAL": lambda p, i: gaya_w10.majalah_image(p, i, latar=gaya_w10.bokeh(W, H, 7200 + i)),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
REELS = {"LAMPU": (lampu_reel, "lampu"), "KONFETI": (konfeti_reel, "konfeti"), "PROGRESS": (gaya_w9.progress_reel, "progress"),
         "GOSOK": (gaya_w9.gosok_reel, "gosok"), "SEARCHGELAP": (lambda p, i, mod: gaya_w8.search_reel(p, i, mod, gelap=True), "search"),
         "KRANSTERANG": (lambda p, i, mod: gaya_w10.krans_reel(p, i, mod, terang=True), "krans")}


def render_week(mod=MOD):
    return gaya_w11.render_week(mod, SIMPLE, REELS, MULAI)


def render_reels(mod=MOD):
    gaya_w11.render_reels(mod, REELS, MULAI)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
