"""Akun Tenang - minggu 9 (konten/tenang_w9.py): 12 gaya baru, satu gaya per slot.
JAM (jam tangan pintar), NAMA (kartu nama "Nama-nama Yesus"), RAMBU (rambu lalu lintas), RESEP (kartu resep tulisan tangan),
UNDANGAN (kartu undangan + segel lilin), PROGRESS (Reels bilah instalasi), GLOBE (bola salju, hitung mundur Natal),
MUSEUM (lukisan di galeri + papan keterangan), KASET (kaset + daftar lagu), GOSOK (Reels kartu gosok),
SERTIFIKAT (sertifikat), JENDELA (jendela berembun di malam hari). Komik Eli 3x seminggu.

  python3 gaya_w9.py [reels]
"""
import importlib
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cerita
import config
import render
from gaya_w6 import cover, foto_warna, georgia, hn, tambah_musik
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tangan, tanpa_kutip, vintage
from gaya_w8 import kayu
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w9"
RW, RH, FPS = 1080, 1920, 30
EMAS = (184, 146, 72)


def kertas_kado(w, h, seed=0):
    """Kertas kado Natal: merah/hijau bergaris diagonal dengan bintang emas."""
    rng = np.random.default_rng(3100 + seed)
    base, garis = [((168, 28, 40), (190, 52, 60)), ((22, 92, 62), (34, 112, 78)), ((120, 20, 34), (150, 40, 50))][seed % 3]
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    for k in range(-h, w, 70):
        d.line((k, 0, k + h, h), fill=garis, width=26)
    for _ in range(int(w * h / 26000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(8, 16)
        d.polygon([(x, y - r), (x + r * .3, y - r * .3), (x + r, y), (x + r * .3, y + r * .3), (x, y + r), (x - r * .3, y + r * .3),
                   (x - r, y), (x - r * .3, y - r * .3)], fill=(236, 196, 100))
    return grain(img, 0.05)


def mahkota(s, col=EMAS + (255,)):
    def g(d, k):
        S = s * k
        d.polygon([(S * .08, S * .78), (S * .14, S * .3), (S * .34, S * .55), (S * .5, S * .18), (S * .66, S * .55),
                   (S * .86, S * .3), (S * .92, S * .78)], fill=col)
        d.rectangle((S * .08, S * .8, S * .92, S * .9), fill=col)
        for x, y in ((.14, .26), (.5, .14), (.86, .26)):
            d.ellipse((S * (x - .05), S * (y - .05), S * (x + .05), S * (y + .05)), fill=col)
    return sprite(s, s, g)


def ayat_bawah(img, p, y0, y1, warna, warna_ref, maxw=W - 180, start=34, stop=22):
    d = ImageDraw.Draw(img)
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), maxw, y1 - y0 - 60, start, stop, 1.36)
    y = y0
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=warna, anchor="ma")
        y += size * 1.36
    d.text((W / 2, y + 10), p["ref"], font=hn(28, 1), fill=warna_ref, anchor="ma")
    return y + 50


# ---------- JAM: jam tangan pintar ----------

PAGI = [((250, 214, 190), (246, 168, 140)), ((206, 226, 240), (150, 190, 226)), ((226, 236, 214), (176, 206, 170)),
        ((240, 226, 250), (200, 176, 236)), ((252, 236, 200), (240, 196, 130)), ((214, 240, 236), (150, 210, 200)),
        ((246, 220, 226), (226, 160, 180))]
TALI = [(120, 140, 120), (60, 70, 96), (196, 170, 140), (150, 110, 120), (70, 100, 110), (200, 130, 90), (90, 90, 96)]


def jam_image(p, i):
    img = grain(gradasi(W, H, *PAGI[i % 7]), 0.05).convert("RGBA")
    cx, top, bw, bh = W / 2, 150, 470, 560
    tali = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tali)
    tc = TALI[i % 7] + (255,)
    td.rounded_rectangle((cx - 160, -40, cx + 160, top + 60), radius=40, fill=tc)
    td.rounded_rectangle((cx - 160, top + bh - 60, cx + 160, top + bh + 210), radius=40, fill=tc)
    for k in range(3):
        y = top + bh + 70 + k * 44
        td.ellipse((cx - 9, y - 9, cx + 9, y + 9), fill=tuple(int(c * 0.6) for c in tc[:3]) + (255,))
    bayangan(img, tali, (0, 0), blur=18, geser=(0, 10), kuat=0.25)
    body = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle((0, 0, bw, bh), radius=130, fill=(70, 72, 78, 255))
    bd.rounded_rectangle((6, 6, bw - 6, bh - 6), radius=124, fill=(28, 28, 32, 255))
    bd.rounded_rectangle((26, 26, bw - 26, bh - 26), radius=104, fill=(0, 0, 0, 255))
    white, grey = (255, 255, 255, 255), (160, 160, 168, 255)
    bd.text((bw - 70, 66), "06.00", font=hn(36, 1), fill=white, anchor="ra")
    bd.ellipse((60, 120, 120, 180), fill=(232, 168, 60, 255))
    bd.rectangle((86, 132, 94, 168), fill=white)
    bd.rectangle((74, 142, 106, 150), fill=white)
    bd.text((136, 150), "TENANG", font=hn(26, 1), fill=grey, anchor="lm")
    bd.text((60, 206), bersih(p["judul"]), font=hn(46, 1), fill=white)
    f, lines, size = pas(bd, bersih(p["pesan"]), lambda s: hn(s, 0), bw - 120, bh - 130 - 272, 36, 22, 1.28)
    y = 272
    for ln in lines:
        bd.text((60, y), ln, font=f, fill=(225, 225, 230, 255))
        y += size * 1.28
    bd.rounded_rectangle((60, bh - 110, bw - 60, bh - 50), radius=30, fill=(44, 44, 50, 255))
    bd.text((bw / 2, bh - 80), "Amin", font=hn(30, 1), fill=white, anchor="mm")
    bayangan(img, body, (cx - bw / 2, top), blur=26, geser=(0, 18), kuat=0.45)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx + bw / 2 - 4, top + 150, cx + bw / 2 + 20, top + 250), radius=10, fill=(90, 92, 98))
    d.rounded_rectangle((cx + bw / 2 - 4, top + 300, cx + bw / 2 + 14, top + 380), radius=8, fill=(80, 82, 88))
    ink = (50, 40, 40)
    ayat_bawah(img, p, 990, H - 70, ink, ink)
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(22, 10), fill=(90, 80, 80), anchor="ma")
    return img


# ---------- NAMA: kartu nama "Nama-nama Yesus" ----------

