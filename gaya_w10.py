"""Akun Tenang - minggu 10 (konten/tenang_w10.py), minggu Adven I: 36 gaya yang diacak tiap hari.
BARU : KRANS (Reels krans Adven), JAMPASIR (Reels jam pasir), MAJALAH (sampul majalah), TOPLES (toples catatan), RASI (rasi bintang),
       GARIS (garis waktu), FILM (poster film "segera"), TELEGRAM, TANYA (kotak tanya-jawab), KOMPAS, UTAS (utas 2 slide),
       KALADVEN (kalender Adven, hitung mundur).
LAMA : ALKITAB, DOA, CUACA, CHAT, POLAROID, PLAYER, LETTER, MENU, FLIP, NAMA, JENDELA, ORNAMEN.
MIX  : NEONLETTER (Reels papan huruf neon), GOSOKNATAL (Reels kartu gosok kertas kado), KALENDERFOTO (kalender sobek + lampu Natal),
       KORANMALAM (koran edisi malam), STRUKNATAL, TIKETBINTANG, POPUPNATAL, KAMUSFOTO, CATATANGELAP (mode gelap),
       KETIKLILIN (mesin tik + cahaya lilin), RESEPNATAL (taplak kotak-kotak), PETAMALAM (peta mode malam).

  python3 gaya_w10.py [reels]
"""
import datetime as dt
import importlib
import math
import sys
from functools import partial

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import cerita
import config
import gaya_w6
import gaya_w7
import gaya_w8
import gaya_w9
import render
from gaya_w6 import cover, foto_warna, georgia, hn, tambah_musik
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tangan, tanpa_kutip, vintage
from gaya_w8 import HARI, halftone, kayu
from gaya_w9 import EMAS, ayat_bawah, kertas_kado
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w10"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2026, 11, 29)
BULAN = {11: "November", 12: "Desember"}


