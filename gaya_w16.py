"""Akun Tenang - minggu 16 (konten/tenang_w16.py), 10 - 16 Jan 2027: Minggu Pembaptisan Tuhan, identitas sebagai anak yang dikasihi.
37 gaya diacak tiap hari + komik Eli.
BARU (terinspirasi akun Instagram kreatif, isinya buatan sendiri):
       SIDIK (sidik jari generatif + kaca pembesar berisi teks mikro), UKUR (coretan tinggi badan di kusen pintu),
       ABJAD (kartu abjad "A untuk Abba" bercincin), JAHIT (pola jahit di kertas tisu di atas alas potong),
       TANGRAM (7 keping tangram membentuk merpati yang turun), PIKTO (piktogram 1 dari 100 domba, a la grafik data),
       HURUF (spesimen huruf "nama kamu"), SILSILAH (bagan silsilah keluarga Allah + cap merah),
       BATIK (motif kawung/ceplok prosedural + kartus), MARMER (kertas marmer bersisir + label buku),
       RIAK (Reel tetes air -> riak membawa suara Bapa), WARNAI (Reel mewarnai menurut nomor, satu bagian menunggu).
LAMA : KARTUPOS, PETA, SERTIFIKAT, JAM, RESEP, UNDANGAN, JENDELA, FILM, GARIS, VINYL, FLIP, PROGRESS.
MIX  : STICKYAIR, POLAROIDAIR, STAMPAIR, MAJALAHAIR (air sungai jernih + riak cahaya kaustik),
       TIKETAWAN, TELEGRAMAWAN, PHOTOBOOTHAWAN (langit awan putih + cahaya turun dari atas),
       KAMUSBENING, ALKITABBENING, KETIKBENING, CATATANBENING, EMAILBENING (efek bening: tint aqua + pantulan air tipis).
KOMIK = komik Eli & Yesus.

  python3 gaya_w16.py [reels]
"""
import datetime as dt
import importlib
import math
import re
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cerita
import config
import gaya_w5
import gaya_w6
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import gaya_w11
import gaya_w12
import render
from gaya_w6 import georgia, hn
from gaya_w7 import bayangan, bersih, comp, ease, fade, gradasi, pas, tangan, tanpa_kutip
from gaya_w11 import konteks
from gaya_w14 import bulat, catmull, goresan, kilau, kurva
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w16"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2027, 1, 10)
SUP = "/System/Library/Fonts/Supplemental/"

# Skema konten gaya BARU (batas = jumlah karakter maksimum). Semua item juga punya ayat, ref, caption.
SKEMA = {
    "SIDIK": "baris[3] = [label ≤10, isi ≤24], mikroteks ≤22, ayat ≤130",
    "UKUR": "tanda[4-6] = [label ≤18, tinggi_cm 60-190], puncak ≤28, ayat ≤140",
    "ABJAD": "huruf (1 huruf A-Z), kata ≤10, sub ≤30, kartu_belakang[2] = [huruf, kata ≤10], nomor ≤5, ayat ≤150",
    "JAHIT": "nomor ≤6, bagian ≤26, instruksi ≤30, ayat ≤150",
    "TANGRAM": "judul ≤20, label_kecil ≤22, ayat ≤150",
    "PIKTO": "judul ≤16, sub ≤50, label ≤10, ayat ≤170, sumber ≤30",
    "HURUF": "nama ≤12, meta[3] ≤26 (boleh 'Label: isi'), frasa ≤36, ayat ≤160",
    "SILSILAH": "puncak ≤10, tengah ≤20, anggota[6-9] ≤10, sorot ≤8, cap ≤24, ayat ≤160",
    "BATIK": "motif ('kawung' atau 'ceplok'), judul ≤20, ayat ≤170",
    "MARMER": "judul ≤18, ayat ≤170",
    "RIAK": "kata[4] ≤12, kicker ≤30, ayat ≤120 (Reels, 11 dtk)",
    "WARNAI": "judul ≤24, palet[6] ≤10, ayat ≤160 (Reels, 14 dtk)",
}


# ================= HURUF & ALAT BANTU =================

@lru_cache(maxsize=None)
def _ft(path, size, idx=0):
    return ImageFont.truetype(path if path.startswith("/") else SUP + path, max(6, int(size)), index=idx)


def avenir(size, idx=0):  # 0 Bold, 2 Demi, 5 Medium, 7 Regular, 8 Heavy
    return _ft("/System/Library/Fonts/Avenir Next.ttc", size, idx)


def helv(size, idx=0):  # 0 Regular, 1 Bold, 7 Light, 10 Medium
    return _ft("/System/Library/Fonts/HelveticaNeue.ttc", size, idx)


def menlo(size, idx=0):  # 0 Regular, 1 Bold
    return _ft("/System/Library/Fonts/Menlo.ttc", size, idx)


def charter(size, idx=0):  # 0 Roman, 1 Italic, 3 Bold, 5 Black
    return _ft("Charter.ttc", size, idx)


def iowan(size, idx=0):  # 0 Roman, 1 Bold, 2 Italic, 3 Bold Italic
    return _ft("Iowan Old Style.ttc", size, idx)


def basker(size, idx=0):  # 0 Regular, 1 Bold, 2 Italic, 3 Bold Italic, 4 SemiBold, 5 SemiBold Italic
    return _ft("Baskerville.ttc", size, idx)


def futura(size, idx=0):  # 0 Medium, 2 Bold, 4 Condensed ExtraBold
    return _ft("Futura.ttc", size, idx)


def din(size):
    return _ft("DIN Condensed Bold.ttf", size)


def kurir(size, tebal=True):
    return _ft("Courier New Bold.ttf" if tebal else "Courier New.ttf", size)


def mesin(size, idx=0):  # American Typewriter: 0 Regular, 2 Bold, 3 Semibold
    return _ft("AmericanTypewriter.ttc", size, idx)


def snell(size, idx=1):  # Snell Roundhand: 0 Regular, 1 Bold, 2 Black
    return _ft("SnellRoundhand.ttc", size, idx)


def gill(size, idx=0):  # Gill Sans: 0 Regular, 1 Bold, 4 SemiBold, 7 Light
    return _ft("GillSans.ttc", size, idx)


def caslon(size):
    return _ft("BigCaslon.ttf", size)


def spidol(size):
    return _ft("Bradley Hand Bold.ttf", size)


def georgia_b(size):
    return _ft("Georgia Bold.ttf", size)


PROBE = ImageDraw.Draw(Image.new("RGB", (10, 10)))


def muat(d, teks, font_fn, maxw, start, stop=12):
    """Font terbesar supaya teks satu baris muat selebar maxw (terus mengecil sampai muat)."""
    s = int(start)
    while s > 8 and d.textlength(teks, font=font_fn(s)) > maxw:
        s -= 2 if s > 40 else 1
    return font_fn(s)


def pas_aman(d, teks, font_fn, maxw, maxh, start, stop, lh):
    """Seperti pas(), tapi kalau di ukuran terkecil masih kepanjangan, terus mengecil sampai muat."""
    f, lines, size = pas(d, teks, font_fn, maxw, maxh, start, stop, lh)
    while (len(lines) * size * lh > maxh or max(d.textlength(ln, font=f) for ln in lines) > maxw) and size > 12:
        size -= 1
        f = font_fn(size)
        lines = wrap(d, teks, f, maxw)
    return f, lines, size


def renggang(d, xy, teks, font, fill, jarak, anchor="ls"):
    """Teks dengan jarak antarhuruf. anchor: l/m/r + baseline/ascender/middle. -> lebar total."""
    lebar = sum(d.textlength(c, font=font) for c in teks) + jarak * max(0, len(teks) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= lebar / 2
    elif anchor[0] == "r":
        x -= lebar
    for c in teks:
        d.text((x, y), c, font=font, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(c, font=font) + jarak
    return lebar


def lebar_renggang(d, teks, font, jarak):
    return sum(d.textlength(c, font=font) for c in teks) + jarak * max(0, len(teks) - 1)


def ref_besar(ref):
    """Nama kitab huruf kapital, pasal:ayat apa adanya (\"Yesaya 43:1b\" -> \"YESAYA 43:1b\")."""
    ref = bersih(ref)
    m = re.match(r"^(.*?)(\s+\d+[:.].*)$", ref)
    return m.group(1).upper() + m.group(2) if m else ref.upper()


def kredit(img, xy, warna, anchor="ma", font=None):
    ImageDraw.Draw(img).text(xy, "@" + HANDLE, font=font or avenir(22, 5), fill=warna, anchor=anchor)


def campur(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def kertas_np(w, h, warna, rng, kuat=0.05):
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (1 - kuat + 2 * kuat * render.fbm2d(h, w, rng, ((3, 1.0), (24, 0.5), (140, 0.3))))[..., None]
    return a


def ke_img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def garis_putus(d, pts, panjang, jeda, fill, width, lewati=None):
    """Garis putus-putus sepanjang polyline. lewati(p0, p1) -> True = segmen tidak digambar."""
    sisa, gambar = panjang, True
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        pos = 0.0
        while pos < L - 1e-6:
            step = min(sisa, L - pos)
            if gambar and not (lewati and lewati((x0, y0), (x1, y1))):
                a, b = pos / L, (pos + step) / L
                d.line((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b), fill=fill, width=width)
            pos += step
            sisa -= step
            if sisa <= 1e-6:
                gambar = not gambar
                sisa = panjang if gambar else jeda


def tulisan(teks, font, warna, sudut=0.0, pad=12):
    """Sprite teks satu baris (untuk diputar)."""
    w = int(font.getlength(teks)) + 2 * pad
    h = int(font.size * 1.7) + 2 * pad
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((pad, h / 2), teks, font=font, fill=warna, anchor="lm")
    return t.rotate(sudut, expand=True, resample=Image.BICUBIC) if sudut else t


_SPRITE = {}


def huruf_sprite(ch, font, fill):
    key = (ch, id(font), fill)
    if key not in _SPRITE:
        s = int(font.size * 2.4) + 8
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((s / 2, s / 2), ch, font=font, fill=fill, anchor="ms")
        _SPRITE[key] = im
    return _SPRITE[key]


def teks_lingkar(img, cx, cy, r, teks, font, fill, start_deg=-90.0, tracking=0.0, arah=1, tengah=True, alpha=1.0):
    """Teks di lingkaran: huruf demi huruf, diputar searah garis singgung.
    arah=1 : searah jarum jam, enak dibaca di busur ATAS (kepala huruf ke luar).
    arah=-1: berlawanan jarum jam, enak dibaca di busur BAWAH (kepala huruf ke dalam).
    start_deg = sudut tengah teks (tengah=True) atau awal teks; 0 = kanan, 90 = bawah."""
    adv = [font.getlength(c) for c in teks]
    total = sum(adv) + tracking * max(0, len(teks) - 1)
    th0 = math.radians(start_deg) - (arah * total / (2 * r) if tengah else 0.0)
    pos = 0.0
    for c, a in zip(teks, adv):
        th = th0 + arah * (pos + a / 2) / r
        pos += a + tracking
        if c == " ":
            continue
        phi = math.degrees(th) + 90 * arah
        sp = huruf_sprite(c, font, fill).rotate(-phi, resample=Image.BICUBIC)
        if alpha < 1:
            sp = fade(sp, alpha)
        comp(img, sp, (cx + r * math.cos(th) - sp.width / 2, cy + r * math.sin(th) - sp.height / 2))
    return total


def teks_jalur(img, pts, teks, font, fill, mulai=0.0, tracking=0.0):
    """Teks mengikuti polyline pts (kepala huruf di kiri arah jalan). -> panjang terpakai."""
    pts = np.asarray(pts, np.float64)
    seg = np.diff(pts, axis=0)
    L = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.concatenate([[0.0], np.cumsum(L)])
    pos = mulai
    for c in teks:
        a = font.getlength(c)
        s = pos + a / 2
        if s > cum[-1]:
            break
        k = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(L) - 1))
        u = (s - cum[k]) / max(L[k], 1e-6)
        x, y = pts[k] + seg[k] * u
        if c != " ":
            phi = math.degrees(math.atan2(seg[k][1], seg[k][0]))
            sp = huruf_sprite(c, font, fill).rotate(-phi, resample=Image.BICUBIC)
            comp(img, sp, (x - sp.width / 2, y - sp.height / 2))
        pos += a + tracking
    return pos


def kaustik(w, h, seed, sel=120, tebal=0.05, turun=4, lengkung=1.1):
    """Jaring cahaya kaustik (tepi sel Voronoi yang dilengkungkan fbm) -> array 0..1 ukuran (h, w)."""
    rng = np.random.default_rng(seed)
    sw, sh = w // turun + 1, h // turun + 1
    n = int(w * h / sel ** 2) + 10
    px = rng.uniform(-sel, w + sel, n) / turun
    py = rng.uniform(-sel, h + sel, n) / turun
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    cel = sel / turun
    X = xx + (render.fbm2d(sh, sw, rng, ((3, 1.0), (7, 0.5))) - 0.5) * cel * lengkung
    Y = yy + (render.fbm2d(sh, sw, rng, ((3, 1.0), (7, 0.5))) - 0.5) * cel * lengkung
    f1 = np.full((sh, sw), 1e9, np.float32)
    f2 = f1.copy()
    for a, b in zip(px, py):
        dd = (X - a) ** 2 + (Y - b) ** 2
        f2 = np.minimum(f2, np.maximum(f1, dd))
        f1 = np.minimum(f1, dd)
    e = np.sqrt(f2) - np.sqrt(f1)
    c = np.exp(-(e / (tebal * cel)) ** 2)
    img = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img).astype(np.float32) / 255


# Dua fungsi di bawah disalin dari gaya_w15 (pisah lapisan depan gaya lama lalu warnai ulang teks terang).

def pisah_lapisan(fn):
    """Render fn(latar) di atas latar hitam & putih -> (rgb premultiplied, alpha) dari semua yang digambar di atas latar."""
    hitam = np.asarray(fn(Image.new("RGB", (W, H), (0, 0, 0))).convert("RGB")).astype(np.float32)
    putih = np.asarray(fn(Image.new("RGB", (W, H), (255, 255, 255))).convert("RGB")).astype(np.float32)
    a = np.clip(1 - (putih - hitam).mean(axis=2) / 255, 0, 1)
    return np.minimum(hitam, a[..., None] * 255), a


def teks_gelap(fn, latar, zona, ink=(46, 42, 74), aksen=(186, 88, 52)):
    """Gaya lama yang mengira latarnya gelap (teks krem/emas) dipakai di latar terang: teks terang di dalam `zona`
    (daftar kotak) diwarnai ulang gelap: emas -> aksen, selain itu -> ink."""
    pre, a = pisah_lapisan(fn)
    bg = np.asarray(latar.convert("RGB").resize((W, H))).astype(np.float32)
    out = pre + (1 - a)[..., None] * bg
    F = pre / np.maximum(a, 1e-3)[..., None]
    lum = F @ np.array([0.299, 0.587, 0.114], np.float32)
    inti = (a > 0.35) & (lum > 135)

    def lebarkan(m, n):
        return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n))) > 0
    terang = lebarkan(inti, 3) & (a > 0.004)
    emas = lebarkan(inti & ((F[..., 0] - F[..., 2]) > 90), 5)
    z = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in zona:
        z[int(y0):int(y1), int(x0):int(x1)] = True
    m = terang & z
    col = np.where(emas[..., None], np.array(aksen, np.float32), np.array(ink, np.float32))
    baru = a[..., None] * col + (1 - a)[..., None] * bg
    out = np.where(m[..., None], baru, out)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


# ================= LATAR & EFEK MINGGU INI =================