def marmer(w, h, rng):
    n = render.fbm2d(h, w, rng, ((3, 1.0), (9, 0.6), (30, 0.3)))
    vein = np.abs(np.sin((n * 14 + np.linspace(0, 3, w)[None, :]) * math.pi))
    arr = np.zeros((h, w, 3), np.float32) + 242
    arr -= (1 - vein[..., None]) ** 8 * 60
    arr -= (n[..., None] - 0.5) * 10
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def nama_image(p, i):
    rng = np.random.default_rng(2100 + i)
    img = grain(marmer(W, H, rng), 0.03).convert("RGBA")
    navy = (24, 36, 70)
    cw, chh = 900, 540
    back = Image.new("RGBA", (cw, chh), navy + (255,))
    comp(back, mahkota(200), (cw / 2 - 100, chh / 2 - 110))
    back = back.rotate(9, expand=True, resample=Image.BICUBIC)
    bayangan(img, back, (W / 2 - back.width / 2 + 40, 40), blur=18, geser=(6, 14), kuat=0.35)
    card = Image.new("RGBA", (cw, chh), (252, 251, 247, 255))
    d = ImageDraw.Draw(card)
    comp(card, mahkota(70), (60, 50))
    d = ImageDraw.Draw(card)
    nama = bersih(p["nama"])
    fn_ = ft("BigCaslon.ttf", 74)
    while d.textlength(nama, font=fn_) > cw - 120:
        fn_ = ft("BigCaslon.ttf", fn_.size - 2)
    d.text((60, 150), nama, font=fn_, fill=navy)
    d.text((62, 150 + fn_.size + 20), bersih(p["sub"]).upper(), font=hn(24, 10), fill=(120, 120, 130))
    d.line((60, 300, 200, 300), fill=EMAS, width=3)
    for k, (lab, val) in enumerate(p["kontak"]):
        y = 340 + k * 56
        d.text((60, y), bersih(lab).upper(), font=hn(22, 1), fill=EMAS)
        d.text((210, y - 4), bersih(val), font=hn(30, 0), fill=(40, 44, 56))
    card = card.rotate(-3, expand=True, resample=Image.BICUBIC)
    bayangan(img, card, (W / 2 - card.width / 2 - 20, 250), blur=20, geser=(8, 18), kuat=0.4)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 880), "NAMA-NAMA YESUS", font=hn(26, 1), fill=EMAS, anchor="ma")
    ayat_bawah(img, p, 930, H - 70, (50, 50, 60), navy)
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(22, 10), fill=(140, 140, 150), anchor="ma")
    return img


# ---------- RAMBU: rambu lalu lintas ----------

def rambu(jenis, teks, s):
    def g(d, k):
        S = s * k
        c = S / 2
        if jenis == "stop":
            pts = [(c + c * .96 * math.cos(math.radians(22.5 + 45 * j)), c + c * .96 * math.sin(math.radians(22.5 + 45 * j))) for j in range(8)]
            d.polygon(pts, fill=(255, 255, 255, 255))
            d.polygon([(c + (x - c) * .9, c + (y - c) * .9) for x, y in pts], fill=(204, 30, 36, 255))
        elif jenis == "larangan":
            d.ellipse((S * .02, S * .02, S * .98, S * .98), fill=(204, 30, 36, 255))
            d.ellipse((S * .14, S * .14, S * .86, S * .86), fill=(255, 255, 255, 255))
        elif jenis == "peringatan":
            pts = [(c, S * .02), (S * .98, c), (c, S * .98), (S * .02, c)]
            d.polygon(pts, fill=(20, 20, 20, 255))
            d.polygon([(c + (x - c) * .9, c + (y - c) * .9) for x, y in pts], fill=(255, 204, 0, 255))
        else:
            d.rounded_rectangle((S * .02, S * .14, S * .98, S * .86), radius=S * .06, fill=(255, 255, 255, 255))
            d.rounded_rectangle((S * .06, S * .18, S * .94, S * .82), radius=S * .05, fill=(18, 82, 170, 255))
    img = sprite(s, s, g)
    d = ImageDraw.Draw(img)
    col = (255, 255, 255) if jenis in ("stop", "petunjuk") else (20, 20, 20)
    box = {"stop": s * .7, "larangan": s * .62, "peringatan": s * .5, "petunjuk": s * .8}[jenis]
    for size in range(int(s * .2), 14, -1):
        f = hn(size, 9)
        lines = wrap(d, bersih(teks).upper(), f, box)
        if len(lines) * size * 1.0 <= box * (0.72 if jenis != "petunjuk" else 0.55) and all(d.textlength(x, font=f) <= box for x in lines):
            break
    y = s / 2 - len(lines) * size / 2
    for ln in lines:
        d.text((s / 2, y + size / 2), ln, font=f, fill=col, anchor="mm")
        y += size
    return img


def rambu_image(p, i):
    img = grain(gradasi(W, H, (214, 230, 242), (244, 240, 230)), 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 760, W, 800), fill=(110, 110, 116))
    for x in range(0, W, 120):
        d.rectangle((x + 20, 776, x + 80, 784), fill=(240, 240, 240))
    d.text((W / 2, 70), "RAMBU HARI INI", font=hn(30, 1), fill=(40, 60, 90), anchor="ma")
    s = 290
    for k, (jenis, teks, ket) in enumerate(p["rambu"]):
        cx = W / 2 + (k - 1) * 340
        d.rectangle((cx - 9, 140 + s - 20, cx + 9, 770), fill=(150, 154, 160))
        d.rectangle((cx - 9, 140 + s - 20, cx - 3, 770), fill=(190, 194, 200))
        bayangan(img, rambu(jenis, teks, s), (cx - s / 2, 140), blur=10, geser=(4, 8), kuat=0.3)
        d = ImageDraw.Draw(img)
        y = 600 - 140 + 0
        lab = Image.new("RGBA", (310, 150), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lab)
        lines = wrap(ld, bersih(ket), hn(28, 10), 270)
        hh = len(lines) * 36 + 28
        ld.rounded_rectangle((0, 0, 310, hh), radius=16, fill=(255, 255, 255, 235))
        yy = 14
        for ln in lines:
            ld.text((155, yy), ln, font=hn(28, 10), fill=(40, 44, 56), anchor="ma")
            yy += 36
        img.alpha_composite(lab.crop((0, 0, 310, hh)), (int(cx - 155), 830))
    ayat_bawah(img, p, 1010, H - 70, (40, 44, 56), (18, 82, 170), start=32)
    d = ImageDraw.Draw(img)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(120, 124, 132), anchor="ma")
    return img


# ---------- RESEP: kartu resep tulisan tangan ----------

