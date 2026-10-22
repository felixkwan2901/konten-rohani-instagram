"""Akun Tenang - minggu 18 (konten/tenang_w18.py), 24 - 30 Jan 2027: kasih & kesatuan (Pekan Doa Sedunia untuk Kesatuan
Umat Kristen, 18-25 Jan), lalu bertekun ketika semangat Januari mulai pudar. 37 gaya diacak tiap hari + komik Eli.
BARU (terinspirasi benda & desain sehari-hari, isinya buatan sendiri):
       KALKULATOR (kalkulator meja berpita kertas, 70 x 7 = 490), UNSUR (petak tabel periodik "Ks · Kasih" + infografik),
       PALET (kartu contoh warna cat: satu kasih, banyak nuansa), MUARA (8 sungai dari seluruh Indonesia menyatu jadi satu),
       TALI (tali tiga untai yang makin erat terpilin), PERCA (selimut perca + label jahitan berisi ayat),
       TANGGA (papan tangga & perosotan: "Jatuh? Lempar lagi."), FASE (cincin fase bulan Januari 2027, dihitung, bukan tebakan),
       KIDUNG (halaman buku nyanyian not angka 4 suara, melodi asli), STENSIL (cat semprot stensil di peti kayu),
       BENANG (Reel benang merah dililitkan di paku membentuk hati), SPIRO (Reel spirograf: satu putaran lagi).
LAMA : SCROLL, PIXEL, CHART, HPJADUL, TAG, KACAPATRI, POSTERTEBAL, BERITA, RAMBU, PANGGUNG (Reel), NEON (Reel), KONFETI (Reel).
MIX  : STICKYTENUN, STAMPTENUN, TELEGRAMTENUN, PHOTOBOOTHTENUN (kain tenun ikat: benang berwarna saling menyilang),
       POLAROIDSENJA, TIKETSENJA, BALONSENJA, RESEPSENJA, MAJALAHSENJA (langit senja merah muda-jingga-ungu, matahari rendah),
       KAMUSHANGAT, KETIKHANGAT, CATATANHANGAT (efek film hangat: sepia lembut, grain, vinyet - kenangan sebulan).
KOMIK = komik Eli & Yesus.

Fase bulan Januari 2027 untuk FASE dihitung di modul ini (lunasi dari bulan baru acuan 6 Jan 2000 18.14 UTC, bulan sinodis
29,530588853 hari, lalu koreksi Meeus bab 49 + suku planet; ΔT 69 detik). Hasil (WIB = UTC + 7):
  bulan baru   : Kamis 7 Jan 2027 20.24 UTC = Jumat 8 Jan 2027 03.24 WIB
  kuartal awal : 15 Jan 20.34 UTC = Sabtu 16 Jan 03.34 WIB
  purnama      : Jumat 22 Jan 2027 12.17 UTC = Jumat 22 Jan 2027 19.17 WIB
  kuartal akhir: 29 Jan 10.55 UTC = Jumat 29 Jan 17.55 WIB
Di cincin, tiap hari digambar seperti terlihat pukul 21.00 WIB (sisi terang di kanan saat bulan membesar, konvensi kalender).

  python3 gaya_w18.py [reels]
"""
import colorsys
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
import gaya_w7
import gaya_w8
import gaya_w9
import gaya_w10
import gaya_w11
import gaya_w12
import gaya_w13
import render
from gaya_w6 import hn
from gaya_w7 import bayangan, bersih, comp, ease, fade
from gaya_w11 import konteks
from gaya_w14 import tinta
from render import OUT, W, H, grain, save, wrap

HANDLE = config.AKUN["tenang"]["handle"]
MOD = "tenang_w18"
RW, RH, FPS = 1080, 1920, 30
MULAI = dt.date(2027, 1, 24)
SUP = "/System/Library/Fonts/Supplemental/"

# Skema konten gaya BARU (batas = jumlah karakter maksimum). Semua item juga punya ayat, ref, caption.
SKEMA = {
    "KALKULATOR": "hitung ≤10 (mis. '70×7'), hasil ≤8 (digit 7-segmen: 0-9, '-', '.', 'E'), tape[3] ≤26, ayat ≤170",
    "UNSUR": "nomor ≤3, simbol ≤2, nama ≤10, kategori ≤22, sifat[3] ≤36, tetangga[2] = [simbol ≤2, nama ≤12], ayat ≤150",
    "PALET": "nama_kartu ≤24, chip[6] = [nama ≤22, kode ≤10], warna_dasar (R, G, B) = warna chip tergelap, ayat ≤140",
    "MUARA": "sumber[6-8] ≤10 (urut dari barat ke timur), muara ≤10, ayat ≤160",
    "TALI": "untai[3] ≤10 (kiri, tengah, kanan), judul ≤24, ayat ≤170",
    "PERCA": "judul ≤22, ayat ≤150",
    "TANGGA": "judul ≤22, tangga[3] = [dari, ke, label ≤12] (dari < ke), turun[3] = [dari, ke, label ≤12] (dari > ke), "
              "bidak 1-100, dadu 1-6, ayat ≤120",
    "FASE": "judul ≤22, label_fase[2] ≤18 (untuk bulan baru, purnama), cincin ≤40, ayat ≤110 (fase dihitung dari tanggal post)",
    "KIDUNG": "nomor ≤5, judul ≤26, nada_dasar ≤8 (mis. 'G'), birama ≤4 (mis. '4/4'), suku_kata[] ≤40 suku (akhiri dengan '-' "
              "kalau katanya berlanjut, mis. 'se-'), not[4][] untuk S A T B, satu token per ketukan: '1'-'7' not, '0' diam, "
              "'.' tahan, akhiran \"'\" = titik atas, ',' = titik bawah, '5_6' = dua not 1/8 bergaris bawah, '|' garis birama (opsional)",
    "STENSIL": "kata_besar[2] ≤8, kecil[2] ≤26, cap ≤16, ayat ≤180",
    "BENANG": "judul ≤30, ayat ≤140 (Reels)",
    "SPIRO": "judul ≤24, label_putaran ≤12, ayat ≤230 (Reels)",
}


# ================= HURUF & ALAT BANTU =================

@lru_cache(maxsize=None)
def _ft(path, size, idx=0, var=None):
    f = ImageFont.truetype(path if path.startswith("/") else SUP + path, max(6, int(round(size))), index=idx)
    if var:
        f.set_variation_by_name(var)
    return f


def iowan(size, idx=0):  # 0 Roman, 1 Bold, 2 Italic, 3 Bold Italic, 4 Black
    return _ft("Iowan Old Style.ttc", size, idx)


def gill(size, idx=0):  # 0 Regular, 1 Bold, 4 SemiBold, 6 UltraBold, 7 Light
    return _ft("GillSans.ttc", size, idx)


def snell(size, idx=1):  # 0 Regular, 1 Bold, 2 Black
    return _ft("SnellRoundhand.ttc", size, idx)


def caslon(size):
    return _ft("BigCaslon.ttf", size)


def din(size):
    return _ft("DIN Condensed Bold.ttf", size)


def futura(size, idx=2):  # 0 Medium, 2 Bold, 4 Condensed ExtraBold
    return _ft("Futura.ttc", size, idx)


def menlo(size, idx=0):  # 0 Regular, 1 Bold
    return _ft("/System/Library/Fonts/Menlo.ttc", size, idx)


def kurir(size, tebal=False):
    return _ft("Courier New Bold.ttf" if tebal else "Courier New.ttf", size)


def impact(size):
    return _ft("Impact.ttf", size)


def helv(size, idx=0):  # 0 Regular, 1 Bold, 10 Medium
    return _ft("/System/Library/Fonts/HelveticaNeue.ttc", size, idx)


def avn(size, idx=0):  # Avenir Next: 0 Bold, 2 Demi, 5 Medium, 7 Regular, 8 Heavy
    return _ft("/System/Library/Fonts/Avenir Next.ttc", size, idx)


def charter(size, idx=0):  # 0 Roman, 1 Italic, 3 Bold
    return _ft("Charter.ttc", size, idx)


def bradley(size):
    return _ft("Bradley Hand Bold.ttf", size)


def rounded(size, berat="Bold"):  # SF Rounded: Regular, Medium, Semibold, Bold, Heavy
    return _ft("/System/Library/Fonts/SFNSRounded.ttf", size, 0, berat)


def muat(d, teks, font_fn, maxw, start, stop=12, step=2):
    """Font terbesar supaya teks satu baris muat selebar maxw."""
    for s in range(int(start), int(stop) - 1, -step):
        if d.textlength(teks, font=font_fn(s)) <= maxw:
            return font_fn(s)
    return font_fn(stop)


NBSP = "\u00a0"


def lekat(teks):
    """Jangan memisahkan 'ay. 7', 'pasal 13', '13:4' dsb. di akhir baris (spasi jadi spasi tak-putus)."""
    return re.sub(r"\b(ay\.|ayat|pasal|No\.|no\.) (\d)", lambda m: m.group(1) + NBSP + m.group(2), teks)


def bungkus(d, teks, fnt, maxw):
    """Seperti render.wrap, tapi spasi tak-putus tidak dipisah."""
    lines, cur = [], ""
    for word in [w for w in teks.split(" ") if w]:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def pas_aman(d, teks, font_fn, maxw, maxh, start, stop, lh):
    """Font terbesar supaya teks muat di kotak maxw x maxh; kalau di ukuran terkecil masih kepanjangan, terus mengecil."""
    teks = lekat(teks)
    size = int(start)
    while True:
        f = font_fn(size)
        lines = bungkus(d, teks, f, maxw)
        ok = len(lines) * size * lh <= maxh and max(d.textlength(ln, font=f) for ln in lines) <= maxw
        if ok or size <= 12:
            return f, lines, size
        size -= 1 if size <= stop else 2


def lebar_renggang(d, teks, font, jarak):
    return sum(d.textlength(c, font=font) for c in teks) + jarak * max(0, len(teks) - 1)


def renggang(d, xy, teks, font, fill, jarak, anchor="ls"):
    """Teks dengan jarak antarhuruf. anchor: l/m/r + baris (s, a, m, d). -> lebar total."""
    lebar = lebar_renggang(d, teks, font, jarak)
    x, y = xy
    if anchor[0] == "m":
        x -= lebar / 2
    elif anchor[0] == "r":
        x -= lebar
    for c in teks:
        d.text((x, y), c, font=font, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(c, font=font) + jarak
    return lebar


def renggang_muat(d, teks, font_fn, maxw, start, jarak_rel=0.12, stop=12):
    """Font + jarak huruf terbesar supaya teks renggang muat selebar maxw."""
    for s in range(int(start), stop - 1, -1):
        f = font_fn(s)
        if lebar_renggang(d, teks, f, s * jarak_rel) <= maxw:
            return f, s * jarak_rel
    return font_fn(stop), stop * jarak_rel


def kredit(img, xy, warna, anchor="ma", size=22, font=None):
    ImageDraw.Draw(img).text(xy, "@" + HANDLE, font=font or helv(size, 10), fill=warna, anchor=anchor)


def campur(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def kertas(w, h, warna, seed, kuat=0.05, butir=0.04):
    """Kertas/permukaan polos: warna dasar + belang halus."""
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), np.float32) + np.array(warna, np.float32)
    base *= (1 - kuat + 2 * kuat * render.fbm2d(h, w, rng, ((3, 1.0), (24, 0.5), (160, 0.3))))[..., None]
    return grain(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), butir)