def bokeh(w, h, seed, warna=((255, 196, 110), (255, 120, 90), (140, 220, 140), (255, 230, 170))):
    rng = np.random.default_rng(seed)
    img = gradasi(w, h, (40, 22, 18), (12, 8, 8)).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(int(w * h / 18000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(14, 60)
        d.ellipse((x - r, y - r, x + r, y + r), fill=warna[int(rng.integers(len(warna)))] + (int(rng.uniform(50, 130)),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    return img


def kotak_kotak(w, h, col=(196, 40, 50)):
    """Taplak kotak-kotak (gingham)."""
    x = (np.arange(w) // 60) % 2
    y = (np.arange(h) // 60) % 2
    a = (x[None, :] + y[:, None]).astype(np.float32) / 2  # 0, .5, 1
    c = np.array(col, np.float32)
    arr = 255 - (255 - c) * (0.15 + 0.85 * a[..., None]) * 0.9
    return grain(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), 0.05)


def bintang5(d, cx, cy, r, col):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


# ================= BARU =================

# ---------- MAJALAH: sampul majalah ----------

def majalah_image(p, i, latar=None):
    ph = (latar.copy() if latar is not None else foto_warna(p["foto"], W, H, seed=3200 + i)).convert("RGB")
    a = np.asarray(ph).astype(np.float32)
    yy = np.linspace(0, 1, H)[:, None, None]
    a *= 1 - 0.55 * np.clip((0.3 - yy) / 0.3, 0, 1) - 0.7 * np.clip((yy - 0.55) / 0.45, 0, 1)
    img = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    white, kuning = (255, 255, 255, 255), (255, 214, 90, 255)
    d.text((W / 2, 40), f"EDISI ADVEN  ·  DESEMBER 2026  ·  @{HANDLE.upper()}", font=hn(22, 1), fill=white, anchor="ma")
    d.text((W / 2, 70), "TENANG", font=ft("Didot.ttc", 230, 2), fill=white, anchor="ma")
    y = 360
    for b in p["berita"]:
        d.rectangle((60, y + 6, 70, y + 40), fill=kuning)
        for ln in wrap(d, bersih(b), hn(34, 1), 760)[:2]:
            d.text((90, y), ln, font=hn(34, 1), fill=white)
            y += 42
        y += 26
    f, lines, size = pas(d, bersih(p["judul_utama"]).upper(), lambda s: hn(s, 9), W - 120, 250, 124, 64, 0.95)
    y = max(y + 30, 860 - (len(lines) - 1) * size * 0.95)
    for ln in lines:
        d.text((60, y), ln, font=f, fill=white)
        y += size * 0.95
    y += 16
    for ln in wrap(d, bersih(p["sub"]), georgia(34, True), W - 140):
        d.text((60, y), ln, font=georgia(34, True), fill=kuning)
        y += 44
    y += 16
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: hn(s, 2), W - 360, H - 70 - y - 30, 28, 20, 1.3)
    for ln in lines:
        d.text((60, y), ln, font=f, fill=(235, 235, 235, 255))
        y += size * 1.3
    d.text((60, y + 6), p["ref"], font=hn(26, 1), fill=white)
    d.rectangle((W - 230, H - 150, W - 60, H - 50), fill=white)
    gaya_w7.barcode(d, W - 220, H - 140, 150, 60, np.random.default_rng(i), (20, 20, 20))
    d.text((W - 145, H - 72), "29-11-2026", font=hn(16, 10), fill=(20, 20, 20), anchor="mm")
    return img


# ---------- TOPLES: toples catatan ----------

def toples_image(p, i, malam=False):
    rng = np.random.default_rng(3300 + i)
    img = grain(gradasi(W, H, (30, 34, 60), (16, 18, 34)) if malam else gradasi(W, H, (246, 232, 222), (236, 214, 200)), 0.04).convert("RGBA")
    if malam:  # lampu tumbler di dinding
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        pts = [(x, 90 + 60 * math.sin(x / 170)) for x in range(-20, W + 40, 60)]
        ld.line(pts, fill=(60, 50, 40, 255), width=3)
        for x, y in pts:
            ld.ellipse((x - 11, y, x + 11, y + 26), fill=(255, 210, 120, 255))
        glow = lay.filter(ImageFilter.GaussianBlur(14))
        img.alpha_composite(glow)
        img.alpha_composite(glow)
        img.alpha_composite(lay)
        hal = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(hal).ellipse((W / 2 - 330, 200, W / 2 + 330, 800), fill=(255, 190, 110, 70))
        img.alpha_composite(hal.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 860, W, H), fill=(70, 46, 34) if malam else (196, 150, 110))
    d.rectangle((0, 860, W, 872), fill=(50, 32, 24) if malam else (170, 126, 90))
    jx0, jy0, jw, jh = 310, 140, 460, 600
    isi = Image.new("RGBA", (jw, jh), (0, 0, 0, 0))
    idr = ImageDraw.Draw(isi)
    warna = [(255, 236, 140), (255, 190, 200), (180, 220, 255), (200, 236, 180), (255, 210, 160), (250, 250, 240)]
    for _ in range(140):
        x, y = rng.uniform(20, jw - 20), rng.uniform(jh * 0.28, jh - 30)
        s = rng.uniform(34, 56)
        n = Image.new("RGBA", (int(s), int(s * 0.6)), warna[int(rng.integers(len(warna)))] + (255,))
        ImageDraw.Draw(n).line((0, s * 0.3, s, s * 0.3), fill=(0, 0, 0, 40), width=2)
        n = n.rotate(rng.uniform(0, 360), expand=True, resample=Image.BICUBIC)
        comp(isi, n, (x - n.width / 2, y - n.height / 2))
    m = Image.new("L", (jw, jh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 40, jw, jh), radius=70, fill=255)
    jar = Image.new("RGBA", (jw, jh), (0, 0, 0, 0))
    jar.paste(isi, (0, 0), m)
    kaca = Image.new("RGBA", (jw, jh), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kaca)
    kd.rounded_rectangle((0, 40, jw, jh), radius=70, fill=(255, 255, 255, 40), outline=(255, 255, 255, 170), width=5)
    kd.rounded_rectangle((40, 90, 70, jh - 80), radius=15, fill=(255, 255, 255, 110))
    kd.rounded_rectangle((60, 0, jw - 60, 56), radius=12, fill=(190, 150, 70, 255))
    for x in range(70, jw - 60, 14):
        kd.line((x, 6, x, 50), fill=(160, 120, 50, 255), width=3)
    jar.alpha_composite(kaca)
    lab = Image.new("RGBA", (300, 110), (214, 186, 140, 255))
    ld = ImageDraw.Draw(lab)
    ld.rectangle((6, 6, 293, 103), outline=(150, 120, 80, 255), width=2)
    fl = tangan(38)
    while ld.textlength(bersih(p["label"]), font=fl) > 270:
        fl = tangan(fl.size - 2)
    ld.text((150, 55), bersih(p["label"]), font=fl, fill=(70, 50, 30), anchor="mm")
    jar.alpha_composite(lab.rotate(-3, expand=True, resample=Image.BICUBIC), (80, 250))
    bayangan(img, jar, (jx0, jy0), blur=20, geser=(10, 16), kuat=0.3)
    note = Image.new("RGBA", (820, 300), (255, 250, 228, 255))
    nd = ImageDraw.Draw(note)
    nd.line((0, 150, 820, 150), fill=(0, 0, 0, 25), width=2)
    f, lines, size = pas(nd, bersih(p["catatan"]), tangan, 740, 230, 44, 28, 1.25)
    y = 150 - len(lines) * size * 1.25 / 2
    for ln in lines:
        nd.text((410, y), ln, font=f, fill=(40, 50, 100), anchor="ma")
        y += size * 1.25
    note = note.rotate(-3, expand=True, resample=Image.BICUBIC)
    bayangan(img, note, ((W - note.width) // 2, 700), blur=14, geser=(6, 12), kuat=0.35)
    ayat_bawah(img, p, 1060, H - 50, (240, 226, 206) if malam else (60, 44, 34), (250, 196, 120) if malam else (150, 70, 50), start=30, stop=20)
    ImageDraw.Draw(img).text((W - 40, H - 16), "@" + HANDLE, font=hn(18, 10), fill=(110, 80, 60), anchor="rs")
    return img


# ---------- RASI: rasi bintang ----------

BENTUK = [[(260, 330), (560, 250), (820, 400), (700, 690), (330, 640)],
          [(220, 520), (420, 300), (620, 520), (820, 300), (900, 620)],
          [(540, 250), (300, 460), (430, 720), (650, 720), (780, 460)]]


def rasi_image(p, i):
    rng = np.random.default_rng(3400 + i)
    img = gradasi(W, H, (8, 12, 34), (26, 22, 60)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(420):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 2.2)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, int(rng.uniform(60, 220))))
    pts = [(x + rng.uniform(-20, 20), y + 60 + rng.uniform(-20, 20)) for x, y in BENTUK[i % 3]]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.line(pts + [pts[0]], fill=(170, 200, 255, 150), width=3)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for x, y in pts:
        gd.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(200, 220, 255, 120))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    for k, ((x, y), lab) in enumerate(zip(pts, p["bintang"])):
        bintang5(d, x, y, 16 if k else 22, (255, 250, 220, 255))
        tw = d.textlength(bersih(lab), font=hn(28, 10))
        tx = min(max(x + 30, 40), W - 40 - tw) if x < W - 260 else x - 30 - tw
        d.text((tx, y - 14), bersih(lab), font=hn(28, 10), fill=(190, 210, 255, 255))
    d.text((W / 2, 80), bersih(p["judul"]), font=georgia(50, True), fill=(250, 240, 210), anchor="ma")
    d.line((W / 2 - 60, 160, W / 2 + 60, 160), fill=(120, 140, 200), width=2)
    ayat_bawah(img, p, 900, H - 60, (220, 226, 245), (250, 220, 150), start=34, stop=22)
    d.text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(120, 130, 170), anchor="ma")
    return img


# ---------- GARIS: garis waktu ----------

def garis_image(p, i):
    img = grain(Image.new("RGB", (W, H), (248, 245, 238)), 0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    navy = (24, 36, 70)
    d.text((70, 80), "GARIS WAKTU", font=hn(26, 1), fill=EMAS)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: hn(s, 1), W - 140, 150, 60, 40, 1.12)
    y = 124
    for ln in lines:
        d.text((70, y), ln, font=f, fill=navy)
        y += size * 1.12
    top = y + 50
    n = len(p["titik"])
    gap = (920 - top) / (n - 1) if n > 1 else 0
    d.line((130, top, 130, top + gap * (n - 1)), fill=(200, 196, 186), width=6)
    for k, (waktu, teks) in enumerate(p["titik"]):
        cy = top + k * gap
        last = k == n - 1
        r = 22 if last else 16
        d.ellipse((130 - r, cy - r, 130 + r, cy + r), fill=EMAS if last else (255, 255, 255), outline=navy, width=5)
        d.text((180, cy - 26), bersih(waktu), font=hn(34, 1), fill=EMAS if last else navy)
        yy = cy + 16
        for ln in wrap(d, bersih(teks), hn(32, 0), W - 260)[:2]:
            d.text((180, yy), ln, font=hn(32, 0), fill=(60, 64, 76))
            yy += 40
    box_y = 1000
    d.rounded_rectangle((60, box_y, W - 60, H - 70), radius=24, fill=(236, 230, 216))
    ayat_bawah(img, p, box_y + 34, H - 90, navy, EMAS, maxw=W - 200, start=30, stop=20)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(150, 146, 136), anchor="ma")
    return img


