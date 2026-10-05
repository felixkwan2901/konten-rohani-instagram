"""Akun Tenang - minggu 6 (konten/tenang_w6.py): 12 gaya berbeda per hari.
Baru (terinspirasi gaya, bukan isi): LAYAR (layar kunci HP), ALKITAB (foto halaman Alkitab + stabilo), RETRO (poster gradien),
POSTER (foto pemandangan + huruf kapital raksasa), MINIMAL (layar hitam satu kalimat), LED (papan titik-titik menyala),
DOA (kartu doa, kalimat kunci merah). Lama: A editorial, C warna, D dinding (Reels), R suasana (Reels), HITUNG, ELI.

  python3 gaya_w6.py [reels]
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cek_ayat
import config
import gaya_w5
import render
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w6"
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
SUP = "/System/Library/Fonts/Supplemental/"


def hn(size, idx=0):
    return ImageFont.truetype(HN, size, index=idx)


def georgia(size, italic=False):
    return ImageFont.truetype(SUP + ("Georgia Italic.ttf" if italic else "Georgia.ttf"), size)


def foto_warna(kind, w=W, h=H, seed=5):
    if kind in ("fajar", "laut"):
        return render.landscape(kind, w, h, seed)
    return render.suasana_scene(kind, w, h, seed)(5.0)


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    return img.crop(((img.width - w) // 2, (img.height - h) // 2, (img.width - w) // 2 + w, (img.height - h) // 2 + h))


# ---------- LAYAR KUNCI ----------

def layar_image(p, i):
    bg = foto_warna(p["foto"], seed=60 + i).filter(ImageFilter.GaussianBlur(3))
    bg = Image.blend(bg, Image.new("RGB", bg.size, "#000000"), 0.18).convert("RGBA")
    d = ImageDraw.Draw(bg)
    d.text((W / 2, 150), p["hari"], font=hn(40, 10), fill=(255, 255, 255, 235), anchor="ma")
    d.text((W / 2, 200), p["jam"], font=hn(230, 7), fill=(255, 255, 255, 245), anchor="ma")
    # kartu notifikasi buram
    f_t, f_b = hn(36, 1), hn(36, 0)
    lines = wrap(d, p["pesan"] + (f" ({p['ref']})" if p.get("ref") else ""), f_b, 820)
    ch = 150 + len(lines) * 48
    x0, y0, x1 = 60, 560, W - 60
    region = bg.crop((x0, y0, x1, y0 + ch)).filter(ImageFilter.GaussianBlur(25))
    glass = Image.blend(region.convert("RGB"), Image.new("RGB", region.size, "#FFFFFF"), 0.55).convert("RGBA")
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, region.width, region.height), radius=40, fill=255)
    bg.paste(glass, (x0, y0), mask)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((x0 + 30, y0 + 30, x0 + 100, y0 + 100), radius=18, fill="#7A4E2D")
    d.rectangle((x0 + 62, y0 + 44, x0 + 68, y0 + 86), fill="#F4E6CC")
    d.rectangle((x0 + 50, y0 + 56, x0 + 80, y0 + 62), fill="#F4E6CC")
    d.text((x0 + 120, y0 + 34), p["pengirim"].upper(), font=hn(26, 10), fill="#3A3A3A")
    d.text((x1 - 30, y0 + 34), "sekarang", font=hn(26, 0), fill="#555555", anchor="ra")
    d.text((x0 + 120, y0 + 70), p["pengirim"], font=f_t, fill="#111111")
    y = y0 + 125
    for ln in lines:
        d.text((x0 + 40, y), ln, font=f_b, fill="#1C1C1C")
        y += 48
    for cx in (150, W - 150):  # tombol senter & kamera
        d.ellipse((cx - 55, H - 190, cx + 55, H - 80), fill=(0, 0, 0, 90))
    d.rounded_rectangle((W / 2 - 140, H - 40, W / 2 + 140, H - 30), radius=5, fill=(255, 255, 255, 230))
    d.text((W / 2, H - 135), "@" + HANDLE, font=hn(24, 10), fill=(255, 255, 255, 220), anchor="mm")
    return bg


# ---------- ALKITAB (halaman + stabilo) ----------

STABILO = {"kuning": (255, 226, 80, 150), "pink": (255, 150, 190, 140), "hijau": (150, 235, 140, 140)}


def alkitab_image(p, i):
    import re
    m = cek_ayat.REF_RE.search(p["ref"])
    book, ch, v = m.group(1), int(m.group(2)), int(m.group(3))
    chap = cek_ayat.tb_chapter(cek_ayat.ID_BOOKS[book], ch)
    nums = sorted(int(k.split(":")[1]) for k in chap if k.startswith(f"{ch}:"))
    pw, ph = 1120, 1900
    page = Image.new("RGBA", (pw, ph), (247, 242, 230, 255))
    d = ImageDraw.Draw(page)
    f, fn, fh = georgia(36), hn(22, 1), hn(28, 1)
    colw, gap, top, lh = 980, 80, 150, 54
    d.text((pw / 2, 60), f"{book.upper()} {ch}", font=fh, fill="#5A4A3A", anchor="ma")
    start = max(nums[0], v - 4)
    hl_boxes = []
    col, y = 0, top
    for n in [k for k in nums if k >= start]:
        words = re.sub(r"\s+", " ", chap[f"{ch}:{n}"]).split()
        x0 = 60 + col * (colw + gap)
        x = x0
        d.text((x, y + 2), str(n), font=fn, fill="#A0522D")
        x += 34
        for wd in words:
            ww = d.textlength(wd + " ", font=f)
            if x + ww > x0 + colw:
                y += lh
                x = x0
                if y > ph - 120:
                    col += 1
                    y, x0 = top, 60 + (col) * (colw + gap)
                    x = x0
            if n == v:
                hl_boxes.append((x - 4, y + 6, x + ww, y + lh - 2))
            d.text((x, y), wd, font=f, fill="#2B2420")
            x += ww
        y += lh
        if y > ph - 120:
            col += 1
            y = top
        if col > 0:
            break
    hl = Image.new("RGBA", page.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    for b in hl_boxes:
        hd.rectangle(b, fill=STABILO.get(p.get("warna"), STABILO["kuning"]))
    page = Image.alpha_composite(page, hl)
    d = ImageDraw.Draw(page)
    if hl_boxes:  # catatan tangan di pinggir + hati
        bx = hl_boxes[0]
        side_right = bx[0] > pw / 2
        nx = pw - 70 if side_right else 15
        tx = ImageFont.truetype(config.FONT["tangan"][0], 34, index=config.FONT["tangan"][1])
        note = Image.new("RGBA", (420, 120), (0, 0, 0, 0))
        nd = ImageDraw.Draw(note)
        nd.text((10, 30), p["catatan"], font=tx, fill=(200, 40, 60, 255))
        hx = 22 + nd.textlength(p["catatan"], font=tx)
        nd.ellipse((hx, 44, hx + 18, 62), fill=(200, 40, 60, 255)); nd.ellipse((hx + 14, 44, hx + 32, 62), fill=(200, 40, 60, 255))
        nd.polygon([(hx + 1, 56), (hx + 31, 56), (hx + 16, 76)], fill=(200, 40, 60, 255))
        note = note.rotate(-8, expand=True)
        page.alpha_composite(note, (int(min(pw - note.width, max(0, bx[2] - 300))), int(max(0, bx[1] - 110))))
    # foto: halaman sedikit miring di atas meja kayu, diperbesar ke area stabilo
    page = page.rotate(-3, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    table = Image.new("RGB", (page.width + 400, page.height + 400), "#6B4A33")
    arr = np.asarray(table).astype(np.float32)
    rng = np.random.default_rng(i)
    grainw = render.fbm2d(table.height, table.width, rng, ((40, 1.0), (3, 0.5)))
    arr *= (0.85 + 0.3 * grainw)[..., None]
    table = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    sh = Image.new("RGBA", page.size, (0, 0, 0, 0))
    sh.putalpha(page.getchannel("A").filter(ImageFilter.GaussianBlur(30)).point(lambda a: int(a * 0.6)))
    table.alpha_composite(sh, (220, 230))
    table.alpha_composite(page, (200, 200))
    if hl_boxes:  # pusat area stabilo (koordinat halaman sebelum diputar, cukup dekat untuk -3 derajat)
        bx0 = min(b[0] for b in hl_boxes); bx1 = max(b[2] for b in hl_boxes)
        by0 = min(b[1] for b in hl_boxes); by1 = max(b[3] for b in hl_boxes)
        cx, cy = 200 + (bx0 + bx1) / 2 + (page.width - pw) / 2, 200 + (by0 + by1) / 2 + (page.height - ph) / 2
    else:
        cx, cy = 200 + page.width / 2, 200 + page.height / 2
    k = 1.22
    cw, chh = W * k, H * k
    cx = min(max(cx, cw / 2 + 120), table.width - cw / 2 - 120)
    cy = min(max(cy, chh / 2 + 120), table.height - chh / 2 - 120)
    box = (int(cx - cw / 2), int(cy - chh / 2), int(cx + cw / 2), int(cy + chh / 2))
    box = (max(0, box[0]), max(0, box[1]), min(table.width, box[2]), min(table.height, box[3]))
    img = cover(table.crop(box).convert("RGB"), W, H)
    # cahaya jendela
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    light = 1 + 0.18 * np.exp(-((xx - W * 0.2) ** 2 + (yy - H * 0.2) ** 2) / (2 * 500.0 ** 2)) - 0.12 * (yy / H)
    img = Image.fromarray(np.clip(np.asarray(img).astype(np.float32) * light[..., None], 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((W - 40, H - 50), "@" + HANDLE, font=hn(22, 1), fill=(255, 255, 255), anchor="rs", stroke_width=2, stroke_fill=(0, 0, 0))
    return grain(img, 0.08)


# ---------- RETRO ----------

def retro_image(p, i):
    rng = np.random.default_rng(80 + i)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    palettes = [[(20, 60, 160), (40, 200, 190), (250, 220, 90), (10, 20, 60)], [(120, 30, 90), (250, 120, 60), (250, 220, 150), (30, 10, 40)],
                [(20, 90, 60), (160, 220, 90), (250, 240, 200), (5, 30, 20)], [(60, 30, 140), (240, 90, 160), (120, 200, 250), (15, 10, 40)]]
    cols = palettes[i % len(palettes)]
    img = np.zeros((H, W, 3), np.float32) + np.array(cols[3])
    for k, c in enumerate(cols[:3]):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(380, 650)
        wgt = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r ** 2))
        img = img * (1 - wgt[..., None]) + np.array(c) * wgt[..., None]
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    img = grain(img, 0.6).convert("RGBA")
    d = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)

    def pill(text, y):
        f = hn(26, 1)
        tw = d.textlength(text.upper(), font=f)
        d.rounded_rectangle((W / 2 - tw / 2 - 30, y, W / 2 + tw / 2 + 30, y + 54), radius=27, outline=white, width=3)
        d.text((W / 2, y + 27), text.upper(), font=f, fill=white, anchor="mm")
    pill(p["atas"], 140)
    dd = ImageFont.truetype(SUP + "Didot.ttc", 150, index=2)
    for size in range(170, 80, -6):
        dd = ImageFont.truetype(SUP + "Didot.ttc", size, index=2)
        lines = wrap(d, p["judul"].upper(), dd, W - 140)
        if len(lines) * size * 0.95 < 640:
            break
    y = H / 2 - len(lines) * size * 0.95 / 2
    for ln in lines:
        d.text((W / 2, y), ln, font=dd, fill=white, anchor="ma")
        y += size * 0.95
    d.polygon([(W / 2, 262), (W / 2 + 10, 290), (W / 2 + 38, 300), (W / 2 + 10, 310), (W / 2, 338), (W / 2 - 10, 310), (W / 2 - 38, 300), (W / 2 - 10, 290)], fill=white)
    pill(p["bawah"], H - 230)
    d.text((W / 2, H - 110), f"{p['ref']}   ·   @{HANDLE}", font=hn(24, 10), fill=white, anchor="ma")
    return img


# ---------- POSTER ----------

def poster_image(p, i):
    ph = foto_warna(p["foto"], seed=120 + i)
    ph = Image.blend(ph, Image.new("RGB", ph.size, "#000000"), 0.2).convert("RGBA")
    d = ImageDraw.Draw(ph)
    white = (255, 255, 255, 255)
    cond = lambda s: hn(s, 9)
    for size in range(230, 90, -6):
        if max(d.textlength(p["baris1"], font=cond(size)), d.textlength(p["baris2"], font=cond(size))) < W - 120:
            break
    y = 250
    d.text((W / 2, y), p["baris1"], font=cond(size), fill=white, anchor="ma")
    y += size * 0.95
    d.text((W / 2, y), p["miring"], font=georgia(int(size * 0.8), True), fill=white, anchor="ma")
    y += size * 0.85
    d.text((W / 2, y), p["baris2"], font=cond(size), fill=white, anchor="ma")
    y += size * 1.15
    f = hn(28, 10)
    pill = f"“{p['ayat_kecil']}” — {p['ref']}"
    lines = wrap(d, pill, f, 760)
    bh = len(lines) * 38 + 30
    d.rounded_rectangle((W / 2 - 420, y, W / 2 + 420, y + bh), radius=14, fill=(250, 222, 90, 235))
    yy = y + 15
    for ln in lines:
        d.text((W / 2, yy), ln, font=f, fill="#1A1A1A", anchor="ma")
        yy += 38
    d.text((W / 2, H - 80), "@" + HANDLE, font=hn(24, 1), fill=white, anchor="ma")
    return ph


# ---------- MINIMAL ----------

def minimal_image(p, i):
    img = Image.new("RGB", (W, H), "#0B0B0B")
    d = ImageDraw.Draw(img)
    f = hn(34, 0)
    lines = wrap(d, p["teks"], f, 700)
    y = H / 2 - len(lines) * 50 / 2
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill="#E9E9E9", anchor="ma")
        y += 50
    d.text((W / 2, H - 70), HANDLE, font=hn(20, 0), fill="#5A5A5A", anchor="ma")
    return grain(img, 0.05)


# ---------- LED ----------

def led_image(p, i):
    pitch, r = 13, 4.6
    cols, rows = W // pitch, H // pitch
    lines = p["teks"].split("\n")
    S = 6
    big = Image.new("L", (cols * S, rows * S), 0)
    gd = ImageDraw.Draw(big)
    fsize = 20 * S
    f = hn(fsize, 1)
    while fsize > 9 * S and max(gd.textlength(ln, font=f) for ln in lines) > (cols - 8) * S:
        fsize -= S
        f = hn(fsize, 1)
    lh = fsize * 1.22
    y = big.height / 2 - len(lines) * lh / 2
    for ln in lines:
        gd.text((big.width / 2, y), ln, font=f, fill=255, anchor="ma")
        y += lh
    grid = big.resize((cols, rows), Image.BOX)
    lit = np.asarray(grid) > 90
    img = Image.new("RGB", (W, H), "#070707")
    glow = Image.new("RGB", (W, H), "#000000")
    d, g = ImageDraw.Draw(img), ImageDraw.Draw(glow)
    amber = (255, 176, 60)
    for yy in range(rows):
        for xx in range(cols):
            cx, cy = xx * pitch + pitch / 2 + (W - cols * pitch) / 2, yy * pitch + pitch / 2 + (H - rows * pitch) / 2
            if lit[yy, xx]:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=amber)
                g.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=amber)
            else:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(28, 26, 24))
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(10)), 0.0)
    img = Image.fromarray(np.clip(np.asarray(img).astype(np.int32) + np.asarray(glow.filter(ImageFilter.GaussianBlur(12))).astype(np.int32) // 2, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    if p.get("ref"):
        d.rounded_rectangle((W / 2 - 170, H - 170, W / 2 + 170, H - 110), radius=30, fill="#070707")
        d.text((W / 2, H - 140), p["ref"].upper(), font=hn(28, 1), fill=amber, anchor="mm")
    d.rounded_rectangle((W / 2 - 170, H - 90, W / 2 + 170, H - 50), radius=20, fill="#070707")
    d.text((W / 2, H - 70), "@" + HANDLE, font=hn(22, 0), fill="#8A8A8A", anchor="mm")
    return img


# ---------- DOA ----------

def doa_image(p, i):
    img = grain(Image.new("RGB", (W, H), "#F2ECE2"), 0.07)
    d = ImageDraw.Draw(img)
    for size in range(110, 50, -4):
        lines = wrap(d, p["judul"].upper(), hn(size, 9), W - 120)
        if len(lines) <= 2:
            break
    y = 120
    for ln in lines:
        d.text((60, y), ln, font=hn(size, 9), fill="#1B1B1B")
        y += size * 0.98
    y += 40
    fonts = {"n": hn(48, 0), "b": hn(48, 1), "i": hn(48, 2), "h": hn(48, 10)}
    colors = {"n": "#2A2A2A", "b": "#2A2A2A", "i": "#2A2A2A", "h": "#C8322A"}
    wl, space, wlen = gaya_w5.layout(gaya_w5.parse(p["isi"]), fonts, W - 140)
    gaya_w5.draw_rich(img, wl, fonts, colors, 60, y, 68, space, wlen, hl=None)
    d.text((W - 60, H - 90), HANDLE.replace(".", " "), font=ImageFont.truetype(SUP + "SnellRoundhand.ttc", 52), fill="#6E6257", anchor="rs")
    return img


# ---------- semua ----------

def tambah_musik(rel):
    import musik
    if "audio" not in subprocess_streams(OUT / rel):
        wav, _ = musik.lagu_unik(rel, musik.durasi(OUT / rel) + 1, set())
        musik.pasang(rel, str(wav))


def subprocess_streams(path):
    import subprocess
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
                          capture_output=True, text=True).stdout


def render_week(mod=MOD):
    import importlib
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    simple = {"LAYAR": layar_image, "ALKITAB": alkitab_image, "RETRO": retro_image, "POSTER": poster_image,
              "MINIMAL": minimal_image, "LED": led_image, "DOA": doa_image, "HITUNG": gaya_w5.hitung_image}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt in simple:
                p = getattr(t, fmt)[idx]
                out[(hari, slot)] = ([save(simple[fmt](p, idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt == "A":
                files, cap = render.render_tenang_quote_editorial(t.POSTS[idx], f"{mod}/editorial{idx + 1}")
                out[(hari, slot)] = (files, cap)
            elif fmt == "C":
                files, cap = render.render_tenang_warna(t.WARNA[idx], f"{mod}/warna{idx + 1}")
                out[(hari, slot)] = (files, cap)
            elif fmt in ("D", "R"):
                name = "dinding" if fmt == "D" else "suasana"
                reel = f"reels/{mod}/{name}{idx + 1}.mp4"
                pool = t.DINDING if fmt == "D" else t.SUASANA
                if (OUT / reel).exists():
                    out[(hari, slot)] = ([reel], pool[idx]["caption"])
            elif fmt == "ELI":
                import tenang_eli
                out[(hari, slot)] = tenang_eli.render_item(t.ELI[idx])
    return out


def render_reels(mod=MOD):
    import importlib
    import reels
    t = importlib.import_module(f"konten.{mod}")
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "D":
                rel = reels.dinding_reel(idx, modul=mod)
            elif fmt == "R":
                rel = reels.suasana_reel(idx, modul=mod)
            else:
                continue
            tambah_musik(rel)
            print(rel)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
