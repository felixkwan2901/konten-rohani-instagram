"""Akun Tenang - gaya minggu 5 (konten/tenang_w5.py), terinspirasi gaya (bukan isi) akun Kristen populer:
  KUTIPAN = halaman buku putih, kutipan serif dengan stabilo pink & huruf miring, garis tepi kiri
  BESAR   = huruf sangat besar yang menembus tepi kiri, campuran tebal / miring biru / stabilo (Reels: baris meluncur)
  KERTAS  = kertas catatan putih di atas foto hitam-putih
  KOMIK   = komik garis biru: "aku" dan Yesus, dua balon dialog (Reels: balon muncul bergantian)
  SERI    = carousel blok warna "Lima Sola" (minggu Reformasi)
  HITUNG  = hitung mundur Natal harian

  python3 gaya_w5.py [reels]
"""
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cerita
import config
import keren
import render
from cerita import bubble_img, jesus_fig, paste_bubble, place
from render import NAVY, OUT, W, H, eli_fig, grain, save, svg_layer

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w5"
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
PINK = (247, 197, 210)


def hn(size, idx=0):
    return ImageFont.truetype(HN, size, index=idx)


# ---------- teks kaya (markup) ----------

def parse(text):
    """'*tebal*', '_miring_', '[stabilo]' -> daftar kata, tiap kata = [(potongan, gaya)]. gaya: n / b / i / h"""
    words, cur, seg, style = [], [], "", "n"
    close = {"*": "b", "_": "i", "[": "h"}

    def flush_seg():
        nonlocal seg
        if seg:
            cur.append((seg, style))
            seg = ""
    for ch in text:
        if ch in "*_[]":
            flush_seg()
            if ch == "]" or (ch in "*_" and style == close[ch]):
                style = "n"
            else:
                style = close[ch]
        elif ch.isspace():
            flush_seg()
            if cur:
                words.append(cur)
                cur = []
        else:
            seg += ch
    flush_seg()
    if cur:
        words.append(cur)
    return words


def layout(words, fonts, maxw):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    wlen = lambda w: sum(d.textlength(t, font=fonts[s]) for t, s in w)
    space = d.textlength(" ", font=fonts["n"])
    lines, cur, cw = [], [], 0
    for w in words:
        ww = wlen(w)
        if cur and cw + space + ww > maxw:
            lines.append(cur)
            cur, cw = [], 0
        cw += (space if cur else 0) + ww
        cur.append(w)
    if cur:
        lines.append(cur)
    return lines, space, wlen


def draw_rich(img, lines, fonts, colors, x0, y0, lh, space, wlen, align="left", width=None, hl=PINK):
    """Gambar baris teks kaya; stabilo = kotak pink setengah tinggi di belakang kata."""
    d = ImageDraw.Draw(img)
    size = fonts["n"].size
    y = y0
    for line in lines:
        total = sum(wlen(w) for w in line) + space * (len(line) - 1)
        x = x0 if align == "left" else x0 + (width - total) / 2
        for k, w in enumerate(line):
            for t, s in w:
                tw = d.textlength(t, font=fonts[s])
                if s == "h":
                    d.rectangle((x - 3, y + size * 0.42, x + tw + 3, y + size * 1.08), fill=hl)
                d.text((x, y), t, font=fonts[s], fill=colors[s])
                x += tw
            nxt = line[k + 1] if k + 1 < len(line) else None
            if nxt and w[-1][1] == "h" and nxt[0][1] == "h":
                d.rectangle((x, y + size * 0.42, x + space, y + size * 1.08), fill=hl)
            x += space
        y += lh
    return y


# ---------- KUTIPAN ----------

