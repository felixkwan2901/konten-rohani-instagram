"""Akun Tenang - minggu 7 (konten/tenang_w7.py): 12 gaya baru, satu gaya per slot.
CUACA (aplikasi cuaca), KAMUS (entri kamus), TIKET (boarding pass), CATATAN (checklist aplikasi catatan), STRUK (struk belanja),
CHAT (Reels obrolan), KALENDER (kalender sobek, hitung mundur Natal), POPUP (jendela komputer jadul), POLAROID (3 foto + tulisan tangan),
NEON (Reels lampu neon di dinding bata), PLAYER (pemutar musik, ayat jadi lirik), KETIK (jurnal mesin tik). Komik Eli 3x seminggu.

  python3 gaya_w7.py [reels]
"""
import importlib
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cerita
import config
import render
from gaya_w6 import cover, foto_warna, georgia, hn, tambah_musik
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w7"
SUP = "/System/Library/Fonts/Supplemental/"
RW, RH, FPS = 1080, 1920, 30
EMOJI = re.compile("[\U0001F000-\U0001FFFF☀-➿️‍]")


def ft(path, size, idx=0):
    return ImageFont.truetype(path if path.startswith("/") else SUP + path, size, index=idx)


def tangan(size):
    return ImageFont.truetype(config.FONT["tangan"][0], size, index=config.FONT["tangan"][1])


def bersih(s):
    """Emoji tidak ada di font gambar; buang dari teks yang digambar (caption tetap utuh)."""
    return re.sub(r"\s{2,}", " ", EMOJI.sub("", s)).replace("→", "›").strip()


def tanpa_kutip(s):
    return bersih(s).strip("“”\"")


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def fade(img, a):
    if a >= 1:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * max(a, 0))))
    return img


def comp(base, layer, pos):
    """alpha_composite yang boleh keluar batas (koordinat negatif)."""
    x, y = int(round(pos[0])), int(round(pos[1]))
    if x >= base.width or y >= base.height or x + layer.width <= 0 or y + layer.height <= 0:
        return
    base.alpha_composite(layer, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))


def bayangan(base, layer, pos, blur=24, geser=(0, 16), kuat=0.45):
    pad = blur * 3
    sh = Image.new("RGBA", (layer.width + 2 * pad, layer.height + 2 * pad), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 255), (pad, pad), layer.getchannel("A").point(lambda a: int(a * kuat)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    comp(base, sh, (pos[0] - pad + geser[0], pos[1] - pad + geser[1]))
    comp(base, layer, pos)


def gradasi(w, h, top, bottom):
    y = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(top, np.float32) * (1 - y) + np.array(bottom, np.float32) * y
    return Image.fromarray(np.broadcast_to(arr, (h, w, 3)).astype(np.uint8))


def sprite(w, h, fn, k=4):
    """Gambar bentuk di kanvas k kali lebih besar lalu dikecilkan (tepi halus)."""
    big = Image.new("RGBA", (int(w * k), int(h * k)), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), k)
    return big.resize((int(w), int(h)), Image.LANCZOS)


def pas(d, text, font_fn, maxw, maxh, start, stop, lh=1.35):
    """Ukuran huruf terbesar supaya teks muat di kotak maxw x maxh -> (font, baris, ukuran)."""
    for size in range(start, stop - 1, -2):
        f = font_fn(size)
        lines = wrap(d, text, f, maxw)
        if len(lines) * size * lh <= maxh:
            break
    return f, lines, size


# ---------- CUACA: aplikasi cuaca ----------

LANGIT = {"cerah": ((38, 112, 214), (124, 188, 246)), "berawan": ((64, 102, 152), (150, 176, 206)),
          "hujan": ((52, 66, 92), (112, 128, 150)), "badai": ((24, 28, 50), (74, 72, 100)),
          "malam": ((12, 20, 52), (48, 64, 112)), "pelangi": ((70, 140, 214), (186, 214, 240)),
          "salju": ((62, 88, 132), (132, 158, 196))}
URUTAN = {"cerah": ["cerah", "cerah", "cerah", "berawan", "cerah", "malam"],
          "berawan": ["berawan", "berawan", "cerah", "berawan", "cerah", "malam"],
          "hujan": ["hujan", "hujan", "berawan", "berawan", "pelangi", "malam"],
          "badai": ["badai", "badai", "hujan", "berawan", "cerah", "malam"],
          "malam": ["malam", "cerah", "cerah", "berawan", "cerah", "malam"],
          "pelangi": ["hujan", "pelangi", "cerah", "cerah", "berawan", "malam"],
          "salju": ["salju", "salju", "berawan", "salju", "berawan", "malam"]}


def ikon(kind, s):
    def gambar(d, k):
        S = s * k
        c = S / 2
        kuning, putih, gelap = (255, 206, 64, 255), (255, 255, 255, 255), (118, 126, 146, 255)

        def awan(cx, cy, w, col):
            d.rounded_rectangle((cx - w * .5, cy - w * .02, cx + w * .5, cy + w * .26), radius=w * .14, fill=col)
            d.ellipse((cx - w * .38, cy - w * .26, cx + w * .02, cy + w * .14), fill=col)
            d.ellipse((cx - w * .14, cy - w * .40, cx + w * .38, cy + w * .12), fill=col)

        def matahari(cx, cy, r):
            for j in range(8):
                a = j * math.pi / 4
                d.line((cx + math.cos(a) * r * 1.35, cy + math.sin(a) * r * 1.35, cx + math.cos(a) * r * 1.75,
                        cy + math.sin(a) * r * 1.75), fill=kuning, width=max(2, int(r * .2)))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=kuning)

        if kind == "cerah":
            matahari(c, c, S * .24)
        elif kind == "berawan":
            matahari(c + S * .14, c - S * .12, S * .17)
            awan(c - S * .04, c + S * .1, S * .72, putih)
        elif kind in ("hujan", "badai"):
            awan(c, c - S * .1, S * .78, putih if kind == "hujan" else gelap)
            if kind == "hujan":
                for j in range(3):
                    x = c - S * .2 + j * S * .2
                    d.line((x, c + S * .24, x - S * .06, c + S * .42), fill=(150, 205, 255, 255), width=max(2, int(S / 22)))
            else:
                d.polygon([(c + S * .04, c + S * .14), (c - S * .1, c + S * .32), (c, c + S * .32), (c - S * .06, c + S * .48),
                           (c + S * .12, c + S * .26), (c + S * .02, c + S * .26), (c + S * .1, c + S * .14)], fill=kuning)
        elif kind == "malam":
            r = S * .26
            d.ellipse((c - r, c - r, c + r, c + r), fill=(250, 238, 190, 255))
            d.ellipse((c - r * .45, c - r * 1.25, c + r * 1.55, c + r * .75), fill=(0, 0, 0, 0))
        elif kind == "pelangi":
            warna = [(240, 80, 80), (250, 160, 60), (250, 220, 80), (110, 200, 110), (90, 160, 240), (150, 110, 220)]
            bw, r = max(3, int(S * .055)), S * .42
            for j, col in enumerate(warna):
                rr = r - j * bw
                d.arc((c - rr, c - rr + S * .12, c + rr, c + rr + S * .12), 180, 360, fill=col + (255,), width=bw)
            awan(c - S * .3, c + S * .2, S * .36, putih)
            awan(c + S * .3, c + S * .2, S * .36, putih)
        elif kind == "salju":
            awan(c, c - S * .12, S * .78, putih)
            for j, (fx, fy) in enumerate(((-.2, .3), (0, .4), (.2, .3))):
                x0, y0, r = c + S * fx, c + S * fy, S * .07
                for a in range(0, 180, 60):
                    ang = math.radians(a)
                    d.line((x0 - r * math.cos(ang), y0 - r * math.sin(ang), x0 + r * math.cos(ang), y0 + r * math.sin(ang)), fill=(220, 236, 255, 255), width=max(2, int(S / 30)))
    return sprite(s, s, gambar)


def kartu_kaca(img, box, alpha=46, radius=34):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, radius=radius, fill=(255, 255, 255, alpha))
    img.alpha_composite(lay)