def air_latar(w, h, seed, gelap=False):
    """AIR: air sungai jernih dilihat dari atas, biru kehijauan, kerikil samar di dasar, riak cahaya kaustik lembut.
    gelap=True untuk gaya yang menaruh teks putih langsung di latar (air lebih dalam)."""
    rng = np.random.default_rng(seed)
    atas, bawah = ((30, 104, 120), (8, 46, 66)) if gelap else ((176, 226, 222), (100, 182, 190))
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(atas, np.float32) * (1 - t) + np.array(bawah, np.float32) * t
    a = np.broadcast_to(a, (h, w, 3)).copy()
    n = render.fbm2d(h, w, rng, ((2, 1.0), (5, 0.6), (13, 0.3)))
    a *= (0.92 + 0.16 * n)[..., None]
    a += ((n - 0.5) * 2)[..., None] * np.array([-8, 6, -2], np.float32)
    img = ke_img(a).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(int(w * h / 26000)):  # kerikil di dasar sungai, buram oleh air
        x, y = rng.uniform(-30, w + 30), rng.uniform(-30, h + 30)
        rx = rng.uniform(16, 58)
        ry = rx * rng.uniform(0.55, 0.85)
        terang = rng.random() < 0.45
        col = (236, 240, 220) if terang else ((0, 30, 40) if gelap else (40, 96, 96))
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=col + (int(rng.uniform(20, 46)),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(7)))
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    c = kaustik(w, h, seed + 1, sel=130, tebal=0.055) * (0.35 + 0.8 * render.fbm2d(h, w, rng, ((3, 1.0), (7, 0.5))))
    c2 = kaustik(w, h, seed + 2, sel=70, tebal=0.06) * 0.3
    c = np.asarray(ke_img(np.clip(c + c2, 0, 1) * 255).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255
    yy = np.linspace(0, 1, h)[:, None]
    kuat = (0.36 - 0.2 * yy) if gelap else (0.32 - 0.1 * yy)
    a += (np.array([235, 255, 250], np.float32) - a) * (c * kuat)[..., None]
    # kilau permukaan: pita cahaya miring yang lembut
    xx = np.linspace(0, 1, w)[None, :]
    kilap = np.exp(-((xx * 0.8 + yy * 0.6 - 0.45) / 0.18) ** 2) * (0.10 if gelap else 0.12)
    a += (255 - a) * kilap[..., None]
    vig = 1 - 0.18 * np.clip(np.hypot(xx - 0.5, yy - 0.5) * 1.6 - 0.3, 0, 1)
    a *= vig[..., None]
    return grain(ke_img(a), 0.025)


def awan_latar(w, h, seed):
    """AWAN: langit lembut dengan awan putih, cahaya turun dari atas (seperti terang/merpati dari langit)."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, h)[:, None, None]
    c0, c1, c2 = np.array([120, 168, 222], np.float32), np.array([188, 214, 238], np.float32), np.array([236, 240, 244], np.float32)
    a = np.where(t < 0.55, c0 * (1 - t / 0.55) + c1 * (t / 0.55), c1 * (1 - (t - 0.55) / 0.45) + c2 * ((t - 0.55) / 0.45))
    a = np.broadcast_to(a, (h, w, 3)).copy()
    xx = np.linspace(0, 1, w)[None, :]
    yy = np.linspace(0, 1, h)[:, None]
    sx = 0.5 + rng.uniform(-0.08, 0.08)
    glow = np.exp(-(((xx - sx) * w / h) ** 2 + (yy + 0.06) ** 2) / 0.09)
    a += (np.array([255, 252, 240], np.float32) - a) * (glow * 0.85)[..., None]
    img = ke_img(a).convert("RGBA")
    # berkas cahaya turun
    s = 4
    m = Image.new("L", (w // s, h // s), 0)
    md = ImageDraw.Draw(m)
    ox, oy = sx * w / s, -0.12 * h / s
    for k in range(9):
        ang = math.radians(90 + (k - 4) * 9 + rng.uniform(-3, 3))
        lb = math.radians(rng.uniform(1.2, 2.6))
        L = 2 * h / s
        md.polygon([(ox, oy), (ox + math.cos(ang - lb) * L, oy + math.sin(ang - lb) * L), (ox + math.cos(ang + lb) * L, oy + math.sin(ang + lb) * L)],
                   fill=int(rng.uniform(60, 120)))
    m = m.filter(ImageFilter.GaussianBlur(6)).resize((w, h), Image.BICUBIC)
    ray = np.asarray(m).astype(np.float32) / 255 * np.clip(1.1 - yy * 1.2, 0, 1)
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    a += (255 - a) * (ray * 0.55)[..., None]
    img = ke_img(a).convert("RGBA")
    # awan: gumpalan elips; bayangan kebiruan di bawah, putih di atas
    for k in range(9):
        cx = rng.uniform(-0.1, 1.1) * w
        cy = (rng.uniform(0.55, 1.02) if k < 6 else rng.uniform(0.12, 0.4)) * h
        if k >= 6 and abs(cx / w - sx) < 0.28:
            cx = (sx + (0.38 if cx / w > sx else -0.38)) * w
        lebar = rng.uniform(240, 460) * (0.7 if k >= 6 else 1)
        puff = []
        for _ in range(int(rng.integers(10, 18))):
            r = rng.uniform(40, 110) * (0.7 if k >= 6 else 1)
            px, py = cx + rng.uniform(-lebar / 2, lebar / 2), cy + rng.uniform(-r * 0.6, r * 0.2)
            puff.append((px, py, r))
        bay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bay)
        for px, py, r in puff:
            bd.ellipse((px - r, py - r * 0.75 + 16, px + r, py + r * 0.75 + 16), fill=(176, 194, 220, 120))
        img.alpha_composite(bay.filter(ImageFilter.GaussianBlur(18)))
        put = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        pd = ImageDraw.Draw(put)
        for px, py, r in puff:
            pd.ellipse((px - r, py - r * 0.75, px + r, py + r * 0.75), fill=(255, 255, 255, 190))
        img.alpha_composite(put.filter(ImageFilter.GaussianBlur(14)))
    return grain(img.convert("RGB"), 0.03)


def bening(img, seed, kuat=1.0):
    """BENING: efek pada gambar jadi: tint aqua bening + pantulan cahaya air (kaustik) tipis dari atas."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    yy = np.linspace(0, 1, h)[:, None]
    xx = np.linspace(0, 1, w)[None, :]
    a = a * np.array([0.87, 0.965, 0.985], np.float32) + np.array([4, 12, 14], np.float32) * (1 - a / 255)
    a += (255 - a) * ((1 - yy) ** 2 * 0.10)[..., None] * np.array([0.7, 1.0, 1.0], np.float32)
    c = kaustik(w, h, seed, sel=150, tebal=0.045)
    c *= 0.45 + 0.75 * render.fbm2d(h, w, rng, ((3, 1.0), (8, 0.5)))
    c *= 0.55 + 0.45 * (1 - yy)
    cs = np.roll(np.roll(c, 6, axis=0), 4, axis=1)
    a *= (1 - 0.07 * kuat * np.clip(cs - c, 0, 1))[..., None]
    a += (np.array([236, 255, 252], np.float32) - a) * (0.36 * kuat * np.clip(c, 0, 1))[..., None]
    vig = np.clip(np.hypot(xx - 0.5, yy - 0.5) * 1.5 - 0.35, 0, 1)
    a = a * (1 - 0.10 * vig[..., None]) + np.array([20, 70, 80], np.float32) * 0.10 * vig[..., None]
    return grain(ke_img(a), 0.02)


# ================= BARU =================

# ---------- SIDIK: sidik jari + kaca pembesar ----------

SIDIK_GAYA = [  # tinta, kartu, meja
    ((34, 40, 58), (248, 246, 242), (196, 202, 208)),
    ((60, 44, 38), (247, 243, 235), (208, 198, 184)),
    ((26, 58, 68), (245, 247, 244), (188, 204, 200)),
]


def sidik_image(p, i):
    rng = np.random.default_rng(16100 + i)
    tinta, kartu_c, meja = SIDIK_GAYA[i % 3]
    merah, garis, rim = (200, 50, 50), (200, 196, 190), (60, 60, 66)
    img = grain(ke_img(kertas_np(W, H, meja, rng, 0.06)), 0.04).convert("RGBA")
    kx0, ky0, kw, kh = 44, 44, W - 88, H - 88
    kartu = ke_img(kertas_np(kw, kh, kartu_c, rng, 0.02)).convert("RGBA")
    bayangan(img, kartu, (kx0, ky0), blur=16, geser=(0, 10), kuat=0.32)
    d = ImageDraw.Draw(img)
    d.text((96, 86), "KARTU SIDIK JARI", font=menlo(26, 1), fill=tinta)
    d.text((W - 96, 90), p.get("_tanggal", "").upper(), font=menlo(20), fill=merah, anchor="ra")
    d.line((96, 132, W - 96, 132), fill=tinta, width=2)
    d.line((96, 137, W - 96, 137), fill=tinta, width=1)
    d.text((96, 150), "TANGAN KANAN · JARI TELUNJUK", font=menlo(16), fill=(130, 128, 126))
    d.text((W - 96, 150), "SATU-SATUNYA", font=menlo(16), fill=(130, 128, 126), anchor="ra")
    # --- sidik jari (2x) ---
    cx, cy, A, B = 396, 482, 226, 290
    S = 2
    bx0, by0 = cx - A - 30, cy - B - 30
    bw, bh = 2 * A + 60, 2 * B + 60
    hh, ww = bh * S, bw * S
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    xx = xx / S + bx0
    yy = yy / S + by0
    dx = xx - cx + 24 * (render.fbm2d(hh, ww, rng, ((2, 1.0), (5, 0.5))) - 0.5)
    dy = yy - cy + 24 * (render.fbm2d(hh, ww, rng, ((2, 1.0), (5, 0.5))) - 0.5)
    f = 30
    iy = -0.12 * B
    rr = np.sqrt((dx / A) ** 2 + ((dy - iy) / B) ** 2) + (3 / f) * np.arctan2(dy - iy, dx) / (2 * np.pi)
    # pangkal jari: guratan melandai jadi busur datar (membentuk delta di kiri-kanan bawah)
    wb = np.clip((dy / B - 0.3) / 0.45, 0, 1) ** 2
    datar = 0.62 + 0.9 * (dy / B - 0.3) + 0.22 * (dx / A) ** 2
    rr = rr * (1 - wb) + datar * wb
    rr += 0.035 * (render.fbm2d(hh, ww, rng, ((6, 1.0), (14, 0.5))) - 0.5)
    rid = np.abs(np.sin(rr * f * np.pi))
    ink = np.clip((0.52 - rid) / 0.14, 0, 1)
    e = np.sqrt((dx / A) ** 2 + (dy / B) ** 2)
    tepi = 1 + 0.1 * (render.fbm2d(hh, ww, rng, ((5, 1.0), (12, 0.5))) - 0.5)
    env = np.clip((tepi - e) / 0.07, 0, 1)
    tekan = np.clip(1.15 - e ** 2 * 0.6, 0.4, 1)
    fp = render.fbm2d(hh, ww, rng, ((70, 1.0), (150, 0.5)))
    putus = np.clip((fp - np.percentile(fp, 7)) / 0.03, 0, 1)  # ujung guratan kecil-kecil (minusi)
    tekstur = 0.7 + 0.4 * render.fbm2d(hh, ww, rng, ((30, 1.0), (90, 0.5)))
    Fx, Fy = cx + 166, cy - 112  # titik fokus kaca pembesar
    r0 = math.hypot((Fx - cx) / A, (Fy - cy) / B)
    e0 = np.sqrt(((xx - cx) / A) ** 2 + ((yy - cy) / B) ** 2)
    lajur = np.clip((np.abs(e0 - r0) - 0.58 / f) / 0.005, 0, 1)  # satu guratan diganti teks mikro
    alpha = np.clip(ink * env * tekan * putus * tekstur * lajur, 0, 1)
    lay = Image.new("RGBA", (ww, hh), tinta + (0,))
    lay.putalpha(Image.fromarray((alpha * 238).astype(np.uint8)))
    mikro = bersih(p["mikroteks"]).strip(" ·")
    awal = math.atan2((Fy - cy) / B, (Fx - cx) / A) - 1.1
    u = np.linspace(awal, awal + 2 * np.pi, 1600)
    pts = [((cx + (A * r0 - 2.6) * math.cos(t) - bx0) * S, (cy + (B * r0 - 2.6) * math.sin(t) - by0) * S) for t in u]
    tl = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
    fm = helv(10 * S, 10)
    unit = mikro + " · "
    keliling = float(np.sum(np.hypot(*np.diff(np.asarray(pts), axis=0).T)))
    lu = sum(fm.getlength(c) for c in unit) + 1.0 * len(unit)
    n_ul = max(1, int(keliling // lu))
    trk = 1.0 + (keliling - n_ul * lu) / (n_ul * len(unit))  # isi lingkar pas, tanpa sambungan bertumpuk
    teks_jalur(tl, pts, unit * n_ul, fm, tinta + (255,), tracking=trk)
    lay.alpha_composite(tl)
    img.alpha_composite(lay.resize((bw, bh), Image.LANCZOS), (bx0, by0))
    d = ImageDraw.Draw(img)
    # tanda merah
    for k, (mx, my, lx, ly) in enumerate(((cx - 150, cy + 150, 112, cy + 236), (cx + 52, cy + 236, cx + 196, cy + 300))):
        d.ellipse((mx - 24, my - 24, mx + 24, my + 24), outline=merah, width=3)
        ang = math.atan2(ly - my, lx - mx)
        d.line((mx + math.cos(ang) * 24, my + math.sin(ang) * 24, lx + (14 if lx < mx else -14), ly), fill=merah, width=2)
        d.text((lx, ly), str(k + 1), font=menlo(22, 1), fill=merah, anchor="mm")
    # --- kaca pembesar ---
    R = 172
    fx2, fy2 = (Fx - bx0) * S, (Fy - by0) * S
    pot = lay.crop((int(fx2 - R), int(fy2 - R), int(fx2 + R), int(fy2 + R)))
    kaca = ke_img(kertas_np(2 * R, 2 * R, campur(kartu_c, (255, 255, 255), 0.4), rng, 0.015)).convert("RGBA")
    kaca.alpha_composite(pot)
    yk, xk = np.mgrid[0:2 * R, 0:2 * R].astype(np.float32)
    rk = np.hypot(xk - R, yk - R) / R
    ka = np.asarray(kaca.convert("RGB")).astype(np.float32)
    ka *= (1 - 0.12 * np.clip(rk - 0.7, 0, 1) / 0.3)[..., None] * np.array([0.97, 0.99, 1.0])
    kilap = np.exp(-(((xk - R * 0.62) ** 2 + (yk - R * 0.55) ** 2) / (R * 0.32) ** 2)) * 0.22
    ka += (255 - ka) * kilap[..., None]
    kaca = ke_img(ka).convert("RGBA")
    mask = Image.new("L", (8 * R, 8 * R), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 8 * R - 1, 8 * R - 1), fill=255)
    kaca.putalpha(mask.resize((2 * R, 2 * R), Image.LANCZOS))
    # gagang dulu (di bawah bingkai)
    gag = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gag)
    ux, uy = math.cos(math.radians(45)), math.sin(math.radians(45))
    p0 = (Fx + ux * (R + 4), Fy + uy * (R + 4))
    p1 = (Fx + ux * (R + 46), Fy + uy * (R + 46))
    p2 = (Fx + ux * (R + 220), Fy + uy * (R + 220))
    gd.line([(p0[0] * 2, p0[1] * 2), (p1[0] * 2, p1[1] * 2)], fill=(150, 150, 156, 255), width=44)
    gd.line([(p1[0] * 2, p1[1] * 2), (p2[0] * 2, p2[1] * 2)], fill=(44, 40, 46, 255), width=72)
    gd.ellipse((p2[0] * 2 - 36, p2[1] * 2 - 36, p2[0] * 2 + 36, p2[1] * 2 + 36), fill=(44, 40, 46, 255))
    gd.line([((p1[0] - uy * 9) * 2, (p1[1] + ux * 9) * 2), ((p2[0] - uy * 9) * 2, (p2[1] + ux * 9) * 2)], fill=(90, 86, 94, 255), width=8)
    gag = gag.resize((W, H), Image.LANCZOS)
    bayangan(img, gag, (0, 0), blur=12, geser=(10, 14), kuat=0.3)
    bay = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0))
    ImageDraw.Draw(bay).ellipse((20, 20, 2 * R + 20, 2 * R + 20), fill=(0, 0, 0, 90))
    comp(img, bay.filter(ImageFilter.GaussianBlur(14)), (Fx - R - 20 + 12, Fy - R - 20 + 16))
    comp(img, kaca, (Fx - R, Fy - R))
    cin = Image.new("RGBA", ((2 * R + 40) * 3, (2 * R + 40) * 3), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cin)
    c3 = (R + 20) * 3
    cd.ellipse((c3 - (R + 8) * 3, c3 - (R + 8) * 3, c3 + (R + 8) * 3, c3 + (R + 8) * 3), outline=rim + (255,), width=16 * 3)
    cd.arc((c3 - (R + 2) * 3, c3 - (R + 2) * 3, c3 + (R + 2) * 3, c3 + (R + 2) * 3), 200, 290, fill=(150, 150, 160, 255), width=3 * 3)
    comp(img, cin.resize((2 * R + 40, 2 * R + 40), Image.LANCZOS), (Fx - R - 20, Fy - R - 20))
    d = ImageDraw.Draw(img)
    # --- ayat ---
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s: charter(s), W - 192, 160, 42, 26, 1.28)
    y = 800 + max(0, (220 - len(lines) * size * 1.28 - 44) / 2)
    for ln in lines:
        d.text((96, y), ln, font=f_, fill=tinta)
        y += size * 1.28
    d.text((96, y + 10), ref_besar(p["ref"]), font=menlo(22, 1), fill=merah)
    # --- kotak keterangan ---
    bx_, by_, bw_ = 96, 1040, W - 192
    rh = 62
    d.rectangle((bx_, by_, bx_ + bw_, by_ + 34), fill=campur(kartu_c, garis, 0.45))
    d.text((bx_ + 16, by_ + 17), "KETERANGAN", font=menlo(17, 1), fill=tinta, anchor="lm")
    d.text((bx_ + bw_ - 16, by_ + 17), "DIISI OLEH: PENCIPTA", font=menlo(15), fill=(120, 116, 112), anchor="rm")
    for k, (lab, isi) in enumerate(p["baris"][:3]):
        y0 = by_ + 34 + k * rh
        d.line((bx_, y0, bx_ + bw_, y0), fill=garis, width=2)
        d.line((bx_ + 214, y0, bx_ + 214, y0 + rh), fill=garis, width=1)
        lab = bersih(lab).upper() + ":"
        d.text((bx_ + 18, y0 + rh / 2), lab, font=muat(d, lab, lambda s: menlo(s, 1), 186, 20), fill=tinta, anchor="lm")
        isi = bersih(isi)
        fi = muat(d, isi, lambda s: menlo(s), bw_ - 270, 27)
        d.text((bx_ + 236, y0 + rh / 2 + 1), isi, font=fi, fill=tinta, anchor="lm")
        if k == 2:  # lingkaran spidol merah di isian terakhir
            tw = d.textlength(isi, font=fi)
            ex0, ex1 = bx_ + 220, bx_ + 252 + tw
            emx, emy = (ex0 + ex1) / 2, y0 + rh / 2
            pts = [(emx + (ex1 - ex0) / 2 * 1.07 * math.cos(t), emy + 27 * math.sin(t)) for t in np.linspace(-2.6, 2 * math.pi - 2.3, 50)]
            goresan(d, pts, 3, merah, rng, 0.9)
    d.rectangle((bx_, by_, bx_ + bw_, by_ + 34 + 3 * rh), outline=garis, width=2)
    d.text((W / 2, H - 82), "@" + HANDLE, font=menlo(18), fill=(140, 138, 136), anchor="ma")
    return img