# ---------- FILM: poster "segera" ----------

def film_image(p, i):
    ph = foto_warna(p["foto"], W, H, seed=3500 + i).convert("RGB")
    a = np.asarray(ph).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True) / 255
    a = np.array([20, 60, 70], np.float32) * (1 - lum) + np.array([255, 180, 110], np.float32) * lum  # teal-oranye
    yy = np.linspace(0, 1, H)[:, None, None]
    a *= 0.95 - 0.75 * np.clip((yy - 0.45) / 0.55, 0, 1)
    img = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.08).convert("RGBA")
    d = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    f, lines, size = pas(d, bersih(p["tagline"]).upper(), lambda s: hn(s, 10), W - 160, 100, 30, 20, 1.3)
    y = 70
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=white, anchor="ma")
        y += size * 1.3
    ft_ = hn(170, 9)
    while d.textlength(bersih(p["judul"]).upper(), font=ft_) > W - 100:
        ft_ = hn(ft_.size - 6, 9)
    d.text((W / 2, 760), bersih(p["judul"]).upper(), font=ft_, fill=white, anchor="ms")
    d.text((W / 2, 800), bersih(p.get("status", "SEGERA")).upper() + "  ·  " + bersih(p["tanggal"]), font=hn(40, 1), fill=(255, 200, 120, 255), anchor="ma")
    y = 880
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 200, 190, 32, 22, 1.34)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(236, 236, 236, 255), anchor="ma")
        y += size * 1.34
    d.text((W / 2, y + 6), p["ref"], font=hn(26, 1), fill=white, anchor="ma")
    fk = hn(22, 4)
    kred = bersih(p["kredit"]).upper()
    y = H - 170
    for ln in wrap(d, kred, fk, W - 200):
        d.text((W / 2, y), ln, font=fk, fill=(200, 200, 200, 255), anchor="ma")
        y += 28
    d.text((W / 2, H - 60), "@" + HANDLE.upper(), font=hn(22, 1), fill=(200, 200, 200, 255), anchor="ma")
    return img


# ---------- TELEGRAM ----------