def cuaca_image(p, i):
    img = grain(gradasi(W, H, *LANGIT[p["ikon"]]), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    white, soft = (255, 255, 255, 255), (255, 255, 255, 200)
    d.text((W / 2, 64), "Hatimu", font=hn(40, 10), fill=white, anchor="ma")
    d.text((W / 2, 114), p["hari"], font=hn(28, 0), fill=soft, anchor="ma")
    d.text((W / 2, 150), p["besar"], font=hn(190, 12), fill=white, anchor="ma")
    d.text((W / 2, 362), p["label_besar"], font=hn(40, 10), fill=white, anchor="ma")
    fk = hn(34, 0)
    tw = d.textlength(p["kondisi"], font=fk) + 60
    comp(img, ikon(p["ikon"], 52), (W / 2 - tw / 2, 412))
    d.text((W / 2 - tw / 2 + 62, 420), p["kondisi"], font=fk, fill=soft)
    # per jam
    y0 = 490
    kartu_kaca(img, (60, y0, W - 60, y0 + 180))
    d = ImageDraw.Draw(img)
    for k, (jam, kind) in enumerate(zip(["Kini", "09", "12", "15", "18", "21"], URUTAN[p["ikon"]])):
        cx = 60 + (W - 120) * (k + 0.5) / 6
        d.text((cx, y0 + 28), jam, font=hn(28, 10), fill=white, anchor="ma")
        comp(img, ikon(kind, 76), (cx - 38, y0 + 80))
    # prakiraan
    y0 = 694
    kartu_kaca(img, (60, y0, W - 60, y0 + 270))
    d = ImageDraw.Draw(img)
    d.text((100, y0 + 26), "PRAKIRAAN HARI INI", font=hn(24, 10), fill=soft)
    for k, (lab, nil) in enumerate(p["baris"]):
        y = y0 + 80 + k * 64
        if k:
            d.line((100, y - 12, W - 100, y - 12), fill=(255, 255, 255, 70), width=2)
        d.text((100, y), lab, font=hn(34, 0), fill=white)
        d.text((W - 100, y), nil, font=hn(34, 1), fill=white, anchor="ra")
    # ayat
    y0 = 988
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: hn(s, 0), W - 200, 190, 34, 24, 1.32)
    kartu_kaca(img, (60, y0, W - 60, y0 + 108 + len(lines) * size * 1.32 + 40))
    d = ImageDraw.Draw(img)
    d.text((100, y0 + 26), "AYAT HARI INI", font=hn(24, 10), fill=soft)
    y = y0 + 72
    for ln in lines:
        d.text((100, y), ln, font=f, fill=white)
        y += size * 1.32
    d.text((100, y + 10), p["ref"], font=hn(30, 1), fill=white)
    d.text((W / 2, H - 46), "@" + HANDLE, font=hn(24, 10), fill=soft, anchor="ma")
    return img


# ---------- KAMUS: entri kamus ----------

def kamus_image(p, i, gelap=False):
    ink, merah, abu = ((236, 230, 220), (236, 132, 96), (150, 140, 130)) if gelap else ((30, 26, 22), (168, 68, 42), (122, 112, 104))
    gb = lambda s: ft("Georgia Bold.ttf", s)
    for k in (1.0, 0.94, 0.88, 0.82, 0.76):
        img = grain(Image.new("RGB", (W, H), "#1C1A18" if gelap else "#F5F0E6"), 0.05).convert("RGBA")
        d = ImageDraw.Draw(img)
        d.text((80, 78), "kamus hati", font=georgia(30, True), fill=abu)
        d.text((W - 80, 74), p["kata"][0].upper(), font=gb(36), fill=merah, anchor="ra")
        d.line((80, 130, W - 80, 130), fill=(207, 198, 184), width=2)
        y = 200
        fw = gb(int(130 * k))
        while d.textlength(p["suku"], font=fw) > W - 160:
            fw = gb(fw.size - 6)
        tw = d.textlength(p["suku"], font=fw)
        hl = Image.new("RGBA", img.size, (0, 0, 0, 0))  # stabilo di bawah kata
        ImageDraw.Draw(hl).rounded_rectangle((70, y + fw.size * 0.62, 90 + tw, y + fw.size * 1.02), radius=10, fill=(255, 214, 70, 120))
        img.alpha_composite(hl)
        d = ImageDraw.Draw(img)
        d.text((80, y), p["suku"], font=fw, fill=ink)
        y += fw.size * 1.22
        fl = georgia(int(40 * k), True)
        d.text((80, y), p["lafal"], font=fl, fill=abu)
        d.text((80 + d.textlength(p["lafal"] + "   ", font=fl), y), p["kelas"], font=fl, fill=merah)
        y += 40 * k * 2.1
        fa = georgia(int(38 * k))
        for n, arti in enumerate(p["arti"], 1):
            d.text((80, y), str(n), font=gb(int(38 * k)), fill=merah)
            for ln in wrap(d, bersih(arti), fa, W - 210):
                d.text((130, y), ln, font=fa, fill=ink)
                y += 38 * k * 1.42
            y += 38 * k * 0.6
        y += 38 * k * 0.5
        d.text((80, y), "contoh:", font=georgia(int(32 * k), True), fill=abu)
        y += 32 * k * 1.7
        fv = georgia(int(36 * k), True)
        lines = wrap(d, bersih(p["ayat"]), fv, W - 230)
        top = y
        for ln in lines:
            d.text((130, y), ln, font=fv, fill=ink)
            y += 36 * k * 1.42
        d.line((96, top + 6, 96, y - 8), fill=merah, width=4)
        d.text((130, y + 6), p["ref"], font=hn(int(30 * k), 1), fill=merah)
        y += 30 * k * 2.2
        if y < H - 190:
            break
    d.line((80, H - 170, W - 80, H - 170), fill=(207, 198, 184), width=2)
    d.text((80, H - 140), "lihat juga: ", font=georgia(30, True), fill=abu)
    d.text((80 + d.textlength("lihat juga: ", font=georgia(30, True)), H - 140), p["lihat"], font=georgia(30), fill=ink)
    d.text((W / 2, H - 64), "@" + HANDLE, font=hn(22, 10), fill=abu, anchor="ma")
    return img


# ---------- TIKET: boarding pass ----------

def pesawat(s, col):
    def gambar(d, k):
        S = s * k
        c = S / 2
        d.rounded_rectangle((S * .08, c - S * .07, S * .92, c + S * .07), radius=S * .07, fill=col)
        d.polygon([(S * .42, c), (S * .62, c), (S * .44, c + S * .42), (S * .36, c + S * .42)], fill=col)
        d.polygon([(S * .42, c), (S * .62, c), (S * .44, c - S * .42), (S * .36, c - S * .42)], fill=col)
        d.polygon([(S * .1, c), (S * .2, c), (S * .12, c + S * .2), (S * .06, c + S * .2)], fill=col)
        d.polygon([(S * .1, c), (S * .2, c), (S * .12, c - S * .2), (S * .06, c - S * .2)], fill=col)
    return sprite(s, s, gambar)


def lokomotif(s, col):
    def gambar(d, k):
        S = s * k
        d.rounded_rectangle((S * .08, S * .3, S * .92, S * .72), radius=S * .08, fill=col)
        d.rectangle((S * .62, S * .16, S * .86, S * .34), fill=col)
        for x in (.2, .45):
            d.rectangle((S * x, S * .38, S * (x + .14), S * .52), fill=(255, 255, 255, 255))
        for x in (.24, .5, .76):
            d.ellipse((S * (x - .09), S * .66, S * (x + .09), S * .84), fill=col)
            d.ellipse((S * (x - .04), S * .71, S * (x + .04), S * .79), fill=(255, 255, 255, 255))
    return sprite(s, s, gambar)


def barcode(d, x0, y0, w, h, rng, col):
    x = x0
    while x < x0 + w - 8:
        bw = int(rng.choice([2, 3, 4, 6]))
        d.rectangle((x, y0, x + bw - 1, y0 + h), fill=col)
        x += bw + int(rng.choice([2, 3, 4]))


