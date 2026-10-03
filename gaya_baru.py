"""Akun Tenang - gaya baru minggu 3 (konten/tenang_w3.py):
  BUKU  = halaman buku terbuka di atas kain krem, judul serif + puisi pendek + tanda tangan
  MEME  = foto hitam-putih + teks putih tebal bergaris hitam
  SKRIP = panggung ibadah hitam-putih + tulisan tangan kuning ("— Tuhan"); bisa jadi Reels
  KISAH = poster editorial kisah Alkitab: langit berbintik + judul serif besar, lalu slide penjelasan

  python3 gaya_baru.py          # render semua gambar + Reels SKRIP malam
"""
import math
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import config
import keren
import render
from render import OUT, W, H, fbm2d, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w3"
SUP = "/System/Library/Fonts/Supplemental/"


def F(name, size, index=0):
    return ImageFont.truetype(SUP + name if "/" not in name else name, size, index=index)


DIDOT = lambda s: F("Didot.ttc", s, 0)
DIDOT_B = lambda s: F("Didot.ttc", s, 2)
BASK = lambda s: F("Baskerville.ttc", s, 0)
BASK_I = lambda s: F("Baskerville.ttc", s, 1)
SNELL = lambda s: F("SnellRoundhand.ttc", s, 0)
BRADLEY = lambda s: F("Bradley Hand Bold.ttf", s)
IMPACT = lambda s: F("Impact.ttf", s)
AVENIR_B = lambda s: F("/System/Library/Fonts/Avenir Next.ttc", s, 2)


# ---------- BUKU ----------

def kain(w, h, seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    folds = sum(np.sin((xx * math.cos(a) + yy * math.sin(a)) / l + rng.uniform(0, 6)) * amp
                for a, l, amp in ((0.5, 90, 10), (0.9, 140, 8), (0.2, 60, 4)))
    base = np.array([196, 174, 146], np.float32) + folds[..., None]
    light = 1 + 0.25 * np.clip((xx / w + (1 - yy / h)) - 0.8, -0.5, 0.6)
    return Image.fromarray(np.clip(base * light[..., None], 0, 255).astype(np.uint8))


def buku_image(p, seed=1):
    big = kain(W + 200, H + 200, seed).convert("RGBA")
    page = Image.new("RGBA", (1500, 1150), (0, 0, 0, 0))
    d = ImageDraw.Draw(page)
    # dua halaman: lengkung di tengah (gutter) + tumpukan kertas di tepi
    for i in range(10, 0, -1):
        d.rounded_rectangle((20 - i * 2, 40 + i * 3, 1480 + i * 2, 1110 + i * 3), radius=14, fill=(215, 200, 176, 255))
    d.rounded_rectangle((20, 30, 1480, 1100), radius=14, fill=(246, 238, 222, 255))
    arr = np.asarray(page).astype(np.float32)
    xx = np.arange(1500, dtype=np.float32)
    gutter = 1 - 0.28 * np.exp(-((xx - 750) / 40) ** 2) - 0.06 * np.exp(-((xx - 750) / 220) ** 2)
    arr[..., :3] *= gutter[None, :, None]
    page = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(page)
    ink = (52, 42, 34, 255)
    cx = 1110
    d.text((cx, 330), p["judul"], font=DIDOT_B(58), fill=ink, anchor="ma")
    y = 440
    for ln in p["baris"]:
        for part in wrap(d, ln, BASK(34), 560):
            d.text((cx, y), part, font=BASK(34), fill=ink, anchor="ma")
            y += 48
    d.text((cx, y + 70), HANDLE.replace(".", " "), font=SNELL(54), fill=(70, 58, 48, 255), anchor="ma")
    page = page.rotate(-5, expand=True, resample=Image.BICUBIC)
    shadow = Image.new("RGBA", page.size, (0, 0, 0, 0))
    shadow.putalpha(page.getchannel("A").point(lambda v: int(v * 0.7)).filter(ImageFilter.GaussianBlur(30)))
    big.alpha_composite(shadow, (-260 + 30, 120 + 40))
    big.alpha_composite(page, (-260, 120))
    # bayangan daun/jendela di atas buku
    yy, xx = np.mgrid[0:big.height, 0:big.width].astype(np.float32)
    leaf = (np.sin(xx / 70 + yy / 40) + np.sin(xx / 33 - yy / 55)) > 1.1
    band = (xx * 0.6 + yy) % 700 < 260
    sh = (leaf | band).astype(np.float32)
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))) / 255.0
    rgb = np.asarray(big.convert("RGB")).astype(np.float32) * (1 - 0.18 * sh[..., None])
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).crop((100, 100, 100 + W, 100 + H))
    return grain(img, 0.12)


