"""Akun Tenang - minggu 15 (konten/tenang_w15.py), 3 - 9 Jan 2027: minggu pertama 2027, kembali bekerja, Epifania.
37 gaya diacak tiap hari + komik Eli.
BARU (terinspirasi benda & desain sehari-hari, isinya buatan sendiri):
       JURNAL (bullet journal di kertas titik-titik + habit tracker), LABEL (pita label timbul a la Dymo di papan kraft),
       CETAKBIRU (denah rumah di kertas cetak biru arsitek), PERPUS (kartu pinjam perpustakaan + cap tanggal ungu),
       CENTANG (aplikasi to-do: centang bulat + cincin progres), SWISS (poster gaya Swiss: grid, Helvetica, lingkaran merah),
       LAPIS (pemandangan kertas berlapis), SULAM (sulaman kristik di ram kayu), APOTEK (resep dokter + etiket obat),
       GIZI (label Informasi Nilai Gizi hitam-putih),
       KERETA (Reel peta jalur kereta, kereta berjalan dari stasiun ke stasiun), TULIS (Reel pena menulis ayat huruf demi huruf).
LAMA : CUACA, STRUK, KORAN, MENU, NAMA, MUSEUM, KASET, RASI, LETTER, CHAT, SEARCH, GOSOK.
MIX  : STICKYJURNAL, PHOTOBOOTHJURNAL (kertas jurnal titik-titik + selotip washi),
       POLAROIDPAGI, TIKETPAGI, BALONPAGI, FLIPPAGI (langit pagi: peach/aprikot di cakrawala -> biru langit pucat),
       ALKITABSINAR, KETIKSINAR, CATATANSINAR (cahaya pagi hangat + berkas sinar),
       KAMUSBIRU, TELEGRAMBIRU, MAJALAHBIRU (duotone biru cetak biru + grid).
KOMIK = komik Eli & Yesus.

  python3 gaya_w15.py [reels]
"""
import datetime as dt
import importlib
import math
import re
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

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
from gaya_w7 import bayangan, bersih, comp, ease, fade, ft, gradasi, pas, sprite, tangan, tanpa_kutip
from gaya_w8 import HARI
from gaya_w11 import konteks
from gaya_w13 import foto_redup
from gaya_w14 import avenir, goresan, spidol, tinta
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w15"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2027, 1, 3)
SUP = "/System/Library/Fonts/Supplemental/"

# Skema konten gaya BARU (batas = jumlah karakter maksimum). Semua item juga punya ayat, ref, caption.
SKEMA = {
    "JURNAL": "judul ≤28, kebiasaan[3] ≤22, catatan ≤90",
    "LABEL": "label[3-4] ≤18 (ditampilkan kapital)",
    "CETAKBIRU": "proyek ≤30, ruang[4] = [nama ≤14, catatan ≤22], catatan ≤60",
    "PERPUS": "buku ≤24, pengarang ≤24, pinjam[4] = [tanggal ≤12, catatan ≤20], cap ≤26",
    "CENTANG": "judul ≤20, tugas[4-5] = [teks ≤34, selesai true/false]",
    "SWISS": "angka ≤3, judul ≤22, baris[2] ≤30",
    "LAPIS": "judul ≤36",
    "SULAM": "teks: 1-2 baris dipisah \\n, tiap baris ≤10 huruf A-Z/spasi, kapital",
    "APOTEK": "pasien ≤18, obat[3] = [nama ≤22, aturan ≤28], catatan ≤50",
    "GIZI": "nama ≤24, porsi ≤20, baris[5] = [nama ≤20, nilai ≤8], catatan ≤60",
    "KERETA": "jalur ≤20, stasiun[5] ≤16, ayat ≤160 (Reels)",
    "TULIS": "ayat ≤150 (ayat itulah yang ditulis) (Reels)",
}


# ================= HURUF & ALAT BANTU =================

@lru_cache(maxsize=None)
def _ft(path, size, idx=0, var=None):
    f = ImageFont.truetype(path if path.startswith("/") else SUP + path, int(size), index=idx)
    if var:
        f.set_variation_by_name(var)
    return f


def sf(size, berat="Regular"):  # SF Pro (variabel): Regular, Medium, Semibold, Bold, Heavy, "Condensed Bold", ...
    return _ft("/System/Library/Fonts/SFNS.ttf", size, 0, berat)


def din(size):
    return _ft("DIN Condensed Bold.ttf", size)


def avc(size, idx=0):  # Avenir Next Condensed: 0 Bold, 2 Demi, 4 Italic, 5 Medium, 6 Medium Italic, 7 Regular, 8 Heavy
    return _ft("/System/Library/Fonts/Avenir Next Condensed.ttc", size, idx)


def iowan(size, idx=0):  # 0 Roman, 1 Bold, 2 Italic, 3 Bold Italic, 4 Black
    return _ft("Iowan Old Style.ttc", size, idx)


def mesin(size, idx=0):  # American Typewriter: 0 Regular, 2 Bold, 3 Semibold
    return _ft("AmericanTypewriter.ttc", size, idx)


def kuas(size):  # SignPainter HouseScript Semibold (judul tulisan tangan)
    return _ft("SignPainter.ttc", size, 1)


def helv(size, idx=0):  # Helvetica Neue: 0 Regular, 1 Bold, 4 Condensed Bold, 9 Condensed Black, 10 Medium
    return _ft("/System/Library/Fonts/HelveticaNeue.ttc", size, idx)


def muat(d, teks, font_fn, maxw, start, stop=16, step=2):
    """Font terbesar supaya teks satu baris muat selebar maxw."""
    for s in range(int(start), int(stop) - 1, -step):
        if d.textlength(teks, font=font_fn(s)) <= maxw:
            return font_fn(s)
    return font_fn(stop)


def pas_aman(d, teks, font_fn, maxw, maxh, start, stop, lh):
    """Seperti pas(), tapi kalau di ukuran terkecil masih kepanjangan, terus mengecil sampai muat."""
    f, lines, size = pas(d, teks, font_fn, maxw, maxh, start, stop, lh)
    while (len(lines) * size * lh > maxh or max(d.textlength(ln, font=f) for ln in lines) > maxw) and size > 12:
        size -= 1
        f = font_fn(size)
        lines = wrap(d, teks, f, maxw)
    return f, lines, size


def renggang(d, xy, teks, font, fill, jarak, anchor="ls"):
    """Teks dengan jarak antarhuruf (tracking). anchor: l/m/r + baseline/ascender. -> lebar total."""
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


def campur(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def kertas(w, h, warna, seed, kuat=0.05, serat=200):
    """Kertas polos: warna dasar + belang halus + serat tipis."""
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (1 - kuat + 2 * kuat * render.fbm2d(h, w, rng, ((3, 1.0), (24, 0.5), (140, 0.3))))[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    if serat:
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        gelap = tuple(int(c * 0.82) for c in warna)
        for _ in range(int(serat * w * h / 1e6)):
            x, y, L, ang = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(5, 18), rng.uniform(0, math.pi)
            col = gelap + (int(rng.uniform(14, 34)),) if rng.random() < 0.6 else (255, 255, 255, int(rng.uniform(20, 50)))
            d.line((x, y, x + math.cos(ang) * L, y + math.sin(ang) * L), fill=col, width=1)
        img.alpha_composite(lay)
    return img.convert("RGB")


def kredit(img, xy, warna, anchor="ma", size=22, font=None):
    ImageDraw.Draw(img).text(xy, "@" + HANDLE, font=font or avenir(size, 5), fill=warna, anchor=anchor)


def tempel_tinta(img, mask, pos, warna, seed, kuat=0.88, kasar=0.6):
    """Cap/stempel: mask L -> tinta bertekstur (tepi kasar, bintik) dicampur multiply ke img (RGBA) di pos."""
    a = tinta(mask, seed, kasar) * kuat
    x, y = int(round(pos[0])), int(round(pos[1]))
    h, w = a.shape
    x0, y0, x1, y1 = max(0, x), max(0, y), min(img.width, x + w), min(img.height, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    a = a[y0 - y:y1 - y, x0 - x:x1 - x, None]
    base = np.asarray(img.crop((x0, y0, x1, y1)).convert("RGB")).astype(np.float32)
    ink = np.array(warna, np.float32)
    out = base * (1 - a) + (base * ink / 255 * 0.7 + ink * 0.3) * a
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA"), (x0, y0))


def hari_ke(p, i=0):
    """0 = Minggu ... 6 = Sabtu, dari _tanggal_panjang (konteks)."""
    nama = p.get("_tanggal_panjang", "").split(",")[0].strip()
    return HARI.index(nama) if nama in HARI else (4 + i) % 7


def tanggal_dt(p):
    try:
        return dt.datetime.strptime(p.get("_tgl_struk", ""), "%d/%m/%Y").date()
    except ValueError:
        return MULAI


def tanpa_tahun(s):
    return re.sub(r"\s+\d{4}$", "", s or "")


# ================= LATAR & EFEK MIX =================

WASHI = [((236, 170, 166), "garis"), ((160, 198, 176), "titik"), ((240, 200, 112), "kotak"),
         ((164, 192, 228), "garis"), ((210, 180, 226), "titik"), ((246, 182, 132), "kotak")]


def washi(w, h, warna, pola, rng):
    """Selotip washi: kertas tipis semi-transparan berpola, kedua ujungnya sobek bergerigi."""
    t = Image.new("RGBA", (w, h), warna + (208,))
    d = ImageDraw.Draw(t)
    terang, gelap = (255, 255, 255, 120), tuple(int(c * 0.78) for c in warna) + (110,)
    if pola == "garis":
        for x in range(-h, w + h, 24):
            d.line((x, h, x + h, 0), fill=terang, width=8)
    elif pola == "titik":
        for yy in range(9, h, 18):
            for xx in range(9 + (yy // 18 % 2) * 9, w, 18):
                d.ellipse((xx - 3.5, yy - 3.5, xx + 3.5, yy + 3.5), fill=terang)
    else:
        for x in range(0, w, 22):
            d.rectangle((x, 0, x + 10, h), fill=gelap)
        for y in range(0, h, 22):
            d.rectangle((0, y, w, y + 10), fill=gelap)
    a = np.asarray(t).astype(np.float32)
    a[..., 3] *= 0.88 + 0.12 * rng.random((h, w))
    t = Image.fromarray(a.astype(np.uint8))
    m = Image.new("L", (w, h), 255)
    md = ImageDraw.Draw(m)
    for x in (0, w):
        s = 1 if x == 0 else -1
        pts = [(x + s * rng.uniform(0, 8), y) for y in range(0, h + 6, 5)]
        md.polygon([(x, 0)] + pts + [(x, h)], fill=0)
    t.putalpha(ImageChops.multiply(t.getchannel("A"), m))
    return t


def tempel_washi(img, cx, cy, panjang, sudut, rng, k=None, tebal=56):
    warna, pola = WASHI[int(rng.integers(len(WASHI))) if k is None else k % len(WASHI)]
    t = washi(int(panjang), tebal, warna, pola, rng).rotate(sudut, expand=True, resample=Image.BICUBIC)
    comp(img, t, (cx - t.width / 2, cy - t.height / 2))


def jurnal_latar(w, h, seed, tempat=None):
    """Kertas jurnal krem bertitik (dot grid) + bayang lipatan buku + beberapa potong selotip washi di tepi.
    tempat: daftar (x, y, sudut) untuk washi; default 3 dari 6 sudut/tepi dipilih acak."""
    rng = np.random.default_rng(seed)
    a = np.asarray(kertas(w, h, (248, 243, 231), seed, 0.03, 120)).astype(np.float32)
    xs = np.linspace(0, 1, w)[None, :, None]
    a *= 1 - 0.12 * np.clip((0.07 - xs) / 0.07, 0, 1) ** 1.6  # lipatan di kiri
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    S, step = 2, 36
    lay = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ox, oy = (w % step) / 2 + step / 2, (h % step) / 2 + step / 2
    y = oy
    while y < h:
        x = ox
        while x < w:
            r = 2.3 * S
            ld.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=(170, 160, 146, 160))
            x += step
        y += step
    img.alpha_composite(lay.resize((w, h), Image.LANCZOS))
    if tempat is None:
        semua = [(40, 70, -38), (w - 60, 60, 34), (60, h - 70, 32), (w - 50, h - 80, -30), (14, h * 0.5, 84), (w - 14, h * 0.42, -86)]
        tempat = [semua[k] for k in rng.permutation(len(semua))[:3]]
    for cx, cy, sd in tempat:
        tempel_washi(img, cx, cy, rng.uniform(200, 260), sd + rng.uniform(-6, 6), rng)
    return grain(img.convert("RGB"), 0.025)


def pagi_latar(w, h, seed):
    """Langit pagi: biru langit pucat di atas -> peach/aprikot di cakrawala bawah, cahaya matahari lembut, awan tipis."""
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, h)[:, None]
    stops = [(0.0, (170, 206, 238)), (0.42, (212, 226, 242)), (0.72, (252, 222, 204)), (1.0, (250, 186, 146))]
    arr = np.zeros((h, 1, 3), np.float32)
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        u = np.clip((y - t0) / (t1 - t0), 0, 1)[..., None]
        seg = ((y >= t0) & (y <= t1))[..., None]
        arr = np.where(seg, np.array(c0, np.float32) * (1 - u) + np.array(c1, np.float32) * u, arr)
    arr = np.broadcast_to(arr, (h, w, 3)).copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sx, sy = w * rng.uniform(0.3, 0.7), h * 0.9
    dd = ((xx - sx) ** 2 + ((yy - sy) * 1.3) ** 2) / (w * 0.62) ** 2
    glow = np.exp(-dd * 2.6)[..., None]
    arr = 255 - (255 - arr) * (1 - 0.55 * glow * np.array([1.0, 0.85, 0.6]))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (255, 255, 255, 0))  # dasar putih: blur tidak menggelapkan tepi
    d = ImageDraw.Draw(lay)
    for _ in range(5):  # awan gumpal
        cx, cy = rng.uniform(-60, w + 60), rng.uniform(0.08, 0.6) * h
        for _ in range(7):
            rx, ry = rng.uniform(70, 170), rng.uniform(34, 70)
            x, y_ = cx + rng.uniform(-170, 170), cy + rng.uniform(-24, 24)
            d.ellipse((x - rx, y_ - ry, x + rx, y_ + ry), fill=(255, 255, 255, 96))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(26)))
    lay = Image.new("RGBA", (w, h), (255, 255, 255, 0))  # dasar putih: blur tidak menggelapkan tepi
    d = ImageDraw.Draw(lay)
    for _ in range(6):  # awan tipis memanjang dekat cakrawala
        cx, cy = rng.uniform(0, w), rng.uniform(0.6, 0.85) * h
        rx, ry = rng.uniform(180, 380), rng.uniform(8, 16)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(255, 240, 230, 120))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8)))
    return grain(img.convert("RGB"), 0.025)


def sinar(img, seed, kuat=1.0):
    """Cahaya pagi hangat: kebocoran cahaya (light leak) di satu sudut atas + berkas sinar lembut yang miring.
    Di antara berkas sinar gambar sedikit lebih teduh, jadi berkasnya tetap terlihat di atas kertas putih."""
    rng = np.random.default_rng(seed)
    w, h = img.size
    base = np.asarray(img.convert("RGB")).astype(np.float32) / 255
    kiri = rng.random() < 0.5
    sx, sy = (-0.1 * w, -0.08 * h) if kiri else (1.1 * w, -0.08 * h)
    s = 4
    m = Image.new("L", (w // s, h // s), 0)
    md = ImageDraw.Draw(m)
    arah = math.atan2(h * 0.7 - sy, w * 0.5 - sx)
    L = 2.2 * max(w, h) / s
    for k in range(6):
        a = arah + (k - 2.5) * 0.13 + rng.uniform(-0.04, 0.04)
        lebar = rng.uniform(0.018, 0.04)
        p0 = (sx / s, sy / s)
        md.polygon([p0, (p0[0] + math.cos(a - lebar) * L, p0[1] + math.sin(a - lebar) * L),
                    (p0[0] + math.cos(a + lebar) * L, p0[1] + math.sin(a + lebar) * L)], fill=int(rng.uniform(150, 230)))
    m = m.filter(ImageFilter.GaussianBlur(7)).resize((w, h), Image.BICUBIC)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    jarak = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / max(w, h)
    rays = np.asarray(m).astype(np.float32) / 255 * np.clip(1.35 - jarak, 0, 1)
    teduh = 0.09 * kuat * (1 - np.clip(rays * 1.5, 0, 1)) * np.clip(1.4 - jarak, 0, 1)
    base = base * (1 - teduh[..., None]) * np.array([1.0, 0.985, 0.95])
    leak = np.exp(-(jarak / 0.5) ** 2 * 1.6)
    col = leak[..., None] * np.array([1.0, 0.62, 0.3]) * 0.7 + leak[..., None] ** 3 * np.array([0.0, 0.25, 0.3]) * 0.6
    col += rays[..., None] * np.array([1.0, 0.88, 0.62]) * 0.32
    col = np.clip(col * kuat, 0, 1)
    out = 1 - (1 - base) * (1 - col)
    out = out * np.array([1.02, 1.0, 0.95]) + np.array([0.012, 0.006, 0.0])
    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))