# ---------- UKUR: coretan tinggi badan di kusen pintu ----------

UKUR_GAYA = [  # dinding, kayu terang, kayu gelap
    ((240, 236, 228), (196, 150, 98), (170, 124, 78)),
    ((226, 234, 226), (204, 160, 108), (172, 124, 80)),
    ((236, 230, 236), (190, 142, 94), (160, 114, 70)),
]


def pensil_sprite(panjang=300):
    def gambar(d, k):
        h = 26
        d.polygon([(0, h * k / 2), (34 * k, 3 * k), (34 * k, (h - 3) * k)], fill=(226, 196, 150))
        d.polygon([(0, h * k / 2), (11 * k, 9.5 * k), (11 * k, (h - 9.5) * k)], fill=(50, 50, 54))
        d.rectangle((34 * k, 2 * k, (panjang - 46) * k, (h - 2) * k), fill=(244, 196, 52))
        for yy in (9, 17):
            d.line((34 * k, yy * k, (panjang - 46) * k, yy * k), fill=(214, 160, 30), width=int(1.5 * k))
        d.rectangle(((panjang - 46) * k, 1 * k, (panjang - 24) * k, (h - 1) * k), fill=(190, 190, 196))
        d.rounded_rectangle(((panjang - 26) * k, 1 * k, panjang * k, (h - 1) * k), radius=6 * k, fill=(236, 140, 150))
    return sprite(panjang, 26, gambar)


def sprite(w, h, fn, k=4):
    big = Image.new("RGBA", (int(w * k), int(h * k)), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), k)
    return big.resize((int(w), int(h)), Image.LANCZOS)