def kutipan_image(p, i):
    img = grain(Image.new("RGB", (W, H), "#FBFAF6"), 0.08)
    fs = 60
    fonts = {"n": ImageFont.truetype(GEORGIA, fs), "b": ImageFont.truetype(GEORGIA, fs), "i": ImageFont.truetype(GEORGIA_I, fs),
             "h": ImageFont.truetype(GEORGIA, fs)}
    colors = {k: "#262626" for k in fonts}
    teks = p["teks"].strip()
    if not teks.startswith(("“", '"')):
        teks = "“" + teks + "”"
    lines, space, wlen = layout(parse(teks), fonts, 780)
    lh = 88
    block = len(lines) * lh
    y0 = H * 0.46 - block / 2
    d = ImageDraw.Draw(img)
    d.text((150, y0 - 80), p["sumber"], font=ImageFont.truetype(GEORGIA_I, 32), fill="#8D877D")
    d.line([(118, y0 - 80), (118, y0 + block + 60)], fill="#DCD6CC", width=5)
    y = draw_rich(img, lines, fonts, colors, 150, y0, lh, space, wlen)
    d.text((150, y + 36), "@" + HANDLE, font=ImageFont.truetype(GEORGIA_I, 28), fill="#A39C91")
    return img


# ---------- BESAR ----------

BIRU = "#2D5BD6"


def besar_fonts(size):
    return {"n": hn(size, 0), "b": hn(size, 1), "i": hn(size, 2), "h": hn(size, 0)}


def besar_layer(p, w=W, h=H, top=None):
    for size in range(104, 60, -4):
        fonts = besar_fonts(size)
        lines, space, wlen = layout(parse(p["teks"]), fonts, w - 100)
        if len(lines) <= 6:
            break
    colors = {"n": "#141414", "b": "#141414", "i": BIRU, "h": "#141414"}
    lh = size * 1.12
    block = len(lines) * lh
    y0 = top if top is not None else h * 0.62 - block / 2
    return fonts, lines, space, wlen, colors, lh, y0, block