def resep_image(p, i, latar=None):
    rng = np.random.default_rng(2300 + i)
    img = (latar.copy() if latar is not None else kayu(W, H, rng, (196, 150, 104))).convert("RGBA")
    cw, chh = 960, 1250
    card = Image.new("RGBA", (cw, chh), (252, 249, 238, 255))
    d = ImageDraw.Draw(card)
    for y in range(190, chh - 30, 52):
        d.line((30, y, cw - 30, y), fill=(178, 206, 232, 255), width=2)
    d.line((30, 150, cw - 30, 150), fill=(220, 90, 90, 255), width=3)
    ink, merah = (36, 52, 110), (190, 50, 50)
    d.text((50, 50), bersih(p["judul"]), font=ft("Bradley Hand Bold.ttf", 60), fill=merah)
    d.text((50, 160), f"Porsi: {bersih(p['porsi'])}   ·   Waktu: {bersih(p['waktu'])}", font=tangan(30), fill=(90, 90, 110))
    y = 230
    d.text((50, y), "Bahan:", font=tangan(38), fill=merah)
    y += 52
    for b in p["bahan"]:
        d.text((70, y), "• " + bersih(b), font=tangan(34), fill=ink)
        y += 52
    y += 10
    d.text((50, y), "Cara membuat:", font=tangan(38), fill=merah)
    y += 52
    for n, l in enumerate(p["langkah"], 1):
        lines = wrap(d, bersih(l), tangan(34), cw - 160)
        for k, ln in enumerate(lines):
            d.text((70, y), (f"{n}. " if k == 0 else "    ") + ln, font=tangan(34), fill=ink)
            y += 52
    y += 20
    f, lines, size = pas(d, bersih(p["ayat"]), tangan, cw - 140, chh - 90 - y, 34, 22, 1.5)
    for ln in lines:
        d.text((70, y), ln, font=f, fill=(70, 70, 90))
        y += size * 1.5
    d.text((cw - 60, y + 4), "— " + p["ref"], font=tangan(32), fill=merah, anchor="ra")
    noda = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))  # bekas cangkir
    ImageDraw.Draw(noda).ellipse((cw - 260, chh - 300, cw - 60, chh - 100), outline=(150, 100, 60, 40), width=10)
    card.alpha_composite(noda.filter(ImageFilter.GaussianBlur(2)))
    ImageDraw.Draw(card).text((cw - 40, chh - 26), "@" + HANDLE, font=hn(20, 10), fill=(160, 150, 140), anchor="rs")
    card = card.rotate(1.5, expand=True, resample=Image.BICUBIC)
    bayangan(img, card, ((W - card.width) // 2, (H - card.height) // 2), blur=18, geser=(8, 14), kuat=0.45)
    return img


# ---------- UNDANGAN: kartu undangan + segel lilin ----------

LATAR_UND = [(186, 150, 150), (150, 170, 150), (60, 74, 110), (170, 150, 120), (120, 100, 130), (150, 120, 100), (90, 120, 120)]


def segel(s, col=(150, 26, 30)):
    def g(d, k):
        S = s * k
        c = S / 2
        pts = [(c + c * (.92 + .06 * math.sin(a * 7)) * math.cos(a), c + c * (.92 + .06 * math.sin(a * 7)) * math.sin(a))
               for a in np.linspace(0, 2 * math.pi, 60)]
        d.polygon(pts, fill=col + (255,))
        d.ellipse((S * .2, S * .2, S * .8, S * .8), outline=tuple(int(x * .7) for x in col) + (255,), width=int(4 * k))
    img = sprite(s, s, g)
    comp(img, mahkota(int(s * .42), (110, 16, 20, 255)), (s * .29, s * .27))
    return img


def undangan_image(p, i):
    rng = np.random.default_rng(2400 + i)
    bgc = LATAR_UND[i % 7]
    img = grain(gradasi(W, H, tuple(min(255, c + 30) for c in bgc), bgc), 0.05).convert("RGBA")
    amp = Image.new("RGBA", (900, 640), (0, 0, 0, 0))  # amplop di belakang
    ad = ImageDraw.Draw(amp)
    ad.rectangle((0, 0, 900, 640), fill=(236, 226, 206, 255))
    ad.polygon([(0, 0), (450, 300), (900, 0)], fill=(226, 214, 190, 255))
    amp = amp.rotate(-6, expand=True, resample=Image.BICUBIC)
    bayangan(img, amp, (W / 2 - amp.width / 2, 640), blur=16, geser=(4, 12), kuat=0.3)
    cw, chh = 780, 1080
    card = np.zeros((chh, cw, 3), np.float32) + np.array([250, 246, 236])
    card *= (0.97 + 0.04 * render.fbm2d(chh, cw, rng, ((30, 1.0), (200, 0.5))))[..., None]
    card = Image.fromarray(np.clip(card, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(card)
    d.rectangle((26, 26, cw - 26, chh - 26), outline=EMAS, width=3)
    d.rectangle((38, 38, cw - 38, chh - 38), outline=EMAS, width=1)
    for cx, cy in ((38, 38), (cw - 38, 38), (38, chh - 38), (cw - 38, chh - 38)):
        d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=EMAS)
    ink = (60, 50, 40)
    d.text((cw / 2, 110), "KAMU DIUNDANG", font=hn(26, 10), fill=EMAS, anchor="ma")
    d.text((cw / 2, 160), "dengan penuh sukacita, kepada", font=georgia(28, True), fill=(110, 100, 90), anchor="ma")
    fu = ft("SnellRoundhand.ttc", 86, 1)
    while d.textlength(bersih(p["untuk"]), font=fu) > cw - 140:
        fu = ft("SnellRoundhand.ttc", fu.size - 4, 1)
    d.text((cw / 2, 260), bersih(p["untuk"]), font=fu, fill=ink, anchor="mm")
    d.text((cw / 2, 340), "untuk hadir di", font=georgia(28, True), fill=(110, 100, 90), anchor="ma")
    f, lines, size = pas(d, bersih(p["judul"]).upper(), lambda s: ft("BigCaslon.ttf", s), cw - 140, 150, 60, 34, 1.15)
    y = 400
    for ln in lines:
        d.text((cw / 2, y), ln, font=f, fill=ink, anchor="ma")
        y += size * 1.15
    y += 20
    d.line((cw / 2 - 120, y, cw / 2 + 120, y), fill=EMAS, width=2)
    d.ellipse((cw / 2 - 6, y - 6, cw / 2 + 6, y + 6), fill=EMAS)
    y += 34
    for lab, val in p["acara"]:
        d.text((cw / 2, y), bersih(lab).upper(), font=hn(22, 1), fill=EMAS, anchor="ma")
        d.text((cw / 2, y + 30), bersih(val), font=georgia(32), fill=ink, anchor="ma")
        y += 86
    y += 6
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), cw - 160, chh - 110 - y, 26, 18, 1.36)
    for ln in lines:
        d.text((cw / 2, y), ln, font=f, fill=(110, 100, 90), anchor="ma")
        y += size * 1.36
    d.text((cw / 2, y + 8), p["ref"], font=hn(22, 1), fill=EMAS, anchor="ma")
    bayangan(img, card, (W / 2 - cw / 2, 90), blur=22, geser=(6, 18), kuat=0.4)
    comp(img, segel(150), (W / 2 + cw / 2 - 130, 90 + chh - 120))
    d = ImageDraw.Draw(img)
    d.text((80, H - 50), "@" + HANDLE, font=hn(22, 10), fill=(255, 255, 255, 200))
    return img


# ---------- GLOBE: bola salju, hitung mundur ----------

def bintang4(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r * .18, cy - r * .18), (cx + r, cy), (cx + r * .18, cy + r * .18), (cx, cy + r),
               (cx - r * .18, cy + r * .18), (cx - r, cy), (cx - r * .18, cy - r * .18)], fill=col)


