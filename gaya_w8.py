"""Akun Tenang - minggu 8 (konten/tenang_w8.py): 12 gaya baru, satu gaya per slot.
KORAN (halaman depan koran "Kabar Baik"), LETTER (papan huruf felt), KUIS (kuis Alkitab 2 slide), STICKY (catatan tempel di kulkas),
MENU (papan kapur kafe), SEARCH (Reels mesin pencari), ORNAMEN (bola hiasan Natal, hitung mundur), KODE (editor kode),
KARTUPOS (kartu pos tulisan tangan), FLIP (Reels papan huruf bandara), PETA (aplikasi peta), LILIN (lilin di malam hari).
Komik Eli 3x seminggu.

  python3 gaya_w8.py [reels]
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
from gaya_w7 import (bayangan, bersih, comp, ease, fade, ft, gradasi, pas, selotip, sprite, tangan, tanpa_kutip,
                     vintage)
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w8"
RW, RH, FPS = 1080, 1920, 30
HARI = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
ADEGAN = ["fajar", "laut", "kabut", "bintang"]


def tanggal(i):
    return f"{HARI[i % 7]}, {15 + i} November 2026"


def justify(d, x, y, text, f, width, lh, fill):
    lines = wrap(d, text, f, width)
    for k, ln in enumerate(lines):
        words = ln.split()
        if k == len(lines) - 1 or len(words) == 1:
            d.text((x, y), ln, font=f, fill=fill)
        else:
            gap = (width - sum(d.textlength(w_, font=f) for w_ in words)) / (len(words) - 1)
            xx = x
            for w_ in words:
                d.text((xx, y), w_, font=f, fill=fill)
                xx += d.textlength(w_, font=f) + gap
        y += lh
    return y


# ---------- KORAN: halaman depan "Kabar Baik" ----------

KERTAS, TINTA = (236, 230, 214), (34, 30, 26)


def halftone(img, w, h, cell=9):
    g = np.asarray(cover(img, w, h).convert("L")).astype(np.float32) / 255
    out = Image.new("RGB", (w, h), KERTAS)
    d = ImageDraw.Draw(out)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            r = (1 - g[y:y + cell, x:x + cell].mean()) * cell * 0.62
            if r > 0.4:
                d.ellipse((x + cell / 2 - r, y + cell / 2 - r, x + cell / 2 + r, y + cell / 2 + r), fill=TINTA)
    return out


def koran_image(p, i):
    rng = np.random.default_rng(1100 + i)
    base = np.zeros((H, W, 3), np.float32) + np.array(KERTAS)
    base *= (0.93 + 0.1 * render.fbm2d(H, W, rng, ((4, 1.0), (30, 0.4))))[..., None]
    yy = np.arange(H, dtype=np.float32)[:, None]
    base *= (1 - 0.05 * np.exp(-((yy - H * 0.52) / 14) ** 2))[..., None]  # bekas lipatan
    img = grain(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), 0.07)
    d = ImageDraw.Draw(img)
    x0, x1 = 60, W - 60
    tnr = lambda s, b=False: ft("Times New Roman Bold.ttf" if b else "Times New Roman.ttf", s)
    d.text((W / 2, 52), f"EDISI KHUSUS  ·  {tanggal(i).upper()}  ·  GRATIS", font=tnr(22, True), fill=TINTA, anchor="ma")
    d.line((x0, 88, x1, 88), fill=TINTA, width=2)
    d.text((W / 2, 98), "KABAR BAIK", font=ft("BigCaslon.ttf", 128), fill=TINTA, anchor="ma")
    d.line((x0, 250, x1, 250), fill=TINTA, width=4)
    d.line((x0, 258, x1, 258), fill=TINTA, width=1)
    d.text((x0, 268), "Untuk semua orang, setiap hari", font=georgia(24, True), fill=TINTA)
    d.text((x1, 268), "@" + HANDLE, font=tnr(24, True), fill=TINTA, anchor="ra")
    d.line((x0, 306, x1, 306), fill=TINTA, width=1)
    f, lines, size = pas(d, bersih(p["judul"]), lambda s: tnr(s, True), x1 - x0, 200, 92, 52, 1.02)
    y = 330
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=TINTA, anchor="ma")
        y += size * 1.02
    y += 14
    for ln in wrap(d, bersih(p["sub"]), georgia(34, True), x1 - x0 - 40):
        d.text((W / 2, y), ln, font=georgia(34, True), fill=(70, 62, 54), anchor="ma")
        y += 44
    y += 22
    d.line((x0, y, x1, y), fill=TINTA, width=2)
    y += 28
    colw = (x1 - x0 - 50) // 2
    xr = x0 + colw + 50
    # kolom kiri: berita (huruf awal besar)
    isi = bersih(p["isi"])
    fv = georgia(28, True)
    batas = H - 56 - (len(wrap(d, bersih(p["ayat"]), fv, x1 - x0 - 80)) * 38 + 130) - 20  # kotak ayat harus muat
    for ukuran in range(30, 21, -1):
        fb = tnr(ukuran)
        if y + (len(wrap(d, isi, fb, colw)) + 2) * ukuran * 1.34 <= batas:
            break
    lh_isi = ukuran * 1.34
    cap = isi[0]
    fc = tnr(112, True)
    d.text((x0, y - 8), cap, font=fc, fill=TINTA)
    cw = d.textlength(cap, font=fc) + 10
    words, lines2, cur = isi[1:].split(), [], ""
    yl = y
    for wd in words:  # tiga baris pertama menyempit di samping huruf awal
        maxw = colw - cw if len(lines2) < 3 else colw
        trial = f"{cur} {wd}".strip()
        if d.textlength(trial, font=fb) <= maxw:
            cur = trial
        else:
            lines2.append(cur)
            cur = wd
    lines2.append(cur)
    for k, ln in enumerate(lines2):
        lx = x0 + cw if k < 3 else x0
        width = colw - cw if k < 3 else colw
        ws = ln.split()
        if k < len(lines2) - 1 and len(ws) > 1:
            gap = (width - sum(d.textlength(w_, font=fb) for w_ in ws)) / (len(ws) - 1)
            xx = lx
            for w_ in ws:
                d.text((xx, yl), w_, font=fb, fill=TINTA)
                xx += d.textlength(w_, font=fb) + gap
        else:
            d.text((lx, yl), ln, font=fb, fill=TINTA)
        yl += lh_isi
    # kolom kanan: foto raster + kotak ayat
    y = int(y)
    ph = int(max(230, min(380, yl - y - 36)))
    img.paste(halftone(foto_warna(("fajar", "laut")[i % 2], 700, 460, seed=1150 + i), colw, ph), (xr, y))
    d.rectangle((xr, y, xr + colw, y + ph), outline=TINTA, width=2)
    d.text((xr, y + ph + 6), "Ilustrasi", font=georgia(20, True), fill=(90, 80, 70))
    by = int(max(yl, y + ph + 36) + 20)
    d.line((x0 + colw + 25, y, x0 + colw + 25, by - 20), fill=(150, 140, 126), width=1)
    # kotak ayat selebar halaman
    d.rectangle((x0, by, x1, H - 56), outline=TINTA, width=3)
    d.rectangle((x0 + 6, by + 6, x1 - 6, H - 62), outline=TINTA, width=1)
    d.text((W / 2, by + 22), "AYAT HARI INI", font=tnr(28, True), fill=TINTA, anchor="ma")
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), x1 - x0 - 80, H - 56 - by - 120, 34, 20, 1.34)
    yv = by + 68
    for ln in lines:
        d.text((W / 2, yv), ln, font=f, fill=TINTA, anchor="ma")
        yv += size * 1.34
    d.text((W / 2, yv + 8), "— " + p["ref"], font=tnr(28, True), fill=TINTA, anchor="ma")
    return img


# ---------- LETTER: papan huruf felt ----------

DINDING = [(232, 214, 200), (205, 220, 214), (226, 222, 236), (240, 226, 196), (214, 226, 236), (236, 210, 206), (222, 230, 210)]


def kayu(w, h, rng, warna=(176, 128, 82)):
    n = render.fbm2d(h, w, rng, ((3, 1.0), (200, 0.6)))
    grain_ = np.sin(np.linspace(0, 60, w)[None, :] + 8 * render.fbm2d(h, w, rng, ((4, 1.0),))) * 0.5 + 0.5
    arr = np.array(warna, np.float32) * (0.8 + 0.2 * n[..., None] + 0.12 * grain_[..., None])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def letter_image(p, i):
    rng = np.random.default_rng(1200 + i)
    img = grain(Image.new("RGB", (W, H), DINDING[i % 7]), 0.05).convert("RGBA")
    bw, bh, fr = 880, 1060, 34
    board = kayu(bw, bh, rng).convert("RGBA")
    felt = np.zeros((bh - 2 * fr, bw - 2 * fr, 3), np.float32) + 30
    felt *= (0.85 + 0.3 * render.fbm2d(bh - 2 * fr, bw - 2 * fr, rng, ((40, 1.0), (300, 0.8))))[..., None]
    pitch = 30
    for yy in range(0, felt.shape[0], pitch):
        felt[yy:yy + 3] *= 0.55
        felt[yy + 3:yy + 5] *= 1.25
    board.paste(Image.fromarray(np.clip(felt, 0, 255).astype(np.uint8)), (fr, fr))
    d = ImageDraw.Draw(board)
    lines = bersih(p["teks"]).upper().split("\n")
    size = 86
    while max(d.textlength(ln, font=hn(size, 1)) + len(ln) * size * 0.08 for ln in lines) > bw - 2 * fr - 80:
        size -= 2
    f = hn(size, 1)
    rows = len(lines) + 1
    lh = math.ceil(size * 1.25 / pitch) * pitch
    top = fr + ((bh - 2 * fr) - rows * lh) // 2 // pitch * pitch + pitch // 2
    huruf = Image.new("RGBA", board.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(huruf)

    def tulis(teks, y, font, track):
        tw = sum(hd.textlength(c, font=font) + track for c in teks) - track
        x = bw / 2 - tw / 2
        for c in teks:
            dy = rng.uniform(-2, 2)
            hd.text((x + 3, y + dy + 4), c, font=font, fill=(0, 0, 0, 120))
            hd.text((x, y + dy), c, font=font, fill=(246, 244, 238, 255))
            x += hd.textlength(c, font=font) + track
    for k, ln in enumerate(lines):
        tulis(ln, top + k * lh, f, size * 0.08)
    fs = hn(int(size * 0.55), 1)
    ref = p["ref"].upper()
    while hd.textlength(ref, font=fs) > bw - 2 * fr - 120:
        fs = hn(fs.size - 2, 1)
    tulis(ref, top + len(lines) * lh + lh * 0.25, fs, fs.size * 0.1)
    board.alpha_composite(huruf.filter(ImageFilter.GaussianBlur(0.4)))
    bayangan(img, board, ((W - bw) // 2, 110), blur=28, geser=(10, 24), kuat=0.45)
    d = ImageDraw.Draw(img)
    d.text((W / 2, H - 70), "@" + HANDLE, font=hn(24, 10), fill=(110, 100, 92), anchor="ma")
    return img


# ---------- KUIS: kuis Alkitab 2 slide ----------

KUIS_WARNA = [((255, 214, 102), (40, 34, 20)), ((150, 210, 255), (16, 34, 60)), ((255, 170, 160), (60, 20, 20)), ((180, 230, 170), (20, 50, 20))]


def kuis_slide(p, i, jawab):
    bg, ink = KUIS_WARNA[i % 4]
    img = grain(Image.new("RGB", (W, H), bg), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    lab = "KUIS ALKITAB" if not jawab else "JAWABANNYA…"
    f = hn(28, 1)
    tw = d.textlength(lab, font=f)
    d.rounded_rectangle((70, 70, 70 + tw + 50, 124), radius=27, fill=ink)
    d.text((95, 97), lab, font=f, fill=bg, anchor="lm")
    d.text((W - 70, 97), "@" + HANDLE, font=hn(24, 10), fill=ink, anchor="rm")
    y = 170
    f, lines, size = pas(d, bersih(p["tanya"]), lambda s: hn(s, 1), W - 140, 300 if not jawab else 160, 66 if not jawab else 52, 36, 1.18)
    for ln in lines:
        d.text((70, y), ln, font=f, fill=ink)
        y += size * 1.18
    y += 30
    benar = p["jawab"]
    ch = 124 if not jawab else 80
    for k, opt in enumerate(p["pilihan"]):
        if jawab and k != benar:
            fill, tc, lc = (255, 255, 255, 110), ink + (110,), ink + (110,)
        elif jawab:
            fill, tc, lc = (46, 160, 90, 255), (255, 255, 255, 255), (255, 255, 255, 255)
        else:
            fill, tc, lc = (255, 255, 255, 235), ink + (255,), ink + (255,)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((70, y, W - 70, y + ch), radius=26, fill=fill)
        ld.ellipse((96, y + ch / 2 - 26, 148, y + ch / 2 + 26), outline=lc, width=4)
        ld.text((122, y + ch / 2), "ABCD"[k], font=hn(30, 1), fill=lc, anchor="mm")
        fo = hn(44 if not jawab else 34, 10)
        ld.text((176, y + ch / 2), bersih(opt), font=fo, fill=tc, anchor="lm")
        if jawab and k == benar:
            ld.line((W - 150, y + ch / 2, W - 128, y + ch / 2 + 20, W - 96, y + ch / 2 - 20), fill="white", width=8, joint="curve")
        img.alpha_composite(lay)
        y += ch + 18
    d = ImageDraw.Draw(img)
    if not jawab:
        d.text((W / 2, H - 150), "Tulis jawabanmu di komentar", font=hn(34, 10), fill=ink, anchor="ma")
        d.text((W / 2, H - 100), "lalu geser untuk lihat jawabannya  ›", font=hn(30, 0), fill=ink, anchor="ma")
        return img
    y += 14
    for ln in wrap(d, bersih(p["penjelasan"]), hn(32, 0), W - 140):
        d.text((70, y), ln, font=hn(32, 0), fill=ink)
        y += 42
    y += 20
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: georgia(s, True), W - 220, H - 90 - y - 110, 34, 22, 1.36)
    box = (70, y, W - 70, y + len(lines) * size * 1.36 + 100)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, radius=26, fill=(255, 255, 255, 200))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    yy = y + 32
    for ln in lines:
        d.text((110, yy), ln, font=f, fill=ink)
        yy += size * 1.36
    d.text((110, yy + 6), p["ref"], font=hn(28, 1), fill=ink)
    return img


def kuis_files(p, i, mod):
    return [save(kuis_slide(p, i, False), f"{mod}/kuis{i + 1}_1.jpg"), save(kuis_slide(p, i, True), f"{mod}/kuis{i + 1}_2.jpg")]


# ---------- STICKY: catatan tempel di kulkas ----------

POSTIT = [(255, 236, 120), (255, 182, 200), (166, 216, 255), (190, 236, 170)]


def postit(w, h, col, teks, font, ink=(40, 40, 60), rng=None):
    n = Image.new("RGBA", (w, h), col + (255,))
    a = np.asarray(n).astype(np.float32)
    yy = np.linspace(0, 1, h)[:, None]
    a[..., :3] *= (1 - 0.1 * yy ** 3)[..., None]  # ujung bawah sedikit melengkung
    n = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(n)
    y = 46
    lh = font.size * 1.25
    for ln in teks:
        d.text((34, y), ln, font=font, fill=ink)
        y += lh
    return n


def sticky_image(p, i):
    rng = np.random.default_rng(1300 + i)
    xs = np.linspace(0, 1, W)[None, :, None]
    base = np.zeros((H, W, 3), np.float32) + np.array([236, 236, 232])
    base *= 0.92 + 0.08 * xs
    base *= (0.98 + 0.03 * render.fbm2d(H, W, rng, ((2, 1.0), (400, 0.3))))[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((26, 120, 58, H - 120), radius=16, fill=(196, 198, 202))  # pegangan kulkas
    d.rounded_rectangle((30, 124, 46, H - 124), radius=8, fill=(226, 228, 232))
    fonts = [tangan(40), ft("Bradley Hand Bold.ttf", 40), ft("/System/Library/Fonts/MarkerFelt.ttc", 40, 0)]
    pos = [(100, 110, -4, 400), (580, 90, 3, 400), (110, 600, -2, 400)]
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for k, (teks, (x, y, rot, s)) in enumerate(zip(p["catatan"], pos)):
        f = fonts[k % 3]
        lines = wrap(probe, bersih(teks), f, s - 70)
        while len(lines) * f.size * 1.25 > s - 90:
            f = f.font_variant(size=f.size - 2)
            lines = wrap(probe, bersih(teks), f, s - 70)
        n = postit(s, s, POSTIT[(k + i) % 4], lines, f).rotate(rot, expand=True, resample=Image.BICUBIC)
        bayangan(img, n, (x, y), blur=10, geser=(4, 10), kuat=0.35)
        d = ImageDraw.Draw(img)
        mx, my = x + n.width / 2, y + 22
        d.ellipse((mx - 20, my - 20, mx + 20, my + 20), fill=[(220, 60, 60), (60, 120, 220), (240, 180, 40)][k % 3])
        d.ellipse((mx - 12, my - 14, mx - 2, my - 4), fill=(255, 255, 255))
    # catatan besar: ayat
    nw, nh = 480, 600
    f, lines, size = pas(probe, bersih(p["ayat"]), tangan, nw - 70, nh - 170, 40, 26, 1.25)
    big = postit(nw, nh, POSTIT[(3 + i) % 4], lines, f)
    bd = ImageDraw.Draw(big)
    bd.text((nw - 34, nh - 60), "— " + p["ref"], font=tangan(min(size + 2, 36)), fill=(40, 40, 60), anchor="ra")
    big = big.rotate(2.5, expand=True, resample=Image.BICUBIC)
    bayangan(img, big, (530, 590), blur=12, geser=(5, 12), kuat=0.38)
    tp = selotip(150, 46, rng)
    comp(img, tp, (530 + big.width / 2 - tp.width / 2, 572))
    d = ImageDraw.Draw(img)
    d.text((300, H - 64), "@" + HANDLE, font=hn(22, 10), fill=(150, 150, 154), anchor="ma")
    return img


# ---------- MENU: papan kapur kafe ----------

def kapur(layer, rng):
    a = np.asarray(layer.getchannel("A")).astype(np.float32)
    a *= 0.5 + 0.5 * rng.random(a.shape)
    layer.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))
    return layer


def menu_image(p, i):
    rng = np.random.default_rng(1400 + i)
    img = kayu(W, H, rng, (120, 82, 50)).convert("RGBA")
    fr = 46
    bw, bh = W - 2 * fr, H - 2 * fr
    board = np.zeros((bh, bw, 3), np.float32) + np.array([40, 52, 44])
    smudge = render.fbm2d(bh, bw, rng, ((3, 1.0), (12, 0.6), (50, 0.3)))
    board += (smudge[..., None] - 0.45) * 60
    img.paste(Image.fromarray(np.clip(board, 0, 255).astype(np.uint8)), (fr, fr))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    putih, kuning, pink = (246, 244, 236, 255), (250, 222, 120, 255), (250, 170, 180, 255)
    fj = ft("Chalkduster.ttf", 74)
    while d.textlength(bersih(p["judul"]), font=fj) > bw - 120:
        fj = ft("Chalkduster.ttf", fj.size - 4)
    d.text((W / 2, 110), bersih(p["judul"]), font=fj, fill=putih, anchor="ma")
    d.line((W / 2 - 220, 215, W / 2 + 220, 215), fill=kuning, width=4)
    for dx in (-250, 250):  # bintang kecil
        cx = W / 2 + dx
        d.line((cx - 14, 215, cx + 14, 215), fill=kuning, width=3)
        d.line((cx, 201, cx, 229), fill=kuning, width=3)
    cs = lambda s, k=1: ft("ChalkboardSE.ttc", s, k)
    y = 270
    for nama, desk, harga in p["item"]:
        fn_, fh = cs(44, 2), cs(40, 2)
        nm, hg = bersih(nama), bersih(harga)
        d.text((110, y), nm, font=fn_, fill=putih)
        d.text((W - 110, y), hg, font=fh, fill=kuning, anchor="ra")
        x0 = 110 + d.textlength(nm, font=fn_) + 20
        x1 = W - 110 - d.textlength(hg, font=fh) - 20
        for x in range(int(x0), int(x1), 18):
            d.ellipse((x, y + 34, x + 5, y + 39), fill=(220, 220, 210, 255))
        d.text((110, y + 60), bersih(desk), font=cs(32, 0), fill=(220, 226, 218, 255))
        y += 150
    y += 10
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: cs(s, 1), bw - 220, H - fr - 150 - y, 36, 24, 1.3)
    bh2 = len(lines) * size * 1.3 + 90
    d.rounded_rectangle((100, y, W - 100, y + bh2), radius=24, outline=pink, width=4)
    yy = y + 28
    for ln in lines:
        d.text((W / 2, yy), ln, font=f, fill=putih, anchor="ma")
        yy += size * 1.3
    d.text((W / 2, yy + 6), p["ref"], font=cs(30, 2), fill=pink, anchor="ma")
    d.text((W / 2, H - fr - 50), "@" + HANDLE, font=cs(26, 0), fill=(200, 206, 198, 255), anchor="ma")
    img.alpha_composite(kapur(lay, rng))
    return grain(img.convert("RGB"), 0.05)


# ---------- ORNAMEN: bola hiasan Natal, hitung mundur ----------

BOLA = [(196, 30, 46), (206, 160, 60), (30, 120, 70), (40, 80, 170), (170, 176, 188), (130, 24, 50), (20, 110, 110)]


def ornamen_image(p, i):
    rng = np.random.default_rng(1500 + i)
    bg = gradasi(W, H, (22, 34, 30), (8, 14, 12)).convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bok)
    for _ in range(26):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(20, 70)
        c = [(255, 200, 120), (255, 170, 90), (255, 230, 170)][int(rng.integers(3))]
        bd.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(rng.uniform(40, 90)),))
    bg.alpha_composite(bok.filter(ImageFilter.GaussianBlur(14)))
    cx, cy, r = W / 2, 520, 300
    gold = (214, 178, 96, 255)
    d = ImageDraw.Draw(bg)
    d.line((cx, 0, cx, cy - r - 50), fill=gold, width=4)
    # bola: gradasi radial + kilau
    yy, xx = np.mgrid[0:2 * r, 0:2 * r].astype(np.float32)
    dist = np.hypot(xx - r, yy - r) / r
    hl = np.hypot(xx - r * 0.62, yy - r * 0.55) / r
    col = np.array(BOLA[i % 7], np.float32)
    shade = np.clip(1.25 - 0.75 * dist ** 1.6, 0, 1.3)[..., None]
    arr = col * shade + 255 * np.clip(1 - hl / 0.32, 0, 1)[..., None] ** 2 * 0.8
    alpha = np.clip((1 - dist) * r, 0, 1) * 255
    ball = Image.fromarray(np.dstack([np.clip(arr, 0, 255), alpha]).astype(np.uint8), "RGBA")
    bayangan(bg, ball, (cx - r, cy - r), blur=30, geser=(0, 30), kuat=0.5)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((cx - 50, cy - r - 46, cx + 50, cy - r + 10), radius=8, fill=gold)
    for x in range(int(cx - 42), int(cx + 44), 12):
        d.line((x, cy - r - 40, x, cy - r + 4), fill=(170, 136, 64), width=3)
    d.ellipse((cx - 16, cy - r - 70, cx + 16, cy - r - 38), outline=gold, width=6)
    num = str(p["angka"])
    fnum = hn(250, 9)
    d.text((cx + 4, cy - 40 + 6), num, font=fnum, fill=(0, 0, 0, 90), anchor="mm")
    d.text((cx, cy - 40), num, font=fnum, fill=(255, 246, 226, 255), anchor="mm")
    d.text((cx, cy + 120), "HARI LAGI", font=hn(42, 1), fill=(255, 246, 226, 235), anchor="mm")
    for _ in range(40):  # kilau salju
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if math.hypot(x - cx, y - cy) > r + 10:
            s = rng.uniform(1, 3)
            d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, int(rng.uniform(90, 200))))
    y = 870
    d.text((cx, y), "menuju Natal", font=georgia(52, True), fill=(236, 206, 140), anchor="ma")
    y += 84
    for ln in wrap(d, bersih(p["teks"]), georgia(34), W - 200):
        d.text((cx, y), ln, font=georgia(34), fill=(240, 236, 226), anchor="ma")
        y += 46
    y += 18
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), W - 220, H - 110 - y, 28, 20, 1.36)
    for ln in lines:
        d.text((cx, y), ln, font=f, fill=(196, 200, 190), anchor="ma")
        y += size * 1.36
    d.text((cx, y + 8), p["ref"], font=hn(26, 1), fill=(236, 206, 140), anchor="ma")
    d.text((cx, H - 46), "@" + HANDLE, font=hn(22, 10), fill=(150, 160, 150), anchor="ma")
    return bg


# ---------- KODE: editor kode ----------

KATA_KUNCI = {"def", "while", "if", "else", "elif", "for", "in", "return", "True", "False", "None", "and", "or", "not",
              "import", "from", "class", "with", "as", "try", "except", "pass", "break", "is"}
WK = {"bg": (30, 30, 46), "teks": (205, 214, 244), "kunci": (203, 166, 247), "str": (166, 227, 161), "kom": (127, 132, 156),
      "angka": (250, 179, 135), "fungsi": (137, 180, 250), "ayat": (249, 226, 175)}


def warnai(line):
    """-> [(teks, warna)] sederhana: komentar, string, kata kunci, angka, nama fungsi."""
    import re
    if "#" in line and line.count('"', 0, line.index("#")) % 2 == 0:
        k = line.index("#")
        return warnai(line[:k]) + [(line[k:], WK["kom"])]
    out = []
    for m in re.finditer(r'"[^"]*"?|[A-Za-z_][A-Za-z0-9_]*|\d+|\s+|.', line):
        t = m.group(0)
        if t.startswith('"'):
            c = WK["str"]
        elif t in KATA_KUNCI:
            c = WK["kunci"]
        elif t.isdigit():
            c = WK["angka"]
        elif re.match(r"[A-Za-z_]", t) and line[m.end():m.end() + 1] == "(":
            c = WK["fungsi"]
        else:
            c = WK["teks"]
        out.append((t, c))
    return out


def kode_image(p, i):
    img = Image.new("RGB", (W, H), (17, 17, 27))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 40, 60, W - 40, H - 60
    d.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=WK["bg"])
    d.rounded_rectangle((x0, y0, x1, y0 + 64), radius=24, fill=(24, 24, 37))
    d.rectangle((x0, y0 + 40, x1, y0 + 64), fill=(24, 24, 37))
    for k, c in enumerate([(243, 139, 168), (249, 226, 175), (166, 227, 161)]):
        d.ellipse((x0 + 26 + k * 34, y0 + 22, x0 + 46 + k * 34, y0 + 42), fill=c)
    tf = hn(24, 10)
    tw = d.textlength(p["file"], font=tf)
    d.rounded_rectangle((x0 + 150, y0 + 14, x0 + 190 + tw, y0 + 64), radius=10, fill=WK["bg"])
    d.text((x0 + 170, y0 + 40), p["file"], font=tf, fill=WK["teks"], anchor="lm")
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    size = 38
    while max(probe.textlength(r, font=ft("/System/Library/Fonts/Menlo.ttc", size)) for r in p["baris"]) > x1 - x0 - 150:
        size -= 1
    mono = ft("/System/Library/Fonts/Menlo.ttc", size)
    lh = int(size * 1.55)
    y = y0 + 100
    rows = [(r.rstrip(), None) for r in p["baris"]] + [("", None)]
    for ln in wrap(probe, bersih(p["ayat"]), mono, x1 - x0 - 200):
        rows.append(("# " + ln, WK["ayat"]))
    rows.append(("# — " + p["ref"], WK["ayat"]))
    for n, (ln, warna) in enumerate(rows, 1):
        d.text((x0 + 70, y), str(n), font=mono, fill=(88, 91, 112), anchor="ra")
        x = x0 + 100
        for t, c in ([(ln, warna)] if warna else warnai(ln)):
            d.text((x, y), t, font=mono, fill=c)
            x += d.textlength(t, font=mono)
        if n == len(p["baris"]):  # kursor berkedip
            d.rectangle((x + 4, y + 2, x + 20, y + 40), fill=(205, 214, 244))
        y += lh
    ty = max(y + 30, y1 - 54 - 230)  # panel terminal
    d.line((x0, ty, x1, ty), fill=(49, 50, 68), width=2)
    d.text((x0 + 30, ty + 20), "TERMINAL", font=hn(22, 1), fill=(127, 132, 156))
    tm = ft("/System/Library/Fonts/Menlo.ttc", 28)
    d.text((x0 + 30, ty + 66), f"$ python {p['file']}", font=tm, fill=WK["teks"])
    d.text((x0 + 30, ty + 110), "selesai, 0 galat", font=tm, fill=WK["str"])
    d.text((x0 + 30, ty + 154), "$", font=tm, fill=WK["teks"])
    d.rectangle((x0 + 56, ty + 156, x0 + 72, ty + 188), fill=WK["teks"])
    d.rounded_rectangle((x0, y1 - 54, x1, y1), radius=24, fill=(137, 180, 250))
    d.rectangle((x0, y1 - 54, x1, y1 - 30), fill=(137, 180, 250))
    d.text((x0 + 30, y1 - 27), "Python  ·  UTF-8  ·  0 galat", font=hn(24, 10), fill=(24, 24, 37), anchor="lm")
    d.text((x1 - 30, y1 - 27), "@" + HANDLE, font=hn(24, 1), fill=(24, 24, 37), anchor="rm")
    return img


# ---------- KARTUPOS: kartu pos tulisan tangan ----------

def prangko(w, h, scene, seed):
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rectangle((0, 0, w, h), fill=(250, 248, 240, 255))
    for x in range(0, w + 1, 14):
        d.ellipse((x - 5, -5, x + 5, 5), fill=(0, 0, 0, 0))
        d.ellipse((x - 5, h - 5, x + 5, h + 5), fill=(0, 0, 0, 0))
    for y in range(0, h + 1, 14):
        d.ellipse((-5, y - 5, 5, y + 5), fill=(0, 0, 0, 0))
        d.ellipse((w - 5, y - 5, w + 5, y + 5), fill=(0, 0, 0, 0))
    s.paste(vintage(cover(foto_warna(scene, 300, 360, seed=seed), w - 24, h - 44)), (12, 12))
    d.text((w / 2, h - 16), "KASIH KARUNIA", font=hn(14, 1), fill=(120, 60, 50), anchor="mm")
    return s


def kartupos_image(p, i):
    rng = np.random.default_rng(1600 + i)
    img = kayu(W, H, rng, (150, 110, 76)).convert("RGBA")
    # depan kartu (di belakang)
    fw, fh = 900, 560
    front = vintage(cover(foto_warna(ADEGAN[(i + 1) % 4], 1200, 760, seed=1650 + i), fw, fh)).convert("RGBA")
    fd = ImageDraw.Draw(front)
    fd.rectangle((0, 0, fw - 1, fh - 1), outline=(250, 248, 240), width=18)
    fd.text((fw / 2, fh / 2 - 60), "Salam dari", font=ft("SnellRoundhand.ttc", 70, 2), fill=(255, 250, 236), anchor="mm",
            stroke_width=2, stroke_fill=(60, 40, 30))
    fdari = hn(96, 9)
    while fd.textlength(bersih(p["dari"]).upper(), font=fdari) > fw - 100:
        fdari = hn(fdari.size - 4, 9)
    fd.text((fw / 2, fh / 2 + 40), bersih(p["dari"]).upper(), font=fdari, fill=(255, 214, 120), anchor="mm",
            stroke_width=4, stroke_fill=(70, 40, 30))
    front = front.rotate(5, expand=True, resample=Image.BICUBIC)
    bayangan(img, front, ((W - front.width) // 2, 40), blur=16, geser=(6, 14), kuat=0.45)
    # belakang kartu
    bw, bh = 980, 660
    back = Image.new("RGBA", (bw, bh), (250, 247, 238, 255))
    bd = ImageDraw.Draw(back)
    bd.line((bw / 2, 40, bw / 2, bh - 40), fill=(200, 192, 178), width=2)
    ink = (36, 52, 110)
    f, lines, size = pas(bd, bersih(p["pesan"]), tangan, bw / 2 - 80, bh - 170, 36, 24, 1.3)
    y = 50
    for ln in lines:
        bd.text((40, y), ln, font=f, fill=ink)
        y += size * 1.3
    bd.text((bw / 2 - 40, bh - 70), "— diam.dan.percaya", font=tangan(30), fill=ink, anchor="ra")
    st = prangko(150, 180, ADEGAN[i % 4], 1680 + i)
    back.alpha_composite(st, (bw - 190, 36))
    cx, cy = bw - 230, 150  # cap pos
    bd.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=(60, 60, 70, 170), width=4)
    bd.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), outline=(60, 60, 70, 120), width=2)
    fpm = hn(18, 1)
    while bd.textlength(bersih(p["dari"]).upper(), font=fpm) > 104 and fpm.size > 10:
        fpm = hn(fpm.size - 1, 1)
    bd.text((cx, cy - 20), bersih(p["dari"]).upper(), font=fpm, fill=(60, 60, 70, 190), anchor="mm")
    bd.text((cx, cy + 12), f"{15 + i}.11.2026", font=hn(18, 10), fill=(60, 60, 70, 190), anchor="mm")
    for k in range(4):
        yy = cy - 30 + k * 20
        bd.line([(cx + 74 + t * 8, yy + 6 * math.sin(t * 0.9)) for t in range(16)], fill=(60, 60, 70, 150), width=3)
    xr = bw / 2 + 40
    bd.text((xr, 270), "Untuk:", font=tangan(30), fill=(110, 100, 90))
    bd.text((xr + 100, 262), bersih(p["untuk"]), font=tangan(38), fill=ink)
    f2, l2, s2 = pas(bd, bersih(p["ayat"]) + " (" + p["ref"] + ")", tangan, bw / 2 - 80, bh - 360 - 30, 30, 20, 1.3)
    y = 340
    for k in range(5):
        bd.line((xr, 330 + (k + 1) * s2 * 1.3, bw - 40, 330 + (k + 1) * s2 * 1.3), fill=(200, 192, 178), width=2)
    for ln in l2:
        bd.text((xr, y), ln, font=f2, fill=ink)
        y += s2 * 1.3
    back = back.rotate(-3, expand=True, resample=Image.BICUBIC)
    bayangan(img, back, ((W - back.width) // 2, H - back.height - 40), blur=18, geser=(8, 16), kuat=0.5)
    return img.convert("RGB")


# ---------- PETA: aplikasi peta dengan rute ----------

def pin(s, col):
    def g(d, k):
        S = s * k
        d.ellipse((S * .18, 0, S * .82, S * .64), fill=col)
        d.polygon([(S * .24, S * .44), (S * .76, S * .44), (S * .5, S)], fill=col)
        d.ellipse((S * .38, S * .2, S * .62, S * .44), fill=(255, 255, 255, 255))
    return sprite(s, s, g)


def peta_image(p, i):
    rng = np.random.default_rng(1700 + i)
    mh = 840
    img = Image.new("RGBA", (W, H), (237, 232, 223, 255))
    d = ImageDraw.Draw(img)
    for _ in range(3):  # taman
        x, y = rng.uniform(80, W - 200), rng.uniform(80, mh - 200)
        d.rounded_rectangle((x, y, x + rng.uniform(120, 260), y + rng.uniform(90, 200)), radius=30, fill=(200, 226, 186, 255))
    pts = [(-20, rng.uniform(150, 300))]  # sungai
    for x in range(0, W + 120, 120):
        pts.append((x, pts[-1][1] + rng.uniform(-40, 70)))
    d.line(pts, fill=(170, 210, 232, 255), width=46, joint="curve")
    xs = sorted(rng.choice(np.arange(60, W - 60, 40), 6, replace=False))
    ys = sorted(rng.choice(np.arange(320, mh - 80, 40), 6, replace=False))
    for x in xs:
        d.line((x, 0, x, mh), fill=(214, 208, 198, 255), width=26)
        d.line((x, 0, x, mh), fill=(255, 255, 255, 255), width=20)
    for y in ys:
        d.line((0, y, W, y), fill=(214, 208, 198, 255), width=26)
        d.line((0, y, W, y), fill=(255, 255, 255, 255), width=20)
    d.line((0, mh * 0.9, W, mh * 0.15), fill=(250, 214, 120, 255), width=30)  # jalan raya diagonal
    sx, sy = xs[0], ys[-1]
    ex, ey = xs[-1], ys[1]
    mid = xs[len(xs) // 2]
    route = [(sx, sy), (mid, sy), (mid, ey), (ex, ey)]
    d.line(route, fill=(30, 90, 200, 255), width=24, joint="curve")
    d.line(route, fill=(66, 133, 244, 255), width=16, joint="curve")
    d.ellipse((sx - 22, sy - 22, sx + 22, sy + 22), fill=(255, 255, 255, 255))
    d.ellipse((sx - 14, sy - 14, sx + 14, sy + 14), fill=(66, 133, 244, 255))
    comp(img, pin(76, (220, 60, 50, 255)), (ex - 38, ey - 74))
    # kartu atas: dari -> ke
    card = Image.new("RGBA", (W - 80, 190), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, card.width, card.height), radius=28, fill=(255, 255, 255, 255))
    cd.ellipse((36, 46, 60, 70), outline=(110, 110, 116), width=4)
    cd.text((90, 58), bersih(p["dari"]), font=hn(36, 0), fill=(40, 40, 44), anchor="lm")
    for yy in (88, 100, 112):
        cd.ellipse((46, yy, 50, yy + 4), fill=(170, 170, 176))
    comp(card, pin(38, (220, 60, 50, 255)), (29, 116))
    cd.text((90, 136), bersih(p["ke"]), font=hn(36, 1), fill=(40, 40, 44), anchor="lm")
    cd.line((86, 95, card.width - 40, 95), fill=(232, 232, 236), width=2)
    bayangan(img, card, (40, 50), blur=16, geser=(0, 8), kuat=0.25)
    # lembar bawah
    sheet = Image.new("RGBA", (W, H - mh + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheet)
    sd.rounded_rectangle((0, 0, W, sheet.height + 40), radius=40, fill=(255, 255, 255, 255))
    sd.rounded_rectangle((W / 2 - 40, 14, W / 2 + 40, 22), radius=4, fill=(220, 220, 224))
    sd.text((60, 46), bersih(p["waktu"]), font=hn(52, 1), fill=(24, 128, 56))
    sd.text((60 + sd.textlength(bersih(p["waktu"]), font=hn(52, 1)) + 20, 66), "· rute terbaik", font=hn(30, 0), fill=(110, 110, 116))
    y = 130
    for k, step in enumerate(p["langkah"]):
        ax, ay = 82, y + 20
        sd.line((ax, ay + 18, ax, ay - 14), fill=(66, 133, 244), width=6)
        if k == 1:
            sd.line((ax, ay - 14, ax + 18, ay - 14), fill=(66, 133, 244), width=6)
        sd.polygon([(ax - 10, ay - 8), (ax + 10, ay - 8), (ax, ay - 24)] if k != 1 else
                   [(ax + 18, ay - 24), (ax + 18, ay - 4), (ax + 32, ay - 14)], fill=(66, 133, 244))
        sd.text((130, y + 4), bersih(step), font=hn(34, 0), fill=(40, 40, 44))
        y += 62
    y += 10
    sd.line((60, y, W - 60, y), fill=(236, 236, 240), width=2)
    y += 22
    f, lines, size = pas(sd, bersih(p["ayat"]), lambda s: hn(s, 2), W - 120, sheet.height - y - 90, 32, 22, 1.32)
    for ln in lines:
        sd.text((60, y), ln, font=f, fill=(70, 70, 76))
        y += size * 1.32
    sd.text((60, y + 6), p["ref"], font=hn(28, 1), fill=(40, 40, 44))
    sd.text((W - 60, sheet.height - 40), "@" + HANDLE, font=hn(22, 10), fill=(160, 160, 166), anchor="rs")
    bayangan(img, sheet, (0, mh - 40), blur=20, geser=(0, -6), kuat=0.2)
    return img


# ---------- LILIN: lilin di malam hari ----------

def lilin_image(p, i):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fx, fy = W / 2, 905
    dist = np.hypot(xx - fx, (yy - fy) * 0.9)
    glow = np.exp(-(dist / 430) ** 2)[..., None]
    base = np.array([14, 10, 8], np.float32) + glow * np.array([150, 90, 40], np.float32)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    cw, ctop = 190, 990  # lilin pilar
    cand = np.zeros((H - ctop + 40, cw, 3), np.float32)
    xs = np.linspace(-1, 1, cw)[None, :]
    cand += np.array([236, 214, 180]) * (0.55 + 0.45 * np.sqrt(np.clip(1 - xs ** 2, 0, 1)))[..., None]
    cand *= np.linspace(1.15, 0.55, cand.shape[0])[:, None, None]
    img.paste(Image.fromarray(np.clip(cand, 0, 255).astype(np.uint8)), (int(fx - cw / 2), ctop))
    d.ellipse((fx - cw / 2, ctop - 18, fx + cw / 2, ctop + 18), fill=(250, 232, 200, 255))
    d.ellipse((fx - cw / 2 + 16, ctop - 10, fx + cw / 2 - 16, ctop + 10), fill=(236, 206, 160, 255))
    d.line((fx, ctop - 4, fx + 2, ctop - 30), fill=(40, 30, 20), width=5)
    flame = Image.new("RGBA", (200, 260), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flame)
    for s, c in [(1.0, (255, 140, 40, 200)), (0.78, (255, 196, 80, 235)), (0.5, (255, 244, 210, 255))]:
        pts = [(100 + 38 * s * math.sin(math.pi * u) * (1 - u) ** 0.6, 236 - 200 * s * u) for u in np.linspace(0, 1, 40)]
        pts += [(200 - x, y) for x, y in reversed(pts)]
        fd.polygon(pts, fill=c)
    flame = flame.filter(ImageFilter.GaussianBlur(3))
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((fx - 90, fy - 150, fx + 90, fy + 40), fill=(255, 190, 90, 120))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(40)))
    comp(img, flame, (fx - 100, ctop - 30 - 236))
    d = ImageDraw.Draw(img)
    warm, soft = (250, 236, 210), (210, 188, 160)
    y = 150
    f, lines, size = pas(d, bersih(p["teks"]), lambda s: georgia(s, True), W - 200, 300, 50, 34, 1.32)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=warm, anchor="ma")
        y += size * 1.32
    y += 34
    d.line((W / 2 - 40, y, W / 2 + 40, y), fill=(160, 120, 80), width=2)
    y += 34
    f, lines, size = pas(d, bersih(p["ayat"]), georgia, W - 240, 760 - y, 32, 22, 1.4)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=soft, anchor="ma")
        y += size * 1.4
    d.text((W / 2, y + 10), p["ref"], font=hn(26, 1), fill=(220, 170, 110), anchor="ma")
    d.text((W - 50, H - 40), "@" + HANDLE, font=hn(22, 10), fill=(120, 100, 80), anchor="rs")
    return grain(img.convert("RGB"), 0.07)


# ---------- SEARCH (Reels): mesin pencari ----------

BIRU_LINK, ABU_T = (26, 84, 200), (95, 99, 104)


def kaca_pembesar(s, col=(110, 114, 120, 255)):
    def g(d, k):
        S = s * k
        d.ellipse((S * .08, S * .08, S * .68, S * .68), outline=col, width=int(S * .1))
        d.line((S * .6, S * .6, S * .92, S * .92), fill=col, width=int(S * .12))
    return sprite(s, s, g)


def search_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/search{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fq = hn(42, 0)
    q = bersih(p["cari"])
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    def bar(y, kursor):
        lay = Image.new("RGBA", (RW, 130), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((60, 10, RW - 60, 120), radius=55, fill=(255, 255, 255, 255), outline=(218, 220, 224), width=3)
        comp(lay, kaca_pembesar(44), (100, 43))
        t = q
        while ld.textlength(t, font=fq) > RW - 280:
            t = "…" + t[2:]
        ld.text((170, 65), t, font=fq, fill=(32, 33, 36), anchor="lm")
        if kursor:
            x = 172 + ld.textlength(t, font=fq)
            ld.rectangle((x, 40, x + 3, 90), fill=(66, 133, 244))
        return lay

    # halaman 1: logo + bar + saran
    hal1 = Image.new("RGBA", (RW, RH), (255, 255, 255, 255))
    h1 = ImageDraw.Draw(hal1)
    h1.text((RW / 2, 560), "cari", font=hn(150, 1), fill=(60, 64, 67), anchor="ms")
    h1.ellipse((RW / 2 + 160, 530, RW / 2 + 190, 560), fill=(66, 133, 244))
    sugg = [bersih(s) for s in p["saran"]]
    drop = Image.new("RGBA", (RW - 120, 40 + len(sugg) * 100), (0, 0, 0, 0))
    dd = ImageDraw.Draw(drop)
    dd.rounded_rectangle((0, 0, drop.width, drop.height), radius=30, fill=(255, 255, 255, 255))
    for k, s in enumerate(sugg):
        y = 20 + k * 100
        comp(drop, kaca_pembesar(34, (160, 164, 170, 255)), (40, y + 33))
        pre = s[:len(q)] if s.startswith(q) else ""
        dd.text((110, y + 50), pre, font=hn(38, 0), fill=(32, 33, 36), anchor="lm")
        dd.text((110 + dd.textlength(pre, font=hn(38, 0)), y + 50), s[len(pre):], font=hn(38, 1), fill=(32, 33, 36), anchor="lm")
    # halaman 2: hasil
    def hasil_layers():
        L = []
        f, lines, size = pas(probe, tanpa_kutip(p["ayat"]), lambda s: hn(s, 0), RW - 220, 380, 42, 30, 1.32)
        card = Image.new("RGBA", (RW - 120, int(len(lines) * size * 1.32 + 190)), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, card.width, card.height), radius=30, fill=(239, 244, 254, 255), outline=(210, 222, 248), width=3)
        cd.text((40, 34), "JAWABAN TERATAS", font=hn(26, 1), fill=BIRU_LINK)
        y = 86
        for ln in lines:
            cd.text((40, y), ln, font=f, fill=(32, 33, 36))
            y += size * 1.32
        cd.text((40, y + 14), p["ref"] + " (TB)", font=hn(34, 1), fill=BIRU_LINK)
        L.append(card)
        for judul, cuplik in p["hasil"]:
            r = Image.new("RGBA", (RW - 120, 260), (0, 0, 0, 0))
            rd = ImageDraw.Draw(r)
            rd.text((0, 0), f"{HANDLE} › renungan", font=hn(28, 0), fill=(32, 33, 36))
            yy = 44
            for ln in wrap(rd, bersih(judul), hn(40, 0), r.width)[:2]:
                rd.text((0, yy), ln, font=hn(40, 0), fill=BIRU_LINK)
                yy += 52
            for ln in wrap(rd, bersih(cuplik), hn(32, 0), r.width)[:3]:
                rd.text((0, yy + 6), ln, font=hn(32, 0), fill=ABU_T)
                yy += 42
            L.append(r.crop((0, 0, r.width, int(yy + 20))))
        return L
    blocks = hasil_layers()
    head2 = Image.new("RGBA", (RW, 370), (255, 255, 255, 255))
    hd = ImageDraw.Draw(head2)
    for k, tab in enumerate(["Semua", "Ayat", "Renungan", "Doa"]):
        x = 80 + k * 200
        hd.text((x, 230), tab, font=hn(32, 1 if k == 0 else 0), fill=BIRU_LINK if k == 0 else ABU_T)
    hd.rectangle((80, 278, 80 + hd.textlength("Semua", font=hn(32, 1)), 284), fill=BIRU_LINK)
    hd.line((0, 300, RW, 300), fill=(232, 234, 237), width=2)
    hd.text((80, 318), "Sekitar 1 jawaban (0,07 detik)", font=hn(26, 0), fill=ABU_T)
    ys, y = [], 390
    for b in blocks:
        ys.append(y)
        y += b.height + 40
    foot = Image.new("RGBA", (RW, 60), (0, 0, 0, 0))
    ImageDraw.Draw(foot).text((RW / 2, 30), "@" + HANDLE, font=hn(26, 10), fill=(170, 174, 180), anchor="mm")
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        if t < 2.3:  # sampul: pertanyaan sudah diketik, saran turun, sorotan bergerak
            frame = hal1.copy()
            comp(frame, bar(680, int(t * 2) % 2 == 0), (0, 680))
            frame.alpha_composite(drop, (60, 820))
            k = min(len(sugg) - 1, int(max(0, t - 0.6) / 0.5))
            if t > 0.6:
                hl = Image.new("RGBA", (RW - 120, 100), (241, 243, 244, 255))
                frame.alpha_composite(hl, (60, 840 + k * 100))
                fd = ImageDraw.Draw(frame)
                s = sugg[k]
                pre = s[:len(q)] if s.startswith(q) else ""
                comp(frame, kaca_pembesar(34, (160, 164, 170, 255)), (100, 840 + k * 100 + 33))
                fd.text((170, 840 + k * 100 + 50), pre, font=hn(38, 0), fill=(32, 33, 36), anchor="lm")
                fd.text((170 + fd.textlength(pre, font=hn(38, 0)), 840 + k * 100 + 50), s[len(pre):], font=hn(38, 1),
                        fill=(32, 33, 36), anchor="lm")
        else:
            a = ease((t - 2.3) / 0.45)
            frame = Image.new("RGBA", (RW, RH), (255, 255, 255, 255))
            frame.alpha_composite(head2)
            comp(frame, bar(0, False), (0, int(680 - (680 - 70) * a)))
            if t < 3.0:
                w = int(RW * min(1, (t - 2.3) / 0.7))
                ImageDraw.Draw(frame).rectangle((0, 300, w, 304), fill=(66, 133, 244))
            for k, b in enumerate(blocks):
                st = 2.9 + k * 0.55
                if t >= st:
                    bb = ease((t - st) / 0.35)
                    comp(frame, fade(b, bb), (60, ys[k] + (1 - bb) * 40))
            frame.alpha_composite(foot, (0, min(RH - 420, ys[-1] + blocks[-1].height + 40)))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- FLIP (Reels): papan huruf bandara ----------

KARAKTER = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'-:"


def flip_reel(p, idx, mod=MOD, seconds=10):
    rel = f"reels/{mod}/flip{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(1800 + idx)
    cols = 16
    lines = [ln.strip().upper() for ln in bersih(p["teks"]).split("\n")]
    rows = [""] + lines + [""]
    target = [ln.center(cols)[:cols] for ln in rows]
    cw, chh, gap = 60, 92, 4
    bw = cols * (cw + gap) + 40
    bh = len(rows) * (chh + gap) + 40
    bx, by = (RW - bw) // 2, 760 - bh // 2
    fdin = ft("DIN Condensed Bold.ttf", 82)
    cache = {}

    def sel(ch, col=(242, 238, 226)):
        key = (ch, col)
        if key not in cache:
            s = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
            sd = ImageDraw.Draw(s)
            sd.rounded_rectangle((0, 0, cw, chh), radius=6, fill=(34, 34, 36, 255))
            sd.rectangle((0, 0, cw, chh // 2), fill=(40, 40, 42, 255))
            if ch.strip():
                sd.text((cw / 2, chh / 2 + 4), ch, font=fdin, fill=col, anchor="mm")
            sd.line((0, chh // 2, cw, chh // 2), fill=(10, 10, 10, 255), width=3)
            cache[key] = s
        return cache[key]

    bg = gradasi(RW, RH, (16, 20, 28), (6, 8, 12)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    amber = (245, 190, 66)
    d.text((bx + 20, by - 70), "PESAN HARI INI", font=hn(34, 1), fill=amber)
    d.text((bx + bw - 20, by - 70), "19:30", font=ft("DIN Condensed Bold.ttf", 46), fill=amber, anchor="ra")
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=18, fill=(14, 14, 16, 255))
    d.text((RW / 2, by + bh + 50), p["ref"].upper(), font=ft("DIN Condensed Bold.ttf", 60), fill=amber, anchor="ma")
    d.text((RW / 2, by + bh + 140), "@" + HANDLE, font=hn(28, 10), fill=(140, 144, 150), anchor="ma")
    # tiap sel: mulai berputar, berganti huruf berurutan, berhenti di huruf tujuan
    jadwal = {}
    for r, ln in enumerate(target):
        for c, ch in enumerate(ln):
            mulai = 0.7 + r * 0.18 + c * 0.05 + rng.uniform(0, 0.3)
            putaran = int(rng.integers(8, 18)) if ch.strip() else int(rng.integers(0, 5))
            jadwal[(r, c)] = (mulai, putaran, ch)
    rate = 16.0
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = bg.copy()
        for (r, c), (mulai, putaran, ch) in jadwal.items():
            k = int((t - mulai) * rate)  # sampul (sebelum mulai) = teks jadi
            if t < mulai or k >= putaran:
                tampil = ch
            else:
                base_i = KARAKTER.index(ch) if ch in KARAKTER else 0
                tampil = KARAKTER[(base_i - putaran + k) % len(KARAKTER)]
            frame.alpha_composite(sel(tampil), (bx + 20 + c * (cw + gap), by + 20 + r * (chh + gap)))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- semua ----------

SIMPLE = {"KORAN": koran_image, "LETTER": letter_image, "STICKY": sticky_image, "MENU": menu_image, "ORNAMEN": ornamen_image,
          "KODE": kode_image, "KARTUPOS": kartupos_image, "PETA": peta_image, "LILIN": lilin_image}
REELS = {"SEARCH": search_reel, "FLIP": flip_reel}


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
            elif fmt == "KUIS":
                out[(hari, slot)] = (kuis_files(t.KUIS[idx], idx, mod), t.KUIS[idx]["caption"])
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