def blok_ayat(img, p, box, font_fn, warna, warna_ref, start=36, stop=20, lh=1.38, ref_font=None, rata="m", vtengah=True,
              ref_jarak=14, ref_teks=None):
    """Ayat + referensi di dalam kotak (x0, y0, x1, y1), ukuran huruf otomatis. -> y bawah teks."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    rf = ref_font or helv(28, 1)
    ref = p["ref"] if ref_teks is None else ref_teks
    rh = rf.size * 1.15 + ref_jarak
    f, lines, size = pas_aman(d, bersih(p["ayat"]), font_fn, x1 - x0, y1 - y0 - rh, start, stop, lh)
    tinggi = len(lines) * size * lh + rh
    y = y0 + max(0, (y1 - y0 - tinggi) / 2) if vtengah else y0
    x, anc = {"m": ((x0 + x1) / 2, "ma"), "l": (x0, "la"), "r": (x1, "ra")}[rata]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=warna, anchor=anc)
        y += size * lh
    d.text((x, y + ref_jarak - size * (lh - 1) * 0.5), ref, font=rf, fill=warna_ref, anchor=anc)
    return y + rh


def teks_lingkar(img, cx, cy, r, teks, font, fill, start_deg=-90.0, jarak=0.0, S=2):
    """Teks melingkar searah jarum jam, kaki huruf menghadap pusat. Tiap huruf = sprite yang diputar sejajar garis
    singgung. start_deg = sudut tepi kiri huruf pertama (-90 = puncak lingkaran). -> sudut akhir (derajat)."""
    lay = Image.new("RGBA", (img.width * S, img.height * S), (0, 0, 0, 0))
    fs = font.font_variant(size=font.size * S)
    th = math.radians(start_deg)
    for ch in teks:
        adv = font.getlength(ch) + jarak
        mid = th + adv / 2 / r
        th += adv / r
        if not ch.strip():
            continue
        sw, sh = int(fs.getlength(ch)) + 8 * S, int(fs.size * 2.6)
        sp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        ImageDraw.Draw(sp).text((sw / 2, sh / 2), ch, font=fs, fill=fill, anchor="ms")
        rot = sp.rotate(-(math.degrees(mid) + 90), resample=Image.BICUBIC, expand=True)
        comp(lay, rot, ((cx + r * math.cos(mid)) * S - rot.width / 2, (cy + r * math.sin(mid)) * S - rot.height / 2))
    img.alpha_composite(lay.resize(img.size, Image.LANCZOS))
    return math.degrees(th)


def kecil_kapital(d, xy, teks, font_fn, size, fill, jarak=0.0, anchor="ls", rasio=0.78):
    """Small caps: huruf kecil ditulis sebagai kapital yang lebih kecil. -> lebar."""
    bagian = [(c.upper(), font_fn(size if (c.isupper() or not c.isalpha()) else size * rasio)) for c in teks]
    lebar = sum(d.textlength(c, font=f) for c, f in bagian) + jarak * max(0, len(bagian) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= lebar / 2
    elif anchor[0] == "r":
        x -= lebar
    for c, f in bagian:
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += d.textlength(c, font=f) + jarak
    return lebar


def bezier3(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = [np.array(v, np.float64) for v in (p0, p1, p2, p3)]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def normal(pts):
    g = np.gradient(pts, axis=0)
    n = np.stack([-g[:, 1], g[:, 0]], 1)
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)


def pita_poly(pts, lebar):
    """Garis tengah + lebar (skalar/array) -> poligon pita."""
    n = normal(pts)
    lw = np.broadcast_to(np.asarray(lebar, np.float64), (len(pts),))[:, None] / 2
    kiri, kanan = pts + n * lw, pts - n * lw
    return [tuple(v) for v in np.vstack([kiri, kanan[::-1]])]


def panah_atas(d, cx, y_atas, lebar, tinggi, fill):
    """Panah ke atas dari poligon (tanpa glyph)."""
    kepala = tinggi * 0.42
    batang = lebar * 0.36
    d.polygon([(cx, y_atas), (cx + lebar / 2, y_atas + kepala), (cx + batang / 2, y_atas + kepala), (cx + batang / 2, y_atas + tinggi),
               (cx - batang / 2, y_atas + tinggi), (cx - batang / 2, y_atas + kepala), (cx - lebar / 2, y_atas + kepala)], fill=fill)


def lapis(w=W, h=H, S=2):
    """Lapisan transparan S kali lebih besar (untuk garis halus)."""
    return Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))


def kecilkan(layer, S=2):
    return layer.resize((layer.width // S, layer.height // S), Image.LANCZOS)


# ================= LATAR & EFEK MINGGU INI =================

# ---------- TENUN: kain tenun ikat ----------

TENUN_PAL = [  # warna dasar (lungsin), benang pakan, warna motif ikat
    ((34, 40, 76), (18, 20, 34), [(234, 218, 184), (186, 80, 48), (222, 166, 66), (126, 42, 46)]),
    ((112, 36, 40), (38, 20, 20), [(238, 222, 188), (228, 170, 68), (40, 54, 98), (28, 24, 26)]),
    ((46, 34, 30), (22, 16, 14), [(208, 146, 68), (178, 80, 52), (230, 212, 176), (46, 108, 108)]),
]
KREM_TENUN = (236, 226, 202)


def _motif_tenun(jenis, u, v, tinggi, dasar, w1, w2):
    """Warna satu baris motif ikat. u: indeks kolom (sudah digeser), v: baris dalam pita. -> (nx, 3)."""
    out = np.zeros((len(u), 3), np.float32) + np.array(dasar, np.float32)
    dv = (v - (tinggi - 1) / 2) / (tinggi / 2)
    if jenis == "ketupat":  # belah ketupat bersusun
        P = max(8, int(tinggi * 1.6))
        du = ((u % P) - P / 2) / (P / 2)
        dd = np.abs(du) + abs(dv)
        cincin = np.floor(dd * 4.4).astype(int)
        out[(dd < 1) & (cincin % 2 == 1)] = w1
        out[(dd < 1) & (cincin == 0)] = w2
        out[(dd >= 1.18) & (dd < 1.5)] = campur(dasar, w2, 0.55)
    elif jenis == "kait":  # zigzag berkait
        P = max(8, tinggi * 2)
        tri = np.abs(((u % P) / P) * 2 - 1)
        vc = 1 + tri * (tinggi - 3)
        out[np.abs(v - vc) < 1.3] = w1
        titik = (np.abs((u % P) - P / 2) < 1.1) & (abs(v - (tinggi - 1) * 0.18) < 1.1)
        titik |= (np.abs(u % P) < 1.1) & (abs(v - (tinggi - 1) * 0.82) < 1.1)
        out[titik] = w2
    elif jenis == "bintang":  # bintang delapan
        P = tinggi + 3
        du = (u % P) - P / 2
        dvv = v - (tinggi - 1) / 2
        s = tinggi / 2 - 0.6
        bintang = (np.abs(du) + abs(dvv) <= s) | (np.maximum(np.abs(du), abs(dvv)) <= s * 0.62)
        out[bintang] = w1
        out[np.abs(du) + abs(dvv) <= s * 0.36] = w2
    else:  # panah (tumpal kecil)
        out[((u + np.abs(dv) * tinggi * 0.5) % 7) < 2.2] = w1
        out[((u + np.abs(dv) * tinggi * 0.5) % 7 >= 3.5) & ((u + np.abs(dv) * tinggi * 0.5) % 7 < 4.3)] = w2
    return out


def tenun_latar(w, h, seed, polos=None, t=6):
    """Kain tenun ikat: pita-pita motif (belah ketupat, kait, bintang, tumpal) dan garis tepi; benang lungsin mendatar
    dengan pinggiran motif yang 'berbulu' khas ikat (tiap benang sedikit bergeser), anyaman benang pakan sesekali tampak,
    belang celup & kerut kain. polos: daftar (y0, y1, "terang"/"gelap") = pita polos tanpa motif (tempat teks)."""
    rng = np.random.default_rng(seed)
    dasar, pakan, mot = TENUN_PAL[seed % len(TENUN_PAL)]
    ny, nx = h // t + 2, w // t + 2
    D = np.zeros((ny, nx, 3), np.float32)
    geser = np.round(2.0 * render.fbm1d(ny, rng, ((5, 1.0), (30, 0.6))) + rng.normal(0, 0.55, ny)).astype(int)
    r = -int(rng.integers(0, 14))
    jenis = ["ketupat", "kait", "bintang", "panah"]
    k = int(rng.integers(0, 4))
    while r < ny:
        tepi = [mot[int(rng.integers(len(mot)))] for _ in range(3)]
        for c, hh in zip(tepi + [dasar], (1, 2, 1, int(rng.integers(2, 5)))):
            if 0 <= r < ny:
                D[max(r, 0):min(r + hh, ny)] = c
            r += hh
        j = jenis[k % 4]
        k += 1 + int(rng.integers(0, 2))
        tinggi = {"ketupat": int(rng.integers(17, 25)), "kait": int(rng.integers(9, 13)), "bintang": int(rng.integers(13, 18)),
                  "panah": int(rng.integers(7, 10))}[j]
        w1, w2 = [mot[q] for q in rng.permutation(len(mot))[:2]]
        if j != "panah" and sum(w1) < 300:  # motif utama sebaiknya terang
            w1, w2 = mot[0], w1
        fase = int(rng.integers(0, 40))
        for v in range(tinggi):
            rr = r + v
            if 0 <= rr < ny:
                D[rr] = _motif_tenun(j, np.arange(nx) + geser[rr] + fase, v, tinggi, dasar, w1, w2)
        r += tinggi
        for c, hh in zip([dasar] + tepi[::-1], (int(rng.integers(2, 4)), 1, 2, 1)):
            if 0 <= r < ny:
                D[r:min(r + hh, ny)] = c
            r += hh
    pakan_b = np.zeros((ny, 3), np.float32) + np.array(pakan, np.float32)  # warna pakan per baris benang
    lembut = np.zeros(ny, np.float32)  # 1 = pita polos terang: tekstur dibuat lebih halus supaya teks terbaca
    for y0, y1, jenis_polos in (polos or []):
        a, b = max(0, int(y0 // t)), min(ny, int(math.ceil(y1 / t)))
        D[a:b] = KREM_TENUN if jenis_polos == "terang" else dasar
        if jenis_polos == "terang":
            pakan_b[a:b] = campur(KREM_TENUN, (120, 100, 80), 0.18)
            lembut[a:b] = 1
        if jenis_polos == "terang":  # garis tepi pita polos
            for rr, c in ((a, mot[1]), (a + 1, dasar), (b - 2, dasar), (b - 1, mot[1])):
                if 0 <= rr < ny:
                    D[rr] = c
    yy, xx = np.mgrid[0:h, 0:w]
    j, c = yy // t, xx // t
    fy, fx = (yy % t + 0.5) / t, (xx % t + 0.5) / t
    warna = D[j, c]
    variasi = (0.93 + 0.12 * rng.random(ny)).astype(np.float32)
    variasi = variasi * (1 - lembut) + (0.98 + 0.03 * rng.random(ny)) * lembut
    k_ = 0.34 - 0.24 * lembut[j]
    lungsin = warna * ((1 - k_ + k_ * np.sin(np.pi * fy)) * (0.92 + 0.08 * np.sin(np.pi * fx)) * variasi[j])[..., None]
    pakan_c = pakan_b[j] * ((0.6 + 0.4 * np.sin(np.pi * fx)) * (0.85 + 0.15 * np.sin(np.pi * fy)))[..., None]
    atas = ((c + 2 * (j % 2)) % 4) != 0
    out = np.where(atas[..., None], lungsin, pakan_c * 0.7 + lungsin * 0.3)
    out *= (0.9 + 0.12 * render.fbm2d(h, w, rng, ((2, 1.0), (7, 0.5))))[..., None]
    out *= (1 + 0.05 * np.sin((xx * 0.55 + yy) / 150.0 + rng.uniform(0, 6)))[..., None]
    out *= (0.95 + 0.07 * rng.random((h, w)))[..., None]
    return grain(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 0.04)


# ---------- SENJA: langit senja dengan matahari rendah ----------

SENJA_PAL = [
    [(0.0, (50, 46, 104)), (0.3, (106, 72, 142)), (0.58, (198, 112, 150)), (0.82, (244, 148, 126)), (1.0, (255, 200, 148))],
    [(0.0, (44, 52, 110)), (0.32, (118, 82, 150)), (0.6, (214, 120, 140)), (0.84, (248, 162, 120)), (1.0, (255, 210, 156))],
    [(0.0, (62, 44, 96)), (0.3, (128, 70, 130)), (0.58, (222, 116, 132)), (0.83, (250, 156, 112)), (1.0, (255, 214, 160))],
]


def senja_latar(w, h, seed, cakrawala=0.74, matahari=None, redup=0.0, pantul=1.0):
    """Langit senja lembut (ungu di atas -> merah muda -> jingga di cakrawala), matahari rendah tenggelam di laut,
    awan tipis berbingkai cahaya, pulau jauh, dan pantulan matahari di air."""
    rng = np.random.default_rng(seed)
    stops = SENJA_PAL[seed % len(SENJA_PAL)]
    hz = int(h * cakrawala)
    ys = np.arange(h, dtype=np.float32)
    tt = np.clip(ys / max(hz, 1), 0, 1)
    pos = [s[0] for s in stops]
    sky = np.stack([np.interp(tt, pos, [s[1][k] for s in stops]) for k in range(3)], 1)
    out = np.zeros((h, w, 3), np.float32) + sky[:, None, :]
    sx = w * (matahari if matahari is not None else rng.uniform(0.3, 0.7))
    rs = w * 0.068
    sy = hz - rs * 0.32
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dist = np.hypot(xx - sx, (yy - sy) * 1.25)
    langit = (yy < hz)[..., None]
    out += langit * (np.exp(-(dist / (w * 0.42)) ** 2)[..., None] * np.array([70, 34, 6], np.float32))
    out += langit * (np.exp(-(dist / (rs * 2.6)) ** 2)[..., None] * np.array([80, 52, 20], np.float32))
    out += langit * (np.exp(-(dist / (rs * 1.4)) ** 2)[..., None] * np.array([60, 50, 30], np.float32))
    # awan tipis memanjang
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for _ in range(14):
        cy = rng.uniform(0.18, 0.95) * hz
        cx = rng.uniform(-0.1, 1.1) * w
        u = cy / hz
        col = campur((150, 110, 170), (255, 186, 160), u ** 1.4)
        for _ in range(4):
            lw, lh = rng.uniform(160, 420), rng.uniform(5, 14)
            ox, oy = rng.uniform(-120, 120), rng.uniform(-10, 10)
            ld.ellipse((cx + ox - lw, cy + oy - lh, cx + ox + lw, cy + oy + lh), fill=col + (int(rng.uniform(50, 110)),))
    lay = lay.filter(ImageFilter.GaussianBlur(7))
    a = np.asarray(lay).astype(np.float32)
    al = a[..., 3:4] / 255 * langit
    out = out * (1 - al) + a[..., :3] * al
    # matahari
    cakram = np.clip((rs - dist / 1.25 * 1.0) / 2.0, 0, 1) * (yy < hz)
    out = out * (1 - cakram[..., None]) + np.array([255, 232, 178], np.float32) * cakram[..., None]
    # laut
    if hz < h:
        dl = np.clip((ys - hz) / max(1, h - hz), 0, 1)
        laut_atas, laut_bawah = campur(stops[-2][1], (90, 60, 110), 0.55), (36, 32, 72)
        lautc = np.stack([np.interp(dl ** 0.7, [0, 1], [laut_atas[k], laut_bawah[k]]) for k in range(3)], 1)
        out[hz:] = lautc[hz:, None, :]
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for y in range(hz + 2, h, 3):
            u = (y - hz) / max(1, h - hz)
            hw = rs * (0.55 + 2.4 * u ** 0.85)
            al_ = (1 - u) ** 1.2 * 235 * pantul
            for _ in range(3):
                x0 = sx + rng.uniform(-hw, hw)
                ln = rng.uniform(10, 40) * (1 + 2 * u)
                ld.line((x0 - ln, y, x0 + ln, y), fill=(255, 206, 156, int(al_ * rng.uniform(0.3, 1))), width=2)
            if rng.random() < 0.5:  # riak
                x0, ln = rng.uniform(0, w), rng.uniform(20, 80)
                ld.line((x0 - ln, y, x0 + ln, y), fill=(220, 170, 200, int(40 * (1 - u))), width=1)
        lay = lay.filter(ImageFilter.GaussianBlur(0.8))
        a = np.asarray(lay).astype(np.float32)
        al = a[..., 3:4] / 255
        out = out * (1 - al) + a[..., :3] * al
        # pulau jauh di cakrawala
        pd = Image.new("L", (w, h), 0)
        pdd = ImageDraw.Draw(pd)
        for _ in range(2):
            px0 = rng.uniform(-0.1, 0.75) * w
            pw = rng.uniform(0.18, 0.4) * w
            if abs((px0 + pw / 2) - sx) < pw / 2 + rs:
                px0 = (sx + rs * 1.4) if sx < w / 2 else (sx - rs * 1.4 - pw)
            tinggi = rng.uniform(10, 26)
            xs = np.linspace(px0, px0 + pw, 40)
            prof = np.sin(np.linspace(0, np.pi, 40)) ** 0.7 * tinggi * (0.85 + 0.15 * np.sin(np.linspace(0, 9, 40)))
            pdd.polygon([(px0, hz + 1)] + [(x, hz + 1 - pr) for x, pr in zip(xs, prof)] + [(px0 + pw, hz + 1)], fill=255)
        m = np.asarray(pd.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[..., None] / 255
        out = out * (1 - m) + np.array(campur(stops[1][1], (40, 30, 60), 0.5), np.float32) * m
    # bintang samar di puncak
    for _ in range(40):
        x, y = int(rng.uniform(0, w)), int(rng.uniform(0, hz * 0.22))
        out[y:y + 2, x:x + 2] = np.minimum(255, out[y:y + 2, x:x + 2] + rng.uniform(30, 90) * (1 - y / (hz * 0.22)))
    if redup:
        out *= 1 - redup
    return grain(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 0.03)


# ---------- HANGAT: efek film hangat untuk gambar jadi ----------

def hangat(img, seed, kuat=1.0):
    """Efek film hangat: sepia lembut, bayangan pudar kecokelatan, halasi pada bagian terang, vinyet, butir film,
    sedikit debu. Terasa seperti foto kenangan sebulan."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255
    h, w = a.shape[:2]
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    sepia = np.stack([lum * 1.07 + 0.03, lum * 0.94 + 0.012, lum * 0.74 - 0.005], -1)
    out = a * (1 - 0.48 * kuat) + sepia * 0.48 * kuat
    out = 0.055 * np.array([1.0, 0.8, 0.6], np.float32) + out * 0.92  # hitam pudar & hangat
    out *= np.array([1.03, 1.0, 0.92], np.float32)
    terang = Image.fromarray((np.clip((lum - 0.72) / 0.28, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
    out += (np.asarray(terang).astype(np.float32) / 255)[..., None] * np.array([0.07, 0.03, 0.0], np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    v = 1 - 0.34 * np.clip((r - 0.5) / 0.5, 0, 1) ** 1.5
    out *= v[..., None] * (1 - (1 - v)[..., None] * np.array([0.0, 0.08, 0.2], np.float32))
    bocor = np.exp(-(np.hypot((xx - w * rng.choice([0.0, 1.0])) / w, (yy - h * rng.uniform(0.0, 0.3)) / h) / 0.38) ** 2)
    out += bocor[..., None] * np.array([0.09, 0.04, 0.0], np.float32)
    lum2 = out @ np.array([0.299, 0.587, 0.114], np.float32)
    n = Image.fromarray(np.clip(rng.normal(128, 40, (h, w)), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    nb = (np.asarray(n).astype(np.float32) - 128) / 128
    out += (nb * 0.06 * (0.5 + 2.0 * lum2 * (1 - lum2)))[..., None]
    res = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(res)
    n = 0
    while n < 12:  # debu & serat hanya di bingkai luar, supaya tidak mirip tanda baca di atas teks
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        if min(x, y, w - x, h - y) > 34 or (y > h - 80 and abs(x - w / 2) < 220):
            continue
        rr = rng.uniform(0.8, 2.0)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(250, 240, 220) if rng.random() < 0.6 else (60, 44, 30))
        n += 1
    for x, y in ((rng.uniform(8, 24), rng.uniform(0.3, 0.6) * h), (w - rng.uniform(8, 24), rng.uniform(0.4, 0.7) * h)):
        pts = [(x + 5 * math.sin(k * 0.9) + rng.normal(0, 1.5), y + 22 * k) for k in range(5)]
        d.line(pts, fill=(236, 226, 206), width=1)
    return res


# ================= BARU =================

# ---------- KALKULATOR: kalkulator meja berpita kertas ----------

SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg",
       "9": "abcdfg", "-": "g", "−": "g", "E": "afged", "r": "eg", "o": "cdeg", "A": "abcefg", "b": "cdefg", "C": "adef", "d": "bcdeg",
       "F": "aefg", "H": "bcefg", "L": "def", "n": "ceg", "P": "abefg", "t": "defg", "U": "bcdef", "y": "bcdfg", " ": ""}


def segmen_poly(seg, x, y, dw, dh, th, gap, miring=0.09):
    """Poligon heksagonal satu batang 7-segmen; (x, y) = pojok kiri atas digit."""
    h2 = th / 2

    def mendatar(xa, xb, yy):
        return [(xa, yy), (xa + h2, yy - h2), (xb - h2, yy - h2), (xb, yy), (xb - h2, yy + h2), (xa + h2, yy + h2)]

    def tegak(xx, ya, yb):
        return [(xx, ya), (xx + h2, ya + h2), (xx + h2, yb - h2), (xx, yb), (xx - h2, yb - h2), (xx - h2, ya + h2)]
    m = dh / 2
    pts = {"a": mendatar(gap, dw - gap, 0), "g": mendatar(gap, dw - gap, m), "d": mendatar(gap, dw - gap, dh),
           "f": tegak(0, gap, m - gap), "b": tegak(dw, gap, m - gap), "e": tegak(0, m + gap, dh - gap), "c": tegak(dw, m + gap, dh - gap)}[seg]
    return [(x + px + (dh - py) * miring, y + py) for px, py in pts]


def sel_7seg(teks):
    """'490' / '3.5' -> daftar (karakter, titik_desimal)."""
    sel = []
    for ch in teks:
        if ch in ".,":
            if sel and not sel[-1][1]:
                sel[-1] = (sel[-1][0], True)
            else:
                sel.append((" ", True))
        else:
            sel.append((ch if ch in SEG else (ch.upper() if ch.upper() in SEG else " "), False))
    return sel


def kunci(d, box, warna, label, f, warna_label, tekan=False):
    x0, y0, x1, y1 = box
    bibir = 3 if tekan else 7
    d.rounded_rectangle((x0, y0 + 4, x1, y1 + 4), radius=14, fill=(0, 0, 0, 60))
    d.rounded_rectangle((x0, y0 + bibir, x1, y1), radius=14, fill=campur(warna, (0, 0, 0), 0.38))
    d.rounded_rectangle((x0, y0 + (bibir - 7 if tekan else 0) + 4 * tekan, x1, y1 - bibir), radius=14, fill=warna)
    d.line((x0 + 14, y0 + 2 + 4 * tekan, x1 - 14, y0 + 2 + 4 * tekan), fill=campur(warna, (255, 255, 255), 0.18), width=2)
    d.text(((x0 + x1) / 2, (y0 + y1 - bibir) / 2 + 2 * tekan + 3), label, font=f, fill=warna_label, anchor="mm")


def kalkulator_image(p, i):
    rng = np.random.default_rng(18000 + i)
    meja = [(236, 233, 226), (226, 230, 232), (238, 230, 222)][i % 3]
    tubuh, lcd, digit, tombol, oranye, kertas_c, tinta_c = (214, 210, 202), (178, 190, 160), (40, 48, 40), (60, 60, 64), (240, 110, 40), (250, 248, 240), (40, 40, 40)
    img = kertas(W, H, meja, 18000 + i, kuat=0.02, butir=0.03).convert("RGBA")
    bx0, by0, bx1, by1 = 150, 296, 930, 1004
    # badan + bayangan
    badan = Image.new("RGBA", (bx1 - bx0, by1 - by0), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badan)
    bd.rounded_rectangle((0, 0, badan.width - 1, badan.height - 1), radius=46, fill=tubuh + (255,))
    ba = np.asarray(badan).astype(np.float32)
    ba[..., :3] *= np.linspace(1.04, 0.93, badan.height)[:, None, None]
    badan = Image.fromarray(np.clip(ba, 0, 255).astype(np.uint8))
    bd = ImageDraw.Draw(badan)
    bd.rounded_rectangle((2, 2, badan.width - 3, badan.height - 3), radius=44, outline=(255, 255, 255, 90), width=2)
    bayangan(img, badan, (bx0, by0), blur=26, geser=(0, 22), kuat=0.32)
    d = ImageDraw.Draw(img)
    # celah printer + pita kertas
    sy = by0 + 40
    d.rounded_rectangle((bx0 + 140, sy - 8, bx1 - 140, sy + 8), radius=8, fill=(52, 52, 56))
    tw_, tx0 = 500, W / 2 - 250
    ty0 = 22
    pita = Image.new("RGBA", (tw_, int(sy - ty0)), kertas_c + (255,))
    pa = np.asarray(pita).astype(np.float32)
    pa[..., :3] *= (0.97 + 0.04 * render.fbm2d(pita.height, tw_, rng, ((4, 1.0), (30, 0.4))))[..., None]
    pa[..., :3] *= np.concatenate([np.ones(tw_ - 40), np.linspace(1, 0.9, 40)])[None, :, None]  # lengkung tepi kanan
    mask = Image.new("L", pita.size, 0)
    zz = [(x, 26 + (9 if (x // 16) % 2 else -9) + rng.uniform(-3, 3)) for x in range(0, tw_ + 16, 16)]
    ImageDraw.Draw(mask).polygon([(0, pita.height)] + zz + [(tw_, pita.height)], fill=255)
    pita = Image.fromarray(np.clip(pa, 0, 255).astype(np.uint8))
    pita.putalpha(mask)
    pd = ImageDraw.Draw(pita)
    baris = [bersih(t) for t in p["tape"]][:3]
    fk = kurir(32, True)
    while max(pd.textlength(b, font=fk) for b in baris) > tw_ - 56 and fk.size > 18:
        fk = kurir(fk.size - 1, True)
    yb = pita.height - 44
    for k, b in enumerate(reversed(baris)):
        pd.text((tw_ - 28, yb - k * fk.size * 1.65), b, font=fk, fill=tinta_c + (235,), anchor="rs")
    ys = yb - len(baris) * fk.size * 1.65 + 6
    for x in range(28, tw_ - 28, 14):
        pd.line((x, ys, x + 6, ys), fill=(150, 150, 150, 200), width=2)
    bayangan(img, pita, (tx0, ty0), blur=10, geser=(6, 6), kuat=0.22)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((bx0 + 140, sy + 2, bx1 - 140, sy + 10), radius=5, fill=(70, 70, 74))
    d.line((bx0 + 150, sy + 12, bx1 - 150, sy + 12), fill=(236, 233, 228), width=2)
    # layar LCD
    lx0, ly0, lx1, ly1 = bx0 + 60, by0 + 80, bx1 - 60, by0 + 262
    d.rounded_rectangle((lx0, ly0, lx1, ly1), radius=20, fill=(120, 118, 112))
    d.rounded_rectangle((lx0 + 12, ly0 + 12, lx1 - 12, ly1 - 12), radius=12, fill=lcd)
    for k in range(14):  # bayang dalam
        d.line((lx0 + 20, ly0 + 13 + k, lx1 - 20, ly0 + 13 + k), fill=campur(lcd, (90, 100, 80), 0.3 * (1 - k / 14)), width=1)
    S = 3
    seg = Image.new("RGBA", ((lx1 - lx0) * S, (ly1 - ly0) * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seg)
    sel = sel_7seg(bersih(str(p["hasil"])))[-8:]
    dw, dh, th, pitch = 42, 78, 10, 66
    x_kanan = (lx1 - lx0) - 40 - dw - 8
    yd = ly1 - ly0 - dh - 24
    for n in range(8):
        x = x_kanan - n * pitch
        for s_ in "abcdefg":
            sd.polygon([(px * S, py * S) for px, py in segmen_poly(s_, x, yd, dw, dh, th, 2.5)], fill=digit + (22,))
        sd.rectangle(((x + dw + 6) * S, (yd + dh - 8) * S, (x + dw + 14) * S, (yd + dh) * S), fill=digit + (22,))
        if n < len(sel):
            ch, titik = sel[len(sel) - 1 - n]
            for s_ in SEG.get(ch, ""):
                sd.polygon([(px * S, py * S) for px, py in segmen_poly(s_, x, yd, dw, dh, th, 2.5)], fill=digit + (255,))
            if titik:
                sd.rectangle(((x + dw + 6) * S, (yd + dh - 8) * S, (x + dw + 14) * S, (yd + dh) * S), fill=digit + (255,))
    img.alpha_composite(seg.resize((lx1 - lx0, ly1 - ly0), Image.LANCZOS), (lx0, ly0))
    d = ImageDraw.Draw(img)
    hit = bersih(p["hitung"])
    hit = hit if hit.endswith("=") else hit + "="
    d.text((lx1 - 40, ly0 + 54), hit, font=muat(d, hit, din, 380, 36, 20), fill=digit, anchor="rs")
    for k, lab in enumerate(("M", "GT", "PRINT")):
        d.text((lx0 + 34 + k * 56, ly0 + 54), lab, font=din(20), fill=campur(lcd, digit, 0.55 if k == 2 else 0.18), anchor="ls")
    # label teknis kecil
    yl = by0 + 293
    d.ellipse((bx0 + 66, yl - 7, bx0 + 80, yl + 7), fill=oranye)
    d.text((bx0 + 92, yl), "PRINT", font=din(22), fill=(96, 92, 86), anchor="lm")
    d.rounded_rectangle((bx0 + 190, yl - 12, bx0 + 270, yl + 12), radius=12, fill=(176, 172, 164))
    d.rounded_rectangle((bx0 + 236, yl - 10, bx0 + 268, yl + 10), radius=10, fill=(70, 70, 74))
    d.text((bx0 + 282, yl), "ON", font=din(22), fill=(96, 92, 86), anchor="lm")
    d.text((bx1 - 66, yl), "Σ  ·  GT  ·  TAPE 58 MM", font=din(22), fill=(120, 116, 108), anchor="rm")
    # tombol 4 x 5
    kx0, ky0, kx1, ky1 = bx0 + 60, by0 + 322, bx1 - 60, by1 - 44
    cw, rh = (kx1 - kx0) / 4, (ky1 - ky0) / 5
    tata = [(0, 0, 1, "C", "c"), (0, 1, 1, "÷", "f"), (0, 2, 1, "×", "f"), (0, 3, 1, "−", "f"),
            (1, 0, 1, "7", "n"), (1, 1, 1, "8", "n"), (1, 2, 1, "9", "n"), (1, 3, 2, "+", "f"),
            (2, 0, 1, "4", "n"), (2, 1, 1, "5", "n"), (2, 2, 1, "6", "n"),
            (3, 0, 1, "1", "n"), (3, 1, 1, "2", "n"), (3, 2, 1, "3", "n"), (3, 3, 2, "=", "e"),
            (4, 0, 1, "0", "n"), (4, 1, 1, "00", "n"), (4, 2, 1, ".", "n")]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(lay)
    for r_, c_, span, lab, jenis in tata:
        box = (kx0 + c_ * cw + 9, ky0 + r_ * rh + 7, kx0 + (c_ + 1) * cw - 9, ky0 + (r_ + span) * rh - 7)
        warna = {"c": (182, 178, 170), "f": (92, 92, 98), "n": tombol, "e": oranye}[jenis]
        kunci(kd, box, warna, lab, din(46), (40, 40, 44) if jenis == "c" else (255, 255, 255), tekan=jenis == "e")
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    blok_ayat(img, p, (100, by1 + 40, W - 100, H - 70), lambda s: charter(s), (44, 42, 40), (214, 92, 30), start=34, stop=22,
              lh=1.36, ref_font=din(32))
    kredit(img, (W / 2, H - 46), (150, 146, 138))
    return img


# ---------- UNSUR: petak tabel periodik "Kasih" ----------

POLA_PERIODIK = ["1................1", "11..........111111", "11..........111111", "111111111111111111",
                 "111111111111111111", "111111111111111111", "111111111111111111"]


def molekul(d, cx, cy, s, col, rng, w=3):
    """Coretan molekul: bola + tongkat."""
    titik = [(cx, cy)]
    for k in range(3):
        a = rng.uniform(0, 2 * math.pi) if k == 0 else a + rng.uniform(1.6, 2.6)
        titik.append((cx + math.cos(a) * s, cy + math.sin(a) * s))
    for x, y in titik[1:]:
        d.line((cx, cy, x, y), fill=col, width=w)
    d.line((cx + 4, cy + 4, titik[1][0] + 4, titik[1][1] + 4), fill=col, width=w)
    for k, (x, y) in enumerate(titik):
        rr = s * (0.32 if k == 0 else 0.2)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(250, 246, 238), outline=col, width=w)


def unsur_image(p, i):
    rng = np.random.default_rng(18100 + i)
    krem, garis, pink, teal, amber, teks = (250, 246, 238), (40, 40, 48), (236, 88, 120), (60, 170, 170), (240, 170, 60), (30, 30, 36)
    aksen = [pink, (230, 110, 90), (200, 80, 150)][i % 3]
    img = kertas(W, H, krem, 18100 + i, kuat=0.02, butir=0.03).convert("RGBA")
    d = ImageDraw.Draw(img)
    # siluet tabel periodik samar
    sel = 52
    sx0, sy0 = (W - 18 * sel) / 2, 108
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for r_, row in enumerate(POLA_PERIODIK):
        for c_, v in enumerate(row):
            if v == "1":
                x, y = sx0 + c_ * sel, sy0 + r_ * sel
                ld.rounded_rectangle((x + 3, y + 3, x + sel - 3, y + sel - 3), radius=6, fill=garis + (10,), outline=garis + (34,), width=2)
    for c_, col in zip(rng.choice([12, 13, 14, 15, 16], 3, replace=False), (aksen, teal, amber)):
        x, y = sx0 + c_ * sel, sy0 + sel
        ld.rounded_rectangle((x + 3, y + 3, x + sel - 3, y + sel - 3), radius=6, fill=col + (110,))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    renggang(d, (90, 70), "INFOGRAFIK KASIH", avn(24, 0), garis, 4, "ls")
    renggang(d, (W - 90, 70), "TABEL UNSUR KEHIDUPAN", avn(20, 2), aksen, 3, "rs")
    d.line((90, 84, W - 90, 84), fill=garis, width=2)
    # petak utama
    tx0, ty0, tx1, ty1 = 90, 236, 560, 772
    petak = Image.new("RGBA", (tx1 - tx0, ty1 - ty0), (0, 0, 0, 0))
    pd = ImageDraw.Draw(petak)
    pw, ph = petak.size
    pd.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=22, fill=(255, 253, 249, 255), outline=garis + (255,), width=6)
    pd.rounded_rectangle((6, ph - 106, pw - 7, ph - 7), radius=16, fill=aksen + (255,))
    pd.rectangle((6, ph - 106, pw - 7, ph - 76), fill=aksen + (255,))
    pd.text((34, 26), bersih(str(p["nomor"])), font=avn(64, 0), fill=teks + (255,))
    ax, ay = pw - 74, 70  # ikon atom
    for sud in (0, 60, 120):
        orb = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        ImageDraw.Draw(orb).ellipse((8, 40, 112, 80), outline=aksen + (255,), width=3)
        orb = orb.rotate(sud, resample=Image.BICUBIC)
        petak.alpha_composite(orb, (ax - 60, ay - 60))
    pd.ellipse((ax - 9, ay - 9, ax + 9, ay + 9), fill=aksen + (255,))
    simbol = bersih(p["simbol"])
    fn = muat(pd, bersih(p["nama"]), lambda s: avn(s, 2), pw - 60, 58, 30)
    nb_ = ph - 140
    atas, bawah = 134, nb_ - pd.textbbox((0, 0), bersih(p["nama"]), font=fn, anchor="ls")[1] * -1 - 18
    for uk in range(250, 80, -4):  # simbol terbesar yang muat (termasuk kaki huruf seperti p, g, y)
        fs = helv(uk, 1)
        bb = pd.textbbox((0, 0), simbol, font=fs, anchor="ls")
        if bb[2] - bb[0] <= pw - 110 and bb[3] - bb[1] <= bawah - atas:
            break
    pd.text((pw / 2 - (bb[0] + bb[2]) / 2, (atas + bawah) / 2 - (bb[1] + bb[3]) / 2), simbol, font=fs, fill=teks + (255,), anchor="ls")
    pd.text((pw / 2, nb_), bersih(p["nama"]), font=fn, fill=teks + (255,), anchor="ms")
    kat = bersih(p["kategori"]).upper()
    f, jr = renggang_muat(pd, kat, lambda s: avn(s, 0), pw - 70, 30, 0.08)
    renggang(pd, (pw / 2, ph - 56), kat, f, (255, 255, 255, 255), jr, "mm")
    bayangan(img, petak, (tx0, ty0), blur=16, geser=(8, 14), kuat=0.22)
    # petak tetangga
    nb = [(610, 236, 990, 488, teal), (610, 520, 990, 772, amber)]
    for (x0, y0, x1, y1, col), (sim, nama) in zip(nb, p["tetangga"]):
        t = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        td = ImageDraw.Draw(t)
        tw, th_ = t.size
        td.rounded_rectangle((0, 0, tw - 1, th_ - 1), radius=18, fill=col + (255,), outline=garis + (255,), width=4)
        renggang(td, (28, 44), "TETANGGA", avn(18, 0), (255, 255, 255, 230), 3, "ls")
        fn2 = muat(td, bersih(nama), lambda s: avn(s, 2), tw - 60, 40, 22)
        td.text((28, 96), bersih(nama), font=fn2, fill=garis + (255,), anchor="ls")
        fs2 = muat(td, bersih(sim), lambda s: helv(s, 1), tw - 80, 128, 60)
        td.text((tw - 30, th_ - 28), bersih(sim), font=fs2, fill=(255, 255, 255, 255), anchor="rs")
        bayangan(img, t, (x0, y0), blur=12, geser=(6, 10), kuat=0.18)
    d = ImageDraw.Draw(img)
    for yb, col in ((362, teal), (646, amber)):  # ikatan antarpetak
        d.line((562, yb - 7, 608, yb - 7), fill=garis, width=4)
        d.line((562, yb + 7, 608, yb + 7), fill=garis, width=4)
        d.ellipse((577, yb - 8, 593, yb + 8), fill=col, outline=garis, width=3)
    # kotak fakta
    lebar = (W - 180 - 48) / 3
    uk = min(pas_aman(d, bersih(f_), lambda s: avn(s, 5), lebar - 44, 100, 30, 18, 1.22)[2] for f_ in p["sifat"])
    for k, (fakta, col) in enumerate(zip(p["sifat"], (aksen, teal, amber))):
        x0, y0 = 90 + k * (lebar + 24), 812
        x1, y1 = x0 + lebar, 1012
        d.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(255, 253, 249), outline=garis, width=3)
        d.rounded_rectangle((x0, y0, x1, y0 + 14), radius=6, fill=col)
        d.ellipse((x0 + 20, y0 + 32, x0 + 58, y0 + 70), fill=col)
        d.text((x0 + 39, y0 + 51), str(k + 1), font=avn(24, 0), fill=(255, 255, 255), anchor="mm")
        d.text((x0 + 70, y0 + 51), "FAKTA", font=avn(20, 0), fill=(120, 116, 110), anchor="lm")
        f, lines, size = pas_aman(d, bersih(fakta), lambda s: avn(s, 5), lebar - 44, 100, uk, 12, 1.22)
        y = y0 + 88
        for ln in lines:
            d.text((x0 + 22, y), ln, font=f, fill=teks)
            y += size * 1.22
    molekul(d, 950, 166, 34, aksen, rng)
    molekul(d, 140, 166, 26, teal, rng, w=2)
    # pita kaki: ayat
    d.rectangle((0, 1046, W, H), fill=garis)
    d.line((0, 1046, W, 1046), fill=aksen, width=6)
    blok_ayat(img, p, (100, 1076, W - 100, H - 64), lambda s: charter(s, 1), (246, 240, 228), aksen, start=32, stop=20,
              lh=1.36, ref_font=avn(26, 0))
    kredit(img, (W / 2, H - 44), (150, 150, 162))
    return img


# ---------- PALET: kartu contoh warna cat ----------

def _lin(c):
    return (np.array(c, np.float64) / 255) ** 2.2


def _srgb(v):
    return tuple(int(round(255 * min(1.0, max(0.0, x)) ** (1 / 2.2))) for x in v)


def tangga_warna(dasar, n=6, pucat=0.2):
    """Gradasi dengan gamma yang benar: pucat (dasar dicampur putih) -> dasar."""
    a, b = _lin((255, 255, 255)) * (1 - pucat) + _lin(dasar) * pucat, _lin(dasar)
    return [_srgb(a + (b - a) * t) for t in np.linspace(0, 1, n) ** 0.75]


def gelap_warna(c):
    r, g, b = [v / 255 for v in c]
    return 0.2126 * r ** 2.2 + 0.7152 * g ** 2.2 + 0.0722 * b ** 2.2 < 0.22


def kartu_warna(lebar, tinggi, ramp, judul=None, sub=None, chips=None, ref=None):
    k = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    d = ImageDraw.Draw(k)
    d.rounded_rectangle((0, 0, lebar - 1, tinggi - 1), radius=14, fill=(252, 251, 248, 255))
    head, kaki = 120, 84
    ch = (tinggi - head - kaki - 5 * 6) / 6
    for n, col in enumerate(ramp):
        y0 = head + n * (ch + 6)
        d.rectangle((22, y0, lebar - 22, y0 + ch), fill=col + (255,))
        if chips:
            nama, kode = [bersih(str(v)) for v in chips[n]]
            tc = (255, 255, 255, 255) if gelap_warna(col) else (40, 40, 40, 255)
            fn = muat(d, nama, lambda s: helv(s, 10), lebar - 100, 30, 18)
            d.text((46, y0 + ch - 48), nama, font=fn, fill=tc, anchor="ls")
            d.text((46, y0 + ch - 20), kode, font=menlo(18), fill=tc[:3] + (200,), anchor="ls")
            d.text((lebar - 46, y0 + ch - 20), f"{n + 1:02d}", font=menlo(18), fill=tc[:3] + (160,), anchor="rs")
    if judul:
        d.text((24, 52), judul, font=muat(d, judul, lambda s: helv(s, 1), lebar - 48, 38, 22), fill=(36, 36, 36, 255), anchor="ls")
        d.text((24, 88), sub, font=menlo(17), fill=(120, 120, 120, 255), anchor="ls")
        d.text((lebar - 24, tinggi - 40), ref or "", font=menlo(17), fill=(120, 120, 120, 255), anchor="rs")
    return k


def palet_image(p, i):
    rng = np.random.default_rng(18200 + i)
    img = kertas(W, H, (230, 230, 228), 18200 + i, kuat=0.03, butir=0.03).convert("RGBA")
    dasar = tuple(int(v) for v in p.get("warna_dasar", (190, 50, 70)))
    hue = colorsys.rgb_to_hsv(*[v / 255 for v in dasar])[0]
    belakang = (30, 110, 110) if not (0.38 < hue < 0.6) else (190, 50, 70)
    x0, y0, cw, chh = 214, 54, 560, 880
    piv = (x0 + 46, y0 + chh - 46)
    # kartu belakang dikipas 8 derajat terhadap paku keling di pojok kiri bawah
    for sudut, warna_b in ((8, belakang),):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(kartu_warna(cw, chh, tangga_warna(warna_b)), (x0, y0))
        lay = lay.rotate(-sudut, resample=Image.BICUBIC, center=piv)
        bayangan(img, lay, (0, 0), blur=16, geser=(4, 10), kuat=0.28)
    ramp = tangga_warna(dasar)
    judul = bersih(p["nama_kartu"])
    kartu = kartu_warna(cw, chh, ramp, judul, "6 nuansa · 1 kasih", p["chip"], "KARTU WARNA No. " + str(13 + i))
    bayangan(img, kartu, (x0, y0), blur=18, geser=(6, 14), kuat=0.32)
    d = ImageDraw.Draw(img)
    px, py = piv
    d.ellipse((px - 17, py - 17, px + 17, py + 17), fill=(150, 146, 140))
    d.ellipse((px - 13, py - 13, px + 13, py + 13), fill=(206, 202, 194))
    d.ellipse((px - 6, py - 9, px + 2, py - 1), fill=(240, 238, 232))
    blok_ayat(img, p, (100, y0 + chh + 96, W - 100, H - 70), lambda s: charter(s), (44, 42, 42), campur(dasar, (0, 0, 0), 0.1),
              start=34, stop=22, lh=1.36, ref_font=helv(28, 1))
    kredit(img, (W / 2, H - 46), (140, 140, 140))
    return img


# ---------- MUARA: banyak sungai, satu muara ----------

MUARA_WARNA = [(230, 90, 70), (240, 160, 60), (230, 200, 70), (120, 180, 90), (60, 160, 150), (70, 120, 200), (130, 90, 180), (200, 90, 140)]


def muara_image(p, i):
    rng = np.random.default_rng(18300 + i)
    krem = (246, 242, 232)
    sungai = [(36, 58, 100), (30, 70, 96), (52, 50, 98)][i % 3]
    img = kertas(W, H, krem, 18300 + i, kuat=0.025, butir=0.03).convert("RGBA")
    S = 2
    src = [bersih(s) for s in p["sumber"]][:8]
    n = len(src)
    warna = [MUARA_WARNA[k] for k in np.round(np.linspace(0, 7, n)).astype(int)]
    xs = np.linspace(150, W - 150, n) + rng.uniform(-12, 12, n)
    ys = np.array([186 if k % 2 == 0 else 262 for k in range(n)], np.float64) + rng.uniform(-10, 10, n)
    ym, yr = 690, 930
    gap = 5
    w_slot = min(40, (380 - (n - 1) * gap) / n)
    tot = n * w_slot + (n - 1) * gap
    slot = W / 2 - tot / 2 + w_slot / 2 + np.arange(n) * (w_slot + gap)
    W_riv = 900
    w_riv = (W_riv - (n - 1) * gap) / n
    riv = W / 2 - W_riv / 2 + w_riv / 2 + np.arange(n) * (w_riv + gap)
    # tubuh sungai (muara) di bawah: tepi atas bergelombang, makin lebar ke bawah
    tepi = Image.new("L", (W * S, H * S), 0)
    atas = [(x, yr - 30 + 120 * (abs(x - W / 2) / (W / 2)) ** 4 + 7 * math.sin(x / 57 + i)) for x in np.linspace(30, W - 30, 80)]
    sisi_k = [(W - 30 + (y - atas[-1][1]) * 0.2 + 6 * math.sin(y / 38), y) for y in np.linspace(atas[-1][1], H + 20, 30)]
    sisi_l = [(30 - (y - atas[0][1]) * 0.2 - 6 * math.sin(y / 41), y) for y in np.linspace(H + 20, atas[0][1], 30)]
    ImageDraw.Draw(tepi).polygon([(x * S, y * S) for x, y in atas + sisi_k + sisi_l], fill=255)
    tepi = tepi.resize((W, H), Image.LANCZOS)
    aa = np.zeros((H, W, 4), np.float32)
    aa[..., :3] = np.array(sungai, np.float32) * (0.94 + 0.12 * np.linspace(0, 1, H) ** 0.6)[:, None, None]
    aa[..., 3] = np.asarray(tepi)
    img.alpha_composite(Image.fromarray(aa.astype(np.uint8)))
    lay = lapis(S=S)
    ld = ImageDraw.Draw(lay)
    halus = lapis(S=S)
    hd = ImageDraw.Draw(halus)
    for k in range(n):
        a = bezier3((xs[k], ys[k]), (xs[k] + rng.uniform(-60, 60), ys[k] + (ym - ys[k]) * 0.45), (slot[k], ym - 190), (slot[k], ym), 160)
        t = np.linspace(0, 1, len(a))
        amp, fr, ph = rng.uniform(10, 24), rng.uniform(1.4, 2.4), rng.uniform(0, 6.3)
        a = a + normal(a) * (amp * np.sin(2 * np.pi * fr * t + ph) * np.sin(np.pi * t) ** 1.2)[:, None]
        b = bezier3((slot[k], ym), (slot[k], ym + 100), (riv[k], yr - 100), (riv[k], yr + 160), 80)[1:]
        pts = np.vstack([a, b])
        w0 = rng.uniform(11, 17)
        lw = np.concatenate([w0 + (w_slot - w0) * t ** 0.8, w_slot + (w_riv - w_slot) * np.linspace(0, 1, len(b)) ** 1.3])
        if k in (0, n - 1):  # anak sungai kecil di sisi luar
            j = int(rng.uniform(0.25, 0.45) * (len(a) - 1))
            px_, py_ = a[j]
            arah = -1 if k == 0 else 1
            cab = bezier3((px_ + arah * rng.uniform(50, 80), py_ - rng.uniform(50, 80)), (px_ + arah * 34, py_ - 24), (px_ + arah * 10, py_ - 6), (px_, py_), 30)
            ld.polygon([(x * S, y * S) for x, y in pita_poly(cab, np.linspace(2.5, 6, len(cab)))], fill=warna[k] + (255,))
        ld.polygon([(x * S, y * S) for x, y in pita_poly(pts, lw)], fill=warna[k] + (255,), outline=krem + (255,), width=2 * S)
        terang = campur(warna[k], (255, 255, 255), 0.45) + (170,)
        for off in (-0.22, 0.2):
            garis = pts + normal(pts) * (lw * off)[:, None]
            hd.line([(x * S, y * S) for x, y in garis[6:]], fill=terang, width=S)
        ld.ellipse(((xs[k] - 8) * S, (ys[k] - 8) * S, (xs[k] + 8) * S, (ys[k] + 8) * S), fill=warna[k] + (255,), outline=krem + (255,), width=3 * S)
    pita_l = kecilkan(lay, S)
    pita_l.alpha_composite(kecilkan(halus, S))
    pa = np.asarray(pita_l).astype(np.float32)
    yy = np.arange(H, dtype=np.float32)
    u = np.clip((yy - (yr - 30)) / 170, 0, 1)
    pa[..., 3] *= (1 - u * u * (3 - 2 * u))[:, None]
    img.alpha_composite(Image.fromarray(pa.astype(np.uint8)))
    # riak kecil di permukaan muara
    lay = lapis(S=S)
    ld = ImageDraw.Draw(lay)
    for k in range(26):
        x0 = rng.uniform(60, W - 60)
        y0 = rng.uniform(yr + 30, H - 20)
        ln = rng.uniform(18, 46)
        if abs(x0 - W / 2) < 480 + ln and yr + 60 < y0 < H - 30:
            continue  # jangan di dekat teks
        ld.line(((x0 - ln) * S, y0 * S, (x0 + ln) * S, y0 * S), fill=(214, 226, 246, 60), width=2 * S)
    img.alpha_composite(kecilkan(lay, S))
    d = ImageDraw.Draw(img)
    # label sumber (Gill Sans renggang)
    for k, nama in enumerate(src):
        teks = nama.upper()
        f, jr = renggang_muat(d, teks, lambda q: gill(q, 4), 230, 22, 0.14)
        lb = lebar_renggang(d, teks, f, jr)
        lx = min(max(xs[k], 70 + lb / 2), W - 70 - lb / 2)
        renggang(d, (lx, ys[k] - 20), teks, f, campur(warna[k], (40, 30, 30), 0.35), jr, "ms")
    mu = bersih(p["muara"]).upper()
    f, jr = renggang_muat(d, mu, lambda q: gill(q, 1), 600, 44, 0.3)
    renggang(d, (W / 2, yr + 112), mu, f, krem, jr, "ms")
    d.line((W / 2 - 160, yr + 134, W / 2 - 40, yr + 134), fill=campur(sungai, krem, 0.5), width=2)
    d.line((W / 2 + 40, yr + 134, W / 2 + 160, yr + 134), fill=campur(sungai, krem, 0.5), width=2)
    d.ellipse((W / 2 - 5, yr + 129, W / 2 + 5, yr + 139), fill=(240, 200, 120))
    blok_ayat(img, p, (110, yr + 160, W - 110, H - 66), lambda s: iowan(s, 2), (255, 255, 255), (246, 214, 150), start=34, stop=22,
              lh=1.36, ref_font=gill(26, 4))
    kredit(img, (W / 2, H - 44), (190, 196, 214))
    return img


# ---------- TALI: tali tiga untai ----------

TALI_WARNA = [(190, 90, 50), (240, 226, 196), (52, 66, 120)]


def tali_image(p, i):
    rng = np.random.default_rng(18400 + i)
    bg, ink = (236, 226, 206), (60, 48, 36)
    img = kertas(W, H, bg, 18400 + i, kuat=0.04, butir=0.05).convert("RGBA")
    kanan = i % 2 == 1
    S = 2
    cx0 = W - 280 if kanan else 280
    y_ikat = 372
    A, sw = 30.0, 44.0
    tips = [(cx0 - 172 + rng.uniform(-10, 10), 250 + rng.uniform(-5, 5)), (cx0 + rng.uniform(-8, 8), 178 + rng.uniform(-4, 4)),
            (cx0 + 172 + rng.uniform(-10, 10), 254 + rng.uniform(-5, 5))]
    ys = np.arange(0, H * S) / S
    lam = 300 - 140 * np.clip((ys - y_ikat) / (H - y_ikat), 0, 1) ** 0.8
    Phi = np.cumsum(2 * np.pi / lam / S) + rng.uniform(0, 6.3)
    cxr = cx0 + 16 * np.sin(ys / 380 + i)
    xa, xb = int((cx0 - 260) * S), int((cx0 + 260) * S)
    X = np.arange(xa, xb, dtype=np.float32)[None, :] / S
    terbaik = np.full((len(ys), xb - xa), -9.0, np.float32)
    idx = np.full((len(ys), xb - xa), -1, np.int8)
    U = np.zeros((len(ys), xb - xa), np.float32)
    for k in range(3):
        ph = Phi + 2 * np.pi * k / 3
        x = cxr + A * np.sin(ph)
        z = np.cos(ph)
        tx, ty = tips[k]
        x_in = np.interp(y_ikat, ys, x)
        s_ = np.clip((ys - ty) / (y_ikat - ty), 0, 1)
        lepas = ys < y_ikat
        sm = s_ * s_ * (3 - 2 * s_)
        x = np.where(lepas, tx + (x_in - tx) * sm, x)
        z = np.where(lepas, -0.2 + 0.3 * k, z)
        lebar = np.where(lepas, sw * (0.82 + 0.18 * s_), sw)
        miring = np.gradient(x) * S
        hw = lebar / 2 * np.sqrt(1 + miring ** 2)
        ada = ys >= ty
        u = (X - x[:, None]) / hw[:, None]
        zz = z[:, None] + 0.25 * np.sqrt(np.clip(1 - u * u, 0, 1))
        upd = (np.abs(u) < 1) & ada[:, None] & (zz > terbaik)
        terbaik = np.where(upd, zz, terbaik)
        idx = np.where(upd, k, idx)
        U = np.where(upd, u, U)
    isi = idx >= 0
    col = np.zeros(idx.shape + (3,), np.float32)
    for k in range(3):
        col[idx == k] = TALI_WARNA[k]
    Y = np.arange(len(ys), dtype=np.float32)[:, None]
    alur = 0.8 + 0.2 * (0.5 + 0.5 * np.sin(2 * np.pi * (Y + U * 30 * S) / (10 * S))) ** 0.7
    bentuk = 0.5 + 0.5 * np.sqrt(np.clip(1 - U * U, 0, 1))
    dalam = 0.72 + 0.28 * np.clip((terbaik + 1) / 2, 0, 1)
    sh = bentuk * alur * dalam
    sh = np.where(np.abs(U) > 0.86, sh * 0.72, sh)
    # bayang kontak: piksel di belakang untai lain yang lebih depan
    zpad = np.where(isi, terbaik, -9)
    tetangga = np.maximum.reduce([np.roll(zpad, 5 * S, 1), np.roll(zpad, -5 * S, 1), np.roll(zpad, 4 * S, 0), np.roll(zpad, -4 * S, 0)])
    sh = np.where(isi & (tetangga > terbaik + 0.35), sh * 0.7, sh)
    rgb = col * sh[..., None] + 70 * np.exp(-((U + 0.38) / 0.16) ** 2)[..., None] * isi[..., None]
    rgba = np.dstack([np.clip(rgb, 0, 255), isi * 255.0]).astype(np.uint8)
    tali = Image.fromarray(rgba, "RGBA").filter(ImageFilter.GaussianBlur(0.6))
    tali = tali.resize((tali.width // S, tali.height // S), Image.LANCZOS)
    bayangan(img, tali, (xa // S, 0), blur=12, geser=(10, 12), kuat=0.3)
    # serat di ujung untai yang lepas + ikatan benang
    lay = lapis(S=S)
    ld = ImageDraw.Draw(lay)
    for k, (tx, ty) in enumerate(tips):
        base = TALI_WARNA[k]
        for _ in range(42):
            ox = rng.uniform(-sw * 0.42, sw * 0.42)
            sx, sy = tx + ox, ty + rng.uniform(2, 16)
            ang = -math.pi / 2 + ox / sw * 1.6 + rng.normal(0, 0.28)
            ln = rng.uniform(16, 52)
            bend = rng.normal(0, 10)
            pts = bezier3((sx, sy), (sx + math.cos(ang) * ln * 0.4, sy + math.sin(ang) * ln * 0.4),
                          (sx + math.cos(ang) * ln * 0.75 + bend, sy + math.sin(ang) * ln * 0.75), (sx + math.cos(ang) * ln + bend * 1.4, sy + math.sin(ang) * ln), 12)
            c = campur(base, (255, 255, 255) if rng.random() < 0.5 else (0, 0, 0), rng.uniform(0.05, 0.25))
            ld.line([(x * S, y * S) for x, y in pts], fill=c + (230,), width=int(rng.choice([2, 3])))
    xr = np.interp(y_ikat, ys, cxr)
    for j in range(10):
        y = y_ikat - 22 + j * 4.6
        c = (128, 96, 60) if j % 2 else (150, 116, 76)
        pts = [(x, y + 3.5 * (1 - ((x - xr) / (A + sw / 2 + 6)) ** 2)) for x in np.linspace(xr - A - sw / 2 - 6, xr + A + sw / 2 + 6, 20)]
        ld.line([(x * S, yy * S) for x, yy in pts], fill=c + (255,), width=int(5 * S))
        ld.line([(x * S, (yy - 1.2) * S) for x, yy in pts], fill=(196, 160, 116, 200), width=S)
    img.alpha_composite(kecilkan(lay, S))
    d = ImageDraw.Draw(img)
    labels = [bersih(t) for t in p["untai"]]
    f = iowan(40, 2)
    while max(d.textlength(t, font=f) for t in labels) > 220 and f.size > 26:
        f = iowan(f.size - 2, 2)
    for k, ((tx, ty), lab) in enumerate(zip(tips, labels)):
        lw_ = d.textlength(lab, font=f)
        geser = (-lw_ / 2 + 22, 0, lw_ / 2 - 22)[k]  # label kiri condong ke kiri, kanan ke kanan
        lx = min(max(tx + geser, 70 + lw_ / 2), W - 70 - lw_ / 2)
        d.text((lx, ty - 66), lab, font=f, fill=ink, anchor="ms")
        d.ellipse((tx - 5, ty - 52, tx + 5, ty - 42), fill=TALI_WARNA[k], outline=ink, width=1)
    # kolom teks
    kx0, kx1 = (70, 520) if kanan else (540, 1010)
    kc = (kx0 + kx1) / 2
    judul = bersih(p["judul"])
    fj, jl, js = pas_aman(d, judul, lambda s: snell(s, 1), kx1 - kx0, 230, 120, 56, 1.0)
    fv, vl, vs = pas_aman(d, bersih(p["ayat"]), lambda s: iowan(s), kx1 - kx0, 700, 38, 24, 1.42)
    tinggi = len(jl) * js + 30 + 56 + len(vl) * vs * 1.42 + 50
    y = max(110, 660 - tinggi / 2)
    for ln in jl:
        d.text((kc, y + js * 0.78), ln, font=fj, fill=(150, 70, 40), anchor="ms")
        y += js * 1.0
    y += 30
    d.line((kc - 120, y, kc - 14, y), fill=ink, width=2)
    d.line((kc + 14, y, kc + 120, y), fill=ink, width=2)
    d.polygon([(kc, y - 7), (kc + 7, y), (kc, y + 7), (kc - 7, y)], fill=(150, 70, 40))
    y += 56
    for ln in vl:
        d.text((kc, y), ln, font=fv, fill=ink, anchor="ma")
        y += vs * 1.42
    d.text((kc, y + 10), bersih(p["ref"]).upper(), font=gill(24, 4), fill=(150, 70, 40), anchor="ma")
    kredit(img, (kc, H - 52), (130, 112, 92))
    return img


# ---------- PERCA: selimut perca ----------

PERCA_WARNA = [(200, 96, 70), (226, 178, 70), (146, 170, 130), (52, 70, 120), (240, 230, 210), (226, 150, 150)]


def kain(warna, pola, rng, size=180, aksen=None):
    """Sepotong kain bercorak kecil: polos, titik, garis, bunga, kotak (gingham), atau silang."""
    img = Image.new("RGB", (size, size), warna)
    d = ImageDraw.Draw(img)
    gelap = sum(warna) < 380
    if aksen is None:
        aksen = campur(warna, (250, 244, 230), 0.65) if gelap else campur(warna, (60, 40, 30), 0.35)
    else:
        aksen = campur(warna, aksen, 0.7)
    if pola == "titik":
        for yy in range(0, size + 20, 18):
            for xx in range(0 if (yy // 18) % 2 else 9, size + 20, 18):
                d.ellipse((xx - 2.6, yy - 2.6, xx + 2.6, yy + 2.6), fill=aksen)
    elif pola == "garis":
        for xx in range(-size, size * 2, 14):
            d.line((xx, 0, xx + size, size), fill=aksen, width=3)
    elif pola == "bunga":
        for yy in range(6, size + 20, 30):
            for xx in range((yy // 30 % 2) * 15 + 6, size + 20, 30):
                for a in range(5):
                    ang = a * 2 * math.pi / 5
                    px, py = xx + 4.2 * math.cos(ang), yy + 4.2 * math.sin(ang)
                    d.ellipse((px - 2.6, py - 2.6, px + 2.6, py + 2.6), fill=aksen)
                d.ellipse((xx - 1.6, yy - 1.6, xx + 1.6, yy + 1.6), fill=(236, 190, 80) if not gelap else (250, 220, 120))
    elif pola == "kotak":
        lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for v in range(0, size, 24):
            ld.rectangle((v, 0, v + 11, size), fill=aksen + (90,))
            ld.rectangle((0, v, size, v + 11), fill=aksen + (90,))
        img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
    elif pola == "silang":
        for yy in range(0, size + 16, 16):
            for xx in range((yy // 16 % 2) * 8, size + 16, 16):
                d.line((xx - 3, yy - 3, xx + 3, yy + 3), fill=aksen, width=2)
                d.line((xx - 3, yy + 3, xx + 3, yy - 3), fill=aksen, width=2)
    a = np.asarray(img).astype(np.float32)
    a *= (0.95 + 0.06 * rng.random((size, size)))[..., None]
    a[::3] *= 0.985
    a[:, ::3] *= 0.985
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def blok_perca(jenis, kk, rng, s=180):
    """Satu blok selimut dari beberapa kain (kk: daftar Image s x s)."""
    blk = kk[0].copy()
    m = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(m)
    if jenis == "segitiga":
        md.polygon([(0, 0), (s, 0), (0, s)] if rng.random() < 0.5 else [(0, 0), (s, 0), (s, s)], fill=255)
        blk.paste(kk[1], (0, 0), m)
    elif jenis == "angsa":
        for r in range(2):
            y0 = r * s / 2
            md.polygon([(0, y0 + s / 2), (s / 2, y0), (s, y0 + s / 2)], fill=255)
        blk.paste(kk[1], (0, 0), m)
    elif jenis == "sembilan":
        for r in range(3):
            for c in range(3):
                if (r + c) % 2 == 0:
                    md.rectangle((c * s / 3, r * s / 3, (c + 1) * s / 3 - 1, (r + 1) * s / 3 - 1), fill=255)
        blk.paste(kk[1], (0, 0), m)
    elif jenis == "kabin":
        st = s / 7.5
        for n in range(4, 0, -1):
            a0 = s / 2 - st * (n - 0.5) - st / 2
            md2 = Image.new("L", (s, s), 0)
            ImageDraw.Draw(md2).rectangle((a0, a0, s - a0, s - a0), fill=255)
            blk.paste(kk[(n % 2) + 1] if n % 2 else kk[0], (0, 0), md2)
        c0 = s / 2 - st * 0.75
        md2 = Image.new("L", (s, s), 0)
        ImageDraw.Draw(md2).rectangle((c0, c0, s - c0, s - c0), fill=255)
        blk.paste(kk[2], (0, 0), md2)
    elif jenis == "kincir":
        h = s / 2
        for (x0, y0), tri in zip(((0, 0), (h, 0), (h, h), (0, h)),
                                 ([(0, 0), (h, 0), (h, h)], [(h, 0), (h, h), (0, h)], [(h, h), (0, h), (0, 0)], [(0, h), (0, 0), (h, 0)])):
            md.polygon([(x0 + x, y0 + y) for x, y in tri], fill=255)
        blk.paste(kk[1], (0, 0), m)
    return blk


def jahitan(d, pts, col, pjg=10, sela=7, w=3, bayang=True):
    """Jahitan jelujur sepanjang garis pts."""
    pts = np.asarray(pts, np.float64)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = 0.0
    while s < cum[-1] - 1:
        e = min(s + pjg, cum[-1])
        a = np.array([np.interp(s, cum, pts[:, 0]), np.interp(s, cum, pts[:, 1])])
        b = np.array([np.interp(e, cum, pts[:, 0]), np.interp(e, cum, pts[:, 1])])
        if bayang:
            d.line((a[0] + 1, a[1] + 2, b[0] + 1, b[1] + 2), fill=(0, 0, 0, 60), width=w)
        d.line((a[0], a[1], b[0], b[1]), fill=col, width=w)
        s += pjg + sela


def gerigi(x0, y0, x1, y1, gigi=14):
    """Poligon persegi bertepi gerigi (gunting zigzag)."""
    pts = []
    for x in np.arange(x0, x1, gigi):
        pts += [(x, y0), (x + gigi / 2, y0 + gigi * 0.45)]
    for y in np.arange(y0, y1, gigi):
        pts += [(x1, y), (x1 - gigi * 0.45, y + gigi / 2)]
    for x in np.arange(x1, x0, -gigi):
        pts += [(x, y1), (x - gigi / 2, y1 - gigi * 0.45)]
    for y in np.arange(y1, y0, -gigi):
        pts += [(x0, y), (x0 + gigi * 0.45, y - gigi / 2)]
    return pts


def hati_poly(cx, cy, s, n=120):
    t = np.linspace(0, 2 * np.pi, n)
    return [(cx + s * 16 * math.sin(a) ** 3 / 17, cy - s * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 17) for a in t]


def perca_image(p, i):
    rng = np.random.default_rng(18500 + i)
    s = 180
    pola = ["polos", "titik", "garis", "bunga", "kotak", "silang"]
    kain_lib = []
    for k in range(18):
        w_ = PERCA_WARNA[k % 6]
        ak = None if sum(w_) < 560 else PERCA_WARNA[int(rng.choice([0, 3, 5, 2]))]
        kain_lib.append(kain(w_, pola[(k * 5 + i) % 6], rng, s, ak))
    quilt = Image.new("RGB", (W, H))
    oy = -45
    jenis = ["segitiga", "angsa", "sembilan", "kabin", "kincir", "segitiga", "polos"]
    for r in range(8):
        for c in range(6):
            kk = [kain_lib[int(q)] for q in rng.choice(18, 3, replace=False)]
            j = jenis[int(rng.integers(len(jenis)))]
            blk = kk[0] if j == "polos" else blok_perca(j, kk, rng, s)
            quilt.paste(blk, (c * s, oy + r * s))
    a = np.asarray(quilt).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = np.minimum(xx % s, s - xx % s)
    dy = np.minimum((yy - oy) % s, s - (yy - oy) % s)
    puff = 0.84 + 0.16 * np.clip(np.minimum(dx, dy) / 26, 0, 1) ** 0.6
    puff *= 0.95 + 0.05 * render.fbm2d(H, W, rng, ((6, 1.0), (24, 0.5)))
    a *= puff[..., None]
    img = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.06).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    benang = (244, 236, 216, 230)
    for c in range(7):
        for off in (-9, 9):
            x = c * s + off
            if 0 < x < W:
                jahitan(ld, [(x, -10), (x, H + 10)], benang, w=2)
    for r in range(9):
        for off in (-9, 9):
            y = oy + r * s + off
            if 0 < y < H:
                jahitan(ld, [(-10, y), (W + 10, y)], benang, w=2)
    img.alpha_composite(lay)
    # label perca berisi ayat
    lx0, ly0, lx1, ly1 = 150, 372, 930, 978
    label = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(gerigi(lx0, ly0, lx1, ly1), fill=255)
    linen = np.zeros((H, W, 3), np.float32) + np.array([247, 240, 224], np.float32)
    linen *= (0.97 + 0.04 * rng.random((H, W)))[..., None]
    linen[::3] *= 0.985
    label.paste(Image.fromarray(np.clip(linen, 0, 255).astype(np.uint8)), (0, 0), m)
    bayangan(img, label, (0, 0), blur=10, geser=(3, 8), kuat=0.42)
    d = ImageDraw.Draw(img)
    indigo, karat = (52, 70, 120), (176, 78, 56)
    d.rectangle((lx0 + 26, ly0 + 26, lx1 - 26, ly0 + 96), fill=indigo)
    judul = bersih(p["judul"])
    uk = 36
    while kecil_kapital(ImageDraw.Draw(Image.new("RGB", (8, 8))), (0, 0), judul, lambda q: avn(q, 2), uk, (0, 0, 0), 3) > lx1 - lx0 - 110 and uk > 18:
        uk -= 2
    kecil_kapital(d, ((lx0 + lx1) / 2, ly0 + 61 + uk * 0.36), judul, lambda q: avn(q, 2), uk, (246, 238, 220), 3, "ms")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    jahitan(ld, [(lx0 + 18, ly0 + 18), (lx1 - 18, ly0 + 18), (lx1 - 18, ly1 - 18), (lx0 + 18, ly1 - 18), (lx0 + 18, ly0 + 18)], karat + (255,), 12, 8, 3, False)
    img.alpha_composite(lay)
    # ayat 'dijahit' (huruf tangan + tekstur benang satin)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    ref_f = avn(28, 2)
    f, vl, vs = pas_aman(probe, bersih(p["ayat"]), bradley, lx1 - lx0 - 120, ly1 - ly0 - 96 - 130, 44, 26, 1.3)
    tinggi = len(vl) * vs * 1.3
    y = ly0 + 96 + (ly1 - ly0 - 96 - 70 - tinggi) / 2
    mk = Image.new("L", (W, H), 0)
    mkd = ImageDraw.Draw(mk)
    for ln in vl:
        mkd.text((W / 2, y), ln, font=f, fill=255, anchor="ma")
        y += vs * 1.3
    satin = 0.78 + 0.22 * (0.5 + 0.5 * np.sin((xx + yy) * 2 * np.pi / 4.5))
    am = np.asarray(mk).astype(np.float32) / 255
    base = np.asarray(img.convert("RGB")).astype(np.float32)
    bay = np.asarray(mk.filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
    bay = np.roll(np.roll(bay, 2, 0), 1, 1) * 0.35
    base *= (1 - bay)[..., None]
    out = base * (1 - am[..., None]) + (np.array(indigo, np.float32) * satin[..., None]) * am[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    kecil_kapital(d, (W / 2, y + 30), "— " + bersih(p["ref"]), lambda q: avn(q, 2), 30, karat, 2, "ms")
    # tambalan hati
    hx, hy, hs = lx1 - 40, ly0 + 10, 66
    hm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hm).polygon(hati_poly(hx, hy, hs), fill=255)
    hk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hk.paste(kain((226, 120, 130), "titik", rng, 200), (int(hx - 100), int(hy - 100)))
    hk.putalpha(hm)
    bayangan(img, hk, (0, 0), blur=6, geser=(2, 5), kuat=0.4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    hp = hati_poly(hx, hy, hs - 7, 70)
    jahitan(ld, hp, (250, 244, 230, 255), 6, 6, 2, False)
    img.alpha_composite(lay)
    # label nama kecil di bawah
    tw = 420
    tag = Image.new("RGBA", (tw, 54), (246, 238, 220, 255))
    tdd = ImageDraw.Draw(tag)
    tdd.text((tw / 2, 28), "dijahit untuk kamu · @" + HANDLE, font=avn(20, 2), fill=indigo, anchor="mm")
    jahitan(tdd, [(10, 6), (tw - 10, 6)], karat + (255,), 6, 5, 2, False)
    jahitan(tdd, [(10, 48), (tw - 10, 48)], karat + (255,), 6, 5, 2, False)
    bayangan(img, tag, ((W - tw) // 2, 1236), blur=6, geser=(2, 5), kuat=0.4)
    return img


# ---------- TANGGA: papan tangga & perosotan ----------

def tag_pil(d, cx, cy, teks, f, col, naik):
    """Label pil putih berbingkai warna + segitiga arah kecil. -> kotak."""
    tw = d.textlength(teks, font=f)
    w_, h_ = tw + 56, f.size + 22
    x0, y0 = cx - w_ / 2, cy - h_ / 2
    d.rounded_rectangle((x0 + 2, y0 + 4, x0 + w_ + 2, y0 + h_ + 4), radius=h_ / 2, fill=(0, 0, 0, 50))
    d.rounded_rectangle((x0, y0, x0 + w_, y0 + h_), radius=h_ / 2, fill=(255, 255, 255, 255), outline=col + (255,), width=3)
    tx, ty = x0 + 22, cy
    if naik:
        d.polygon([(tx - 8, ty + 6), (tx + 8, ty + 6), (tx, ty - 8)], fill=col + (255,))
    else:
        d.polygon([(tx - 8, ty - 6), (tx + 8, ty - 6), (tx, ty + 8)], fill=col + (255,))
    d.text((x0 + 36 + tw / 2, cy + 1), teks, font=f, fill=(50, 44, 40, 255), anchor="mm")
    return (x0, y0, x0 + w_, y0 + h_)


def tumpang(a, b, pad=6):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def dadu(nilai, s=96):
    def gambar(d, k):
        d.rounded_rectangle((4 * k, 4 * k, (s - 4) * k, (s - 4) * k), radius=18 * k, fill=(250, 250, 248, 255), outline=(60, 56, 52, 255), width=int(3 * k))
        d.rounded_rectangle((10 * k, 10 * k, (s - 10) * k, (s - 14) * k), radius=14 * k, fill=(255, 255, 255, 255))
        pos = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
               5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[nilai]
        for px, py in pos:
            cx, cy, r = s / 2 + px * s * 0.24, s / 2 + py * s * 0.24, s * 0.085
            d.ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k), fill=(28, 26, 26, 255))
    from gaya_w7 import sprite
    return sprite(s, s, gambar)


def tangga_image(p, i):
    rng = np.random.default_rng(18600 + i)
    meja = [(246, 234, 210), (230, 236, 228), (242, 228, 222)][i % 3]
    bingkai = [(196, 84, 60), (60, 110, 120), (120, 86, 150)][i % 3]
    kayu_t, seluncur, seluncur_g, merah = (166, 110, 60), (90, 170, 150), (52, 122, 106), (230, 70, 50)
    img = kertas(W, H, meja, 18600 + i, kuat=0.03, butir=0.04).convert("RGBA")
    d = ImageDraw.Draw(img)
    sq = 82
    bx0, by0 = (W - 10 * sq) / 2, 196
    bx1, by1 = bx0 + 10 * sq, by0 + 10 * sq
    papan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(papan)
    pd.rounded_rectangle((bx0 - 20, by0 - 20, bx1 + 20, by1 + 20), radius=26, fill=bingkai + (255,))
    pd.rounded_rectangle((bx0 - 7, by0 - 7, bx1 + 7, by1 + 7), radius=10, fill=campur(bingkai, (0, 0, 0), 0.25) + (255,))
    tint = [(246, 236, 214), (252, 226, 208), (232, 238, 214), (250, 232, 190), (226, 234, 236)]

    def pusat(n):
        r, c = divmod(int(n) - 1, 10)
        if r % 2:
            c = 9 - c
        return np.array([bx0 + (c + 0.5) * sq, by1 - (r + 0.5) * sq])
    for n in range(1, 101):
        cx, cy = pusat(n)
        r, c = divmod(n - 1, 10)
        col = tint[0] if (r + c) % 2 == 0 else tint[1 + (n * 7 + i) % 4]
        pd.rectangle((cx - sq / 2, cy - sq / 2, cx + sq / 2 - 1, cy + sq / 2 - 1), fill=col + (255,))
        pd.text((cx - sq / 2 + 7, cy - sq / 2 + 5), str(n), font=futura(19), fill=(150, 116, 86, 255))
    cx, cy = pusat(1)
    pd.text((cx, cy + 18), "MULAI", font=futura(15), fill=bingkai + (255,), anchor="mm")
    cx, cy = pusat(100)
    from gaya_w14 import bintang_poly
    pd.polygon(bintang_poly(cx + 6, cy + 8, 22), fill=(240, 180, 50, 255))
    bayangan(img, papan, (0, 0), blur=18, geser=(0, 12), kuat=0.3)
    S = 2
    lay, bay = lapis(S=S), lapis(S=S)
    ld, bd = ImageDraw.Draw(lay), ImageDraw.Draw(bay)
    jalur = []
    # perosotan (pengganti ular): pita bergaris melengkung
    for k, (dari, ke, lab) in enumerate(p["turun"]):
        p0, p1 = pusat(dari), pusat(ke)
        v = p1 - p0
        L = np.hypot(*v)
        nrm = np.array([-v[1], v[0]]) / L
        off = 0.2 * L * (1 if k % 2 == 0 else -1)
        pts = bezier3(p0, p0 + v * 0.33 + nrm * off, p0 + v * 0.66 - nrm * off, p1, 90)
        poly = pita_poly(pts, 40)
        bd.polygon([((x + 6) * S, (y + 9) * S) for x, y in poly], fill=(0, 0, 0, 70))
        ld.polygon([(x * S, y * S) for x, y in poly], fill=seluncur + (255,))
        cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
        nn = normal(pts)
        for s_ in np.arange(16, cum[-1] - 14, 30):  # garis-garis lebar seperti perosotan taman bermain
            j = int(np.searchsorted(cum, s_))
            j2 = min(len(pts) - 1, int(np.searchsorted(cum, s_ + 12)))
            a_, a2 = pts[j] + nn[j] * 17, pts[j2] + nn[j2] * 17
            b_, b2 = pts[j2] - nn[j2] * 17, pts[min(len(pts) - 1, j2 + (j2 - j))] - nn[min(len(pts) - 1, j2 + (j2 - j))] * 17
            ld.polygon([(a_[0] * S, a_[1] * S), (a2[0] * S, a2[1] * S), (b2[0] * S, b2[1] * S), (b_[0] * S, b_[1] * S)], fill=(132, 198, 182, 255))
        kilap = pts + nn * 7
        ld.line([(x * S, y * S) for x, y in kilap[4:-4]], fill=(236, 250, 244, 150), width=3 * S, joint="curve")
        for sisi in (1, -1):
            tepi = pts + nn * 20 * sisi
            ld.line([(x * S, y * S) for x, y in tepi], fill=seluncur_g + (255,), width=7 * S, joint="curve")
        for (x, y), rr in ((p0, 15), (p1, 17)):
            ld.ellipse(((x - rr) * S, (y - rr) * S, (x + rr) * S, (y + rr) * S), fill=seluncur_g + (255,))
            ld.ellipse(((x - rr + 5) * S, (y - rr + 5) * S, (x + rr - 5) * S, (y + rr - 5) * S), fill=seluncur + (255,))
        jalur.append((pts, bersih(lab), seluncur_g, False))
    # tangga
    for dari, ke, lab in p["tangga"]:
        p0, p1 = pusat(dari), pusat(ke)
        v = p1 - p0
        L = np.hypot(*v)
        u = v / L
        nrm = np.array([-u[1], u[0]])
        a_, b_ = p0 - u * 16, p1 + u * 16
        for sisi in (1, -1):
            r0, r1 = a_ + nrm * 18 * sisi, b_ + nrm * 18 * sisi
            bd.line(((r0[0] + 6) * S, (r0[1] + 9) * S, (r1[0] + 6) * S, (r1[1] + 9) * S), fill=(0, 0, 0, 70), width=10 * S)
        for t_ in np.arange(20, L + 32 - 14, 30):
            c0, c1 = a_ + u * t_ + nrm * 18, a_ + u * t_ - nrm * 18
            bd.line(((c0[0] + 6) * S, (c0[1] + 9) * S, (c1[0] + 6) * S, (c1[1] + 9) * S), fill=(0, 0, 0, 60), width=7 * S)
            ld.line((c0[0] * S, c0[1] * S, c1[0] * S, c1[1] * S), fill=(110, 70, 36, 255), width=9 * S)
            ld.line((c0[0] * S, c0[1] * S, c1[0] * S, c1[1] * S), fill=kayu_t + (255,), width=5 * S)
        for sisi in (1, -1):
            r0, r1 = a_ + nrm * 18 * sisi, b_ + nrm * 18 * sisi
            ld.line((r0[0] * S, r0[1] * S, r1[0] * S, r1[1] * S), fill=(110, 70, 36, 255), width=12 * S)
            ld.line((r0[0] * S, r0[1] * S, r1[0] * S, r1[1] * S), fill=kayu_t + (255,), width=8 * S)
            ld.line(((r0[0] - nrm[0] * 1.5) * S, (r0[1] - nrm[1] * 1.5) * S, (r1[0] - nrm[0] * 1.5) * S, (r1[1] - nrm[1] * 1.5) * S),
                    fill=(206, 156, 100, 255), width=2 * S)
        jalur.append((bezier3(p0, p0 + v / 3, p0 + 2 * v / 3, p1, 60), bersih(lab), (150, 96, 50), True))
    img.alpha_composite(kecilkan(bay.filter(ImageFilter.GaussianBlur(4 * S)), S))
    img.alpha_composite(kecilkan(lay, S))
    # bidak
    bx, by = pusat(p["bidak"]) + np.array([14, 10])
    pion = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    qd = ImageDraw.Draw(pion)
    qd.ellipse((bx - 28, by + 14, bx + 34, by + 32), fill=(0, 0, 0, 70))
    qd.ellipse((bx - 24, by + 6, bx + 24, by + 26), fill=campur(merah, (0, 0, 0), 0.3) + (255,))
    qd.polygon([(bx - 18, by + 16), (bx + 18, by + 16), (bx + 8, by - 22), (bx - 8, by - 22)], fill=merah + (255,))
    qd.ellipse((bx - 16, by - 52, bx + 16, by - 20), fill=merah + (255,))
    qd.ellipse((bx - 9, by - 46, bx - 1, by - 38), fill=(255, 190, 170, 255))
    qd.line((bx - 10, by - 14, bx - 14, by + 12), fill=(255, 150, 130, 200), width=3)
    img.alpha_composite(pion.filter(ImageFilter.GaussianBlur(0.4)))
    # label jalur (cari tempat yang tidak bertumpuk)
    d = ImageDraw.Draw(img)
    f = rounded(21, "Semibold")
    kotak = [(bx - 30, by - 56, bx + 34, by + 30)]
    for pts, lab, col, naik in jalur:
        best = None
        for t_ in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.2, 0.8):
            j = int(t_ * (len(pts) - 1))
            cx, cy = pts[j]
            tw = d.textlength(lab, font=f) + 56
            cx = min(max(cx, bx0 + tw / 2 + 4), bx1 - tw / 2 - 4)
            box = (cx - tw / 2, cy - 22, cx + tw / 2, cy + 22)
            skor = sum(tumpang(box, b) for b in kotak)
            if best is None or skor < best[0]:
                best = (skor, cx, cy)
            if skor == 0:
                break
        kotak.append(tag_pil(d, best[1], best[2], lab, f, col, naik))
    # judul + dadu
    judul = bersih(p["judul"])
    fj = muat(d, judul, lambda s: rounded(s, "Bold"), bx1 - bx0 - 130, 64, 30)
    d.text((bx0 - 8, 128), judul, font=fj, fill=(52, 44, 40), anchor="ls")
    dd = dadu(int(p["dadu"])).rotate(-9, expand=True, resample=Image.BICUBIC)
    bayangan(img, dd, (bx1 - dd.width + 14, 48), blur=8, geser=(4, 8), kuat=0.35)
    blok_ayat(img, p, (110, by1 + 48, W - 110, H - 70), lambda s: charter(s), (52, 44, 40), merah, start=34, stop=22, lh=1.36,
              ref_font=futura(26))
    kredit(img, (W / 2, H - 46), (150, 130, 112))
    return img


# ---------- FASE: cincin fase bulan ----------

SINODIS = 29.530588853
ACUAN_BULAN_BARU = dt.datetime(2000, 1, 6, 18, 14)  # UTC
DELTA_T = 69.0  # detik, TT - UT sekitar 2027
WIB = dt.timedelta(hours=7)
BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def jde_fase(k):
    """Meeus, Astronomical Algorithms bab 49. k = lunasi sejak bulan baru 6 Jan 2000 (+0,25/0,5/0,75 untuk kuartal & purnama)."""
    T = k / 1236.85
    jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * T ** 2 - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4
    E = 1 - 0.002516 * T - 0.0000074 * T ** 2
    r, s, c = math.radians, math.sin, math.cos
    M = r(2.5534 + 29.10535670 * k - 0.0000014 * T ** 2 - 0.00000011 * T ** 3)
    Mp = r(201.5643 + 385.81693528 * k + 0.0107582 * T ** 2 + 0.00001238 * T ** 3 - 0.000000058 * T ** 4)
    F = r(160.7108 + 390.67050284 * k - 0.0016118 * T ** 2 - 0.00000227 * T ** 3 + 0.000000011 * T ** 4)
    Om = r(124.7746 - 1.56375588 * k + 0.0020672 * T ** 2 + 0.00000215 * T ** 3)
    q = round((k % 1) * 4) % 4
    if q in (0, 2):
        a = (-0.40720, 0.17241, 0.01608, 0.01039, 0.00739, -0.00514, 0.00208) if q == 0 else (-0.40614, 0.17302, 0.01614, 0.01043, 0.00734, -0.00515, 0.00209)
        kor = (a[0] * s(Mp) + a[1] * E * s(M) + a[2] * s(2 * Mp) + a[3] * s(2 * F) + a[4] * E * s(Mp - M) + a[5] * E * s(Mp + M)
               + a[6] * E * E * s(2 * M) - 0.00111 * s(Mp - 2 * F) - 0.00057 * s(Mp + 2 * F) + 0.00056 * E * s(2 * Mp + M)
               - 0.00042 * s(3 * Mp) + 0.00042 * E * s(M + 2 * F) + 0.00038 * E * s(M - 2 * F) - 0.00024 * E * s(2 * Mp - M)
               - 0.00017 * s(Om) - 0.00007 * s(Mp + 2 * M) + 0.00004 * s(2 * Mp - 2 * F) + 0.00004 * s(3 * M)
               + 0.00003 * s(Mp + M - 2 * F) + 0.00003 * s(2 * Mp + 2 * F) - 0.00003 * s(Mp + M + 2 * F)
               + 0.00003 * s(Mp - M + 2 * F) - 0.00002 * s(Mp - M - 2 * F) - 0.00002 * s(3 * Mp + M) + 0.00002 * s(4 * Mp))
    else:
        kor = (-0.62801 * s(Mp) + 0.17172 * E * s(M) - 0.01183 * E * s(Mp + M) + 0.00862 * s(2 * Mp) + 0.00804 * s(2 * F)
               + 0.00454 * E * s(Mp - M) + 0.00204 * E * E * s(2 * M) - 0.00180 * s(Mp - 2 * F) - 0.00070 * s(Mp + 2 * F)
               - 0.00040 * s(3 * Mp) - 0.00034 * E * s(2 * Mp - M) + 0.00032 * E * s(M + 2 * F) + 0.00032 * E * s(M - 2 * F)
               - 0.00028 * E * E * s(Mp + 2 * M) + 0.00027 * E * s(2 * Mp + M) - 0.00017 * s(Om) - 0.00005 * s(Mp - M - 2 * F)
               + 0.00004 * s(2 * Mp + 2 * F) - 0.00004 * s(Mp + M + 2 * F) + 0.00004 * s(Mp - 2 * M) + 0.00003 * s(Mp + M - 2 * F)
               + 0.00003 * s(3 * M) + 0.00002 * s(2 * Mp - 2 * F) + 0.00002 * s(Mp - M + 2 * F) - 0.00002 * s(3 * Mp + M))
        w_ = 0.00306 - 0.00038 * E * c(M) + 0.00026 * c(Mp) - 0.00002 * c(Mp - M) + 0.00002 * c(Mp + M) + 0.00002 * c(2 * F)
        kor += w_ if q == 1 else -w_
    A = [299.77 + 0.107408 * k - 0.009173 * T ** 2, 251.88 + 0.016321 * k, 251.83 + 26.651886 * k, 349.42 + 36.412478 * k,
         84.66 + 18.206239 * k, 141.74 + 53.303771 * k, 207.14 + 2.453732 * k, 154.84 + 7.306860 * k, 34.52 + 27.261239 * k,
         207.19 + 0.121824 * k, 291.34 + 1.844379 * k, 161.72 + 24.198154 * k, 239.56 + 25.513099 * k, 331.55 + 3.592518 * k]
    ka = [0.000325, 0.000165, 0.000164, 0.000126, 0.000110, 0.000062, 0.000060, 0.000056, 0.000047, 0.000042, 0.000040, 0.000037, 0.000035, 0.000023]
    return jde + kor + sum(a_ * s(r(x)) for a_, x in zip(ka, A))


def waktu_fase(k):
    """-> datetime UTC (naif) fase utama ke-k."""
    return dt.datetime(2000, 1, 1, 12) + dt.timedelta(days=jde_fase(k) - 2451545.0, seconds=-DELTA_T)


@lru_cache(maxsize=None)
def fase_utama(tahun, bulan):
    """Fase utama (waktu UTC, 0 baru / 1 kuartal awal / 2 purnama / 3 kuartal akhir) dari ~40 hari sebelum s.d. ~70 hari sesudah awal bulan."""
    awal = dt.datetime(tahun, bulan, 1) - dt.timedelta(days=40)
    k0 = math.floor((awal - ACUAN_BULAN_BARU).total_seconds() / 86400 / SINODIS)
    return tuple(sorted((waktu_fase(k + q / 4), q) for k in range(k0, k0 + 5) for q in range(4)))


def sudut_bulan(t_utc):
    """Sudut fase (radian) 0 = bulan baru, pi = purnama; interpolasi di antara fase utama Meeus."""
    fs = fase_utama(t_utc.year, t_utc.month)
    for (ta, qa), (tb, _) in zip(fs[:-1], fs[1:]):
        if ta <= t_utc < tb:
            return ((qa + (t_utc - ta) / (tb - ta)) % 4) * math.pi / 2
    raise ValueError(t_utc)


def nama_fase(sudut):
    deg = math.degrees(sudut) % 360
    for batas, nama in ((7, "bulan baru"), (83, "sabit awal"), (97, "perbani awal"), (173, "cembung awal"), (187, "purnama"),
                        (263, "cembung akhir"), (277, "perbani akhir"), (353, "sabit akhir"), (361, "bulan baru")):
        if deg < batas:
            return nama


def tanggal_post(p, default):
    """(date, jam, menit) dari konteks (_tanggal '24 Januari 2027', _jam '21.00')."""
    try:
        d_, b_, y_ = p["_tanggal"].split()
        tgl = dt.date(int(y_), BULAN_ID.index(b_) + 1, int(d_))
    except (KeyError, ValueError):
        tgl = default
    jam, menit = [int(v) for v in p.get("_jam", "21.00").split(".")]
    return tgl, jam, menit


@lru_cache(maxsize=None)
def _detail_bulan(n):
    """Tekstur halus permukaan bulan (sama untuk semua cakram berukuran sama: bulan selalu menampakkan wajah yang sama)."""
    return render.fbm2d(n, n, np.random.default_rng(1969), ((5, 1.0), (13, 0.6), (31, 0.35), (70, 0.2)))


def cakram_bulan(r, sudut, S=3, cahaya=True):
    """Sprite bulan berdiameter 2r (+ pendar). Sisi terang di kanan saat membesar."""
    pad = int(r * 0.8) + 4 if cahaya else 3
    n = (2 * r + 2 * pad) * S
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    x = (xx - n / 2 + 0.5) / (r * S)
    y = (yy - n / 2 + 0.5) / (r * S)
    rr = np.hypot(x, y)
    cov = np.clip((1 - rr) * r * S + 0.5, 0, 1)
    t = math.cos(sudut) * np.sqrt(np.clip(1 - y * y, 0, 1))
    xs_ = x if sudut % (2 * math.pi) < math.pi else -x
    lit = np.clip((xs_ - t) / 0.035 + 0.5, 0, 1)
    tex = 0.93 + 0.025 * (np.sin(9 * x + 2 * y) + np.sin(5 * y - 7 * x + 1) + np.sin(17 * x + 13 * y))
    for cx, cy, rad, k in ((-0.22, -0.28, 0.32, 0.17), (0.18, -0.12, 0.26, 0.15), (-0.05, 0.25, 0.22, 0.12), (0.34, 0.3, 0.18, 0.1),
                           (-0.42, 0.18, 0.16, 0.09)):
        tex -= k * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / rad ** 2)
    for cx, cy, rad in ((0.1, 0.62, 0.07), (-0.55, -0.3, 0.06), (0.5, -0.45, 0.05)):
        dd = np.hypot(x - cx, y - cy)
        tex += 0.08 * np.exp(-((dd - rad) / 0.02) ** 2)
    tex *= 0.9 + 0.14 * _detail_bulan(n)
    tex *= 1 - 0.18 * rr ** 4
    terang = np.array([240, 232, 210], np.float32)
    gelap = np.array([36, 40, 64], np.float32) * (0.95 + 0.1 * tex)[..., None]
    rgb = gelap + (terang * tex[..., None] - gelap) * lit[..., None]
    a = cov * 255
    out = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    if cahaya:
        g = Image.fromarray((lit * cov * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r * S * 0.35))
        glow = Image.new("RGBA", img.size, (255, 240, 200, 0))
        glow.putalpha(g.point(lambda v: int(v * 0.42)))
        glow.alpha_composite(img)
        img = glow
    return img.resize((n // S, n // S), Image.LANCZOS), pad


def fase_image(p, i):
    rng = np.random.default_rng(18700 + i)
    krem, emas = (240, 232, 210), (232, 196, 120)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, 832
    rad = np.hypot(xx - cx, yy - cy) / 900
    base = np.array([14, 18, 40], np.float32) + np.array([16, 18, 30], np.float32) * np.clip(1 - rad, 0, 1)[..., None] ** 2
    img = grain(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), 0.05).convert("RGBA")
    d = ImageDraw.Draw(img)
    for _ in range(220):  # bintang, menjauhi teks dan cincin
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.5, 1.6)
        if math.hypot(x - cx, y - cy) < 400 or y < 150 or 350 < y < 400 or y > 1225 or (180 < y < 350 and abs(x - W / 2) < 110):
            continue
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(rng.uniform(30, 120))))
    tgl, jam, menit = tanggal_post(p, MULAI + dt.timedelta(days=i * 2))
    t_post = dt.datetime(tgl.year, tgl.month, tgl.day, jam, menit) - WIB
    sud = sudut_bulan(t_post)
    persen = round(50 * (1 - math.cos(sud)))
    # kepala
    kepala = f"{BULAN_ID[tgl.month - 1].upper()} {tgl.year}  ·  FASE BULAN  ·  WIB"
    f, jr = renggang_muat(d, kepala, lambda s: gill(s, 0), W - 160, 20, 0.2)
    renggang(d, (W / 2, 62), kepala, f, krem + (170,), jr, "ms")
    judul = bersih(p["judul"])
    d.text((W / 2, 128), judul, font=muat(d, judul, lambda s: iowan(s, 2), W - 180, 52, 30), fill=krem, anchor="ms")
    besar, pad = cakram_bulan(76, sud)
    img.alpha_composite(besar, (int(W / 2 - 76 - pad), int(262 - 76 - pad)))
    d = ImageDraw.Draw(img)
    hari = HARI_ID[tgl.weekday()]
    info = f"{hari} {tgl.day} {BULAN_ID[tgl.month - 1]}  ·  {nama_fase(sud)}  ·  {persen}% terang".upper()
    f, jr = renggang_muat(d, info, lambda s: gill(s, 4), W - 160, 21, 0.14)
    renggang(d, (W / 2, 384), info, f, emas, jr, "ms")
    # cincin hari-hari bulan ini
    R, rd = 320, 23
    hari_bulan = (dt.date(tgl.year + tgl.month // 12, tgl.month % 12 + 1, 1) - dt.timedelta(days=1)).day
    fs = fase_utama(tgl.year, tgl.month)
    tanda = {}
    for t_, q in fs:
        tw_ = t_ + WIB
        if (tw_.year, tw_.month) == (tgl.year, tgl.month) and q in (0, 2) and q not in tanda.values():
            tanda[tw_] = q
    tanggal_tanda = {tw_.day: q for tw_, q in tanda.items()}
    for dd_ in range(1, hari_bulan + 1):
        a = -math.pi / 2 + (dd_ - 1) * 2 * math.pi / hari_bulan
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        s_ = sudut_bulan(dt.datetime(tgl.year, tgl.month, dd_, 21, 0) - WIB)
        kecil, pk = cakram_bulan(rd, s_, cahaya=False)
        img.alpha_composite(kecil, (int(px - rd - pk), int(py - rd - pk)))
        d = ImageDraw.Draw(img)
        if dd_ == tgl.day:
            d.ellipse((px - rd - 8, py - rd - 8, px + rd + 8, py + rd + 8), outline=emas, width=3)
        elif dd_ in tanggal_tanda:
            d.ellipse((px - rd - 6, py - rd - 6, px + rd + 6, py + rd + 6), outline=krem + (130,), width=2)
        tx, ty = cx + (R + 44) * math.cos(a), cy + (R + 44) * math.sin(a)
        d.text((tx, ty), str(dd_), font=gill(19, 4 if dd_ == tgl.day else 0), fill=emas if dd_ == tgl.day else krem + (150,), anchor="mm")
    cincin = bersih(p["cincin"]).strip(" ·") + "  ·  "
    fr = gill(20, 0)
    keliling = 2 * math.pi * 276
    satu = sum(fr.getlength(c) for c in cincin)
    ulang = max(1, int(keliling // (satu + len(cincin) * 3)))
    jarak = (keliling - ulang * satu) / (ulang * len(cincin))
    teks_lingkar(img, cx, cy, 276, cincin * ulang, fr, krem + (150,), start_deg=-90, jarak=jarak)
    blok_ayat(img, p, (cx - 222, cy - 170, cx + 222, cy + 170), lambda s: iowan(s, 2), krem, emas, start=34, stop=20, lh=1.34,
              ref_font=gill(24, 4))
    # keterangan bulan baru & purnama (dihitung)
    d = ImageDraw.Draw(img)
    for k, (tw_, q) in enumerate(sorted(tanda.items(), key=lambda kv: kv[1])):
        lab = bersih(p["label_fase"][0 if q == 0 else 1]).upper()
        kx = W / 2 + (-235 if q == 0 else 235)
        ik, pk = cakram_bulan(13, 0.0 if q == 0 else math.pi, cahaya=False)
        f, jr = renggang_muat(d, lab, lambda s: gill(s, 4), 360, 21, 0.12)
        lw_ = lebar_renggang(d, lab, f, jr)
        x0 = kx - (lw_ + 40) / 2
        img.alpha_composite(ik, (int(x0 - pk), int(1252 - 13 - pk)))
        d = ImageDraw.Draw(img)
        if q == 0:
            d.ellipse((x0 - 13, 1252 - 13, x0 + 13, 1252 + 13), outline=krem + (120,), width=1)
        renggang(d, (x0 + 40, 1260), lab, f, krem, jr, "ls")
        teks = f"{tw_.day} {BULAN_ID[tw_.month - 1][:3].upper()} {tw_.year}  {tw_:%H.%M} WIB"
        d.text((kx, 1292), teks, font=gill(18, 0), fill=krem + (150,), anchor="ms")
    kredit(img, (W / 2, H - 22), krem + (120,), anchor="ms", size=20)
    return img


# ---------- KIDUNG: halaman buku nyanyian not angka ----------

def _not(tok):
    """'5' / "1'" / '5,' / '0' / '.' -> (karakter, oktaf)."""
    tok = tok.strip()
    ch = tok[0]
    return ch, tok.count("'") - tok.count(",")


def baca_suara(seq):
    """Token per ketukan -> daftar ketukan (tiap ketukan: daftar (karakter, oktaf)) dan indeks garis birama."""
    if isinstance(seq, str):
        seq = seq.split()
    ketuk, birama = [], []
    for tok in seq:
        tok = str(tok).strip()
        if not tok:
            continue
        if tok in ("|", "||"):
            birama.append(len(ketuk))
            continue
        ketuk.append([_not(x) for x in tok.split("_") if x])
    return ketuk, birama


def kertas_tua(w, h, seed):
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), np.float32) + np.array([240, 232, 212], np.float32)
    base *= (0.93 + 0.09 * render.fbm2d(h, w, rng, ((3, 1.0), (14, 0.5), (60, 0.3))))[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tepi = np.minimum.reduce([xx, yy, w - xx, h - yy])
    base *= (0.86 + 0.14 * np.clip(tepi / 90, 0, 1) ** 0.6)[..., None]
    base *= (0.9 + 0.1 * np.clip(xx / 120, 0, 1) ** 0.5)[..., None]  # bayang lipatan buku di kiri
    for _ in range(26):  # bintik kecokelatan (foxing)
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(2, 9)
        m = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (r * r))
        base -= m[..., None] * np.array([18, 26, 34], np.float32) * rng.uniform(0.4, 1)
    return grain(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), 0.07)


def kidung_image(p, i):
    tinta_c, merah, abu = (40, 32, 26), (170, 40, 36), (120, 110, 100)
    img = kertas_tua(W, H, 18800 + i).convert("RGBA")
    d = ImageDraw.Draw(img)
    # kepala halaman
    d.line((90, 72, W - 90, 72), fill=tinta_c, width=3)
    d.line((90, 79, W - 90, 79), fill=tinta_c, width=1)
    d.text((W - 90, 60), str(140 + i * 3), font=caslon(24), fill=abu, anchor="rs")
    d.text((90, 60), "NYANYIAN JEMAAT", font=caslon(20), fill=abu, anchor="ls")
    d.text((90, 140), "No. " + bersih(str(p["nomor"])), font=caslon(40), fill=merah, anchor="ls")
    judul = bersih(p["judul"]).upper()
    d.text((W / 2, 200), judul, font=muat(d, judul, caslon, W - 200, 52, 28), fill=tinta_c, anchor="ms")
    d.text((W / 2, 250), "untuk empat suara", font=snell(36, 0), fill=abu, anchor="ms")
    nd = bersih(str(p["nada_dasar"]))
    kunci_t = (nd if "=" in nd else "Do = " + nd) + "     " + bersih(str(p["birama"]))
    d.text((90, 312), kunci_t, font=iowan(28, 1), fill=tinta_c, anchor="ls")
    d.text((W - 90, 312), "Syair: " + bersih(p["ref"]), font=iowan(24, 2), fill=merah, anchor="rs")
    # not
    suara = [baca_suara(s) for s in p["not"]]
    nket = max(len(s[0]) for s in suara)
    for s in suara:
        while len(s[0]) < nket:
            s[0].append([(".", 0)])
    suku = p["suku_kata"]
    if isinstance(suku, str):
        suku = [sk + ("-" if j < len(w_.split("-")) - 1 else "") for w_ in suku.split() for j, sk in enumerate(w_.split("-"))]
    suku = [bersih(str(x)) for x in suku]
    try:
        bilangan = int(str(p["birama"]).split("/")[0])
    except ValueError:
        bilangan = 4
    birama = suara[0][1] or list(range(bilangan, nket, bilangan))
    birama = sorted(set(b for b in birama if 0 < b < nket))
    # suku kata untuk tiap not sopran
    sk_not = {}
    n_suku = 0
    for b, ketukan in enumerate(suara[0][0]):
        for j, (ch, _) in enumerate(ketukan):
            if ch in "1234567" and n_suku < len(suku):
                sk_not[(b, j)] = suku[n_suku]
                n_suku += 1
    x_kiri, x_kanan = 150, W - 90
    uk = 40
    while True:
        fd, fs_ = menlo(uk, 1), iowan(int(uk * 0.8))
        lebar = []
        for b in range(nket):
            sub = max(len(s[0][b]) for s in suara)
            perlu = [d.textlength(sk_not.get((b, j), "").rstrip("-"), font=fs_) + uk * 0.5 for j in range(sub)]
            lebar.append(max(uk * 1.5 * sub, sum(perlu), sub * max(perlu)))
        sistem, cur, cw = [], [], 0
        batas = [0] + birama + [nket]
        bar = list(zip(batas[:-1], batas[1:]))
        lb = [sum(lebar[a_:b_]) + uk * 0.9 for a_, b_ in bar]
        for (a_, b_), wb in zip(bar, lb):
            if cur and cw + wb > x_kanan - x_kiri:
                sistem.append(cur)
                cur, cw = [], 0
            cur.append((a_, b_))
            cw += wb
        sistem.append(cur)
        if len(sistem) > 1:  # bagi birama serata mungkin ke jumlah sistem yang sama
            target = sum(lb) / len(sistem)
            rata, cur, cw = [], [], 0
            for k, ((a_, b_), wb) in enumerate(zip(bar, lb)):
                sisa_bar, sisa_sis = len(bar) - k, len(sistem) - len(rata)
                if cur and (cw + wb / 2 > target or sisa_bar < sisa_sis) and len(rata) < len(sistem) - 1:
                    rata.append(cur)
                    cur, cw = [], 0
                cur.append((a_, b_))
                cw += wb
            rata.append(cur)
            if all(sum(lb[bar.index(x)] for x in sis) <= x_kanan - x_kiri for sis in rata):
                sistem = rata
        rh = uk * 1.72
        bawah_b = max([-o for s_ in suara[3:] for kt in s_[0] for _, o in kt] + [0])  # titik bawah terbanyak di suara bas
        jarak_syair = uk * 0.55 + 14 + 8 * bawah_b + uk * 0.62
        tinggi_sis = 3 * rh + jarak_syair + uk * 0.3
        tinggi = len(sistem) * tinggi_sis + (len(sistem) - 1) * uk * 1.3
        if tinggi <= 660 or uk <= 18:
            break
        uk -= 2
    y = 362 + rh * 0.5
    for sis in sistem:
        # posisi x tiap ketukan
        lebar_sis = sum(sum(lebar[a_:b_]) + uk * 0.9 for a_, b_ in sis)
        skala = min(1.6, (x_kanan - x_kiri) / lebar_sis)
        xpos, x = {}, x_kiri
        garis_birama = []
        for a_, b_ in sis:
            for b in range(a_, b_):
                xpos[b] = (x, x + lebar[b] * skala)
                x += lebar[b] * skala
            garis_birama.append(x + uk * 0.45 * skala)
            x += uk * 0.9 * skala
        for v, (nama, (ketuk, _)) in enumerate(zip("SATB", suara)):
            yv = y + v * rh
            d.text((x_kiri - 34, yv), nama, font=iowan(int(uk * 0.72), 2), fill=abu, anchor="rm")
            for b in xpos:
                x0, x1 = xpos[b]
                notes = ketuk[b]
                sub = len(notes)
                for j, (ch, okt) in enumerate(notes):
                    xc = x0 + (x1 - x0) * (j + 0.5) / sub
                    if ch == ".":
                        d.ellipse((xc - uk * 0.1, yv - uk * 0.1, xc + uk * 0.1, yv + uk * 0.1), fill=tinta_c)
                        continue
                    d.text((xc, yv), ch, font=fd, fill=tinta_c, anchor="mm")
                    garis = 1 if sub == 2 else (2 if sub >= 3 else 0)
                    for o in range(okt):
                        oy = yv - uk * 0.52 - 6 - o * 8
                        d.ellipse((xc - 3.3, oy - 3.3, xc + 3.3, oy + 3.3), fill=tinta_c)
                    for o in range(-okt):
                        oy = yv + uk * 0.5 + 4 + garis * 6 + 5 + o * 8
                        d.ellipse((xc - 3.3, oy - 3.3, xc + 3.3, oy + 3.3), fill=tinta_c)
                if sub >= 2:
                    for g in range(1 if sub == 2 else 2):
                        gy = yv + uk * 0.5 + 3 + g * 6
                        d.line((x0 + (x1 - x0) * 0.5 / sub - uk * 0.34, gy, x0 + (x1 - x0) * (sub - 0.5) / sub + uk * 0.34, gy), fill=tinta_c, width=2)
        # garis birama menembus 4 suara; birama akhir ganda
        for k, gx in enumerate(garis_birama):
            akhir = sis is sistem[-1] and k == len(garis_birama) - 1
            d.line((gx, y - rh * 0.42, gx, y + 3 * rh + rh * 0.42), fill=tinta_c, width=2)
            if akhir:
                d.line((gx + 7, y - rh * 0.42, gx + 7, y + 3 * rh + rh * 0.42), fill=tinta_c, width=6)
        d.line((x_kiri - 12, y - rh * 0.42, x_kiri - 12, y + 3 * rh + rh * 0.42), fill=tinta_c, width=3)
        for yb in (y - rh * 0.42, y + 3 * rh + rh * 0.42):
            d.line((x_kiri - 12, yb, x_kiri - 2, yb), fill=tinta_c, width=3)
        # syair
        yl = y + 3 * rh + jarak_syair
        pos_suku = []
        for b in xpos:
            x0, x1 = xpos[b]
            sub = len(suara[0][0][b])
            for j in range(sub):
                if (b, j) in sk_not:
                    pos_suku.append((x0 + (x1 - x0) * (j + 0.5) / sub, sk_not[(b, j)]))
        for k, (xc, sk) in enumerate(pos_suku):
            d.text((xc, yl), sk.rstrip("-"), font=fs_, fill=tinta_c, anchor="ms")
            if sk.endswith("-"):
                xa = xc + d.textlength(sk.rstrip("-"), font=fs_) / 2
                if k + 1 < len(pos_suku):
                    xb = pos_suku[k + 1][0] - d.textlength(pos_suku[k + 1][1].rstrip("-"), font=fs_) / 2
                else:  # kata berlanjut ke sistem berikutnya
                    xb = xa + uk * 1.1
                d.text(((xa + xb) / 2, yl), "-", font=fs_, fill=tinta_c, anchor="ms")
        y += tinggi_sis + uk * 1.3
    # hiasan + ayat
    y = max(y - uk * 0.6, 820)
    d.line((W / 2 - 150, y, W / 2 - 16, y), fill=abu, width=1)
    d.line((W / 2 + 16, y, W / 2 + 150, y), fill=abu, width=1)
    d.polygon([(W / 2, y - 8), (W / 2 + 8, y), (W / 2, y + 8), (W / 2 - 8, y)], fill=merah)
    blok_ayat(img, p, (120, y + 40, W - 120, H - 86), lambda s: iowan(s, 2), tinta_c, merah, start=32, stop=20, lh=1.38,
              ref_font=caslon(24), ref_teks=bersih(p["ref"]).upper(), vtengah=False)
    d.line((90, H - 70, W - 90, H - 70), fill=tinta_c, width=1)
    kredit(img, (W / 2, H - 40), abu, anchor="ms", size=20, font=caslon(20))
    return img


# ---------- STENSIL: cat semprot stensil di peti kayu ----------

def peti(w, h, seed):
    """Muka peti kayu: papan mendatar bercelah, dua papan tegak di sisi, paku."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    papan_h = 225
    idx = (yy // papan_h).astype(int)
    warna = np.array([(200, 168, 120), (186, 150, 104), (206, 174, 128), (180, 146, 100), (196, 162, 112), (190, 156, 108), (204, 170, 124)], np.float32)
    base = warna[idx % 7]
    serat = render.fbm2d(h // 4, w, rng, ((3, 1.0), (40, 0.6), (300, 0.4)))
    serat = np.asarray(Image.fromarray(serat).resize((w, h), Image.BICUBIC))
    garis = np.sin((yy + 22 * serat) * 0.9 + idx * 3) * 0.5 + 0.5
    base *= (0.86 + 0.16 * serat + 0.05 * garis ** 6)[..., None]
    for _ in range(5):  # mata kayu
        kx, ky = rng.uniform(100, w - 100), rng.uniform(40, h - 40)
        dd = np.hypot((xx - kx) / 1.8, yy - ky)
        base *= (1 - 0.22 * np.exp(-(dd / 10) ** 2) - 0.06 * (np.sin(dd / 3) ** 2) * np.exp(-(dd / 40) ** 2))[..., None]
    sisi = (xx < 86) | (xx > w - 86)
    base = np.where(sisi[..., None], base * 0.9 + np.array([6, 4, 0], np.float32), base)
    celah = ((yy % papan_h) < 7) & ~sisi
    base = np.where(celah[..., None], np.array([60, 44, 30], np.float32) * (0.8 + 0.3 * ((yy % papan_h) / 7))[..., None], base)
    tepi_s = (np.abs(xx - 86) < 3) | (np.abs(xx - (w - 86)) < 3)
    base = np.where(tepi_s[..., None], base * 0.55, base)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    for r in range(h // papan_h + 1):
        for x in (43, w - 43):
            for dy in (60, 165):
                y = r * papan_h + dy
                d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(70, 66, 62))
                d.ellipse((x - 6, y - 7, x + 4, y + 3), fill=(120, 116, 110))
                d.ellipse((x - 4, y - 5, x, y - 1), fill=(170, 166, 160))
    return grain(img.convert("RGB"), 0.06), papan_h


def stensil_mask(teks, f, w, h, xy, anchor="ms", jembatan=11):
    """Mask teks stensil: tiap huruf berlubang tertutup (A, O, D, ...) diberi jembatan seperti cetakan stensil."""
    m = np.zeros((h, w), np.float32)
    probe = ImageDraw.Draw(Image.new("L", (8, 8)))
    total = probe.textlength(teks, font=f)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    for ch in teks:
        adv = probe.textlength(ch, font=f)
        if ch.strip():
            bb = probe.textbbox((0, 0), ch, font=f, anchor="ls")
            gw, gh = bb[2] - bb[0] + 24, bb[3] - bb[1] + 24
            g = Image.new("L", (gw, gh), 0)
            ImageDraw.Draw(g).text((12 - bb[0], 12 - bb[1]), ch, font=f, fill=255, anchor="ls")
            ga = np.asarray(g) > 127
            inv = Image.fromarray(((~ga) * 255).astype(np.uint8)).copy()
            ImageDraw.floodfill(inv, (0, 0), 128)
            lubang = np.asarray(inv) == 255
            if lubang.any():
                kol = np.where(lubang.any(axis=0))[0]
                grup = np.split(kol, np.where(np.diff(kol) > 1)[0] + 1)
                ga = ga.copy()
                for gr in grup:
                    cxg = int(gr.mean())
                    for cx_ in range(cxg - jembatan // 2, cxg + jembatan // 2 + 1):
                        rows = np.where(lubang[:, cx_])[0] if 0 <= cx_ < gw else []
                        if len(rows) == 0:
                            continue
                        yy_ = rows.min() - 1
                        while yy_ >= 0 and ga[yy_, cx_]:
                            ga[yy_, cx_] = False
                            yy_ -= 1
                        yy_ = rows.max() + 1
                        while yy_ < gh and ga[yy_, cx_]:
                            ga[yy_, cx_] = False
                            yy_ += 1
            gx, gy = int(x + bb[0] - 12), int(y + bb[1] - 12)
            x0, y0 = max(gx, 0), max(gy, 0)
            x1, y1 = min(gx + gw, w), min(gy + gh, h)
            if x1 > x0 and y1 > y0:
                m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], ga[y0 - gy:y1 - gy, x0 - gx:x1 - gx])
        x += adv
    return m


def semprot(base, mask, warna, rng, seed, kuat=0.92):
    """Cat semprot lewat stensil: tepi sedikit lembut, semburan tipis di sekitar huruf, bintik, serat kayu tembus."""
    h, w = mask.shape
    mk = Image.fromarray((mask * 255).astype(np.uint8))
    lunak = np.asarray(mk.filter(ImageFilter.GaussianBlur(1.1))).astype(np.float32) / 255
    kabut = np.asarray(mk.filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255 * 0.25
    bintik = (rng.random((h, w)) < 0.03) & (kabut > 0.03) & (lunak < 0.1)
    a = np.maximum(lunak * kuat * (0.86 + 0.14 * render.fbm2d(h, w, np.random.default_rng(seed), ((6, 1.0), (40, 0.6)))), kabut)
    a = np.maximum(a, bintik * 0.7)
    return base * (1 - a[..., None]) + np.array(warna, np.float32) * a[..., None]


def stensil_image(p, i):
    rng = np.random.default_rng(18900 + i)
    cat, merah, hitam_t = [(30, 28, 26), (34, 40, 52), (40, 30, 26)][i % 3], (200, 50, 40), (36, 36, 38)
    kayu_img, papan_h = peti(W, H, 18900 + i)
    base = np.asarray(kayu_img).astype(np.float32)
    probe = ImageDraw.Draw(Image.new("L", (8, 8)))
    m = np.zeros((H, W), np.float32)
    # kata besar bertumpuk
    kata = [bersih(k).upper() for k in p["kata_besar"]][:2]
    uk = 330
    while max(probe.textlength(k, font=din(uk)) for k in kata) > W - 230 and uk > 120:
        uk -= 6
    cap = probe.textbbox((0, 0), "H", font=din(uk), anchor="ls")
    tinggi_cap = cap[3] - cap[1]
    y1 = 250 + tinggi_cap
    y2 = y1 + tinggi_cap + 34
    for k_, yb in zip(kata, (y1, y2)):
        m = np.maximum(m, stensil_mask(k_, din(uk), W, H, (W / 2, yb), "ms", jembatan=max(9, uk // 26)))
    # stensil kecil atas: dua panah ke atas + teks
    kecil = [bersih(k).upper() for k in p["kecil"]][:2]
    fk = din(64)
    while probe.textlength(kecil[0], font=fk) > W - 420 and fk.size > 34:
        fk = din(fk.size - 2)
    lk = probe.textlength(kecil[0], font=fk)
    m = np.maximum(m, stensil_mask(kecil[0], fk, W, H, (W / 2 + 0, 186), "ms", jembatan=max(3, fk.size // 18)))
    pm = Image.new("L", (W, H), 0)
    pdm = ImageDraw.Draw(pm)
    for sx in (W / 2 - lk / 2 - 100, W / 2 + lk / 2 + 30):
        for dx in (0, 38):
            panah_atas(pdm, sx + dx + 16, 128, 34, 62, 255)
    m = np.maximum(m, np.asarray(pm).astype(np.float32) / 255)
    fk2 = din(56)
    while probe.textlength(kecil[1], font=fk2) > 450 and fk2.size > 28:
        fk2 = din(fk2.size - 2)
    y3 = y2 + 96
    m = np.maximum(m, stensil_mask(kecil[1], fk2, W, H, (128, y3), "ls", jembatan=max(3, fk2.size // 18)))
    out = semprot(base, m, cat, rng, 18950 + i)
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    # label kiriman putih berstaples, berisi ayat
    lw_, lh_ = 720, 360
    lbl = Image.new("RGBA", (lw_, lh_), (248, 246, 240, 255))
    la = np.asarray(lbl).astype(np.float32)
    la[..., :3] *= (0.97 + 0.03 * render.fbm2d(lh_, lw_, rng, ((4, 1.0), (30, 0.4))))[..., None]
    lbl = Image.fromarray(la.astype(np.uint8))
    ldd = ImageDraw.Draw(lbl)
    ldd.rectangle((14, 14, lw_ - 14, lh_ - 14), outline=hitam_t + (255,), width=3)
    ldd.rectangle((14, 14, lw_ - 14, 66), fill=hitam_t + (255,))
    ldd.text((32, 41), "LABEL KIRIMAN", font=kurir(26, True), fill=(248, 246, 240, 255), anchor="lm")
    ldd.text((lw_ - 32, 41), "dari @" + HANDLE, font=kurir(19, True), fill=(220, 218, 212, 255), anchor="rm")
    f, vl, vs = pas_aman(ldd, bersih(p["ayat"]), lambda s: kurir(s), lw_ - 70, lh_ - 66 - 100, 34, 16, 1.32)
    yy_ = 66 + 14 + max(0, (lh_ - 66 - 100 - len(vl) * vs * 1.32) / 2)
    for ln in vl:
        ldd.text((34, yy_), ln, font=f, fill=hitam_t + (255,))
        yy_ += vs * 1.32
    ldd.line((14, lh_ - 76, lw_ - 14, lh_ - 76), fill=hitam_t + (255,), width=2)
    ldd.text((34, lh_ - 44), bersih(p["ref"]).upper(), font=kurir(24, True), fill=hitam_t + (255,), anchor="lm")
    ldd.text((lw_ - 34, lh_ - 44), "ISI BERHARGA", font=kurir(18, True), fill=(110, 108, 104, 255), anchor="rm")
    for sx_, sy_ in ((70, 7), (lw_ - 70, 7), (70, lh_ - 7), (lw_ - 70, lh_ - 7)):  # staples di tepi label
        ldd.rectangle((sx_ - 16, sy_ - 3, sx_ + 16, sy_ + 3), fill=(140, 140, 146, 255))
        ldd.line((sx_ - 16, sy_ - 3, sx_ + 16, sy_ - 3), fill=(222, 222, 228, 255), width=1)
        ldd.line((sx_ - 16, sy_ + 3, sx_ + 16, sy_ + 3), fill=(90, 90, 96, 255), width=1)
    lbl = lbl.rotate(1.6, expand=True, resample=Image.BICUBIC)
    ly0 = min(max(y3 + 56, 850), H - lbl.height - 44)
    bayangan(img, lbl, ((W - lbl.width) // 2, ly0), blur=10, geser=(4, 8), kuat=0.4)
    # cap merah miring
    teks_cap = bersih(p["cap"]).upper()
    fc = impact(64)
    while probe.textlength(teks_cap, font=fc) > 330 and fc.size > 28:
        fc = impact(fc.size - 2)
    cw_ = int(probe.textlength(teks_cap, font=fc) + 70)
    ch_ = fc.size + 50
    cm = Image.new("L", (cw_, ch_), 0)
    cd = ImageDraw.Draw(cm)
    cd.rectangle((4, 4, cw_ - 5, ch_ - 5), outline=255, width=6)
    cd.rectangle((14, 14, cw_ - 15, ch_ - 15), outline=255, width=2)
    cd.text((cw_ / 2, ch_ / 2 + 2), teks_cap, font=fc, fill=255, anchor="mm")
    cm = cm.rotate(14, expand=True, resample=Image.BICUBIC)
    full = Image.new("L", (W, H), 0)
    cpx, cpy = int(W - 80 - cm.width), int(y3 - 22 - cm.height / 2)
    full.paste(cm, (cpx, cpy))
    a = tinta(full, 18960 + i, 0.6) * 0.88
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    arr = arr * (1 - a[..., None]) + np.array(merah, np.float32) * a[..., None] * (arr / 255 * 0.35 + 0.65)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    return grain(img.convert("RGB"), 0.04).convert("RGBA")


# ---------- BENANG (Reels): benang dililitkan di paku membentuk hati ----------

def titik_hati(n, cx, cy, s):
    """n titik berjarak busur sama di kurva hati, mulai dari lekuk atas (tengah)."""
    t = np.linspace(0, 2 * np.pi, 6000)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    cum = np.concatenate([[0], np.cumsum(np.hypot(np.diff(x), np.diff(y)))])
    u = np.linspace(0, cum[-1], n, endpoint=False)
    return np.stack([cx + s * np.interp(u, cum, x), cy + s * np.interp(u, cum, y)], 1)


def paku(r=11):
    def gambar(d, k):
        d.ellipse(((2 + 3) * k, (2 + 5) * k, (2 * r + 2 + 3) * k, (2 * r + 2 + 5) * k), fill=(0, 0, 0, 110))
        d.ellipse((2 * k, 2 * k, (2 * r + 2) * k, (2 * r + 2) * k), fill=(150, 118, 52, 255))
        d.ellipse((4 * k, 3 * k, (2 * r) * k, (2 * r - 1) * k), fill=(200, 170, 90, 255))
        d.ellipse(((r - 3) * k, 6 * k, (r + 3) * k, 11 * k), fill=(250, 232, 170, 255))
    from gaya_w7 import sprite
    return sprite(2 * r + 10, 2 * r + 10, gambar)


def benang_reel(p, idx, mod=MOD, seconds=13):
    rel = f"reels/{mod}/benang{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(19000 + idx)
    krem, emas, merah = (240, 230, 210), (230, 180, 70), (220, 40, 60)
    bg = gaya_w8.kayu(RW, RH, rng, [(70, 46, 34), (62, 42, 34), (76, 50, 36)][idx % 3]).convert("RGB")
    a = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:RH, 0:RW].astype(np.float32)
    a *= (1.05 - 0.4 * (np.hypot((xx - RW / 2) / RW, (yy - 860) / RH) ** 1.6))[..., None]
    bg = grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05).convert("RGBA")
    n = 36
    cx, cy, sk = RW / 2, 852, 24
    nails = titik_hati(n, cx, cy, sk)
    kali = [2, 3, 13][idx % 3]
    merah_seg = []
    for i_ in range(n):
        for a_, b_ in ((i_, (i_ * kali) % n), ((i_ * kali) % n, (i_ + 1) % n)):
            if a_ != b_:
                merah_seg.append((a_, b_))
    krem_seg = [(3 * j % n, 3 * ((j + 5) % 12) % n) for j in range(12)]
    emas_seg = [(j, (j + 1) % n) for j in range(n)]
    S = 2
    bx0, by0, bx1, by1 = 120, 480, RW - 120, 1290
    lay = Image.new("RGBA", ((bx1 - bx0) * S, (by1 - by0) * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)

    def pos(k):
        return ((nails[k][0] - bx0) * S, (nails[k][1] - by0) * S)

    def tarik(a_, b_, col, w=2.2):
        (x0, y0), (x1, y1) = pos(a_), pos(b_)
        ld.line((x0 + 3, y0 + 4, x1 + 3, y1 + 4), fill=(0, 0, 0, 60), width=int((w + 1.4) * S))
        ld.line((x0, y0, x1, y1), fill=col + (235,), width=int(w * S))
    jadwal = []  # (t_mulai, t_selesai, a, b, warna, tebal)
    Nr = len(merah_seg)
    for j, (a_, b_) in enumerate(merah_seg):
        t0 = 1.5 + 5.5 * (j / Nr) ** (1 / 1.7)
        t1 = 1.5 + 5.5 * ((j + 1) / Nr) ** (1 / 1.7)
        jadwal.append((t0, t1, a_, b_, merah, 2.0))
    for j, (a_, b_) in enumerate(krem_seg):
        jadwal.append((7.0 + 1.4 * j / 12, 7.0 + 1.4 * (j + 1) / 12, a_, b_, krem, 2.6))
    for j, (a_, b_) in enumerate(emas_seg):
        jadwal.append((8.0 + 1.5 * j / n, 8.0 + 1.5 * (j + 1) / n, a_, b_, emas, 3.2))
    jadwal.sort()
    spr = paku()
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    judul = bersih(p["judul"]).upper()
    fj, jr = renggang_muat(probe, judul, lambda s: gill(s, 4), RW - 200, 36, 0.22)
    jl = Image.new("RGBA", (RW, 120), (0, 0, 0, 0))
    jd = ImageDraw.Draw(jl)
    renggang(jd, (RW / 2, 70), judul, fj, krem + (235,), jr, "ms")
    jd.line((RW / 2 - 40, 96, RW / 2 + 40, 96), fill=merah + (220,), width=3)
    av = Image.new("RGBA", (RW, 300), (0, 0, 0, 0))
    blok_ayat(av, dict(p), (110, 0, RW - 110, 252), lambda s: iowan(s, 2), krem + (255,), emas + (255,), start=42, stop=26,
              lh=1.34, ref_font=gill(30, 4))
    kredit_l = Image.new("RGBA", (RW, 60), (0, 0, 0, 0))
    kredit(kredit_l, (RW / 2, 30), (220, 200, 180, 170), anchor="mm", size=24)

    def simpul(lapisan, u):
        """Simpul pita kecil di lekuk atas hati: dua lengkung, simpul tengah, dua ujung menjuntai."""
        if u <= 0:
            return
        sp = Image.new("RGBA", (200 * S, 160 * S), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sp)
        c = (100 * S, 50 * S)
        for sgn in (-1, 1):
            pts = [(c[0] + sgn * (8 + 38 * math.sin(v) ** 0.9) * S, c[1] + (-18 * math.sin(2 * v)) * S) for v in np.linspace(0, math.pi, 30)]
            sd.line(pts + [pts[0]], fill=merah + (255,), width=6 * S, joint="curve")
            pts = [(c[0] + sgn * (6 + 26 * v) * S, c[1] + (8 + 62 * v + 8 * math.sin(v * 6)) * S) for v in np.linspace(0, 1, 16)]
            sd.line(pts, fill=merah + (255,), width=5 * S, joint="curve")
        sd.ellipse((c[0] - 11 * S, c[1] - 11 * S, c[0] + 11 * S, c[1] + 11 * S), fill=emas + (255,), outline=merah + (255,), width=3 * S)
        sp = sp.resize((int(200 * u), int(160 * u)), Image.LANCZOS)
        x, y = nails[0]
        lapisan.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height * 50 / 160)))

    cache = {"n": 0, "kecil": None}

    def frame_at(T, sampul=False):
        f = bg.copy()
        if sampul:
            T = 99.0
        while cache["n"] < len(jadwal) and jadwal[cache["n"]][1] <= T:
            _, _, a_, b_, col, w = jadwal[cache["n"]]
            tarik(a_, b_, col, w)
            cache["n"] += 1
            cache["kecil"] = None
        if cache["kecil"] is None:
            cache["kecil"] = lay.resize((bx1 - bx0, by1 - by0), Image.LANCZOS)
        f.alpha_composite(cache["kecil"], (bx0, by0))
        d = ImageDraw.Draw(f)
        if cache["n"] < len(jadwal) and jadwal[cache["n"]][0] <= T:  # benang yang sedang ditarik
            t0, t1, a_, b_, col, w = jadwal[cache["n"]]
            u = (T - t0) / max(t1 - t0, 1e-6)
            (x0, y0), (x1, y1) = nails[a_], nails[b_]
            d.line((x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), fill=col + (235,), width=int(w + 0.5))
        for k, (x, y) in enumerate(nails):
            tk = 0.08 + 1.2 * k / n
            u = 1.0 if T > tk + 0.3 else (0.0 if T < tk else (T - tk) / 0.3)
            if u <= 0:
                continue
            sc = 1 + 0.25 * math.sin(math.pi * u) if u < 1 else 1.0
            sp = spr if sc == 1.0 else spr.resize((max(2, int(spr.width * sc * u ** 0.5)), max(2, int(spr.height * sc * u ** 0.5))), Image.LANCZOS)
            f.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
        if T >= 9.5:
            simpul(f, ease((T - 9.5) / 0.6))
        z = 1 + 0.04 * ease((T - 9.5) / 1.0) if T >= 9.5 and not sampul else 1.0
        if z > 1.0001:
            w_, h_ = RW / z, RH / z
            x0 = min(max(cx - w_ / 2, 0), RW - w_)
            y0 = min(max(cy - h_ * (cy / RH), 0), RH - h_)
            f = f.crop((int(x0), int(y0), int(x0 + w_), int(y0 + h_))).resize((RW, RH), Image.BILINEAR)
        f.alpha_composite(jl if sampul else fade(jl, ease(T / 0.6)), (0, 352))
        if sampul or T >= 10.3:
            f.alpha_composite(av if sampul else fade(av, ease((T - 10.3) / 0.9)), (0, 1284))
        f.alpha_composite(kredit_l, (0, 1580))
        return f

    sampul = frame_at(0, sampul=True)
    cache.update(n=0, kecil=None)
    lay.paste((0, 0, 0, 0), (0, 0, lay.width, lay.height))
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for k in range(int(seconds * FPS)):
        t = k / FPS
        frame = sampul if t < 0.4 else frame_at(t - 0.4)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


# ---------- SPIRO (Reels): spirograf, satu putaran lagi ----------

SPIRO_SET = [(300, 144, 110), (296, 96, 80), (276, 144, 120)]  # (R, r, d): r/fpb(R, r) = 12 putaran
SOROT = ["dengan tekun", "bertekun", "ketekunan", "tekun", "bertahan", "kesabaran", "sabar", "jangan jemu-jemu", "tidak jemu-jemu"]


def baris_sorot(d, teks, f, maxw):
    """Bungkus teks; -> (baris, (awal, akhir) indeks karakter frasa yang disorot atau None)."""
    lines = bungkus(d, lekat(teks), f, maxw)
    gabung = " ".join(lines)
    for fr in SOROT:
        m = re.search(r"\b" + re.escape(fr) + r"\b", gabung, re.IGNORECASE)
        if m:
            return lines, (m.start(), m.end())
    return lines, None


def spiro_reel(p, idx, mod=MOD, seconds=14):
    rel = f"reels/{mod}/spiro{idx + 1}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    kertas_c, gir, teal, koral, abu = (250, 248, 242), (180, 180, 186), (30, 140, 150), (230, 100, 80), (60, 60, 66)
    R, r, dd = SPIRO_SET[idx % 3]
    putaran = r // math.gcd(R, r)
    sc = 430 / R
    cx, cy = RW / 2, 930
    bg = kertas(RW, RH, kertas_c, 19100 + idx, kuat=0.015, butir=0.03).convert("RGBA")
    d = ImageDraw.Draw(bg)
    for x in range(0, RW, 40):
        d.line((x, 0, x, RH), fill=(226, 230, 236), width=1)
    for y in range(0, RH, 40):
        d.line((0, y, RW, y), fill=(226, 230, 236), width=1)

    def kurva(t, d_):
        return (cx + ((R - r) * np.cos(t) + d_ * np.cos((R - r) * t / r)) * sc, cy + ((R - r) * np.sin(t) - d_ * np.sin((R - r) * t / r)) * sc)
    # cincin gigi (statis)
    S = 2
    Rp = R * sc
    gl = Image.new("RGBA", (RW * S, RH * S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    luar = Rp + 36
    gd.ellipse(((cx - luar) * S, (cy - luar) * S, (cx + luar) * S, (cy + luar) * S), fill=(232, 234, 240, 120), outline=gir + (255,), width=3 * S)
    gd.ellipse(((cx - Rp) * S, (cy - Rp) * S, (cx + Rp) * S, (cy + Rp) * S), fill=(0, 0, 0, 0), outline=gir + (255,), width=2 * S)
    gl = gl.resize((RW, RH), Image.LANCZOS)
    lubang = Image.new("L", (RW * S, RH * S), 0)
    ImageDraw.Draw(lubang).ellipse(((cx - Rp + 6) * S, (cy - Rp + 6) * S, (cx + Rp - 6) * S, (cy + Rp - 6) * S), fill=255)
    lubang = lubang.resize((RW, RH), Image.LANCZOS)
    ga = np.asarray(gl).copy()
    ga[..., 3] = np.where(np.asarray(lubang) > 128, ga[..., 3] * 0, ga[..., 3])
    gl = Image.fromarray(ga)
    gd = ImageDraw.Draw(gl)
    gigi = int(R / 4)
    for k in range(gigi):
        a = 2 * math.pi * k / gigi
        gd.line((cx + math.cos(a) * (Rp - 7), cy + math.sin(a) * (Rp - 7), cx + math.cos(a) * (Rp + 1), cy + math.sin(a) * (Rp + 1)), fill=gir + (255,), width=3)
    rp = r * sc

    def roda(t, d_, rot=0.0):
        """Roda kecil di dalam cincin pada parameter t (sprite + posisi), lubang pena sejauh d_; rot = putaran pola kedua."""
        wx, wy = cx + (R - r) * sc * math.cos(t + rot), cy + (R - r) * sc * math.sin(t + rot)
        phi = -(R - r) * t / r + rot
        m = int(rp + 30)
        sp = Image.new("RGBA", (2 * m * S, 2 * m * S), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sp)
        c = m * S
        sd.ellipse((c - rp * S, c - rp * S, c + rp * S, c + rp * S), fill=(226, 230, 238, 150), outline=gir + (255,), width=2 * S)
        gg = int(r / 4)
        for k in range(gg):
            a = phi + 2 * math.pi * k / gg
            sd.line((c + math.cos(a) * (rp - 6) * S, c + math.sin(a) * (rp - 6) * S, c + math.cos(a) * rp * S, c + math.sin(a) * rp * S), fill=gir + (255,), width=2 * S)
        for k, frac in enumerate((0.25, 0.45, 0.65)):
            a = phi + 2.1 * (k + 1)
            hx, hy = c + math.cos(a) * rp * frac * S, c + math.sin(a) * rp * frac * S
            sd.ellipse((hx - 6 * S, hy - 6 * S, hx + 6 * S, hy + 6 * S), outline=gir + (255,), width=2 * S)
        px, py = c + math.cos(phi) * d_ * sc * S, c + math.sin(phi) * d_ * sc * S
        sd.ellipse((px - 9 * S, py - 9 * S, px + 9 * S, py + 9 * S), outline=abu + (255,), width=2 * S)
        sd.ellipse((c - 4 * S, c - 4 * S, c + 4 * S, c + 4 * S), fill=gir + (255,))
        sp = sp.resize((2 * m, 2 * m), Image.LANCZOS)
        return sp, (int(wx - m), int(wy - m))
    # lapisan tinta 2x (hanya area lingkaran)
    rr = int((R - r + dd) * sc + 12)
    ox, oy = int(cx - rr), int(cy - rr)
    tinta_l = Image.new("RGBA", (2 * rr * S, 2 * rr * S), (0, 0, 0, 0))
    td = ImageDraw.Draw(tinta_l)
    T_end = 2 * math.pi * putaran
    d2 = dd * 0.58
    rot2 = math.pi / (R / math.gcd(R, r))

    def garis(t0, t1, col, d_, rot=0.0, w=2.6):
        if t1 <= t0:
            return
        ts = np.linspace(t0, t1, max(2, int((t1 - t0) / 0.02) + 1))
        x, y = kurva(ts, d_)
        if rot:
            xr, yr = x - cx, y - cy
            x, y = cx + xr * math.cos(rot) - yr * math.sin(rot), cy + xr * math.sin(rot) + yr * math.cos(rot)
        td.line([((a - ox) * S, (b - oy) * S) for a, b in zip(x, y)], fill=col + (230,), width=int(w * S), joint="curve")
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    judul = bersih(p["judul"])
    jl = Image.new("RGBA", (RW, 120), (0, 0, 0, 0))
    ImageDraw.Draw(jl).text((RW / 2, 84), judul, font=muat(probe, judul, lambda s: rounded(s, "Bold"), RW - 160, 64, 30), fill=abu + (255,), anchor="ms")
    lab = bersih(p["label_putaran"])

    def penghitung(n_):
        c = Image.new("RGBA", (RW, 120), (0, 0, 0, 0))
        cd_ = ImageDraw.Draw(c)
        cd_.text((RW / 2, 50), f"{lab} {n_}", font=menlo(44, 1), fill=abu + (255,), anchor="ms")
        for k in range(putaran):
            x = RW / 2 + (k - (putaran - 1) / 2) * 26
            if k < n_:
                cd_.ellipse((x - 7, 82, x + 7, 96), fill=teal + (255,))
            else:
                cd_.ellipse((x - 7, 82, x + 7, 96), outline=gir + (255,), width=2)
        return c
    hitung_cache = {}
    # ayat dengan frasa tekun disorot
    vb = (110, 0, RW - 110, 470)
    fv, vl, vs = pas_aman(probe, bersih(p["ayat"]), lambda s: iowan(s), vb[2] - vb[0], vb[3] - 80, 44, 24, 1.36)
    vl, sorot = baris_sorot(probe, bersih(p["ayat"]), fv, vb[2] - vb[0])
    av = Image.new("RGBA", (RW, 500), (0, 0, 0, 0))
    ad = ImageDraw.Draw(av)
    y = 0
    pos = 0
    for ln in vl:
        lw_ = ad.textlength(ln, font=fv)
        x = RW / 2 - lw_ / 2
        for j, ch in enumerate(ln):
            g = pos + j
            on = sorot is not None and sorot[0] <= g < sorot[1]
            if on:
                cw = ad.textlength(ch, font=fv)
                bl = y + fv.getmetrics()[0]
                ad.rectangle((x - 1, bl + 5, x + cw + 1, bl + 10), fill=koral + (200,))
            ad.text((x, y), ch, font=fv, fill=(koral if on else abu) + (255,), anchor="la")
            x += ad.textlength(ln[:j + 1], font=fv) - ad.textlength(ln[:j], font=fv)
        pos += len(ln) + 1
        y += vs * 1.36
    ad.text((RW / 2, y + 12), bersih(p["ref"]), font=rounded(34, "Bold"), fill=teal + (255,), anchor="ma")
    kred = Image.new("RGBA", (RW, 50), (0, 0, 0, 0))
    kredit(kred, (RW / 2, 25), (150, 150, 156, 255), anchor="mm", size=24)

    def frame_at(T, sampul=False):
        f = bg.copy()
        if sampul:
            T = 10.0
        t_pen = T_end * min(1.0, max(0.0, (T - 1.0) / 7.0)) ** 1.08
        t_pen2 = T_end * min(1.0, max(0.0, (T - 8.0) / 2.0))
        state = frame_at.state
        garis(state["t1"], t_pen, teal, dd)
        state["t1"] = max(state["t1"], t_pen)
        garis(state["t2"], t_pen2, koral, d2, rot2, 2.2)
        state["t2"] = max(state["t2"], t_pen2)
        if state["kecil_t"] != (state["t1"], state["t2"]):
            state["kecil"] = tinta_l.resize((2 * rr, 2 * rr), Image.LANCZOS)
            state["kecil_t"] = (state["t1"], state["t2"])
        a_g = 0.0 if sampul else (ease(T / 1.0) if T < 10 else 1 - ease(T - 10.0))
        if a_g > 0:
            f.alpha_composite(fade(gl, a_g))
        z = 1.0 if sampul else 1 - 0.4 * ease((T - 11.0) / 1.0)
        dy = 0.0 if sampul else -170 * ease((T - 11.0) / 1.0)
        tk = state["kecil"]
        if z < 0.999:
            tk = tk.resize((max(2, int(tk.width * z)), max(2, int(tk.height * z))), Image.LANCZOS)
        f.alpha_composite(tk, (int(cx - tk.width / 2), int(cy + dy - tk.height / 2)))
        if a_g > 0 and T < 11:
            tw = t_pen2 if T >= 8 else t_pen
            dpen, rot = (d2, rot2) if T >= 8 else (dd, 0.0)
            sp, xy = roda(tw, dpen, rot)
            f.alpha_composite(fade(sp, a_g), xy)
            px, py = kurva(np.array([tw]), dpen)
            if rot:
                xr, yr = px[0] - cx, py[0] - cy
                px, py = [cx + xr * math.cos(rot) - yr * math.sin(rot)], [cy + xr * math.sin(rot) + yr * math.cos(rot)]
            col = koral if T >= 8 else teal
            ImageDraw.Draw(f).ellipse((px[0] - 6, py[0] - 6, px[0] + 6, py[0] + 6), fill=col + (int(255 * a_g),))
        f.alpha_composite(jl if sampul else fade(jl, ease(T / 0.6)), (0, 360))
        n_ = putaran if sampul else min(putaran, int(t_pen / (2 * math.pi)) + 1) if T >= 1.0 else 0
        if n_ not in hitung_cache:
            hitung_cache[n_] = penghitung(n_)
        a_h = 1.0 if sampul else (ease((T - 0.6) / 0.5) if T < 10 else 1 - ease((T - 10.0) / 0.8))
        if a_h > 0 and n_ > 0:
            f.alpha_composite(fade(hitung_cache[n_], a_h), (0, 1400))
        if not sampul and T >= 11.3:
            f.alpha_composite(fade(av, ease((T - 11.3) / 1.0)), (0, 1046))
        f.alpha_composite(kred, (0, 1572))
        return f

    frame_at.state = {"t1": 0.0, "t2": 0.0, "kecil": None, "kecil_t": None}
    sampul = frame_at(0, sampul=True)
    tinta_l.paste((0, 0, 0, 0), (0, 0, tinta_l.width, tinta_l.height))
    frame_at.state = {"t1": 0.0, "t2": 0.0, "kecil": None, "kecil_t": None}
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for k in range(int(seconds * FPS)):
        t = k / FPS
        frame = sampul if t < 0.4 else frame_at(t - 0.4)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel



# ================= MIX =================

def tahun_post(p, default="2027"):
    return (p.get("_tanggal") or default).split()[-1]


def tulis_ulang(img, xy, teks, font, warna, anchor):
    """Menimpa teks yang sudah digambar gaya lama (posisi & huruf sama) dengan warna yang lebih terbaca."""
    ImageDraw.Draw(img).text(xy, teks, font=font, fill=warna, anchor=anchor)
    return img


def sticky_tenun(p, i):
    latar = tenun_latar(W, H, 18010 + i, polos=[(H - 100, H - 20, "gelap")])
    img = gaya_w8.sticky_image(p, i, latar=latar)
    return tulis_ulang(img, (300, H - 64), "@" + HANDLE, hn(22, 10), KREM_TENUN, "ma")


def stamp_tenun(p, i):
    """Perangko di atas kain tenun; ayat (teks gelap) jatuh di pita polos krem. Tahun di perangko ikut tahun post."""
    img = gaya_w12.stamp_image(p, i, latar=tenun_latar(W, H, 18020 + i, polos=[(952, H + 10, "terang")]))
    sw, sh = 700, 860
    patch = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    pd = ImageDraw.Draw(patch)
    pd.rectangle((70, sh - 90, sw - 70, sh - 50), fill=(252, 250, 244, 255))
    pd.text((sw / 2, sh - 80), f"POS SUKACITA · {tahun_post(p)}", font=hn(26, 1), fill=(90, 80, 70, 255), anchor="ma")
    patch = patch.rotate(-3, expand=True, resample=Image.BILINEAR)
    comp(img, patch, ((W - patch.width) // 2, 50))
    return tulis_ulang(img, (W / 2, H - 40), "@" + HANDLE, hn(22, 10), (96, 80, 64), "ma")


def photobooth_tenun(p, i):
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    n = len(wrap(probe, bersih(p["judul"]), gaya_w7.tangan(64), 410))
    latar = tenun_latar(W, H, 18030 + i, polos=[(96, 140 + n * 76 + 26, "gelap"), (H - 64, H, "gelap")])
    img = gaya_w11.photobooth_image(p, i, latar=latar)
    return tulis_ulang(img, (W - 40, H - 30), "@" + HANDLE, hn(22, 10), KREM_TENUN, "rs")


def majalah_senja(p, i):
    """Sampul majalah di langit senja, tulisan edisi ikut bulan post (bukan 'EDISI ADVEN · DESEMBER 2026')."""
    foto = senja_latar(W, H, 18080 + i, cakrawala=0.86, redup=0.12)
    img = gaya_w10.majalah_image(p, i, latar=foto).convert("RGB")
    a = np.asarray(foto).astype(np.float32)[30:70]
    yy = np.linspace(0, 1, H)[30:70, None, None]
    a *= 1 - 0.55 * np.clip((0.3 - yy) / 0.3, 0, 1)
    img.paste(grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 0.05), (0, 30))
    d = ImageDraw.Draw(img)
    bulan = " ".join((p.get("_tanggal") or "30 Januari 2027").split()[1:]).upper()
    edisi = bersih(p.get("edisi", "EDISI SENJA")).upper()
    d.text((W / 2, 40), f"{edisi}  ·  {bulan}  ·  @{HANDLE.upper()}", font=hn(22, 1), fill=(255, 255, 255), anchor="ma")
    d.rectangle((W - 226, H - 82, W - 64, H - 60), fill=(255, 255, 255))
    d.text((W - 145, H - 72), p.get("_tgl_struk", "30/01/2027").replace("/", "-"), font=hn(16, 10), fill=(20, 20, 20), anchor="mm")
    return img


def pixel_tahun(p, i):
    """PIXEL lama dengan 'SKOR <tahun post>' (aslinya 'SKOR 2026')."""
    img = gaya_w11.pixel_image(p, i)
    sw, k = 270, 4
    kecil = Image.new("RGB", (sw, 338), (16, 14, 40))
    kd = ImageDraw.Draw(kecil)
    kd.fontmode = "1"
    rng = np.random.default_rng(5600 + i)  # bintang yang sama seperti gaya aslinya
    for _ in range(60):
        x, y = rng.integers(0, sw), rng.integers(0, 200)
        kd.point((int(x), int(y)), fill=(200, 200, 255))
    fs = gaya_w7.ft("/System/Library/Fonts/Menlo.ttc", 9, 1)
    x0, y0, x1, y1 = kd.textbbox((sw - 12, 30), "SKOR 2026", font=fs, anchor="ra")
    kd.text((sw - 12, 30), f"SKOR {tahun_post(p)}", font=fs, fill=(220, 220, 240), anchor="ra")
    box = (x0 - 1, y0 - 1, x1 + 1, y1 + 1)
    img.paste(kecil.crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.NEAREST), (box[0] * k, box[1] * k))
    return img


SIMPLE = {
    # baru
    "KALKULATOR": kalkulator_image, "UNSUR": unsur_image, "PALET": palet_image, "MUARA": muara_image, "TALI": tali_image,
    "PERCA": perca_image, "TANGGA": tangga_image, "FASE": fase_image, "KIDUNG": kidung_image, "STENSIL": stensil_image,
    # lama
    "SCROLL": gaya_w11.scroll_image, "PIXEL": pixel_tahun, "CHART": gaya_w11.chart_image, "HPJADUL": gaya_w11.hpjadul_image,
    "TAG": lambda p, i: gaya_w11.tag_image(p, i, latar=tenun_latar(W, H, 18600 + i)),  # bukan kertas kado Natal
    "KACAPATRI": gaya_w11.kacapatri_image, "POSTERTEBAL": gaya_w13.postertebal_image,
    "BERITA": gaya_w13.berita_image, "RAMBU": gaya_w9.rambu_image,
    # mix: latar TENUN / SENJA, efek HANGAT
    "STICKYTENUN": sticky_tenun,
    "STAMPTENUN": stamp_tenun,
    "TELEGRAMTENUN": lambda p, i: gaya_w10.telegram_image(p, i, latar=tenun_latar(W, H, 18040 + i)),
    "PHOTOBOOTHTENUN": photobooth_tenun,
    "POLAROIDSENJA": lambda p, i: gaya_w7.polaroid_image(p, i, latar=senja_latar(W, H, 18050 + i)),
    "TIKETSENJA": lambda p, i: gaya_w7.tiket_image(p, i, latar=senja_latar(W, H, 18060 + i)),
    "BALONSENJA": lambda p, i: gaya_w12.balon_image(p, i, latar=senja_latar(W, H, 18070 + i, cakrawala=0.44, matahari=0.8, pantul=0.45)),
    "RESEPSENJA": lambda p, i: gaya_w9.resep_image(p, i, latar=senja_latar(W, H, 18090 + i)),
    "MAJALAHSENJA": majalah_senja,
    "KAMUSHANGAT": lambda p, i: hangat(gaya_w7.kamus_image(p, i), 18100 + i),
    "KETIKHANGAT": lambda p, i: hangat(gaya_w7.ketik_image(p, i), 18110 + i),
    "CATATANHANGAT": lambda p, i: hangat(tulis_ulang(gaya_w7.catatan_image(p, i), (W / 2, H - 30), "@" + HANDLE, hn(20, 0),
                                                     (140, 140, 146), "ms"), 18120 + i),
    # komik Eli
    "KOMIK": gaya_w5.komik_image,
}
MULTI = {}
REELS = {"BENANG": (benang_reel, "benang"), "SPIRO": (spiro_reel, "spiro"), "PANGGUNG": (gaya_w13.panggung_reel, "panggung"),
         "NEON": (gaya_w7.neon_reel, "neon"), "KONFETI": (gaya_w12.konfeti_reel, "konfeti")}  # KONFETI: tampilan siang (bawaan)


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