def telegram_image(p, i, latar=None):
    rng = np.random.default_rng(3600 + i)
    img = (latar.copy() if latar is not None else kayu(W, H, rng, (110, 76, 52))).convert("RGBA")
    fw, fh = 960, 1220
    form = np.zeros((fh, fw, 3), np.float32) + np.array([240, 226, 180])
    form *= (0.94 + 0.08 * render.fbm2d(fh, fw, rng, ((5, 1.0), (40, 0.4))))[..., None]
    form = Image.fromarray(np.clip(form, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(form)
    ink = (90, 50, 40)
    tb = lambda s: ft("Times New Roman Bold.ttf", s)
    d.text((fw / 2, 50), "T E L E G R A M", font=tb(64), fill=ink, anchor="ma")
    d.line((60, 140, fw - 60, 140), fill=ink, width=3)
    d.line((60, 148, fw - 60, 148), fill=ink, width=1)
    cour = ft("Courier New Bold.ttf", 34)
    rows = [("DARI", bersih(p["dari"]).upper()), ("UNTUK", bersih(p["untuk"]).upper()), ("TANGGAL", p.get("_tgl_struk", "29/11/2026"))]
    for k, (lab, val) in enumerate(rows):
        y = 180 + k * 64
        d.text((70, y), lab + ":", font=tb(28), fill=ink)
        d.line((240, y + 40, fw - 70, y + 40), fill=(150, 110, 90), width=1)
        d.text((250, y + 2), val, font=cour, fill=(30, 30, 30))
    y = 400
    for ln in wrap(d, bersih(p["isi"]).upper(), cour, fw - 220):  # pita kertas tempel
        strip = Image.new("RGBA", (int(d.textlength(ln, font=cour) + 40), 54), (252, 250, 244, 255))
        ImageDraw.Draw(strip).text((20, 8), ln, font=cour, fill=(25, 25, 25))
        strip = strip.rotate(rng.uniform(-0.6, 0.6), expand=True, resample=Image.BICUBIC)
        comp(form, strip, (90, y))
        y += 66
    d = ImageDraw.Draw(form)
    y += 24
    d.line((60, y, fw - 60, y), fill=ink, width=1)
    y += 26
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: ft("Courier New.ttf", s), fw - 160, fh - 130 - y, 30, 20, 1.36)
    for ln in lines:
        d.text((80, y), ln, font=f, fill=(40, 40, 40))
        y += size * 1.36
    d.text((80, y + 6), p["ref"].upper(), font=ft("Courier New Bold.ttf", 30), fill=(40, 40, 40))
    cx, cy = fw - 170, fh - 150  # cap "DITERIMA"
    cap = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.ellipse((10, 10, 250, 250), outline=(180, 40, 40, 200), width=8)
    cd.ellipse((34, 34, 226, 226), outline=(180, 40, 40, 160), width=3)
    cd.text((130, 115), "DITERIMA", font=tb(34), fill=(180, 40, 40, 210), anchor="mm")
    cd.text((130, 160), "dengan sukacita", font=ft("Times New Roman Italic.ttf", 22), fill=(180, 40, 40, 200), anchor="mm")
    comp(form, cap.rotate(-14, resample=Image.BICUBIC), (cx - 130, cy - 130))
    ImageDraw.Draw(form).text((60, fh - 50), "@" + HANDLE, font=hn(20, 10), fill=(130, 100, 80))
    form = form.rotate(-1.2, expand=True, resample=Image.BICUBIC)
    bayangan(img, form, ((W - form.width) // 2, (H - form.height) // 2), blur=20, geser=(8, 16), kuat=0.5)
    return img


# ---------- TANYA: kotak tanya-jawab ----------

TANYA_WARNA = [((120, 80, 220), (240, 110, 160)), ((250, 130, 70), (240, 70, 110)), ((40, 150, 160), (90, 90, 200))]


def tanya_image(p, i):
    img = grain(gradasi(W, H, *TANYA_WARNA[i % 3]), 0.04).convert("RGBA")
    white = (255, 255, 255, 255)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fq, ql, qs = pas(probe, bersih(p["tanya"]), lambda s: hn(s, 1), 760, 220, 44, 30, 1.25)
    bh = int(110 + len(ql) * qs * 1.25 + 50)
    box = Image.new("RGBA", (860, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 0, 860, bh), radius=40, fill=white)
    bd.rounded_rectangle((0, 0, 860, 90), radius=40, fill=(30, 30, 40, 255))
    bd.rectangle((0, 50, 860, 90), fill=(30, 30, 40, 255))
    bd.text((430, 45), "Tanya apa saja", font=hn(34, 1), fill=white, anchor="mm")
    y = 120
    for ln in ql:
        bd.text((430, y), ln, font=fq, fill=(30, 30, 40), anchor="ma")
        y += qs * 1.25
    bayangan(img, box, ((W - 860) // 2, 90), blur=20, geser=(0, 14), kuat=0.25)
    d = ImageDraw.Draw(img)
    y = 90 + bh + 60
    fa, al, asz = pas(d, bersih(p["jawab"]), lambda s: hn(s, 10), W - 160, 460, 42, 28, 1.3)
    for ln in al:
        d.text((80, y), ln, font=fa, fill=white)
        y += asz * 1.3
    y += 30
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 220, H - 110 - y - 60, 32, 20, 1.34)
    card = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((60, y - 20, W - 60, y + len(lines) * size * 1.34 + 70), radius=26, fill=(255, 255, 255, 60))
    img.alpha_composite(card)
    d = ImageDraw.Draw(img)
    for ln in lines:
        d.text((100, y), ln, font=f, fill=white)
        y += size * 1.34
    d.text((100, y + 6), p["ref"], font=hn(28, 1), fill=white)
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(24, 10), fill=(255, 255, 255, 200), anchor="ma")
    return img


# ---------- KOMPAS ----------

def kompas_image(p, i):
    rng = np.random.default_rng(3700 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array([232, 218, 186])
    base *= (0.9 + 0.14 * render.fbm2d(H, W, rng, ((4, 1.0), (30, 0.5))))[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for k in range(9):  # garis peta samar
        pts = [(x, 200 + k * 130 + 40 * math.sin(x / 140 + k)) for x in range(0, W + 20, 20)]
        d.line(pts, fill=(190, 170, 130, 255), width=2)
    d.text((W / 2, 70), bersih(p["judul"]), font=georgia(50, True), fill=(80, 50, 30), anchor="ma")
    cx, cy, R = W / 2, 560, 330

    def badan(dd, k):
        S = 2 * R * k
        c = S / 2
        for j in range(30):
            t = j / 30
            col = tuple(int(v) for v in np.array([150, 110, 50]) * (1 - t) + np.array([230, 196, 120]) * t)
            r = c - j * k
            dd.ellipse((c - r, c - r, c + r, c + r), fill=col + (255,))
        rf = c - 34 * k
        dd.ellipse((c - rf, c - rf, c + rf, c + rf), fill=(248, 240, 220, 255))
        for a in range(0, 360, 5):
            r1 = rf - (26 if a % 45 == 0 else 14) * k
            ang = math.radians(a)
            dd.line((c + rf * math.cos(ang), c + rf * math.sin(ang), c + r1 * math.cos(ang), c + r1 * math.sin(ang)),
                    fill=(90, 70, 50, 255), width=int((3 if a % 45 == 0 else 1.5) * k))
    comp(img, sprite(2 * R, 2 * R, badan, k=2), (cx - R, cy - R))
    d = ImageDraw.Draw(img)
    for k, (lab, (dx, dy)) in enumerate(zip(p["arah"], [(0, -1), (1, 0), (0, 1), (-1, 0)])):
        f = georgia(34 if k == 0 else 28, k == 0)
        tw = d.textlength(bersih(lab).upper(), font=f)
        rr = R - 100 - (tw / 2 if dx else 0)
        d.text((cx + dx * rr, cy + dy * (R - 100)), bersih(lab).upper(), font=f, fill=(170, 40, 40) if k == 0 else (70, 56, 40), anchor="mm")

    def jarum(dd, k):
        S = 2 * R * k
        c = S / 2
        L = (R - 150) * k
        dd.polygon([(c, c - L), (c + 22 * k, c), (c - 22 * k, c)], fill=(190, 40, 40, 255))
        dd.polygon([(c, c + L), (c + 22 * k, c), (c - 22 * k, c)], fill=(240, 236, 226, 255), outline=(120, 110, 100, 255))
        dd.ellipse((c - 16 * k, c - 16 * k, c + 16 * k, c + 16 * k), fill=(180, 140, 60, 255))
    comp(img, sprite(2 * R, 2 * R, jarum, k=2).rotate(rng.uniform(-6, 6), resample=Image.BICUBIC), (cx - R, cy - R))
    kil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(kil).arc((cx - R + 50, cy - R + 50, cx + R - 50, cy + R - 50), 200, 250, fill=(255, 255, 255, 120), width=14)
    img.alpha_composite(kil.filter(ImageFilter.GaussianBlur(3)))
    ayat_bawah(img, p, 960, H - 60, (70, 50, 34), (170, 40, 40), start=32, stop=20)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(130, 110, 80), anchor="ma")
    return img


# ---------- UTAS: utas 2 slide ----------

def utas_slide(p, posts, nomor, total, dengan_ayat):
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    for start in range(44, 22, -2):
        f = hn(start, 0)
        tinggi = sum(100 + len(wrap(d, bersih(t), f, W - 220)) * start * 1.32 + 50 for t in posts)
        if dengan_ayat:
            tinggi += 60 + len(wrap(d, tanpa_kutip(p["ayat"]), georgia(start - 6, True), W - 260)) * (start - 6) * 1.36 + 110
        if tinggi < H - 160:
            break
    y = 80
    ys = []
    for k, t in enumerate(posts):
        ys.append(y)
        d.ellipse((60, y, 140, y + 80), fill=(24, 24, 28))
        d.text((100, y + 40), "dp", font=hn(34, 1), fill="white", anchor="mm")
        d.text((165, y + 6), "Diam dan Percaya", font=hn(32, 1), fill=(20, 20, 24))
        d.text((165, y + 46), f"@{HANDLE} · {nomor + k}/{total}", font=hn(26, 0), fill=(120, 120, 128))
        yy = y + 100
        for ln in wrap(d, bersih(t), f, W - 220):
            d.text((165, yy), ln, font=f, fill=(20, 20, 24))
            yy += start * 1.32
        y = yy + 50
        if k < len(posts) - 1:
            d.line((100, ys[-1] + 92, 100, y - 8), fill=(214, 214, 220), width=4)
    if dengan_ayat:
        fv = georgia(start - 6, True)
        lines = wrap(d, tanpa_kutip(p["ayat"]), fv, W - 260)
        d.rounded_rectangle((165, y, W - 60, y + len(lines) * (start - 6) * 1.36 + 90), radius=24, fill=(244, 244, 248))
        yy = y + 26
        for ln in lines:
            d.text((195, yy), ln, font=fv, fill=(40, 40, 46))
            yy += (start - 6) * 1.36
        d.text((195, yy + 6), p["ref"], font=hn(28, 1), fill=(20, 20, 24))
    else:
        d.text((W - 60, H - 60), "geser  ›", font=hn(30, 1), fill=(120, 120, 128), anchor="rs")
    return img


def utas_files(p, i, mod):
    ps = p["posting"]
    return [save(utas_slide(p, ps[:2], 1, 4, False), f"{mod}/utas{i + 1}_1.jpg"),
            save(utas_slide(p, ps[2:], 3, 4, True), f"{mod}/utas{i + 1}_2.jpg")]


# ---------- KALADVEN: kalender Adven ----------

PINTU = [(196, 40, 50), (30, 110, 70), (214, 170, 70), (240, 236, 226), (160, 60, 90), (40, 80, 130)]
PINTU_MERAH = [(250, 214, 150), (30, 110, 70), (214, 170, 70), (240, 236, 226), (60, 40, 70), (40, 80, 130)]


def kaladven_image(p, i, merah=False):
    rng = np.random.default_rng(3800 + i)
    img = grain(gradasi(W, H, (150, 26, 38), (78, 10, 20)) if merah else gradasi(W, H, (28, 70, 50), (14, 40, 28)), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(80):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.5, 3.5)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, int(rng.uniform(80, 180))))
    d.text((W / 2, 50), "KALENDER ADVEN", font=hn(30, 1), fill=(236, 206, 140), anchor="ma")
    d.text((W / 2, 96), f"{p['angka']} hari lagi", font=georgia(78, True), fill=(255, 246, 226), anchor="ma")
    cols, rows, cw, ch, gx = 6, 4, 150, 120, 14
    x0 = (W - (cols * cw + (cols - 1) * gx)) / 2
    y0 = 230
    urutan = list(range(1, 25))
    np.random.default_rng(77).shuffle(urutan)  # nomor pintu acak tapi tetap sama tiap hari
    for k, n in enumerate(urutan):
        x = x0 + (k % cols) * (cw + gx)
        y = y0 + (k // cols) * (ch + gx)
        col = (PINTU_MERAH if merah else PINTU)[(n * 7) % len(PINTU)]
        if n < p["pintu"]:
            d.rounded_rectangle((x, y, x + cw, y + ch), radius=10, fill=(20, 30, 24))
            bintang5(d, x + cw / 2, y + ch / 2, 18, (236, 206, 140, 180))
            d.polygon([(x, y), (x + 28, y + 10), (x + 28, y + ch - 10), (x, y + ch)], fill=col)
        elif n == p["pintu"]:
            gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).rounded_rectangle((x - 16, y - 16, x + cw + 16, y + ch + 16), radius=20, fill=(255, 220, 140, 150))
            img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((x, y, x + cw, y + ch), radius=10, fill=(255, 248, 226))
            bintang5(d, x + cw / 2, y + ch / 2 - 8, 30, (226, 170, 50, 255))
            d.text((x + cw / 2, y + ch - 14), "hari ini", font=hn(20, 1), fill=(150, 60, 40), anchor="ms")
            d.polygon([(x, y), (x + 34, y + 12), (x + 34, y + ch - 12), (x, y + ch)], fill=col)
        else:
            d.rounded_rectangle((x, y, x + cw, y + ch), radius=10, fill=col)
            tc = (40, 40, 40) if sum(col) > 600 else (255, 250, 236)
            d.text((x + cw / 2, y + ch / 2), str(n), font=ft("Georgia Bold.ttf", 50), fill=tc, anchor="mm")
            d.ellipse((x + cw - 22, y + ch / 2 - 5, x + cw - 12, y + ch / 2 + 5), fill=(236, 206, 140))
    y = y0 + rows * (ch + gx) + 30
    d.text((W / 2, y), p["tanggal"].upper(), font=hn(26, 10), fill=(200, 220, 200), anchor="ma")
    y += 50
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 200):
        d.text((W / 2, y), ln, font=georgia(34), fill=(250, 244, 230), anchor="ma")
        y += 46
    ayat_bawah(img, p, y + 20, H - 60, (210, 220, 210), (236, 206, 140), start=28, stop=20)
    ImageDraw.Draw(img).text((W / 2, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(150, 180, 160), anchor="ma")
    return img


# ---------- KRANS (Reels): krans Adven ----------

LILIN_WARNA = [(110, 60, 140), (110, 60, 140), (210, 130, 170), (110, 60, 140)]


def nyala_sprite(s, k=1.0):
    def g(d, kk):
        S = s * kk
        for sc, c in [(1.0, (255, 140, 40, 210)), (0.75, (255, 200, 90, 240)), (0.45, (255, 248, 220, 255))]:
            pts = [(S / 2 + S * .22 * sc * math.sin(math.pi * u) * (1 - u) ** 0.6, S * .98 - S * .9 * sc * u) for u in np.linspace(0, 1, 40)]
            pts += [(S - x, y) for x, y in reversed(pts)]
            d.polygon(pts, fill=c)
    return sprite(s, s, g).filter(ImageFilter.GaussianBlur(1.5))


def krans_reel(p, idx, mod=MOD, seconds=12, terang=False):
    rel = f"reels/{mod}/krans{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(3900 + idx)
    bg = (gradasi(RW, RH, (248, 240, 228), (222, 204, 182)) if terang else gradasi(RW, RH, (44, 24, 34), (14, 8, 12))).convert("RGBA")
    cx, cy, rx, ry = RW / 2, 1150, 380, 130
    angs = [200, 250, 290, 340]
    lil = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in angs]
    order = sorted(range(4), key=lambda k: lil[k][1])

    def daun(half):
        lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        r2 = np.random.default_rng(4000 + half)
        for _ in range(700):
            a = r2.uniform(0, 2 * math.pi)
            if (math.sin(a) < 0) != (half == 0):
                continue
            rr = r2.uniform(-40, 40)
            x, y = cx + (rx + rr) * math.cos(a), cy + (ry + rr * 0.4) * math.sin(a)
            L = r2.uniform(30, 60)
            ang = a + math.pi / 2 + r2.uniform(-0.6, 0.6)
            col = [(30, 90, 50), (40, 110, 60), (24, 70, 40), (60, 130, 70)][int(r2.integers(4))]
            dd.polygon([(x, y), (x + L * math.cos(ang) - 8 * math.sin(ang), y + L * math.sin(ang) * 0.5 + 8 * math.cos(ang)),
                        (x + L * math.cos(ang) * 1.1, y + L * math.sin(ang) * 0.55),
                        (x + L * math.cos(ang) + 8 * math.sin(ang), y + L * math.sin(ang) * 0.5 - 8 * math.cos(ang))], fill=col + (255,))
        for _ in range(26):
            a = r2.uniform(0, 2 * math.pi)
            if (math.sin(a) < 0) != (half == 0):
                continue
            x, y = cx + rx * math.cos(a) + r2.uniform(-20, 20), cy + ry * math.sin(a) + r2.uniform(-10, 10)
            dd.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(200, 30, 40, 255))
        return lay
    belakang, depan = daun(0), daun(1)
    tinggi = [330, 330, 330, 330]
    lilin_lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lilin_lay)
    for k in order:
        x, y = lil[k]
        c = np.array(LILIN_WARNA[k], np.float32)
        for j in range(70):
            t = j / 69
            shade = 0.65 + 0.45 * math.sin(math.pi * t)
            ld.line((x - 35 + j, y - tinggi[k], x - 35 + j, y), fill=tuple(int(v) for v in np.clip(c * shade, 0, 255)) + (255,))
        ld.ellipse((x - 35, y - tinggi[k] - 10, x + 35, y - tinggi[k] + 10), fill=tuple(int(v * 1.2) for v in c) + (255,))
        ld.line((x, y - tinggi[k] - 4, x, y - tinggi[k] - 24), fill=(30, 20, 16, 255), width=4)
    base = bg.copy()
    base.alpha_composite(belakang)
    base.alpha_composite(lilin_lay)
    base.alpha_composite(depan)
    glow = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((150, 150, 550, 550), fill=(255, 170, 80, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    api = nyala_sprite(90)
    total = p.get("lilin", 1)
    nyala_t = [0.0] + ([5.0] * (total - 1) if total <= 2 else [1.8 + 1.4 * k for k in range(total - 1)])  # lilin pertama menyala di sampul
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tl = wrap(probe, bersih(p["teks"]), georgia(40), RW - 200)
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 300, 36, 24, 1.36)
    teks = Image.new("RGBA", (RW, 520), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks)
    td.text((RW / 2, 0), bersih(p["judul"]), font=georgia(58, True), fill=(140, 40, 60) if terang else (250, 226, 170), anchor="ma")
    y = 100
    for ln in tl:
        td.text((RW / 2, y), ln, font=georgia(40), fill=(60, 44, 40) if terang else (246, 238, 226), anchor="ma")
        y += 54
    ayat = Image.new("RGBA", (RW, 420), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(70, 54, 48) if terang else (226, 214, 200), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 12), p["ref"], font=hn(30, 1), fill=(160, 70, 60) if terang else (250, 200, 120), anchor="ma")
    ad.text((RW / 2, y + 70), "@" + HANDLE, font=hn(26, 10), fill=(140, 120, 110) if terang else (170, 150, 150), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = base.copy()
        for k in range(total):
            if t < nyala_t[k]:
                continue
            a = 1.0 if k == 0 else ease((t - nyala_t[k]) / 0.8)
            fl = 0.88 + 0.12 * math.sin(t * 11 + k * 2) * math.sin(t * 7.3 + k)
            x, y = lil[k]
            comp(frame, fade(glow, a * fl), (x - 350, y - tinggi[k] - 380))
            s = api.resize((int(90 * (0.6 + 0.4 * a)), int(90 * (0.6 + 0.4 * a) * (1 + 0.06 * math.sin(t * 13 + k)))))
            comp(frame, fade(s, a), (x - s.width / 2, y - tinggi[k] - 20 - s.height))
        frame.alpha_composite(fade(teks, 1.0 if t < 0.1 else ease((t - 0.2) / 0.8) if t < 1.0 else 1.0), (0, 240))
        if t >= 2.5:
            frame.alpha_composite(fade(ayat, ease((t - 2.5) / 0.8)), (0, 1360))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- JAMPASIR (Reels): jam pasir ----------

def jampasir_reel(p, idx, mod=MOD, seconds=12):
    rel = f"reels/{mod}/jampasir{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    bg = grain(gradasi(RW, RH, (246, 226, 196), (214, 150, 110)), 0.05).convert("RGBA")
    cx, top, neck, bot = RW / 2, 640, 960, 1280

    def lebar(u):  # u: 0 di ujung bulb, 1 di leher
        return 16 + 200 * max(0.0, 1 - u ** 1.7) ** 0.65
    atas = [(cx + lebar((y - top) / (neck - top)), y) for y in np.linspace(top, neck, 50)]
    bawah = [(cx + lebar((bot - y) / (bot - neck)), y) for y in np.linspace(neck, bot, 50)]
    outline = atas + bawah + [(2 * cx - x, y) for x, y in reversed(bawah)] + [(2 * cx - x, y) for x, y in reversed(atas)]
    kayu_ = (110, 66, 40)
    pasir = (226, 176, 96)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    teks = Image.new("RGBA", (RW, 420), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks)
    td.text((RW / 2, 0), bersih(p["judul"]), font=georgia(58, True), fill=(90, 40, 30), anchor="ma")
    y = 96
    for ln in wrap(td, bersih(p["teks"]), georgia(40), RW - 200):
        td.text((RW / 2, y), ln, font=georgia(40), fill=(70, 46, 36), anchor="ma")
        y += 54
    f, vl, vs = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), RW - 220, 260, 34, 24, 1.36)
    ayat = Image.new("RGBA", (RW, 360), (0, 0, 0, 0))
    ad = ImageDraw.Draw(ayat)
    y = 0
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f, fill=(70, 40, 30), anchor="ma")
        y += vs * 1.36
    ad.text((RW / 2, y + 10), p["ref"], font=hn(30, 1), fill=(150, 60, 40), anchor="ma")
    ad.text((RW / 2, y + 64), "@" + HANDLE, font=hn(26, 10), fill=(140, 90, 70), anchor="ma")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frac = 0.2 + 0.6 * t / seconds  # bagian pasir yang sudah turun
        frame = bg.copy()
        lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.polygon(outline, fill=(255, 255, 255, 70))
        ys = top + (neck - top) * (0.25 + 0.75 * frac)  # permukaan pasir atas turun ke leher
        sa = [(cx + lebar((y - top) / (neck - top)) - 6, y) for y in np.linspace(ys, neck, 30)]
        d.polygon(sa + [(2 * cx - x, y) for x, y in reversed(sa)], fill=pasir + (255,))
        yb = bot - (bot - neck) * 0.62 * frac  # tumpukan bawah
        sb = [(cx + lebar((bot - y) / (bot - neck)) - 6, y) for y in np.linspace(yb, bot - 4, 30)]
        d.polygon([(cx, yb - 40)] + sb + [(2 * cx - x, y) for x, y in reversed(sb)], fill=pasir + (255,))
        d.line((cx, neck, cx, yb - 30), fill=pasir + (255,), width=5)
        d.line(outline + [outline[0]], fill=(255, 255, 255, 200), width=5)
        d.line([(cx - lebar((y - top) / (neck - top)) + 30, y) for y in np.linspace(top + 30, neck - 80, 20)], fill=(255, 255, 255, 140), width=8)
        frame.alpha_composite(lay)
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((cx - 270, top - 50, cx + 270, top), radius=14, fill=kayu_)
        d.rounded_rectangle((cx - 270, bot, cx + 270, bot + 50), radius=14, fill=kayu_)
        for sx in (cx - 240, cx + 240):
            d.rounded_rectangle((sx - 12, top - 10, sx + 12, bot + 10), radius=10, fill=(130, 80, 50))
        frame.alpha_composite(teks, (0, 210))
        if t >= 2.5:
            frame.alpha_composite(fade(ayat, ease((t - 2.5) / 0.8)), (0, 1380))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