def globe_image(p, i):
    rng = np.random.default_rng(2500 + i)
    bg = gradasi(W, H, (40, 26, 40), (14, 10, 18)).convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bok)
    for _ in range(24):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(20, 70)
        bd.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 130, int(rng.uniform(30, 80))))
    bg.alpha_composite(bok.filter(ImageFilter.GaussianBlur(16)))
    cx, cy, r = W / 2, 470, 330
    # isi bola: langit malam, bintang, kota kecil, salju
    S = 2 * r
    inner = gradasi(S, S, (24, 34, 86), (90, 60, 120)).convert("RGBA")
    idr = ImageDraw.Draw(inner)
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((r - 90, 70, r + 90, 250), fill=(255, 230, 160, 140))
    inner.alpha_composite(glow.filter(ImageFilter.GaussianBlur(30)))
    idr = ImageDraw.Draw(inner)
    bintang4(idr, r, 160, 46, (255, 240, 200, 255))
    num = str(p["angka"])
    idr.text((r, 330), num, font=hn(190, 9), fill=(255, 226, 150, 255), anchor="mm")
    idr.text((r, 440), "HARI LAGI", font=hn(36, 1), fill=(255, 236, 200, 255), anchor="mm")
    kota = [(0, S)] + [(x, S - 120 - (40 if 220 < x < 300 else 0) - (rng.uniform(0, 60) if x % 70 < 35 else 0)) for x in range(0, S + 1, 35)] + [(S, S)]
    idr.polygon(kota, fill=(20, 18, 36, 255))
    idr.polygon([(r - 70, S - 120), (r, S - 190), (r + 70, S - 120)], fill=(30, 26, 50, 255))
    for _ in range(140):
        x, y, s = rng.uniform(0, S), rng.uniform(0, S), rng.uniform(1.5, 4)
        idr.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, int(rng.uniform(120, 230))))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
    ball = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ball.paste(inner, (0, 0), m)
    kil = Image.new("RGBA", (S, S), (0, 0, 0, 0))  # kilau kaca
    kd = ImageDraw.Draw(kil)
    kd.arc((40, 40, S - 40, S - 40), 200, 260, fill=(255, 255, 255, 150), width=18)
    kd.ellipse((S * .2, S * .16, S * .3, S * .26), fill=(255, 255, 255, 120))
    ball.alpha_composite(kil.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(ball).ellipse((2, 2, S - 2, S - 2), outline=(255, 255, 255, 90), width=4)
    bayangan(bg, ball, (cx - r, cy - r), blur=24, geser=(0, 20), kuat=0.4)
    d = ImageDraw.Draw(bg)
    by = cy + r - 40  # alas kayu
    d.polygon([(cx - 260, by), (cx + 260, by), (cx + 300, by + 140), (cx - 300, by + 140)], fill=(110, 66, 40))
    d.rectangle((cx - 300, by + 140, cx + 300, by + 160), fill=(80, 46, 28))
    d.rounded_rectangle((cx - 120, by + 40, cx + 120, by + 100), radius=10, fill=(200, 164, 90))
    d.text((cx, by + 70), "NATAL 2026", font=hn(28, 1), fill=(80, 50, 20), anchor="mm")
    y = by + 200
    d.text((cx, y), "menuju Natal", font=georgia(50, True), fill=(240, 206, 150), anchor="ma")
    y += 78
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 200):
        d.text((cx, y), ln, font=georgia(34), fill=(240, 232, 222), anchor="ma")
        y += 46
    y += 14
    ayat_bawah(bg, p, y, H - 60, (200, 190, 196), (240, 206, 150), start=28, stop=20)
    ImageDraw.Draw(bg).text((cx, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(150, 140, 150), anchor="ma")
    return bg


# ---------- MUSEUM: lukisan di galeri ----------

def cat_minyak(img, rng):
    img = img.filter(ImageFilter.ModeFilter(9)).filter(ImageFilter.SMOOTH_MORE)
    a = np.asarray(img).astype(np.float32)
    h, w = a.shape[:2]
    stroke = render.fbm2d(h, w, rng, ((int(w / 6), 1.0), (int(w / 2), 0.6)))
    a *= (0.92 + 0.16 * stroke)[..., None]
    kanvas = (np.sin(np.arange(w)[None, :] * 1.7) + np.sin(np.arange(h)[:, None] * 1.7)) * 3
    return Image.fromarray(np.clip(a + kanvas[..., None], 0, 255).astype(np.uint8))


def museum_image(p, i):
    rng = np.random.default_rng(2600 + i)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wall = np.zeros((H, W, 3), np.float32) + np.array([236, 230, 220])
    wall *= (0.78 + 0.3 * np.exp(-(((xx - W / 2) / 420) ** 2 + ((yy - 300) / 520) ** 2)))[..., None]
    img = grain(Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8)), 0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 60, W, H), fill=(120, 86, 60))
    pw, ph = 640, 500
    jenis = {"kabut": "fajar"}.get(p["lukisan"], p["lukisan"])  # kabut terlalu datar untuk lukisan
    lukis = cat_minyak(cover(foto_warna(jenis, 900, 700, seed=2650 + i), pw, ph).convert("RGB"), rng)
    fr = 46
    frame = Image.new("RGBA", (pw + 2 * fr, ph + 2 * fr), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    for k in range(fr):  # bingkai emas berlapis
        t = k / fr
        c = tuple(int(v) for v in np.array([120, 88, 40]) * (1 - t) + np.array([226, 190, 110]) * t * (0.8 + 0.2 * math.sin(t * 9)))
        fd.rectangle((k, k, frame.width - 1 - k, frame.height - 1 - k), outline=c + (255,), width=1)
    frame.paste(lukis, (fr, fr))
    bayangan(img, frame, (W / 2 - frame.width / 2, 110), blur=20, geser=(0, 22), kuat=0.45)
    # papan keterangan
    pw2 = 760
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, lines, size = pas(probe, bersih(p["ayat"]), lambda s: georgia(s, True), pw2 - 80, 200, 30, 20, 1.36)
    plh = int(190 + len(lines) * size * 1.36 + 60)
    plak = Image.new("RGBA", (pw2, plh), (250, 250, 248, 255))
    pd = ImageDraw.Draw(plak)
    pd.text((40, 34), bersih(p["judul"]), font=hn(38, 1), fill=(30, 30, 34))
    pd.text((40, 86), bersih(p["tahun"]), font=georgia(28, True), fill=(110, 110, 116))
    pd.text((40, 126), bersih(p["medium"]), font=hn(26, 0), fill=(110, 110, 116))
    pd.line((40, 172, pw2 - 40, 172), fill=(220, 220, 224), width=2)
    y = 190
    for ln in lines:
        pd.text((40, y), ln, font=f, fill=(50, 50, 56))
        y += size * 1.36
    pd.text((40, y + 8), p["ref"], font=hn(24, 1), fill=(30, 30, 34))
    pd.text((pw2 - 30, plh - 26), "@" + HANDLE, font=hn(18, 10), fill=(160, 160, 166), anchor="rs")
    bayangan(img, plak, (W / 2 - pw2 / 2, min(110 + frame.height + 70, H - 90 - plh)), blur=10, geser=(2, 6), kuat=0.25)
    return img


# ---------- KASET: kaset + daftar lagu ----------

KASET_WARNA = [(230, 190, 70), (90, 170, 170), (220, 120, 100), (130, 150, 210), (150, 190, 120), (200, 140, 180), (240, 170, 90)]


def kaset_image(p, i):
    rng = np.random.default_rng(2700 + i)
    bgc = KASET_WARNA[i % 7]
    img = grain(Image.new("RGB", (W, H), bgc), 0.08).convert("RGBA")
    kw, kh = 860, 540
    k = Image.new("RGBA", (kw, kh), (0, 0, 0, 0))
    d = ImageDraw.Draw(k)
    d.rounded_rectangle((0, 0, kw, kh), radius=30, fill=(40, 40, 46, 255))
    d.rounded_rectangle((40, 36, kw - 40, kh - 130), radius=16, fill=(246, 240, 224, 255))
    d.rectangle((40, 100, kw - 40, 110), fill=bgc + (255,))
    d.text((70, 40), "A", font=hn(48, 1), fill=(40, 40, 46))
    fj = ft("/System/Library/Fonts/MarkerFelt.ttc", 50, 1)
    while d.textlength(bersih(p["judul"]), font=fj) > kw - 260:
        fj = ft("/System/Library/Fonts/MarkerFelt.ttc", fj.size - 2, 1)
    d.text((130, 44), bersih(p["judul"]), font=fj, fill=(30, 40, 90))
    d.rounded_rectangle((180, 160, kw - 180, 300), radius=60, fill=(30, 30, 34, 255))
    for cx in (270, kw - 270):
        d.ellipse((cx - 54, 176, cx + 54, 284), fill=(250, 250, 250, 255))
        d.ellipse((cx - 30, 200, cx + 30, 260), fill=(40, 40, 46, 255))
        for a in range(0, 360, 60):
            x, y = cx + 22 * math.cos(math.radians(a)), 230 + 22 * math.sin(math.radians(a))
            d.rectangle((x - 4, y - 4, x + 4, y + 4), fill=(250, 250, 250, 255))
    d.rectangle((330, 200, kw - 330, 262), fill=(90, 60, 40, 255))
    d.polygon([(160, kh), (220, kh - 110), (kw - 220, kh - 110), (kw - 160, kh)], fill=(60, 60, 66, 255))
    for x, y in ((30, 30), (kw - 30, 30), (30, kh - 30), (kw - 30, kh - 30), (kw / 2, kh - 40)):
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(110, 110, 116, 255))
    k = k.rotate(-4, expand=True, resample=Image.BICUBIC)
    bayangan(img, k, (W / 2 - k.width / 2, 70), blur=18, geser=(8, 16), kuat=0.4)
    jc = Image.new("RGBA", (900, 640), (250, 248, 240, 255))
    jd = ImageDraw.Draw(jc)
    jd.rectangle((0, 0, 900, 70), fill=(40, 40, 46, 255))
    jd.text((40, 35), "SISI A  ·  MIXTAPE MINGGU INI", font=hn(26, 1), fill=bgc, anchor="lm")
    y = 100
    for n, lagu in enumerate(p["lagu"], 1):
        jd.text((50, y), f"{n}.", font=tangan(38), fill=(150, 60, 60))
        jd.text((100, y), bersih(lagu), font=tangan(38), fill=(30, 40, 90))
        y += 58
    y += 12
    jd.line((50, y, 850, y), fill=(220, 214, 200), width=2)
    y += 20
    f, lines, size = pas(jd, bersih(p["ayat"]), lambda s: georgia(s, True), 800, 640 - y - 70, 28, 20, 1.36)
    for ln in lines:
        jd.text((50, y), ln, font=f, fill=(70, 66, 60))
        y += size * 1.36
    jd.text((50, y + 6), p["ref"], font=hn(24, 1), fill=(150, 60, 60))
    jd.text((870, 620), "@" + HANDLE, font=hn(18, 10), fill=(160, 156, 150), anchor="rs")
    jc = jc.rotate(2, expand=True, resample=Image.BICUBIC)
    bayangan(img, jc, (W / 2 - jc.width / 2, H - jc.height - 40), blur=16, geser=(6, 12), kuat=0.35)
    return img