def tiket_image(p, i, latar=None, kereta=False):
    rng = np.random.default_rng(200 + i)
    img = (latar.copy() if latar is not None else grain(gradasi(W, H, (120, 176, 232), (250, 210, 176)), 0.06)).convert("RGBA")
    navy, abu = (29, 43, 83), (138, 143, 156)
    cw, chh = 920, 1170
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, cw, chh), radius=36, fill=(255, 255, 255, 255))
    d.rounded_rectangle((0, 0, cw, 140), radius=36, fill=navy)
    d.rectangle((0, 100, cw, 140), fill=navy)
    d.text((50, 70), "TIKET KERETA" if kereta else "BOARDING PASS", font=hn(34, 1), fill="white", anchor="lm")
    d.text((cw - 50, 70), "@" + HANDLE, font=hn(24, 10), fill=(200, 210, 235), anchor="rm")
    fk = hn(118, 1)
    d.text((60, 200), p["kode_dari"], font=fk, fill=navy)
    d.text((cw - 60, 200), p["kode_ke"], font=fk, fill=navy, anchor="ra")
    d.text((64, 350), p["dari"], font=hn(34, 0), fill=abu)
    d.text((cw - 64, 350), p["ke"], font=hn(34, 0), fill=abu, anchor="ra")
    xa, xb = 60 + d.textlength(p["kode_dari"], font=fk) + 30, cw - 60 - d.textlength(p["kode_ke"], font=fk) - 30
    for x in range(int(xa), int(xb) - 10, 22):
        d.line((x, 262, x + 10, 262), fill=(200, 204, 214), width=3)
    pl = (lokomotif if kereta else pesawat)(84, navy + (255,))
    card.paste((255, 255, 255, 255), (int((xa + xb) / 2 - 50), 218, int((xa + xb) / 2 + 50), 306))
    comp(card, pl, ((xa + xb) / 2 - 42, 220))
    d = ImageDraw.Draw(card)
    fields = [("PENUMPANG", p["penumpang"]), ("KELAS", p["kelas"]), ("KURSI", p["kursi"]),
              ("GERBANG", p["gerbang"]), ("BERANGKAT", p["berangkat"]), ("BAGASI", "Tinggalkan")]
    for k, (lab, val) in enumerate(fields):
        x, y = 60 + (k % 3) * 290, 440 + (k // 3) * 140
        d.text((x, y), lab, font=hn(24, 10), fill=abu)
        fv = hn(38, 1)
        while d.textlength(val, font=fv) > 250:
            fv = hn(fv.size - 2, 1)
        d.text((x, y + 40), val, font=fv, fill=navy)
    yp = 740  # garis sobek
    for x in range(50, cw - 50, 26):
        d.line((x, yp, x + 13, yp), fill=(200, 204, 214), width=3)
    for cx in (0, cw):
        d.ellipse((cx - 32, yp - 32, cx + 32, yp + 32), fill=(0, 0, 0, 0))
    f, lines, size = pas(d, tanpa_kutip(p["ayat"]), lambda s: hn(s, 0), cw - 120, 210, 34, 24, 1.34)
    y = 790
    for ln in lines:
        d.text((60, y), ln, font=f, fill=(40, 44, 56))
        y += size * 1.34
    d.text((60, y + 12), p["ref"].upper(), font=hn(28, 1), fill=navy)
    barcode(d, 60, chh - 150, cw - 120, 90, rng, navy)
    bayangan(img, card, ((W - cw) // 2, 90))
    return img


# ---------- CATATAN: checklist aplikasi catatan ----------

def lingkaran_cek(s, status):
    def gambar(d, k):
        S = s * k
        if status == "v":
            d.ellipse((2 * k, 2 * k, S - 2 * k, S - 2 * k), fill=(227, 165, 11, 255))
            d.line((S * .28, S * .52, S * .44, S * .68, S * .74, S * .34), fill="white", width=int(S * .1), joint="curve")
        else:
            d.ellipse((2 * k, 2 * k, S - 2 * k, S - 2 * k), outline=(199, 199, 204, 255), width=int(3 * k))
    return sprite(s, s, gambar)


def catatan_image(p, i, gelap=False):
    img = grain(Image.new("RGB", (W, H), "#0B0B0D" if gelap else "#FFFFFF"), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    amber, abu, hitam = (227, 165, 11), (154, 154, 158), (20, 20, 20)
    if gelap:
        abu, hitam = (130, 130, 136), (236, 236, 240)
    jam = p.get("_jam", "10.30")
    d.text((80, 44), jam, font=hn(32, 1), fill=hitam)
    d.rounded_rectangle((W - 140, 48, W - 84, 76), radius=8, outline=hitam, width=3)
    d.rounded_rectangle((W - 135, 53, W - 100, 71), radius=4, fill=hitam)
    d.rectangle((W - 82, 56, W - 78, 68), fill=hitam)
    d.line((84, 150, 64, 130, 84, 110), fill=amber, width=6)
    d.text((100, 130), "Catatan", font=hn(38, 0), fill=amber, anchor="lm")
    d.ellipse((W - 116, 104, W - 64, 156), outline=amber, width=4)
    for dx in (-12, 0, 12):
        d.ellipse((W - 90 + dx - 4, 126, W - 90 + dx + 4, 134), fill=amber)
    d.text((W / 2, 200), p.get("_tanggal", f"{8 + i} November 2026") + " pukul " + jam, font=hn(26, 0), fill=abu, anchor="ma")
    y = 270
    ft_ = hn(62, 1)
    for ln in wrap(d, bersih(p["judul"]), ft_, W - 160):
        d.text((80, y), ln, font=ft_, fill=hitam)
        y += 76
    y += 30
    fi = hn(42, 0)
    for teks, status in p["item"]:
        comp(img, lingkaran_cek(52, status), (80, y))
        d = ImageDraw.Draw(img)
        col = abu if status == "x" else hitam
        d.text((160, y + 26), bersih(teks), font=fi, fill=col, anchor="lm")
        if status == "x":
            d.line((156, y + 28, 164 + d.textlength(bersih(teks), font=fi), y + 28), fill=(120, 120, 124), width=4)
        y += 92
    y += 24
    d.line((80, y, W - 80, y), fill=(44, 44, 48) if gelap else (232, 232, 236), width=2)
    y += 36
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: hn(s, 2), W - 160, H - 150 - y - 60, 40, 26, 1.38)
    for ln in lines:
        d.text((80, y), ln, font=f, fill=(206, 206, 212) if gelap else (50, 50, 54))
        y += size * 1.38
    d.text((80, y + 8), p["ref"], font=hn(size, 1), fill=hitam)
    # toolbar bawah
    yb = H - 92
    d.line((0, yb - 26, W, yb - 26), fill=(44, 44, 48) if gelap else (236, 236, 240), width=2)
    for k, cx in enumerate((150, 400, 680, 930)):
        if k == 0:
            for j in range(3):
                d.ellipse((cx - 30, yb - 4 + j * 18 - 6, cx - 18, yb - 4 + j * 18 + 6), outline=amber, width=3)
                d.line((cx - 8, yb - 4 + j * 18, cx + 30, yb - 4 + j * 18), fill=amber, width=3)
        elif k == 1:
            d.rounded_rectangle((cx - 30, yb - 12, cx + 30, yb + 32), radius=8, outline=amber, width=4)
            d.ellipse((cx - 11, yb - 1, cx + 11, yb + 21), outline=amber, width=4)
        elif k == 2:
            d.line((cx - 26, yb + 32, cx + 22, yb - 16), fill=amber, width=7)
            d.line((cx - 30, yb + 36, cx - 22, yb + 28), fill=amber, width=4)
        else:
            d.rounded_rectangle((cx - 30, yb - 12, cx + 22, yb + 36), radius=8, outline=amber, width=4)
            d.line((cx - 6, yb + 14, cx + 30, yb - 22), fill=amber, width=6)
    d.text((W / 2, H - 30), "@" + HANDLE, font=hn(20, 0), fill=(190, 190, 194), anchor="ms")
    return img


# ---------- STRUK: struk belanja ----------

ALAS = ["#D9C7B0", "#BFD4CF", "#E3C9C9", "#C9CFE3", "#D6D1C4", "#CDE0C5", "#E6D7B8"]


def struk_image(p, i, alas=None):
    rng = np.random.default_rng(300 + i)
    mono = lambda s, b=False: ft("/System/Library/Fonts/Menlo.ttc", s, 1 if b else 0)
    pw, cols, cs = 700, 30, 30
    ink = (38, 38, 38)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rows = []  # (teks, font, perataan, tinggi)

    def baris(t, f=None, al="l", h=None):
        f = f or mono(cs)
        rows.append((t, f, al, h or int(f.size * 1.45)))

    def kiri_kanan(a, b, f=None):
        f = f or mono(cs)
        rows.append(((a, b), f, "lr", int(f.size * 1.45)))

    for ln in wrap(probe, p["toko"], mono(40, True), pw - 100):
        baris(ln, mono(40, True), "c")
    baris("@" + HANDLE, mono(24), "c")
    baris("", h=16)
    kiri_kanan(p.get("_tgl_struk", f"{8 + i:02d}/11/2026"), p.get("_jam", "12:00").replace(".", ":"))
    baris("-" * cols)
    for nama, harga in p["item"]:
        kiri_kanan(bersih(nama), bersih(harga))
    baris("-" * cols)
    kiri_kanan(p["total"][0], p["total"][1], mono(36, True))
    baris("", h=10)
    for ln in wrap(probe, bersih(p["bayar"]), mono(28, True), pw - 100):
        baris(ln, mono(28, True), "c")
    baris("=" * cols)
    for ln in wrap(probe, bersih(p["ayat"]), mono(27), pw - 100):
        baris(ln, mono(27), "c")
    baris(p["ref"], mono(27, True), "c")
    baris("", h=24)
    baris("BARCODE", h=110)
    baris("* TERIMA KASIH *", mono(26, True), "c")
    ph = 70 + sum(r[3] for r in rows) + 60
    paper = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(paper)
    zig = 14
    poly = [(0, zig)] + [(x, 0 if (x // zig) % 2 else zig) for x in range(0, pw + 1, zig)] + [(pw, zig), (pw, ph - zig)]
    poly += [(x, ph if (x // zig) % 2 else ph - zig) for x in range(pw, -1, -zig)] + [(0, ph - zig)]
    d.polygon(poly, fill=(251, 250, 246, 255))
    y = 70
    for t, f, al, h in rows:
        if t == "BARCODE":
            barcode(d, 60, y, pw - 120, 90, rng, ink)
        elif t:
            if al == "lr":
                d.text((50, y), t[0], font=f, fill=ink)
                d.text((pw - 50, y), t[1], font=f, fill=ink, anchor="ra")
            else:
                x = {"l": 50, "c": pw / 2}[al]
                d.text((x, y), t, font=f, fill=ink, anchor="la" if al == "l" else "ma")
        y += h
    paper = paper.filter(ImageFilter.GaussianBlur(0.35))
    a = np.asarray(paper).astype(np.float32)  # tinta termal sedikit tidak rata
    fade_map = 0.88 + 0.12 * render.fbm2d(ph, pw, rng, ((4, 1.0), (16, 0.5)))
    a[..., :3] = 255 - (255 - a[..., :3]) * fade_map[..., None]
    paper = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    paper = paper.rotate(-2.2 if i % 2 else 2.0, expand=True, resample=Image.BICUBIC)
    if paper.height > H - 80:
        s = (H - 80) / paper.height
        paper = paper.resize((int(paper.width * s), int(paper.height * s)), Image.LANCZOS)
    img = (alas.copy() if alas is not None else grain(Image.new("RGB", (W, H), ALAS[i % len(ALAS)]), 0.07)).convert("RGBA")
    bayangan(img, paper, ((W - paper.width) // 2, (H - paper.height) // 2), blur=20, geser=(10, 18), kuat=0.35)
    return img


# ---------- KALENDER: kalender sobek, hitung mundur Natal ----------

def kalender_image(p, i, latar=None):
    rng = np.random.default_rng(600 + i)
    wall = np.asarray(gradasi(W, H, (239, 230, 216), (214, 200, 180))).astype(np.float32)
    wall *= (0.92 + 0.16 * render.fbm2d(H, W, rng, ((6, 1.0), (60, 0.4))))[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wall *= (1.06 - 0.22 * np.hypot((xx - W * 0.3) / W, (yy - H * 0.15) / H))[..., None]
    img = (latar.copy() if latar is not None else grain(Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8)), 0.05)).convert("RGBA")
    merah, ink, abu = (179, 38, 46), (40, 34, 30), (130, 120, 110)
    pw, x0, top, pb = 740, (W - 740) // 2, 200, 1255
    pad = Image.new("RGBA", (pw, pb - top + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(pad)
    for k in range(4, 0, -1):  # tebal tumpukan halaman
        d.rectangle((6 + k, 150 + k * 6, pw - 6 - k, pb - top + k * 6), fill=(236 - k * 8, 232 - k * 8, 224 - k * 8, 255))
    d.rectangle((0, 0, pw, 130), fill=merah)
    d.text((pw / 2, 66), ("DESEMBER" if "Desember" in p["tanggal"] else "NOVEMBER") + " 2026", font=hn(44, 1), fill="white", anchor="mm")
    d.rectangle((0, 130, pw, pb - top), fill=(251, 248, 242, 255))
    ys = 132  # sisa sobekan halaman kemarin
    pts = [(0, ys)] + [(x, ys + 10 + rng.uniform(0, 16)) for x in range(0, pw + 1, 18)] + [(pw, ys)]
    d.polygon(pts, fill=(238, 233, 224, 255))
    d.line(pts[1:-1], fill=(214, 206, 194, 255), width=2)
    y = 186
    d.text((pw / 2, y), p["tanggal"].upper(), font=hn(28, 10), fill=abu, anchor="ma")
    y += 40
    d.text((pw / 2, y), str(p["angka"]), font=hn(250, 9), fill=merah, anchor="ma")
    y += 272
    d.text((pw / 2, y), "H A R I   L A G I", font=hn(40, 1), fill=ink, anchor="ma")
    y += 58
    d.text((pw / 2, y), "menuju Natal", font=georgia(46, True), fill=merah, anchor="ma")
    y += 80
    for ln in wrap(d, bersih(p["teks"]), georgia(34), pw - 120):
        d.text((pw / 2, y), ln, font=georgia(34), fill=ink, anchor="ma")
        y += 46
    y += 16
    d.line((pw / 2 - 60, y, pw / 2 + 60, y), fill=(210, 200, 186), width=2)
    y += 26
    f, lines, size = pas(d, bersih(p["ayat"]), lambda s: georgia(s, True), pw - 140, pb - top - 60 - y, 28, 22, 1.36)
    for ln in lines:
        d.text((pw / 2, y), ln, font=f, fill=(90, 82, 74), anchor="ma")
        y += size * 1.36
    d.text((pw / 2, y + 8), p["ref"], font=hn(24, 1), fill=merah, anchor="ma")
    bayangan(img, pad, (x0, top), blur=26, geser=(8, 20), kuat=0.4)
    d = ImageDraw.Draw(img)
    # paku, tali, ring
    d.line((W / 2, 112, x0 + 180, top + 8), fill=(120, 100, 80), width=3)
    d.line((W / 2, 112, x0 + pw - 180, top + 8), fill=(120, 100, 80), width=3)
    d.ellipse((W / 2 - 12, 100, W / 2 + 12, 124), fill=(90, 90, 96))
    for cx in (x0 + 180, x0 + pw - 180):
        d.rounded_rectangle((cx - 12, top - 22, cx + 12, top + 34), radius=12, outline=(150, 150, 158), width=7)
    # ranting holly
    hx, hy = x0 + pw - 40, top + 128

    def holly(dd, k):
        for a, s in ((-30, 1), (40, -1)):
            ang = math.radians(a)
            cx, cy = 90 * k + math.cos(ang) * 46 * k * s, 90 * k + math.sin(ang) * 30 * k
            leaf = [(cx + math.cos(ang) * 50 * k * t - math.sin(ang) * 18 * k * math.sin(math.pi * t) * w,
                     cy + math.sin(ang) * 50 * k * t + math.cos(ang) * 18 * k * math.sin(math.pi * t) * w)
                    for w in (1, -1) for t in (np.linspace(-1, 1, 12) if w == 1 else np.linspace(1, -1, 12))]
            dd.polygon(leaf, fill=(40, 110, 60, 255))
        for bx, by in ((80, 84), (98, 80), (90, 98)):
            dd.ellipse(((bx - 10) * k, (by - 10) * k, (bx + 10) * k, (by + 10) * k), fill=(200, 30, 40, 255))
    comp(img, sprite(180, 180, holly), (hx - 90, hy - 90))
    d = ImageDraw.Draw(img)
    d.text((W / 2, H - 50), "@" + HANDLE, font=hn(24, 10), fill=(120, 108, 96), anchor="ma")
    return img


# ---------- POPUP: jendela komputer jadul ----------

ABU95, NAVY95 = (192, 192, 192), (0, 0, 128)


def ms(size):
    return ft("Microsoft Sans Serif.ttf", size)


def tahoma_b(size):
    return ft("Tahoma Bold.ttf", size)


def bevel(d, box, ditekan=False, isi=ABU95):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=isi)
    terang, gelap = ((255, 255, 255), (0, 0, 0)) if not ditekan else ((0, 0, 0), (255, 255, 255))
    d.line((x0, y1, x0, y0, x1, y0), fill=terang, width=2)
    d.line((x0, y1, x1, y1, x1, y0), fill=gelap, width=2)
    d.line((x0 + 2, y1 - 2, x1 - 2, y1 - 2, x1 - 2, y0 + 2), fill=(128, 128, 128), width=2)


def jendela(img, box, judul):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    bevel(d, box)
    tb = np.linspace(0, 1, x1 - x0 - 12)[None, :, None]
    bar = (np.array(NAVY95) * (1 - tb) + np.array((16, 132, 208)) * tb).astype(np.uint8)
    img.paste(Image.fromarray(np.broadcast_to(bar, (50, x1 - x0 - 12, 3)).copy()), (x0 + 6, y0 + 6))
    d = ImageDraw.Draw(img)
    d.text((x0 + 22, y0 + 31), judul, font=tahoma_b(28), fill="white", anchor="lm")
    bx = x1 - 52
    bevel(d, (bx, y0 + 12, bx + 38, y0 + 48))
    d.line((bx + 11, y0 + 21, bx + 27, y0 + 39), fill="black", width=4)
    d.line((bx + 27, y0 + 21, bx + 11, y0 + 39), fill="black", width=4)
    return d


def ikon95(kind, s):
    def gambar(d, k):
        S = s * k
        if kind == "peringatan":
            d.polygon([(S / 2, S * .06), (S * .96, S * .92), (S * .04, S * .92)], fill=(0, 0, 0, 255))
            d.polygon([(S / 2, S * .14), (S * .9, S * .88), (S * .1, S * .88)], fill=(255, 232, 0, 255))
            d.rounded_rectangle((S * .46, S * .36, S * .54, S * .66), radius=S * .03, fill=(0, 0, 0, 255))
            d.ellipse((S * .45, S * .72, S * .55, S * .82), fill=(0, 0, 0, 255))
        else:
            col = (200, 20, 20, 255) if kind == "galat" else (20, 60, 200, 255)
            d.ellipse((S * .04, S * .04, S * .96, S * .96), fill=(0, 0, 0, 255))
            d.ellipse((S * .08, S * .08, S * .92, S * .92), fill=col)
            if kind == "galat":
                d.line((S * .32, S * .32, S * .68, S * .68), fill="white", width=int(S * .1))
                d.line((S * .68, S * .32, S * .32, S * .68), fill="white", width=int(S * .1))
            else:
                d.text((S / 2, S / 2), "i" if kind == "info" else "?", font=ft("Times New Roman Bold.ttf", int(S * .66)),
                       fill="white", anchor="mm")
    return sprite(s, s, gambar)


def ikon_desktop(kind, s):
    def gambar(d, k):
        S = s * k
        if kind == "buku":
            d.rectangle((S * .2, S * .1, S * .8, S * .9), fill=(120, 40, 30, 255), outline=(0, 0, 0, 255), width=int(2 * k))
            d.rectangle((S * .47, S * .25, S * .53, S * .65), fill=(240, 200, 80, 255))
            d.rectangle((S * .36, S * .35, S * .64, S * .41), fill=(240, 200, 80, 255))
        elif kind == "folder":
            d.rectangle((S * .08, S * .22, S * .45, S * .34), fill=(240, 210, 90, 255), outline=(0, 0, 0, 255), width=int(2 * k))
            d.rectangle((S * .08, S * .3, S * .92, S * .82), fill=(250, 224, 110, 255), outline=(0, 0, 0, 255), width=int(2 * k))
        else:  # tempat sampah
            d.rectangle((S * .22, S * .3, S * .78, S * .92), fill=(220, 220, 220, 255), outline=(0, 0, 0, 255), width=int(2 * k))
            d.rectangle((S * .14, S * .2, S * .86, S * .3), fill=(200, 200, 200, 255), outline=(0, 0, 0, 255), width=int(2 * k))
            for x in (.38, .5, .62):
                d.line((S * x, S * .4, S * x, S * .84), fill=(110, 110, 110, 255), width=int(2 * k))
    return sprite(s, s, gambar)


def kursor(s):
    def gambar(d, k):
        S = s * k
        pts = [(0, 0), (0, S * .78), (S * .2, S * .62), (S * .34, S * .94), (S * .46, S * .88), (S * .32, S * .58), (S * .56, S * .58)]
        d.polygon([(x + 2 * k, y + 2 * k) for x, y in pts], fill=(0, 0, 0, 255))
        d.polygon([(x * .86 + 5 * k, y * .86 + 7 * k) for x, y in pts], fill=(255, 255, 255, 255))
    return sprite(s, s, gambar)


def popup_image(p, i, natal=False):
    img = Image.new("RGBA", (W, H), (18, 84, 62, 255) if natal else (0, 128, 128, 255))
    if natal:  # wallpaper Natal: salju & bintang
        rs = np.random.default_rng(640 + i)
        sd = ImageDraw.Draw(img)
        for _ in range(160):
            x, y, s = rs.uniform(0, W), rs.uniform(0, H), rs.uniform(2, 5)
            sd.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, 180))
        for x, y in ((960, 1180), (140, 1150), (900, 600)):
            sd.polygon([(x, y - 30), (x + 8, y - 8), (x + 30, y), (x + 8, y + 8), (x, y + 30), (x - 8, y + 8), (x - 30, y), (x - 8, y - 8)], fill=(250, 214, 110, 255))
    for k, (kind, lab) in enumerate((("buku", "Alkitab"), ("folder", "Doa"), ("sampah", "Khawatir"))):
        y = 60 + k * 180
        comp(img, ikon_desktop(kind, 84), (54, y))
        ImageDraw.Draw(img).text((96, y + 100), lab, font=ms(24), fill="white", anchor="ma")
    # dialog
    x0, x1, y0 = 210, W - 50, 90
    probe = ImageDraw.Draw(img)
    fm = ms(40)
    lines = wrap(probe, bersih(p["pesan"]), fm, x1 - x0 - 200)
    body = max(110, len(lines) * 52)
    y1 = y0 + 56 + 50 + body + 50 + 76 + 36
    d = jendela(img, (x0, y0, x1, y1), bersih(p["judul"]))
    comp(img, ikon95(p["ikon"], 100), (x0 + 40, y0 + 96))
    d = ImageDraw.Draw(img)
    y = y0 + 56 + 50
    for ln in lines:
        d.text((x0 + 170, y), ln, font=fm, fill="black")
        y += 52
    fb = ms(32)
    tombol = [bersih(t) for t in p["tombol"]]
    ws = [max(220, d.textlength(t, font=fb) + 70) for t in tombol]
    bx = (x0 + x1) / 2 - (sum(ws) + 30) / 2
    by = y1 - 36 - 76
    for k, (t, w) in enumerate(zip(tombol, ws)):
        box = (int(bx), by, int(bx + w), by + 76)
        if k == 0:
            d.rectangle((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3), outline="black", width=3)
        bevel(d, box)
        if k == 0:
            for xx in range(box[0] + 10, box[2] - 10, 6):
                d.point([(xx, box[1] + 10), (xx, box[3] - 10)], fill="black")
            for yy in range(box[1] + 10, box[3] - 10, 6):
                d.point([(box[0] + 10, yy), (box[2] - 10, yy)], fill="black")
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), t, font=fb, fill="black", anchor="mm")
        if k == 0:
            cur = (box[2] - 34, box[3] - 22)
        bx += w + 30
    # catatan ayat
    nx0, nx1, ny0 = 150, W - 110, y1 + 46
    fc = ft("Courier New.ttf", 36)
    vlines = wrap(probe, bersih(p["ayat"]), fc, nx1 - nx0 - 90)
    ny1 = ny0 + 56 + 44 + 26 + len(vlines) * 46 + 30 + 50 + 40
    ny1 = min(ny1, H - 100)
    d = jendela(img, (nx0, ny0, nx1, ny1), "ayat.txt - Catatan")
    d.text((nx0 + 24, ny0 + 64), "Berkas   Edit   Format   Bantuan", font=ms(26), fill="black")
    d.rectangle((nx0 + 12, ny0 + 108, nx1 - 12, ny1 - 12), fill="white", outline=(128, 128, 128), width=2)
    y = ny0 + 130
    for ln in vlines:
        d.text((nx0 + 40, y), ln, font=fc, fill="black")
        y += 46
    d.text((nx0 + 40, y + 20), p["ref"], font=ft("Courier New Bold.ttf", 36), fill="black")
    # taskbar
    ty = H - 70
    d.rectangle((0, ty, W, H), fill=ABU95)
    d.line((0, ty + 2, W, ty + 2), fill="white", width=2)
    bevel(d, (8, ty + 10, 168, H - 8))
    d.rectangle((26, ty + 22, 32, ty + 52), fill=(150, 30, 30))
    d.rectangle((18, ty + 30, 40, ty + 36), fill=(150, 30, 30))
    d.text((52, ty + 36), "Mulai", font=tahoma_b(28), fill="black", anchor="lm")
    bevel(d, (180, ty + 10, 560, H - 8), ditekan=True, isi=(212, 212, 212))
    d.text((196, ty + 36), "@" + HANDLE, font=ms(24), fill="black", anchor="lm")
    bevel(d, (W - 140, ty + 10, W - 8, H - 8), ditekan=True)
    d.text((W - 74, ty + 36), p.get("_jam", "16.30"), font=ms(26), fill="black", anchor="mm")
    comp(img, kursor(54), cur)
    return img


# ---------- POLAROID ----------

def vintage(img):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    a = a * 0.86 + 24
    a[..., 0] += 10
    a[..., 2] -= 8
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def selotip(w, h, rng):
    t = Image.new("RGBA", (w, h), (236, 226, 196, 200))
    d = ImageDraw.Draw(t)
    for x in (0, w - 1):
        for y in range(0, h, 6):
            d.line((x, y, x + (4 if x == 0 else -4), y + 3), fill=(0, 0, 0, 0), width=3)
    return t.rotate(rng.uniform(-14, 14), expand=True, resample=Image.BICUBIC)


def polaroid_image(p, i, latar=None):
    rng = np.random.default_rng(400 + i)
    gab = render.fbm2d(H, W, rng, ((10, 1.0), (60, 0.6), (240, 0.5)))
    cork = np.zeros((H, W, 3), np.float32) + np.array([176, 132, 88])
    cork *= (0.78 + 0.45 * gab)[..., None]
    spots = rng.random((H, W)) < 0.012
    cork[spots] *= 0.6
    img = (latar.copy() if latar is not None else grain(Image.fromarray(np.clip(cork, 0, 255).astype(np.uint8)), 0.1)).convert("RGBA")
    # judul di selotip kertas
    fj = tangan(56)
    tw = ImageDraw.Draw(img).textlength(bersih(p["judul"]), font=fj)
    strip = Image.new("RGBA", (int(tw + 90), 100), (246, 240, 222, 255))
    ImageDraw.Draw(strip).text((45, 50), bersih(p["judul"]), font=fj, fill=(40, 40, 40), anchor="lm")
    strip = strip.rotate(-2, expand=True, resample=Image.BICUBIC)
    bayangan(img, strip, ((W - strip.width) // 2, 36), blur=10, geser=(4, 8), kuat=0.35)
    pos = [(50, 175, -6), (660, 165, 5), (345, 540, -3)]
    for (scene, label), (x, y, rot) in zip(p["foto"], pos):
        fr = Image.new("RGBA", (340, 410), (251, 251, 247, 255))
        photo = vintage(cover(foto_warna(scene, 480, 480, seed=410 + i * 3 + x), 306, 306))
        fr.paste(photo, (18, 18))
        fd = ImageDraw.Draw(fr)
        fl = tangan(36)
        while fd.textlength(bersih(label), font=fl) > 304:
            fl = tangan(fl.size - 2)
        fd.text((170, 368), bersih(label), font=fl, fill=(40, 40, 60), anchor="mm")
        fr = fr.rotate(rot, expand=True, resample=Image.BICUBIC)
        bayangan(img, fr, (x, y), blur=14, geser=(6, 12), kuat=0.45)
        tp = selotip(130, 40, rng)
        comp(img, tp, (x + fr.width / 2 - tp.width / 2, y - 12))
    # catatan ayat
    nw = 900
    probe = ImageDraw.Draw(img)
    f, lines, size = pas(probe, bersih(p["ayat"]), tangan, nw - 100, 170, 38, 26, 1.3)
    lines.append("— " + p["ref"])
    nh = int(len(lines) * size * 1.3 + 110)
    note = Image.new("RGBA", (nw, nh), (255, 253, 245, 255))
    nd = ImageDraw.Draw(note)
    for yy in range(70, nh - 10, int(size * 1.3)):
        nd.line((30, yy + size * 1.3 - 8, nw - 30, yy + size * 1.3 - 8), fill=(190, 210, 235), width=2)
    yy = 50
    for k, ln in enumerate(lines):
        last = k == len(lines) - 1
        nd.text((nw - 50 if last else 50, yy), ln, font=f, fill=(36, 54, 120), anchor="ra" if last else "la")
        yy += size * 1.3
    nd.text((nw - 30, nh - 22), "@" + HANDLE, font=hn(20, 0), fill=(150, 150, 150), anchor="rs")
    note = note.rotate(1.2, expand=True, resample=Image.BICUBIC)
    ny = max(990, min(H - note.height - 24, 1060))
    bayangan(img, note, ((W - note.width) // 2, ny), blur=14, geser=(5, 10), kuat=0.4)
    tp = selotip(160, 44, rng)
    comp(img, tp, (W / 2 - tp.width / 2, ny - 18))
    return img


# ---------- PLAYER: pemutar musik, ayat = lirik ----------

def player_image(p, i, terang=False):
    art = foto_warna(p["foto"], 900, 900, seed=500 + i)
    bg = cover(art, W, H).filter(ImageFilter.GaussianBlur(70))
    bg = Image.blend(bg, Image.new("RGB", bg.size, "#FFFFFF" if terang else "#000000"), 0.62 if terang else 0.5)
    img = grain(bg, 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    white = (30, 30, 40, 255) if terang else (255, 255, 255, 255)
    fg = white[:3]
    d.text((W / 2, 46), "SEDANG DIPUTAR", font=hn(22, 10), fill=fg + (170,), anchor="ma")
    d.text((W / 2, 76), "dari album " + p["album"], font=hn(26, 1), fill=white, anchor="ma")
    s = 420
    sq = cover(art, s, s).convert("RGBA")
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s, s), radius=26, fill=255)
    sq.putalpha(m)
    bayangan(img, sq, ((W - s) // 2, 130), blur=30, geser=(0, 20), kuat=0.5)
    d = ImageDraw.Draw(img)
    y = 590
    d.text((90, y), bersih(p["judul"]), font=hn(50, 1), fill=white)
    d.text((90, y + 64), f"{p['penyanyi']} — {p['album']}", font=hn(34, 0), fill=fg + (180,))
    for dx in (-14, 0, 14):
        d.ellipse((W - 112 + dx - 5, y + 50, W - 112 + dx + 5, y + 60), fill=white)
    y = 730
    d.rounded_rectangle((90, y, W - 90, y + 8), radius=4, fill=fg + (80,))
    px = 90 + (W - 180) * (0.28 + 0.08 * (i % 4))
    d.rounded_rectangle((90, y, px, y + 8), radius=4, fill=white)
    d.ellipse((px - 11, y - 7, px + 11, y + 15), fill=white)
    d.text((90, y + 24), f"{1 + i % 3}:{(17 * i + 12) % 60:02d}", font=hn(22, 10), fill=fg + (160,))
    d.text((W - 90, y + 24), f"-{2 + i % 2}:{(23 * i + 31) % 60:02d}", font=hn(22, 10), fill=fg + (160,), anchor="ra")
    cy = 840
    d.rectangle((W / 2 - 22, cy - 30, W / 2 - 8, cy + 30), fill=white)  # jeda
    d.rectangle((W / 2 + 8, cy - 30, W / 2 + 22, cy + 30), fill=white)
    for sgn in (-1, 1):
        cx = W / 2 + sgn * 230
        for k in (0, 1):
            tip = cx + sgn * (k * 28 + 14)
            d.polygon([(tip - sgn * 28, cy - 20), (tip - sgn * 28, cy + 20), (tip, cy)], fill=white)
    lirik = tanpa_kutip(p["ayat"])
    f, lines, size = pas(d, lirik, lambda s: hn(s, 1), W - 180, H - 950 - 90, 40, 26, 1.32)
    y, aktif = 930, min(1, len(lines) - 1)
    for k, ln in enumerate(lines):
        a = 255 if k == aktif else 165 if k < aktif else 130
        d.text((90, y), ln, font=f, fill=fg + (a,))
        y += size * 1.32
    d.text((90, H - 66), f"Lirik: {p['ref']} (TB)", font=hn(24, 10), fill=fg + (170,))
    d.text((W - 90, H - 66), "@" + HANDLE, font=hn(24, 10), fill=fg + (170,), anchor="ra")
    return img


# ---------- KETIK: jurnal mesin tik ----------

def ketik_image(p, i):
    rng = np.random.default_rng(700 + i)
    desk = np.zeros((H, W, 3), np.float32) + np.array([46, 40, 36])
    desk *= (0.8 + 0.4 * render.fbm2d(H, W, rng, ((3, 1.0), (90, 0.3))))[..., None]
    img = Image.fromarray(np.clip(desk, 0, 255).astype(np.uint8)).convert("RGBA")
    pw, ph = 920, 1240
    paper = Image.new("RGBA", (pw, ph), (244, 238, 220, 255))
    pa = np.asarray(paper).astype(np.float32)
    pa[..., :3] *= (0.95 + 0.07 * render.fbm2d(ph, pw, rng, ((5, 1.0), (40, 0.4))))[..., None]
    paper = Image.fromarray(np.clip(pa, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(paper)
    tf = lambda s: ft("AmericanTypewriter.ttc", s, 0)
    body = bersih(p["isi"])
    ayat = bersih(p["ayat"])
    for size in range(36, 22, -2):
        f = tf(size)
        lh = size * 1.5
        b = wrap(d, body, f, pw - 160)
        v = wrap(d, ayat, f, pw - 220)
        if 150 + (len(b) + len(v) + 4) * lh < ph - 110:
            break

    def ketik(x, y, teks):
        for ch in teks:
            a = int(rng.uniform(150, 245))
            d.text((x + rng.uniform(-0.8, 0.8), y + rng.uniform(-1.2, 1.2)), ch, font=f, fill=(30, 28, 26, a))
            x += d.textlength(ch, font=f)

    ketik(pw - 80 - d.textlength(bersih(p["tanggal"]), font=f), 90, bersih(p["tanggal"]))
    y = 90 + lh * 2
    for ln in b:
        ketik(80, y, ln)
        y += lh
    y += lh
    for ln in v:
        ketik(140, y, ln)
        y += lh
    ketik(pw - 80 - d.textlength("— " + p["ref"], font=f), y, "— " + p["ref"])
    d.text((pw / 2, ph - 60), "@" + HANDLE, font=tf(22), fill=(120, 110, 96), anchor="ma")
    paper = paper.filter(ImageFilter.GaussianBlur(0.3)).rotate(-1.0 if i % 2 else 1.0, expand=True, resample=Image.BICUBIC)
    bayangan(img, paper, ((W - paper.width) // 2, (H - paper.height) // 2), blur=22, geser=(10, 18), kuat=0.6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)  # lampu meja dari kiri atas
    light = 1.12 - 0.35 * np.hypot((xx - W * 0.25) / W, (yy - H * 0.1) / H)
    out = np.asarray(img.convert("RGB")).astype(np.float32) * light[..., None]
    return grain(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 0.06)


# ---------- CHAT (Reels): obrolan dengan teman ----------

BIRU, ABU_CHAT = (47, 124, 246), (233, 233, 235)
TOP_CHAT, BAWAH_CHAT = 270, 1440


def gelembung(teks, kanan, maxw=700, aksen=BIRU):
    f = hn(40, 0)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = wrap(probe, teks, f, maxw - 64)
    w = int(max(probe.textlength(ln, font=f) for ln in lines) + 64)
    h = int(len(lines) * 52 + 40)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=36, fill=(aksen if kanan else ABU_CHAT) + (255,))
    y = 20
    for ln in lines:
        d.text((32, y), ln, font=f, fill="white" if kanan else (18, 18, 18))
        y += 52
    return img


def kartu_ayat_chat(ayat, ref, maxw=760, aksen=BIRU):
    f = hn(38, 0)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = wrap(probe, tanpa_kutip(ayat), f, maxw - 90)
    h = int(70 + len(lines) * 50 + 76)
    img = Image.new("RGBA", (maxw, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, maxw, h), radius=30, fill=(255, 255, 255, 255), outline=(222, 222, 226, 255), width=3)
    d.rounded_rectangle((22, 24, 30, h - 24), radius=4, fill=aksen + (255,))
    d.text((54, 26), "AYAT UNTUKMU", font=hn(26, 1), fill=aksen)
    y = 70
    for ln in lines:
        d.text((54, y), ln, font=f, fill=(20, 20, 20))
        y += 50
    d.text((54, y + 14), ref, font=hn(32, 1), fill=aksen)
    return img


def chat_reel(p, idx, mod=MOD, natal=False):
    aksen = (196, 40, 50) if natal else BIRU
    rel = f"reels/{mod}/chat{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    msgs = [(w, bersih(t)) for w, t in p["pesan"]] + [("ayat", p["ayat"])]
    sprites = [kartu_ayat_chat(t, p["ref"], aksen=aksen) if w == "ayat" else gelembung(t, w == "aku", aksen=aksen) for w, t in msgs]
    ys, y = [], TOP_CHAT + 40
    for k, sp in enumerate(sprites):
        ys.append(y)
        nxt = msgs[k + 1][0] if k + 1 < len(msgs) else None
        y += sp.height + (12 if nxt and (nxt == "aku") == (msgs[k][0] == "aku") else 28)
    # waktu: pesan pertama sudah tampil di frame pertama (jadi sampul Reels)
    muncul, ketik, t = [], [], 0.0
    for k, (who, teks) in enumerate(msgs):
        if k:
            dur = 0.8 if who == "aku" else (1.2 if who == "ayat" else 0.9)
            ketik.append((who, k, t, t + dur))
            t += dur
        muncul.append(t)
        t += 0.35 + (len(teks) / 26 if who != "ayat" else 7.0)
    total = t + 0.5
    target = []  # (waktu, offset gulir)
    for k in range(len(msgs)):
        for w_, kk, t0, t1 in ketik:
            if kk == k and w_ != "aku":
                target.append((t0, max(0, ys[k] + 96 - BAWAH_CHAT)))
        target.append((muncul[k], max(0, ys[k] + sprites[k].height - BAWAH_CHAT)))

    def gulir(t):
        prev, off = 0.0, 0.0
        for t0, tg in target:
            if t0 <= t:
                off = prev + (tg - prev) * ease((t - t0) / 0.3)
                prev = tg if t - t0 >= 0.3 else off
        return off

    # bagian tetap: header & kolom ketik
    head = Image.new("RGBA", (RW, TOP_CHAT), (248, 248, 250, 255))
    hd = ImageDraw.Draw(head)
    hd.text((70, 60), p.get("_jam", "13.30"), font=hn(34, 1), fill=(10, 10, 10))
    hd.rounded_rectangle((RW - 150, 64, RW - 92, 92), radius=8, outline=(10, 10, 10), width=3)
    hd.rounded_rectangle((RW - 145, 69, RW - 110, 87), radius=4, fill=(10, 10, 10))
    hd.line((92, 190, 68, 166, 92, 142), fill=aksen, width=7)
    warna = [(240, 140, 90), (120, 180, 120), (140, 120, 220), (230, 110, 150), (90, 160, 220), (220, 170, 70), (110, 190, 190)]
    av = sprite(96, 96, lambda dd, k: dd.ellipse((0, 0, 96 * k, 96 * k), fill=warna[idx % 7] + (255,)))
    comp(head, av, (RW / 2 - 48, 110))
    hd = ImageDraw.Draw(head)
    hd.text((RW / 2, 158), p["nama"][0].upper(), font=hn(46, 1), fill="white", anchor="mm")
    hd.text((RW / 2, 216), p["nama"], font=hn(30, 10), fill=(10, 10, 10), anchor="ma")
    hd.line((0, TOP_CHAT - 2, RW, TOP_CHAT - 2), fill=(224, 224, 228), width=2)
    fi = hn(36, 0)

    def kolom(teks):
        lay = Image.new("RGBA", (RW, RH - BAWAH_CHAT - 10), (255, 255, 255, 255))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((60, 40, RW - 160, 130), radius=45, outline=(214, 214, 220), width=3)
        if teks:
            while ld.textlength(teks, font=fi) > RW - 300:
                teks = teks[1:]
            ld.text((100, 85), teks, font=fi, fill=(20, 20, 20), anchor="lm")
        else:
            ld.text((100, 85), "Ketik pesan", font=fi, fill=(170, 170, 176), anchor="lm")
        ld.ellipse((RW - 140, 40, RW - 50, 130), fill=aksen if teks else (200, 200, 206))
        ld.polygon([(RW - 95, 62), (RW - 118, 92), (RW - 72, 92)], fill="white")
        ld.rectangle((RW - 100, 88, RW - 90, 112), fill="white")
        ld.text((RW / 2, 230), "@" + HANDLE, font=hn(26, 10), fill=(180, 180, 186), anchor="ma")
        return lay

    kosong = kolom("")
    latar_chat = Image.new("RGBA", (RW, RH), (252, 246, 238, 255) if natal else (255, 255, 255, 255))
    if natal:  # wallpaper obrolan: kepingan salju & bintang samar
        rs = np.random.default_rng(950 + idx)
        ld_ = ImageDraw.Draw(latar_chat)
        for _ in range(90):
            x, y, r = rs.uniform(0, RW), rs.uniform(TOP_CHAT, BAWAH_CHAT), rs.uniform(6, 14)
            for a in range(0, 180, 60):
                ang = math.radians(a)
                ld_.line((x - r * math.cos(ang), y - r * math.sin(ang), x + r * math.cos(ang), y + r * math.sin(ang)), fill=(232, 212, 206, 255), width=2)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(int(total * FPS)):
        t = n / FPS
        off = gulir(t)
        frame = latar_chat.copy()
        for k, sp in enumerate(sprites):
            if t >= muncul[k]:
                a = 1.0 if k == 0 else ease((t - muncul[k]) / 0.25)
                x = RW - 50 - sp.width if msgs[k][0] == "aku" else 50
                comp(frame, fade(sp, a), (x, ys[k] - off + (1 - a) * 40))
        bar = kosong
        for who, k, t0, t1 in ketik:
            if t0 <= t < t1:
                if who == "aku":
                    teks = msgs[k][1]
                    bar = kolom(teks[:max(1, int(len(teks) * (t - t0) / (t1 - t0 - 0.1)))])
                else:
                    tb = Image.new("RGBA", (150, 84), (0, 0, 0, 0))
                    td = ImageDraw.Draw(tb)
                    td.rounded_rectangle((0, 0, 150, 84), radius=42, fill=ABU_CHAT + (255,))
                    for j in range(3):
                        dy = 8 * math.sin(2 * math.pi * (t * 2.2 - j * 0.18))
                        td.ellipse((35 + j * 30 - 9, 42 - dy - 9, 35 + j * 30 + 9, 42 - dy + 9), fill=(140, 140, 146))
                    comp(frame, tb, (50, ys[k] - off))
        frame.alpha_composite(head, (0, 0))
        frame.alpha_composite(bar, (0, BAWAH_CHAT + 10))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- NEON (Reels): lampu neon di dinding bata ----------

NEON = {"pink": (255, 70, 170), "biru": (60, 170, 255), "kuning": (255, 196, 60), "hijau": (60, 255, 150),
        "ungu": (180, 100, 255), "merah": (255, 64, 64)}


def bata(w, h, seed):
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), np.float32) + np.array([34, 30, 30])
    bw, bh, m = 150, 56, 8
    for row in range(h // bh + 1):
        off = (row % 2) * bw // 2
        for col in range(-1, w // bw + 2):
            x0, y0 = col * bw + off, row * bh
            c = np.array([92, 48, 40]) * rng.uniform(0.7, 1.15)
            img[max(0, y0 + m // 2):min(h, y0 + bh - m // 2), max(0, x0 + m // 2):min(w, x0 + bw - m // 2)] = c
    img *= (0.7 + 0.6 * render.fbm2d(h, w, rng, ((8, 1.0), (60, 0.5), (240, 0.4))))[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    img *= (0.55 - 0.3 * np.hypot((xx - w / 2) / w, (yy - h * 0.45) / h))[..., None]
    return img


def neon_layer(mask, col):
    """-> (cahaya tambahan float, alpha tabung, warna tabung) untuk satu teks neon."""
    m = np.asarray(mask).astype(np.float32) / 255
    blur = lambda r: np.asarray(mask.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255
    c = np.array(col, np.float32)
    light = blur(130)[..., None] * c * 1.6 + blur(34)[..., None] * c * 1.3 + blur(9)[..., None] * c * 0.9
    core = np.asarray(mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
    tube = c * 0.45 + 255 * 0.55
    return light, m, core, tube


def neon_mask(lines, font, w, h, cy, lh):
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    y = cy - len(lines) * lh / 2
    for ln in lines:
        d.text((w / 2, y + lh / 2), ln, font=font, fill=255, anchor="mm", stroke_width=2, stroke_fill=255)
        y += lh
    return mask


def neon_reel(p, idx, mod=MOD, seconds=10):
    rel = f"reels/{mod}/neon{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    wall = bata(RW, RH, 800 + idx)
    lines = bersih(p["teks"]).split("\n")
    probe = ImageDraw.Draw(Image.new("L", (10, 10)))
    size = 190
    sp = lambda s: ft("SignPainter.ttc", s, 1)
    while max(probe.textlength(ln, font=sp(size)) for ln in lines) > RW - 180:
        size -= 6
    lh = size * 0.98
    col = NEON.get(p["warna"], NEON["pink"])
    layers = [neon_layer(neon_mask([ln], sp(size), RW, RH, 820 - (len(lines) - 1) * lh / 2 + k * lh, lh), col)
              for k, ln in enumerate(lines)]
    ref_mask = neon_mask([p["ref"].upper()], ft("Futura.ttc", 48, 0), RW, RH, 820 + len(lines) * lh / 2 + 110, 60)
    ref_l = neon_layer(ref_mask, (255, 236, 210))
    hand = Image.new("L", (RW, RH), 0)
    ImageDraw.Draw(hand).text((RW / 2, 1360), "@" + HANDLE, font=hn(30, 10), fill=255, anchor="mm")
    hand = np.asarray(hand).astype(np.float32)[..., None] / 255
    rng = np.random.default_rng(900 + idx)
    flick = rng.random(seconds * FPS)

    def nyala(t, k):
        if t < 0.6:
            return 1.0
        if t < 1.7:
            on = [(0.75, 0.85), (1.1, 1.16), (1.3, 1.7)]
            for a, b in on:
                if a <= t < b:
                    return ease((t - a) / 0.05) if b - a < 0.2 else ease((t - a) / 0.3)
            return 0.0
        if k == len(lines) - 1 and 5.2 <= t < 5.5:
            return 0.15 if int(t * 20) % 2 else 1.0
        return 0.97 + 0.03 * math.sin(2 * math.pi * 7 * t)

    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(seconds * FPS):
        t = n / FPS
        frame = wall.copy()
        tubes = []
        for k, (light, m, core, tube) in enumerate(layers):
            a = nyala(t, k) * (0.96 + 0.04 * flick[n])
            frame += light * a
            tubes.append((m, core, tube, a))
        ra = 1.0 if t < 0.6 else (0.0 if t < 1.9 else ease((t - 1.9) / 0.4))
        frame += ref_l[0] * ra * 0.6
        tubes.append((ref_l[1], ref_l[2], ref_l[3], ra))
        for m, core, tube, a in tubes:
            mm = m[..., None]
            lit = tube * a + np.array([70, 64, 64], np.float32) * (1 - a)
            frame = frame * (1 - mm) + lit * mm
            frame = frame * (1 - core[..., None] * a * 0.8) + 255 * core[..., None] * a * 0.8
        frame = frame * (1 - hand * 0.7) + 200 * hand * 0.7
        img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8))
        z = 1 + 0.05 * t / seconds
        zw, zh = int(RW * z), int(RH * z)
        img = img.resize((zw, zh), Image.BILINEAR).crop(((zw - RW) // 2, (zh - RH) // 2, (zw - RW) // 2 + RW, (zh - RH) // 2 + RH))
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- semua ----------

SIMPLE = {"CUACA": cuaca_image, "KAMUS": kamus_image, "TIKET": tiket_image, "CATATAN": catatan_image, "STRUK": struk_image,
          "KALENDER": kalender_image, "POPUP": popup_image, "POLAROID": polaroid_image, "PLAYER": player_image, "KETIK": ketik_image}
REELS = {"CHAT": chat_reel, "NEON": neon_reel}


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