NEON_WARNA = [(255, 70, 170), (60, 170, 255), (255, 196, 60)]


def neonletter_reel(p, idx, mod=MOD, seconds=10):
    """Papan huruf felt, tapi hurufnya lampu neon yang menyala satu baris demi satu baris."""
    rel = f"reels/{mod}/neonletter{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(4100 + idx)
    wall = np.asarray(gradasi(RW, RH, (34, 30, 36), (14, 12, 16))).astype(np.float32)
    bw, bh, fr = 900, 1100, 34
    bx, by = (RW - bw) // 2, 380
    board = gaya_w8.kayu(bw, bh, rng, (120, 86, 56))
    felt = np.zeros((bh - 2 * fr, bw - 2 * fr, 3), np.float32) + 22
    for yy in range(0, felt.shape[0], 30):
        felt[yy:yy + 3] *= 0.5
    board.paste(Image.fromarray(np.clip(felt, 0, 255).astype(np.uint8)), (fr, fr))
    wall[by:by + bh, bx:bx + bw] = np.asarray(board).astype(np.float32)
    lines = bersih(p["teks"]).upper().split("\n")
    probe = ImageDraw.Draw(Image.new("L", (10, 10)))
    size = 96
    while max(probe.textlength(ln, font=hn(size, 1)) for ln in lines) > bw - 160:
        size -= 2
    lh = size * 1.3
    cy0 = by + bh / 2 - (len(lines) + 1) * lh / 2
    col = NEON_WARNA[idx % 3]
    layers = []
    for k, ln in enumerate(lines):
        m = Image.new("L", (RW, RH), 0)
        ImageDraw.Draw(m).text((RW / 2, cy0 + k * lh + lh / 2), ln, font=hn(size, 1), fill=255, anchor="mm")
        layers.append(gaya_w7.neon_layer(m, col))
    m = Image.new("L", (RW, RH), 0)
    ImageDraw.Draw(m).text((RW / 2, cy0 + len(lines) * lh + lh / 2), p["ref"].upper(), font=hn(int(size * 0.5), 1), fill=255, anchor="mm")
    layers.append(gaya_w7.neon_layer(m, (255, 236, 210)))
    hand = Image.new("L", (RW, RH), 0)
    ImageDraw.Draw(hand).text((RW / 2, by + bh + 60), "@" + HANDLE, font=hn(28, 10), fill=255, anchor="mm")
    hand = np.asarray(hand).astype(np.float32)[..., None] / 255

    def nyala(t, k):
        if t < 0.5:
            return 1.0
        mulai = 0.9 + k * 0.7
        if t < mulai:
            return 0.0
        dt_ = t - mulai
        if dt_ < 0.35:
            return 1.0 if int(dt_ * 24) % 3 else 0.2
        return 0.97 + 0.03 * math.sin(2 * math.pi * 6 * t + k)

    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = wall.copy()
        tubes = []
        for k, (light, m_, core, tube) in enumerate(layers):
            a = nyala(t, k)
            frame += light * a * 0.8
            tubes.append((m_, core, tube, a))
        for m_, core, tube, a in tubes:
            mm = m_[..., None]
            lit = tube * a + np.array([60, 58, 60], np.float32) * (1 - a)
            frame = frame * (1 - mm) + lit * mm
            frame = frame * (1 - core[..., None] * a * 0.8) + 255 * core[..., None] * a * 0.8
        frame = frame * (1 - hand * 0.7) + 190 * hand * 0.7
        ff.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