def biru(img, seed):
    """Duotone cetak biru: luminans dipetakan biru tua (gelap) -> putih (terang), plus garis grid tipis."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    lum = (a @ np.array([0.299, 0.587, 0.114], np.float32)) / 255
    lo, hi = min(np.percentile(lum, 1), 0.12), max(np.percentile(lum, 99.5), 0.88)
    t = np.clip((lum - lo) / (hi - lo), 0, 1)
    navy, kobalt, putih = np.array([12, 32, 84], np.float32), np.array([34, 90, 178], np.float32), np.array([242, 247, 255], np.float32)
    k = 0.5
    u1, u2 = np.clip(t / k, 0, 1)[..., None], np.clip((t - k) / (1 - k), 0, 1)[..., None]
    out = np.where((t < k)[..., None], navy * (1 - u1) + kobalt * u1, kobalt * (1 - u2) + putih * u2)
    out *= (0.975 + 0.05 * render.fbm2d(h, w, rng, ((3, 1.0), (20, 0.5), (90, 0.3))))[..., None]
    g = np.zeros((h, w), np.float32)
    g[:, 13::27] = 0.09
    g[13::27, :] = 0.09
    g[:, 13::135] = 0.18
    g[13::135, :] = 0.18
    gcol = np.where((t > 0.5)[..., None], np.array([70, 120, 200], np.float32), np.array([150, 190, 245], np.float32))
    out = out * (1 - g[..., None]) + gcol * g[..., None]
    return grain(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 0.03)


def pisah_lapisan(fn):
    """Render fn(latar) di atas latar hitam & putih -> (rgb premultiplied, alpha) dari semua yang digambar di atas latar."""
    hitam = np.asarray(fn(Image.new("RGB", (W, H), (0, 0, 0))).convert("RGB")).astype(np.float32)
    putih = np.asarray(fn(Image.new("RGB", (W, H), (255, 255, 255))).convert("RGB")).astype(np.float32)
    a = np.clip(1 - (putih - hitam).mean(axis=2) / 255, 0, 1)
    return np.minimum(hitam, a[..., None] * 255), a


def teks_gelap(fn, latar, zona, ink=(46, 42, 74), aksen=(186, 88, 52)):
    """Gaya lama yang mengira latarnya gelap (teks krem/emas) dipakai di latar terang: lapisan depannya dipisahkan,
    lalu teks terang di dalam `zona` (daftar kotak) diwarnai ulang gelap: emas -> aksen, selain itu -> ink."""
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


# ================= BARU =================

# ---------- JURNAL: bullet journal + habit tracker ----------

JURNAL_WARNA = [  # (spidol 3 kebiasaan, stabilo judul, tinta)
    ([(116, 172, 150), (234, 136, 118), (232, 184, 84)], (255, 214, 120), (40, 46, 78)),
    ([(124, 156, 214), (186, 146, 210), (242, 166, 126)], (184, 214, 242), (40, 42, 82)),
    ([(198, 112, 82), (134, 158, 92), (226, 146, 170)], (248, 196, 188), (58, 42, 40)),
]
HURUF_HARI = ["M", "S", "S", "R", "K", "J", "S"]


def kotak_tangan(d, box, col, w, rng, S=2):
    x0, y0, x1, y1 = [v * S for v in box]
    pts = [(x0 - 2 * S, y0), (x1 + S, y0 + rng.uniform(-1, 1) * S), (x1, y1 + 2 * S), (x0 + rng.uniform(-1, 1) * S, y1), (x0, y0 - S)]
    goresan(d, pts, w * S, col, rng, 1.1 * S)


def blok_spidol(d, box, col, rng, S=2):
    """Kotak diwarnai spidol: blok agak transparan + coretan zigzag yang lebih pekat."""
    x0, y0, x1, y1 = [v * S for v in box]
    m = 6 * S
    d.rounded_rectangle((x0 + m + rng.uniform(-2, 2) * S, y0 + m, x1 - m, y1 - m + rng.uniform(-2, 2) * S), radius=9 * S, fill=col + (150,))
    pts, n = [], 6
    for k in range(n + 1):
        t = k / n
        pts.append((x0 + m + 3 * S, y0 + m + 3 * S + (y1 - y0 - 2 * m - 6 * S) * t) if k % 2 == 0 else
                   (x1 - m - 3 * S, y0 + m + 3 * S + (y1 - y0 - 2 * m - 6 * S) * t))
    goresan(d, pts, 9 * S, col + (235,), rng, 1.4 * S)


def jurnal_image(p, i):
    rng = np.random.default_rng(15100 + i)
    spidol3, stabilo, ink = JURNAL_WARNA[i % 3]
    img = jurnal_latar(W, H, 15100 + i, tempat=[(14, H * 0.5, 84), (60, H - 70, 32), (W - 14, H * 0.4, -86)]).convert("RGBA")
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    d = ImageDraw.Draw(img)
    hari = hari_ke(p, i)
    tgl = tanggal_dt(p)
    kepala = tanpa_tahun(p.get("_tanggal_panjang", "")).upper().replace(", ", " · ")
    renggang(d, (96, 104), kepala, avenir(22, 2), campur(ink, (248, 243, 231), 0.25), 3)
    renggang(d, (W - 96, 104), f"HARI KE-{tgl.timetuple().tm_yday}", avenir(22, 2), campur(ink, (248, 243, 231), 0.25), 3, anchor="rs")
    # judul tulisan tangan + stabilo
    judul = bersih(p["judul"])
    fj = muat(d, judul, kuas, W - 200, 112, 66, 4)
    lines = [judul] if d.textlength(judul, font=fj) <= W - 200 else wrap(d, judul, kuas(80), W - 200)
    fj = fj if len(lines) == 1 else kuas(80)
    y = 140
    for ln in lines:
        base = y + fj.size * 0.78
        tw = d.textlength(ln, font=fj)
        x0 = (W - tw) / 2
        ld.polygon([((x0 - 14) * S, (base - fj.size * 0.36) * S), ((x0 + tw + 18) * S, (base - fj.size * 0.42) * S),
                    ((x0 + tw + 12) * S, (base + fj.size * 0.06) * S), ((x0 - 8) * S, (base + fj.size * 0.1) * S)], fill=stabilo + (170,))
        y = base + fj.size * 0.22
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    y = 140
    for ln in lines:
        base = y + fj.size * 0.78
        d.text((W / 2, base), ln, font=fj, fill=ink, anchor="ms")
        y = base + fj.size * 0.22
    # habit tracker
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    y0 = y + 34
    d.text((92, y0 + 34), "habit tracker", font=kuas(50), fill=ink, anchor="ls")
    goresan(ld, [((92 + 236) * S, (y0 + 22) * S), ((92 + 290) * S, (y0 + 26) * S)], 3 * S, ink + (220,), rng, S)
    goresan(ld, [((92 + 276) * S, (y0 + 16) * S), ((92 + 292) * S, (y0 + 26) * S), ((92 + 274) * S, (y0 + 34) * S)], 3 * S, ink + (220,), rng, S)
    cw, gap = 58, 12
    gx0 = W - 92 - 7 * cw - 6 * gap
    lw = gx0 - 92 - 26
    hy = y0 + 76
    fh = tangan(30)
    for k in range(7):
        cx = gx0 + k * (cw + gap) + cw / 2
        d.text((cx, hy), HURUF_HARI[k], font=fh, fill=ink, anchor="mm")
        if k == hari:
            pts = [((cx + 27 * math.cos(t)) * S, (hy + 2 + 24 * math.sin(t)) * S) for t in np.linspace(-0.9, 2 * math.pi - 0.5, 30)]
            goresan(ld, pts, 3.5 * S, spidol3[1] + (230,), rng, 1.2 * S)
    kebiasaan = [bersih(k) for k in p["kebiasaan"]][:3]
    fk = tangan(36)
    for s in range(36, 21, -1):
        fk = tangan(s)
        if max(d.textlength(k, font=fk) for k in kebiasaan) <= lw:
            break
    ry = hy + 36
    for r, teks in enumerate(kebiasaan):
        d.text((92, ry + cw / 2), teks, font=fk, fill=ink, anchor="lm")
        for k in range(7):
            x = gx0 + k * (cw + gap)
            if k <= hari:
                blok_spidol(ld, (x, ry, x + cw, ry + cw), spidol3[r], rng)
            kotak_tangan(ld, (x, ry, x + cw, ry + cw), ink + (200,), 2.4, rng)
            if k == hari:
                goresan(ld, [((x + 15) * S, (ry + 30) * S), ((x + 26) * S, (ry + 43) * S), ((x + 48) * S, (ry + 12) * S)], 5 * S, ink + (255,), rng, S)
        ry += cw + 20
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # kartu ayat bertempel washi
    cy0, cy1 = ry + 26, H - 290
    cwd = 880
    card = kertas(cwd, int(cy1 - cy0), (254, 252, 246), 15150 + i, 0.02, 60).convert("RGBA")
    cd = ImageDraw.Draw(card)
    cd.text((34, 6), "“", font=ft("Georgia Bold.ttf", 120), fill=spidol3[0])
    fr = kuas(52)
    f, vl, size = pas_aman(cd, tanpa_kutip(p["ayat"]), tangan, cwd - 170, card.height - 70 - 70, 44, 26, 1.32)
    yy = 44 + max(0, (card.height - 70 - 60 - len(vl) * size * 1.32) / 2)
    for ln in vl:
        cd.text((100, yy), ln, font=f, fill=ink)
        yy += size * 1.32
    cd.text((cwd - 50, min(yy + 52, card.height - 24)), p["ref"], font=fr, fill=campur(spidol3[1], (0, 0, 0), 0.25), anchor="rs")
    card = card.rotate(-1.0, expand=True, resample=Image.BICUBIC)
    cx0 = (W - card.width) / 2
    bayangan(img, card, (cx0, cy0), blur=12, geser=(4, 8), kuat=0.25)
    tempel_washi(img, cx0 + 50, cy0 + 16, 170, 38, rng, i)
    tempel_washi(img, cx0 + card.width - 50, cy0 + card.height - 16, 170, 36, rng, i + 3)
    # catatan
    d = ImageDraw.Draw(img)
    ny0 = cy0 + card.height + 40
    d.text((96, ny0 + 40), "catatan:", font=kuas(50), fill=campur(spidol3[1], (0, 0, 0), 0.25), anchor="ls")
    tx = 96 + d.textlength("catatan:", font=kuas(50)) + 20
    fc, cl, cs = pas_aman(d, bersih(p["catatan"]), tangan, W - 92 - tx, H - 80 - ny0, 34, 24, 1.3)
    yy = ny0 + 4
    for ln in cl:
        d.text((tx, yy), ln, font=fc, fill=ink)
        yy += cs * 1.3
    kredit(img, (W / 2, H - 46), campur(ink, (248, 243, 231), 0.4))
    return img


# ---------- LABEL: pita label timbul a la Dymo ----------

DYMO = [(28, 28, 30), (192, 32, 42), (26, 74, 170), (20, 122, 78)]


def kraft(w, h, seed, warna=(196, 154, 108)):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (0.92 + 0.16 * render.fbm2d(h, w, rng, ((4, 1.0), (30, 0.6), (200, 0.4))))[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(int(w * h / 700)):
        x, y, L, ang = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(3, 14), rng.uniform(0, math.pi)
        col = (96, 64, 34, int(rng.uniform(25, 70))) if rng.random() < 0.6 else (244, 224, 192, int(rng.uniform(25, 70)))
        d.line((x, y, x + math.cos(ang) * L, y + math.sin(ang) * L), fill=col, width=1)
    img.alpha_composite(lay)
    return grain(img.convert("RGB"), 0.06)


def dymo_ukuran(teks, size):
    """-> (lebar, tinggi, daftar langkah per huruf) pita Dymo untuk teks & ukuran huruf ini."""
    f = helv(size, 4)
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    jarak = size * 0.13
    langkah = [size * 0.42 if c == " " else probe.textlength(c, font=f) + jarak for c in teks]
    pad = int(size * 0.62)
    return int(sum(langkah) - jarak + 2 * pad), int(size * 1.6), langkah


def dymo(teks, warna, size, rng):
    """Pita label timbul: plastik mengilap + huruf putih yang 'ditekan' (sedikit goyang seperti roda embos)."""
    f = helv(size, 4)
    tw, th, langkah = dymo_ukuran(teks, size)
    pad = int(size * 0.62)
    yy = np.linspace(0, 1, th)[:, None]
    base = np.array(warna, np.float32)[None, None, :] * (1.0 + 0.16 * np.exp(-((yy - 0.16) / 0.07) ** 2) - 0.2 * yy ** 2)[..., None]
    base = np.broadcast_to(base, (th, tw, 3)).copy()
    base *= (0.97 + 0.03 * np.sin(np.arange(th) * 2.1))[:, None, None]  # garis halus pita
    base *= (0.96 + 0.06 * rng.random((th, tw)))[..., None]
    base += np.array([255, 255, 255]) * 0.18 * np.exp(-((yy - 0.1) / 0.03) ** 2)[..., None]  # kilau tipis
    m = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(m)
    x = pad
    for c, lk in zip(teks, langkah):
        if c != " ":
            md.text((x + rng.uniform(-0.8, 0.8), th / 2 + rng.uniform(-1.6, 1.6)), c, font=f, fill=255, anchor="lm")
        x += lk
    a = np.asarray(m).astype(np.float32) / 255
    bawah = np.roll(np.roll(a, 2, 0), 2, 1)
    atas = np.roll(np.roll(a, -1, 0), -1, 1)
    bayang = np.clip(bawah - a, 0, 1)[..., None]
    kilap = np.clip(atas - a, 0, 1)[..., None]
    out = base * (1 - 0.55 * bayang) + 255 * 0.25 * kilap * (1 - bayang)
    huruf = np.array([244, 244, 238], np.float32) * (0.93 + 0.07 * rng.random((th, tw)))[..., None]
    huruf *= (1 - 0.08 * np.clip(np.roll(a, -1, 0) - a, 0, 1))[..., None]
    out = out * (1 - a[..., None]) + huruf * a[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    mask = Image.new("L", (tw * 3, th * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw * 3 - 1, th * 3 - 1), radius=int(th * 0.4), fill=255)
    img.putalpha(mask.resize((tw, th), Image.LANCZOS))
    return img


def label_image(p, i):
    rng = np.random.default_rng(15200 + i)
    img = kraft(W, H, 15200 + i, [(196, 154, 108), (186, 146, 104), (204, 166, 120)][i % 3]).convert("RGBA")
    labels = [bersih(t).upper() for t in p["label"]][:4]
    n = len(labels)
    warna = DYMO[i % 4:] + DYMO[:i % 4]
    size = 72 if n <= 3 else 62
    while size > 34 and max(dymo_ukuran(t, size)[0] for t in labels) > W - 200:
        size -= 2
    th = dymo_ukuran("A", size)[1]
    area0, area1 = 128, 640
    langkah = (area1 - area0 - th) / max(1, n - 1)
    for k, t in enumerate(labels):
        tape = dymo(t, warna[k % 4], size, rng).rotate((-1) ** k * rng.uniform(0.8, 2.0), expand=True, resample=Image.BICUBIC)
        x = (W - tape.width) / 2 + (-1) ** (k + i) * rng.uniform(10, 60)
        x = min(max(x, 80), W - 80 - tape.width)
        y = area0 + k * langkah + (langkah - th) * 0.25 if n > 1 else 300
        bayangan(img, tape, (x, y), blur=4, geser=(3, 5), kuat=0.5)
    # kartu indeks berisi ayat, disematkan dengan paku payung
    cw, ch = 860, 560
    card = kertas(cw, ch, (252, 250, 243), 15210 + i, 0.02, 60).convert("RGBA")
    cd = ImageDraw.Draw(card)
    ref = bersih(p["ref"]).upper()
    rs = 34
    while rs > 22 and dymo_ukuran(ref, rs)[0] > cw - 120:
        rs -= 2
    tape = dymo(ref, DYMO[0], rs, rng)
    f, vl, size_ = pas_aman(cd, bersih(p["ayat"]), lambda s: georgia(s, True), cw - 120, ch - 110 - tape.height - 40, 40, 26, 1.38)
    lh = size_ * 1.38
    blok = len(vl) * lh
    y0 = 96 + max(0, (ch - 96 - tape.height - 50 - blok) / 2)
    cd.line((40, 64, cw - 40, 64), fill=(226, 112, 112), width=2)
    garis = y0 + size_ * 1.08
    while garis - lh > 80:
        garis -= lh
    while garis < ch - 20:  # garis biru kartu indeks sejajar dengan baris ayat
        cd.line((40, garis, cw - 40, garis), fill=(196, 214, 236), width=1)
        garis += lh
    yy = y0
    for ln in vl:
        cd.text((cw / 2, yy), ln, font=f, fill=(42, 40, 44), anchor="ma")
        yy += lh
    comp(card, tape, ((cw - tape.width) / 2, min(yy + 18, ch - tape.height - 24)))
    card = card.rotate(0.8 * (-1) ** i, expand=True, resample=Image.BICUBIC)
    cx0, cy0 = (W - card.width) / 2, 676
    bayangan(img, card, (cx0, cy0), blur=14, geser=(6, 12), kuat=0.42)
    pin = sprite(56, 56, lambda dd, k: (dd.ellipse((6 * k, 6 * k, 50 * k, 50 * k), fill=(200, 40, 46, 255)),
                                         dd.ellipse((14 * k, 12 * k, 28 * k, 24 * k), fill=(255, 190, 190, 200))))
    bayangan(img, pin, (W / 2 - 28, cy0 - 10), blur=5, geser=(6, 8), kuat=0.55)
    kredit(img, (W / 2, H - 44), (92, 62, 36))
    return img


# ---------- CETAKBIRU: denah rumah di kertas cetak biru ----------

BIRU_CB = [(22, 70, 146), (18, 56, 122), (24, 86, 156)]


def kertas_biru(w, h, warna, seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (0.9 + 0.14 * render.fbm2d(h, w, rng, ((3, 1.0), (16, 0.5), (90, 0.3))))[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1.04 - 0.2 * np.clip(r - 0.55, 0, 1))[..., None]
    g = np.zeros((h, w), np.float32)
    g[:, 9::27] = 0.06
    g[9::27, :] = 0.06
    g[:, 9::135] = 0.13
    g[9::135, :] = 0.13
    a = a * (1 - g[..., None]) + np.array([210, 228, 255], np.float32) * g[..., None]
    for pos, ax in ((w * 0.5 + rng.uniform(-40, 40), 1), (h * 0.5 + rng.uniform(-40, 40), 0)):  # lipatan kertas
        dpos = (xx if ax == 1 else yy) - pos
        a *= (1 + 0.07 * np.exp(-(dpos / 3) ** 2) - 0.05 * np.exp(-((dpos - 6) / 6) ** 2))[..., None]
    return grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.04)


def cetakbiru_image(p, i):
    rng = np.random.default_rng(15300 + i)
    bg = BIRU_CB[i % 3]
    img = kertas_biru(W, H, bg, 15300 + i).convert("RGBA")
    putih, redup = (238, 245, 255), campur((238, 245, 255), bg, 0.35)
    d = ImageDraw.Draw(img)
    renggang(d, (70, 82), "CETAK BIRU  ·  DENAH LANTAI", din(26), redup, 3)
    renggang(d, (W - 70, 82), "SKALA 1:50", din(26), redup, 3, anchor="rs")
    proyek = bersih(p["proyek"]).upper()
    fp = muat(d, proyek, din, W - 140, 84, 40)
    d.text((W / 2, 112), proyek, font=fp, fill=putih, anchor="ma")
    # denah (2x)
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    P = lambda *xy: [v * S for v in xy]
    X0, Y0, X1, Y1 = 176, 286, 904, 712
    fx, fx2, fy = [(0.56, 0.40, 0.50), (0.46, 0.60, 0.46), (0.62, 0.36, 0.54)][i % 3]
    vt, vb, hy = X0 + (X1 - X0) * fx, X0 + (X1 - X0) * fx2, Y0 + (Y1 - Y0) * fy
    garis = putih + (255,)
    tipis = putih + (200,)
    t_ext = 14
    ld.rectangle(P(X0, Y0, X1, Y1), outline=garis, width=4 * S)
    ld.rectangle(P(X0 + t_ext, Y0 + t_ext, X1 - t_ext, Y1 - t_ext), outline=garis, width=2 * S)
    hatch = Image.new("L", lay.size, 0)
    hd = ImageDraw.Draw(hatch)
    for x in range(int(X0) - 800, int(X1) + 50, 9):
        hd.line(P(x, Y1 + 20, x + (Y1 - Y0) + 60, Y0 - 40), fill=150, width=S)
    band = Image.new("L", lay.size, 0)
    bd = ImageDraw.Draw(band)
    bd.rectangle(P(X0, Y0, X1, Y1), fill=255)
    bd.rectangle(P(X0 + t_ext, Y0 + t_ext, X1 - t_ext, Y1 - t_ext), fill=0)
    lay.paste(Image.new("RGBA", lay.size, garis), (0, 0), ImageChops.multiply(hatch, band))
    ld = ImageDraw.Draw(lay)
    ld.line(P(vt, Y0 + t_ext, vt, hy), fill=garis, width=7 * S)
    ld.line(P(vb, hy, vb, Y1 - t_ext), fill=garis, width=7 * S)
    ld.line(P(X0 + t_ext, hy, X1 - t_ext, hy), fill=garis, width=7 * S)
    kosong = (0, 0, 0, 0)
    rintangan = []  # kotak busur pintu, supaya label ruang tidak menimpanya

    def pintu(hx, hy_, arah, panjang=62):
        """Celah di dinding + daun pintu + busur ayun. arah: (dx, dy) sepanjang dinding, (nx, ny) arah ayun."""
        (dx, dy), (nx, ny) = arah
        xs_, ys_ = [hx, hx + dx * panjang, hx + nx * panjang], [hy_, hy_ + dy * panjang, hy_ + ny * panjang]
        rintangan.append((min(xs_) - 8, min(ys_) - 8, max(xs_) + 8, max(ys_) + 8))
        ld.line(P(hx, hy_, hx + dx * panjang, hy_ + dy * panjang), fill=kosong, width=11 * S)
        ld.line(P(hx, hy_, hx + nx * panjang, hy_ + ny * panjang), fill=garis, width=3 * S)
        a0 = math.degrees(math.atan2(dy, dx))
        a1 = math.degrees(math.atan2(ny, nx))
        lo, hi = sorted((a0, a1))
        if hi - lo > 180:
            lo, hi = hi, lo + 360
        ld.arc(P(hx - panjang, hy_ - panjang, hx + panjang, hy_ + panjang), lo, hi, fill=tipis, width=2 * S)

    def jendela(x0, y0, x1, y1):
        if y0 == y1:
            ld.rectangle(P(x0, y0 - 1, x1, y0 + t_ext + 1), fill=kosong)
            for o in (0, t_ext / 2, t_ext):
                ld.line(P(x0, y0 + o, x1, y0 + o), fill=garis, width=2 * S)
            for x in (x0, x1):
                ld.line(P(x, y0, x, y0 + t_ext), fill=garis, width=2 * S)
        else:
            ld.rectangle(P(x0 - 1, y0, x0 + t_ext + 1, y1), fill=kosong)
            for o in (0, t_ext / 2, t_ext):
                ld.line(P(x0 + o, y0, x0 + o, y1), fill=garis, width=2 * S)
            for y in (y0, y1):
                ld.line(P(x0, y, x0 + t_ext, y), fill=garis, width=2 * S)

    pintu(vt, hy - 24 - 62, ((0, 1), (-1, 0)))
    pintu(vb, hy + 24, ((0, 1), (1, 0)))
    pintu(X0 + 40 + rng.uniform(0, 40), hy, ((1, 0), (0, 1)))
    pintu(X1 - 120, hy, ((1, 0), (0, -1)))
    pintu(vb + (X1 - vb) * 0.7, Y1 - t_ext, ((1, 0), (0, -1)), 60)  # pintu masuk
    jendela(X0 + (vt - X0) * 0.3, Y0, X0 + (vt - X0) * 0.3 + 120, Y0)
    jendela(vt + (X1 - vt) * 0.3, Y0, vt + (X1 - vt) * 0.3 + 110, Y0)
    jendela(X0, hy + (Y1 - hy) * 0.3, X0, hy + (Y1 - hy) * 0.3 + 100)
    jendela(X1 - t_ext, Y0 + (hy - Y0) * 0.3, X1 - t_ext, Y0 + (hy - Y0) * 0.3 + 100)
    # garis ukur
    PXM = 80.0  # piksel per meter

    def ukur_h(xs, y):
        ld.line(P(xs[0], y, xs[-1], y), fill=tipis, width=2 * S)
        for x in xs:
            ld.line(P(x, y + 10, x, Y0 - 8), fill=putih + (110,), width=S)
            ld.line(P(x - 8, y + 8, x + 8, y - 8), fill=garis, width=3 * S)
        for a, b in zip(xs, xs[1:]):
            teks = f"{(b - a) / PXM:.2f}".replace(".", ",")
            ld.text(P((a + b) / 2, y - 8), teks, font=din(24 * S), fill=garis, anchor="ms")

    ukur_h([X0, vt, X1], Y0 - 44)
    xv = X0 - 46
    ld.line(P(xv, Y0, xv, Y1), fill=tipis, width=2 * S)
    for yv in (Y0, hy, Y1):
        ld.line(P(xv + 10, yv, X0 - 8, yv), fill=putih + (110,), width=S)
        ld.line(P(xv - 8, yv + 8, xv + 8, yv - 8), fill=garis, width=3 * S)
    for a, b in ((Y0, hy), (hy, Y1)):
        t = Image.new("RGBA", (200 * S, 40 * S), (0, 0, 0, 0))
        ImageDraw.Draw(t).text((100 * S, 30 * S), f"{(b - a) / PXM:.2f}".replace(".", ","), font=din(24 * S), fill=garis, anchor="ms")
        t = t.rotate(90, expand=True)
        lay.alpha_composite(t, (int((xv - 34) * S), int(((a + b) / 2 - 100) * S)))
    # panah utara
    nx, ny_ = W - 98, Y0 + 10
    ld.ellipse(P(nx - 24, ny_ - 24, nx + 24, ny_ + 24), outline=garis, width=2 * S)
    ld.polygon(P(nx, ny_ - 34, nx + 10, ny_ + 8, nx, ny_, nx - 10, ny_ + 8), fill=garis)
    ld.text(P(nx, ny_ + 50), "U", font=din(24 * S), fill=garis, anchor="ms")
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    # label ruang
    rooms = [(X0, Y0, vt, hy), (vt, Y0, X1, hy), (X0, hy, vb, Y1), (vb, hy, X1, Y1)]
    for (nama, cat), (x0, y0, x1, y1) in zip(p["ruang"], rooms):
        x0, y0, x1, y1 = x0 + t_ext, y0 + t_ext, x1 - t_ext, y1 - t_ext
        rw = x1 - x0 - 40
        nama, cat = bersih(nama).upper(), bersih(cat)
        fn = muat(d, nama, din, rw, 38, 22)
        fc = muat(d, cat, lambda s: avc(s, 6), rw, 26, 20)
        if d.textlength(cat, font=fc) <= rw:
            cl, cs = [cat], fc.size
        else:
            fc, cl, cs = pas_aman(d, cat, lambda s: avc(s, 6), rw, 64, 26, 18, 1.15)
        luas = f"{(x1 - x0 + 2 * t_ext) * (y1 - y0 + 2 * t_ext) / PXM ** 2:.1f} m²".replace(".", ",")
        lebar = max([d.textlength(nama, font=fn)] + [d.textlength(ln, font=fc) for ln in cl]) + 12
        # posisi label terdekat ke tengah ruang yang tidak menimpa busur pintu (kalau sempit, luas m² tidak ditulis)
        cx0, cy0 = (x0 + x1) / 2, (y0 + y1) / 2
        calon = sorted(((ox, oy) for ox in range(-240, 241, 6) for oy in range(-120, 121, 3)), key=lambda o: o[0] ** 2 + 3 * o[1] ** 2)
        ketemu = None
        for pakai_luas in (True, False):
            tinggi = fn.size + 8 + len(cl) * cs * 1.15 + (30 if pakai_luas else 0)
            for ox, oy in calon:
                bx0, by0 = cx0 + ox - lebar / 2, cy0 + oy - tinggi / 2
                bx1, by1 = bx0 + lebar, by0 + tinggi
                if bx0 < x0 + 4 or bx1 > x1 - 4 or by0 < y0 + 2 or by1 > y1 - 2:
                    continue
                if all(bx1 < r[0] or bx0 > r[2] or by1 < r[1] or by0 > r[3] for r in rintangan):
                    ketemu = (cx0 + ox, by0, pakai_luas)
                    break
            if ketemu:
                break
        tinggi = fn.size + 8 + len(cl) * cs * 1.15 + 30
        cx, yy, pakai_luas = ketemu or (cx0, cy0 - tinggi / 2, True)
        d.text((cx, yy + fn.size * 0.85), nama, font=fn, fill=putih, anchor="ms")
        yy += fn.size + 8
        for ln in cl:
            d.text((cx, yy), ln, font=fc, fill=redup, anchor="ma")
            yy += cs * 1.15
        if pakai_luas:
            d.text((cx, yy + 6), luas, font=din(20), fill=campur(putih, bg, 0.5), anchor="ma")
    # skala + catatan
    ys = Y1 + 40
    for k in range(4):
        x = X0 + k * PXM * 0.75
        box = (x, ys, x + PXM * 0.75, ys + 12)
        d.rectangle(box, fill=putih if k % 2 == 0 else None, outline=putih, width=2)
        d.text((x, ys + 36), str(k), font=din(20), fill=redup, anchor="ms")
    d.text((X0 + 3 * PXM, ys + 36), "3 m", font=din(20), fill=redup, anchor="ms")
    cx0 = X0 + 4 * PXM * 0.75 + 70
    renggang(d, (cx0, ys + 12), "CATATAN", din(24), putih, 2)
    fc, cl, cs = pas_aman(d, bersih(p["catatan"]), lambda s: avc(s, 5), W - 70 - cx0, 76, 30, 20, 1.2)
    yy = ys + 22
    for ln in cl:
        d.text((cx0, yy), ln, font=fc, fill=putih)
        yy += cs * 1.2
    # kotak spesifikasi (ayat)
    ay0, ay1 = max(yy + 22, ys + 104), 1084
    d.rectangle((70, ay0, W - 70, ay1), outline=putih, width=2)
    lab = "SPESIFIKASI"
    lw = lebar_renggang(d, lab, din(22), 3) + 24
    d.rectangle((70, ay0 - 15, 70 + lw, ay0 + 15), fill=putih)
    renggang(d, (82, ay0 + 9), lab, din(22), bg, 3)
    f, vl, size = pas_aman(d, bersih(p["ayat"]), lambda s: georgia(s, True), W - 220, ay1 - ay0 - 86, 38, 22, 1.32)
    yy = ay0 + 28 + max(0, (ay1 - ay0 - 86 - len(vl) * size * 1.32) / 2)
    for ln in vl:
        d.text((W / 2, yy), ln, font=f, fill=putih, anchor="ma")
        yy += size * 1.32
    d.text((W / 2, yy + 6), p["ref"].upper(), font=din(30), fill=campur(putih, (255, 214, 120), 0.6), anchor="ma")
    # kotak judul
    tb0, tb1 = 1104, 1268
    d.rectangle((70, tb0, W - 70, tb1), outline=putih, width=3)
    tm = (tb0 + tb1) / 2
    d.line((70, tm, W - 70, tm), fill=putih, width=2)
    xa, xb = 70 + (W - 140) * 0.62, 70 + (W - 140) * 0.42
    d.line((xa, tb0, xa, tm), fill=putih, width=2)
    d.line((xb, tm, xb, tb1), fill=putih, width=2)
    d.line((xb + (W - 70 - xb) * 0.6, tm, xb + (W - 70 - xb) * 0.6, tb1), fill=putih, width=2)
    sel = [(70, tb0, xa, "PROYEK", proyek), (xa, tb0, W - 70, "TANGGAL", p.get("_tanggal", "").upper()),
           (70, tm, xb, "PERANCANG", "TUHAN"), (xb, tm, xb + (W - 70 - xb) * 0.6, "DIGAMBAR", "@" + HANDLE),
           (xb + (W - 70 - xb) * 0.6, tm, W - 70, "LEMBAR", f"0{i + 1}/03")]
    for x0, y0, x1, lab, val in sel:
        renggang(d, (x0 + 16, y0 + 26), lab, din(18), redup, 2)
        fv = muat(d, val, din, x1 - x0 - 32, 36, 16)
        d.text((x0 + 16, y0 + 72), val, font=fv, fill=putih, anchor="ls")
    return img


# ---------- PERPUS: kartu pinjam perpustakaan ----------

PERPUS_WARNA = [(46, 82, 66), (112, 40, 48), (34, 52, 94)]


def kertas_sampul(w, h, warna, seed):
    """Kertas sampul dalam buku tua: warna tua + kisi belah ketupat samar."""
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    a *= (0.88 + 0.2 * render.fbm2d(h, w, rng, ((3, 1.0), (20, 0.5), (120, 0.35))))[..., None]
    yy, xx = np.mgrid[0:h, 0:w]
    kisi = (((xx + yy) % 48) < 2) | (((xx - yy) % 48) < 2)
    titik = ((((xx + 24) % 48 - 24) ** 2 + ((yy) % 48 - 24) ** 2) < 10)
    a *= (1 + 0.12 * kisi + 0.15 * titik)[..., None]
    return grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05)


def perpus_image(p, i):
    rng = np.random.default_rng(15400 + i)
    img = kertas_sampul(W, H, PERPUS_WARNA[i % 3], 15400 + i).convert("RGBA")
    ungu, merah = (92, 60, 156), (196, 38, 46)
    # kartu pinjam
    cw, ch = 660, 900
    card = kertas(cw, ch, (250, 245, 226), 15410 + i, 0.03, 80).convert("RGBA")
    cd = ImageDraw.Draw(card)
    coklat = (70, 56, 46)
    cd.text((cw / 2, 24), "KARTU PINJAM", font=mesin(36, 2), fill=coklat, anchor="ma")
    cd.text((cw - 26, 30), f"No. {270 + i * 13:04d}", font=mesin(18), fill=(130, 116, 100), anchor="ra")
    cd.line((26, 80, cw - 26, 80), fill=(196, 72, 64), width=3)
    cd.line((26, 86, cw - 26, 86), fill=(196, 72, 64), width=1)
    for k, (lab, val) in enumerate((("Judul", bersih(p["buku"])), ("Pengarang", bersih(p["pengarang"])))):
        y = 100 + k * 58
        cd.text((26, y + 34), lab, font=mesin(20), fill=(140, 124, 106), anchor="ls")
        fv = muat(cd, val, lambda s: mesin(s, 3), cw - 170 - 26, 32, 18)
        cd.text((166, y + 34), val, font=fv, fill=(36, 32, 30), anchor="ls")
        for x in range(166, cw - 26, 10):
            cd.line((x, y + 44, x + 4, y + 44), fill=(170, 156, 140), width=1)
    ty, rh = 226, 64
    cd.line((26, ty, cw - 26, ty), fill=coklat, width=2)
    cd.text((26 + 95, ty + 14), "TGL. KEMBALI", font=mesin(17, 2), fill=coklat, anchor="ma")
    cd.text((214 + (cw - 26 - 214) / 2, ty + 14), "PEMINJAM / CATATAN", font=mesin(17, 2), fill=coklat, anchor="ma")
    cd.line((26, ty + 46, cw - 26, ty + 46), fill=coklat, width=2)
    k = 1
    while ty + 46 + k * rh < ch - 20:
        cd.line((26, ty + 46 + k * rh, cw - 26, ty + 46 + k * rh), fill=(170, 196, 226), width=1)
        k += 1
    cd.line((214, ty, 214, ch - 30), fill=coklat, width=2)
    tangan_ = [lambda s: tangan(s), lambda s: spidol(s), lambda s: kuas(int(s * 1.35))]
    tinta_ = [(30, 52, 132), (36, 36, 40), (24, 86, 120), (110, 40, 60)]
    for k, (tgl, cat) in enumerate(p["pinjam"][:4]):
        y = ty + 46 + k * rh
        teks = bersih(tgl).upper()
        m = Image.new("L", (200, 60), 0)
        md = ImageDraw.Draw(m)
        fs = muat(md, teks, din, 168, 34, 18)
        md.text((100, 32), teks, font=fs, fill=255, anchor="mm")
        m = m.rotate(rng.uniform(-6, 6), resample=Image.BICUBIC)
        tempel_tinta(card, m, (20, y + 3), ungu, 15420 + i * 7 + k, kuat=0.86, kasar=0.5)
        fn_ = tangan_[k % 3]
        fc = muat(cd, bersih(cat), fn_, cw - 26 - 236, 34, 18)
        ImageDraw.Draw(card).text((232, y + rh * 0.7), bersih(cat), font=fc, fill=tinta_[k % 4], anchor="ls")
    # cap besar di baris kosong kartu
    cap = bersih(p["cap"]).upper()
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    fc = muat(probe, cap, din, 500, 62, 20)
    baris = [cap]
    if fc.size < 46 and " " in cap:
        kata = cap.split()
        pot = min(range(1, len(kata)), key=lambda k: max(len(" ".join(kata[:k])), len(" ".join(kata[k:]))))
        baris = [" ".join(kata[:pot]), " ".join(kata[pot:])]
        fc = din(48)
        while max(probe.textlength(b, font=fc) for b in baris) > 500 and fc.size > 24:
            fc = din(fc.size - 2)
    lebar = max(probe.textlength(b, font=fc) for b in baris) + 64
    tinggi = len(baris) * fc.size * 0.98 + 44
    m = Image.new("L", (int(lebar) + 40, int(tinggi) + 40), 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle((20, 20, 20 + lebar, 20 + tinggi), radius=14, outline=255, width=7)
    md.rounded_rectangle((32, 32, 8 + lebar, 8 + tinggi), radius=8, outline=255, width=2)
    for k, b in enumerate(baris):
        md.text((20 + lebar / 2, 20 + 22 + (k + 0.82) * fc.size * 0.98), b, font=fc, fill=255, anchor="ms")
    m = m.rotate((-6 if i % 2 == 0 else 5) if len(baris) == 1 else (-4 if i % 2 == 0 else 4), expand=True, resample=Image.BICUBIC)
    ycap = ty + 46 + 4 * rh + 12 + max(0, (ch - 175 - (ty + 46 + 4 * rh + 12) - m.height) / 2)
    tempel_tinta(card, m, (cw / 2 - m.width / 2, ycap), merah, 15440 + i, kuat=0.86, kasar=0.8)
    card = card.rotate(-1.4, expand=True, resample=Image.BICUBIC)
    bayangan(img, card, ((W - card.width) / 2 + 6, 46), blur=14, geser=(4, 10), kuat=0.5)
    # kantong manila
    px0, py0, px1, py1 = 140, 790, 940, 1254
    pw, ph = px1 - px0, py1 - py0
    kantong = kertas(pw, ph, (232, 206, 152), 15430 + i, 0.05, 160).convert("RGBA")
    kd = ImageDraw.Draw(kantong)
    lipat = (206, 178, 124)
    kd.rectangle((0, 0, 22, ph), fill=lipat)
    kd.rectangle((pw - 22, 0, pw, ph), fill=lipat)
    kd.rectangle((0, ph - 22, pw, ph), fill=lipat)
    kd.line((22, 0, 22, ph - 22), fill=(176, 148, 98), width=2)
    kd.line((pw - 22, 0, pw - 22, ph - 22), fill=(176, 148, 98), width=2)
    kd.line((22, ph - 22, pw - 22, ph - 22), fill=(176, 148, 98), width=2)
    mask = Image.new("L", (pw * 2, ph * 2), 255)
    ImageDraw.Draw(mask).ellipse((pw - 150, -150, pw + 150, 150), fill=0)
    kantong.putalpha(mask.resize((pw, ph), Image.LANCZOS))
    kd = ImageDraw.Draw(kantong)
    tinta_cetak = (84, 58, 36)
    renggang(kd, (pw / 2, 104), "PERPUSTAKAAN DIAM DAN PERCAYA", mesin(20, 2), tinta_cetak, 4, anchor="ms")
    kd.line((pw / 2 - 120, 124, pw / 2 + 120, 124), fill=tinta_cetak, width=2)
    ruang = ph - 150 - 100
    f, vl, size = pas_aman(kd, bersih(p["ayat"]), lambda s: mesin(s), pw - 130, ruang, 36, 22, 1.38)
    yy = 150 + max(0, (ruang - len(vl) * size * 1.38) / 2)
    for ln in vl:
        kd.text((pw / 2, yy), ln, font=f, fill=(58, 42, 30), anchor="ma")
        yy += size * 1.38
    kd.text((pw / 2, yy + 12), p["ref"].upper(), font=mesin(28, 2), fill=tinta_cetak, anchor="ma")
    kd.text((pw / 2, ph - 36), "@" + HANDLE, font=mesin(20), fill=(140, 112, 76), anchor="ms")
    bayangan(img, kantong, (px0, py0), blur=10, geser=(0, 8), kuat=0.5)
    return img


# ---------- CENTANG: aplikasi to-do ----------

CENTANG_WARNA = [((10, 122, 255), (244, 246, 251)), ((40, 164, 96), (245, 248, 244)), ((244, 112, 54), (250, 247, 242))]


def cek(d, cx, cy, r, col):
    d.line([(cx - r * 0.42, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.34), (cx + r * 0.46, cy - r * 0.32)], fill=col, width=max(2, int(r * 0.2)), joint="curve")


def centang_image(p, i):
    aksen, bg = CENTANG_WARNA[i % 3]
    img = gradasi(W, H, bg, campur(bg, (255, 255, 255), 0.6)).convert("RGBA")
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    d = ImageDraw.Draw(img)
    gelap, abu = (24, 24, 30), (138, 138, 150)
    # status bar
    d.text((84, 50), p.get("_jam", "06.00"), font=sf(30, "Semibold"), fill=gelap, anchor="lm")
    for k in range(4):
        d.rounded_rectangle((W - 214 + k * 12, 58 - 8 - k * 5, W - 206 + k * 12, 60), radius=2, fill=gelap)
    d.rounded_rectangle((W - 150, 38, W - 92, 62), radius=7, outline=gelap, width=2)
    d.rounded_rectangle((W - 146, 42, W - 108, 58), radius=4, fill=gelap)
    d.rounded_rectangle((W - 89, 45, W - 85, 55), radius=2, fill=gelap)
    tugas = [(bersih(t), bool(s)) for t, s in p["tugas"]][:5]
    selesai = sum(s for _, s in tugas)
    # tanggal, judul, cincin
    d.text((70, 168), tanpa_tahun(p.get("_tanggal_panjang", "")).upper(), font=sf(26, "Semibold"), fill=aksen, anchor="ls")
    judul = bersih(p["judul"])
    fj = muat(d, judul, lambda s: sf(s, "Bold"), W - 140 - 230, 84, 44)
    d.text((70, 252), judul, font=fj, fill=gelap, anchor="ls")
    d.text((70, 304), f"{selesai} dari {len(tugas)} selesai", font=sf(30), fill=abu, anchor="ls")
    cx, cy, r = W - 160, 222, 80
    ld.ellipse([v * S for v in (cx - r, cy - r, cx + r, cy + r)], outline=(226, 228, 236, 255), width=18 * S)
    if selesai:
        ld.arc([v * S for v in (cx - r, cy - r, cx + r, cy + r)], -90, -90 + 360 * selesai / len(tugas), fill=aksen + (255,), width=18 * S)
        ujung = math.radians(-90 + 360 * selesai / len(tugas))
        for a_ in (math.radians(-90), ujung):
            ex, ey = cx + (r - 9) * math.cos(a_), cy + (r - 9) * math.sin(a_)
            ld.ellipse([v * S for v in (ex - 9, ey - 9, ex + 9, ey + 9)], fill=aksen + (255,))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    d.text((cx, cy - 4), f"{round(100 * selesai / len(tugas))}%", font=sf(36, "Bold"), fill=gelap, anchor="mm")
    d.text((cx, cy + 30), "hari ini", font=sf(18, "Medium"), fill=abu, anchor="mm")
    # daftar tugas
    rh = 98 if len(tugas) >= 5 else 106
    ky0 = 344
    ky1 = ky0 + rh * len(tugas)
    kartu = Image.new("RGBA", (W - 120, ky1 - ky0), (255, 255, 255, 255))
    mask = Image.new("L", ((W - 120) * 3, (ky1 - ky0) * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mask.width - 1, mask.height - 1), radius=34 * 3, fill=255)
    kartu.putalpha(mask.resize(kartu.size, Image.LANCZOS))
    bayangan(img, kartu, (60, ky0), blur=18, geser=(0, 8), kuat=0.1)
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    d = ImageDraw.Draw(img)
    ft_ = lambda s: sf(s, "Medium")
    fmax = 38
    for t, _ in tugas:
        fmax = min(fmax, muat(d, t, ft_, W - 60 - 160 - 40, 38, 24).size)
    f = ft_(fmax)
    for k, (t, s) in enumerate(tugas):
        y = ky0 + k * rh
        cy_ = y + rh / 2
        if k:
            d.line((160, y, W - 60, y), fill=(232, 233, 238), width=2)
        box = [v * S for v in (110 - 26, cy_ - 26, 110 + 26, cy_ + 26)]
        if s:
            ld.ellipse(box, fill=aksen + (255,))
            cek(ld, 110 * S, cy_ * S, 26 * S, (255, 255, 255, 255))
        else:
            ld.ellipse(box, outline=(196, 198, 208, 255), width=4 * S)
        d.text((160, cy_), t, font=f, fill=abu if s else gelap, anchor="lm")
        if s:
            tw = d.textlength(t, font=f)
            d.line((160, cy_ + 2, 160 + tw, cy_ + 2), fill=(170, 170, 180), width=3)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # catatan ayat
    ny0, ny1 = ky1 + 30, H - 150
    nw = W - 120
    nota = Image.new("RGBA", (nw, int(ny1 - ny0)), campur(aksen, (255, 255, 255), 0.9) + (255,))
    mask = Image.new("L", (nota.width * 3, nota.height * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mask.width - 1, mask.height - 1), radius=30 * 3, fill=255)
    nota.putalpha(mask.resize(nota.size, Image.LANCZOS))
    nd = ImageDraw.Draw(nota)
    nd.rounded_rectangle((34, 36, 40, nota.height - 36), radius=3, fill=aksen)
    nd.text((66, 54), "CATATAN", font=sf(22, "Bold"), fill=aksen, anchor="ls")
    fa, vl, size = pas_aman(nd, tanpa_kutip(p["ayat"]), lambda s: iowan(s, 2), nw - 120, nota.height - 140, 40, 24, 1.32)
    yy = 80 + max(0, (nota.height - 140 - len(vl) * size * 1.32) / 2)
    for ln in vl:
        nd.text((66, yy), ln, font=fa, fill=gelap)
        yy += size * 1.32
    nd.text((66, yy + 10), p["ref"], font=sf(28, "Semibold"), fill=aksen)
    img.alpha_composite(nota, (60, int(ny0)))
    # tombol tambah
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    fx, fy = W - 112, H - 78
    ld.ellipse([v * S for v in (fx - 42, fy - 42, fx + 42, fy + 42)], fill=aksen + (255,))
    ld.line([v * S for v in (fx - 16, fy, fx + 16, fy)], fill=(255, 255, 255, 255), width=6 * S)
    ld.line([v * S for v in (fx, fy - 16, fx, fy + 16)], fill=(255, 255, 255, 255), width=6 * S)
    sh = lay.resize((W, H), Image.LANCZOS)
    bayangan(img, sh, (0, 0), blur=12, geser=(0, 6), kuat=0.25)
    kredit(img, (70, H - 78), abu, anchor="lm", font=sf(24, "Medium"))
    return img


# ---------- SWISS: poster tipografi Swiss ----------

def swiss_image(p, i):
    rng = np.random.default_rng(15500 + i)
    kertas_ = (242, 240, 233)
    img = kertas(W, H, kertas_, 15500 + i, 0.025, 60).convert("RGBA")
    hitam, merah = (20, 20, 20), (226, 38, 28)
    S = 2
    v = i % 3
    angka = bersih(str(p["angka"]))
    # angka besar
    fa = helv(560, 1)
    probe = ImageDraw.Draw(img)
    while True:
        bb = probe.textbbox((0, 0), angka, font=fa, anchor="ls")
        if bb[2] - bb[0] <= (W - 140 if v != 1 else W - 340) and bb[3] - bb[1] <= 470:
            break
        fa = helv(fa.size - 10, 1)
    bb = probe.textbbox((0, 0), angka, font=fa, anchor="ls")
    base = 636
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    if v == 0:  # lingkaran merah menumpuk sebagian angka
        r = 232
        ax, warna_a = 62 - bb[0], hitam
        cx, cy = min(W - 70 - r, ax + bb[2] + r * 0.42), 154 + r
        ld.ellipse([q * S for q in (cx - r, cy - r, cx + r, cy + r)], fill=merah + (255,))
    elif v == 1:  # balok merah mengisi ruang kiri sampai dekat angka
        ax, warna_a = W - 70 - bb[2], hitam
        ld.rectangle([q * S for q in (70, 150, max(250, ax + bb[0] - 44), base)], fill=merah + (255,))
    else:
        r = 236
        cx, cy = 70 + r, 150 + r
        ld.ellipse([q * S for q in (cx - r, cy - r, cx + r, cy + r)], outline=hitam + (255,), width=4 * S)
        ld.ellipse([q * S for q in (W - 70 - 60, 150, W - 70, 210)], fill=hitam + (255,))
        ax, warna_a = W - 70 - bb[2], merah
    lingkaran = lay.resize((W, H), Image.LANCZOS)
    img.alpha_composite(lingkaran)
    angka_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(angka_l).text((ax, base), angka, font=fa, fill=warna_a + (255,), anchor="ls")
    if v == 0:  # di dalam lingkaran merah angkanya 'dilubangi' jadi warna kertas
        al = np.asarray(angka_l).astype(np.float32)[..., 3:] / 255
        di_dalam = np.asarray(lingkaran).astype(np.float32)[..., 3:] / 255
        warna = np.array(warna_a, np.float32) * (1 - di_dalam) + np.array(kertas_, np.float32) * di_dalam
        a = np.asarray(img).astype(np.float32)
        a[..., :3] = a[..., :3] * (1 - al) + warna * al
        img = Image.fromarray(a.astype(np.uint8))
    else:
        img.alpha_composite(angka_l)
    d = ImageDraw.Draw(img)
    # baris meta + garis
    d.text((70, 76), "TENANG", font=helv(22, 1), fill=hitam, anchor="ls")
    d.text((400, 76), p.get("_tgl_titik", "03.01.2027"), font=helv(22), fill=hitam, anchor="ls")
    d.text((W - 70, 76), f"Nº {15:02d}/{i + 1}", font=helv(22), fill=hitam, anchor="rs")
    d.line((70, 100, W - 70, 100), fill=hitam, width=2)
    d.line((70, 676, W - 70, 676), fill=hitam, width=2)
    # judul
    judul = bersih(p["judul"])
    fj, jl, js = pas_aman(d, judul, lambda s: helv(s, 1), W - 140, 168, 84, 46, 1.02)
    y = 704
    for ln in jl:
        d.text((66, y + js * 0.8), ln, font=fj, fill=hitam, anchor="ls")
        y += js * 1.02
    # dua kolom baris
    y += 22
    kol = [(70, 520), (560, W - 70)]
    fb = helv(32, 0)
    tinggi = 0
    for (x0, x1), teks in zip(kol, p["baris"][:2]):
        bl = wrap(d, bersih(teks), fb, x1 - x0)
        for k, ln in enumerate(bl):
            d.text((x0, y + k * 40), ln, font=fb, fill=hitam)
        tinggi = max(tinggi, len(bl) * 40)
    d.rectangle((70, y - 18, 86, y - 14), fill=merah)
    y += tinggi + 26
    d.line((70, y, W - 70, y), fill=hitam, width=2)
    # ayat di grid: label kiri, teks kanan
    y += 30
    d.text((70, y + 6), "Ayat", font=helv(26, 1), fill=merah)
    d.text((70, y + 40), "Alkitab TB", font=helv(22), fill=hitam)
    fa_, vl, size = pas_aman(d, tanpa_kutip(p["ayat"]), lambda s: helv(s, 0), W - 70 - 330, H - 120 - y - 70, 38, 22, 1.28)
    for ln in vl:
        d.text((330, y), ln, font=fa_, fill=hitam)
        y += size * 1.28
    d.text((330, y + 14), p["ref"], font=helv(30, 1), fill=hitam)
    # kaki
    d.line((70, H - 96, W - 70, H - 96), fill=hitam, width=1)
    d.text((70, H - 62), "@" + HANDLE, font=helv(22, 1), fill=hitam, anchor="ls")
    d.text((W - 70, H - 62), "Diam dan percaya.", font=helv(22), fill=hitam, anchor="rs")
    return img


# ---------- LAPIS: pemandangan kertas berlapis ----------

LAPIS_WARNA = [  # langit atas, langit bawah, bukit belakang -> depan, matahari, judul
    ((252, 218, 196), (255, 240, 222), [(246, 198, 178), (238, 166, 154), (212, 124, 130), (160, 84, 112), (104, 54, 92), (60, 34, 66)],
     (255, 247, 228), (96, 44, 76)),
    ((204, 230, 236), (250, 244, 224), [(188, 222, 202), (142, 196, 172), (94, 160, 142), (54, 122, 112), (30, 88, 86), (16, 56, 58)],
     (255, 236, 186), (20, 74, 74)),
    ((220, 216, 246), (252, 228, 216), [(208, 200, 238), (170, 160, 222), (130, 120, 198), (92, 84, 162), (58, 56, 120), (30, 30, 78)],
     (255, 224, 210), (44, 40, 104)),
]


def lapis_image(p, i):
    rng = np.random.default_rng(15600 + i)
    atas, bawah, bukit, matahari, wjudul = LAPIS_WARNA[i % 3]
    img = grain(gradasi(W, H, atas, bawah), 0.02).convert("RGBA")
    d = ImageDraw.Draw(img)

    def tekstur(col, w, h, seed):
        r = np.random.default_rng(seed)
        a = np.zeros((h, w, 3), np.float32) + np.array(col, np.float32)
        yy = np.linspace(0, 1, h)[:, None, None]
        a *= 1.06 - 0.12 * yy
        a *= (0.97 + 0.05 * render.fbm2d(h, w, r, ((6, 1.0), (40, 0.5), (200, 0.4))))[..., None]
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

    def tempel(mask, col, seed, kuat=0.38):
        m = mask.convert("L")
        lapisan = tekstur(col, W, H, seed)
        lapisan.putalpha(m)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh.putalpha(m.point(lambda v: int(v * kuat)))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        img.alpha_composite(sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, 5)))  # bayang sedikit naik ke lapisan belakang
        img.alpha_composite(lapisan)

    # matahari (cincin kertas)
    sx, sy = W * [0.7, 0.3, 0.66][i % 3], 532
    for k, (rr, t) in enumerate(((132, 0.0), (106, 0.35), (80, 0.7))):
        m = Image.new("L", (W * 2, H * 2), 0)
        ImageDraw.Draw(m).ellipse(((sx - rr) * 2, (sy - rr) * 2, (sx + rr) * 2, (sy + rr) * 2), fill=255)
        tempel(m.resize((W, H), Image.LANCZOS), campur(matahari, (255, 255, 255), t), 15610 + k, 0.22)
    # awan kertas
    for k in range(2):
        cx, cy = (W * 0.2, 470) if k == 0 else (W * 0.84, 440)
        cx += rng.uniform(-30, 30)
        m = Image.new("L", (W * 2, H * 2), 0)
        md = ImageDraw.Draw(m)
        for dx, dy, rr in ((-70, 10, 44), (-20, -18, 60), (44, -4, 50), (90, 14, 36)):
            md.ellipse(((cx + dx - rr) * 2, (cy + dy - rr) * 2, (cx + dx + rr) * 2, (cy + dy + rr) * 2), fill=255)
        md.rectangle(((cx - 130) * 2, (cy + 10) * 2, (cx + 140) * 2, (cy + 90) * 2), fill=0)
        tempel(m.resize((W, H), Image.LANCZOS), (255, 252, 246), 15620 + k, 0.2)
    # burung kecil di sisi yang jauh dari matahari
    lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    bx0 = W * (0.36 if sx > W / 2 else 0.6)
    for k, (dx, dy, sk) in enumerate(((0, 0, 1.0), (54, 22, 0.8), (-40, 34, 0.7))):
        bx, by, u = bx0 + dx, 405 + dy, 20 * sk
        pts = [(bx - u, by - u * 0.45), (bx - u * 0.45, by - u * 0.25), (bx, by + u * 0.15), (bx + u * 0.45, by - u * 0.25), (bx + u, by - u * 0.45)]
        ld.line([(x * 2, y * 2) for x, y in pts], fill=campur(wjudul, atas, 0.25) + (255,), width=6, joint="curve")
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # bukit berlapis
    dasar = [540, 640, 735, 815, 878, 936]
    amp = [80, 66, 52, 44, 34, 26]
    for k in range(6):
        xs = np.linspace(-10, W + 10, 160)
        f1, f2, f3 = rng.uniform(0.7, 1.4), rng.uniform(1.8, 3.2), rng.uniform(4, 7)
        ph1, ph2, ph3 = rng.uniform(0, 6.28, 3)
        ys = dasar[k] + amp[k] * (0.65 * np.sin(xs / W * 2 * np.pi * f1 + ph1) + 0.28 * np.sin(xs / W * 2 * np.pi * f2 + ph2)
                                  + 0.08 * np.sin(xs / W * 2 * np.pi * f3 + ph3))
        if k == 5:
            ys = np.minimum(ys, 960)
        m = Image.new("L", (W * 2, H * 2), 0)
        md = ImageDraw.Draw(m)
        md.polygon([(x * 2, y * 2) for x, y in zip(xs, ys)] + [((W + 10) * 2, H * 2), (-20, H * 2)], fill=255)
        if k == 4:  # pohon cemara kertas di lapisan kedua dari depan
            for tx in rng.uniform(60, W - 60, 6):
                ty = float(np.interp(tx, xs, ys)) + 6
                th_ = rng.uniform(70, 110)
                for s in range(3):
                    w_ = th_ * (0.36 - s * 0.08)
                    y_ = ty - th_ * (0.25 + s * 0.28)
                    md.polygon([((tx - w_) * 2, (y_ + th_ * 0.32) * 2), (tx * 2, (y_ - th_ * 0.22) * 2), ((tx + w_) * 2, (y_ + th_ * 0.32) * 2)], fill=255)
                md.rectangle(((tx - 5) * 2, (ty - th_ * 0.2) * 2, (tx + 5) * 2, (ty + 4) * 2), fill=255)
        tempel(m.resize((W, H), Image.LANCZOS), bukit[k], 15630 + k + i * 10, 0.42)
    d = ImageDraw.Draw(img)
    # judul di langit
    judul = bersih(p["judul"])
    fj, jl, js = pas_aman(d, judul, lambda s: avenir(s, 0), W - 200, 196, 78, 44, 1.1)
    y = 164 + max(0, (196 - len(jl) * js * 1.1) / 2)
    for ln in jl:
        d.text((W / 2, y), ln, font=fj, fill=wjudul, anchor="ma")
        y += js * 1.1
    renggang(d, (W / 2, 140), tanpa_tahun(p.get("_tanggal_panjang", "")).upper(), avenir(20, 2), campur(wjudul, atas, 0.35), 4, anchor="ms")
    # ayat di lapisan depan
    krem = (255, 244, 230)
    f, vl, size = pas_aman(d, bersih(p["ayat"]), lambda s: georgia(s, True), W - 200, 1238 - 1000 - 50, 38, 22, 1.34)
    yy = 1000 + max(0, (1238 - 1000 - 50 - len(vl) * size * 1.34) / 2)
    for ln in vl:
        d.text((W / 2, yy), ln, font=f, fill=krem, anchor="ma")
        yy += size * 1.34
    d.text((W / 2, yy + 10), p["ref"], font=avenir(30, 0), fill=matahari, anchor="ma")
    kredit(img, (W / 2, H - 46), campur(krem, bukit[5], 0.4))
    return img


# ---------- SULAM: sulaman kristik di ram kayu ----------

HURUF5 = {
    "A": ".###. #...# #...# ##### #...# #...# #...#", "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.", "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####", "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####", "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": ".###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.", "J": "..### ...#. ...#. ...#. ...#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#", "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#", "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.", "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#", "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.", "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.", "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.", "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..", "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.", "1": "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    "2": ".###. #...# ....# ...#. ..#.. .#... #####", "3": "####. ....# ....# .###. ....# ....# ####.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.", "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": "..##. .#... #.... ####. #...# #...# .###.", "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.", "9": ".###. #...# #...# .#### ....# ...#. .##..",
    "!": "# # # # # . #", "?": ".###. #...# ....# ...#. ..#.. ..... ..#..", ".": ". . . . . . #", ",": ".. .. .. .. .. .# #.",
    "-": "... ... ... ### ... ... ...", "'": "# # . . . . .", ":": ". . # . . # .", " ": "... ... ... ... ... ... ...",
}
MOTIF = {
    "hati": ".##.##. ####### ####### .#####. ..###.. ...#...",
    "bunga": ".a. aya .a. .g. gg.",
    "salib": ".#. ### .#. .#.",
}


def glyph(c):
    return [list(r) for r in HURUF5.get(c, HURUF5[" "]).split()]


def linen(w, h, warna, seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    anyam = 0.025 * np.sin(xx * 1.9 + rng.uniform(0, 6)) + 0.025 * np.sin(yy * 2.1)
    a *= (1 + anyam + 0.06 * (render.fbm2d(h, w, rng, ((4, 1.0), (40, 0.5), (300, 0.5))) - 0.5))[..., None]
    a *= (1 - 0.04 * (rng.random((h, 1)) < 0.08))[..., None]  # benang tebal sesekali
    return grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05)


SULAM_WARNA = [  # latar linen, benang teks, benang motif, kelopak, tengah bunga
    ((234, 216, 208), (172, 36, 50), (60, 112, 84), (226, 108, 120), (240, 190, 70)),
    ((210, 220, 228), (34, 58, 122), (206, 146, 46), (120, 160, 214), (250, 214, 100)),
    ((216, 224, 206), (42, 100, 72), (200, 98, 116), (236, 150, 160), (246, 206, 96)),
]


def sulam_image(p, i):
    rng = np.random.default_rng(15700 + i)
    latar, c_teks, c_motif, c_kelopak, c_tengah = SULAM_WARNA[i % 3]
    daun = (78, 132, 86)
    img = linen(W, H, latar, 15700 + i).convert("RGBA")
    baris = []
    for ln in str(p["teks"]).split("\n"):
        ln = re.sub(r"[^A-Z0-9!?.,'\-: ]", "", bersih(ln).upper()).strip()
        if ln:
            baris.append(ln)
    baris = baris[:2] or ["TENANG"]
    # susun grid jahitan: teks + motif
    sel = []  # (gx, gy, warna)

    def lebar_baris(t):
        return sum(len(glyph(c)[0]) for c in t) + len(t) - 1

    kol = max(lebar_baris(t) for t in baris)
    gy = 0
    for t in baris:
        gx = (kol - lebar_baris(t)) // 2
        for c in t:
            g = glyph(c)
            for ry, row in enumerate(g):
                for rx, ch in enumerate(row):
                    if ch == "#":
                        sel.append((gx + rx, gy + ry, c_teks))
            gx += len(g[0]) + 1
        gy += 7 + 3
    tinggi_teks = gy - 3
    # baris motif di atas & bawah
    urut = ["bunga", "hati", "bunga", "hati", "bunga"] if kol >= 34 else ["bunga", "hati", "bunga"]
    if kol < 22:
        urut = ["hati", "bunga", "hati"] if kol >= 14 else ["hati"]
    lebar_m = sum(len(MOTIF[m].split()[0]) for m in urut) + 3 * (len(urut) - 1)
    peta = {"#": None, "a": c_kelopak, "y": c_tengah, "g": daun}
    for oy, terbalik in ((-4 - 6, False), (tinggi_teks + 4, True)):
        gx = (kol - lebar_m) // 2
        for k, m in enumerate(urut):
            rows = MOTIF[m].split()
            mh = len(rows)
            for ry, row in enumerate(rows):
                for rx, ch in enumerate(row):
                    if ch != ".":
                        col = peta[ch] or (c_motif if m == "hati" else c_teks)
                        sel.append((gx + rx, oy + (6 - mh) + ry, col))
            gx += len(rows[0]) + 3
    gmin = min(s[1] for s in sel)
    gmax = max(s[1] for s in sel)
    rows_total = gmax - gmin + 1
    cx, cy, R = W / 2, 500, 376
    s = int(min(26, 640 / kol, 470 / rows_total))
    ox = cx - kol * s / 2
    oy = cy - (gmin + rows_total / 2) * s
    # kain aida di dalam ram
    box = (int(cx - R), int(cy - R), int(cx + R), int(cy + R))
    bw = box[2] - box[0]
    yy, xx = np.mgrid[box[1]:box[3], box[0]:box[2]].astype(np.float32)
    u, v = ((xx - ox) % s) / s, ((yy - oy) % s) / s
    du, dv = np.minimum(u, 1 - u), np.minimum(v, 1 - v)
    lubang = np.exp(-(du ** 2 + dv ** 2) / 0.012)
    tenun = 1 - 4 * ((u - 0.5) ** 2 + (v - 0.5) ** 2)
    kain = np.zeros((bw, bw, 3), np.float32) + np.array([246, 241, 228], np.float32)
    kain *= (1 - 0.3 * lubang + 0.035 * tenun)[..., None]
    kain *= (0.97 + 0.04 * render.fbm2d(bw, bw, rng, ((5, 1.0), (30, 0.5))))[..., None]
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    kain *= (1 - 0.18 * np.clip((r - (R - 60)) / 60, 0, 1) ** 1.5)[..., None]
    kain_img = Image.fromarray(np.clip(kain, 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (bw * 3, bw * 3), 0)
    ImageDraw.Draw(m).ellipse((0, 0, bw * 3 - 1, bw * 3 - 1), fill=255)
    kain_img.putalpha(m.resize((bw, bw), Image.LANCZOS))
    # bayangan ram di linen
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - R - 34, cy - R - 34 + 14, cx + R + 34 + 8, cy + R + 34 + 22), fill=(40, 30, 20, 110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(kain_img, (box[0], box[1]))
    # jahitan silang (2x)
    K = 2
    lay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    bay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
    ld, bd = ImageDraw.Draw(lay), ImageDraw.Draw(bay)
    tw = max(2, s * 0.34) * K
    mg = s * 0.1
    # pinggiran tusuk jelujur melingkar
    rb = R - 26
    n = int(2 * math.pi * rb / (s * 1.7))
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 0.55) / n
        pts = [((cx + rb * math.cos(a)) * K, (cy + rb * math.sin(a)) * K) for a in np.linspace(a0, a1, 4)]
        ld.line(pts, fill=c_motif + (255,), width=int(max(2, s * 0.26) * K))
    for gx, gy_, col in sel:
        x0, y0 = ox + gx * s + mg, oy + gy_ * s + mg
        x1, y1 = ox + (gx + 1) * s - mg, oy + (gy_ + 1) * s - mg
        var = rng.uniform(0.9, 1.06)
        c1 = tuple(int(min(255, c * var * 0.82)) for c in col) + (255,)
        c2 = tuple(int(min(255, c * var)) for c in col) + (255,)
        hl = tuple(int(min(255, c * var + (255 - c) * 0.35)) for c in col) + (200,)
        j = lambda: rng.uniform(-0.6, 0.6)
        bd.line(((x0 + 1) * K, (y0 + 1.5) * K, (x1 + 1) * K, (y1 + 1.5) * K), fill=(0, 0, 0, 120), width=int(tw))
        bd.line(((x0 + 1) * K, (y1 + 1.5) * K, (x1 + 1) * K, (y0 + 1.5) * K), fill=(0, 0, 0, 120), width=int(tw))
        ld.line(((x0 + j()) * K, (y0 + j()) * K, (x1 + j()) * K, (y1 + j()) * K), fill=c1, width=int(tw))
        ax, ay, bx, by = x0 + j(), y1 + j(), x1 + j(), y0 + j()
        ld.line((ax * K, ay * K, bx * K, by * K), fill=c2, width=int(tw))
        ld.line(((ax + (bx - ax) * 0.2) * K, (ay + (by - ay) * 0.2 - s * 0.06) * K, (ax + (bx - ax) * 0.75) * K, (ay + (by - ay) * 0.75 - s * 0.06) * K),
                fill=hl, width=int(max(1, tw * 0.3)))
    img.alpha_composite(bay.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2)))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
    # ram kayu (2 cincin) + sekrup
    Rr0, Rr1 = R - 6, R + 34
    ring = np.zeros((2 * Rr1 + 4, 2 * Rr1 + 4, 3), np.float32)
    n_ = ring.shape[0]
    yy, xx = np.mgrid[0:n_, 0:n_].astype(np.float32) - n_ / 2
    rr = np.sqrt(xx ** 2 + yy ** 2)
    th = np.arctan2(yy, xx)
    kayu = np.array([212, 168, 118], np.float32)
    serat = 0.06 * np.sin(rr * 1.3 + 3 * np.sin(th * 5)) + 0.04 * np.sin(rr * 3.1)
    cahaya_ = 1 + 0.13 * np.cos(th + 2.3) - 0.06 * ((rr - (Rr0 + Rr1) / 2) / ((Rr1 - Rr0) / 2)) ** 2
    ring = kayu * (cahaya_ + serat)[..., None]
    garis_tengah = np.exp(-((rr - (R + 12)) / 1.4) ** 2)
    ring *= (1 - 0.35 * garis_tengah)[..., None]
    alpha = np.clip(np.minimum(rr - Rr0, Rr1 - rr) + 0.5, 0, 1)
    ring_img = Image.fromarray(np.dstack([np.clip(ring, 0, 255), alpha * 255]).astype(np.uint8), "RGBA")
    bayangan(img, ring_img, (cx - n_ / 2, cy - n_ / 2), blur=6, geser=(3, 5), kuat=0.35)
    # penjepit & sekrup di atas
    d = ImageDraw.Draw(img)
    ty = cy - Rr1
    for bx0 in (cx - 42, cx + 8):
        d.rounded_rectangle((bx0, ty - 34, bx0 + 34, ty + 10), radius=6,
                            fill=campur(tuple(int(c) for c in kayu), (90, 60, 30), 0.2), outline=campur(tuple(int(c) for c in kayu), (60, 40, 20), 0.5), width=2)
    sekrup = sprite(220, 44, lambda dd, k: (
        dd.rounded_rectangle((20 * k, 14 * k, 180 * k, 30 * k), radius=8 * k, fill=(196, 160, 84, 255)),
        dd.rectangle((20 * k, 16 * k, 180 * k, 19 * k), fill=(240, 216, 150, 255)),
        [dd.line(((30 + q * 9) * k, 14 * k, (34 + q * 9) * k, 30 * k), fill=(150, 116, 50, 255), width=k) for q in range(16)],
        dd.ellipse((172 * k, 2 * k, 214 * k, 42 * k), fill=(204, 168, 92, 255), outline=(150, 116, 50, 255), width=2 * k),
        dd.ellipse((182 * k, 10 * k, 196 * k, 22 * k), fill=(246, 226, 170, 220))))
    bayangan(img, sekrup, (cx - 100, ty - 34), blur=4, geser=(2, 4), kuat=0.4)
    # ayat di bawah ram
    d = ImageDraw.Draw(img)
    tinta_ = campur(c_teks, (30, 26, 24), 0.55)
    f, vl, size = pas_aman(d, bersih(p["ayat"]), lambda s_: georgia(s_, True), W - 180, H - 110 - 950 - 50, 38, 22, 1.34)
    yy = 950 + max(0, (H - 110 - 950 - 50 - len(vl) * size * 1.34) / 2)
    for ln in vl:
        d.text((W / 2, yy), ln, font=f, fill=tinta_, anchor="ma")
        yy += size * 1.34
    d.text((W / 2, yy + 10), p["ref"], font=avenir(30, 0), fill=c_teks, anchor="ma")
    kredit(img, (W / 2, H - 46), campur(latar, (0, 0, 0), 0.5))
    return img


# ---------- APOTEK: resep dokter + etiket ----------

APOTEK_WARNA = [((0, 128, 118), (214, 234, 228)), ((36, 96, 176), (220, 230, 242)), ((40, 140, 84), (226, 236, 220))]


def coretan_ttd(d, x, y, col, rng, S=1):
    pts = []
    for k in range(60):
        t = k / 59
        pts.append(((x + 200 * t + 18 * math.sin(t * 19)) * S, (y - 22 * math.sin(t * 9.5) * (1 - t * 0.6) + 10 * math.cos(t * 23)) * S))
    goresan(d, pts, 3 * S, col, rng, 0.6 * S)
    goresan(d, [((x - 10) * S, (y + 22) * S), ((x + 230) * S, (y + 14) * S)], 3 * S, col, rng, 0.6 * S)


def apotek_image(p, i):
    rng = np.random.default_rng(15800 + i)
    aksen, meja = APOTEK_WARNA[i % 3]
    img = grain(gradasi(W, H, meja, campur(meja, (0, 0, 0), 0.08)), 0.03).convert("RGBA")
    pw, ph = 920, 1256
    kertas_ = kertas(pw, ph, (253, 253, 249), 15810 + i, 0.015, 40).convert("RGBA")
    biru_tinta = (26, 42, 112)
    abu = (120, 124, 128)
    S = 2
    lay = Image.new("RGBA", (pw * S, ph * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    # kop: logo salib apotek
    ld.ellipse((40 * S, 38 * S, 132 * S, 130 * S), fill=aksen + (255,))
    ld.rectangle((76 * S, 54 * S, 96 * S, 114 * S), fill=(255, 255, 255, 255))
    ld.rectangle((56 * S, 74 * S, 116 * S, 94 * S), fill=(255, 255, 255, 255))
    kertas_.alpha_composite(lay.resize((pw, ph), Image.LANCZOS))
    lay = Image.new("RGBA", (pw * S, ph * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    d = ImageDraw.Draw(kertas_)
    d.text((156, 82), "APOTEK KASIH KARUNIA", font=muat(d, "APOTEK KASIH KARUNIA", lambda s: avenir(s, 0), pw - 156 - 40, 48, 30), fill=aksen, anchor="ls")
    d.text((158, 122), "Jl. Damai Sejahtera No. 7  ·  Buka 24 jam, tanpa antre", font=avenir(22, 5), fill=abu, anchor="ls")
    d.line((40, 152, pw - 40, 152), fill=aksen, width=4)
    d.line((40, 160, pw - 40, 160), fill=aksen, width=1)
    d.text((40, 204), "Dokter:", font=avenir(24, 5), fill=abu, anchor="ls")
    d.text((132, 204), "Tabib yang Agung", font=avenir(26, 2), fill=(40, 44, 50), anchor="ls")
    d.text((pw - 40, 204), "Tgl. " + p.get("_tanggal", ""), font=avenir(24, 5), fill=abu, anchor="rs")
    d.text((40, 262), "Untuk:", font=avenir(24, 5), fill=abu, anchor="ls")
    for x in range(132, pw - 40, 10):
        d.line((x, 272, x + 4, 272), fill=(190, 194, 200), width=2)
    pasien = bersih(p["pasien"])
    d.text((140, 260), pasien, font=muat(d, pasien, spidol, pw - 200, 48, 28), fill=biru_tinta, anchor="ls")
    # R/ tiga "obat"
    d.text((36, 286), "R/", font=ft("Georgia Bold Italic.ttf", 92), fill=aksen)
    y = 304
    for k, (nama, aturan) in enumerate(p["obat"][:3]):
        nama, aturan = bersih(nama), bersih(aturan)
        no = f"No. {'I' * (k + 1)}"
        fno = spidol(30)
        fn = muat(d, nama, spidol, pw - 176 - 60 - d.textlength(no, font=fno) - 24, 46, 26)
        d.text((176, y + 44), nama, font=fn, fill=biru_tinta, anchor="ls")
        d.text((176 + d.textlength(nama, font=fn) + 24, y + 44), no, font=fno, fill=biru_tinta, anchor="ls")
        fa = muat(d, "S. " + aturan, spidol, pw - 206 - 60, 34, 22)
        d.text((206, y + 90), "S. " + aturan, font=fa, fill=biru_tinta, anchor="ls")
        ex = 206 + d.textlength("S. " + aturan, font=fa) + 14
        goresan(ld, [(ex * S, (y + 84) * S), ((ex + 14) * S, (y + 74) * S), ((ex + 22) * S, (y + 92) * S)], 2.6 * S, biru_tinta + (255,), rng, 0.4 * S)
        goresan(ld, [(196 * S, (y + 106) * S), ((pw - 110) * S, (y + 102) * S)], 2 * S, biru_tinta + (90,), rng, 0.5 * S)
        y += 118
    # catatan
    d.text((40, y + 38), "Catatan:", font=avenir(24, 5), fill=abu, anchor="ls")
    fc, cl, cs = pas_aman(d, bersih(p["catatan"]), spidol, pw - 180 - 50, 88, 38, 24, 1.18)
    yc = y + 6
    for ln in cl:
        d.text((180, yc + cs), ln, font=fc, fill=(180, 40, 50), anchor="ls")
        yc += cs * 1.18
    garis_bawah = 180 + max(d.textlength(ln, font=fc) for ln in cl)
    goresan(ld, [(176 * S, (yc + 16) * S), ((180 + (garis_bawah - 180) * 0.5) * S, (yc + 22) * S), (garis_bawah * S, (yc + 12) * S)], 3 * S, (180, 40, 50, 230), rng, 0.6 * S)
    # etiket berisi ayat
    ey0, ey1 = yc + 46, ph - 132
    d.rounded_rectangle((40, ey0, pw - 40, ey1), radius=18, outline=aksen, width=3)
    d.rounded_rectangle((40, ey0, pw - 40, ey0 + 54), radius=18, fill=aksen)
    d.rectangle((40, ey0 + 30, pw - 40, ey0 + 54), fill=aksen)
    renggang(d, (pw / 2, ey0 + 38), "ETIKET  ·  PETUNJUK PEMAKAIAN", avenir(22, 0), (255, 255, 255), 3, anchor="ms")
    ruang = ey1 - ey0 - 54 - 86
    f, vl, size = pas_aman(d, bersih(p["ayat"]), lambda s: georgia(s, True), pw - 140, ruang, 36, 22, 1.32)
    yy = ey0 + 72 + max(0, (ruang - len(vl) * size * 1.32) / 2)
    for ln in vl:
        d.text((pw / 2, yy), ln, font=f, fill=(40, 44, 50), anchor="ma")
        yy += size * 1.32
    d.text((pw / 2, yy + 8), p["ref"], font=avenir(28, 0), fill=aksen, anchor="ma")
    # tanda tangan
    coretan_ttd(ld, pw - 330, ph - 84, biru_tinta + (255,), rng, S)
    kertas_.alpha_composite(lay.resize((pw, ph), Image.LANCZOS))
    d = ImageDraw.Draw(kertas_)
    d.line((pw - 350, ph - 52, pw - 60, ph - 52), fill=(150, 154, 160), width=2)
    d.text((pw - 205, ph - 24), "Tabib yang Agung", font=avenir(22, 2), fill=(90, 94, 100), anchor="ms")
    d.text((40, ph - 24), "@" + HANDLE, font=avenir(22, 5), fill=(150, 154, 160), anchor="ls")
    kertas_ = kertas_.rotate(0.7 * (-1) ** i, expand=True, resample=Image.BICUBIC)
    bayangan(img, kertas_, ((W - kertas_.width) / 2, (H - kertas_.height) / 2), blur=18, geser=(6, 12), kuat=0.3)
    return img


# ---------- GIZI: label Informasi Nilai Gizi ----------

def gizi_image(p, i):
    rng = np.random.default_rng(15900 + i)
    putih, hitam = (250, 250, 247), (14, 14, 14)
    img = kertas(W, H, putih, 15900 + i, 0.015, 30).convert("RGBA")
    d = ImageDraw.Draw(img)
    v = i % 3
    if v == 1:  # garis-garis diagonal samar
        for x in range(-H, W, 34):
            d.line((x, H, x + H, 0), fill=(236, 236, 232), width=12)
    elif v == 2:  # titik raster samar
        for y in range(10, H, 26):
            for x in range(10 + (y // 26 % 2) * 13, W, 26):
                d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(232, 232, 228))
    nama = bersih(p["nama"]).upper()
    fn = muat(d, nama, lambda s: helv(s, 9), W - 140, 96, 40)
    pita1 = 56 + fn.size + 40
    d.rectangle((0, 56, W, pita1), fill=hitam)
    d.text((W / 2, 56 + 20 + fn.size * 0.86), nama, font=fn, fill=putih, anchor="ms")
    # label digambar di lapisan sendiri (y mulai 0), lalu ditaruh di tengah ruang yang tersisa
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, x1 = 150, W - 150
    xi0, xi1 = x0 + 22, x1 - 22
    y = 22
    fj = muat(d, "Informasi Nilai Gizi", lambda s: helv(s, 9), xi1 - xi0, 84, 40)
    d.text((xi0, y + fj.size * 0.86), "Informasi Nilai Gizi", font=fj, fill=hitam, anchor="ls")
    y += fj.size + 10
    d.line((xi0, y, xi1, y), fill=hitam, width=2)
    y += 8
    porsi = bersih(p["porsi"])
    d.text((xi0, y + 34), "Takaran saji", font=helv(30, 0), fill=hitam, anchor="ls")
    fp = muat(d, porsi, lambda s: helv(s, 1), xi1 - xi0 - d.textlength("Takaran saji", font=helv(30, 0)) - 30, 30, 18)
    d.text((xi1, y + 34), porsi, font=fp, fill=hitam, anchor="rs")
    y += 50
    d.rectangle((xi0, y, xi1, y + 18), fill=hitam)
    y += 18 + 8
    d.text((xi0, y + 26), "JUMLAH PER SAJIAN", font=helv(22, 1), fill=hitam, anchor="ls")
    d.text((xi1, y + 26), "SETIAP HARI", font=helv(22, 1), fill=hitam, anchor="rs")
    y += 36
    d.rectangle((xi0, y, xi1, y + 8), fill=hitam)
    y += 8
    for k, (nm, nilai) in enumerate(p["baris"][:5]):
        nm, nilai = bersih(nm), bersih(str(nilai))
        besar = k == 0
        rh = 78 if besar else 64
        fnm = helv(42 if besar else 32, 1 if besar else 0)
        fnl = helv(42 if besar else 32, 1)
        maxnm = xi1 - xi0 - (0 if besar else 20) - d.textlength(nilai, font=fnl) - 24
        if d.textlength(nm, font=fnm) > maxnm:
            fnm = muat(d, nm, lambda s: helv(s, 1 if besar else 0), maxnm, fnm.size, 18)
        d.text((xi0 + (0 if besar else 20), y + rh * 0.68), nm, font=fnm, fill=hitam, anchor="ls")
        d.text((xi1, y + rh * 0.68), nilai, font=fnl, fill=hitam, anchor="rs")
        y += rh
        if besar:
            d.rectangle((xi0, y, xi1, y + 8), fill=hitam)
            y += 8
        elif k < 4:
            d.line((xi0, y, xi1, y), fill=hitam, width=2)
    d.rectangle((xi0, y, xi1, y + 18), fill=hitam)
    y += 30
    fc, cl, cs = pas_aman(d, "*" + bersih(p["catatan"]), lambda s: helv(s, 0), xi1 - xi0, 80, 26, 18, 1.25)
    for ln in cl:
        d.text((xi0, y), ln, font=fc, fill=hitam)
        y += cs * 1.25
    y += 16
    label_h = y
    d.rectangle((x0, 0, x1, label_h), outline=hitam, width=7)
    # komposisi = ayat
    atas, bawah = pita1 + 36, H - 136
    ky0 = label_h + 34
    ruang = bawah - atas - ky0 - 46
    fa, vl, size = pas_aman(d, "KOMPOSISI: " + tanpa_kutip(p["ayat"]), lambda s: helv(s, 0), x1 - x0, ruang, 34, 20, 1.3)
    yy = ky0
    for k, ln in enumerate(vl):
        if k == 0 and ln.startswith("KOMPOSISI:"):
            d.text((x0, yy), "KOMPOSISI:", font=helv(size, 1), fill=hitam)
            d.text((x0 + d.textlength("KOMPOSISI: ", font=helv(size, 1)), yy), ln[len("KOMPOSISI: "):], font=fa, fill=hitam)
        else:
            d.text((x0, yy), ln, font=fa, fill=hitam)
        yy += size * 1.3
    d.text((x0, yy + 6), "(" + p["ref"] + ")", font=helv(28, 1), fill=hitam)
    total = yy + 6 + 34
    off = int(atas + max(0, (bawah - atas - total) / 2))
    ImageDraw.Draw(img).rectangle((x0, off, x1, off + label_h), fill=putih)
    img.alpha_composite(lay.crop((0, 0, W, H - off)), (0, off))
    # kaki: barcode + kredit
    d = ImageDraw.Draw(img)
    d.rectangle((W - 330, H - 116, W - 70, H - 40), fill=putih)
    gaya_w7.barcode(d, W - 320, H - 112, 240, 46, rng, hitam)
    d.text((W - 200, H - 44), f"8 99{i + 1}027 {15:03d}0{i + 3}", font=helv(18), fill=hitam, anchor="ms")
    d.text((70, H - 54), "@" + HANDLE, font=helv(22, 1), fill=hitam, anchor="ls")
    return img


# ---------- KERETA (Reels): peta jalur kereta ----------

KERETA_WARNA = [(0, 150, 114), (226, 74, 52), (40, 98, 204)]
KERETA_RUTE = [  # titik stasiun + sisi label
    ([(200, 690), (200, 880), (390, 1070), (390, 1260), (580, 1450)], ["r", "r", "r", "r", "r"]),
    ([(880, 690), (880, 880), (690, 1070), (690, 1260), (500, 1450)], ["l", "l", "l", "l", "l"]),
    ([(210, 690), (210, 880), (400, 1070), (590, 1260), (590, 1450)], ["r", "r", "r", "r", "r"]),
]


def jalur_oktilinear(pts):
    """Sambungkan stasiun dengan ruas lurus + diagonal 45 derajat (peta transit)."""
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        dg = min(abs(dx), abs(dy))
        if abs(dx) > abs(dy):
            out.append((x0 + math.copysign(abs(dx) - dg, dx), y0))
        elif abs(dy) > abs(dx):
            out.append((x0, y0 + math.copysign(abs(dy) - dg, dy)))
        out.append((x1, y1))
    return out


def titik_di(path, cum, s):
    s = min(max(s, 0), cum[-1])
    k = int(np.searchsorted(cum, s, side="right")) - 1
    k = min(k, len(path) - 2)
    seg = cum[k + 1] - cum[k]
    u = 0 if seg == 0 else (s - cum[k]) / seg
    (x0, y0), (x1, y1) = path[k], path[k + 1]
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u


def peta_latar(w, h, seed):
    rng = np.random.default_rng(seed)
    img = kertas(w, h, (246, 244, 238), seed, 0.012, 20).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(5):  # taman
        x, y, r = rng.uniform(0, w), rng.uniform(300, h - 200), rng.uniform(60, 150)
        d.rounded_rectangle((x - r, y - r * 0.7, x + r, y + r * 0.7), radius=40, fill=(224, 236, 214))
    sungai = [(x, 340 + 120 * math.sin(x / 300 + seed) + x * 0.35) for x in range(-40, w + 60, 20)]
    d.line(sungai, fill=(208, 226, 240), width=46, joint="curve")
    for _ in range(14):  # jalan
        if rng.random() < 0.5:
            y = rng.uniform(0, h)
            d.line((0, y, w, y + rng.uniform(-60, 60)), fill=(236, 233, 226), width=int(rng.uniform(5, 12)))
        else:
            x = rng.uniform(0, w)
            d.line((x, 0, x + rng.uniform(-60, 60), h), fill=(236, 233, 226), width=int(rng.uniform(5, 12)))
    return img


def kereta_sprite(col):
    def gambar(d, k):
        d.rounded_rectangle((4 * k, 6 * k, 126 * k, 54 * k), radius=24 * k, fill=(255, 255, 255, 255), outline=(40, 40, 46, 255), width=4 * k)
        d.rounded_rectangle((10 * k, 38 * k, 120 * k, 48 * k), radius=5 * k, fill=col + (255,))
        for x in (24, 48, 72):
            d.rounded_rectangle((x * k, 15 * k, (x + 18) * k, 31 * k), radius=4 * k, fill=(46, 56, 76, 255))
        d.rounded_rectangle((100 * k, 14 * k, 120 * k, 32 * k), radius=8 * k, fill=(46, 56, 76, 255))
    return sprite(130, 60, gambar)


def kereta_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/kereta{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    col = KERETA_WARNA[idx % 3]
    titik, sisi = KERETA_RUTE[idx % 3]
    stasiun = [bersih(s) for s in p["stasiun"]][:5]
    jalur = bersih(p["jalur"])
    kode = (re.findall(r"[A-Za-z]", jalur.split()[-1]) or ["T"])[0].upper()
    bg = peta_latar(RW, RH, 15950 + idx)
    path = jalur_oktilinear(titik)
    cum = np.concatenate([[0], np.cumsum([math.dist(a, b) for a, b in zip(path, path[1:])])])
    pos_st = [float(cum[path.index(t)]) for t in titik]
    S = 2
    # judul
    judul = Image.new("RGBA", (RW, 220), (0, 0, 0, 0))
    jd = ImageDraw.Draw(judul)
    renggang(jd, (90, 40), "PETA JALUR  ·  " + p.get("_tanggal", "").upper(), sf(24, "Semibold"), (120, 120, 128), 2, anchor="ls")
    fj = muat(jd, jalur, lambda s: sf(s, "Bold"), RW - 90 - 200, 64, 34)
    jd.rounded_rectangle((90, 70, 180, 160), radius=24, fill=col)
    jd.text((135, 116), kode, font=sf(52, "Heavy"), fill=(255, 255, 255), anchor="mm")
    jd.text((206, 140), jalur, font=fj, fill=(28, 28, 34), anchor="ls")
    jd.text((206, 184), f"{len(stasiun)} stasiun  ·  @{HANDLE}", font=sf(26, "Medium"), fill=(120, 120, 128), anchor="ls")

    def garis_layer(panjang):
        lay = Image.new("RGBA", (RW * S, RH * S), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        if panjang > 0:
            pts = [path[0]]
            for k in range(1, len(path)):
                if cum[k] <= panjang:
                    pts.append(path[k])
                else:
                    pts.append(titik_di(path, cum, panjang))
                    break
            if len(pts) >= 2:
                ld.line([(x * S, y * S) for x, y in pts], fill=col + (255,), width=36 * S, joint="curve")
                for x, y in (pts[0], pts[-1]):
                    ld.ellipse(((x - 18) * S, (y - 18) * S, (x + 18) * S, (y + 18) * S), fill=col + (255,))
        return lay.resize((RW, RH), Image.LANCZOS)

    garis_penuh = garis_layer(cum[-1] + 1)

    def halte(aktif, skala=1.0):
        r = (28 if not aktif else 32) * skala
        def gambar(d, k):
            c = 40
            d.ellipse(((c - r) * k, (c - r) * k, (c + r) * k, (c + r) * k), fill=(255, 255, 255, 255), outline=(32, 32, 38, 255), width=int(8 * k * skala))
            if aktif:
                d.ellipse(((c - r * 0.45) * k, (c - r * 0.45) * k, (c + r * 0.45) * k, (c + r * 0.45) * k), fill=col + (255,))
        return sprite(80, 80, gambar)

    halte_kosong, halte_aktif = halte(False), halte(True)
    label = []
    for k, (nama, sd) in enumerate(zip(stasiun, sisi)):
        lab = Image.new("RGBA", (560, 120), (0, 0, 0, 0))
        ldr = ImageDraw.Draw(lab)
        ruang = (RW - 70 - (titik[k][0] + 62)) if sd == "r" else (titik[k][0] - 62 - 70)
        fl = muat(ldr, nama, lambda s: sf(s, "Bold"), min(520, ruang), 48, 24)
        kd = f"{kode}{k + 1:02d}"
        fk = sf(22, "Bold")
        kw = ldr.textlength(kd, font=fk) + 22
        if sd == "r":
            ldr.rounded_rectangle((0, 22, kw, 56), radius=8, fill=col)
            ldr.text((kw / 2, 39), kd, font=fk, fill=(255, 255, 255), anchor="mm")
            ldr.text((0, 100), nama, font=fl, fill=(26, 26, 32), anchor="ls")
        else:
            ldr.rounded_rectangle((560 - kw, 22, 560, 56), radius=8, fill=col)
            ldr.text((560 - kw / 2, 39), kd, font=fk, fill=(255, 255, 255), anchor="mm")
            ldr.text((560, 100), nama, font=fl, fill=(26, 26, 32), anchor="rs")
        label.append(lab)

    def pos_label(k):
        x, y = titik[k]
        return (x + 62, y - 76) if sisi[k] == "r" else (x - 62 - 560, y - 76)

    sprite_kereta = kereta_sprite(col)
    # kartu ayat
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    fa, vl, vs = pas_aman(probe, bersih(p["ayat"]), lambda s: georgia(s, True), RW - 260, 560, 48, 28, 1.36)
    ch = int(140 + len(vl) * vs * 1.36 + 120)
    kartu = Image.new("RGBA", (RW - 140, ch), (0, 0, 0, 0))
    kd_ = ImageDraw.Draw(kartu)
    kd_.rounded_rectangle((0, 0, kartu.width - 1, ch - 1), radius=36, fill=(255, 255, 255, 255))
    kd_.rounded_rectangle((0, 0, kartu.width - 1, 104), radius=36, fill=col)
    kd_.rectangle((0, 60, kartu.width - 1, 104), fill=col)
    tujuan = "TIBA DI " + stasiun[-1].upper()
    renggang(kd_, (kartu.width / 2, 66), tujuan, muat(kd_, tujuan, lambda s: sf(s, "Bold"), kartu.width - 120, 30, 18), (255, 255, 255), 2, anchor="ms")
    yy = 140
    for ln in vl:
        kd_.text((kartu.width / 2, yy), ln, font=fa, fill=(36, 36, 42), anchor="ma")
        yy += vs * 1.36
    kd_.text((kartu.width / 2, yy + 18), p["ref"], font=sf(34, "Bold"), fill=col, anchor="ma")
    kd_.text((kartu.width / 2, yy + 70), "@" + HANDLE, font=sf(24, "Medium"), fill=(140, 140, 150), anchor="ma")
    kartu_y = int(max(400, 960 - ch / 2))
    # jadwal
    T_GARIS0, T_GARIS1 = 0.3, 2.0
    tiba = [2.0]
    for k in range(1, 5):
        tiba.append(tiba[-1] + 0.3 + 1.45)
    T_KARTU = tiba[-1] + 0.6

    def pos_kereta(t):
        if t <= tiba[0]:
            return pos_st[0]
        for k in range(4):
            berangkat = tiba[k] + 0.3
            if t < berangkat:
                return pos_st[k]
            if t < tiba[k + 1]:
                u = ease((t - berangkat) / (tiba[k + 1] - berangkat))
                return pos_st[k] + (pos_st[k + 1] - pos_st[k]) * u
        return pos_st[-1]

    def gambar(t, sampul=False):
        frame = bg.copy()
        frame.alpha_composite(judul if sampul else fade(judul, ease(t / 0.5)), (0, 380))
        if sampul or t >= T_GARIS1:
            frame.alpha_composite(garis_penuh)
            panjang = cum[-1]
        else:
            panjang = cum[-1] * ease(max(0.0, (t - T_GARIS0) / (T_GARIS1 - T_GARIS0)))
            frame.alpha_composite(garis_layer(panjang))
        s_ker = cum[-1] if sampul else pos_kereta(t)
        for k, (x, y) in enumerate(titik):
            if pos_st[k] > panjang + 1:
                continue
            sudah = sampul or t >= tiba[k] - 0.05
            h_ = halte_aktif if sudah else halte_kosong
            frame.alpha_composite(h_, (int(x - 40), int(y - 40)))
            if sampul or t >= tiba[k]:
                u = 1.0 if sampul else ease((t - tiba[k]) / 0.35)
                lx, ly = pos_label(k)
                frame.alpha_composite(fade(label[k], u), (int(lx), int(ly + 14 * (1 - u))))
                if not sampul and t - tiba[k] < 0.7:
                    rr = 30 + 60 * (t - tiba[k]) / 0.7
                    ring = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
                    ImageDraw.Draw(ring).ellipse((100 - rr, 100 - rr, 100 + rr, 100 + rr), outline=col + (int(200 * (1 - (t - tiba[k]) / 0.7)),), width=5)
                    frame.alpha_composite(ring, (int(x - 100), int(y - 100)))
        if sampul or t >= T_GARIS1 - 0.3:
            x, y = titik_di(path, cum, s_ker)
            xa, ya = titik_di(path, cum, s_ker - 26)
            xb, yb = titik_di(path, cum, s_ker + 26)
            ang = math.degrees(math.atan2(yb - ya, xb - xa)) if (xb, yb) != (xa, ya) else 90
            kr = sprite_kereta.rotate(-ang, expand=True, resample=Image.BICUBIC)
            a = 1.0 if sampul else ease((t - (T_GARIS1 - 0.3)) / 0.3)
            bayangan(frame, fade(kr, a), (x - kr.width / 2, y - kr.height / 2), blur=6, geser=(3, 6), kuat=0.35)
        if not sampul and t >= T_KARTU:
            u = ease((t - T_KARTU) / 0.7)
            putih = Image.new("RGBA", (RW, RH), (246, 244, 238, int(225 * u)))
            frame.alpha_composite(putih)
            bayangan(frame, fade(kartu, u), (70, kartu_y + 40 * (1 - u)), blur=24, geser=(0, 14), kuat=0.25 * u)
        return frame

    sampul = gambar(0, sampul=True)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(int(seconds * FPS)):
        t = n / FPS
        frame = sampul if t < 0.4 else gambar(t - 0.4)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- TULIS (Reels): pena menulis ayat ----------

def pena_sprite():
    """Pena celup/fountain pen miring; -> (sprite RGBA, posisi ujung pena di sprite)."""
    L, T = 560, 46
    def gambar(d, k):
        cy = 30
        d.polygon([(8 * k, cy * k), (84 * k, (cy - 15) * k), (84 * k, (cy + 15) * k)], fill=(214, 172, 84, 255))
        d.line((14 * k, cy * k, 70 * k, cy * k), fill=(120, 86, 30, 255), width=2 * k)
        d.ellipse((58 * k, (cy - 4) * k, 66 * k, (cy + 4) * k), fill=(120, 86, 30, 255))
        d.rounded_rectangle((80 * k, (cy - 18) * k, 176 * k, (cy + 18) * k), radius=8 * k, fill=(30, 30, 36, 255))
        d.rectangle((172 * k, (cy - 22) * k, 186 * k, (cy + 22) * k), fill=(214, 176, 92, 255))
        d.rounded_rectangle((184 * k, (cy - 23) * k, (L - 10) * k, (cy + 23) * k), radius=20 * k, fill=(26, 44, 92, 255))
        d.rounded_rectangle((200 * k, (cy - 16) * k, (L - 30) * k, (cy - 9) * k), radius=4 * k, fill=(90, 120, 186, 150))
        d.rounded_rectangle((300 * k, (cy - 26) * k, 470 * k, (cy - 20) * k), radius=3 * k, fill=(220, 186, 104, 255))
        d.rectangle((452 * k, (cy - 24) * k, 466 * k, (cy + 24) * k), fill=(214, 176, 92, 255))
    pen = sprite(L, 60, gambar)
    sudut = 36
    rot = pen.rotate(sudut, expand=True, resample=Image.BICUBIC)
    # posisi ujung (8, 30) setelah rotasi terhadap pusat
    cx, cy = L / 2, 30
    a = math.radians(sudut)
    dx, dy = 8 - cx, 30 - cy
    rx, ry = dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)
    return rot, (rot.width / 2 + rx, rot.height / 2 + ry)


def tulis_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/tulis{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(15960 + idx)
    tinta_ = [(26, 40, 98), (34, 30, 40), (88, 36, 52)][idx % 3]
    # kertas krem bergaris samar
    bg = kertas(RW, RH, (247, 240, 223), 15960 + idx, 0.035, 160).convert("RGBA")
    a = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:RH, 0:RW].astype(np.float32)
    vig = 1 - 0.16 * np.clip(np.sqrt(((xx - RW / 2) / (RW / 2)) ** 2 + ((yy - RH / 2) / (RH / 2)) ** 2) - 0.6, 0, 1)
    a[..., :3] *= vig[..., None]
    bg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    teks = bersih(p["ayat"])
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f, lines, size = pas_aman(probe, teks, spidol, RW - 220, 760, 76, 44, 1.45)
    lh = size * 1.45
    y0 = 1000 - (len(lines) * lh) / 2
    d = ImageDraw.Draw(bg)
    for k in range(-1, len(lines) + 2):
        yb = y0 + k * lh + size * 0.98
        d.line((90, yb + 8, RW - 90, yb + 8), fill=(196, 206, 222), width=2)
    renggang(d, (RW - 110, y0 - lh * 1.2 - 10), p.get("_tanggal", ""), tangan(34), (150, 140, 126), 1, anchor="rs")
    # posisi tiap huruf
    lebar_baris = [probe.textlength(ln, font=f) for ln in lines]
    x0s = [(RW - lw) / 2 for lw in lebar_baris]
    huruf = []  # (baris, x_awal, x_akhir)
    for b, ln in enumerate(lines):
        for c in range(len(ln)):
            xa = x0s[b] + probe.textlength(ln[:c], font=f)
            xb = x0s[b] + probe.textlength(ln[:c + 1], font=f)
            huruf.append((b, xa, xb, ln[c]))
    teks_l = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    td = ImageDraw.Draw(teks_l)
    for b, ln in enumerate(lines):
        td.text((x0s[b], y0 + b * lh), ln, font=f, fill=tinta_ + (255,))
    # bobot waktu per huruf: spasi & tanda baca lebih cepat/berhenti sebentar
    bobot = np.array([0.35 if ch == " " else (1.8 if ch in ",.;:!?…" else 1.0) for _, _, _, ch in huruf])
    T0, T1 = 0.9, seconds - 3.6
    batas = T0 + np.concatenate([[0], np.cumsum(bobot)]) / bobot.sum() * (T1 - T0)
    pena, ujung = pena_sprite()
    pena_bay = Image.new("RGBA", pena.size, (0, 0, 0, 0))
    pena_bay.putalpha(pena.getchannel("A").point(lambda v: int(v * 0.28)))
    pena_bay = pena_bay.filter(ImageFilter.GaussianBlur(10))
    # referensi
    ref_l = Image.new("RGBA", (RW, 240), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ref_l)
    ref = "— " + p["ref"]
    fr = muat(rd, ref, lambda s: iowan(s, 3), RW - 240, 52, 30)
    rd.text((RW / 2, 70), ref, font=fr, fill=tinta_ + (255,), anchor="ms")
    rw_ = rd.textlength(ref, font=fr)
    kredit_l = Image.new("RGBA", (RW, 80), (0, 0, 0, 0))
    ImageDraw.Draw(kredit_l).text((RW / 2, 40), "@" + HANDLE, font=avenir(28, 5), fill=(140, 128, 112, 255), anchor="mm")
    ref_y = int(y0 + len(lines) * lh + 30)

    def garis_ref(u):
        if u <= 0:
            return Image.new("RGBA", (RW, 240), (0, 0, 0, 0))
        lay = Image.new("RGBA", (RW * 2, 240 * 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        xs = np.linspace(RW / 2 - rw_ / 2 - 10, RW / 2 + rw_ / 2 + 30, 40)
        n = max(2, int(len(xs) * u))
        pts = [(x * 2, (96 + 6 * math.sin((x - xs[0]) / 60)) * 2) for x in xs[:n]]
        ld.line(pts, fill=tinta_ + (230,), width=6, joint="curve")
        return lay.resize((RW, 240), Image.LANCZOS)

    def reveal(t, sampul=False):
        if sampul or t >= batas[-1]:
            return teks_l
        k = int(np.searchsorted(batas, t, side="right")) - 1
        if k < 0:
            return None
        u = (t - batas[k]) / max(1e-6, batas[k + 1] - batas[k])
        b, xa, xb, _ = huruf[k]
        m = Image.new("L", (RW, RH), 0)
        md = ImageDraw.Draw(m)
        for bb in range(b):
            md.rectangle((0, y0 + bb * lh - 20, RW, y0 + (bb + 1) * lh - 10), fill=255)
        md.rectangle((0, y0 + b * lh - 20, xa + (xb - xa) * u, y0 + (b + 1) * lh - 10), fill=255)
        lay = teks_l.copy()
        lay.putalpha(ImageChops.multiply(teks_l.getchannel("A"), m))
        return lay, (xa + (xb - xa) * u, y0 + b * lh + size * 0.82)

    def gambar(t, sampul=False):
        frame = bg.copy()
        r = reveal(t, sampul)
        tip = None
        if isinstance(r, tuple):
            frame.alpha_composite(r[0])
            tip = r[1]
        elif r is not None:
            frame.alpha_composite(r)
        # pena
        if not sampul:
            if t < T0:
                b, xa, _, _ = huruf[0]
                tgt = (xa, y0 + size * 0.82)
                u = ease(t / T0)
                px, py = RW + 200 + (tgt[0] - RW - 200) * u, RH * 0.75 + (tgt[1] - RH * 0.75) * u
            elif tip is not None:
                goyang = math.sin(t * 22) * size * 0.12
                px, py = tip[0], tip[1] - size * 0.25 + goyang
            else:
                b, _, xb, _ = huruf[-1]
                ex, ey = xb, y0 + b * lh + size * 0.6
                u = ease((t - batas[-1]) / 0.9)
                px, py = ex + (RW + 300 - ex) * u, ey + (RH * 0.8 - ey) * u
            if px < RW + 260:
                frame.alpha_composite(pena_bay, (int(px - ujung[0] + 26), int(py - ujung[1] + 30)))
                comp(frame, pena, (px - ujung[0], py - ujung[1]))
        if sampul or t >= batas[-1] + 0.4:
            u = 1.0 if sampul else ease((t - batas[-1] - 0.4) / 0.8)
            frame.alpha_composite(fade(ref_l, u), (0, int(ref_y + 16 * (1 - u))))
            frame.alpha_composite(garis_ref(1.0 if sampul else ease((t - batas[-1] - 0.9) / 0.7)), (0, int(ref_y + 16 * (1 - u))))
            frame.alpha_composite(fade(kredit_l, u), (0, int(min(ref_y + 130, 1500))))
        return frame

    sampul = gambar(0, sampul=True)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(int(seconds * FPS)):
        t = n / FPS
        frame = sampul if t < 0.4 else gambar(t - 0.4)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ================= MIX =================

def photobooth_jurnal(p, i):
    latar = jurnal_latar(W, H, 16100 + i, tempat=[(W - 60, 56, 34), (W - 14, H * 0.5, -86), (40, H - 60, 32)])
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    n = len(wrap(probe, bersih(p["judul"]), tangan(64), 410))
    return teks_gelap(lambda bg: gaya_w11.photobooth_image(p, i, latar=bg), latar, [(592, 100, W, 140 + n * 76 + 20)], ink=(40, 48, 92))


def balon_pagi(p, i):
    latar = pagi_latar(W, H, 16200 + i)
    return teks_gelap(lambda bg: gaya_w12.balon_image(p, i, latar=bg), latar, [(0, 596, W, H)], ink=(50, 44, 80), aksen=(190, 86, 50))


def flip_pagi(p, i):
    latar = pagi_latar(W, H, 16300 + i)
    return teks_gelap(lambda bg: gaya_w11.flipclock_image(p, i, latar=bg), latar, [(0, 0, W, 150), (0, 616, W, H)], ink=(50, 44, 80), aksen=(190, 86, 50))


def majalah_biru(p, i):
    """Sampul majalah dengan tulisan edisi Januari (bukan 'EDISI ADVEN · DESEMBER 2026'), lalu duotone biru."""
    foto = foto_redup(p["foto"], W, H, 16400 + i, gelap=0.18, blur=0)
    img = gaya_w10.majalah_image(p, i, latar=foto).convert("RGB")
    a = np.asarray(foto).astype(np.float32)[30:68]
    yy = np.linspace(0, 1, H)[30:68, None, None]
    a *= 1 - 0.55 * np.clip((0.3 - yy) / 0.3, 0, 1)
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), (0, 30))
    d = ImageDraw.Draw(img)
    bulan = " ".join(p.get("_tanggal", "3 Januari 2027").split()[1:]).upper()
    d.text((W / 2, 40), f"{bersih(p.get('edisi', 'EDISI AWAL TAHUN')).upper()}  ·  {bulan}  ·  @{HANDLE.upper()}", font=hn(22, 1), fill=(255, 255, 255), anchor="ma")
    d.rectangle((W - 226, H - 82, W - 64, H - 60), fill=(255, 255, 255))
    d.text((W - 145, H - 72), p.get("_tgl_struk", "03/01/2027").replace("/", "-"), font=hn(16, 10), fill=(20, 20, 20), anchor="mm")
    return biru(img, 16450 + i)


SIMPLE = {
    # baru
    "JURNAL": jurnal_image, "LABEL": label_image, "CETAKBIRU": cetakbiru_image, "PERPUS": perpus_image,
    "CENTANG": centang_image, "SWISS": swiss_image, "LAPIS": lapis_image, "SULAM": sulam_image,
    "APOTEK": apotek_image, "GIZI": gizi_image,
    # lama
    "CUACA": gaya_w7.cuaca_image, "STRUK": gaya_w7.struk_image, "KORAN": gaya_w8.koran_image, "MENU": gaya_w8.menu_image,
    "NAMA": gaya_w9.nama_image, "MUSEUM": gaya_w9.museum_image, "KASET": gaya_w9.kaset_image, "RASI": gaya_w10.rasi_image,
    "LETTER": gaya_w8.letter_image,
    # mix
    "STICKYJURNAL": lambda p, i: gaya_w8.sticky_image(p, i, latar=jurnal_latar(W, H, 16000 + i)),
    "PHOTOBOOTHJURNAL": photobooth_jurnal,
    "POLAROIDPAGI": lambda p, i: gaya_w7.polaroid_image(p, i, latar=pagi_latar(W, H, 16500 + i)),
    "TIKETPAGI": lambda p, i: gaya_w7.tiket_image(p, i, latar=pagi_latar(W, H, 16600 + i)),
    "BALONPAGI": balon_pagi,
    "FLIPPAGI": flip_pagi,
    "ALKITABSINAR": lambda p, i: sinar(gaya_w6.alkitab_image(p, i), 16700 + i),
    "KETIKSINAR": lambda p, i: sinar(gaya_w7.ketik_image(p, i), 16710 + i),
    "CATATANSINAR": lambda p, i: sinar(gaya_w7.catatan_image(p, i), 16720 + i),
    "KAMUSBIRU": lambda p, i: biru(gaya_w7.kamus_image(p, i), 16730 + i),
    "TELEGRAMBIRU": lambda p, i: biru(gaya_w10.telegram_image(p, i), 16740 + i),
    "MAJALAHBIRU": majalah_biru,
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {}
REELS = {"KERETA": (kereta_reel, "kereta"), "TULIS": (tulis_reel, "tulis"),
         "CHAT": (gaya_w7.chat_reel, "chat"), "SEARCH": (gaya_w8.search_reel, "search"), "GOSOK": (gaya_w9.gosok_reel, "gosok")}


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