# ---------- SERTIFIKAT ----------

def sertifikat_image(p, i):
    rng = np.random.default_rng(2800 + i)
    img = kayu(W, H, rng, (90, 60, 44)).convert("RGBA")
    cw, chh = 960, 1240
    c = np.zeros((chh, cw, 3), np.float32) + np.array([250, 244, 228])
    c *= (0.96 + 0.05 * render.fbm2d(chh, cw, rng, ((5, 1.0), (60, 0.4))))[..., None]
    card = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(card)
    hijau = (40, 90, 80)
    for k in range(6):  # bingkai guilloche
        off = k * 0.9
        for side in range(4):
            pts = []
            for t in np.linspace(0, 1, 300):
                if side in (0, 2):
                    x, y = 40 + t * (cw - 80), (40 if side == 0 else chh - 40) + 12 * math.sin(t * 90 + off)
                else:
                    x, y = (40 if side == 3 else cw - 40) + 12 * math.sin(t * 110 + off), 40 + t * (chh - 80)
                pts.append((x, y))
            d.line(pts, fill=hijau + (120,), width=1)
    d.rectangle((70, 70, cw - 70, chh - 70), outline=hijau, width=3)
    comp(card, mahkota(80), (cw / 2 - 40, 110))
    d = ImageDraw.Draw(card)
    f, lines, size = pas(d, bersih(p["judul"]).upper(), lambda s: ft("BigCaslon.ttf", s), cw - 200, 150, 58, 34, 1.15)
    y = 210
    for ln in lines:
        d.text((cw / 2, y), ln, font=f, fill=hijau, anchor="ma")
        y += size * 1.15
    y += 20
    d.text((cw / 2, y), "dengan ini diberikan kepada", font=georgia(30, True), fill=(110, 100, 90), anchor="ma")
    y += 60
    fn_ = ft("SnellRoundhand.ttc", 110, 1)
    nama = bersih(p["nama"])
    nama = nama.title() if nama.isupper() else nama
    while d.textlength(nama, font=fn_) > cw - 220:
        fn_ = ft("SnellRoundhand.ttc", fn_.size - 4, 1)
    d.text((cw / 2, y + 60), nama, font=fn_, fill=(40, 40, 50), anchor="mm")
    y += 140
    d.line((cw / 2 - 260, y, cw / 2 + 260, y), fill=(150, 140, 120), width=2)
    y += 30
    for ln in wrap(d, bersih(p["isi"]), georgia(32), cw - 240):
        d.text((cw / 2, y), ln, font=georgia(32), fill=(50, 46, 40), anchor="ma")
        y += 44
    y += 20
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), cw - 260, chh - 330 - y, 28, 20, 1.36)
    for ln in lines:
        d.text((cw / 2, y), ln, font=f, fill=(110, 100, 90), anchor="ma")
        y += size * 1.36
    d.text((cw / 2, y + 6), p["ref"], font=hn(24, 1), fill=hijau, anchor="ma")
    sy = chh - 210
    d.line((120, sy, 440, sy), fill=(60, 60, 60), width=2)
    d.text((280, sy + 14), bersih(p["dasar"]), font=georgia(24, True), fill=(90, 86, 80), anchor="ma")
    d.text((280, sy - 50), f"{22 + i} November 2026", font=tangan(34), fill=(36, 52, 110), anchor="ma")

    def meterai(dd, k):
        S = 240 * k
        c0 = S / 2
        for side, ang in ((-1, 70), (1, 110)):
            a = math.radians(ang)
            x0, y0 = c0 + side * 30 * k, c0 + 40 * k
            dd.polygon([(x0 - 22 * k, y0), (x0 + 22 * k, y0), (x0 + 22 * k + math.cos(a) * 90 * k * -side * 0.3, y0 + 110 * k),
                        (x0, y0 + 90 * k), (x0 - 22 * k + math.cos(a) * 90 * k * -side * 0.3, y0 + 110 * k)], fill=(150, 30, 40, 255))
        pts = [(c0 + c0 * .7 * (1 if j % 2 == 0 else .88) * math.cos(math.pi * j / 18), c0 * .85 + c0 * .7 * (1 if j % 2 == 0 else .88) * math.sin(math.pi * j / 18)) for j in range(36)]
        dd.polygon(pts, fill=(206, 168, 80, 255))
        dd.ellipse((c0 - 62 * k, c0 * .85 - 62 * k, c0 + 62 * k, c0 * .85 + 62 * k), outline=(150, 116, 50, 255), width=int(4 * k))
        dd.rectangle((c0 - 7 * k, c0 * .85 - 40 * k, c0 + 7 * k, c0 * .85 + 40 * k), fill=(150, 116, 50, 255))
        dd.rectangle((c0 - 28 * k, c0 * .85 - 18 * k, c0 + 28 * k, c0 * .85 - 4 * k), fill=(150, 116, 50, 255))
    comp(card, sprite(240, 240, meterai), (cw - 340, chh - 330))
    card = card.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    bayangan(img, card, ((W - card.width) // 2, (H - card.height) // 2), blur=20, geser=(8, 16), kuat=0.5)
    ImageDraw.Draw(img).text((W - 40, H - 14), "@" + HANDLE, font=hn(20, 10), fill=(220, 200, 180), anchor="rs")
    return img


# ---------- JENDELA: jendela berembun ----------

def jendela_image(p, i):
    rng = np.random.default_rng(2900 + i)
    wh = 1040
    sky = np.asarray(gradasi(W, wh, (10, 16, 44), (36, 40, 86))).astype(np.float32)
    yy, xx = np.mgrid[0:wh, 0:W].astype(np.float32)
    mx, my = W * (0.72 if i % 2 else 0.28), 230
    sky += (np.exp(-((xx - mx) ** 2 + (yy - my) ** 2) / (2 * 160.0 ** 2)) * 70)[..., None]
    scene = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8)).convert("RGBA")
    sd = ImageDraw.Draw(scene)
    for _ in range(90):
        x, y, s = rng.uniform(0, W), rng.uniform(0, wh * 0.6), rng.uniform(1, 2.6)
        sd.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 240, int(rng.uniform(120, 255))))
    sd.ellipse((mx - 60, my - 60, mx + 60, my + 60), fill=(250, 244, 220, 255))
    sd.polygon([(0, wh)] + [(x, wh - 160 - rng.uniform(0, 140) * (x % 90 < 50)) for x in range(0, W + 1, 45)] + [(W, wh)], fill=(14, 14, 26, 255))
    lamp = Image.new("RGBA", (W, wh), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lamp)
    for _ in range(60):
        x, y, s = rng.uniform(0, W), rng.uniform(wh - 280, wh - 20), rng.uniform(3, 9)
        ld.ellipse((x - s, y - s, x + s, y + s), fill=(255, 200, 120, int(rng.uniform(120, 230))))
    scene.alpha_composite(lamp.filter(ImageFilter.GaussianBlur(3)))
    # embun + tulisan jari
    fog = render.fbm2d(wh, W, rng, ((6, 1.0), (40, 0.6), (200, 0.4)))
    fog_a = (0.7 + 0.28 * fog) * 255
    tulis = Image.new("L", (W, wh), 0)
    td = ImageDraw.Draw(tulis)
    teks = bersih(p["teks"])
    f = ft("Bradley Hand Bold.ttf", 130)
    lines = wrap(td, teks, f, W - 220)
    while len(lines) > 2 or max(td.textlength(x, font=f) for x in lines) > W - 220:
        f = ft("Bradley Hand Bold.ttf", f.size - 6)
        lines = wrap(td, teks, f, W - 220)
    y = wh * 0.5 - len(lines) * f.size * 0.6
    for ln in lines:
        td.text((W / 2, y), ln, font=f, fill=255, anchor="ma", stroke_width=7, stroke_fill=255)
        y += f.size * 1.2
    for _ in range(14):  # tetesan air dari huruf
        ys_, xs_ = np.nonzero(np.asarray(tulis)[::7, ::7])
        if len(xs_) == 0:
            break
        j = int(rng.integers(len(xs_)))
        x0, y0 = xs_[j] * 7, ys_[j] * 7
        td.line((x0, y0, x0 + rng.uniform(-3, 3), y0 + rng.uniform(40, 160)), fill=200, width=int(rng.integers(4, 9)))
    clear = np.asarray(tulis.filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255
    fog_l = Image.fromarray(np.clip(fog_a * (1 - clear), 0, 255).astype(np.uint8))
    blurred = scene.filter(ImageFilter.GaussianBlur(14))
    white = Image.new("RGBA", (W, wh), (200, 210, 225, 255))
    foggy = Image.blend(blurred, white, 0.5)
    out = scene.copy()
    out.paste(foggy, (0, 0), fog_l)
    img = Image.new("RGBA", (W, H), (60, 40, 30, 255))
    img.paste(out, (0, 0))
    d = ImageDraw.Draw(img)
    wood = (70, 46, 32)
    d.rectangle((0, 0, W, 26), fill=wood)
    d.rectangle((0, 0, 26, wh), fill=wood)
    d.rectangle((W - 26, 0, W, wh), fill=wood)
    d.rectangle((0, wh - 10, W, wh + 40), fill=(96, 64, 44))
    d.rectangle((0, wh + 40, W, wh + 48), fill=(50, 32, 22))
    ruang = np.zeros((H - wh - 48, W, 3), np.float32) + np.array([44, 30, 24])
    img.paste(Image.fromarray(ruang.astype(np.uint8)), (0, wh + 48))
    ayat_bawah(img, p, wh + 80, H - 40, (236, 222, 200), (230, 180, 120), start=30, stop=20)
    ImageDraw.Draw(img).text((W - 40, H - 16), "@" + HANDLE, font=hn(18, 10), fill=(150, 120, 100), anchor="rs")
    return img


# ---------- PROGRESS (Reels): bilah instalasi ----------

def kado(s):
    def g(d, k):
        S = s * k
        d.rounded_rectangle((S * .1, S * .38, S * .9, S * .95), radius=S * .06, fill=(200, 50, 60, 255))
        d.rounded_rectangle((S * .04, S * .26, S * .96, S * .42), radius=S * .05, fill=(220, 66, 76, 255))
        d.rectangle((S * .44, S * .26, S * .56, S * .95), fill=(240, 196, 80, 255))
        d.ellipse((S * .24, S * .06, S * .5, S * .3), outline=(240, 196, 80, 255), width=int(S * .06))
        d.ellipse((S * .5, S * .06, S * .76, S * .3), outline=(240, 196, 80, 255), width=int(S * .06))
    return sprite(s, s, g)


def progress_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/progress{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    bg = gradasi(RW, RH, (226, 220, 246), (196, 214, 244)).convert("RGBA")
    ww, wy = 900, 560
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, lines, size = pas(probe, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), ww - 120, 360, 40, 28, 1.36)
    vcard = Image.new("RGBA", (ww, int(len(lines) * size * 1.36 + 150)), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vcard)
    vd.rounded_rectangle((0, 0, vcard.width, vcard.height), radius=30, fill=(255, 255, 255, 235))
    y = 50
    for ln in lines:
        vd.text((ww / 2, y), ln, font=f, fill=(40, 40, 60), anchor="ma")
        y += size * 1.36
    vd.text((ww / 2, y + 12), p["ref"], font=hn(32, 1), fill=(90, 70, 190), anchor="ma")
    icon = kado(150)

    def nilai(t):  # progres 18% di sampul -> 100% di 7 detik, sempat tertahan di 62%
        if t < 3.2:
            return 0.18 + 0.44 * ease(t / 3.2)
        if t < 4.2:
            return 0.62 + 0.02 * (t - 3.2)
        return min(1.0, 0.64 + 0.36 * ease((t - 4.2) / 2.8))

    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        win = Image.new("RGBA", (ww, 640), (0, 0, 0, 0))
        wd = ImageDraw.Draw(win)
        wd.rounded_rectangle((0, 0, ww, 640), radius=34, fill=(255, 255, 255, 255))
        wd.rounded_rectangle((0, 0, ww, 70), radius=34, fill=(244, 244, 248, 255))
        wd.rectangle((0, 40, ww, 70), fill=(244, 244, 248, 255))
        for k, c in enumerate([(255, 96, 92), (255, 190, 46), (40, 200, 64)]):
            wd.ellipse((30 + k * 36, 24, 52 + k * 36, 46), fill=c)
        wd.text((ww / 2, 35), "Penginstal", font=hn(26, 10), fill=(110, 110, 120), anchor="mm")
        win.alpha_composite(icon, (ww // 2 - 75, 100))
        wd.text((ww / 2, 290), bersih(p["judul"]), font=hn(44, 1), fill=(30, 30, 40), anchor="ma")
        v = nilai(t)
        selesai = t >= 7.2
        wd.rounded_rectangle((70, 400, ww - 70, 428), radius=14, fill=(230, 230, 238, 255))
        wd.rounded_rectangle((70, 400, 70 + (ww - 140) * v, 428), radius=14, fill=(110, 90, 220, 255))
        if not selesai:
            status = bersih(p["langkah"][min(3, int((v - 0.18) / 0.82 * 4))])
            wd.text((70, 450), status, font=hn(32, 0), fill=(90, 90, 100))
            wd.text((ww - 70, 450), f"{int(v * 100)}%", font=hn(32, 1), fill=(110, 90, 220), anchor="ra")
        else:
            a = ease((t - 7.2) / 0.4)
            r = 34 * a
            wd.ellipse((ww / 2 - r, 550 - r, ww / 2 + r, 550 + r), fill=(46, 170, 90, 255))
            if a > 0.6:
                wd.line((ww / 2 - 15, 550, ww / 2 - 4, 562, ww / 2 + 17, 536), fill="white", width=7, joint="curve")
            wd.text((ww / 2, 446), bersih(p["selesai"]), font=hn(34, 1), fill=(46, 140, 80), anchor="ma")
        bayangan(frame, win, ((RW - ww) // 2, wy), blur=26, geser=(0, 16), kuat=0.25)
        if t >= 8.0:
            a = ease((t - 8.0) / 0.5)
            comp(frame, fade(vcard, a), ((RW - ww) // 2, wy + 700 + (1 - a) * 50))
        ImageDraw.Draw(frame).text((RW / 2, 380), "@" + HANDLE, font=hn(28, 10), fill=(110, 100, 150), anchor="ma")
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- GOSOK (Reels): kartu gosok ----------

def gosok_reel(p, idx, mod=MOD, seconds=12, natal=False):
    rel = f"reels/{mod}/gosok{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(3000 + idx)
    warna = [(22, 92, 70), (150, 30, 44), (30, 60, 120), (110, 40, 110), (20, 100, 110), (170, 90, 30), (60, 70, 40)][idx % 7]
    if natal:
        warna = [(150, 30, 44), (22, 92, 70), (160, 110, 30)][idx % 3]
    bg = (kertas_kado(RW, RH, idx) if natal else gradasi(RW, RH, tuple(min(255, c + 30) for c in warna), tuple(int(c * 0.6) for c in warna))).convert("RGBA")
    bd = ImageDraw.Draw(bg)
    for _ in range(90):
        x, y, s = rng.uniform(0, RW), rng.uniform(0, RH), rng.uniform(4, 10)
        bd.rectangle((x, y, x + s, y + s * 2), fill=[(255, 220, 120), (255, 255, 255), (255, 160, 170)][int(rng.integers(3))] + (90,))
    cw, chh, cx0, cy0 = 880, 1120, (RW - 880) // 2, 330
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, cw, chh), radius=40, fill=(255, 252, 244, 255))
    cd.text((cw / 2, 60), bersih(p["atas"]), font=hn(42, 1), fill=warna, anchor="ma")
    cd.text((cw / 2, 124), "@" + HANDLE, font=hn(26, 10), fill=(150, 150, 150), anchor="ma")
    px0, py0, pw, ph = 60, 200, cw - 120, chh - 260
    cd.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=26, fill=(255, 246, 220, 255))
    f, lines, size = pas(cd, bersih(p["hadiah"]), lambda s: hn(s, 1), pw - 100, 300, 76, 40, 1.15)
    f2, l2, s2 = pas(cd, bersih(p["ayat"]), lambda s: georgia(s, True), pw - 100, ph - 200 - len(lines) * size * 1.15, 36, 24, 1.36)
    tinggi = len(lines) * size * 1.15 + 30 + len(l2) * s2 * 1.36 + 50
    y = py0 + max(50, (ph - tinggi) / 2)
    for ln in lines:
        cd.text((cw / 2, y), ln, font=f, fill=warna, anchor="ma")
        y += size * 1.15
    y += 30
    for ln in l2:
        cd.text((cw / 2, y), ln, font=f2, fill=(60, 56, 50), anchor="ma")
        y += s2 * 1.36
    cd.text((cw / 2, y + 10), p["ref"], font=hn(30, 1), fill=warna, anchor="ma")
    perak = np.zeros((ph, pw, 3), np.float32)
    g_ = np.linspace(0, 1, pw)[None, :]
    perak += (np.array([196, 198, 204]) * (0.85 + 0.25 * np.sin(g_ * 6 + np.linspace(0, 2, ph)[:, None]))[..., None])
    perak += (rng.random((ph, pw)) * 24 - 12)[..., None]
    silver = Image.fromarray(np.clip(perak, 0, 255).astype(np.uint8)).convert("RGBA")
    sd = ImageDraw.Draw(silver)
    for k in range(0, pw + ph, 60):
        sd.line((k, 0, k - ph, ph), fill=(220, 222, 228, 120), width=10)
    sd.text((pw / 2, ph / 2 - 30), "GOSOK DI SINI", font=hn(72, 9), fill=(70, 72, 82, 255), anchor="mm", stroke_width=4, stroke_fill=(236, 238, 242, 255))
    sd.text((pw / 2, ph / 2 + 46), "pesan untukmu", font=hn(36, 1), fill=(70, 72, 82, 255), anchor="mm", stroke_width=3, stroke_fill=(236, 238, 242, 255))
    m_ = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m_).rounded_rectangle((0, 0, pw, ph), radius=26, fill=255)
    silver.putalpha(m_)
    # jalur gosok zig-zag
    rows = 9
    path = []
    for r in range(rows):
        y = (r + 0.5) * ph / rows
        xs = (40, pw - 40) if r % 2 == 0 else (pw - 40, 40)
        path += [(xs[0], y), (xs[1], y + ph / rows * 0.3)]
    seg = [math.dist(path[j], path[j + 1]) for j in range(len(path) - 1)]
    total = sum(seg)

    def titik(dist):
        for j, L in enumerate(seg):
            if dist <= L:
                a = dist / L
                return path[j][0] + (path[j + 1][0] - path[j][0]) * a, path[j][1] + (path[j + 1][1] - path[j][1]) * a
            dist -= L
        return path[-1]
    mask = Image.new("L", (pw, ph), 0)
    md = ImageDraw.Draw(mask)
    t0, t1 = 0.8, 5.2
    done = 0.0
    koin = sprite(90, 90, lambda dd, k: (dd.ellipse((0, 0, 90 * k, 90 * k), fill=(214, 172, 70, 255)),
                                         dd.ellipse((10 * k, 10 * k, 80 * k, 80 * k), outline=(170, 130, 40, 255), width=int(4 * k))))
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        target = total * min(1, max(0, (t - t0) / (t1 - t0)))
        while done < target:
            x, y = titik(done)
            r = 52 + rng.uniform(-6, 6)
            md.ellipse((x - r, y - r, x + r, y + r), fill=255)
            done += 12
        frame = bg.copy()
        c = card.copy()
        s = silver.copy()
        a = np.asarray(s.getchannel("A")).astype(np.float32) * (1 - np.asarray(mask).astype(np.float32) / 255)
        if t > t1 + 0.2:
            a *= max(0.0, 1 - (t - t1 - 0.2) / 0.5)
        s.putalpha(Image.fromarray(a.astype(np.uint8)))
        c.alpha_composite(s, (px0, py0))
        bayangan(frame, c, (cx0, cy0), blur=26, geser=(0, 18), kuat=0.35)
        if t0 <= t <= t1:
            x, y = titik(done)
            comp(frame, koin, (cx0 + px0 + x - 45, cy0 + py0 + y - 45))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- semua ----------

SIMPLE = {"JAM": jam_image, "NAMA": nama_image, "RAMBU": rambu_image, "RESEP": resep_image, "UNDANGAN": undangan_image,
          "GLOBE": globe_image, "MUSEUM": museum_image, "KASET": kaset_image, "SERTIFIKAT": sertifikat_image,
          "JENDELA": jendela_image}
REELS = {"PROGRESS": progress_reel, "GOSOK": gosok_reel}


def render_week(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt in SIMPLE:
                p = getattr(t, fmt)[idx]
                out[(hari, slot)] = ([save(SIMPLE[fmt](p, idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt in REELS:
                rel = f"reels/{mod}/{fmt.lower()}{idx + 1}.mp4"
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], getattr(t, fmt)[idx]["caption"])
            elif fmt == "ELI":
                import tenang_eli
                out[(hari, slot)] = tenang_eli.render_item(t.ELI[idx])
    return out


def render_reels(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt in REELS:
                rel = REELS[fmt](getattr(t, fmt)[idx], idx, mod)
                tambah_musik(rel)
                print(rel, flush=True)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
