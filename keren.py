"""Akun Tenang - format baru (konten/tenang_keren.py): photo dump, dulu vs sekarang, tipografi sinematik,
animasi karakter. Semua gambar/foto dibuat sendiri (tanpa foto stok).

  python3 keren.py            # semua: carousel + Reels
  python3 keren.py foto       # hanya carousel photo dump & dulu vs sekarang
  python3 keren.py kinetik 1  # Reels tipografi nomor 1
  python3 keren.py jalan 1 2  # Reels animasi karakter nomor 1 dan 2
"""
import importlib
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

import cerita
import config
import render
from konten import tenang_keren as tk
from render import OUT, W, H, fbm1d, fbm2d, font, save, wrap

RW, RH, FPS = 1080, 1920, 30
HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_keren"


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def text_layer(size, draws, shadow=8, shadow_alpha=1.0):
    """draws(d) menggambar teks putih/krem; hasilnya diberi bayangan lembut supaya terbaca di latar apa pun."""
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    draws(ImageDraw.Draw(lay))
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    a = lay.getchannel("A").filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.4 * shadow_alpha)))
    out.putalpha(a)
    out.alpha_composite(lay)
    return out


def with_alpha(img, alpha):
    if alpha >= 1:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    return img


# ---------- foto hitam-putih buatan sendiri ----------

def _sky(h, w, top, bot, power=1.0):
    y = (np.linspace(0, 1, h) ** power)[:, None, None]
    return np.broadcast_to(np.array(top) * (1 - y) + np.array(bot) * y, (h, w, 3)).astype(np.float32).copy()


def foto(kind, w=W, h=H, seed=3):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if kind == "laut":
        img = np.asarray(render.landscape("laut", w, h, seed)).astype(np.float32)
    elif kind == "gunung":
        img = np.asarray(render.landscape("fajar", w, h, seed)).astype(np.float32)
    elif kind == "kabut":
        img = np.asarray(render.suasana_scene("kabut", w, h, seed)(3.0)).astype(np.float32)
    elif kind == "bintang":
        img = np.asarray(render.suasana_scene("bintang", w, h, seed)(3.0)).astype(np.float32)
    elif kind == "awan":
        img = _sky(h, w, (70, 90, 120), (210, 214, 220))
        c = fbm2d(h, w, rng, ((3, 1.0), (7, 0.6), (18, 0.3), (50, 0.12)))
        m = np.clip((c - 0.42) * 2.6, 0, 1)
        img = img * (1 - m[..., None]) + np.array([240, 240, 240]) * m[..., None] * (0.75 + 0.35 * (1 - yy / h))[..., None]
        sx, sy = w * 0.7, h * 0.18
        ang = np.arctan2(yy - sy, xx - sx)
        rays = (np.sin(ang * 18) * 0.5 + 0.5) ** 6 * np.exp(-np.hypot(xx - sx, yy - sy) / (h * 0.6))
        img += (rays * 70 + np.exp(-np.hypot(xx - sx, yy - sy) ** 2 / (2 * 120 ** 2)) * 160)[..., None]
    elif kind == "jendela":
        img = np.full((h, w, 3), 34, np.float32) + fbm2d(h, w, rng)[..., None] * 18
        x0, x1, y0, y1 = w * 0.22, w * 0.78, h * 0.12, h * 0.62
        win = (xx > x0) & (xx < x1) & (yy > y0) & (yy < y1)
        img[win] = 200 + (1 - (yy[win] - y0) / (y1 - y0))[..., None] * 40
        frame = win & ((np.abs(xx - w / 2) < 9) | (np.abs(yy - (y0 + y1) / 2) < 9))
        img[frame] = 30
        for _ in range(140):  # tetes hujan di kaca
            cx, cy, r = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(3, 9)
            sel = (xx - cx) ** 2 + (yy - cy) ** 2 < r * r
            img[sel] = img[sel] * 0.75
        # cahaya jatuh ke lantai
        floor = (yy > h * 0.72) & (np.abs(xx - w / 2 - (yy - h * 0.72) * 0.5) < (w * 0.28 + (yy - h * 0.72) * 0.25))
        img[floor] += 35
        img = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)
    elif kind == "lilin":
        img = np.full((h, w, 3), 10, np.float32)
        cx, top_y = w / 2, h * 0.55
        glow = np.exp(-((xx - cx) ** 2 + (yy - (top_y - 60)) ** 2) / (2 * 260.0 ** 2))
        img += glow[..., None] * 120
        body = (np.abs(xx - cx) < 70) & (yy > top_y) & (yy < h * 0.95)
        img[body] = (200 - (yy[body] - top_y) * 0.2 - np.abs(xx[body] - cx) * 0.9)[..., None]
        flame = ((xx - cx) / 22) ** 2 + ((yy - (top_y - 70)) / 60) ** 2 < 1
        img[flame] = 255
        wick = (np.abs(xx - cx) < 3) & (yy > top_y - 16) & (yy < top_y)
        img[wick] = 20
    elif kind == "jalan":
        hz = h * 0.5
        img = _sky(h, w, (90, 100, 115), (215, 215, 212))
        c = fbm2d(h, w, rng, ((4, 1.0), (10, 0.5), (30, 0.2)))
        img += (np.clip(c - 0.5, 0, 1) * 120 * (yy < hz))[..., None]
        ground = yy > hz
        grass = fbm2d(h, w, rng, ((20, 1.0), (60, 0.5), (160, 0.3)))
        img[ground] = (60 + grass[ground] * 60 + (yy[ground] - hz) * 0.02)[..., None]
        road = ground & (np.abs(xx - w / 2) < (yy - hz) * 0.5 + 2)
        img[road] = (130 + (yy[road] - hz) * 0.08)[..., None]
        dash = road & (np.abs(xx - w / 2) < (yy - hz) * 0.03 + 1) & (np.sin((np.log(np.maximum(yy - hz, 1))) * 9) > 0.3)
        img[dash] = 225
    elif kind == "pohon":
        img = _sky(h, w, (120, 128, 140), (225, 222, 215))
        ridge = h * 0.78 - np.exp(-((np.arange(w) - w * 0.55) / (w * 0.35)) ** 2) * 120 + fbm1d(w, rng) * 8
        img[yy > ridge[None, :]] = 40
        tree = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(tree)

        def branch(x, y, ang, ln, wd, depth):
            x2, y2 = x + math.sin(ang) * ln, y - math.cos(ang) * ln
            d.line([(x, y), (x2, y2)], fill=255, width=max(1, int(wd)))
            if depth == 0:
                d.ellipse([x2 - 26, y2 - 20, x2 + 26, y2 + 20], fill=255)
                return
            for k in (-1, 1):
                branch(x2, y2, ang + k * rng.uniform(0.3, 0.6), ln * rng.uniform(0.66, 0.8), wd * 0.68, depth - 1)
        tx = int(w * 0.55)
        branch(tx, ridge[tx] + 10, 0, 230, 34, 7)
        m = np.asarray(tree.filter(ImageFilter.GaussianBlur(1))).astype(np.float32) / 255
        img = img * (1 - m[..., None]) + 30 * m[..., None]
    else:
        raise ValueError(kind)
    g = img.mean(axis=2)
    g = np.clip((g - 128) * 1.15 + 128, 0, 255)  # sedikit lebih kontras
    vign = 1 - 0.45 * (((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h / 2) / (h * 0.75)) ** 2)
    g = np.clip(g * vign, 0, 255).astype(np.uint8)
    return render.grain(Image.fromarray(g).convert("RGB"), 0.55)