def besar_image(p, i):
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.text((W - 50, 50), "©" + HANDLE.upper(), font=hn(26, 1), fill="#141414", anchor="ra")
    fonts, lines, space, wlen, colors, lh, y0, block = besar_layer(p)
    y = draw_rich(img, lines, fonts, colors, 44, y0, lh, space, wlen)
    if p.get("ref"):
        d.text((48, y + 10), f"({p['ref']})", font=hn(fonts["n"].size // 2 + 6, 0), fill="#555555")
    return img


def besar_reel(p, i, seconds=9):
    """Baris-baris besar meluncur masuk dari kanan bergantian, lalu diam; referensi muncul di akhir."""
    import musik
    rel = f"reels/{MOD}/besar{i + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rw, rh = 1080, 1920
    fonts, lines, space, wlen, colors, lh, y0, block = besar_layer(p, rw, rh, top=None)
    y0 = rh * 0.48 - block / 2
    sprites = []
    for k, line in enumerate(lines):
        lay = Image.new("RGBA", (rw + 200, int(lh + 40)), (0, 0, 0, 0))
        draw_rich(lay, [line], fonts, colors, 0, 10, lh, space, wlen)
        sprites.append(lay)
    head = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    ImageDraw.Draw(head).text((rw - 50, 260), "©" + HANDLE.upper(), font=hn(28, 1), fill="#141414", anchor="ra")
    ref = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    if p.get("ref"):
        ImageDraw.Draw(ref).text((48, y0 + block + 20), f"({p['ref']})", font=hn(44, 0), fill="#555555")
    ff = cerita.ffmpeg_writer(out, rw, rh, 30)
    for n in range(30 * seconds):
        t = n / 30
        frame = Image.new("RGBA", (rw, rh), "#FFFFFF")
        frame.alpha_composite(head)
        for k, sp in enumerate(sprites):
            a = keren.ease((t - 0.4 - k * 0.45) / 0.7)
            if a <= 0:
                continue
            x = int(44 + (1 - a) * (rw * 0.9) * (1 if k % 2 == 0 else -1))
            frame.alpha_composite(keren.with_alpha(sp, a), (x, int(y0 + k * lh - 10)))
        last = 0.4 + len(sprites) * 0.45 + 0.8
        if t > last:
            frame.alpha_composite(keren.with_alpha(ref, keren.ease((t - last) / 0.5)))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(rel)
    wav, _ = musik.lagu_unik(rel, seconds + 1, set())
    musik.pasang(rel, str(wav))
    return rel


# ---------- KERTAS ----------

def kertas_image(p, i):
    photo = keren.foto(p["foto"], seed=700 + i)
    photo = Image.blend(photo, Image.new("RGB", photo.size, "#000000"), 0.25).convert("RGBA")
    f = hn(56, 1)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = render.wrap(probe, p["teks"], f, 700)
    lh = 70
    ref_h = 60 if p.get("ref") else 0
    cw, ch = 820, 100 + len(lines) * lh + ref_h
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rectangle((0, 0, cw, ch), fill=(250, 250, 247, 255))
    y = 50
    for ln in lines:
        d.text((55, y), ln, font=f, fill="#151515")
        y += lh
    if p.get("ref"):
        d.text((55, y + 8), p["ref"], font=hn(32, 0), fill="#444444")
    card = card.rotate(-1.5, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.putalpha(card.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55)))
    x, y = (W - card.width) // 2, int(H * 0.47 - card.height / 2)
    photo.alpha_composite(sh, (x + 10, y + 16))
    photo.alpha_composite(card, (x, y))
    ImageDraw.Draw(photo).text((W - 50, 50), HANDLE.upper(), font=hn(24, 1), fill=(255, 255, 255, 220), anchor="ra")
    return photo


# ---------- KOMIK ----------

CREAM = "#FBF7EE"
GROUND, KF = 1150, 2.6


def latar(adegan):
    s = f'stroke="{NAVY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    floor = f'<path d="M70,{GROUND} L1010,{GROUND}" {s} fill="none"/>'
    if adegan == "pintu":
        return (floor + f'<rect x="120" y="470" width="250" height="680" fill="#FFFFFF" {s}/>'
                f'<path d="M370,470 L470,520 L470,1150 L370,1150" fill="#E9EFF9" {s}/><circle cx="452" cy="830" r="8" fill="{NAVY}"/>'
                f'<rect x="150" y="1150" width="200" height="16" rx="6" fill="#F8C9D2" {s}/>'), (245, 870)
    if adegan == "kamar":
        stars = "".join(f'<path d="M{x},{y} l4,10 l10,4 l-10,4 l-4,10 l-4,-10 l-10,-4 l10,-4 z" fill="#FBE38E" stroke="{NAVY}" stroke-width="1.5"/>'
                        for x, y in ((700, 260), (840, 330), (760, 400)))
        return (floor + f'<rect x="640" y="200" width="300" height="300" fill="#26407A" {s}/>'
                f'<path d="M790,200 L790,500 M640,350 L940,350" {s}/><circle cx="880" cy="260" r="34" fill="#FBE38E" stroke="{NAVY}" stroke-width="2"/>'
                + stars + f'<rect x="90" y="930" width="470" height="220" rx="18" fill="#E9EFF9" {s}/>'
                f'<rect x="110" y="880" width="150" height="70" rx="22" fill="#FFFFFF" {s}/>'), (330, 760)
    if adegan == "hujan":
        rain = "".join(f'<path d="M{x},{y} l-18,40" stroke="#8FA9D6" stroke-width="3" stroke-linecap="round"/>'
                       for x in range(90, 1020, 70) for y in range(170 + (x % 140), 1100, 160))
        return floor + rain + f'<path d="M200,{GROUND - 4} q40,-14 80,0 q40,14 80,0" fill="none" stroke="#8FA9D6" stroke-width="3"/>', (440, 690)
    if adegan == "jalan":
        return (f'<path d="M70,760 Q300,690 540,740 T1010,720" fill="none" {s}/>'
                f'<path d="M440,1150 Q520,900 560,760 M760,1150 Q640,900 590,760" fill="none" {s}/>'
                f'<circle cx="820" cy="320" r="60" fill="#FBE38E" stroke="{NAVY}" stroke-width="2"/>' + floor), (420, 720)
    # bangku
    return (floor + f'<path d="M160,1150 L160,1010 M520,1150 L520,1010" {s}/><rect x="120" y="980" width="440" height="34" rx="8" fill="#F3D9B1" {s}/>'
            f'<rect x="120" y="900" width="440" height="26" rx="8" fill="#F3D9B1" {s}/>'
            f'<path d="M880,1150 L880,700" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/><circle cx="880" cy="560" r="170" fill="#CFE8D4" {s}/>'), (330, 760)


def komik_layers(p, w=W, h=H):
    body, (xa, ya) = latar(p["adegan"])
    duduk = p["adegan"] in ("kamar", "bangku")
    aku_x = 330 if duduk else {"pintu": 700, "hujan": 660}.get(p["adegan"], 420)
    aku_y = (GROUND - 160) if p["adegan"] == "kamar" else (GROUND - 140 if p["adegan"] == "bangku" else GROUND)
    yesus_x = {"pintu": 245, "kamar": 760, "hujan": 380, "jalan": 650, "bangku": 700}[p["adegan"]]
    arms = p["yesus"] if p["yesus"] in ("bawah", "sambut", "tunjuk", "payung") else "bawah"
    figs = place(jesus_fig(arms), yesus_x, GROUND, KF) + place(eli_fig(p["wajah"], p["tangan"], piyama=p["adegan"] == "kamar", duduk=duduk), aku_x, aku_y, KF)
    if p["adegan"] == "hujan":
        hx0, hy = yesus_x + 46 * KF, GROUND - 140 * KF  # tangan Yesus
        hx, top = hx0 + 20, GROUND - 236 * KF  # payung di atas kepala keduanya (Yesus di kiri, anak di kanan)
        figs += (f'<path d="M{hx0},{hy} L{hx},{top}" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>'
                 f'<path d="M{hx - 300},{top} Q{hx},{top - 230} {hx + 300},{top} Q{hx + 225},{top - 30} {hx + 150},{top} '
                 f'Q{hx + 75},{top - 30} {hx},{top} Q{hx - 75},{top - 30} {hx - 150},{top} Q{hx - 225},{top - 30} {hx - 300},{top} Z" '
                 f'fill="#F8C9D2" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    panel = f'<rect x="60" y="110" width="960" height="1130" fill="none" stroke="{NAVY}" stroke-width="4"/>'
    base = Image.new("RGBA", (W, H), CREAM)
    base.alpha_composite(svg_layer(body + figs + panel))
    d = ImageDraw.Draw(base)
    d.text((W / 2, H - 70), "@" + HANDLE.upper(), font=hn(22, 1), fill=NAVY, anchor="ma")
    left_is_aku = aku_x < yesus_x
    b_aku = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b_yes = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ax = 300 if left_is_aku else 760
    yx = 760 if left_is_aku else 300
    ya, yy = (200, 330) if p["adegan"] == "hujan" else (300, 470)
    paste_bubble(b_aku, bubble_img(p["aku"], "#F8C9D2", (60 if left_is_aku else -60, 110), maxw=300), (ax, ya))
    paste_bubble(b_yes, bubble_img(p["kata_yesus"], "#FBE38E", (-60 if left_is_aku else 60, 120), maxw=320), (yx, yy))
    return base, b_aku, b_yes


def komik_image(p, i):
    base, a, b = komik_layers(p)
    base.alpha_composite(a)
    base.alpha_composite(b)
    return base


def komik_reel(p, i, seconds=10):
    import musik
    rel = f"reels/{MOD}/komik{i + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    base, ba, bb = komik_layers(p)
    canvas_bg = Image.new("RGB", (1080, 1920), CREAM)
    ff = cerita.ffmpeg_writer(out, 1080, 1920, 30)

    def pop(layer, t0, t):
        a = keren.ease((t - t0) / 0.35)
        if a <= 0:
            return None
        if a >= 1:
            return layer
        bbox = layer.getbbox()
        crop = layer.crop(bbox)
        k = 0.7 + 0.3 * a
        crop = crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))), Image.BILINEAR)
        lay = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
        lay.alpha_composite(keren.with_alpha(crop, a), (int(cx - crop.width / 2), int(cy - crop.height / 2)))
        return lay
    for n in range(30 * seconds):
        t = n / 30
        frame = base.copy()
        for layer, t0 in ((ba, 1.0), (bb, 3.2)):
            l = pop(layer, t0, t)
            if l is not None:
                frame.alpha_composite(l)
        z = 1 + 0.04 * t / seconds
        zw, zh = int(W * z), int(H * z)
        fr = frame.convert("RGB").resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        c = canvas_bg.copy()
        c.paste(fr, (0, 285))
        ff.stdin.write(c.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(rel)
    wav, _ = musik.lagu_unik(rel, seconds + 1, set())
    musik.pasang(rel, str(wav))
    return rel


# ---------- SERI ----------

PALET = [("#1F3D2B", "#F4EEDF", "#E8B04B"), ("#B4532A", "#FBF1E3", "#F3D9B1"), ("#1B2A4A", "#F4EEDF", "#E8B04B"),
         ("#E2A72E", "#1E1E1E", "#FFFFFF"), ("#4A2545", "#F4EEDF", "#E8B04B"), ("#1F5C5B", "#F4EEDF", "#F3D9B1"),
         ("#7A1F2B", "#FBF1E3", "#E8B04B")]


def didot(size):
    return ImageFont.truetype(DIDOT, size, index=2)


def seri_slides(p, i):
    bg, fg, ac = PALET[i % len(PALET)]
    total = len(p["slides"]) + 2
    out = []
    # sampul
    img = grain(Image.new("RGB", (W, H), bg), 0.1)
    d = ImageDraw.Draw(img)
    d.text((70, 60), p["nomor"], font=didot(320), fill=None, stroke_width=3, stroke_fill=ac)
    d.text((80, 470), "SERI REFORMASI", font=hn(30, 1), fill=ac)
    for size in range(150, 70, -6):
        lines = render.wrap(d, p["judul"], didot(size), W - 160)
        if len(lines) <= 2:
            break
    y = 540
    for ln in lines:
        d.text((76, y), ln, font=didot(size), fill=fg)
        y += size * 1.05
    d.text((80, y + 30), p["arti"], font=ImageFont.truetype(GEORGIA_I, 48), fill=fg)
    d.text((80, H - 120), f"geser  ›    1/{total}", font=hn(28, 1), fill=ac)
    d.text((W - 70, H - 120), "@" + HANDLE, font=hn(26, 0), fill=fg, anchor="ra")
    out.append(img)
    for n, (hd, bd) in enumerate(p["slides"], 2):
        img = grain(Image.new("RGB", (W, H), bg), 0.1)
        d = ImageDraw.Draw(img)
        d.text((80, 90), f"{p['nomor']} · {p['judul'].upper()}", font=hn(26, 1), fill=ac)
        d.line([(80, 140), (W - 80, 140)], fill=ac, width=2)
        y = 330
        for ln in render.wrap(d, hd, didot(76), W - 160):
            d.text((80, y), ln, font=didot(76), fill=fg)
            y += 86
        y += 40
        for ln in render.wrap(d, bd, hn(42, 0), W - 160):
            d.text((80, y), ln, font=hn(42, 0), fill=fg)
            y += 60
        d.text((80, H - 120), f"{n}/{total}", font=hn(28, 1), fill=ac)
        out.append(img)
    img = grain(Image.new("RGB", (W, H), ac), 0.1)
    d = ImageDraw.Draw(img)
    ink = bg
    y = 360
    for ln in render.wrap(d, p["ayat"], ImageFont.truetype(GEORGIA_I, 54), W - 180):
        d.text((90, y), ln, font=ImageFont.truetype(GEORGIA_I, 54), fill=ink)
        y += 76
    d.text((90, y + 30), p["ref"].upper(), font=hn(32, 1), fill=ink)
    d.text((90, H - 120), f"{total}/{total}   ·   @{HANDLE}", font=hn(26, 1), fill=ink)
    out.append(img)
    return [save(s, f"{MOD}/seri{i + 1}_{n}.jpg") for n, s in enumerate(out, 1)]


# ---------- HITUNG ----------

def hitung_image(p, i):
    rng = np.random.default_rng(900 + i)
    img = Image.new("RGB", (W, H), "#173E2E")
    d = ImageDraw.Draw(img)
    for _ in range(140):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.choice([1.5, 2, 2.5, 3.5])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(232, 196, 110))
    img = grain(img, 0.12)
    d = ImageDraw.Draw(img)
    tx, ty, tw, th = (W - 440) // 2, 230, 440, 470
    d.rounded_rectangle((tx + 10, ty + 14, tx + tw + 10, ty + th + 14), radius=36, fill="#0E2A1F")
    d.rounded_rectangle((tx, ty, tx + tw, ty + th), radius=36, fill="#FBF6EA")
    d.rounded_rectangle((tx, ty, tx + tw, ty + 110), radius=36, fill="#B3262E")
    d.rectangle((tx, ty + 70, tx + tw, ty + 110), fill="#B3262E")
    d.text((W / 2, ty + 55), "MENUJU NATAL", font=hn(38, 1), fill="#FBF6EA", anchor="mm")
    d.text((W / 2, ty + 290), str(p["hari"]), font=hn(260, 1), fill="#1B1B1B", anchor="mm")
    d.text((W / 2, ty + th + 90), "hari lagi menuju Natal", font=ImageFont.truetype(GEORGIA_I, 58), fill="#FBF6EA", anchor="ma")
    y = ty + th + 200
    for ln in render.wrap(d, p["teks"], hn(42, 0), W - 220):
        d.text((W / 2, y), ln, font=hn(42, 0), fill="#E8C46E", anchor="ma")
        y += 58
    d.text((W / 2, H - 90), "@" + HANDLE, font=hn(26, 1), fill="#FBF6EA", anchor="ma")
    return img


