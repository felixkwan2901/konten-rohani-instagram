"""Akun Tenang - minggu 11 (konten/tenang_w11.py), Adven II "Damai": 36 gaya diacak tiap hari + komik Eli baru.
BARU : VINYL (Reels piringan hitam berputar), SALJU (Reels salju turun di desa malam), FLIPCLOCK (jam flip, hitung mundur),
       KACAPATRI (jendela kaca patri), SCROLL (gulungan kitab), HPJADUL (SMS di HP jadul), PHOTOBOOTH (strip foto),
       SIGNPOST (papan penunjuk arah), TAG (label kado), CHART (grafik batang), PIXEL (layar game 8-bit), REKAP (rekap tahunan).
LAMA : SEARCH, NEON, GLOBE, KORAN, TIKET, POPUP, STICKY, KAMUS, RESEP, UNDANGAN, KASET, LILIN.
MIX  : CHATNATAL, FLIPEMAS, ORNAMENSALJU, LETTERPUTIH, CUACASALJU, POLAROIDLINEN, PLAYERTERANG, ALKITABMALAM, NAMAEMAS,
       DOAFOTO, MENUPUTIH, TOPLESMALAM.  KOMIK = komik Eli & Yesus (gaya child.ink) pengganti folder Eli yang sudah habis.

  python3 gaya_w11.py [reels]
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
import gaya_w6
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import render
from gaya_w6 import cover, foto_warna, georgia, hn, tambah_musik
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tangan, tanpa_kutip, vintage
from gaya_w8 import HARI, kayu
from gaya_w9 import EMAS, ayat_bawah, kertas_kado
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w11"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2026, 12, 6)
BULAN = {11: "November", 12: "Desember"}


def konteks(p, hari, slot, mulai=MULAI):
    """Tanggal & jam slot untuk gaya lama yang menampilkan waktu."""
    tgl = mulai + dt.timedelta(days=hari - 1)
    jam = config.AKUN["tenang"]["jam"][slot].replace(":", ".")
    return dict(p, _jam=jam, _tanggal=f"{tgl.day} {BULAN[tgl.month]} 2026", _tgl_struk=tgl.strftime("%d/%m/%Y"),
                _tgl_titik=tgl.strftime("%d.%m.%Y"), _tanggal_panjang=f"{HARI[(hari - 1) % 7]}, {tgl.day} {BULAN[tgl.month]} 2026")


def kepingan(d, x, y, r, col, w=2):
    for a in range(0, 180, 60):
        ang = math.radians(a)
        d.line((x - r * math.cos(ang), y - r * math.sin(ang), x + r * math.cos(ang), y + r * math.sin(ang)), fill=col, width=w)


def salju_latar(w, h, seed):
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (22, 34, 70), (8, 12, 30)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 9000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(3, 9)
        if r > 7:
            kepingan(d, x, y, r, (220, 230, 255, 160))
        else:
            d.ellipse((x - r / 3, y - r / 3, x + r / 3, y + r / 3), fill=(255, 255, 255, int(rng.uniform(90, 200))))
    return img


def linen_latar(w, h, seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array([238, 232, 222])
    a += (np.sin(np.arange(w) * 2.1)[None, :, None] + np.sin(np.arange(h) * 2.3)[:, None, None]) * 3
    a *= (0.95 + 0.07 * render.fbm2d(h, w, rng, ((4, 1.0), (30, 0.5))))[..., None]
    img = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))  # lampu tumbler
    d = ImageDraw.Draw(lay)
    pts = [(x, 60 + 46 * math.sin(x / 150)) for x in range(-20, w + 40, 55)]
    d.line(pts, fill=(120, 110, 100, 255), width=3)
    for x, y in pts:
        d.ellipse((x - 9, y, x + 9, y + 22), fill=(255, 206, 120, 255))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(lay)
    return img


# ================= BARU =================

# ---------- FLIPCLOCK: jam flip hitung mundur ----------

def kartu_flip(teks, w, h):
    k = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(k)
    d.rounded_rectangle((0, 0, w, h), radius=26, fill=(30, 30, 34, 255))
    d.rounded_rectangle((0, 0, w, h // 2), radius=26, fill=(40, 40, 46, 255))
    d.rectangle((0, h // 2 - 26, w, h // 2), fill=(40, 40, 46, 255))
    d.text((w / 2, h / 2 + 8), teks, font=hn(int(h * 0.82), 9), fill=(246, 242, 232, 255), anchor="mm")
    d.rectangle((0, h // 2 - 3, w, h // 2 + 3), fill=(8, 8, 10, 255))
    for x in (0, w - 10):
        d.rectangle((x, h // 2 - 14, x + 10, h // 2 + 14), fill=(70, 70, 76, 255))
    return k


def flipclock_image(p, i, latar=None):
    rng = np.random.default_rng(5000 + i)
    img = latar.copy().convert("RGBA") if latar is not None else gaya_w10.bokeh(W, H, 5000 + i, ((255, 200, 120), (255, 150, 100), (200, 220, 255)))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 70), p["tanggal"].upper(), font=hn(28, 10), fill=(240, 220, 190), anchor="ma")
    angka = f"{p['angka']:02d}"
    cw, chh, gap = 330, 440, 30
    x0 = W / 2 - cw - gap / 2
    for k, c in enumerate(angka):
        bayangan(img, kartu_flip(c, cw, chh), (x0 + k * (cw + gap), 160), blur=20, geser=(0, 16), kuat=0.5)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 650), bersih(p.get("label", "HARI LAGI")), font=hn(52, 1), fill=(255, 246, 226), anchor="ma")
    d.text((W / 2, 724), bersih(p.get("sublabel", "menuju Natal")), font=georgia(48, True), fill=(240, 196, 120), anchor="ma")
    y = 810
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 200):
        d.text((W / 2, y), ln, font=georgia(34), fill=(246, 238, 226), anchor="ma")
        y += 46
    ayat_bawah(img, p, y + 24, H - 60, (220, 210, 200), (240, 196, 120), start=30, stop=20)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(170, 150, 130), anchor="ma")
    return img


# ---------- KACAPATRI: jendela kaca patri ----------

KACA = [(40, 70, 150), (30, 110, 160), (70, 50, 140), (40, 120, 90), (120, 40, 90), (30, 90, 130), (60, 100, 170)]
HANGAT = [(250, 200, 70), (255, 236, 160), (230, 120, 50), (250, 170, 60)]


def motif_mask(motif, w, h):
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    cx, cy = w / 2, h * 0.52
    if motif == "salib":
        d.rectangle((cx - w * .07, h * .2, cx + w * .07, h * .86), fill=255)
        d.rectangle((cx - w * .26, h * .36, cx + w * .26, h * .47), fill=255)
    elif motif == "bintang":
        pts = []
        for k in range(10):
            rr = w * .34 if k % 2 == 0 else w * .14
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=255)
    elif motif == "merpati":
        d.ellipse((cx - w * .2, cy - h * .07, cx + w * .16, cy + h * .07), fill=255)
        d.ellipse((cx + w * .08, cy - h * .12, cx + w * .24, cy + h * .0), fill=255)
        d.polygon([(cx - w * .05, cy - h * .02), (cx - w * .34, cy - h * .2), (cx + w * .06, cy - h * .05)], fill=255)
        d.polygon([(cx - w * .18, cy), (cx - w * .36, cy + h * .08), (cx - w * .16, cy + h * .05)], fill=255)
        d.polygon([(cx + w * .24, cy - h * .07), (cx + w * .32, cy - h * .05), (cx + w * .24, cy - h * .03)], fill=255)
    else:  # lilin
        d.rectangle((cx - w * .09, cy - h * .05, cx + w * .09, h * .86), fill=255)
        d.polygon([(cx, cy - h * .3), (cx + w * .08, cy - h * .14), (cx, cy - h * .08), (cx - w * .08, cy - h * .14)], fill=255)
    return np.asarray(m) > 128


def kacapatri_image(p, i):
    rng = np.random.default_rng(5100 + i)
    ww, wh = 700, 900
    sw, sh = ww // 4, wh // 4
    n = 150
    sx, sy = rng.uniform(0, sw, n), rng.uniform(0, sh, n)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    lab = np.argmin((xx[..., None] - sx) ** 2 + (yy[..., None] - sy) ** 2, axis=2)
    lab = np.asarray(Image.fromarray(lab.astype(np.int32)).resize((ww, wh), Image.NEAREST))
    mot = motif_mask(p["motif"], ww, wh)
    cols = np.zeros((n, 3), np.float32)
    for k in range(n):
        cx_, cy_ = int(sx[k] * 4), int(sy[k] * 4)
        inside = mot[min(wh - 1, cy_), min(ww - 1, cx_)]
        cols[k] = HANGAT[k % len(HANGAT)] if inside else KACA[k % len(KACA)]
    arr = cols[lab]
    arr[mot] = arr[mot] * 0.3 + np.array([252, 214, 110]) * 0.7  # motif dipertegas
    tepi = (np.diff(lab, axis=0, prepend=lab[:1]) != 0) | (np.diff(lab, axis=1, prepend=lab[:, :1]) != 0)
    mb = np.asarray(Image.fromarray(mot.astype(np.uint8) * 255).filter(ImageFilter.FIND_EDGES)) > 0
    lead = Image.fromarray(((tepi | mb) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    yyf = np.linspace(1.25, 0.8, wh)[:, None, None]
    arr = arr * yyf * (0.9 + 0.2 * render.fbm2d(wh, ww, rng, ((8, 1.0), (60, 0.5))))[..., None]
    kaca = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    kaca.paste((24, 22, 24, 255), (0, 0), lead)
    m = Image.new("L", (ww, wh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, ww, wh + 400), radius=ww // 2, fill=255)
    kaca.putalpha(m)
    wall = np.zeros((H, W, 3), np.float32) + np.array([70, 64, 60])
    wall *= (0.75 + 0.4 * render.fbm2d(H, W, rng, ((10, 1.0), (80, 0.5))))[..., None]
    img = Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8)).convert("RGBA")
    frame = Image.new("RGBA", (ww + 60, wh + 60), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle((0, 0, ww + 60, wh + 460), radius=(ww + 60) // 2, fill=(150, 140, 126, 255))
    frame = frame.crop((0, 0, ww + 60, wh + 60))
    x0, y0 = (W - ww) // 2, 70
    bayangan(img, frame, (x0 - 30, y0 - 30), blur=20, geser=(0, 10), kuat=0.5)
    img.alpha_composite(kaca, (x0, y0))
    sinar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sinar).polygon([(x0 + 80, y0 + wh), (x0 + ww - 80, y0 + wh), (W - 20, H), (20, H)], fill=(255, 220, 160, 40))
    img.alpha_composite(sinar.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img)
    d.text((W / 2, y0 + wh + 40), bersih(p["judul"]), font=georgia(44, True), fill=(250, 226, 170), anchor="ma")
    ayat_bawah(img, p, y0 + wh + 110, H - 50, (236, 228, 214), (250, 206, 120), start=30, stop=20)
    ImageDraw.Draw(img).text((W - 40, H - 16), "@" + HANDLE, font=hn(18, 10), fill=(170, 160, 150), anchor="rs")
    return img


# ---------- SCROLL: gulungan kitab ----------

def scroll_image(p, i):
    rng = np.random.default_rng(5200 + i)
    img = grain(gradasi(W, H, (60, 40, 30), (30, 20, 16)), 0.06).convert("RGBA")
    pw, ph = 860, 1080
    kertas = np.zeros((ph, pw, 3), np.float32) + np.array([232, 212, 168])
    kertas *= (0.86 + 0.2 * render.fbm2d(ph, pw, rng, ((4, 1.0), (20, 0.6), (90, 0.3))))[..., None]
    xs = np.linspace(-1, 1, pw)[None, :]
    kertas *= (1 - 0.18 * xs ** 6)[..., None]
    perk = Image.fromarray(np.clip(kertas, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(perk)
    ink = (60, 36, 20)
    ft_ = ft("Trattatello.ttf", 64)
    while d.textlength(bersih(p["judul"]), font=ft_) > pw - 140:
        ft_ = ft("Trattatello.ttf", ft_.size - 4)
    d.text((pw / 2, 90), bersih(p["judul"]), font=ft_, fill=(130, 40, 30), anchor="ma")
    d.line((pw / 2 - 160, 190, pw / 2 + 160, 190), fill=(130, 40, 30), width=2)
    iow = lambda s: ft("Iowan Old Style.ttc", s, 2)
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), iow, pw - 160, ph - 380, 46, 28, 1.42)
    y = 240 + (ph - 380 - len(lines) * size * 1.42) / 2
    for ln in lines:
        d.text((pw / 2, y), ln, font=f, fill=ink, anchor="ma")
        y += size * 1.42
    d.text((pw / 2, y + 26), p["ref"], font=ft("Iowan Old Style.ttc", 32, 1), fill=(130, 40, 30), anchor="ma")
    x0, y0 = (W - pw) // 2, 150
    bayangan(img, perk, (x0, y0), blur=18, geser=(0, 14), kuat=0.5)
    d = ImageDraw.Draw(img)
    for yy in (y0 - 40, y0 + ph - 30):  # gulungan atas & bawah
        gl = np.zeros((70, pw + 60, 3), np.float32)
        t = np.linspace(-1, 1, 70)[:, None]
        gl += np.array([210, 186, 140]) * (0.55 + 0.45 * np.sqrt(np.clip(1 - t ** 2, 0, 1)))[..., None]
        img.paste(Image.fromarray(np.clip(gl, 0, 255).astype(np.uint8)), (x0 - 30, yy))
        for ex in (x0 - 70, x0 + pw + 30):
            d.rounded_rectangle((ex, yy - 6, ex + 40, yy + 76), radius=14, fill=(110, 66, 36))
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(22, 10), fill=(200, 170, 130), anchor="ma")
    return img


# ---------- HPJADUL: SMS di HP jadul ----------

def hpjadul_image(p, i):
    img = grain(gradasi(W, H, (210, 226, 214), (160, 190, 176)), 0.05).convert("RGBA")
    hw, hh = 520, 1010
    hp = Image.new("RGBA", (hw, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(hp)
    d.rounded_rectangle((hw - 120, 0, hw - 80, 120), radius=16, fill=(50, 52, 56, 255))  # antena
    d.rounded_rectangle((0, 70, hw, hh), radius=90, fill=(70, 74, 80, 255))
    d.rounded_rectangle((14, 84, hw - 14, hh - 14), radius=80, fill=(92, 96, 104, 255))
    d.rounded_rectangle((70, 170, hw - 70, 560), radius=26, fill=(40, 44, 48, 255))
    lw, lh = 152, 132  # layar LCD resolusi rendah lalu diperbesar
    lcd = Image.new("L", (lw, lh), 0)
    ld = ImageDraw.Draw(lcd)
    ld.fontmode = "1"
    fpx = ft("/System/Library/Fonts/Menlo.ttc", 11, 1)
    ld.text((2, 1), f"Pesan dari:", font=fpx, fill=255)
    ld.text((2, 13), bersih(p["pengirim"])[:20], font=fpx, fill=255)
    ld.line((0, 27, lw, 27), fill=255)
    lines = wrap(ld, bersih(p["pesan"]), fpx, lw - 4)
    y = 31
    for ln in lines[:7]:
        ld.text((2, y), ln, font=fpx, fill=255)
        y += 13
    ld.text((2, lh - 13), "Balas        Opsi", font=fpx, fill=255)
    lcdc = Image.new("RGBA", (lw, lh), (150, 176, 110, 255))
    lcdc.paste((30, 44, 26, 255), (0, 0), lcd.point(lambda v: 255 if v > 110 else 0))
    lcdc = lcdc.resize((int(lw * 2.45), int(lh * 2.45)), Image.NEAREST)
    hp.alpha_composite(lcdc, ((hw - lcdc.width) // 2, 202))
    d = ImageDraw.Draw(hp)
    for r in range(4):
        for c in range(3):
            x, y = 110 + c * 110, 640 + r * 84
            d.rounded_rectangle((x - 42, y - 26, x + 42, y + 26), radius=22, fill=(200, 204, 210, 255))
            d.text((x, y), "123456789*0#"[r * 3 + c], font=hn(30, 1), fill=(50, 52, 56, 255), anchor="mm")
    d.rounded_rectangle((hw / 2 - 70, 580, hw / 2 + 70, 612), radius=16, fill=(180, 184, 190, 255))
    hp = hp.rotate(-6, expand=True, resample=Image.BICUBIC)
    bayangan(img, hp, (60, 40), blur=22, geser=(10, 18), kuat=0.45)
    d = ImageDraw.Draw(img)
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), 385, 700, 36, 24, 1.38)
    y = 360
    for ln in lines:
        d.text((660, y), ln, font=f, fill=(30, 50, 40))
        y += size * 1.38
    d.text((660, y + 10), p["ref"], font=hn(28, 1), fill=(30, 90, 60))
    d.text((W - 40, H - 30), "@" + HANDLE, font=hn(22, 10), fill=(60, 80, 70), anchor="rs")
    return img


# ---------- PHOTOBOOTH: strip foto ----------

def photobooth_image(p, i, latar=None):
    rng = np.random.default_rng(5300 + i)
    img = latar.copy().convert("RGBA") if latar is not None else grain(gradasi(W, H, (244, 214, 214), (226, 196, 214)), 0.05).convert("RGBA")
    sw, sh = 420, 1220
    strip = Image.new("RGBA", (sw, sh), (252, 252, 250, 255))
    for k, (scene, lab) in enumerate(p["foto"]):
        y = 30 + k * 296
        ph = vintage(cover(foto_warna(scene, 500, 360, seed=5350 + i * 4 + k), sw - 40, 230))
        strip.paste(ph, (20, y))
        ImageDraw.Draw(strip).text((sw / 2, y + 252), bersih(lab), font=tangan(30), fill=(60, 60, 80), anchor="ma")
    strip = strip.rotate(-4, expand=True, resample=Image.BICUBIC)
    bayangan(img, strip, (70, (H - strip.height) // 2), blur=16, geser=(8, 14), kuat=0.4)
    d = ImageDraw.Draw(img)
    fj = tangan(64)
    lines = wrap(d, bersih(p["judul"]), fj, 410)
    y = 140
    for ln in lines:
        d.text((610, y), ln, font=fj, fill=(255, 226, 170) if latar is not None else (110, 40, 60))
        y += 76
    y += 40
    card_w = 430
    f, vl, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), card_w - 60, 640, 34, 22, 1.38)
    card = Image.new("RGBA", (card_w, int(len(vl) * size * 1.38 + 110)), (255, 255, 255, 230))
    cd = ImageDraw.Draw(card)
    yy = 30
    for ln in vl:
        cd.text((30, yy), ln, font=f, fill=(60, 40, 50))
        yy += size * 1.38
    cd.text((30, yy + 10), p["ref"], font=hn(28, 1), fill=(150, 50, 80))
    bayangan(img, card, (600, y), blur=12, geser=(4, 8), kuat=0.25)
    ImageDraw.Draw(img).text((W - 40, H - 30), "@" + HANDLE, font=hn(22, 10), fill=(140, 100, 120), anchor="rs")
    return img


# ---------- SIGNPOST: papan penunjuk arah ----------

def signpost_image(p, i):
    rng = np.random.default_rng(5400 + i)
    img = grain(gradasi(W, H, (150, 196, 236), (236, 226, 200)), 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.ellipse((-300, 900, W + 300, 1700), fill=(140, 180, 110))
    d.ellipse((-200, 960, W + 400, 1800), fill=(120, 164, 96))
    d.rectangle((W / 2 - 22, 160, W / 2 + 22, 1020), fill=(110, 76, 50))
    d.rectangle((W / 2 - 22, 160, W / 2 - 10, 1020), fill=(130, 92, 62))
    rock = ft("Rockwell.ttc", 44, 2)
    for k, (teks, jarak) in enumerate(p["papan"]):
        kanan = k % 2 == 0
        y = 200 + k * 170
        bw_, bh_ = 430, 110
        wood = kayu(bw_ + 60, bh_, np.random.default_rng(5450 + i * 4 + k), (186, 140, 92)).convert("RGBA")
        m = Image.new("L", wood.size, 0)
        pts = [(0, 0), (bw_, 0), (bw_ + 60, bh_ / 2), (bw_, bh_), (0, bh_)]
        if not kanan:
            pts = [(bw_ + 60 - x, y_) for x, y_ in pts]
        ImageDraw.Draw(m).polygon(pts, fill=255)
        wood.putalpha(m)
        wd = ImageDraw.Draw(wood)
        tx = 30 if kanan else 90
        f = rock
        batas = bw_ - 50 - wd.textlength(bersih(jarak), font=hn(28, 1)) - 40
        while wd.textlength(bersih(teks).upper(), font=f) > batas:
            f = ft("Rockwell.ttc", f.size - 2, 2)
        wd.text((tx, bh_ / 2), bersih(teks).upper(), font=f, fill=(60, 34, 20), anchor="lm")
        wd.text((tx + bw_ - 50 if kanan else tx + bw_ - 60, bh_ / 2), bersih(jarak), font=hn(28, 1), fill=(80, 50, 30), anchor="rm")
        wood = wood.rotate(rng.uniform(-3, 3), expand=True, resample=Image.BICUBIC)
        x = W / 2 - 10 if kanan else W / 2 + 10 - wood.width
        bayangan(img, wood, (x, y), blur=8, geser=(4, 8), kuat=0.35)
    ayat_bawah(img, p, 1060, H - 60, (30, 50, 30), (110, 60, 30), start=32, stop=22)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(40, 70, 40), anchor="ma")
    return img


# ---------- TAG: label kado ----------

def tag_image(p, i, kado_seed=None):
    rng = np.random.default_rng(5500 + i)
    img = kertas_kado(W, H, i + 1 if kado_seed is None else kado_seed).convert("RGBA")
    tw, th = 720, 1060
    tg = np.zeros((th, tw, 3), np.float32) + np.array([196, 160, 116])
    tg *= (0.9 + 0.14 * render.fbm2d(th, tw, rng, ((6, 1.0), (60, 0.5))))[..., None]
    tag = Image.fromarray(np.clip(tg, 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(m).polygon([(130, 0), (tw - 130, 0), (tw, 130), (tw, th), (0, th), (0, 130)], fill=255)
    tag.putalpha(m)
    d = ImageDraw.Draw(tag)
    d.ellipse((tw / 2 - 40, 50, tw / 2 + 40, 130), fill=(230, 216, 190, 255))
    d.ellipse((tw / 2 - 20, 70, tw / 2 + 20, 110), fill=(0, 0, 0, 0))
    ink = (60, 36, 24)
    d.text((70, 190), "Untuk:", font=tangan(36), fill=(120, 80, 50))
    d.text((200, 180), bersih(p["untuk"]), font=tangan(48), fill=ink)
    d.text((70, 260), "Dari:", font=tangan(36), fill=(120, 80, 50))
    d.text((200, 250), bersih(p["dari"]), font=tangan(48), fill=ink)
    d.line((70, 340, tw - 70, 340), fill=(150, 110, 70), width=2)
    f, lines, size = pas(d, bersih(p["pesan"]), tangan, tw - 140, 260, 50, 32, 1.25)
    y = 370
    for ln in lines:
        d.text((tw / 2, y), ln, font=f, fill=ink, anchor="ma")
        y += size * 1.25
    y += 30
    f2, l2, s2 = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), tw - 140, th - 110 - y, 32, 20, 1.36)
    for ln in l2:
        d.text((tw / 2, y), ln, font=f2, fill=(80, 50, 30), anchor="ma")
        y += s2 * 1.36
    d.text((tw / 2, y + 8), p["ref"], font=hn(26, 1), fill=(130, 40, 30), anchor="ma")
    tag = tag.rotate(4, expand=True, resample=Image.BICUBIC)
    x0, y0 = (W - tag.width) // 2, 220
    d = ImageDraw.Draw(img)
    d.line((W / 2 - 20, 0, W / 2 + 10, y0 + 90), fill=(236, 226, 200), width=8)
    d.line((W / 2 + 40, 0, W / 2 + 10, y0 + 90), fill=(220, 206, 176), width=8)
    bayangan(img, tag, (x0, y0), blur=14, geser=(6, 12), kuat=0.45)
    ImageDraw.Draw(img).text((W - 40, H - 30), "@" + HANDLE, font=hn(22, 10), fill=(255, 236, 200), anchor="rs")
    return img


# ---------- CHART: grafik batang ----------

def chart_image(p, i):
    img = grain(Image.new("RGB", (W, H), (250, 247, 240)), 0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    navy = (28, 40, 76)
    warna = [(232, 112, 90), (240, 180, 70), (90, 170, 130), (90, 130, 220)]
    d.text((70, 70), "INFOGRAFIS", font=hn(24, 1), fill=(232, 112, 90))
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: hn(s, 1), W - 140, 150, 58, 36, 1.15)
    y = 110
    for ln in lines:
        d.text((70, y), ln, font=f, fill=navy)
        y += size * 1.15
    y += 50
    for k, (lab, nilai) in enumerate(p["batang"]):
        d.text((70, y), bersih(lab), font=hn(32, 10), fill=navy)
        d.rounded_rectangle((70, y + 46, W - 70, y + 96), radius=25, fill=(234, 230, 220))
        x1 = 70 + (W - 140) * max(0.04, min(1, nilai / 100))
        d.rounded_rectangle((70, y + 46, x1, y + 96), radius=25, fill=warna[k % 4])
        d.text((min(x1 + 16, W - 160), y + 71), f"{nilai}%", font=hn(30, 1), fill=navy, anchor="lm")
        y += 140
    y += 10
    for ln in wrap(d, bersih(p["catatan"]), georgia(34, True), W - 140):
        d.text((70, y), ln, font=georgia(34, True), fill=(90, 80, 70))
        y += 46
    by = y + 30
    d.rounded_rectangle((60, by, W - 60, H - 80), radius=24, fill=(238, 234, 224))
    ayat_bawah(img, p, by + 30, H - 100, navy, (232, 112, 90), maxw=W - 200, start=30, stop=20)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(150, 146, 136), anchor="ma")
    return img


# ---------- PIXEL: layar game 8-bit ----------

def pixel_image(p, i, natal=False):
    sw, sh, k = 270, 338, 4
    img = Image.new("RGB", (sw, sh), (10, 40, 26) if natal else (16, 14, 40))
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    rng = np.random.default_rng(5600 + i)
    for _ in range(60):
        x, y = rng.integers(0, sw), rng.integers(0, 200)
        d.point((int(x), int(y)), fill=(200, 200, 255))
    fb = ft("/System/Library/Fonts/Menlo.ttc", 12, 1)
    fs = ft("/System/Library/Fonts/Menlo.ttc", 9, 1)
    d.text((sw / 2, 10), bersih(p["level"]).upper()[:22], font=fb, fill=(255, 220, 90), anchor="ma")
    for h_ in range(5):  # nyawa
        x = 12 + h_ * 14
        d.rectangle((x, 32, x + 9, 39), fill=(230, 60, 80))
        d.rectangle((x + 2, 30, x + 3, 31), fill=(230, 60, 80))
        d.rectangle((x + 6, 30, x + 7, 31), fill=(230, 60, 80))
    d.text((sw - 12, 30), "SKOR 2026", font=fs, fill=(220, 220, 240), anchor="ra")
    if natal:  # salju & pohon Natal 8-bit
        for _ in range(80):
            x, y = rng.integers(0, sw), rng.integers(0, 150)
            d.point((int(x), int(y)), fill=(255, 255, 255))
        for r_ in range(6):
            d.rectangle((236 - r_ * 3, 104 + r_ * 7, 244 + r_ * 3, 110 + r_ * 7), fill=(40, 150, 70))
        d.rectangle((238, 146, 242, 150), fill=(120, 70, 40))
        for x, y, c in ((234, 116, (255, 80, 80)), (246, 125, (255, 220, 80)), (232, 135, (90, 160, 255)), (248, 140, (255, 80, 80))):
            d.point((x, y), fill=c)
    d.rectangle((0, 150, sw, 158), fill=(240, 244, 255) if natal else (60, 160, 80))  # tanah + tokoh
    d.rectangle((0, 158, sw, 168), fill=(110, 70, 40))
    px, py = 60, 126
    for (dx, dy, w_, h2, c) in [(4, 0, 8, 6, (250, 210, 170)), (2, 6, 12, 10, (60, 120, 220)), (4, 16, 3, 8, (40, 40, 60)), (9, 16, 3, 8, (40, 40, 60)), (3, -3, 10, 4, (90, 60, 30))]:
        d.rectangle((px + dx, py + dy, px + dx + w_, py + dy + h2), fill=c)
    sx = 200  # bintang tujuan
    for dx, dy in [(0, -6), (-6, 0), (6, 0), (0, 6), (0, 0), (-3, -3), (3, -3), (-3, 3), (3, 3)]:
        d.rectangle((sx + dx - 1, 120 + dy - 1, sx + dx + 1, 120 + dy + 1), fill=(255, 230, 80))
    for x in range(80, 190, 10):
        d.rectangle((x, 132, x + 3, 135), fill=(255, 230, 80))
    d.text((12, 50), "MISI:", font=fb, fill=(120, 220, 255))
    y = 66
    for ln in wrap(d, bersih(p["misi"]), fs, sw - 24)[:4]:
        d.text((12, y), ln, font=fs, fill=(240, 240, 250))
        y += 11
    d.text((12, 176), "INVENTARIS:", font=fs, fill=(120, 220, 255))
    for j, it in enumerate(p["item"][:3]):
        x = 12 + j * 86
        d.rectangle((x, 189, x + 78, 207), outline=(255, 220, 90))
        d.text((x + 39, 198), bersih(it)[:12], font=fs, fill=(255, 255, 255), anchor="mm")
    d.rectangle((6, 216, sw - 6, sh - 22), fill=(0, 0, 0), outline=(255, 255, 255))
    vl = wrap(d, tanpa_kutip(p["ayat"]), fs, sw - 26)
    y = 222
    for ln in vl[:8]:
        d.text((13, y), ln, font=fs, fill=(255, 255, 255))
        y += 11
    d.text((13, min(y + 2, sh - 34)), p["ref"].upper(), font=fs, fill=(255, 220, 90))
    d.text((sw / 2, sh - 16), "TEKAN START  -  @" + HANDLE.upper(), font=fs, fill=(150, 150, 190), anchor="ma")
    big = img.resize((sw * k, sh * k), Image.NEAREST)
    return big.crop((0, 0, W, H))


# ---------- REKAP: rekap tahunan ----------

def rekap_image(p, i):
    pal = [((110, 50, 200), (250, 120, 90)), ((20, 120, 110), (40, 40, 120)), ((220, 60, 100), (250, 170, 60))][i % 3]
    img = grain(gradasi(W, H, *pal), 0.04).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.ellipse((W - 420, -180, W + 200, 440), fill=(255, 255, 255, 40))
    ld.ellipse((-260, H - 520, 360, H + 100), fill=(0, 0, 0, 40))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((70, 70, 360, 124), radius=27, fill=(255, 255, 255, 255))
    d.text((215, 97), "REKAP 2026", font=hn(28, 1), fill=pal[0], anchor="mm")
    fa = hn(300, 9)
    while d.textlength(bersih(p["angka"]), font=fa) > W - 140:
        fa = hn(fa.size - 10, 9)
    d.text((70, 150), bersih(p["angka"]), font=fa, fill=(255, 255, 255))
    y = 150 + fa.size * 1.02
    for ln in wrap(d, bersih(p["label"]), hn(52, 1), W - 140):
        d.text((70, y), ln, font=hn(52, 1), fill=(255, 255, 255))
        y += 62
    y += 30
    for pt in p["poin"]:
        d.ellipse((74, y + 12, 94, y + 32), fill=(255, 230, 120))
        for k, ln in enumerate(wrap(d, bersih(pt), hn(36, 10), W - 210)):
            d.text((120, y), ln, font=hn(36, 10), fill=(255, 255, 255))
            y += 46
        y += 16
    ayat_bawah(img, p, max(y + 30, 960), H - 60, (255, 255, 255), (255, 230, 120), start=30, stop=20)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(255, 255, 255, 200), anchor="ma")
    return img


# ---------- VINYL (Reels): piringan hitam ----------

def piringan(r, judul, penyanyi, seed):
    S = 2 * r
    disc = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(disc)
    d.ellipse((0, 0, S, S), fill=(18, 18, 20, 255))
    for rr in range(r - 10, int(r * 0.36), -6):
        g = 26 + (rr % 12)
        d.ellipse((r - rr, r - rr, r + rr, r + rr), outline=(g, g, g + 2, 255), width=2)
    lr = int(r * 0.34)
    col = [(200, 60, 60), (60, 120, 180), (220, 170, 60), (90, 150, 90)][seed % 4]
    d.ellipse((r - lr, r - lr, r + lr, r + lr), fill=col + (255,))
    f = hn(30, 1)
    while d.textlength(judul, font=f) > lr * 1.6:
        f = hn(f.size - 2, 1)
    d.text((r, r - 40), judul, font=f, fill=(255, 255, 255, 255), anchor="mm")
    d.text((r, r + 40), penyanyi, font=hn(22, 10), fill=(255, 255, 255, 220), anchor="mm")
    d.ellipse((r - 10, r - 10, r + 10, r + 10), fill=(230, 230, 230, 255))
    kil = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(kil).pieslice((0, 0, S, S), 200, 230, fill=(255, 255, 255, 30))
    return disc, kil


def vinyl_reel(p, idx, mod=MOD, seconds=12):
    rel = f"reels/{mod}/vinyl{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    bg = grain(gradasi(RW, RH, (244, 230, 210), (214, 186, 160)), 0.05).convert("RGBA")
    d = ImageDraw.Draw(bg)
    d.text((RW / 2, 230), "SEDANG DIPUTAR", font=hn(30, 1), fill=(150, 90, 60), anchor="ma")
    d.text((RW / 2, 280), bersih(p["judul"]), font=georgia(62, True), fill=(60, 36, 28), anchor="ma")
    d.text((RW / 2, 364), bersih(p["penyanyi"]), font=hn(34, 10), fill=(120, 80, 60), anchor="ma")
    r, cx, cy = 340, RW / 2 - 40, 820
    disc, kil = piringan(r, bersih(p["judul"]), bersih(p["penyanyi"]), idx)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, lines, size = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 200, 380, 40, 26, 1.36)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        rot = disc.rotate(-t * 200, resample=Image.BICUBIC)
        bayangan(frame, rot, (cx - r, cy - r), blur=24, geser=(0, 18), kuat=0.4)
        frame.alpha_composite(kil, (int(cx - r), int(cy - r)))
        d = ImageDraw.Draw(frame)
        ax, ay = cx + r + 40, cy - r + 40  # lengan pemutar
        d.ellipse((ax - 40, ay - 40, ax + 40, ay + 40), fill=(190, 190, 196))
        d.line((ax, ay, cx + 150, cy + 120), fill=(200, 200, 206), width=16)
        d.rectangle((cx + 120, cy + 100, cx + 190, cy + 150), fill=(60, 60, 66))
        y = 1250
        for k, ln in enumerate(lines):
            a = 1.0 if k == 0 else ease((t - 0.6 - k * 0.9) / 0.5)
            if a > 0:
                d.text((RW / 2, y + (1 - a) * 12), ln, font=f, fill=(60, 36, 28, int(255 * a)), anchor="ma")
            y += size * 1.36
        a = ease((t - 0.6 - len(lines) * 0.9) / 0.5)
        if a > 0:
            d.text((RW / 2, y + 14), p["ref"], font=hn(32, 1), fill=(160, 70, 50, int(255 * a)), anchor="ma")
            d.text((RW / 2, y + 70), "@" + HANDLE, font=hn(26, 10), fill=(140, 100, 80, int(255 * a)), anchor="ma")
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- SALJU (Reels): salju di desa malam ----------

def salju_reel(p, idx, mod=MOD, seconds=12, emas=False):
    rel = f"reels/{mod}/salju{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(5700 + idx)
    bg = (gradasi(RW, RH, (40, 22, 12), (96, 58, 26)) if emas else gradasi(RW, RH, (14, 22, 52), (40, 50, 96))).convert("RGBA")
    d = ImageDraw.Draw(bg)
    for _ in range(140):
        x, y, s = rng.uniform(0, RW), rng.uniform(0, 900), rng.uniform(1, 2.4)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 240, int(rng.uniform(100, 230))))
    d.ellipse((840, 640, 940, 740), fill=(250, 244, 220))
    gy = 1500
    pts = [(0, RH)] + [(x, gy - 40 * math.sin(x / 260) - 20) for x in range(0, RW + 20, 20)] + [(RW, RH)]
    d.polygon(pts, fill=(226, 232, 246))
    for k in range(7):  # rumah kecil dengan jendela hangat
        x = 60 + k * 150 + rng.uniform(-20, 20)
        hw_, hh_ = rng.uniform(90, 130), rng.uniform(80, 120)
        base = gy - 40 * math.sin(x / 260) - 10
        d.rectangle((x, base - hh_, x + hw_, base), fill=(40, 36, 54))
        d.polygon([(x - 14, base - hh_), (x + hw_ / 2, base - hh_ - 60), (x + hw_ + 14, base - hh_)], fill=(236, 240, 250))
        d.rectangle((x + hw_ * 0.3, base - hh_ * 0.6, x + hw_ * 0.55, base - hh_ * 0.3), fill=(255, 200, 110))
    flakes = np.column_stack([rng.uniform(0, RW, 260), rng.uniform(-RH, RH, 260), rng.uniform(2, 7, 260), rng.uniform(40, 120, 260), rng.uniform(0, 6.28, 260)])
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    teks = Image.new("RGBA", (RW, 520), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks)
    td.text((RW / 2, 0), bersih(p["judul"]), font=georgia(60, True), fill=(250, 236, 200), anchor="ma")
    y = 100
    for ln in wrap(td, bersih(p["teks"]), georgia(40), RW - 200):
        td.text((RW / 2, y), ln, font=georgia(40), fill=(236, 240, 250), anchor="ma")
        y += 54
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 330, 36, 24, 1.36)
    ayat = Image.new("RGBA", (RW, 460), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    ad.rounded_rectangle((70, 0, RW - 70, len(vl) * vs * 1.36 + 130), radius=30, fill=(10, 16, 40, 150))
    y = 30
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(236, 238, 248), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 10), p["ref"], font=hn(30, 1), fill=(250, 210, 140), anchor="ma")
    ad.text((RW / 2, y + 60), "@" + HANDLE, font=hn(24, 10), fill=(170, 180, 210), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        frame.alpha_composite(teks, (0, 230))
        if t >= 2.0:
            frame.alpha_composite(fade(ayat, ease((t - 2.0) / 0.8)), (0, 820))
        lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for x, y0, r, v, ph in flakes:
            y = (y0 + v * t * 1.6) % (RH + 40) - 20
            xx = x + 18 * math.sin(t * 1.3 + ph)
            ld.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 214, 120, 220) if emas else (255, 255, 255, 210))
        frame.alpha_composite(lay)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def alkitabmalam_image(p, i):
    img = gaya_w6.alkitab_image(p, i).convert("RGB")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = W * 0.78, H * 0.12
    light = 0.32 + 0.95 * np.exp(-(np.hypot((xx - lx) / W, (yy - ly) / H) / 0.62) ** 2)
    a = np.asarray(img).astype(np.float32) * light[..., None] * np.array([1.08, 0.98, 0.8])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


SIMPLE = {
    # baru
    "FLIPCLOCK": flipclock_image, "KACAPATRI": kacapatri_image, "SCROLL": scroll_image, "HPJADUL": hpjadul_image,
    "PHOTOBOOTH": photobooth_image, "SIGNPOST": signpost_image, "TAG": tag_image, "CHART": chart_image, "PIXEL": pixel_image,
    "REKAP": rekap_image,
    # lama
    "GLOBE": gaya_w9.globe_image, "KORAN": gaya_w8.koran_image, "TIKET": gaya_w7.tiket_image, "POPUP": gaya_w7.popup_image,
    "STICKY": gaya_w8.sticky_image, "KAMUS": gaya_w7.kamus_image, "RESEP": gaya_w9.resep_image, "UNDANGAN": gaya_w9.undangan_image,
    "KASET": gaya_w9.kaset_image, "LILIN": gaya_w8.lilin_image,
    # mix
    "ORNAMENSALJU": lambda p, i: gaya_w8.ornamen_image(p, i, latar=salju_latar(W, H, 5800 + i)),
    "LETTERPUTIH": lambda p, i: gaya_w8.letter_image(p, i, putih=True),
    "CUACASALJU": gaya_w7.cuaca_image,
    "POLAROIDLINEN": lambda p, i: gaya_w7.polaroid_image(p, i, latar=linen_latar(W, H, 5900 + i)),
    "PLAYERTERANG": lambda p, i: gaya_w7.player_image(p, i, terang=True),
    "ALKITABMALAM": alkitabmalam_image,
    "NAMAEMAS": lambda p, i: gaya_w9.nama_image(p, i, emas=True),
    "DOAFOTO": lambda p, i: gaya_w6.doa_image(p, i, foto=foto_warna(("fajar", "laut", "bintang")[i % 3], W, H, seed=6000 + i)),
    "MENUPUTIH": lambda p, i: gaya_w8.menu_image(p, i, putih=True),
    "TOPLESMALAM": lambda p, i: gaya_w10.toples_image(p, i, malam=True),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
REELS = {"VINYL": (vinyl_reel, "vinyl"), "SALJU": (salju_reel, "salju"), "SEARCH": (gaya_w8.search_reel, "search"),
         "NEON": (gaya_w7.neon_reel, "neon"), "CHATNATAL": (lambda p, i, mod: gaya_w7.chat_reel(p, i, mod, natal=True), "chat"),
         "FLIPEMAS": (lambda p, i, mod: gaya_w8.flip_reel(p, i, mod, emas=True), "flip")}


def render_week(mod=MOD, simple=None, reels=None, mulai=MULAI):
    simple, reels = simple or SIMPLE, reels or REELS
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            p = getattr(t, fmt)[idx]
            if fmt in simple:
                out[(hari, slot)] = ([save(simple[fmt](konteks(p, hari, slot, mulai), idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt in reels:
                rel = f"reels/{mod}/{reels[fmt][1]}{idx + 1}.mp4"
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], p["caption"])
    return out


def render_reels(mod=MOD, reels=None, mulai=MULAI):
    reels = reels or REELS
    t = importlib.import_module(f"konten.{mod}")
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt in reels:
                rel = reels[fmt][0](konteks(getattr(t, fmt)[idx], hari, slot, mulai), idx, mod)
                tambah_musik(rel)
                print(rel, flush=True)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