def dump_slide(kind, text, n, total, seed):
    img = foto(kind, seed=seed).convert("RGBA")
    size = 52 if n == 1 else 44
    f = font("serif_italic", size)

    def draw(d):
        lines = wrap(d, text, f, 820)
        y = H * 0.5 - len(lines) * size * 1.3 / 2
        for ln in lines:
            d.text((W / 2, y), ln, font=f, fill=(255, 255, 255, 255), anchor="ma")
            y += size * 1.3
        d.text((W / 2, H - 90), f"{n}/{total}   ·   @{HANDLE}", font=font("sans", 22), fill=(255, 255, 255, 190), anchor="ma")
    img.alpha_composite(text_layer(img.size, draw, 10))
    return img


def render_dump(i, m=tk, mod=MOD):
    p = m.DUMP[i]
    files = [save(dump_slide(kind, text, n, len(p["slides"]), seed=i * 10 + n), f"{mod}/dump{i + 1}_{n}.jpg")
             for n, (kind, text) in enumerate(p["slides"], 1)]
    return files, p["caption"]


# ---------- dulu vs sekarang ----------
GELAP, KREM, EMAS, ABU = "#161616", "#EFE8DC", "#C9A84C", "#8A857C"


def dulu_slide(kiri, kanan, n, total):
    img = Image.new("RGB", (W, H), GELAP)
    d = ImageDraw.Draw(img)
    d.rectangle([W // 2, 0, W, H], fill=KREM)
    img = render.grain(img, 0.12)
    d = ImageDraw.Draw(img)
    lab, sub = font("sans_bold", 24), font("serif_italic", 30)
    d.text((W * 0.25, 150), "D U L U", font=lab, fill=ABU, anchor="ma")
    d.text((W * 0.75, 150), "S E K A R A N G", font=lab, fill="#6B5B2E", anchor="ma")
    d.text((W * 0.25, 200), "aku pikir…", font=sub, fill=ABU, anchor="ma")
    d.text((W * 0.75, 200), "aku tahu…", font=sub, fill="#6B5B2E", anchor="ma")
    f = font("serif", 50)
    for text, cx, col, coret in ((kiri, W * 0.25, "#BDB7AC", True), (kanan, W * 0.75, "#1A1A1A", False)):
        lines = wrap(d, text, f, 420)
        y = H * 0.5 - len(lines) * 66 / 2
        for ln in lines:
            d.text((cx, y), ln, font=f, fill=col, anchor="ma")
            if coret:  # dicoret tipis
                wln = d.textlength(ln, font=f)
                d.line([(cx - wln / 2 - 6, y + 34), (cx + wln / 2 + 6, y + 30)], fill="#8A3B32", width=4)
            y += 66
    d.text((W / 2, H - 110), f"{n}/{total}", font=font("sans", 24), fill=EMAS, anchor="ma")
    d.line([(W // 2, 280), (W // 2, H - 180)], fill=EMAS, width=2)
    return img


def dulu_cover(judul, total):
    img = Image.new("RGB", (W, H), GELAP)
    d = ImageDraw.Draw(img)
    d.rectangle([W // 2, 0, W, H], fill=KREM)
    img = render.grain(img, 0.12)
    d = ImageDraw.Draw(img)
    big = font("serif", 120)
    d.text((W * 0.25, H * 0.40), "dulu", font=big, fill="#BDB7AC", anchor="mm")
    d.text((W * 0.75, H * 0.40), "kini", font=big, fill="#1A1A1A", anchor="mm")
    band = Image.new("RGBA", (W, 150), (201, 168, 76, 255))
    img.paste(band, (0, int(H * 0.52)), band)
    d.text((W / 2, H * 0.52 + 75), judul, font=font("serif_italic", 64), fill="#161616", anchor="mm")
    d.text((W * 0.25, H * 0.75), "yang dulu aku pikir", font=font("sans", 30), fill=ABU, anchor="ma")
    d.text((W * 0.75, H * 0.75), "yang sekarang aku tahu", font=font("sans", 30), fill="#6B5B2E", anchor="ma")
    d.text((W / 2, H - 110), f"geser  →   ·   1/{total}", font=font("sans", 24), fill=EMAS, anchor="ma")
    return img


def dulu_penutup(ayat, ref, n, total):
    img = render.grain(Image.new("RGB", (W, H), KREM), 0.12)
    d = ImageDraw.Draw(img)
    f = font("serif_italic", 52)
    lines = wrap(d, ayat, f, 820)
    y = H * 0.45 - len(lines) * 72 / 2
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill="#1A1A1A", anchor="ma")
        y += 72
    d.text((W / 2, y + 40), ref.upper(), font=font("sans_bold", 28), fill="#6B5B2E", anchor="ma")
    d.line([(W / 2 - 60, y + 110), (W / 2 + 60, y + 110)], fill=EMAS, width=3)
    d.text((W / 2, H - 150), "mana yang paling kamu rasakan?", font=font("serif_italic", 34), fill="#555", anchor="ma")
    d.text((W / 2, H - 100), f"@{HANDLE}   ·   {n}/{total}", font=font("sans", 24), fill=ABU, anchor="ma")
    return img


def render_dulu(i, m=tk, mod=MOD):
    p = m.DULU[i]
    total = len(p["pasangan"]) + 2
    slides = [dulu_cover(p["judul"], total)] + [dulu_slide(a, b, n, total) for n, (a, b) in enumerate(p["pasangan"], 2)] \
        + [dulu_penutup(p["ayat"], p["ref"], total, total)]
    return [save(s, f"{mod}/dulu{i + 1}_{n}.jpg") for n, s in enumerate(slides, 1)], p["caption"]


# ---------- suara latar lembut untuk Reels baru ----------

def add_pad(silent, out, seconds, root=220.0):
    """Akor lembut (sine) dengan fade in/out, supaya Reels tidak sunyi. Musik IG tetap bisa ditambah manual."""
    notes = [root, root * 1.25, root * 1.5, root * 2]
    tone = "+".join(f"{a}*sin(2*PI*{f:.2f}*t)*(0.75+0.25*sin(2*PI*{0.11 + k * 0.07:.2f}*t))"
                    for k, (f, a) in enumerate(zip(notes, (0.09, 0.06, 0.05, 0.03))))
    env = f"min(1,t/2.5)*min(1,({seconds}-t)/2)"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-f", "lavfi", "-i",
                    f"aevalsrc='({tone})*{env}':s=44100:d={seconds}", "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-maxrate", "4M",
                    "-bufsize", "8M", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", str(out)], check=True)  # dikompres: butiran film bikin file raksasa (jsDelivr maks 20 MB)
    silent.unlink()


def grains(n=6, size=(RW, RH), strength=0.25):
    return [Image.effect_noise(size, 40).point(lambda v: int(128 + (v - 128) * strength)).convert("RGB") for _ in range(n)]


def writer(rel):
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    silent = out.with_name(out.stem + "_sunyi.mp4")
    return out, silent, cerita.ffmpeg_writer(silent, RW, RH, FPS)


def finish(ff, silent, out, seconds, root, rel):
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    add_pad(silent, out, seconds, root)
    return rel


# ---------- K: tipografi sinematik ----------

def kinetik_words(frasa):
    """Tata letak satu frasa: [(sprite, x, y, i)] per kata, baris di tengah layar."""
    fn, fh = font("sans_bold", 86), font("serif_italic", 96)
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = [(w.strip("*"), w.startswith("*")) for w in frasa.split()]
    space = 26
    lines, cur, cw = [], [], 0
    for wd, hl in words:
        f = fh if hl else fn
        ww = d.textlength(wd, font=f)
        if cur and cw + space + ww > 900:
            lines.append((cur, cw))
            cur, cw = [], 0
        cur.append((wd, hl, ww))
        cw += (space if len(cur) > 1 else 0) + ww
    lines.append((cur, cw))
    lh = 118
    y0 = RH * 0.46 - len(lines) * lh / 2
    out, i = [], 0
    for li, (row, rw) in enumerate(lines):
        x = RW / 2 - rw / 2
        for wd, hl, ww in row:
            f = fh if hl else fn
            sp = text_layer((int(ww) + 40, lh + 40), lambda dd, wd=wd, f=f, hl=hl: dd.text(
                (20, 20 + lh * 0.8), wd, font=f, fill=(226, 190, 104, 255) if hl else (244, 240, 232, 255), anchor="ls"), 10)
            out.append((sp, int(x) - 20, int(y0 + li * lh) - 20, i))
            x += ww + space
            i += 1
    return out


def kinetik_bg(seed, w, h):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = np.full((h, w, 3), (12, 12, 14), np.float32)
    blob = np.exp(-(((xx - w * 0.3) / (w * 0.5)) ** 2 + ((yy - h * 0.35) / (h * 0.35)) ** 2))
    tint = [(90, 62, 40), (40, 56, 90), (70, 40, 60), (40, 70, 64), (86, 70, 40), (60, 50, 90)][seed % 6]
    base += blob[..., None] * np.array(tint) * 0.9
    base += (fbm2d(h, w, rng, ((3, 1.0), (8, 0.5))) - 0.5)[..., None] * 30
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def kinetik_reel(i, mod=MOD):
    p = importlib.import_module(f"konten.{mod}").KINETIK[i]
    rel = f"reels/{mod}/kinetik{i + 1}.mp4"
    per_word, hold, gap = 0.34, 1.3, 0.35
    phrases, t = [], 0.6
    for fr in p["frasa"]:
        words = kinetik_words(fr)
        dur = len(words) * per_word + hold
        phrases.append((t, t + dur, words))
        t += dur + gap
    end_t = t
    seconds = math.ceil(end_t + 2.6)
    ref = text_layer((RW, RH), lambda d: (
        d.text((RW / 2, RH * 0.44), p["ref"].upper(), font=font("sans_bold", 40), fill=(226, 190, 104, 255), anchor="mm"),
        d.text((RW / 2, RH * 0.50), f"@{HANDLE}", font=font("sans", 34), fill=(244, 240, 232, 220), anchor="mm")), 8)
    big = kinetik_bg(i, int(RW * 1.12), int(RH * 1.12))
    gr = grains()
    out, silent, ff = writer(rel)
    for n in range(FPS * seconds):
        t = n / FPS
        z = t / seconds  # zoom pelan: potong makin ke tengah
        cw, ch = int(big.width - (big.width - RW) * z), int(big.height - (big.height - RH) * z)
        bx, by = (big.width - cw) // 2, (big.height - ch) // 2
        frame = big.crop((bx, by, bx + cw, by + ch)).resize((RW, RH), Image.BILINEAR).convert("RGBA")
        for t0, t1, words in phrases:
            if not (t0 <= t <= t1 + gap):
                continue
            out_a = 1 - ease((t - t1) / gap)
            for sp, x, y, k in words:
                a = ease((t - t0 - k * per_word) / 0.28)
                if a <= 0:
                    continue
                frame.alpha_composite(with_alpha(sp, a * out_a), (x, y + int((1 - a) * 26)))
        if t > end_t:
            frame.alpha_composite(with_alpha(ref, ease((t - end_t) / 0.6)))
        rgb = ImageChops.add(frame.convert("RGB"), gr[n % len(gr)], scale=1, offset=-128)
        ff.stdin.write(rgb.tobytes())
    return finish(ff, silent, out, seconds, (196.0, 220.0, 174.6, 207.6, 233.1, 185.0)[i % 6], rel)


# ---------- J: animasi karakter di pemandangan lukisan ----------
CREAM, CREAM_BACK = (242, 230, 200), (206, 192, 160)
L = {"head": 62, "neck": 20, "torso": 215, "upper": 132, "fore": 120, "thigh": 158, "shin": 152, "foot": 44}
WIDTH = {"torso": 66, "limb": 40}
SS = 2  # gambar karakter 2x lalu diperkecil supaya halus


def painterly(arr, k=3, seed=0):
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    small = img.resize((img.width // k, img.height // k), Image.BILINEAR).filter(ImageFilter.ModeFilter(5))
    img = small.resize(img.size, Image.BICUBIC)
    rng = np.random.default_rng(seed)
    h, w = img.height, img.width
    stroke = np.asarray(Image.fromarray((rng.random((h // 6, w // 30)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)) / 255.0
    arr = np.asarray(img).astype(np.float32) * (0.93 + 0.14 * stroke)[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8)


def scene(kind, w, h, fw, seed):
    """(langit RGB lebar w, tanah depan RGBA lebar fw, kurva tanah, info)"""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    hz = h * 0.60
    info = {}
    if kind == "fajar":
        sky = np.asarray(render.landscape("fajar", w, h, seed)).astype(np.float32)
        fg_col, info["sun"] = (30, 34, 52), (w * 0.42, h * 0.62)
    elif kind == "laut":
        sky = np.asarray(render.landscape("laut", w, h, seed)).astype(np.float32)
        fg_col, info["sun"] = (70, 56, 50), (w * 0.42, h * 0.58)
    else:
        top, mid, hor = {"senja": ((52, 44, 88), (190, 104, 118), (250, 180, 112)),
                         "malam": ((6, 10, 28), (18, 28, 60), (44, 58, 96)),
                         "kabut": ((58, 66, 70), (120, 130, 128), (176, 182, 176))}[kind]
        t1 = np.clip(yy / (hz * 0.6), 0, 1)[..., None]
        t2 = np.clip((yy - hz * 0.6) / (hz * 0.4), 0, 1)[..., None]
        sky = (np.array(top) * (1 - t1) + np.array(mid) * t1) * (1 - t2) + np.array(hor) * t2
        c = fbm2d(h, w, rng, ((4, 1.0), (12, 0.5), (30, 0.25)))
        cm = np.clip((c - 0.55) * 2.5, 0, 0.6) * (yy < hz)
        cloud = {"senja": (250, 196, 190), "malam": (40, 50, 80), "kabut": (196, 200, 196)}[kind]
        sky = sky * (1 - cm[..., None]) + np.array(cloud) * cm[..., None]
        if kind == "senja":
            sx, sy = w * 0.62, hz + 30
            sky += np.exp(-((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * 260.0 ** 2))[..., None] * np.array([255, 190, 120]) * 0.6
            info["sun"] = (sx, sy)
        if kind == "malam":
            mx, my = w * 0.74, h * 0.3
            sky += np.exp(-((xx - mx) ** 2 + (yy - my) ** 2) / (2 * 150.0 ** 2))[..., None] * np.array([120, 130, 160]) * 0.5
            sky[(xx - mx) ** 2 + (yy - my) ** 2 < 58 ** 2] = (236, 232, 214)
            info["stars"] = (rng.uniform(0, w, 420), rng.uniform(0, hz * 0.95, 420), rng.uniform(0, 6.3, 420), rng.choice([1, 1, 2, 2, 3], 420))
        for j, (base, amp, col_t) in enumerate([(0.62, 60, 0.5), (0.67, 80, 0.25)]):  # bukit jauh
            ridge = h * base + fbm1d(w, rng, ((5, 1.0), (14, 0.4), (40, 0.15))) * amp
            dark = np.array(hor) * col_t + np.array(top) * (1 - col_t) * 0.9
            sky = np.where((yy > ridge[None, :])[..., None], dark, sky)
        fg_col = {"senja": (46, 30, 44), "malam": (10, 14, 28), "kabut": (50, 58, 56)}[kind]
    ground = h * 0.70 + fbm1d(fw, rng, ((3, 1.0), (7, 0.35))) * 26
    fgy, fgx = np.mgrid[0:h, 0:fw].astype(np.float32)
    fg = np.zeros((h, fw, 4), np.float32)
    fg[..., :3] = np.array(fg_col) * (1 - 0.25 * np.clip((fgy - h * 0.7) / (h * 0.3), 0, 1))[..., None]
    fg[..., :3] += (fbm2d(h, fw, rng, ((60, 1.0), (200, 0.5))) - 0.5)[..., None] * 14
    fg[..., 3] = np.clip((fgy - ground[None, :]) * 0.8, 0, 1) * 255
    sky_img = painterly(sky, 3, seed)
    fg_rgb = painterly(fg[..., :3], 3, seed + 1)
    fg_img = Image.fromarray(np.dstack([fg_rgb, fg[..., 3].astype(np.uint8)]), "RGBA")
    return sky_img, fg_img, ground, info


def pt(p, ln, ang):
    return (p[0] + ln * math.sin(ang), p[1] + ln * math.cos(ang))


def figure_points(q, hip=(0.0, 0.0)):
    """q: sudut (radian, 0 = lurus ke bawah, positif = ke depan/kanan). Mengembalikan titik-titik sendi."""
    sh = (hip[0] + L["torso"] * math.sin(q["tilt"]), hip[1] - L["torso"] * math.cos(q["tilt"]))
    ha = q["tilt"] + q.get("head", 0)
    head = (sh[0] + (L["neck"] + L["head"]) * math.sin(ha), sh[1] - (L["neck"] + L["head"]) * math.cos(ha))
    pts = {"hip": hip, "sh": sh, "head": head}
    for side in ("n", "f"):  # n = dekat (depan), f = jauh (belakang)
        el = pt(sh, L["upper"], q[f"ua_{side}"])
        pts[f"el_{side}"], pts[f"hand_{side}"] = el, pt(el, L["fore"], q[f"ua_{side}"] + q[f"eb_{side}"])
        kn = pt(hip, L["thigh"], q[f"th_{side}"])
        ft = pt(kn, L["shin"], q[f"th_{side}"] - q[f"kb_{side}"])
        pts[f"kn_{side}"], pts[f"ft_{side}"] = kn, ft
        pts[f"toe_{side}"] = pt(ft, L["foot"], q[f"th_{side}"] - q[f"kb_{side}"] + math.pi / 2)
    return pts


def draw_figure(frame, q, x, ground_y, extra=None):
    pts = figure_points(q)
    r = WIDTH["limb"] / 2
    low = max(p[1] for k, p in pts.items() if k != "head") + r
    dx, dy = x, ground_y - low
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    pad = 90
    bx0, by0 = int(min(xs) + dx - pad), int(min(ys) + dy - pad)
    bw, bh = int(max(xs) - min(xs) + 2 * pad), int(max(ys) - min(ys) + 2 * pad)
    lay = Image.new("RGBA", (bw * SS, bh * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    P = lambda k: ((pts[k][0] + dx - bx0) * SS, (pts[k][1] + dy - by0) * SS)

    def limb(a, b, col, wd):
        d.line([P(a), P(b)], fill=col, width=int(wd * SS))
        for k in (a, b):
            cx, cy = P(k)
            rr = wd * SS / 2
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    for side, col in (("f", CREAM_BACK),):
        limb("sh", f"el_{side}", col, WIDTH["limb"]); limb(f"el_{side}", f"hand_{side}", col, WIDTH["limb"] * 0.9)
        limb("hip", f"kn_{side}", col, WIDTH["limb"] * 1.1); limb(f"kn_{side}", f"ft_{side}", col, WIDTH["limb"]); limb(f"ft_{side}", f"toe_{side}", col, WIDTH["limb"] * 0.8)
    limb("hip", "sh", CREAM, WIDTH["torso"])
    hx, hy = P("head")
    hr = L["head"] * SS
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=CREAM)
    limb("hip", "kn_n", CREAM, WIDTH["limb"] * 1.1); limb("kn_n", "ft_n", CREAM, WIDTH["limb"]); limb("ft_n", "toe_n", CREAM, WIDTH["limb"] * 0.8)
    limb("sh", "el_n", CREAM, WIDTH["limb"]); limb("el_n", "hand_n", CREAM, WIDTH["limb"] * 0.9)
    lay = lay.resize((bw, bh), Image.LANCZOS)
    # bayangan lembut di tanah
    sh = Image.new("RGBA", (360, 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([20, 12, 340, 48], fill=(0, 0, 0, 90))
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (int(x - 180), int(ground_y - 30)))
    frame.alpha_composite(lay, (bx0, by0))
    hand = (pts["hand_n"][0] + dx, pts["hand_n"][1] + dy)
    return hand


def lerp_q(a, b, t):
    return {k: a[k] + (b[k] - a[k]) * t for k in a}


STAND = {"tilt": 0.0, "head": 0.0, "ua_n": 0.06, "eb_n": 0.1, "ua_f": -0.06, "eb_f": 0.1,
         "th_n": 0.04, "kb_n": 0.02, "th_f": -0.04, "kb_f": 0.02}


def walk_q(t, hz=0.9, arm=None):
    ph = t * 2 * math.pi * hz
    s = math.sin(ph)
    q = dict(STAND, tilt=0.06, head=0.05)
    q.update(th_n=0.42 * s, th_f=-0.42 * s,
             kb_n=0.1 + 0.7 * max(0.0, math.sin(ph + 1.9)), kb_f=0.1 + 0.7 * max(0.0, math.sin(ph + 1.9 + math.pi)),
             ua_n=-0.38 * s, ua_f=0.38 * s, eb_n=0.35, eb_f=0.35)
    if arm:
        q.update(arm)
    return q


def pose(gerak, t, seconds):
    if gerak == "jalan":
        return walk_q(t)
    if gerak == "lentera":
        q = walk_q(t, 0.65, {"ua_n": 0.75 + 0.04 * math.sin(t * 4.1), "eb_n": 0.55})
        return q
    if gerak == "duduk":
        up = ease((t - 3.5) / 3.0)
        return {"tilt": -0.22 - 0.08 * up + 0.015 * math.sin(t * 1.6), "head": 0.3 - 0.75 * up,
                "ua_n": -0.5, "eb_n": 0.05, "ua_f": -0.6, "eb_f": 0.05,
                "th_n": 2.2, "kb_n": 1.95, "th_f": 2.05, "kb_f": 1.8}
    if gerak == "berlutut":
        bow = ease((t - 2.0) / 4.0)
        return {"tilt": 0.12 + 0.28 * bow + 0.012 * math.sin(t * 1.5), "head": 0.25 + 0.35 * bow,
                "ua_n": 0.55, "eb_n": 2.0, "ua_f": 0.45, "eb_f": 2.05,
                "th_n": 0.12, "kb_n": 1.62, "th_f": 0.08, "kb_f": 1.62}
    if gerak == "meraih":
        up = ease((t - 3.0) / 4.5)
        q = dict(STAND, head=-0.75 * ease((t - 2.0) / 4.0))
        q.update(ua_n=0.06 + 2.45 * up, eb_n=0.1 + 0.2 * (1 - up), tilt=-0.08 * up)
        return q
    if gerak == "bangkit":
        crouch = {"tilt": 1.05, "head": 0.3, "ua_n": 0.0, "eb_n": 0.15, "ua_f": -0.05, "eb_f": 0.2,
                  "th_n": 0.9, "kb_n": 2.3, "th_f": 0.75, "kb_f": 2.2}
        end = dict(STAND, head=-0.35, ua_n=0.55, eb_n=0.2, ua_f=-0.4, eb_f=0.2)
        return lerp_q(crouch, end, ease((t - 3.2) / 3.6))
    raise ValueError(gerak)


def glow_sprite(radius, color, strength=1.0):
    s = radius * 2
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    a = np.exp(-((xx - radius) ** 2 + (yy - radius) ** 2) / (2 * (radius / 2.6) ** 2)) * 255 * strength
    img = np.zeros((s, s, 4), np.uint8)
    img[..., :3] = color
    img[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def jalan_reel(i, seconds=13):
    p = tk.JALAN[i]
    rel = f"reels/{MOD}/jalan{i + 1}.mp4"
    moving = p["gerak"] in ("jalan", "lentera")
    speed = {"jalan": 95, "lentera": 70}.get(p["gerak"], 0)
    sky_w = RW + int(speed * 0.25 * seconds) + 4
    fg_w = RW + int(speed * seconds) + 4
    sky, fg, ground, info = scene(p["adegan"], sky_w, RH, fg_w, seed=40 + i)
    sky_img = Image.fromarray(sky) if isinstance(sky, np.ndarray) else sky
    tangan = font("tangan", 66)

    def lines_layer(a, b, y):
        def draw(d):
            for k, ln in enumerate([a, b]):
                if ln:
                    d.text((RW / 2, y + k * 84), ln.upper(), font=tangan, fill=(244, 234, 208, 255), anchor="ma")
        return text_layer((RW, RH), draw, 9)
    atas, bawah = lines_layer(p["atas"], p["atas2"], 300), lines_layer(p["bawah"], p["bawah2"], int(RH * 0.735))
    lantern = glow_sprite(260, (255, 196, 110), 0.55)
    sunglow = glow_sprite(520, (255, 214, 150), 0.6)
    gr = grains(strength=0.18)
    out, silent, ff = writer(rel)
    cx = RW * (0.42 if moving else 0.5)
    for n in range(FPS * seconds):
        t = n / FPS
        ox = int(speed * t)
        frame = sky_img.crop((int(ox * 0.25), 0, int(ox * 0.25) + RW, RH)).convert("RGBA")
        if "stars" in info:
            sx, sy, ph, sz = info["stars"]
            d = ImageDraw.Draw(frame)
            vis = (sx - ox * 0.25 > 0) & (sx - ox * 0.25 < RW)
            tw = 0.5 + 0.5 * np.sin(ph + t * 2.5)
            for x, y, a, r in zip(sx[vis] - ox * 0.25, sy[vis], tw[vis], sz[vis]):
                v = int(150 + 105 * a)
                d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill=(v, v, min(255, v + 10), 255))
        if p["gerak"] in ("meraih", "bangkit") and "sun" not in info:
            info["sun"] = (RW * 0.5, RH * 0.2)
        if p["gerak"] in ("meraih", "bangkit"):
            k = 0.25 + 0.75 * ease((t - 3.0) / 5.0)
            gx, gy = info["sun"]
            frame.alpha_composite(with_alpha(sunglow, k), (int(gx - ox * 0.25 - 520), int(gy - 520)))
        frame.alpha_composite(fg.crop((ox, 0, ox + RW, RH)))
        gy = float(ground[int(ox + cx)]) + 8
        hand = draw_figure(frame, pose(p["gerak"], t, seconds), cx, gy)
        if p["gerak"] == "lentera":
            hx, hy = hand
            frame.alpha_composite(lantern, (int(hx - 260), int(hy + 40 - 260)))
            d = ImageDraw.Draw(frame)
            d.line([(hx, hy), (hx, hy + 22)], fill=(40, 34, 30, 255), width=4)
            d.rounded_rectangle([hx - 18, hy + 22, hx + 18, hy + 70], radius=6, fill=(255, 214, 140, 255), outline=(60, 44, 30, 255), width=4)
        frame.alpha_composite(with_alpha(atas, ease((t - 0.5) / 0.9)))
        frame.alpha_composite(with_alpha(bawah, ease((t - 5.5) / 0.9)))
        rgb = ImageChops.add(frame.convert("RGB"), gr[n % len(gr)], scale=1, offset=-128)
        ff.stdin.write(rgb.tobytes())
    return finish(ff, silent, out, seconds, (174.6, 196.0, 164.8, 220.0, 185.0, 207.6)[i % 6], rel)


def relatable(p, i, mod):
    """Teks relatable gaya @jesusarmyid: latar putih, teks hitam besar rata kiri, handle kanan atas."""
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.text((W - 70, 90), HANDLE.upper(), font=font("sans_bold", 40), fill="#111111", anchor="ra")
    size = 84
    while True:
        f = font("sans", size)
        rows = []
        for para in p["teks"].split("\n"):
            rows += wrap(d, para, f, W - 150) + [""]
        rows = rows[:-1]
        if len(rows) * size * 1.18 < H * 0.62 or size <= 56:
            break
        size -= 4
    y = H * 0.52 - len(rows) * size * 1.18 / 2
    if p.get("atas"):
        d.text((75, y - 80), p["atas"], font=font("sans_medium", 34), fill="#8A8A8A")
    for r in rows:
        d.text((75, y), r, font=f, fill="#111111")
        y += size * 1.18 if r else size * 0.6
    return [save(img, f"{mod}/relatable{i + 1}.jpg")]


def render_keren(mod=MOD):
    """Carousel (F, V, T) -> {(hari, slot): (files, caption)}; Reels (K, J) dipakai kalau file-nya sudah ada."""
    m = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in m.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "F":
                out[(hari, slot)] = render_dump(idx, m, mod)
            elif fmt == "V":
                out[(hari, slot)] = render_dulu(idx, m, mod)
            elif fmt == "T":
                out[(hari, slot)] = (relatable(m.RELATABLE[idx], idx, mod), m.RELATABLE[idx]["caption"])
            else:
                rel = f"reels/{mod}/{'kinetik' if fmt == 'K' else 'jalan'}{idx + 1}.mp4"
                pool = m.KINETIK if fmt == "K" else m.JALAN
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], pool[idx]["caption"])
    return out


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "semua"
    mod = MOD
    if what == "w2":  # python3 keren.py w2 [kinetik] -> minggu 2 (konten/tenang_keren2.py)
        mod, what = "tenang_keren2", (sys.argv[2] if len(sys.argv) > 2 else "semua")
        sys.argv = sys.argv[1:]
    nums = [int(a) - 1 for a in sys.argv[2:]]
    if what in ("semua", "foto"):
        for k, (files, _) in render_keren(mod).items():
            print(k, len(files))
    if what in ("semua", "kinetik"):
        for i in nums or range(len(importlib.import_module(f"konten.{mod}").KINETIK)):
            print(kinetik_reel(i, mod))
    if what in ("semua", "jalan") and mod == MOD:
        for i in nums or range(len(tk.JALAN)):
            print(jalan_reel(i))