def gosoknatal_reel(p, idx, mod=MOD):
    return gaya_w9.gosok_reel(p, idx, mod, natal=True)


def koranmalam_image(p, i):
    img = gaya_w8.koran_image(dict(p, _edisi="EDISI MALAM"), i).convert("RGB")
    a = np.asarray(ImageOps.invert(img)).astype(np.float32)
    a *= np.array([0.86, 0.9, 1.0])
    a += np.array([6, 10, 24])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def kamusfoto_image(p, i):
    kartu = gaya_w7.kamus_image(p, i).convert("RGBA")
    kartu = kartu.resize((int(W * 0.84), int(H * 0.84)), Image.LANCZOS)
    rng = np.random.default_rng(4200 + i)
    m = Image.new("L", kartu.size, 0)
    w_, h_ = kartu.size
    pts = [(x, rng.uniform(0, 10)) for x in range(0, w_ + 1, 14)] + [(w_, h_ - rng.uniform(0, 10))]
    pts += [(x, h_ - rng.uniform(0, 10)) for x in range(w_, -1, -14)]
    ImageDraw.Draw(m).polygon(pts, fill=255)
    kartu.putalpha(m)
    kartu = kartu.rotate(-2.5 if i % 2 else 2.0, expand=True, resample=Image.BICUBIC)
    latar = vintage(foto_warna(("laut", "fajar")[i % 2], W, H, seed=4250 + i)).filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    bayangan(latar, kartu, ((W - kartu.width) // 2, (H - kartu.height) // 2), blur=20, geser=(10, 18), kuat=0.5)
    return latar


def ketiklilin_image(p, i):
    img = gaya_w7.ketik_image(p, i).convert("RGB")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = W * (0.85 if i % 2 else 0.15), H * 0.9
    dist = np.hypot((xx - lx) / W, (yy - ly) / H)
    light = 0.5 + 0.75 * np.exp(-(dist / 0.75) ** 2)
    a = np.asarray(img).astype(np.float32) * light[..., None] * np.array([1.08, 0.96, 0.78])
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((lx - 160, ly - 160, lx + 160, ly + 160), fill=(255, 170, 80, 110))
    out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
    return out


SIMPLE = {
    # baru
    "MAJALAH": majalah_image, "TOPLES": toples_image, "RASI": rasi_image, "GARIS": garis_image, "FILM": film_image,
    "TELEGRAM": telegram_image, "TANYA": tanya_image, "KOMPAS": kompas_image, "KALADVEN": kaladven_image,
    # lama
    "ALKITAB": gaya_w6.alkitab_image, "DOA": gaya_w6.doa_image, "CUACA": gaya_w7.cuaca_image, "POLAROID": gaya_w7.polaroid_image,
    "PLAYER": gaya_w7.player_image, "LETTER": gaya_w8.letter_image, "MENU": gaya_w8.menu_image, "NAMA": gaya_w9.nama_image,
    "JENDELA": gaya_w9.jendela_image, "ORNAMEN": gaya_w8.ornamen_image,
    # mix
    "KALENDERFOTO": lambda p, i: gaya_w7.kalender_image(p, i, latar=bokeh(W, H, 4300 + i)),
    "KORANMALAM": koranmalam_image,
    "STRUKNATAL": lambda p, i: gaya_w7.struk_image(p, i, alas=kertas_kado(W, H, i)),
    "TIKETBINTANG": lambda p, i: gaya_w7.tiket_image(p, i, latar=render.suasana_scene("bintang", W, H, 4400 + i)(3.0)),
    "POPUPNATAL": lambda p, i: gaya_w7.popup_image(p, i, natal=True),
    "KAMUSFOTO": kamusfoto_image,
    "CATATANGELAP": lambda p, i: gaya_w7.catatan_image(p, i, gelap=True),
    "KETIKLILIN": ketiklilin_image,
    "RESEPNATAL": lambda p, i: gaya_w9.resep_image(p, i, latar=kotak_kotak(W, H)),
    "PETAMALAM": lambda p, i: gaya_w8.peta_image(p, i, gelap=True),
}
REELS = {"KRANS": (krans_reel, "krans"), "JAMPASIR": (jampasir_reel, "jampasir"), "NEONLETTER": (neonletter_reel, "neonletter"),
         "GOSOKNATAL": (gosoknatal_reel, "gosok"), "CHAT": (gaya_w7.chat_reel, "chat"), "FLIP": (gaya_w8.flip_reel, "flip")}


def konteks(p, hari, slot):
    """Tanggal & jam slot untuk gaya lama yang menampilkan waktu."""
    tgl = MULAI + dt.timedelta(days=hari - 1)
    jam = config.AKUN["tenang"]["jam"][slot].replace(":", ".")
    return dict(p, _jam=jam, _tanggal=f"{tgl.day} {BULAN[tgl.month]} 2026", _tgl_struk=tgl.strftime("%d/%m/%Y"),
                _tanggal_panjang=f"{HARI[(hari - 1) % 7]}, {tgl.day} {BULAN[tgl.month]} 2026")


def render_week(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "ELI":
                import tenang_eli
                out[(hari, slot)] = tenang_eli.render_item(t.ELI[idx])
                continue
            p = getattr(t, fmt)[idx]
            if fmt in SIMPLE:
                out[(hari, slot)] = ([save(SIMPLE[fmt](konteks(p, hari, slot), idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt == "UTAS":
                out[(hari, slot)] = (utas_files(p, idx, mod), p["caption"])
            elif fmt in REELS:
                rel = f"reels/{mod}/{REELS[fmt][1]}{idx + 1}.mp4"
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], p["caption"])
    return out


def render_reels(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt in REELS:
                rel = REELS[fmt][0](konteks(getattr(t, fmt)[idx], hari, slot), idx, mod)
                tambah_musik(rel)
                print(rel, flush=True)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