# ---------- semua ----------

def render_week(mod=MOD):
    import importlib
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "KUTIPAN":
                p = t.KUTIPAN[idx]
                out[(hari, slot)] = ([save(kutipan_image(p, idx), f"{mod}/kutipan{idx + 1}.jpg")], p["caption"])
            elif fmt == "BESAR":
                p = t.BESAR[idx]
                reel = f"reels/{mod}/besar{idx + 1}.mp4"
                files = [reel] if slot in ("siang2", "malam0") and (OUT / reel).exists() else [save(besar_image(p, idx), f"{mod}/besar{idx + 1}.jpg")]
                out[(hari, slot)] = (files, p["caption"])
            elif fmt == "KERTAS":
                p = t.KERTAS[idx]
                out[(hari, slot)] = ([save(kertas_image(p, idx), f"{mod}/kertas{idx + 1}.jpg")], p["caption"])
            elif fmt == "KOMIK":
                p = t.KOMIK[idx]
                reel = f"reels/{mod}/komik{idx + 1}.mp4"
                files = [reel] if slot == "malam0" and (OUT / reel).exists() else [save(komik_image(p, idx), f"{mod}/komik{idx + 1}.jpg")]
                out[(hari, slot)] = (files, p["caption"])
            elif fmt == "SERI":
                p = t.SERI[idx]
                out[(hari, slot)] = (seri_slides(p, idx), p["caption"])
            elif fmt == "ELI":
                import tenang_eli
                out[(hari, slot)] = tenang_eli.render_item(t.ELI[idx])
            elif fmt == "HITUNG":
                p = t.HITUNG[idx]
                out[(hari, slot)] = ([save(hitung_image(p, idx), f"{mod}/hitung{idx + 1}.jpg")], p["caption"])
    return out


def render_reels(mod=MOD):
    import importlib
    t = importlib.import_module(f"konten.{mod}")
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "BESAR" and slot in ("siang2", "malam0"):
                print(besar_reel(t.BESAR[idx], idx))
            if fmt == "KOMIK" and slot == "malam0":
                print(komik_reel(t.KOMIK[idx], idx))


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