def ukur_image(p, i):
    rng = np.random.default_rng(16200 + i)
    dind, k1, k2 = UKUR_GAYA[i % 3]
    tick, pensil, merah, teks_c = (60, 48, 36), (88, 88, 96), (214, 64, 52), (48, 44, 40)
    a = kertas_np(W, H, dind, rng, 0.025)
    a *= (0.995 + 0.012 * np.sin(np.arange(W) * 0.045 + 3 * render.fbm2d(1, W, rng, ((4, 1.0),))[0]))[None, :, None]
    FX0, FX1 = 60, 236
    fw = FX1 - FX0
    nn = render.fbm2d(H, fw, rng, ((2, 1.0), (6, 0.5)))
    s = 0.5 + 0.5 * np.sin(np.arange(fw)[None, :] * 0.25 + 4 * nn)
    wood = np.array(k1, np.float32) * (1 - s[..., None]) + np.array(k2, np.float32) * s[..., None]
    serat = np.asarray(Image.fromarray((rng.random((H // 90, fw // 2)) * 255).astype(np.uint8)).resize((fw, H), Image.BICUBIC)).astype(np.float32) / 255
    wood *= (0.9 + 0.14 * serat + 0.06 * render.fbm2d(H, fw, rng, ((1, 1.0), (40, 0.4))))[..., None]
    sh = np.ones(fw, np.float32)
    sh[:10] = 1.10
    sh[-14:] = np.linspace(0.95, 0.78, 14)
    sh[28:31] = 0.86
    wood *= sh[None, :, None]
    a[:, FX0:FX1] = wood
    a[:, :FX0] = np.array(campur(dind, (255, 255, 255), 0.35), np.float32) * np.linspace(0.86, 0.95, FX0)[None, :, None]
    a[:, FX1:FX1 + 26] *= np.linspace(0.84, 1.0, 26)[None, :, None]
    plint = 1262
    a[plint:, FX1:] = np.array([246, 244, 238], np.float32)
    a[plint:plint + 5, FX1:] *= 0.86
    a[plint + 5:plint + 14, FX1:] *= np.linspace(0.93, 1, 9)[:, None, None]
    img = grain(ke_img(a), 0.035).convert("RGBA")
    d = ImageDraw.Draw(img)
    # skala
    tanda = [(bersih(lab), int(cm)) for lab, cm in p["tanda"]]
    tertinggi = max(cm for _, cm in tanda)
    puncak_cm = min(tertinggi + 12, 214)
    ppc = (plint - 170) / puncak_cm  # 0 cm tepat di lantai (atas plint), +-6 px per cm
    ycm = lambda cm: plint - cm * ppc
    cm_top, cm_bot = int(puncak_cm + 170 / ppc) + 1, 0
    for cm in range(cm_bot, cm_top + 1):
        y = ycm(cm)
        if not (0 <= y <= H):
            continue
        L = 32 if cm % 10 == 0 else (21 if cm % 5 == 0 else 11)
        d.line((FX0 + 10, y, FX0 + 10 + L, y), fill=tick, width=2 if cm % 5 == 0 else 1)
        if cm % 10 == 0:
            d.text((FX0 + 50, y + 1), str(cm), font=din(26), fill=tick, anchor="lm")
    # coretan pensil
    urut = sorted(tanda, key=lambda t: -t[1])
    akhir = ycm(puncak_cm) + 66
    tempat = []
    for lab, cm in urut:
        y = ycm(cm)
        yl = max(y, akhir + 42)
        tempat.append((lab, cm, y, yl))
        akhir = yl
    for lab, cm, y, yl in tempat:
        goresan(d, [(150, y + rng.normal(0, 0.8)), (210, y + rng.normal(0, 0.8)), (292, y + rng.normal(0, 1.2))], 3, pensil, rng, 0.6)
        goresan(d, [(162, y + 2), (280, y + 2.5)], 1, campur(pensil, dind, 0.4), rng, 0.6)
        fn = muat(d, lab, spidol, 280, 30, 18)
        t = tulisan(lab, fn, pensil + (235,), rng.uniform(-2, 2))
        comp(img, t, (300, yl - t.height / 2))
        if yl - y > 6:
            goresan(d, [(294, y), (304, yl - 6)], 1.5, pensil, rng, 0.4)
    # puncak: krayon merah
    yp = ycm(puncak_cm)
    kr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kr)
    for k in range(4):
        goresan(kd, [(140, yp + rng.normal(0, 1.5) + k - 2), (220, yp + rng.normal(0, 1.5)), (300, yp + rng.normal(0, 2) + k * 0.6 - 1)], 5, merah + (200,), rng, 1.0)
    ka = np.asarray(kr.getchannel("A")).astype(np.float32) * (0.55 + 0.6 * render.fbm2d(H, W, rng, ((60, 1.0), (240, 0.8))))
    kr.putalpha(ke_img(ka).convert("L"))
    img.alpha_composite(kr)
    pk = bersih(p["puncak"])
    t = tulisan(pk, muat(d, pk, spidol, W - 70 - 304, 38, 22), merah + (240,), rng.uniform(-1.5, 1))
    comp(img, t, (300, yp - t.height / 2 - 2))
    t = tulisan(p.get("_tanggal", ""), spidol(24), pensil + (220,), rng.uniform(-1.5, 1.5))
    comp(img, t, (304, yp + 18))
    # anak kecil coretan, tangannya menyentuh tanda terendah
    _, _, ylow, ylb = tempat[-1]
    ax, ay = 336, ylb + 34
    sk = min(1.0, max(0.55, (plint - 20 - ay) / 150))
    d = ImageDraw.Draw(img)
    hx, hy = ax, ay + 20 * sk
    d.ellipse((hx - 15 * sk, hy - 15 * sk, hx + 15 * sk, hy + 15 * sk), outline=pensil, width=3)
    goresan(d, [(hx, hy + 15 * sk), (hx + 1, hy + 70 * sk)], 3, pensil, rng, 0.8)
    goresan(d, [(hx, hy + 28 * sk), (hx - 22 * sk, hy + 4 * sk), (296, ylow + 4)], 3, pensil, rng, 0.8)
    goresan(d, [(hx, hy + 30 * sk), (hx + 26 * sk, hy + 18 * sk)], 3, pensil, rng, 0.8)
    goresan(d, [(hx + 1, hy + 70 * sk), (hx - 14 * sk, hy + 112 * sk)], 3, pensil, rng, 0.8)
    goresan(d, [(hx + 1, hy + 70 * sk), (hx + 16 * sk, hy + 112 * sk)], 3, pensil, rng, 0.8)
    d.arc((hx - 7 * sk, hy - 2 * sk, hx + 7 * sk, hy + 8 * sk), 20, 160, fill=pensil, width=2)
    # ayat di kanan
    x0, y0, y1 = 616, max(yp + 140, 330), 1180
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s_: charter(s_), W - 70 - x0, y1 - y0 - 80, 44, 24, 1.34)
    tinggi = len(lines) * size * 1.34 + 60
    y = y0 + max(0, (y1 - y0 - tinggi) / 2)
    for ln in lines:
        d.text((x0, y), ln, font=f_, fill=teks_c)
        y += size * 1.34
    d.text((x0, y + 14), ref_besar(p["ref"]), font=din(32), fill=k2)
    pn = pensil_sprite(300).rotate(2.5, expand=True, resample=Image.BICUBIC)
    bayangan(img, pn, (620, plint - 30), blur=4, geser=(2, 4), kuat=0.3)
    kredit(img, (W - 76, plint + 44), (150, 146, 140), anchor="rm", font=avenir(20, 5))
    return img


# ---------- ABJAD: kartu abjad bercincin ----------

ABJAD_LATAR = [(120, 190, 240), (122, 198, 178), (246, 178, 124)]


def huruf_kecil(h):
    """Pasangan huruf kecil untuk kartu abjad (satu huruf Latin saja, bukan teks konten)."""
    return chr(ord(h) + 32) if "A" <= h <= "Z" else h


def abjad_image(p, i):
    rng = np.random.default_rng(16300 + i)
    bg = ABJAD_LATAR[i % 3]
    merah, navy, kuning, cincin, krem = (230, 70, 60), (30, 44, 90), (250, 200, 40), (180, 184, 190), (252, 247, 236)
    a = np.zeros((H, W, 3), np.float32) + np.array(bg, np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a += (255 - a) * (0.18 * np.exp(-(((xx - W * 0.5) / 700) ** 2 + ((yy - H * 0.4) / 600) ** 2)))[..., None]
    img = grain(ke_img(a), 0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    for k in range(14):  # konfeti bentuk dasar samar
        x, y, r = rng.uniform(40, W - 40), rng.uniform(40, 260 if k < 7 else H - 300), rng.uniform(8, 18)
        if 120 < x < 960 and 250 < y < 1000:
            continue
        col = campur(bg, (255, 255, 255), 0.35)
        if k % 3 == 0:
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)
        elif k % 3 == 1:
            d.polygon([(x, y - r), (x + r, y + r), (x - r, y + r)], fill=col)
        else:
            d.rectangle((x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8), fill=col)
    cw, ch = 780, 670
    x0, y0 = 132, 304
    px, py = x0 + 58, y0 + 58
    K = 2

    def kartu_kosong(warna):
        c = Image.new("RGBA", (cw * K, ch * K), (0, 0, 0, 0))
        cd = ImageDraw.Draw(c)
        cd.rounded_rectangle((0, 0, cw * K - 1, ch * K - 1), radius=34 * K, fill=warna + (255,), outline=campur(warna, (150, 130, 110), 0.25) + (255,), width=2 * K)
        cd.ellipse(((58 - 15) * K, (58 - 15) * K, (58 + 15) * K, (58 + 15) * K), fill=campur(bg, (0, 0, 0), 0.25) + (255,))
        return c, cd
    # kartu belakang (yang paling jauh dulu)
    belakang = p["kartu_belakang"][:2]
    for k, (sudut, warna_k, warna_h) in enumerate(((20, (238, 228, 206), navy), (10, (246, 238, 220), merah))):
        hb, kb = belakang[1 - k] if len(belakang) > 1 - k else ("", "")
        c, cd = kartu_kosong(warna_k)
        hb = bersih(hb).strip()[:1].upper()
        kb = bersih(kb).upper()
        fh, fk = futura(48 * K, 2), bulat(36 * K, "Bold")
        lk = cd.textlength(kb, font=fk)
        lt = cd.textlength(hb + " · ", font=fh)
        xr = (cw - 40) * K
        cd.text((xr - lk, 52 * K), kb, font=fk, fill=navy, anchor="ls")
        cd.text((xr - lk - lt, 52 * K), hb + " · ", font=fh, fill=warna_h, anchor="ls")
        c = c.resize((cw, ch), Image.LANCZOS)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(c, (x0, y0))
        lay = lay.rotate(sudut, resample=Image.BICUBIC, center=(px, py))
        bayangan(img, lay, (0, 0), blur=12, geser=(0, 8), kuat=0.25)
    # kartu depan
    c, cd = kartu_kosong(krem)
    huruf = bersih(p["huruf"]).strip()[:1].upper() or "A"
    fA, fa = futura(320 * K, 2), futura(250 * K, 0)
    lebar = cd.textlength(huruf, font=fA) + 16 * K + cd.textlength(huruf_kecil(huruf), font=fa)
    skala = min(1.0, 410 * K / lebar)
    fA, fa = futura(320 * K * skala, 2), futura(250 * K * skala, 0)
    cd.text((54 * K, 404 * K), huruf, font=fA, fill=merah, anchor="ls")
    cd.text((54 * K + cd.textlength(huruf, font=fA) + 16 * K * skala, 404 * K), huruf_kecil(huruf), font=fa, fill=merah, anchor="ls")
    S = lambda *v: [q * K for q in v]
    cd.ellipse(S(510, 112, 714, 316), fill=kuning)
    for k in range(10):  # sinar kecil
        ang = math.radians(-160 + k * 16)
        cd.line(S(612 + math.cos(ang) * 116, 214 + math.sin(ang) * 116, 612 + math.cos(ang) * 140, 214 + math.sin(ang) * 140), fill=kuning, width=6 * K)
    cd.ellipse(S(548, 150, 604, 206), fill=navy)
    cd.polygon([(556 * K, 216 * K), (596 * K, 216 * K), (620 * K, 392 * K), (532 * K, 392 * K)], fill=navy)
    cd.ellipse(S(662, 262, 702, 302), fill=merah)
    cd.polygon([(666 * K, 310 * K), (698 * K, 310 * K), (712 * K, 392 * K), (652 * K, 392 * K)], fill=merah)
    cd.line([(596 * K, 262 * K), (628 * K, 304 * K), (668 * K, 322 * K)], fill=navy, width=11 * K, joint="curve")
    cd.ellipse(S(652, 312, 674, 334), fill=navy)
    cd.line(S(492, 395, 742, 395), fill=navy, width=4 * K)
    hx, hy = 636, 244  # hati kecil
    cd.ellipse(S(hx - 13, hy - 10, hx + 1, hy + 4), fill=merah)
    cd.ellipse(S(hx - 1, hy - 10, hx + 13, hy + 4), fill=merah)
    cd.polygon([((hx - 12.5) * K, (hy - 1) * K), ((hx + 12.5) * K, (hy - 1) * K), (hx * K, (hy + 14) * K)], fill=merah)
    nomor = bersih(p["nomor"])
    fn_ = avenir(26 * K, 2)
    nw = cd.textlength(nomor, font=fn_) + 36 * K
    cd.rounded_rectangle(((cw - 40) * K - nw, 34 * K, (cw - 40) * K, 78 * K), radius=22 * K, outline=navy, width=3 * K)
    cd.text(((cw - 40) * K - nw / 2, 56 * K), nomor, font=fn_, fill=navy, anchor="mm")
    kata = bersih(p["kata"]).upper()
    fk = muat(cd, kata, lambda s_: bulat(s_, "Bold"), (cw - 110) * K, 74 * K)
    tw = cd.textlength(kata, font=fk)
    cd.rounded_rectangle((48 * K, 452 * K, 48 * K + tw + 24 * K, 452 * K + fk.size * 0.5), radius=10 * K, fill=kuning)
    cd.text((60 * K, 418 * K), kata, font=fk, fill=navy, anchor="la")
    sub = bersih(p["sub"])
    cd.text((60 * K, 548 * K), sub, font=muat(cd, sub, lambda s_: avenir(s_, 5), (cw - 120) * K, 30 * K), fill=navy, anchor="la")
    garis_putus(cd, [(60 * K, 610 * K), ((cw - 60) * K, 610 * K)], 10 * K, 10 * K, campur(krem, navy, 0.25), 2 * K)
    cd.text(((cw - 44) * K, (ch - 30) * K), "@" + HANDLE, font=avenir(20 * K, 5), fill=(150, 150, 160), anchor="rs")
    c = c.resize((cw, ch), Image.LANCZOS)
    bayangan(img, c, (x0, y0), blur=14, geser=(0, 10), kuat=0.3)
    # cincin
    k3 = 3
    rcx, rcy, r3 = 50 * k3, 50 * k3, 40 * k3
    big = Image.new("RGBA", (100 * k3, 100 * k3), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    bd.ellipse(((50 - 13) * k3, (90 - 13) * k3, (50 + 13) * k3, (90 + 13) * k3), fill=(40, 40, 50, 255))
    bd.arc((rcx - r3, rcy - r3 + 10 * k3, rcx + r3, rcy + r3 + 10 * k3), 112, 428, fill=cincin + (255,), width=12 * k3)
    bd.arc((rcx - r3 + 5 * k3, rcy - r3 + 15 * k3, rcx + r3 - 5 * k3, rcy + r3 + 5 * k3), 190, 300, fill=(236, 238, 242, 255), width=3 * k3)
    ring = big.resize((100, 100), Image.LANCZOS)
    bayangan(img, ring, (px - 50, py - 90), blur=4, geser=(2, 4), kuat=0.35)
    # pita ayat
    d = ImageDraw.Draw(img)
    yb = 1012
    d.rectangle((0, yb, W, H), fill=navy)
    d.rectangle((0, yb, W, yb + 8), fill=kuning)
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s_: charter(s_), W - 180, 200, 34, 22, 1.34)
    y = yb + 34 + max(0, (200 - len(lines) * size * 1.34) / 2)
    for ln in lines:
        d.text((W / 2, y), ln, font=f_, fill=krem, anchor="ma")
        y += size * 1.34
    d.text((W / 2, y + 12), ref_besar(p["ref"]), font=avenir(26, 2), fill=kuning, anchor="ma")
    return img


# ---------- JAHIT: pola jahit di kertas tisu ----------

JAHIT_ALAS = [((54, 110, 96), (90, 150, 130)), ((44, 82, 122), (84, 126, 170)), ((66, 70, 80), (106, 112, 124))]


def bentuk_pola(jenis):
    """Kepingan pola dalam kotak satuan -> dict: garis (titik), lipat (x atau None), takik, titik, area_teks, serat."""
    if jenis == "lengan":
        cap = catmull([(0, 0.32), (0.12, 0.22), (0.3, 0.07), (0.5, 0.02), (0.7, 0.07), (0.88, 0.22), (1, 0.32)], 16)
        garis = cap + [(0.86, 0.985), (0.14, 0.985)]
        return {"garis": garis, "lipat": None, "takik": [(0.2, 0.17, 1), (0.8, 0.17, 2), (0.5, 0.02, 1)],
                "titik": [(0.5, 0.1)], "teks": (0.17, 0.36, 0.83, 0.93), "serat": (0.5, 0.12, 0.31)}
    belakang = jenis == "belakang"
    leher = [(0, 0.065), (0.15, 0.06), (0.26, 0.04), (0.31, 0.02)] if belakang else [(0, 0.15), (0.14, 0.135), (0.25, 0.085), (0.31, 0.02)]
    garis = catmull(leher, 12) + catmull([(0.76, 0.095), (0.72, 0.2), (0.735, 0.31), (0.8, 0.38), (0.9, 0.4)], 12) \
        + catmull([(0.95, 0.97), (0.7, 0.985), (0.35, 0.99), (0, 0.985)], 12)
    info = {"garis": garis, "lipat": 0.0, "takik": [(0.927, 0.6, 2 if belakang else 1), (0.735, 0.3, 2 if belakang else 1)],
            "titik": [(0.52, 0.17), (0.3, 0.26)], "teks": (0.09, 0.33, 0.68, 0.93), "serat": (0.8, 0.48, 0.9)}
    if belakang:  # cermin: lipatan di kanan
        info["garis"] = [(1 - x, y) for x, y in info["garis"]]
        info["lipat"] = 1.0
        info["takik"] = [(1 - x, y, n) for x, y, n in info["takik"]]
        info["titik"] = [(1 - x, y) for x, y in info["titik"]]
        x0, y0, x1, y1 = info["teks"]
        info["teks"] = (1 - x1, y0, 1 - x0, y1)
        info["serat"] = (0.2, 0.48, 0.9)
    return info


def gunting_sprite(s=90):
    def gambar(d, k):
        S = s * k
        col = (40, 36, 34, 255)
        for cy in (0.3, 0.7):
            d.ellipse((S * 0.02, S * (cy - 0.13), S * 0.28, S * (cy + 0.13)), outline=col, width=int(S * 0.045))
        d.polygon([(S * 0.27, S * 0.36), (S * 0.98, S * 0.56), (S * 0.3, S * 0.5)], fill=col)
        d.polygon([(S * 0.27, S * 0.64), (S * 0.98, S * 0.44), (S * 0.3, S * 0.5)], fill=col)
        d.ellipse((S * 0.42, S * 0.46, S * 0.5, S * 0.54), fill=(226, 206, 170, 255))
    return sprite(s, s, gambar)


def jahit_image(p, i):
    rng = np.random.default_rng(16400 + i)
    alas, grid = JAHIT_ALAS[i % 3]
    ink, merah, kepala, baja = (40, 36, 34), (190, 50, 40), (230, 60, 60), (190, 190, 196)
    img = grain(ke_img(kertas_np(W, H, alas, rng, 0.04)), 0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    for x in range(14, W, 27):
        d.line((x, 0, x, H), fill=grid, width=2 if (x - 14) % 135 == 0 else 1)
    for y in range(14, H, 27):
        d.line((0, y, W, y), fill=grid, width=2 if (y - 14) % 135 == 0 else 1)
    for k in range(-3, 6):
        x = k * 270
        d.line((x, 0, x + H, H), fill=campur(alas, grid, 0.5), width=1)
    # kertas tisu
    tw_, th_ = W - 50, H - 50
    sisi = []
    for (ax, ay), (bx, by) in zip([(0, 0), (tw_, 0), (tw_, th_), (0, th_)], [(tw_, 0), (tw_, th_), (0, th_), (0, 0)]):
        for t in np.linspace(0, 1, 30, endpoint=False):
            sisi.append((ax + (bx - ax) * t + rng.normal(0, 1.4), ay + (by - ay) * t + rng.normal(0, 1.4)))
    m = Image.new("L", (tw_ + 20, th_ + 20), 0)
    ImageDraw.Draw(m).polygon([(x + 10, y + 10) for x, y in sisi], fill=232)
    yy, xx = np.mgrid[0:th_ + 20, 0:tw_ + 20].astype(np.float32)
    keriput = 0.965 + 0.035 * np.sin((xx * 0.7 + yy) * 0.02 + 4 * render.fbm2d(th_ + 20, tw_ + 20, rng, ((3, 1.0), (8, 0.5))))
    ta = np.zeros((th_ + 20, tw_ + 20, 3), np.float32) + np.array([236, 218, 184], np.float32)
    ta *= keriput[..., None]
    lip = Image.new("L", (tw_ + 20, th_ + 20), 0)
    ld = ImageDraw.Draw(lip)
    for _ in range(5):
        x0_, y0_ = rng.uniform(0, tw_), rng.uniform(0, th_)
        ang = rng.uniform(0, math.pi)
        L = rng.uniform(300, 900)
        ld.line([(x0_ + math.cos(ang) * L * t + 18 * math.sin(t * 5), y0_ + math.sin(ang) * L * t) for t in np.linspace(-0.5, 0.5, 30)], fill=255, width=3)
    lipa = np.asarray(lip.filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    ta += (255 - ta) * (lipa * 0.35)[..., None]
    tis = ke_img(ta).convert("RGBA")
    tis.putalpha(m)
    tis = tis.rotate(-0.8, expand=True, resample=Image.BICUBIC)
    bayangan(img, tis, (25 - 10 - (tis.width - tw_ - 20) / 2, 25 - 10 - (tis.height - th_ - 20) / 2), blur=10, geser=(0, 6), kuat=0.2)
    # lapisan cetak pola (2x)
    K = 2
    lay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    P = lambda pts: [(x * K, y * K) for x, y in pts]
    jenis = ["depan", "lengan", "belakang"][i % 3]
    info = bentuk_pola(jenis)
    bx0, by0, bw, bh = 150, 186, 780, 1000
    pt = lambda x, y: (bx0 + x * bw, by0 + y * bh)
    garis = [pt(x, y) for x, y in info["garis"]]
    gx = sum(x for x, _ in garis) / len(garis)
    gy = sum(y for _, y in garis) / len(garis)
    lipat_x = None if info["lipat"] is None else bx0 + info["lipat"] * bw
    for k, (sk, pj, jd) in enumerate(((1.035, 4, 7), (1.07, 14, 6))):  # garis ukuran lain
        ax_ = lipat_x if lipat_x is not None else gx
        g2 = [(ax_ + (x - ax_) * sk, gy + (y - gy) * sk) for x, y in garis]
        garis_putus(ld, P(g2 + [g2[0]]), pj * K, jd * K, ink + (150,), 2 * K, lewati=lambda a_, b_: lipat_x is not None and abs(a_[0] - lipat_x * K) < 3 * K and abs(b_[0] - lipat_x * K) < 3 * K)
        tx, ty = g2[int(len(g2) * (0.3 + 0.07 * k))]
        nx, ny = tx - gx, ty - gy
        nl = math.hypot(nx, ny) or 1
        ld.text(((tx + nx / nl * 16) * K, (ty + ny / nl * 16) * K), str(4 + 2 * k), font=kurir(18 * K), fill=ink + (170,), anchor="mm")
    ld.line(P(garis + [garis[0]]), fill=ink + (255,), width=4 * K, joint="curve")
    jahit = [(gx + (x - gx) * 0.95, gy + (y - gy) * 0.95) for x, y in garis]
    if lipat_x is not None:
        jahit = [(lipat_x if abs(x0_ - lipat_x) < 3 else gx + (x0_ - gx) * 0.95, y) for (x0_, _), (_, y) in zip(garis, jahit)]
    garis_putus(ld, P(jahit + [jahit[0]]), 12 * K, 8 * K, ink + (230,), 2 * K, lewati=lambda a_, b_: lipat_x is not None and abs(a_[0] - lipat_x * K) < 3 * K and abs(b_[0] - lipat_x * K) < 3 * K)
    for tx, ty, n in info["takik"]:
        x, y = pt(tx, ty)
        ang = math.atan2(gy - y, gx - x)
        for j in range(n):
            o = (j - (n - 1) / 2) * 18
            bx_, by_ = x - math.sin(ang) * o, y + math.cos(ang) * o
            ld.polygon(P([(bx_ - math.sin(ang) * 7, by_ + math.cos(ang) * 7), (bx_ + math.sin(ang) * 7, by_ - math.cos(ang) * 7),
                          (bx_ + math.cos(ang) * 16, by_ + math.sin(ang) * 16)]), fill=ink + (255,))
    for tx, ty in info["titik"]:
        x, y = pt(tx, ty)
        ld.ellipse(P([(x - 8, y - 8), (x + 8, y + 8)]), fill=ink + (255,))
        ld.ellipse(P([(x - 3, y - 3), (x + 3, y + 3)]), fill=(226, 206, 170, 255))
    sx, sy0, sy1 = info["serat"]
    ax_, ay0, ay1 = bx0 + sx * bw, by0 + sy0 * bh, by0 + sy1 * bh
    ld.line(P([(ax_, ay0 + 14), (ax_, ay1 - 14)]), fill=ink + (255,), width=3 * K)
    for yy_, s_ in ((ay0, 1), (ay1, -1)):
        ld.polygon(P([(ax_, yy_), (ax_ - 10, yy_ + 24 * s_), (ax_ + 10, yy_ + 24 * s_)]), fill=ink + (255,))
    st = tulisan("ARAH SERAT KAIN", kurir(17 * K), ink + (255,), 90)
    lay.alpha_composite(st, (int(ax_ * K - st.width - 10 * K), int(((ay0 + ay1) / 2) * K - st.height / 2)))
    if lipat_x is not None:  # tanda lipatan
        kanan = info["lipat"] > 0.5
        lx = lipat_x + (-26 if kanan else 26)
        ya, yb = by0 + 0.3 * bh, by0 + 0.88 * bh
        ld.line(P([(lx, ya), (lx, yb)]), fill=ink + (255,), width=2 * K)
        for yy_ in (ya, yb):
            ld.line(P([(lx, yy_), (lipat_x, yy_)]), fill=ink + (255,), width=2 * K)
            s_ = 1 if kanan else -1
            ld.polygon(P([(lipat_x, yy_), (lipat_x - 12 * s_, yy_ - 6), (lipat_x - 12 * s_, yy_ + 6)]), fill=ink + (255,))
        st = tulisan("LETAKKAN DI LIPATAN KAIN", kurir(17 * K), ink + (255,), 90 if not kanan else -90)
        lay.alpha_composite(st, (int((lx + (8 if not kanan else -8)) * K - (0 if not kanan else st.width)), int((ya + yb) / 2 * K - st.height / 2)))
    # teks di dalam kepingan
    tx0, ty0, tx1, ty1 = info["teks"]
    tx0, ty0, tx1, ty1 = bx0 + tx0 * bw, by0 + ty0 * bh, bx0 + tx1 * bw, by0 + ty1 * bh
    if jenis == "lengan":
        ty0 = by0 + 0.36 * bh
    bag = bersih(p["bagian"]).upper()
    ins = bersih(p["instruksi"]).upper()
    fb = muat(ld, bag, lambda s_: kurir(s_ * K), (tx1 - tx0) * K, 36)
    fi = muat(ld, ins, lambda s_: kurir(s_ * K), (tx1 - tx0) * K, 26)
    kepala_h = fb.size / K * 1.2 + fi.size / K * 1.3 + 12 + 22
    f_, lines, _ = pas_aman(ld, bersih(p["ayat"]), lambda s_: mesin(s_ * K), (tx1 - tx0) * K, (ty1 - ty0 - kepala_h - 50) * K, 32, 20, 1.34)
    total = kepala_h + len(lines) * f_.size / K * 1.34 + 40
    y = ty0 + max(0, (ty1 - ty0 - total) * 0.4)
    ld.text((tx0 * K, y * K), bag, font=fb, fill=ink + (255,))
    y += fb.size / K * 1.2
    ld.text((tx0 * K, y * K), ins, font=fi, fill=merah + (255,))
    y += fi.size / K * 1.3 + 12
    ld.line(P([(tx0, y), (tx1, y)]), fill=ink + (200,), width=2 * K)
    y += 22
    for ln in lines:
        ld.text((tx0 * K, y * K), ln, font=f_, fill=ink + (255,))
        y += f_.size / K * 1.34
    ld.text((tx0 * K, (y + 10) * K), ref_besar(p["ref"]), font=kurir(22 * K), fill=merah + (255,))
    # kepala lembar pola
    ld.text((70 * K, 52 * K), "POLA", font=kurir(26 * K), fill=ink + (255,))
    nomor = bersih(p["nomor"])
    nomor = nomor if nomor[:2] in ("No", "NO", "no") else "No. " + nomor
    ld.text((70 * K, 82 * K), nomor, font=din(78 * K), fill=ink + (255,))
    ld.text((W * K - 76 * K, 60 * K), "UKURAN 2 · 4 · 6", font=kurir(18 * K), fill=ink + (220,), anchor="ra")
    ld.text((W * K - 76 * K, 88 * K), "ANAK-ANAK", font=kurir(18 * K), fill=ink + (220,), anchor="ra")
    # keterangan garis
    ly_ = H - 112
    ld.line(P([(70, ly_), (150, ly_)]), fill=ink + (255,), width=4 * K)
    ld.text((166 * K, ly_ * K), "GARIS POTONG", font=kurir(16 * K), fill=ink + (255,), anchor="lm")
    garis_putus(ld, P([(70, ly_ + 30), (150, ly_ + 30)]), 12 * K, 8 * K, ink + (255,), 2 * K)
    ld.text((166 * K, (ly_ + 30) * K), "GARIS JAHIT 1,5 CM", font=kurir(16 * K), fill=ink + (255,), anchor="lm")
    lay = lay.resize((W, H), Image.LANCZOS)
    la = np.asarray(lay.getchannel("A")).astype(np.float32) * (0.82 + 0.18 * render.fbm2d(H, W, rng, ((40, 1.0), (160, 0.6))))
    lay.putalpha(ke_img(la).convert("L"))
    img.alpha_composite(lay)
    # gunting di garis potong, jarum pentul
    gk = int(len(garis) * (0.62 if jenis != "lengan" else 0.12))
    (ax_, ay_), (bx_, by_) = garis[gk], garis[min(gk + 2, len(garis) - 1)]
    ang = math.degrees(math.atan2(by_ - ay_, bx_ - ax_))
    gs = gunting_sprite(96).rotate(-ang + 180, expand=True, resample=Image.BICUBIC)
    bayangan(img, gs, (ax_ - gs.width / 2, ay_ - gs.height / 2), blur=3, geser=(3, 4), kuat=0.3)
    for (qx, qy, sud) in ((300 + 40 * (i % 2), 250, 28), (770 - 60 * (i % 2), 1110, -152)):
        L = 120
        ex, ey = qx + math.cos(math.radians(sud)) * L, qy + math.sin(math.radians(sud)) * L
        jl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        jd = ImageDraw.Draw(jl)
        jd.line((qx, qy, ex, ey), fill=baja + (255,), width=3)
        jd.ellipse((qx - 12, qy - 12, qx + 12, qy + 12), fill=kepala + (255,))
        jd.ellipse((qx - 6, qy - 8, qx - 1, qy - 3), fill=(255, 210, 210, 255))
        bayangan(img, jl, (0, 0), blur=3, geser=(4, 5), kuat=0.35)
    kredit(img, (W - 76, H - 70), ink, anchor="rs", font=kurir(18))
    return img


# ---------- TANGRAM: tujuh keping membentuk merpati ----------

TG_KEPING = {  # bujur sangkar tangram baku 4x4: luas 4, 4, 2, 2, 1, 1, 2 (= 16)
    "LT1": [(0, 0), (4, 0), (2, 2)],               # segitiga besar
    "LT2": [(0, 0), (2, 2), (0, 4)],               # segitiga besar
    "MT": [(4, 2), (4, 4), (2, 4)],                # segitiga sedang
    "SQ": [(2, 2), (3, 1), (4, 2), (3, 3)],        # persegi
    "ST1": [(3, 1), (4, 0), (4, 2)],               # segitiga kecil
    "ST2": [(1, 3), (2, 2), (3, 3)],               # segitiga kecil
    "PL": [(0, 4), (1, 3), (3, 3), (2, 4)],        # jajaran genjang
}
# merpati (menghadap kiri): keping -> (putar derajat, geser x, geser y, cermin); disetel sekali dengan mata, lalu dimiringkan.
# badan = segitiga besar, sayap terangkat = segitiga besar + jajaran genjang (sayap belakang), kepala = persegi,
# paruh = segitiga kecil, ekor = segitiga sedang + segitiga kecil.
DOVE = {
    "LT1": (0, -2.0, -2.0, False),        # badan
    "LT2": (45, 1.8284, -4.8284, False),  # sayap terangkat
    "PL": (90, 5.8284, -2.0, True),       # sayap belakang (dicerminkan)
    "SQ": (0, -4.0, -5.0, False),         # kepala
    "ST1": (270, -3.0, 0.0, False),       # paruh
    "MT": (225, 2.0, 3.6569, False),      # ekor
    "ST2": (45, 3.4142, -4.8284, False),  # ujung ekor
}
MIRING = -28  # seluruh merpati diputar: kepala turun (merpati turun dari langit)
TG_WARNA = {"LT1": (40, 80, 200), "LT2": (230, 70, 50), "MT": (250, 200, 40), "SQ": (90, 190, 160), "ST1": (240, 150, 170),
            "ST2": (30, 40, 90), "PL": (245, 140, 40)}


def tg_transform(nama, deg, dx, dy, flip):
    a = math.radians(deg)
    out = []
    for x, y in TG_KEPING[nama]:
        if flip:
            x = -x
        out.append((x * math.cos(a) - y * math.sin(a) + dx, x * math.sin(a) + y * math.cos(a) + dy))
    return out


def tg_luas(pts):
    return 0.5 * abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts))))


assert sorted(round(tg_luas(v)) for v in TG_KEPING.values()) == [1, 1, 2, 2, 2, 4, 4]
assert all(abs(tg_luas(tg_transform(n, *t)) - tg_luas(TG_KEPING[n])) < 1e-6 for n, t in DOVE.items())


def susut(pts, px):
    cx, cy = sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
    out = []
    for x, y in pts:
        L = math.hypot(x - cx, y - cy)
        out.append((x - (x - cx) / L * px, y - (y - cy) / L * px))
    return out


def tangram_image(p, i):
    rng = np.random.default_rng(16500 + i)
    bg, sinar_c = (244, 241, 234), (200, 196, 186)
    img = grain(ke_img(kertas_np(W, H, bg, rng, 0.015)), 0.025).convert("RGBA")
    warna = dict(TG_WARNA)
    if i % 3 == 1:
        warna.update({"LT1": (230, 70, 50), "LT2": (40, 80, 200)})
    elif i % 3 == 2:
        warna.update({"LT1": (30, 40, 90), "ST2": (40, 80, 200), "LT2": (90, 190, 160), "SQ": (230, 70, 50)})
    # merpati
    poli = {}
    a = math.radians(MIRING)
    for n, t in DOVE.items():
        pts = tg_transform(n, *t)
        pts = [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        if i % 2 == 1:
            pts = [(-x, y) for x, y in pts]
        poli[n] = pts
    xs = [x for v in poli.values() for x, _ in v]
    ys = [y for v in poli.values() for _, y in v]
    bx0, by0, bx1, by1 = 170, 250, 930, 880
    sk = min((bx1 - bx0) / (max(xs) - min(xs)), (by1 - by0) / (max(ys) - min(ys)))
    ox = (bx0 + bx1) / 2 - (max(xs) + min(xs)) / 2 * sk
    oy = (by0 + by1) / 2 - (max(ys) + min(ys)) / 2 * sk
    # sinar dari atas
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    sx = W / 2 + (40 if i % 2 == 0 else -40)
    for k in range(13):
        ang = math.radians(60 + k * 5)
        ld.line((sx, -60, sx + math.cos(ang) * 1300, -60 + math.sin(ang) * 1300), fill=sinar_c + (255,), width=2)
    yy_ = np.linspace(0, 1, H)
    al = np.asarray(lay.getchannel("A")).astype(np.float32) * (np.clip((yy_ * H - 150) / 140, 0, 1) * np.clip(1.25 - yy_ * 1.55, 0, 1))[:, None]
    lay.putalpha(ke_img(al).convert("L"))
    img.alpha_composite(lay)
    K = 3
    big = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    for n, pts in poli.items():
        q = susut([(ox + x * sk, oy + y * sk) for x, y in pts], 2.5)
        bd.polygon([(x * K, y * K) for x, y in q], fill=warna[n] + (255,))
    dove = big.resize((W, H), Image.LANCZOS)
    bayangan(img, dove, (0, 0), blur=10, geser=(0, 12), kuat=0.12)
    d = ImageDraw.Draw(img)
    # bujur sangkar asal (kiri atas)
    s0, qx, qy = 37, 80, 74
    big = Image.new("RGBA", (int(4 * s0 + 4) * K, int(4 * s0 + 4) * K), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    for n, pts in TG_KEPING.items():
        q = susut([(2 + x * s0, 2 + y * s0) for x, y in pts], 1.5)
        bd.polygon([(x * K, y * K) for x, y in q], fill=warna[n] + (255,))
    comp(img, big.resize((4 * s0 + 4, 4 * s0 + 4), Image.LANCZOS), (qx - 2, qy - 2))
    lk = bersih(p["label_kecil"])
    d.text((qx, qy + 4 * s0 + 18), lk, font=muat(d, lk, lambda s_: avenir(s_, 2), 330, 22), fill=(110, 104, 96))
    pts = kurva((qx + 4 * s0 + 18, qy + 60), (qx + 4 * s0 + 120, qy + 20), (qx + 4 * s0 + 170, qy + 150), 30)
    garis_putus(d, pts, 9, 7, (150, 144, 134), 3)
    (ax_, ay_), (bx_, by_) = pts[-3], pts[-1]
    ang = math.atan2(by_ - ay_, bx_ - ax_)
    d.polygon([(bx_ + math.cos(ang) * 6, by_ + math.sin(ang) * 6), (bx_ - math.cos(ang - 0.5) * 16, by_ - math.sin(ang - 0.5) * 16),
               (bx_ - math.cos(ang + 0.5) * 16, by_ - math.sin(ang + 0.5) * 16)], fill=(150, 144, 134))
    judul = bersih(p["judul"])
    fj = muat(d, judul, lambda s_: futura(s_, 2), W - 70 - 330, 58)
    d.text((W - 72, 70), judul, font=fj, fill=(30, 40, 90), anchor="ra")
    d.text((W - 74, 70 + fj.size * 1.25), p.get("_tanggal", ""), font=avenir(22, 5), fill=(140, 134, 126), anchor="ra")
    # ayat kiri bawah
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s_: avenir(s_, 7), 700, 1200 - 930 - 50, 33, 22, 1.36)
    y = 930 + max(0, (1200 - 930 - 50 - len(lines) * size * 1.36) / 2)
    for ln in lines:
        d.text((80, y), ln, font=f_, fill=(44, 42, 50))
        y += size * 1.36
    d.text((80, y + 12), ref_besar(p["ref"]), font=futura(26, 2), fill=warna["LT1"] if i % 3 != 2 else (40, 80, 200))
    kredit(img, (W - 72, H - 64), (150, 144, 136), anchor="rs", font=avenir(20, 5))
    return img


# ---------- PIKTO: 1 dari 100 ----------

def domba(d, x, y, s, col, kepala=(110, 104, 98)):
    """Piktogram domba menghadap kanan, pusat (x, y), lebar ~s (d boleh 4x; koordinat sudah dikali)."""
    r = 0.21 * s
    for ox, oy in ((-0.2, 0.02), (0.0, -0.08), (0.2, 0.0), (-0.08, 0.1), (0.1, 0.1)):
        d.ellipse((x + ox * s - r, y + oy * s - r, x + ox * s + r, y + oy * s + r), fill=col)
    for lx in (-0.12, 0.14):
        d.rounded_rectangle((x + lx * s - 0.035 * s, y + 0.18 * s, x + lx * s + 0.035 * s, y + 0.42 * s), radius=0.03 * s, fill=kepala)
    d.ellipse((x + 0.3 * s, y - 0.17 * s, x + 0.52 * s, y + 0.03 * s), fill=kepala)
    d.ellipse((x + 0.28 * s, y - 0.16 * s, x + 0.36 * s, y - 0.1 * s), fill=kepala)


PIKTO_AKSEN = [(238, 120, 60), (214, 72, 96), (34, 150, 140)]


def pikto_image(p, i):
    rng = np.random.default_rng(16600 + i)
    krem, abu, kepala, teks_c, panah_c = (247, 242, 232), (196, 192, 184), (110, 104, 98), (40, 36, 32), (120, 112, 104)
    aksen = PIKTO_AKSEN[i % 3]
    img = grain(ke_img(kertas_np(W, H, krem, rng, 0.015)), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    judul = bersih(p["judul"])
    d.text((80, 82), judul, font=muat(d, judul, georgia_b, W - 160, 66), fill=teks_c)
    f_, lines, size = pas_aman(d, bersih(p["sub"]), lambda s_: georgia(s_, True), W - 160, 84, 30, 22, 1.3)
    y = 172
    for ln in lines:
        d.text((80, y), ln, font=f_, fill=(96, 90, 84))
        y += size * 1.3
    kiri = i % 2 == 0
    pitch, s = 68, 52
    gx0 = 86 if kiri else W - 86 - 10 * pitch
    gy0 = 296
    kol_x = (gx0 + 10 * pitch + 22, W - 70) if kiri else (70, gx0 - 22)
    hilang = ([4, 6, 2][i % 3], 9 if kiri else 0)
    K = 4
    big = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    for r in range(10):
        for c in range(10):
            x, y = gx0 + c * pitch + pitch / 2, gy0 + r * pitch + pitch / 2
            if (r, c) == hilang:
                hx, hy = x, y
                continue
            domba(bd, x * K, y * K, s * K, abu, kepala)
    domba(bd, hx * K, hy * K, s * K, campur(krem, aksen, 0.22), campur(krem, aksen, 0.35))  # bayang domba yang hilang
    # domba yang ditemukan
    fx = (kol_x[0] + kol_x[1]) / 2
    fy = gy0 + 6.6 * pitch
    domba(bd, fx * K, fy * K, s * 1.6 * K, aksen, (70, 50, 40))
    if not kiri:  # menghadap ke kanan tetap, tidak apa-apa; cerminkan supaya menghadap kawanan
        pass
    img.alpha_composite(big.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    # bekas tempat yang kosong
    kot = [(hx - pitch / 2 + 4, hy - pitch / 2 + 4), (hx + pitch / 2 - 4, hy - pitch / 2 + 4), (hx + pitch / 2 - 4, hy + pitch / 2 - 4),
           (hx - pitch / 2 + 4, hy + pitch / 2 - 4), (hx - pitch / 2 + 4, hy - pitch / 2 + 4)]
    garis_putus(d, kot, 6, 5, aksen, 2)
    # tongkat gembala
    tx, ty = fx + (40 if kiri else -40), gy0 + 1.0 * pitch
    lay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    hook = [(tx * K + 26 * K * math.cos(t), (ty + 26) * K - 26 * K * math.sin(t)) for t in np.linspace(math.pi, -0.15, 30)]
    ld.line([(tx * K - 26 * K, (ty + 26) * K), (tx * K - 26 * K, (ty + 190) * K)], fill=teks_c + (255,), width=6 * K)
    ld.line(hook, fill=teks_c + (255,), width=6 * K, joint="curve")
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    # panah putus-putus melengkung dari tongkat ke domba
    p0 = (tx - 26 + (24 if kiri else -24), ty + 160)
    p2 = (fx + (-34 if kiri else 34), fy - s * 0.55)
    p1 = (p0[0] + (70 if kiri else -70), (p0[1] + p2[1]) / 2 - 10)
    pts = kurva(p0, p1, p2, 30)
    garis_putus(d, pts, 10, 8, panah_c, 3)
    (ax_, ay_), (bx_, by_) = pts[-3], pts[-1]
    ang = math.atan2(by_ - ay_, bx_ - ax_)
    d.polygon([(bx_ + math.cos(ang) * 6, by_ + math.sin(ang) * 6), (bx_ - math.cos(ang - 0.5) * 18, by_ - math.sin(ang - 0.5) * 18),
               (bx_ - math.cos(ang + 0.5) * 18, by_ - math.sin(ang + 0.5) * 18)], fill=panah_c)
    lab = bersih(p["label"])
    fl = muat(d, lab, spidol, kol_x[1] - kol_x[0] - 10, 40)
    d.text((fx, fy + s * 0.95), lab, font=fl, fill=aksen, anchor="ma")
    tw = d.textlength(lab, font=fl)
    goresan(d, [(fx - tw / 2, fy + s * 0.95 + fl.size * 1.15), (fx + tw / 2 + 6, fy + s * 0.95 + fl.size * 1.1)], 3, aksen, rng, 0.8)
    d.text((gx0, gy0 + 10 * pitch + 12), "1 ikon = 1 domba", font=helv(18), fill=(130, 124, 118))
    d.text((gx0 + 10 * pitch, gy0 + 10 * pitch + 12), "99 + 1 = 100", font=helv(18, 1), fill=(130, 124, 118), anchor="ra")
    # ayat
    y0 = gy0 + 10 * pitch + 58
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s_: georgia(s_), W - 160, 1228 - y0 - 46, 30, 20, 1.36)
    for ln in lines:
        d.text((80, y0), ln, font=f_, fill=teks_c)
        y0 += size * 1.36
    d.text((80, y0 + 8), bersih(p["ref"]), font=georgia_b(26), fill=aksen)
    d.line((80, 1252, W - 80, 1252), fill=(214, 208, 198), width=1)
    d.text((80, 1266), bersih(p["sumber"]), font=helv(20), fill=(110, 104, 98))
    kredit(img, (W - 80, 1266), (110, 104, 98), anchor="ra", font=helv(20, 10))
    return img


# ---------- HURUF: spesimen huruf "nama kamu" ----------

HURUF_GAYA = [((248, 214, 72), lambda s: basker(s, 0)), ((244, 150, 124), lambda s: caslon(s)), ((150, 208, 190), lambda s: basker(s, 2))]


def huruf_image(p, i):
    aksen, fam = HURUF_GAYA[i % 3]
    hitam, putih, garis = (20, 20, 20), (252, 252, 250), (210, 210, 210)
    img = Image.new("RGBA", (W, H), putih + (255,))
    d = ImageDraw.Draw(img)
    YK = 500
    d.rectangle((0, 0, W, YK), fill=aksen)
    d.text((34, YK - 42), "Aa", font=fam(1000), fill=hitam, anchor="ls")
    img = grain(img.convert("RGB"), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((W - 70, YK + 34), "SPESIMEN HURUF", font=helv(16, 1), fill=hitam, anchor="ra")
    d.text((W - 70, YK + 58), p.get("_tanggal", ""), font=helv(16), fill=(110, 110, 110), anchor="ra")
    nama = bersih(p["nama"])
    judul = f"{nama} {['Regular', 'Regular', 'Italic'][i % 3]}"
    d.text((70, YK + 22), judul, font=muat(d, judul, fam, W - 140 - 230, 64), fill=hitam)
    d.line((70, YK + 116, W - 70, YK + 116), fill=garis, width=1)
    # metadata
    y = YK + 136
    for m in p["meta"][:3]:
        m = bersih(m)
        if ":" in m:
            lab, isi = [t.strip() for t in m.split(":", 1)]
        else:
            lab, isi = "", m
        if lab:
            d.text((70, y), lab.upper(), font=helv(14, 1), fill=(130, 130, 130))
            y += 22
        fi = menlo(18)
        lines = wrap(d, isi, fi, 250)
        if len(lines) > 2:
            fi = muat(d, isi, menlo, 500, 18)
            lines = wrap(d, isi, fi, 250)
        for ln in lines[:3]:
            d.text((70, y), ln, font=fi, fill=hitam)
            y += 24
        y += 18
    # kisi glif (huruf nama disorot)
    glif = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&?!"
    gx0, gy0, cs = 360, YK + 136, 50
    fg = fam(30)
    for k, ch in enumerate(glif):
        x, y_ = gx0 + (k % 13) * cs, gy0 + (k // 13) * cs
        if ch in nama:
            d.rectangle((x, y_, x + cs, y_ + cs), fill=campur(aksen, putih, 0.35))
        d.text((x + cs / 2, y_ + cs / 2 + 2), ch, font=fg, fill=hitam, anchor="mm")
    for k in range(14):
        d.line((gx0 + k * cs, gy0, gx0 + k * cs, gy0 + 5 * cs), fill=garis, width=1)
    for k in range(6):
        d.line((gx0, gy0 + k * cs, gx0 + 13 * cs, gy0 + k * cs), fill=garis, width=1)
    d.line((70, gy0 + 5 * cs + 22, W - 70, gy0 + 5 * cs + 22), fill=garis, width=1)
    # air terjun ukuran
    frasa = bersih(p["frasa"])
    ukuran = [64, 44, 30, 20]
    lebar = PROBE.textlength(frasa, font=fam(64))
    sk = min(1.0, (W - 70 - 130) / lebar)
    y = gy0 + 5 * cs + 40
    for u in ukuran:
        uu = max(12, int(u * sk)) if u == 64 else max(12, int(u * min(1.0, (W - 200) / PROBE.textlength(frasa, font=fam(u)))))
        f_ = fam(uu)
        d.text((70, y + uu * 0.62), f"{u}", font=helv(14), fill=(150, 150, 150), anchor="lm")
        d.text((130, y), frasa, font=f_, fill=hitam)
        y += uu * 1.3 + 6
    d.line((70, y + 8, W - 70, y + 8), fill=garis, width=1)
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s_: basker(s_, 2), W - 140, 1290 - (y + 26) - 30, 30, 18, 1.3)
    y += 24
    for ln in lines:
        d.text((70, y), ln, font=f_, fill=hitam)
        y += size * 1.3
    d.text((70, y + 6), ref_besar(p["ref"]), font=helv(18, 1), fill=hitam)
    kredit(img, (W - 70, y + 6), (120, 120, 120), anchor="ra", font=helv(18))
    return img


# ---------- SILSILAH: bagan silsilah ----------

SILSILAH_KERTAS = [(236, 226, 204), (232, 222, 196), (238, 230, 212)]


def kotak_nama(d, cx, cy, teks, font, isi, tinta, ganda=None, pad=26, h=None):
    w = d.textlength(teks, font=font) + 2 * pad
    h = h or font.size * 1.9
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rectangle((x0, y0, x1, y1), fill=isi, outline=ganda or tinta, width=3 if ganda else 2)
    d.rectangle((x0 + 5, y0 + 5, x1 - 5, y1 - 5), outline=tinta, width=1)
    d.text((cx, cy + 1), teks, font=font, fill=tinta, anchor="mm")
    return x0, y0, x1, y1


def silsilah_image(p, i):
    rng = np.random.default_rng(16800 + i)
    kertas_c = SILSILAH_KERTAS[i % 3]
    sepia, emas, segel, kotak_c = (90, 62, 40), (200, 160, 70), (180, 40, 40), (246, 238, 220)
    a = kertas_np(W, H, kertas_c, rng, 0.06)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = np.clip(np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * 1.7 - 0.45, 0, 1)
    a *= (1 - 0.22 * v)[..., None] * np.array([1.0, 0.97, 0.92])
    for _ in range(3):  # noda tua
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(60, 160)
        noda = np.exp(-(((xx - x) / r) ** 2 + ((yy - y) / r) ** 2))
        a *= (1 - 0.07 * noda)[..., None]
    img = grain(ke_img(a), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle((40, 40, W - 40, H - 40), outline=sepia, width=2)
    d.rectangle((50, 50, W - 50, H - 50), outline=sepia, width=1)
    for x, y in ((40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)):
        d.polygon([(x, y - 10), (x + 10, y), (x, y + 10), (x - 10, y)], fill=sepia)
    d.text((W / 2, 108), "Silsilah Keluarga Allah", font=snell(66), fill=sepia, anchor="ms")
    d.line((W / 2 - 200, 140, W / 2 - 16, 140), fill=sepia, width=1)
    d.line((W / 2 + 16, 140, W / 2 + 200, 140), fill=sepia, width=1)
    d.polygon([(W / 2, 133), (W / 2 + 7, 140), (W / 2, 147), (W / 2 - 7, 140)], fill=emas)
    # puncak & tengah
    pk = bersih(p["puncak"])
    b1 = kotak_nama(d, W / 2, 230, pk, iowan(40, 1), kotak_c, sepia, ganda=emas, pad=40, h=82)
    d.rectangle((b1[0] - 6, b1[1] - 6, b1[2] + 6, b1[3] + 6), outline=emas, width=2)
    tg = bersih(p["tengah"])
    b2 = kotak_nama(d, W / 2, 380, tg, muat(d, tg, lambda s: iowan(s), 560, 32), kotak_c, sepia, pad=30, h=70)
    d.line((W / 2, b1[3] + 6, W / 2, b2[1]), fill=sepia, width=2)
    # anggota
    nama = [bersih(n) for n in p["anggota"][:9]]
    sorot = bersih(p["sorot"])
    semua = nama + [sorot]
    fnm = iowan(26)
    lebar = [d.textlength(n, font=fnm) + 40 for n in semua]
    jarak = 22
    n1 = math.ceil(len(semua) / 2)
    baris = [list(range(n1)), list(range(n1, len(semua)))]
    while sum(lebar[k] for k in baris[0]) + jarak * (len(baris[0]) - 1) > W - 200 and fnm.size > 16:
        fnm = iowan(fnm.size - 1)
        lebar = [d.textlength(n, font=fnm) + 36 for n in semua]
    ys = [560, 700]
    pos = {}
    for r, idxs in enumerate(baris):
        tot = sum(lebar[k] for k in idxs) + jarak * (len(idxs) - 1)
        x = W / 2 - tot / 2
        for k in idxs:
            pos[k] = (x + lebar[k] / 2, ys[r])
            x += lebar[k] + jarak
    rel = min(pos[k][0] - lebar[k] / 2 for k in pos) - 30
    for r, idxs in enumerate(baris):
        bus = ys[r] - 54
        xs = [pos[k][0] for k in idxs]
        d.line((min(xs + [rel]), bus, max(xs), bus), fill=sepia, width=2)
        for k in idxs:
            d.line((pos[k][0], bus, pos[k][0], ys[r] - 30), fill=sepia, width=2)
    d.line((W / 2, b2[3], W / 2, ys[0] - 54), fill=sepia, width=2)
    d.line((rel, ys[0] - 54, rel, ys[1] - 54), fill=sepia, width=2)
    for k, n in enumerate(semua):
        cx, cy = pos[k]
        if k == len(semua) - 1:
            bb = kotak_nama(d, cx, cy, n, iowan(fnm.size, 1), (240, 214, 150), sepia, ganda=segel, pad=18, h=60)
            sx_, sy_ = bb[2], bb[3]
        else:
            kotak_nama(d, cx, cy, n, fnm, kotak_c, sepia, pad=18, h=60)
    # cap merah
    R = 92
    capm = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0))
    c0 = R + 20
    cd = ImageDraw.Draw(capm)
    cd.ellipse((c0 - R, c0 - R, c0 + R, c0 + R), outline=segel + (255,), width=6)
    cd.ellipse((c0 - R + 30, c0 - R + 30, c0 + R - 30, c0 + R - 30), outline=segel + (255,), width=2)
    cap = bersih(p["cap"]).upper()
    fc = gill(19, 1)
    while fc.getlength(cap) + 3 * len(cap) > 2 * math.pi * (R - 22) * 0.9 and fc.size > 11:
        fc = gill(fc.size - 1, 1)
    teks_lingkar(capm, c0, c0, R - 22, cap + " ·", fc, segel + (255,), start_deg=-90, tracking=3)
    cd.polygon([(c0 + (24 if k % 2 == 0 else 10) * math.sin(math.pi * k / 5), c0 - (24 if k % 2 == 0 else 10) * math.cos(math.pi * k / 5)) for k in range(10)], fill=segel + (255,))
    capm = capm.rotate(-12, resample=Image.BICUBIC)
    ca = np.asarray(capm.getchannel("A")).astype(np.float32)
    ca *= np.clip(0.55 + 0.6 * render.fbm2d(ca.shape[0], ca.shape[1], rng, ((6, 1.0), (30, 0.6))), 0, 1)
    ca[rng.random(ca.shape) < 0.04] *= 0.3
    capm.putalpha(ke_img(ca).convert("L"))
    ccx = min(W - 66 - R, sx_ - 30)  # cap di bawah kotak sorotan, tidak menutupi namanya
    comp(img, capm, (ccx - capm.width / 2, sy_ + 8 - 20))
    d = ImageDraw.Draw(img)
    # ayat
    y0, y1 = sy_ + 2 * R + 10, 1230
    f_, lines, size = pas_aman(d, bersih(p["ayat"]), lambda s: basker(s, 2), W - 220, y1 - y0 - 60, 36, 22, 1.36)
    y = y0 + max(0, (y1 - y0 - 60 - len(lines) * size * 1.36) / 2)
    for ln in lines:
        d.text((W / 2, y), ln, font=f_, fill=sepia, anchor="ma")
        y += size * 1.36
    d.text((W / 2, y + 14), ref_besar(p["ref"]), font=iowan(24, 1), fill=segel, anchor="ma")
    kredit(img, (W / 2, H - 98), campur(sepia, kertas_c, 0.3), font=iowan(20, 2))
    return img


# ---------- BATIK: kawung / ceplok + kartus ----------

BATIK_PAL = [  # latar, isi motif, dalam, aksen, garis retak, kartus
    ((70, 40, 22), (232, 212, 170), (150, 92, 46), (36, 46, 80), (50, 30, 18)),
    ((232, 212, 170), (150, 92, 46), (70, 40, 22), (36, 46, 80), (90, 56, 30)),
    ((36, 46, 80), (232, 212, 170), (150, 92, 46), (70, 40, 22), (24, 30, 56)),
]


def oval(cx, cy, panjang, lebar, sudut, rng, goyang=1.5, n=40):
    a = math.radians(sudut)
    pts = []
    for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
        x, y = panjang / 2 * math.cos(t), lebar / 2 * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a) + rng.uniform(-goyang, goyang), cy + x * math.sin(a) + y * math.cos(a) + rng.uniform(-goyang, goyang)))
    return pts


def motif_batik(motif, w, h, pal, rng, S=2):
    latar, isi, dalam, aksen, retak = pal
    img = Image.new("RGB", (w * S, h * S), latar)
    d = ImageDraw.Draw(img)
    P = 150 * S
    g = 1.5 * S
    if motif == "ceplok":
        for gy in range(-1, h * S // P + 2):
            for gx in range(-1, w * S // P + 2):
                cx, cy = gx * P + P / 2, gy * P + P / 2
                for k in range(8):  # kelopak
                    ang = k * 45
                    a = math.radians(ang)
                    d.polygon(oval(cx + math.cos(a) * 34 * S, cy + math.sin(a) * 34 * S, 52 * S, 24 * S, ang, rng, g, 24), fill=isi)
                    d.polygon(oval(cx + math.cos(a) * 36 * S, cy + math.sin(a) * 36 * S, 30 * S, 10 * S, ang, rng, g * 0.6, 20), fill=dalam)
                d.ellipse((cx - 17 * S, cy - 17 * S, cx + 17 * S, cy + 17 * S), fill=aksen, outline=isi, width=3 * S)
                d.ellipse((cx - 5 * S, cy - 5 * S, cx + 5 * S, cy + 5 * S), fill=isi)
                for qx, qy in ((cx + P / 2, cy + P / 2),):
                    d.polygon([(qx, qy - 22 * S), (qx + 22 * S, qy), (qx, qy + 22 * S), (qx - 22 * S, qy)], fill=dalam)
                    d.polygon([(qx, qy - 11 * S), (qx + 11 * S, qy), (qx, qy + 11 * S), (qx - 11 * S, qy)], fill=aksen)
                for qx, qy in ((cx + P / 2, cy), (cx, cy + P / 2)):
                    for o in (-1, 1):
                        d.ellipse((qx + o * 8 * S - 3 * S, qy - 3 * S, qx + o * 8 * S + 3 * S, qy + 3 * S), fill=isi)
                        d.ellipse((qx - 3 * S, qy + o * 8 * S - 3 * S, qx + 3 * S, qy + o * 8 * S + 3 * S), fill=isi)
    else:  # kawung: empat oval di diagonal tiap titik kisi
        rc = P * math.sqrt(2) / 4
        for gy in range(-1, h * S // P + 2):
            for gx in range(-1, w * S // P + 2):
                cx, cy = gx * P, gy * P
                for ang in (45, 135, 225, 315):
                    a = math.radians(ang)
                    ox, oy = cx + math.cos(a) * rc, cy + math.sin(a) * rc
                    d.polygon(oval(ox, oy, 100 * S, 60 * S, ang, rng, g), fill=isi)
                    d.line(oval(ox, oy, 84 * S, 46 * S, ang, rng, g * 0.7) + [oval(ox, oy, 84 * S, 46 * S, ang, rng, 0)[0]], fill=dalam, width=2 * S)
                    d.polygon(oval(ox + math.cos(a) * 6 * S, oy + math.sin(a) * 6 * S, 50 * S, 26 * S, ang, rng, g * 0.7), fill=dalam)
                    d.ellipse((ox + math.cos(a) * 8 * S - 4 * S, oy + math.sin(a) * 8 * S - 4 * S, ox + math.cos(a) * 8 * S + 4 * S, oy + math.sin(a) * 8 * S + 4 * S), fill=isi)
                d.ellipse((cx - 11 * S, cy - 11 * S, cx + 11 * S, cy + 11 * S), fill=aksen, outline=isi, width=2 * S)
                for qx, qy in ((cx + P / 2, cy), (cx, cy + P / 2)):  # isen di celah belah ketupat
                    d.polygon([(qx, qy - 13 * S), (qx + 13 * S, qy), (qx, qy + 13 * S), (qx - 13 * S, qy)], fill=aksen)
                    for o in (-1, 1):
                        d.ellipse((qx + o * 24 * S - 3 * S, qy - 3 * S, qx + o * 24 * S + 3 * S, qy + 3 * S), fill=isi)
                        d.ellipse((qx - 3 * S, qy + o * 24 * S - 3 * S, qx + 3 * S, qy + o * 24 * S + 3 * S), fill=isi)
    img = img.resize((w, h), Image.LANCZOS)
    a = np.asarray(img).astype(np.float32)
    # retak lilin (hanya di bagian terang)
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    # retak lilin: jaring garis tipis bersudut (tepi sel Voronoi), terputus-putus, hanya di bagian terang
    seed_r = int(rng.integers(1 << 30))
    ret = kaustik(w, h, seed_r, sel=110, tebal=0.022, turun=1, lengkung=0.3)
    ret = np.maximum(ret, kaustik(w, h, seed_r + 1, sel=240, tebal=0.014, turun=1, lengkung=0.3))
    ret *= np.clip((render.fbm2d(h, w, rng, ((3, 1.0), (7, 0.5))) - 0.42) / 0.08, 0, 1)
    ret *= np.clip((lum - 110) / 40, 0, 1) * 0.45
    a = a * (1 - ret[..., None]) + np.array(retak, np.float32) * ret[..., None]
    xx = np.arange(w)[None, :]
    yy = np.arange(h)[:, None]
    a *= (0.95 + 0.05 * np.sin(1.3 * xx) * np.sin(1.3 * yy))[..., None]
    a *= (0.92 + 0.12 * render.fbm2d(h, w, rng, ((3, 1.0), (9, 0.5), (30, 0.3))))[..., None]
    return grain(ke_img(a), 0.04)


def batik_image(p, i):
    rng = np.random.default_rng(16900 + i)
    pal = BATIK_PAL[i % 3]
    motif = "ceplok" if re.search("ceplok", bersih(p.get("motif", "kawung")), re.I) else "kawung"
    img = motif_batik(motif, W, H, pal, rng).convert("RGBA")
    krem, soga, tua, indigo = (246, 236, 212), (150, 92, 46), (62, 38, 24), (36, 46, 80)
    probe = ImageDraw.Draw(img)
    kw = 780
    f_, lines, size = pas_aman(probe, bersih(p["ayat"]), lambda s: charter(s), kw - 140, 330, 34, 22, 1.36)
    kh = int(70 + 30 + 60 + 50 + len(lines) * size * 1.36 + 60 + 70)
    kh = max(kh, 600)
    kx, ky = (W - kw) // 2, (H - kh) // 2
    kar = ke_img(kertas_np(kw, kh, krem, rng, 0.03)).convert("RGBA")
    m = Image.new("L", (kw * 3, kh * 3), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, kw * 3 - 1, kh * 3 - 1), radius=60 * 3, fill=255)
    kar.putalpha(m.resize((kw, kh), Image.LANCZOS))
    kd = ImageDraw.Draw(kar)
    kd.rounded_rectangle((14, 14, kw - 15, kh - 15), radius=48, outline=soga, width=4)
    kd.rounded_rectangle((24, 24, kw - 25, kh - 25), radius=40, outline=indigo, width=1)
    lab = "motif " + motif
    renggang(kd, (kw / 2, 66), lab.upper(), gill(18, 4), soga, 4, anchor="ma")
    judul = bersih(p["judul"])
    fj = muat(kd, judul, lambda s: iowan(s, 2), kw - 140, 54)
    kd.text((kw / 2, 100), judul, font=fj, fill=tua, anchor="ma")
    y = 100 + fj.size * 1.25 + 8
    kd.line((kw / 2 - 120, y, kw / 2 - 18, y), fill=soga, width=2)
    kd.line((kw / 2 + 18, y, kw / 2 + 120, y), fill=soga, width=2)
    for ox, oy in ((-8, 0), (8, 0), (0, -8), (0, 8)):  # kawung mini
        kd.ellipse((kw / 2 + ox - 5, y + oy - 5, kw / 2 + ox + 5, y + oy + 5), fill=soga)
    y += 40
    tinggi_ayat = len(lines) * size * 1.36
    sisa = kh - 70 - y - 60
    y += max(0, (sisa - tinggi_ayat) / 2)
    for ln in lines:
        kd.text((kw / 2, y), ln, font=f_, fill=tua, anchor="ma")
        y += size * 1.36
    renggang(kd, (kw / 2, y + 16), ref_besar(p["ref"]), gill(22, 4), soga, 3, anchor="ma")
    kd.text((kw / 2, kh - 62), "@" + HANDLE, font=gill(18), fill=campur(soga, krem, 0.3), anchor="ma")
    bayangan(img, kar, (kx, ky), blur=22, geser=(0, 14), kuat=0.5)
    return img


# ---------- MARMER: kertas marmer bersisir ----------

MARMER_PAL = [
    [((24, 52, 110), 24), ((40, 130, 140), 18), ((240, 240, 232), 12), ((24, 52, 110), 14), ((40, 130, 140), 10), ((240, 240, 232), 7), ((210, 170, 80), 3)],
    [((22, 40, 86), 22), ((150, 52, 58), 16), ((240, 234, 220), 12), ((22, 40, 86), 12), ((60, 120, 150), 12), ((240, 234, 220), 7), ((210, 170, 80), 3)],
    [((22, 70, 72), 22), ((60, 140, 120), 16), ((238, 238, 226), 12), ((30, 60, 100), 14), ((60, 140, 120), 10), ((238, 238, 226), 7), ((210, 170, 80), 3)],
]


def marmer_latar(w, h, seed, pal):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tine_jarak = 120
    k0 = np.floor(yy / tine_jarak)
    tarik = np.zeros_like(yy)
    for k in (k0, k0 + 1):  # dua garu terdekat dijumlahkan supaya tidak ada sambungan
        tarik += np.where(k % 2 == 0, 1.0, -1.0) * 80 * np.exp(-np.abs(yy - k * tine_jarak) / 30)
    x1 = xx - tarik                                              # 3. tarik garu tiap 120 px
    y2 = yy - 35 * np.sin(x1 / 28)                              # 2. sisir
    x3 = x1 - 60 * np.sin(y2 / 90)                              # 1. gelombang besar
    fb = render.fbm2d(h, w, rng, ((3, 1.0), (7, 0.5), (16, 0.25)))
    xi = np.clip(x3.astype(np.int32), 0, w - 1)
    yi = np.clip(y2.astype(np.int32), 0, h - 1)
    v = y2 + 40 * (fb[yi, xi] - 0.5) * 2
    lebar = np.array([wd for _, wd in pal], np.float32) * 0.55
    batas = np.cumsum(lebar)
    per = batas[-1]
    idx = np.searchsorted(batas, np.mod(v, per), side="right")
    idx = np.clip(idx, 0, len(pal) - 1)
    warna = np.array([c for c, _ in pal], np.float32)
    a = warna[idx]
    img = ke_img(a).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(img).astype(np.float32)
    a *= (0.95 + 0.08 * render.fbm2d(h, w, rng, ((2, 1.0), (6, 0.5))))[..., None]
    return grain(ke_img(a), 0.03)


def marmer_image(p, i):
    rng = np.random.default_rng(17000 + i)
    img = marmer_latar(W, H, 17000 + i, MARMER_PAL[i % 3]).convert("RGBA")
    label_c, tinta = (246, 240, 226), (30, 30, 40)
    probe = ImageDraw.Draw(img)
    lw = 720
    f_, lines, size = pas_aman(probe, bersih(p["ayat"]), lambda s: basker(s), lw - 150, 360, 34, 22, 1.36)
    lh = int(90 + 60 + 40 + len(lines) * size * 1.36 + 60 + 80)
    lh = max(lh, 520)
    lab = ke_img(kertas_np(lw, lh, label_c, rng, 0.03)).convert("RGBA")
    c = 34
    m = Image.new("L", (lw, lh), 0)
    ImageDraw.Draw(m).polygon([(c, 0), (lw - c, 0), (lw, c), (lw, lh - c), (lw - c, lh), (c, lh), (0, lh - c), (0, c)], fill=255)
    lab.putalpha(m)
    ld = ImageDraw.Draw(lab)
    for o, wd in ((16, 3), (24, 1)):
        cc = c + o * 0.4
        ld.polygon([(cc, o), (lw - cc, o), (lw - o, cc), (lw - o, lh - cc), (lw - cc, lh - o), (cc, lh - o), (o, lh - cc), (o, cc)], outline=tinta, width=wd)
    judul = bersih(p["judul"])
    fj = muat(ld, judul, lambda s: basker(s, 2), lw - 140, 46)
    ld.text((lw / 2, 74), judul, font=fj, fill=tinta, anchor="ma")
    y = 74 + fj.size * 1.3
    ld.line((lw / 2 - 60, y, lw / 2 + 60, y), fill=(160, 130, 70), width=2)
    y += 30
    sisa = lh - 80 - y - 60
    y += max(0, (sisa - len(lines) * size * 1.36) / 2)
    for ln in lines:
        ld.text((lw / 2, y), ln, font=f_, fill=tinta, anchor="ma")
        y += size * 1.36
    renggang(ld, (lw / 2, y + 16), ref_besar(p["ref"]), basker(22, 4), (120, 90, 40), 3, anchor="ma")
    ld.text((lw / 2, lh - 56), "@" + HANDLE, font=basker(19, 2), fill=(120, 116, 110), anchor="ma")
    bayangan(img, lab, ((W - lw) // 2, (H - lh) // 2), blur=18, geser=(0, 12), kuat=0.5)
    return img


# ---------- RIAK (Reels): tetes air, riak membawa suara Bapa ----------

def tetes_sprite(r=16):
    def gambar(d, k):
        R = r * k
        cx, cy = R * 1.2, R * 2.4
        d.polygon([(cx, 0), (cx + R * 0.95, cy - R * 0.3), (cx - R * 0.95, cy - R * 0.3)], fill=(196, 236, 240, 235))
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(196, 236, 240, 235))
        d.ellipse((cx - R * 0.55, cy - R * 0.6, cx - R * 0.1, cy - R * 0.05), fill=(255, 255, 255, 230))
    return sprite(int(r * 2.4), int(r * 3.5), gambar)


RIAK_PAL = [((12, 40, 52), (20, 64, 78)), ((10, 34, 58), (22, 58, 86)), ((12, 42, 46), (22, 70, 72))]


def riak_reel(p, idx, mod=MOD, seconds=11):
    rel = f"reels/{mod}/riak{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    cx, cy = RW / 2, 760.0
    hw, hh = RW // 2, RH // 2
    yy, xx = np.mgrid[0:hh, 0:hw].astype(np.float32)
    X, Y = xx * 2, yy * 2
    R = np.hypot(X - cx, Y - cy)
    top, bot = RIAK_PAL[idx % 3]
    ty = (Y / RH)[..., None]
    dasar = np.array(top, np.float32) * (1 - ty) + np.array(bot, np.float32) * ty
    vig = 1 - 0.4 * np.clip(np.hypot((X - RW / 2) / RW, (Y - RH * 0.42) / RH) * 1.7 - 0.3, 0, 1)
    dasar = dasar * vig[..., None]
    # kaustik: dua tekstur jaring cahaya, digoyang medan sinus yang bergerak (seperti cahaya di dasar air)
    K0 = kaustik(hw, hh, 17150 + idx, sel=75, tebal=0.07, turun=2)
    K1 = kaustik(hw, hh, 17160 + idx, sel=55, tebal=0.07, turun=2)
    xi0, yi0 = xx.astype(np.int32), yy.astype(np.int32)
    sorot = np.array([0.80, 0.96, 0.96], np.float32)
    T_CINCIN = [1.8 + 0.5 * k for k in range(6)]
    V, LB = 290.0, 15.0
    kata = [bersih(k) for k in p["kata"][:4]]
    RK = [150, 250, 350, 450]
    T_KATA = [2.4, 3.0, 3.6, 4.2]
    fonts = []
    for k, kt in enumerate(kata):
        f = iowan(56 + 6 * k, 2)
        while f.getlength(kt) / RK[k] > 2.3 and f.size > 28:
            f = iowan(f.size - 2, 2)
        fonts.append(f)
    putih = (250, 246, 230, 255)
    # kicker
    kick = bersih(p["kicker"]).upper()
    kl = Image.new("RGBA", (RW, 90), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kl)
    fk = gill(30, 4)
    while lebar_renggang(kd, kick, fk, 6) > RW - 180 and fk.size > 18:
        fk = gill(fk.size - 1, 4)
    renggang(kd, (RW / 2, 20), kick, fk, (200, 236, 232, 255), 6, anchor="ma")
    kd.line((RW / 2 - 40, 74, RW / 2 + 40, 74), fill=(200, 236, 232, 160), width=2)
    # ayat
    f_, vl, vs = pas_aman(PROBE, tanpa_kutip(p["ayat"]), lambda s: iowan(s, 2), RW - 220, 470, 56, 32, 1.32)
    ah = int(len(vl) * vs * 1.32 + 110)
    ayat = Image.new("RGBA", (RW, ah + 160), (0, 0, 0, 0))
    bk = Image.new("RGBA", ayat.size, (0, 0, 0, 0))
    ImageDraw.Draw(bk).ellipse((40, 30, RW - 40, ah + 130), fill=(4, 18, 26, 150))
    ayat.alpha_composite(bk.filter(ImageFilter.GaussianBlur(50)))
    ad = ImageDraw.Draw(ayat)
    y = 80
    for ln in vl:
        ad.text((RW / 2, y), ln, font=f_, fill=putih, anchor="ma")
        y += vs * 1.32
    renggang(ad, (RW / 2, y + 22), ref_besar(p["ref"]), gill(28, 4), (200, 236, 232, 255), 4, anchor="ma")
    ay0 = int(960 - ayat.height / 2)
    tetes = tetes_sprite(15)
    kred = Image.new("RGBA", (RW, 50), (0, 0, 0, 0))
    ImageDraw.Draw(kred).text((RW / 2, 10), "@" + HANDLE, font=gill(26), fill=(200, 236, 232, 170), anchor="ma")

    def frame(t, sampul=False):
        tenang = 1.0 - 0.85 * ease((t - 6.0) / 2.5)
        gx = 4 * np.sin(yy * 0.045 + t * 1.3) + 3 * np.sin(xx * 0.03 - t * 0.8)
        gy = 4 * np.sin(xx * 0.04 - t * 1.1) + 3 * np.sin(yy * 0.025 + t * 0.7)
        xa = np.clip(xi0 + gx.astype(np.int32), 0, hw - 1)
        ya = np.clip(yi0 + gy.astype(np.int32), 0, hh - 1)
        xb = np.clip(xi0 - gy.astype(np.int32), 0, hw - 1)
        yb = np.clip(yi0 + gx.astype(np.int32), 0, hh - 1)
        kaus = 0.65 * K0[ya, xa] + 0.45 * K1[yb, xb]
        Sx = np.zeros_like(R)
        for k, t0 in enumerate(T_CINCIN):
            u = t - t0
            if u <= 0:
                continue
            r = V * u
            dec = math.exp(-r / 820) * min(1.0, u / 0.15) * tenang * (0.88 ** k)
            if dec < 0.01:
                continue
            Sx += (np.exp(-((R - r) / LB) ** 2) - 0.5 * np.exp(-((R - r + 2.2 * LB) / (1.4 * LB)) ** 2)) * dec
        if 1.5 <= t < 2.6:  # gangguan di tengah setelah tetes
            u = (t - 1.5) / 1.1
            Sx += np.exp(-(R / (30 + 60 * u)) ** 2) * (1 - u) * 0.8
        a = dasar + (60 * Sx + 22 * kaus * (0.7 + 0.3 * tenang))[..., None] * sorot
        img = ke_img(a).resize((RW, RH), Image.BILINEAR).convert("RGBA")
        lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        if 0.9 <= t < 1.5:  # tetes jatuh makin cepat
            u = (t - 0.9) / 0.6
            ty_ = 300 + (cy - 300) * u * u
            sk = 1 - 0.35 * u
            ts = tetes.resize((max(2, int(tetes.width * sk)), max(2, int(tetes.height * sk))), Image.LANCZOS)
            rr = 10 + 30 * u
            ld.ellipse((cx - rr, cy - rr * 0.6, cx + rr, cy + rr * 0.6), fill=(0, 10, 16, int(60 * u)))
            lay.alpha_composite(ts, (int(cx - ts.width / 2), int(ty_ - ts.height)))
        if 1.5 <= t < 1.9:  # percikan
            u = (t - 1.5) / 0.4
            for k in range(16):
                ang = 2 * math.pi * k / 16
                rr = 18 + 110 * ease(u)
                pr = 6 * (1 - u) + 2
                px, py = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * 0.9
                ld.ellipse((px - pr, py - pr, px + pr, py + pr), fill=(220, 248, 248, int(230 * (1 - u))))
            fl = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
            ImageDraw.Draw(fl).ellipse((100, 100, 300, 300), fill=(230, 255, 255, int(200 * (1 - u))))
            lay.alpha_composite(fl.filter(ImageFilter.GaussianBlur(40)), (int(cx - 200), int(cy - 200)))
        img.alpha_composite(lay)
        # kata-kata di cincin
        for k, kt in enumerate(kata):
            if sampul:
                al, settle = 1.0, 1.0
            else:
                al = ease((t - T_KATA[k]) / 0.5) * (1 - ease((t - 5.8) / 0.5))
                settle = ease((t - T_KATA[k]) / 0.7)
            if al <= 0.01:
                continue
            r = RK[k] - 18 * (1 - settle)
            gl = Image.new("RGBA", (2 * RK[k] + 8, RK[k] + 8), (0, 0, 0, 0))
            ImageDraw.Draw(gl).arc((4, -RK[k] + 4, 2 * RK[k] + 4, RK[k] + 4), 8, 172, fill=(200, 240, 240, int(80 * al)), width=2)
            img.alpha_composite(gl, (int(cx - RK[k] - 4), int(cy - 4)))
            drift = (1 if k % 2 == 0 else -1) * 1.5 * max(0.0, (t if not sampul else 4.9) - T_KATA[k])
            naik = fonts[k].getbbox("Ak")[3] - fonts[k].getbbox("Ak")[1]
            teks_lingkar(img, cx, cy, r + naik + 8, kt, fonts[k], putih, start_deg=90 + drift, arah=-1, tracking=1.5, alpha=al)
        if sampul or t >= 0.2:
            img.alpha_composite(kl if sampul else fade(kl, ease((t - 0.2) / 0.6)), (0, 410))
        if not sampul and t >= 6.2:
            img.alpha_composite(fade(ayat, ease((t - 6.2) / 0.8)), (0, ay0))
        img.alpha_composite(kred, (0, 1470))
        return img

    sampul = frame(4.9, sampul=True)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(int(seconds * FPS)):
        t = n / FPS
        fr = sampul if t < 0.4 else frame(t - 0.4)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- WARNAI (Reels): mewarnai menurut nomor ----------

WARNAI_PAL = [(243, 226, 188), (244, 150, 70), (200, 90, 60), (140, 170, 120), (90, 140, 190), (236, 190, 80)]


def peta_wilayah(cw, ch, seed):
    """Peta label matahari terbit -> (label HxW, warna per label (1..6), titik nomor, urutan isi)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    sx, sy, sr = cw * [0.5, 0.38, 0.62][seed % 3], ch * 0.5, 96
    Rs = np.hypot(xx - sx, yy - sy)
    f1, f2, f3 = rng.uniform(0, 2 * math.pi, 3)
    b1 = yy > ch * 0.6 + 30 * np.sin(xx / 150 + f1) + 16 * np.sin(xx / 61)
    b2 = yy > ch * 0.73 + 40 * np.sin(xx / 190 + f2) + 12 * np.sin(xx / 47 + 2)
    b3 = yy > ch * 0.87 + 24 * np.sin(xx / 110 + f3)
    y0 = ch * 0.64
    xr = cw * 0.52 + 70 * np.sin(yy / 75) * np.clip((yy - y0) / (ch - y0), 0, 1)
    wr = 6 + 0.42 * (yy - y0)
    sungai = b1 & (yy > y0) & (np.abs(xx - xr) < wr)
    lab = np.zeros((ch, cw), np.int32)
    # langit: cincin x Voronoi 8 titik
    seeds = np.stack([rng.uniform(0, cw, 10), rng.uniform(0, ch * 0.62, 10)], 1)
    dmin = np.full((ch, cw), 1e9, np.float32)
    sel = np.zeros((ch, cw), np.int32)
    for k, (qx, qy) in enumerate(seeds):
        dd = (xx - qx) ** 2 + (yy - qy) ** 2
        sel = np.where(dd < dmin, k, sel)
        dmin = np.minimum(dmin, dd)
    ring = np.floor((Rs - sr) / 96).astype(np.int32)
    lab = 100 + ring * 16 + sel
    lab = np.where(Rs < sr, 1, lab)
    lab = np.where(b1 & ~b2, np.where(xx < cw * 0.42 + 30 * np.sin(yy / 40), 2, 3), lab)
    lab = np.where(b2 & ~b3, np.where(xx < cw * 0.62, 4, 5), lab)
    lab = np.where(b3, 6, lab)
    lab = np.where(sungai, np.where(yy < ch * 0.8, 7, 8), lab)
    # gabungkan wilayah kecil ke tetangganya
    for _ in range(4):
        ids, cnt = np.unique(lab, return_counts=True)
        kecil = [k for k, c in zip(ids, cnt) if c < 2200 and k != 1]
        if not kecil:
            break
        for k in kecil:
            m = lab == k
            if not m.any():
                continue
            mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
            tepi = (np.asarray(mi) > 0) & ~m
            tet = lab[tepi]
            tet = tet[tet != k]
            if len(tet):
                v, c = np.unique(tet, return_counts=True)
                lab[m] = v[np.argmax(c)]
    # pisahkan wilayah yang terbelah jadi beberapa pulau tidak perlu; susun ulang label
    ids = np.unique(lab)
    peta = {k: n for n, k in enumerate(ids)}
    lab2 = np.vectorize(peta.get)(lab).astype(np.int32)
    warna, titik, urut = {}, {}, []
    for k, n in peta.items():
        m = lab2 == n
        ys_, xs_ = np.nonzero(m)
        if k == 1:
            c = 6
        elif k in (2, 3):
            c = 4 if k == 2 else 3
        elif k in (4, 5):
            c = 3 if k == 4 else 2
        elif k == 6:
            c = 4
        elif k in (7, 8):
            c = 5
        else:
            rg, sl = (k - 100) // 16, (k - 100) % 16
            c = (2 if (rg + sl) % 2 == 0 else 1) if rg < 2 else (5 if (rg + sl) % 2 == 0 else 1)
        warna[n] = c
        # titik nomor: kikis berulang sampai hampir habis
        y0_, y1_, x0_, x1_ = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
        mm = Image.fromarray((m[y0_:y1_, x0_:x1_] * 255).astype(np.uint8))
        akhir = mm
        for _ in range(60):
            mm = mm.filter(ImageFilter.MinFilter(5))
            if not np.asarray(mm).any():
                break
            akhir = mm
        ay, ax = np.nonzero(np.asarray(akhir))
        my, mx = ay.mean(), ax.mean()
        j = np.argmin((ay - my) ** 2 + (ax - mx) ** 2)
        titik[n] = (x0_ + ax[j], y0_ + ay[j])
        grup = 0 if k in (6, 7, 8) else (1 if k in (4, 5) else (2 if k in (2, 3) else (4 if k == 1 else 3)))
        urut.append((grup, -float(np.hypot(titik[n][0] - sx, titik[n][1] - sy)), n))
    urut = [n for _, _, n in sorted(urut)]
    return lab2, warna, titik, urut


def centang(d, x, y, s, col, u=1.0):
    """Tanda centang digambar sebagai garis (u = progres 0..1)."""
    pts = [(x - s * 0.5, y), (x - s * 0.12, y + s * 0.38), (x + s * 0.55, y - s * 0.42)]
    L1 = math.dist(pts[0], pts[1])
    L2 = math.dist(pts[1], pts[2])
    tot = (L1 + L2) * u
    if tot <= 0:
        return
    if tot <= L1:
        q = (pts[0][0] + (pts[1][0] - pts[0][0]) * tot / L1, pts[0][1] + (pts[1][1] - pts[0][1]) * tot / L1)
        d.line([pts[0], q], fill=col, width=int(s * 0.16))
    else:
        r = (tot - L1) / L2
        q = (pts[1][0] + (pts[2][0] - pts[1][0]) * r, pts[1][1] + (pts[2][1] - pts[1][1]) * r)
        d.line([pts[0], pts[1], q], fill=col, width=int(s * 0.16), joint="curve")


def warnai_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/warnai{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(17200 + idx)
    cw, ch = 900, 790
    CX, CY = 90, 520
    lab, warna, titik, urut = peta_wilayah(cw, ch, 17250 + idx)
    N = lab.max() + 1
    matahari = [n for n in range(N) if warna[n] == 6][0]
    urut = [n for n in urut if n != matahari] + [matahari]
    kertas_c = np.array([255, 255, 254], np.float32)
    garis_c = np.array([96, 86, 78], np.float32)
    ol = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
    ol[0, :] = ol[:, 0] = False
    ol = np.asarray(Image.fromarray((ol * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
    oy, ox = np.nonzero(ol)
    kuas = render.fbm2d(ch, cw, rng, ((3, 1.0), (40, 0.5), (160, 0.4)))
    gores = np.asarray(Image.fromarray((rng.random((ch // 6, cw // 40)) * 255).astype(np.uint8)).resize((cw, ch), Image.BICUBIC)).astype(np.float32) / 255
    shade = (0.9 + 0.09 * kuas + 0.05 * gores)[..., None]
    pal = np.array(WARNAI_PAL, np.float32)
    piks = {}
    for n in range(N):
        ys_, xs_ = np.nonzero(lab == n)
        tx, ty = titik[n]
        dist = np.hypot(xs_ - tx, ys_ - ty) + rng.uniform(0, 14, len(xs_))
        piks[n] = (ys_, xs_, dist, dist.max() + 2)
    t_mulai, t_akhir = 1.3, 9.3
    jadwal = {n: t_mulai + k * (t_akhir - t_mulai) / max(1, len(urut) - 2) for k, n in enumerate(urut[:-1])}
    jadwal[matahari] = 12.5
    DUR = 0.75
    selesai_warna = {}
    for c in range(1, 7):
        ns = [n for n in range(N) if warna[n] == c]
        selesai_warna[c] = max(jadwal[n] for n in ns) + DUR if ns else 0.0
    # sprite nomor
    fnum = avenir(24, 5)
    nomor = {}
    for n in range(N):
        s_ = Image.new("RGBA", (44, 40), (0, 0, 0, 0))
        ImageDraw.Draw(s_).text((22, 20), str(warna[n]), font=fnum, fill=(120, 108, 98, 255), anchor="mm")
        nomor[n] = s_
    # latar & lembar
    atas, bawah = [((238, 226, 204), (226, 212, 188)), ((222, 230, 218), (204, 216, 200)), ((240, 224, 214), (226, 204, 192))][idx % 3]
    bg = grain(gradasi(RW, RH, atas, bawah), 0.04).convert("RGBA")
    d = ImageDraw.Draw(bg)
    judul = bersih(p["judul"])
    fj = muat(d, judul, lambda s: bulat(s, "Bold"), RW - 160, 76)
    d.text((RW / 2, 456), judul, font=fj, fill=(200, 90, 60), anchor="ms")
    lembar = Image.new("RGBA", (940, 970), (255, 253, 249, 255))
    bayangan(bg, lembar, (70, 500), blur=16, geser=(0, 10), kuat=0.25)
    d = ImageDraw.Draw(bg)
    d.rectangle((CX - 2, CY - 2, CX + cw + 1, CY + ch + 1), outline=(96, 86, 78), width=2)
    kred = Image.new("RGBA", (RW, 40), (0, 0, 0, 0))
    ImageDraw.Draw(kred).text((RW / 2, 4), "@" + HANDLE, font=avenir(24, 5), fill=(150, 130, 110, 255), anchor="ma")
    # chip palet
    palet = [bersih(t) for t in p["palet"][:6]]
    chip_y = 1388

    def chips(t, alpha=1.0):
        lay = Image.new("RGBA", (RW, 120), (0, 0, 0, 0))
        cd = ImageDraw.Draw(lay)
        for k in range(6):
            x = 90 + 150 * k + 75
            col = WARNAI_PAL[k]
            cd.ellipse((x - 28, 6, x + 28, 62), fill=col + (255,), outline=(96, 86, 78, 255), width=2)
            cd.text((x, 34), str(k + 1), font=avenir(24, 2), fill=(70, 60, 54, 255) if k in (0, 5) else (255, 255, 255, 255), anchor="mm")
            nm = palet[k] if k < len(palet) else ""
            cd.text((x, 72), nm, font=muat(cd, nm, lambda s: avenir(s, 5), 140, 22), fill=(90, 80, 72, 255), anchor="ma")
            u = (t - selesai_warna[k + 1]) / 0.35
            if u > 0:
                centang(cd, x + 26, 18, 30, (60, 140, 80, 255), min(1.0, u))
        return fade(lay, alpha) if alpha < 1 else lay
    # panel ayat
    f_, vl, vs = pas_aman(PROBE, bersih(p["ayat"]), lambda s: iowan(s), 800, 300, 38, 24, 1.34)
    ph = int(len(vl) * vs * 1.34 + 140)
    panel = Image.new("RGBA", (920, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((0, 0, 919, ph - 1), radius=28, fill=(255, 250, 240, 242), outline=(200, 90, 60, 255), width=3)
    y = 40
    for ln in vl:
        pd.text((460, y), ln, font=f_, fill=(60, 50, 44, 255), anchor="ma")
        y += vs * 1.34
    pd.text((460, y + 16), ref_besar(p["ref"]), font=avenir(28, 2), fill=(200, 90, 60, 255), anchor="ma")
    panel_y = min(1470 - ph, 1080)

    def kanvas(t, st):
        """st: dict(arr, isi, n) -> kanvas pada waktu t (isi wilayah berurutan, bertambah saja)."""
        for n in urut:
            u = (t - jadwal[n]) / DUR
            if u <= 0:
                continue
            ys_, xs_, dist, dmax = piks[n]
            r = ease(min(1.0, u)) * dmax
            if st["r"].get(n, -1) >= r:
                continue
            m = dist <= r
            st["arr"][ys_[m], xs_[m]] = pal[warna[n] - 1] * shade[ys_[m], xs_[m]]
            st["isi"][ys_[m], xs_[m]] = True
            st["r"][n] = r
        a = st["arr"].copy()
        f = np.where(st["isi"][oy, ox], 0.6, 0.0)[:, None]
        a[oy, ox] = a[oy, ox] * f + garis_c * (1 - f)
        return ke_img(a)

    def baru():
        return {"arr": np.broadcast_to(kertas_c, (ch, cw, 3)).copy(), "isi": np.zeros((ch, cw), bool), "r": {}}

    def frame(t, st, sampul=False):
        img = bg.copy()
        kv = kanvas(t, st).convert("RGBA")
        if t < 1.3 and not sampul:
            kv = Image.blend(Image.new("RGBA", kv.size, (255, 255, 254, 255)), kv, ease(t / 1.2))
        img.alpha_composite(kv, (CX, CY))
        for n in range(N):
            u = (t - jadwal[n]) / DUR
            if u >= 0.35:
                continue
            al = (1 - max(0.0, u) / 0.35) * (1.0 if sampul else ease(t / 1.2))
            tx, ty = titik[n]
            sp = nomor[n]
            if n == matahari and 9.6 <= t < 12.5:
                s_ = 1 + 0.35 * abs(math.sin((t - 9.6) * math.pi * 1.6))
                sp = sp.resize((int(44 * s_), int(40 * s_)), Image.LANCZOS)
                halo = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
                ImageDraw.Draw(halo).ellipse((20, 20, 100, 100), fill=(236, 190, 80, int(120 * abs(math.sin((t - 9.6) * math.pi * 1.6)))))
                img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(10)), (int(CX + tx - 60), int(CY + ty - 60)))
            img.alpha_composite(fade(sp, al), (int(CX + tx - sp.width / 2), int(CY + ty - sp.height / 2)))
        if sampul:
            img.alpha_composite(chips(t), (0, chip_y))
        else:
            img.alpha_composite(chips(t, 1 - ease((t - 10.4) / 0.4)), (0, chip_y))
            if t >= 10.6:
                img.alpha_composite(fade(panel, ease((t - 10.6) / 0.8)), (80, panel_y))
            if t >= 13.1:  # kilau kecil
                u = (t - 13.1) / 0.6
                lay = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
                ld = ImageDraw.Draw(lay)
                tx, ty = titik[matahari]
                for k, (dx, dy, rr) in enumerate(((-120, -80, 26), (110, -110, 20), (140, 10, 16), (-150, 20, 14))):
                    s_ = math.sin(min(1.0, u) * math.pi) * (1.2 if k == 0 else 1)
                    if s_ > 0.02:
                        kilau(ld, CX + tx + dx, CY + ty + dy, rr * s_, (255, 250, 220, 255))
                img.alpha_composite(lay)
        img.alpha_composite(kred, (0, 1490))
        return img

    sampul = frame(6.6, baru(), sampul=True)
    st = baru()
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(int(seconds * FPS)):
        t = n / FPS
        fr = sampul if t < 0.4 else frame(t - 0.4, st)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def kredit_jelas(img, xy, anchor, font, warna=(255, 255, 255), bayang=(20, 60, 70)):
    """Gaya lama menulis handle abu-abu tipis; di latar air ditimpa handle yang lebih terbaca di tempat yang sama."""
    d = ImageDraw.Draw(img)
    d.text((xy[0] + 1, xy[1] + 1), "@" + HANDLE, font=font, fill=bayang, anchor=anchor)
    d.text(xy, "@" + HANDLE, font=font, fill=warna, anchor=anchor)
    return img


def sticky_air(p, i):
    img = gaya_w8.sticky_image(p, i, latar=air_latar(W, H, 17500 + i)).convert("RGBA")
    return kredit_jelas(img, (300, H - 64), "ma", hn(22, 10))


def stamp_air(p, i):
    img = gaya_w12.stamp_image(p, i, latar=air_latar(W, H, 17530 + i)).convert("RGBA")
    return kredit_jelas(img, (W / 2, H - 40), "ma", hn(22, 10), warna=(30, 70, 80), bayang=(200, 236, 236))


def photobooth_awan(p, i):
    latar = awan_latar(W, H, 17300 + i)
    n = len(wrap(PROBE, bersih(p["judul"]), tangan(64), 410))
    return teks_gelap(lambda bg: gaya_w11.photobooth_image(p, i, latar=bg), latar, [(592, 100, W, 140 + n * 76 + 20)],
                      ink=(36, 58, 104), aksen=(36, 58, 104))


def majalah_air(p, i):
    """Sampul majalah di atas air yang dalam; tulisan edisi lama (Adven/Desember 2026) diganti edisi Januari."""
    latar = air_latar(W, H, 17400 + i, gelap=True)
    img = gaya_w10.majalah_image(p, i, latar=latar).convert("RGB")
    a = np.asarray(latar.convert("RGB")).astype(np.float32)[30:68]
    yy = np.linspace(0, 1, H)[30:68, None, None]
    a *= 1 - 0.55 * np.clip((0.3 - yy) / 0.3, 0, 1)
    img.paste(grain(ke_img(a), 0.05), (0, 30))
    d = ImageDraw.Draw(img)
    bulan = " ".join(p.get("_tanggal", "10 Januari 2027").split()[1:]).upper()
    edisi = bersih(p.get("edisi", "EDISI BAPTISAN TUHAN")).upper()
    teks = f"{edisi}  ·  {bulan}  ·  @{HANDLE.upper()}"
    d.text((W / 2, 40), teks, font=muat(d, teks, lambda s: hn(s, 1), W - 140, 22), fill=(255, 255, 255), anchor="ma")
    d.rectangle((W - 226, H - 82, W - 64, H - 60), fill=(255, 255, 255))
    d.text((W - 145, H - 72), p.get("_tgl_struk", "10/01/2027").replace("/", "-"), font=hn(16, 10), fill=(20, 20, 20), anchor="mm")
    return img


SIMPLE = {
    # baru
    "SIDIK": sidik_image, "UKUR": ukur_image, "ABJAD": abjad_image, "JAHIT": jahit_image, "TANGRAM": tangram_image,
    "PIKTO": pikto_image, "HURUF": huruf_image, "SILSILAH": silsilah_image, "BATIK": batik_image, "MARMER": marmer_image,
    # lama
    "KARTUPOS": gaya_w8.kartupos_image, "PETA": gaya_w8.peta_image, "SERTIFIKAT": gaya_w9.sertifikat_image,
    "JAM": gaya_w9.jam_image, "RESEP": gaya_w9.resep_image, "UNDANGAN": gaya_w9.undangan_image,
    "JENDELA": gaya_w9.jendela_image, "FILM": gaya_w10.film_image, "GARIS": gaya_w10.garis_image,
    # mix
    "STICKYAIR": sticky_air,
    "POLAROIDAIR": lambda p, i: gaya_w7.polaroid_image(p, i, latar=air_latar(W, H, 17510 + i)),
    "TIKETAWAN": lambda p, i: gaya_w7.tiket_image(p, i, latar=awan_latar(W, H, 17520 + i)),
    "STAMPAIR": stamp_air,
    "TELEGRAMAWAN": lambda p, i: gaya_w10.telegram_image(p, i, latar=awan_latar(W, H, 17540 + i)),
    "KAMUSBENING": lambda p, i: bening(gaya_w7.kamus_image(p, i), 17550 + i),
    "ALKITABBENING": lambda p, i: bening(gaya_w6.alkitab_image(p, i), 17560 + i),
    "PHOTOBOOTHAWAN": photobooth_awan,
    "MAJALAHAIR": majalah_air,
    "KETIKBENING": lambda p, i: bening(gaya_w7.ketik_image(p, i), 17570 + i),
    "CATATANBENING": lambda p, i: bening(gaya_w7.catatan_image(p, i), 17580 + i),
    "EMAILBENING": lambda p, i: bening(gaya_w12.email_image(p, i), 17590 + i),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {}
REELS = {"RIAK": (riak_reel, "riak"), "WARNAI": (warnai_reel, "warnai"),
         "VINYL": (gaya_w11.vinyl_reel, "vinyl"), "FLIP": (gaya_w8.flip_reel, "flip"), "PROGRESS": (gaya_w9.progress_reel, "progress")}


def render_week(mod=MOD):
    t = importlib.import_module(f"konten.{mod}")
    for old in (OUT / mod).glob("*.jpg"):
        old.unlink()
    out = {}
    for hari, slots in t.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            p = getattr(t, fmt)[idx]
            if fmt in SIMPLE:
                out[(hari, slot)] = ([save(SIMPLE[fmt](konteks(p, hari, slot, MULAI), idx), f"{mod}/{fmt.lower()}{idx + 1}.jpg")], p["caption"])
            elif fmt in MULTI:
                out[(hari, slot)] = (MULTI[fmt](konteks(p, hari, slot, MULAI), idx, mod), p["caption"])
            elif fmt in REELS:
                rel = f"reels/{mod}/{REELS[fmt][1]}{idx + 1}.mp4"
                if (OUT / rel).exists():
                    out[(hari, slot)] = ([rel], p["caption"])
    return out


def render_reels(mod=MOD):
    gaya_w11.render_reels(mod, REELS, MULAI)


if __name__ == "__main__":
    if "reels" in sys.argv:
        render_reels()
    print(len(render_week()), "post")