# ---------- MEME ----------

def outlined(d, xy, text, font, fill="#FFFFFF", stroke=6):
    d.text(xy, text, font=font, fill=fill, stroke_width=stroke, stroke_fill="#000000")


def panggung(w, h, seed=2):
    """Panggung ibadah gelap dengan sorot lampu (hitam-putih)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    img = np.full((h, w), 14, np.float32)
    for i in range(6):
        sx = w * (0.15 + i * 0.14) + rng.uniform(-20, 20)
        ang = (sx - w / 2) / w * 0.5
        dist = np.abs((xx - sx) - (yy - h * 0.12) * ang) / (6 + (yy - h * 0.12).clip(0) * 0.09)
        beam = np.exp(-dist ** 2) * np.clip((yy - h * 0.12) / (h * 0.5), 0, 1) * np.exp(-(yy - h * 0.12).clip(0) / (h * 0.9))
        img += beam * 90
        img += np.exp(-((xx - sx) ** 2 + (yy - h * 0.12) ** 2) / 120) * 240
    stage = yy > h * 0.7
    img[stage] = 26 + (yy[stage] - h * 0.7) * 0.02
    img += np.exp(-((xx - w / 2) ** 2 / (w * 0.4) ** 2 + (yy - h * 0.62) ** 2 / (h * 0.12) ** 2)) * 70
    crowd = yy > h * 0.84 + np.abs(np.sin(xx / 46)) * -38 + np.sin(xx / 13) * 5
    img[crowd] = 6
    img = img + (fbm2d(h, w, rng) - 0.5) * 18
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGB")


def meme_image(p, i):
    base = panggung(W, H, i) if p["foto"] == "panggung" else keren.foto(p["foto"], seed=50 + i)
    img = grain(base.convert("L").convert("RGB"), 0.4)
    d = ImageDraw.Draw(img)
    for size in range(84, 50, -4):
        f = AVENIR_B(size)
        lines = wrap(d, p["teks"], f, W - 220)
        if len(lines) * size * 1.12 < H * 0.42:
            break
    y = H * 0.16
    for ln in lines:
        outlined(d, (110, y), ln, f, stroke=max(4, size // 14))
        y += size * 1.12
    d.text((W / 2, H - 90), "@" + HANDLE, font=AVENIR_B(24), fill="#FFFFFF", anchor="ma", stroke_width=2, stroke_fill="#000000")
    return img


# ---------- SKRIP ----------

def skrip_layer(p, w=W, h=H, size=128):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    words = p["teks"].split()
    while True:
        f = BRADLEY(size)
        lines, cur = [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=f) > w * 0.56 and cur:
                lines.append(cur)
                cur = wd
            else:
                cur = t
        lines.append(cur)
        widest = max(d.textlength(ln, font=f) + k * 40 for k, ln in enumerate(lines))
        if widest <= w * 0.66 or size <= 70:
            break
        size -= 8
    y = h * 0.5 - (len(lines) + 0.8) * size * 1.05 / 2
    x0 = (w - widest) / 2
    for k, ln in enumerate(lines):
        d.text((x0 + k * 40, y), ln, font=f, fill=(245, 205, 40, 255))
        y += size * 1.05
    d.text((x0 + widest, y + 10), p["dari"], font=BRADLEY(int(size * 0.62)), fill=(245, 205, 40, 255), anchor="ra")
    return lay.rotate(10, resample=Image.BICUBIC, center=(w / 2, h / 2))


def skrip_image(p, i):
    img = grain(panggung(W, H, 10 + i), 0.35).convert("RGBA")
    img.alpha_composite(skrip_layer(p))
    ImageDraw.Draw(img).text((W / 2, H - 70), "@" + HANDLE, font=AVENIR_B(22), fill=(220, 220, 220, 255), anchor="ma")
    return img


def skrip_reel(p, i, seconds=9):
    """Panggung bergerak pelan (lampu berkedip), tulisan kuning muncul seperti ditulis tangan (sapuan dari kiri)."""
    import cerita
    import musik
    rel = f"reels/{MOD}/skrip{i + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rw, rh = 1080, 1920
    bg = [grain(panggung(rw, rh, 10 + i + k), 0.35) for k in range(2)]
    text = skrip_layer(p, rw, rh, 150)
    handle = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    ImageDraw.Draw(handle).text((rw / 2, rh - 260), "@" + HANDLE, font=AVENIR_B(30), fill=(220, 220, 220, 255), anchor="ma")
    ff = cerita.ffmpeg_writer(out, rw, rh, 30)
    for n in range(30 * seconds):
        t = n / 30
        k = 0.5 + 0.5 * math.sin(t * 1.3)
        frame = Image.blend(bg[0], bg[1], k).convert("RGBA")
        reveal = min(1.0, max(0.0, (t - 0.8) / 2.2))
        mask = Image.new("L", (rw, rh), 0)
        ImageDraw.Draw(mask).rectangle((0, 0, int(rw * reveal * 1.1), rh), fill=255)
        tl = text.copy()
        tl.putalpha(ImageChops.multiply(text.getchannel("A"), mask.filter(ImageFilter.GaussianBlur(30))))
        frame.alpha_composite(tl)
        frame.alpha_composite(handle)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(rel)
    wav, _ = musik.lagu_unik(rel, seconds + 1, set())
    musik.pasang(rel, str(wav))
    return rel


# ---------- KISAH ----------

def langit(w, h, seed):
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, h)[:, None, None]
    sky = np.array([70, 128, 196]) * (1 - yy) + np.array([150, 190, 228]) * yy
    img = np.broadcast_to(sky, (h, w, 3)).astype(np.float32).copy()
    c = fbm2d(h, w, rng, ((3, 1.0), (8, 0.6), (20, 0.3), (60, 0.15)))
    m = np.clip((c - 0.5) * 3.2, 0, 1)
    img = img * (1 - m[..., None]) + np.array([248, 248, 250]) * m[..., None]
    return grain(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)), 0.5)


def kisah_cover(p, seed):
    img = langit(W, H, seed).convert("RGBA")
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    white = (255, 255, 255, 255)
    for size in range(300, 120, -10):
        if max(d.textlength(p["judul1"], font=DIDOT_B(size)), d.textlength(p["judul2"], font=DIDOT_B(size))) < W - 160:
            break
    d.text((W / 2, 300), p["judul1"], font=DIDOT_B(size), fill=white, anchor="ma")
    d.text((W / 2, 300 + size * 1.22), p["judul2"], font=DIDOT_B(size), fill=white, anchor="ma")
    d.text((W / 2, 300 + size * 1.1), p["ref"].upper(), font=AVENIR_B(40), fill=(30, 60, 110, 255), anchor="mm")
    d.text((W / 2, 300 + size * 2.42), p["sub"], font=AVENIR_B(54), fill=white, anchor="ma")
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(lay.getchannel("A").filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.35)))
    img.alpha_composite(sh)
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    d.text((W / 2, H - 120), "geser  ›", font=BASK_I(40), fill=white, anchor="ma")
    d.text((W / 2, H - 70), "@" + HANDLE, font=AVENIR_B(24), fill=white, anchor="ma")
    return img


def kisah_slide(p, n, total, heading, body, seed, akhir=False):
    img = langit(W, H, seed + n).convert("RGBA")
    probe = ImageDraw.Draw(img)
    f_h = DIDOT_B(64) if not akhir else BASK_I(52)
    f_b = BASK(42) if not akhir else AVENIR_B(30)
    hl = wrap(probe, heading, f_h, W - 280)
    bl = wrap(probe, body, f_b, W - 280)
    content = 70 + len(hl) * f_h.size * 1.18 + 40 + len(bl) * f_b.size * 1.45 + 90
    top = (H - content) / 2
    veil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(veil).rounded_rectangle((80, top - 50, W - 80, top + content + 30), radius=28, fill=(255, 255, 255, 232))
    img.alpha_composite(veil)
    d = ImageDraw.Draw(img)
    ink = (28, 40, 64)
    d.text((W / 2, top), f"{p['judul1']} {p['judul2']}".upper(), font=AVENIR_B(26), fill=(70, 110, 170), anchor="ma")
    y = top + 70
    for ln in hl:
        d.text((W / 2, y), ln, font=f_h, fill=ink, anchor="ma")
        y += f_h.size * 1.18
    y += 40
    for ln in bl:
        d.text((W / 2, y), ln, font=f_b, fill=ink if not akhir else (70, 110, 170), anchor="ma")
        y += f_b.size * 1.45
    d.text((W / 2, y + 40), f"{n}/{total}   ·   @{HANDLE}", font=AVENIR_B(22), fill=(110, 130, 160), anchor="ma")
    return img


def kisah_carousel(p, i):
    seed = 300 + i * 10
    slides = [kisah_cover(p, seed)]
    total = len(p["slides"]) + 2
    for n, (hd, bd) in enumerate(p["slides"], 2):
        slides.append(kisah_slide(p, n, total, hd, bd, seed))
    slides.append(kisah_slide(p, total, total, p["ayat"], p["ayat_ref"].upper(), seed, akhir=True))
    return [save(s, f"{MOD}/kisah{i + 1}_{n}.jpg") for n, s in enumerate(slides, 1)]


# ---------- semua ----------

def render_w3():
    """{(hari, slot): (files, caption)} untuk konten/tenang_w3.py."""
    from konten import tenang_w3 as t
    for old in (OUT / MOD).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "BUKU":
                p = t.BUKU[idx]
                out[(hari, slot)] = ([save(buku_image(p, idx), f"{MOD}/buku{idx + 1}.jpg")], p["caption"])
            elif fmt == "MEME":
                p = t.MEME[idx]
                out[(hari, slot)] = ([save(meme_image(p, idx), f"{MOD}/meme{idx + 1}.jpg")], p["caption"])
            elif fmt == "SKRIP":
                p = t.SKRIP[idx]
                reel = f"reels/{MOD}/skrip{idx + 1}.mp4"
                files = [reel] if slot == "malam0" and (OUT / reel).exists() else [save(skrip_image(p, idx), f"{MOD}/skrip{idx + 1}.jpg")]
                out[(hari, slot)] = (files, p["caption"])
            elif fmt == "KISAH":
                p = t.KISAH[idx]
                out[(hari, slot)] = (kisah_carousel(p, idx), p["caption"])
            elif fmt == "T":
                p = t.RELATABLE[idx]
                out[(hari, slot)] = (keren.relatable(p, idx, MOD), p["caption"])
            elif fmt == "K":
                reel = f"reels/{MOD}/kinetik{idx + 1}.mp4"
                if (OUT / reel).exists():
                    out[(hari, slot)] = ([reel], t.KINETIK[idx]["caption"])
    return out


if __name__ == "__main__":
    from konten import tenang_w3 as t
    what = sys.argv[1] if len(sys.argv) > 1 else "semua"
    if what in ("semua", "reels"):
        for hari, slots in t.JADWAL.items():
            for slot, (fmt, idx) in slots.items():
                if fmt == "SKRIP" and slot == "malam0":
                    print(skrip_reel(t.SKRIP[idx], idx))
        for i in range(len(t.KINETIK)):
            print(keren.kinetik_reel(i, MOD))
    print(len(render_w3()), "post")
