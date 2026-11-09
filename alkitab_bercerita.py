"""Seri "Alkitab Bercerita" di @diam.dan.percaya: setiap Jumat & Sabtu satu Reels dari YouTube Shorts Felix,
dengan post PREVIEW sebelumnya dan post PENDUKUNG sesudahnya. Desainnya selalu sama supaya penonton mengenali serinya.

  16.00 WIB  preview  (3 slide: cover + hook, teaser, kartu seri dengan jadwal minggu itu)
  19.00 WIB  Reels    (video Shorts, dikompres <17 MB untuk jsDelivr, cover 9:16 khusus)
  21.30 WIB  pendukung (5 slide: cover, 3 pelajaran dengan ayat TB, penutup + episode berikutnya)
  + Story 10 menit setelah masing-masing (gambar 9:16; video Reels > 60 detik tidak bisa jadi Story lewat API)

Isi: konten/alkitab_bercerita.py (JADWAL_AB + EPISODES). Bahan: ~/Desktop/CHANNEL_KRISTEN/<dir>.
Hasil: output/ab/<slug>/..., state/alkitab_bercerita.json (semua item). terapkan() dipanggil render.build_schedule
setelah Story dibuat, jadi render ulang tetap memuat seri ini. jadwal_3hari.py tidak menyentuh item ber-"seri".

  python3 alkitab_bercerita.py            # render semua episode di JADWAL_AB lalu gabungkan ke output/schedule.json
  python3 alkitab_bercerita.py yusuf      # render ulang satu episode saja
  python3 cek_modul.py alkitab_bercerita  # cek ayat dulu
"""
import json
import subprocess
import sys
import textwrap
from datetime import date, datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from konten.alkitab_bercerita import EPISODES, JADWAL_AB

ROOT = Path(__file__).parent
OUT = ROOT / "output"
SUMBER = Path.home() / "Desktop" / "CHANNEL_KRISTEN"
STATE = ROOT / "state" / "alkitab_bercerita.json"
JAM = {"preview": "16:00", "reels": "19:00", "pendukung": "21:30"}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BATAS_MB = 16.5  # jsDelivr tidak menyajikan file GitHub > 20 MB

BG = (21, 16, 11)
EMAS = (214, 178, 106)
KRIM = (244, 233, 210)
REDUP = (196, 178, 145)
W, H = 1080, 1350

_F = {
    "serif": ("/System/Library/Fonts/Supplemental/Baskerville.ttc", 4),   # SemiBold
    "italic": ("/System/Library/Fonts/Supplemental/Baskerville.ttc", 2),
    "caps": ("/System/Library/Fonts/Supplemental/BigCaslon.ttf", 0),
    "sans": ("/System/Library/Fonts/Avenir Next.ttc", 5),                 # Medium
    "sans_tebal": ("/System/Library/Fonts/Avenir Next.ttc", 2),           # Demi Bold
}


def F(kind, size):
    path, idx = _F[kind]
    return ImageFont.truetype(path, size, index=idx)


# ---------- alat gambar ----------

def isi(path, w, h, fokus=0.4):
    """Gambar menutupi w x h (crop), fokus = posisi vertikal potongan (0 atas, 1 bawah)."""
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = round((im.height - h) * fokus)
    return im.crop((x, y, x + w, y + h))


def gradien(img, y0, y1, a0, a1, warna=BG):
    """Lapisan warna dengan alpha naik/turun linear dari y0 ke y1 (di bawah y1 tetap a1)."""
    lap = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(lap)
    for y in range(img.height):
        if y < y0:
            a = a0
        elif y > y1:
            a = a1
        else:
            a = a0 + (a1 - a0) * (y - y0) / max(1, y1 - y0)
        d.line([(0, y), (img.width, y)], fill=round(255 * a))
    return Image.composite(Image.new("RGB", img.size, warna), img, lap)


def gelap(img, a):
    return Image.blend(img, Image.new("RGB", img.size, BG), a)


def lebar_spasi(text, font, spasi):
    return sum(font.getlength(c) for c in text) + spasi * (len(text) - 1)


def spasi_teks(d, cx, y, text, font, fill, spasi=4):
    """Teks huruf besar berjarak, rata tengah di cx."""
    x = cx - lebar_spasi(text, font, spasi) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + spasi


def bungkus(text, font, maxw):
    kata, baris, cur = text.split(), [], ""
    for k in kata:
        coba = (cur + " " + k).strip()
        if font.getlength(coba) <= maxw or not cur:
            cur = coba
        else:
            baris.append(cur)
            cur = k
    if cur:
        baris.append(cur)
    return baris


def paragraf(d, cx, y, text, font, fill, maxw, jarak=1.25, rata="tengah", x0=None):
    """Tulis paragraf terbungkus; kembalikan y setelahnya."""
    tinggi = font.size * jarak
    for b in bungkus(text, font, maxw):
        if rata == "tengah":
            d.text((cx, y), b, font=font, fill=fill, anchor="ma")
        else:
            d.text((x0, y), b, font=font, fill=fill)
        y += tinggi
    return y


def tinggi_paragraf(text, font, maxw, jarak=1.25):
    return len(bungkus(text, font, maxw)) * font.size * jarak


def pas(text, kind, maxw, maxh, besar, kecil=28, jarak=1.25):
    """Font terbesar (besar..kecil) yang membuat paragraf muat di maxh."""
    for s in range(besar, kecil - 1, -2):
        f = F(kind, s)
        if tinggi_paragraf(text, f, maxw, jarak) <= maxh:
            return f
    return F(kind, kecil)


_IKON = None


def ikon(size):
    """Logo buku Alkitab Bercerita (dari foto profil channel), dipotong bulat."""
    global _IKON
    if _IKON is None:
        _IKON = Image.open(SUMBER / "branding" / "ALKITAB_BERCERITA_PROFIL.png").convert("RGB")
    im = _IKON.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    return im, mask.resize((size, size), Image.LANCZOS)


def tempel_ikon(img, cx, y, size):
    im, m = ikon(size)
    img.paste(im, (cx - size // 2, y), m)
    ImageDraw.Draw(img).ellipse((cx - size // 2 - 2, y - 2, cx + size // 2 + 1, y + size + 1), outline=EMAS, width=2)


def merek(img, y=54, size=64):
    """Kepala seri: ikon + ALKITAB BERCERITA + garis emas. Sama di semua slide."""
    tempel_ikon(img, img.width // 2, y, size)
    d = ImageDraw.Draw(img)
    spasi_teks(d, img.width // 2, y + size + 18, "ALKITAB BERCERITA", F("caps", 30), EMAS, 7)
    return y + size + 18 + 44


def bar(img, teks, tinggi=96):
    """Pita emas di bawah: ciri khas seri."""
    d = ImageDraw.Draw(img)
    d.rectangle((0, img.height - tinggi, img.width, img.height), fill=EMAS)
    f = F("sans_tebal", 29)
    spasi_teks(d, img.width // 2, img.height - tinggi + (tinggi - 40) // 2, teks, f, BG, 4)


def label(d, cx, y, teks):
    """Label kecil berbingkai emas, mis. EPISODE 01."""
    f = F("sans_tebal", 24)
    w = lebar_spasi(teks, f, 5) + 48
    d.rounded_rectangle((cx - w / 2, y, cx + w / 2, y + 46), radius=23, outline=EMAS, width=2)
    spasi_teks(d, cx, y + 9, teks, f, EMAS, 5)


def gambar(ep, nama):
    return SUMBER / ep["dir"] / "gambar" / nama


# ---------- slide ----------

def cover(ep, no, latar, headline, sub, label_teks, bar_teks, size=(W, H), fokus=0.35):
    w, h = size
    img = isi(latar, w, h, fokus)
    img = gradien(img, 0, int(h * 0.26), 0.78, 0.0) if h == H else gradien(img, 330, 760, 0.8, 0.0)  # 9:16: logo di y 300
    img = gradien(img, int(h * 0.38), int(h * 0.80), 0.0, 0.94)
    merek(img, y=54 if h == H else 300)
    d = ImageDraw.Draw(img)
    bawah = h - 96 - (70 if h == H else 330)  # 9:16: teks tetap di area tengah (grid Instagram memotong 4:5)
    fsub = F("sans", 30)
    fh = pas(headline, "serif", w - 160, 330, 76, 50, 1.18)
    th = tinggi_paragraf(headline, fh, w - 160, 1.18)
    y = bawah - 46 - 26 - th - 34 - 46
    label(d, w // 2, y, label_teks)
    y = paragraf(d, w // 2, y + 46 + 34, headline, fh, KRIM, w - 160, 1.18)
    d.line((w // 2 - 60, y + 14, w // 2 + 60, y + 14), fill=EMAS, width=3)
    d.text((w // 2, y + 40), sub, font=fsub, fill=REDUP, anchor="ma")
    bar(img, bar_teks)
    return img


def teaser(ep, no, hari):
    img = isi(gambar(ep, ep["gambar"]["teaser"]), W, H, 0.4)
    img = gelap(img, 0.35)
    img = gradien(img, 0, 170, 0.75, 0.0)
    img = gradien(img, int(H * 0.25), int(H * 0.75), 0.0, 0.9)
    d = ImageDraw.Draw(img)
    spasi_teks(d, W // 2, 70, f"ALKITAB BERCERITA  ·  EPISODE {no:02d}", F("sans_tebal", 24), EMAS, 5)
    f1 = pas(ep["teaser"], "serif", W - 180, 360, 68, 46, 1.2)
    f2 = pas(ep["teaser_kecil"], "italic", W - 200, 150, 42, 30, 1.25)
    t1, t2 = tinggi_paragraf(ep["teaser"], f1, W - 180, 1.2), tinggi_paragraf(ep["teaser_kecil"], f2, W - 200, 1.25)
    y = H - 96 - 110 - t1 - 40 - t2
    y = paragraf(d, W // 2, y, ep["teaser"], f1, KRIM, W - 180, 1.2)
    d.line((W // 2 - 60, y + 16, W // 2 + 60, y + 16), fill=EMAS, width=3)
    paragraf(d, W // 2, y + 40, ep["teaser_kecil"], f2, EMAS, W - 200, 1.25)
    bar(img, f"JAWABANNYA DI REELS  ·  {hari.upper()} 19.00 WIB")
    return img


def kartu_seri(ep, minggu_ini, slug_ini):
    """Kartu seri: ikon besar, nama seri, jadwal Jumat & Sabtu minggu ini (yang tayang hari ini disorot)."""
    img = isi(gambar(ep, ep["gambar"]["cover"]), W, H, 0.4).filter(ImageFilter.GaussianBlur(28))
    img = gelap(img, 0.78)
    tempel_ikon(img, W // 2, 130, 170)
    d = ImageDraw.Draw(img)
    spasi_teks(d, W // 2, 350, "ALKITAB BERCERITA", F("caps", 60), EMAS, 8)
    paragraf(d, W // 2, 445, "Kisah nyata dari Alkitab, diceritakan dalam 1–2 menit, dengan ayat asli Terjemahan Baru.",
             F("italic", 38), KRIM, W - 220, 1.3)
    y = 640
    spasi_teks(d, W // 2, y, "MINGGU INI DI REELS", F("sans_tebal", 24), REDUP, 5)
    y += 56
    for tgl, slug in minggu_ini:
        hari = HARI[date.fromisoformat(tgl).weekday()].upper()
        nyala = slug == slug_ini
        d.rounded_rectangle((100, y, W - 100, y + 136), radius=20, fill=EMAS if nyala else None, outline=EMAS, width=2)
        warna = BG if nyala else KRIM
        spasi_teks(d, 245, y + 28, hari, F("sans_tebal", 32), warna, 4)
        d.text((245, y + 76), "19.00 WIB", font=F("sans", 28), fill=BG if nyala else REDUP, anchor="ma")
        d.line((390, y + 26, 390, y + 110), fill=BG if nyala else EMAS, width=2)
        d.text((430, y + 68), EPISODES[slug]["nama"], font=pas(EPISODES[slug]["nama"], "serif", 420, 60, 46, 34), fill=warna, anchor="lm")
        if nyala:
            d.text((W - 130, y + 68), "HARI INI", font=F("sans_tebal", 22), fill=BG, anchor="rm")
        y += 160
    y += 40
    d.text((W // 2, y), "Nyalakan notifikasi post @diam.dan.percaya", font=F("sans", 32), fill=KRIM, anchor="ma")
    d.text((W // 2, y + 54), "Seri lengkapnya juga ada di YouTube: Alkitab Bercerita", font=F("sans", 28), fill=REDUP, anchor="ma")
    bar(img, "SETIAP JUMAT & SABTU  ·  19.00 WIB")
    return img


def pelajaran(ep, no, i, p, latar):
    img = Image.new("RGB", (W, H), BG)
    atas = isi(latar, W, 640, 0.35)
    atas = gradien(atas, 0, 150, 0.7, 0.0)
    atas = gradien(atas, 360, 640, 0.0, 1.0)
    img.paste(atas, (0, 0))
    d = ImageDraw.Draw(img)
    spasi_teks(d, W // 2, 46, "3 HAL DARI KISAH INI", F("sans_tebal", 22), EMAS, 5)
    d.text((86, 600), f"0{i + 1}", font=F("serif", 130), fill=EMAS, anchor="ls")
    # judul: satu baris kalau bisa (font 62 -> 46), kalau tidak dua baris tanpa kata yatim
    fj = pas(p["judul"], "serif", W - 180, 62 * 1.15, 62, 46, 1.15)
    if len(bungkus(p["judul"], fj, W - 180)) > 1:
        fj = pas(p["judul"], "serif", W - 180, 150, 58, 42, 1.15)
    lebar_j = W - 180
    while len(bungkus(p["judul"], fj, lebar_j)) == 2 and len(bungkus(p["judul"], fj, lebar_j)[-1].split()) == 1 and lebar_j > 560:
        lebar_j -= 40
    tj = tinggi_paragraf(p["judul"], fj, lebar_j, 1.15)
    fa = pas(p["ayat"], "italic", W - 230, 300, 44, 30, 1.3)
    ta = tinggi_paragraf(p["ayat"], fa, W - 230, 1.3)
    fi = pas(p["isi"], "sans", W - 180, 220, 36, 26, 1.4)
    ti = tinggi_paragraf(p["isi"], fi, W - 180, 1.4)
    blok = tj + 30 + ta + 84 + ti
    y = 640 + max(0, (1225 - 640 - blok) * 0.45)  # rata tengah (sedikit ke atas) di bawah gambar
    y = paragraf(d, 0, y, p["judul"], fj, KRIM, lebar_j, 1.15, rata="kiri", x0=90) + 30
    d.line((90, y + 6, 90, y + ta + 44), fill=EMAS, width=4)
    y2 = paragraf(d, 0, y, p["ayat"], fa, KRIM, W - 230, 1.3, rata="kiri", x0=120)
    spasi_teks(d, 120 + lebar_spasi(p["ref"].upper(), F("sans_tebal", 24), 3) / 2, y2 + 8, p["ref"].upper(),
               F("sans_tebal", 24), EMAS, 3)
    paragraf(d, 0, y2 + 84, p["isi"], fi, REDUP, W - 180, 1.4, rata="kiri", x0=90)
    d.line((90, H - 92, W - 90, H - 92), fill=(70, 58, 40), width=1)
    spasi_teks(d, W // 2, H - 70, f"ALKITAB BERCERITA  ·  {ep['nama'].upper()}  ·  {i + 2}/5", F("sans_tebal", 20), EMAS, 4)
    return img


def penutup(ep, no, berikut):
    img = isi(gambar(ep, ep["gambar"]["pendukung"]), W, H, 0.4).filter(ImageFilter.GaussianBlur(24))
    img = gelap(img, 0.72)
    y = merek(img, y=120, size=110) + 90
    d = ImageDraw.Draw(img)
    y = paragraf(d, W // 2, y, "Sudah nonton Reels-nya?", F("serif", 70), KRIM, W - 160, 1.15)
    y = paragraf(d, W // 2, y + 14, "Kisah lengkapnya ada di postingan sebelum ini.", F("italic", 40), KRIM, W - 200, 1.3)
    y += 90
    d.rounded_rectangle((110, y, W - 110, y + 250), radius=22, outline=EMAS, width=2)
    spasi_teks(d, W // 2, y + 34, "BERIKUTNYA", F("sans_tebal", 24), REDUP, 6)
    spasi_teks(d, W // 2, y + 80, berikut[0].upper(), F("sans_tebal", 32), EMAS, 4)
    paragraf(d, W // 2, y + 140, berikut[1], pas(berikut[1], "serif", W - 300, 60, 52, 36, 1.1), KRIM, W - 300, 1.1)
    y += 340
    d.text((W // 2, y), "Simpan & kirim ke teman yang perlu kisah ini", font=F("sans", 32), fill=KRIM, anchor="ma")
    d.text((W // 2, y + 54), "Seri lengkap di YouTube: Alkitab Bercerita", font=F("sans", 28), fill=REDUP, anchor="ma")
    bar(img, "SETIAP JUMAT & SABTU  ·  19.00 WIB")
    return img


# ---------- video ----------

def kompres(src, dst):
    """Kompres ke < BATAS_MB (2-pass). 1080p kalau bitratenya cukup, kalau tidak 720p."""
    if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime and dst.stat().st_size < BATAS_MB * 1e6:
        return
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
    kbps = min(4000, int(BATAS_MB * 8e3 / dur * 0.96) - 128)
    skala = "1080:1920" if kbps >= 2200 else "720:1280"
    dst.parent.mkdir(parents=True, exist_ok=True)
    log = str(dst.parent / "ffpass")
    umum = ["-vf", f"scale={skala}:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{kbps}k",
            "-maxrate", f"{int(kbps * 1.5)}k", "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p", "-r", "30", "-passlogfile", log]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *umum, "-pass", "1", "-an", "-f", "mp4", "/dev/null"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *umum, "-pass", "2", "-c:a", "aac", "-b:a", "128k",
                    "-ar", "44100", "-movflags", "+faststart", str(dst)], check=True)
    for p in dst.parent.glob("ffpass*"):
        p.unlink()
    mb = dst.stat().st_size / 1e6
    assert mb < BATAS_MB + 0.5, f"{dst} {mb:.1f} MB"
    print(f"  video {dst.name}: {dur:.0f} detik, {skala}, {kbps} kbps, {mb:.1f} MB")


# ---------- caption ----------

TAGAR = "#AlkitabBercerita #KisahAlkitab #{tag} #RenunganHarian #AyatAlkitab #FirmanTuhan #RenunganKristen"


def cap_preview(ep, hari):
    return (f"🎬 Malam ini {hari} 19.00 WIB di Reels: {ep['nama']}\n\n"
            f"{ep['hook']}\n\n{ep['teaser']} {ep['teaser_kecil']}\n\n"
            "Alkitab Bercerita adalah seri kisah nyata dari Alkitab, diceritakan singkat dengan ilustrasi dan ayat "
            "Terjemahan Baru. Tayang setiap Jumat & Sabtu jam 19.00 WIB di @diam.dan.percaya.\n\n"
            "🔔 Nyalakan notifikasi supaya tidak ketinggalan.\n\n" + TAGAR.format(tag=ep["tag"]))


def cap_reels(ep):
    return (f"{ep['hook']} | {ep['nama']}\n\n{ep['ringkas']}\n\n📖 {ep['kitab']}\n\n{ep['tanya']}\n\n"
            "Seri Alkitab Bercerita tayang setiap Jumat & Sabtu jam 19.00 WIB. Seri lengkapnya juga ada di YouTube: "
            "Alkitab Bercerita.\n\n"
            "Ayat dikutip dari Alkitab Terjemahan Baru © LAI 1974. Ilustrasi dan suara narator dibuat dengan bantuan AI.\n\n"
            + TAGAR.format(tag=ep["tag"]) + " #Reels")


def cap_pendukung(ep, berikut):
    poin = "\n\n".join(f"{i + 1}. {p['judul']}\n{p['ayat']} ({p['ref']})\n{p['isi']}" for i, p in enumerate(ep["pelajaran"]))
    return (f"{ep['nama']}: 3 hal dari kisah ini 📖\n\n{poin}\n\n"
            f"Belum nonton Reels-nya? Ada di postingan sebelum ini 🎬\nBerikutnya, {berikut[0]}: {berikut[1]}.\n\n"
            "Simpan post ini dan kirim ke teman yang perlu diingatkan hari ini 🤍\n\n" + TAGAR.format(tag=ep["tag"]))


# ---------- susun ----------

def simpan(img, rel):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(p, "JPEG", quality=92)
    return rel


def berikutnya(idx):
    tgl = date.fromisoformat(JADWAL_AB[idx][0])
    if idx + 1 < len(JADWAL_AB):
        t2, s2 = JADWAL_AB[idx + 1]
        d2 = date.fromisoformat(t2)
        hari = HARI[d2.weekday()]
        kapan = f"besok, {hari} 19.00 WIB" if (d2 - tgl).days == 1 else f"{hari} depan, 19.00 WIB"
        return kapan, EPISODES[s2]["nama"]
    return "Jumat depan, 19.00 WIB", "Kisah baru dari Alkitab"


def render_ep(idx):
    tgl, slug = JADWAL_AB[idx]
    ep, no = EPISODES[slug], idx + 1
    hari = HARI[date.fromisoformat(tgl).weekday()]
    senin = date.fromisoformat(tgl) - timedelta(days=date.fromisoformat(tgl).weekday())
    minggu_ini = [(t, s) for t, s in JADWAL_AB if senin <= date.fromisoformat(t) < senin + timedelta(days=7)]
    berikut = berikutnya(idx)
    base = f"ab/{slug}"
    g = ep["gambar"]
    print(f"{tgl} {hari}: {ep['nama']}")
    pv = [simpan(cover(ep, no, gambar(ep, g["cover"]), ep["hook"], f"{ep['nama']}  ·  {ep['kitab']}", f"EPISODE {no:02d}",
                       f"REELS MALAM INI  ·  {hari.upper()} 19.00 WIB"), f"{base}/preview_1.jpg"),
          simpan(teaser(ep, no, hari), f"{base}/preview_2.jpg"),
          simpan(kartu_seri(ep, minggu_ini, slug), f"{base}/preview_3.jpg")]
    pd = [simpan(cover(ep, no, gambar(ep, g["pendukung"]), ep["nama"], ep["kitab"], "3 HAL DARI KISAH INI",
                       f"SUDAH TAYANG DI REELS  ·  EPISODE {no:02d}"), f"{base}/pendukung_1.jpg")]
    pd += [simpan(pelajaran(ep, no, i, p, gambar(ep, g["p"][i])), f"{base}/pendukung_{i + 2}.jpg")
           for i, p in enumerate(ep["pelajaran"])]
    pd.append(simpan(penutup(ep, no, berikut), f"{base}/pendukung_5.jpg"))
    s9 = (1080, 1920)
    cov = simpan(cover(ep, no, gambar(ep, g["reels"]), ep["hook"], ep["nama"], f"EPISODE {no:02d}",
                       "ALKITAB BERCERITA  ·  REELS", size=s9, fokus=0.5), f"{base}/cover_reels.jpg")
    st = {"preview": simpan(cover(ep, no, gambar(ep, g["cover"]), ep["hook"], ep["nama"], f"EPISODE {no:02d}",
                                  f"REELS MALAM INI  ·  19.00 WIB", size=s9, fokus=0.5), f"stories/ab-{slug}-preview.jpg"),
          "reels": simpan(cover(ep, no, gambar(ep, g["reels"]), ep["hook"], ep["nama"], "REELS BARU",
                                "TONTON SEKARANG DI FEED", size=s9, fokus=0.5), f"stories/ab-{slug}-reels.jpg"),
          "pendukung": simpan(cover(ep, no, gambar(ep, g["pendukung"]), ep["nama"], "3 hal dari kisah ini",
                                    "POST BARU", "GESER UNTUK 3 PELAJARAN", size=s9, fokus=0.5),
                              f"stories/ab-{slug}-pendukung.jpg")}
    kompres(SUMBER / ep["dir"] / ep["video"], OUT / base / "reels.mp4")
    items = []
    for jenis, files, caption in (("preview", pv, cap_preview(ep, hari)), ("reels", [f"{base}/reels.mp4"], cap_reels(ep)),
                                  ("pendukung", pd, cap_pendukung(ep, berikut))):
        waktu = datetime.fromisoformat(f"{tgl}T{JAM[jenis]}:00+07:00")
        it = {"id": f"ab-{slug}-{jenis}", "akun": "tenang", "seri": "alkitab-bercerita", "waktu": waktu.isoformat(),
              "files": files, "caption": caption}
        if jenis == "reels":
            it["cover"] = cov
        items.append(it)
        items.append({"id": f"story-ab-{slug}-{jenis}", "akun": "tenang", "seri": "alkitab-bercerita", "story": True,
                      "waktu": (waktu + timedelta(minutes=10)).isoformat(), "files": [st[jenis]], "caption": ""})
    return items


def terapkan(items):
    """Ganti item seri ini di jadwal dengan isi state/alkitab_bercerita.json."""
    if not STATE.exists():
        return items
    seri = json.loads(STATE.read_text())
    return [it for it in items if it.get("seri") != "alkitab-bercerita"] + seri


def pratinjau(items, rel="preview_alkitab_bercerita.jpg"):
    posts = [it for it in items if not it.get("story")]
    tw, th = 216, 270
    kolom = 5
    rows = []
    for it in posts:
        fs = it["files"] if not it["files"][0].endswith(".mp4") else [it["cover"]]
        rows.append(fs)
    sheet = Image.new("RGB", (tw * kolom, th * len(rows)), "white")
    for r, fs in enumerate(rows):
        for c, f in enumerate(fs[:kolom]):
            im = Image.open(OUT / f).convert("RGB")
            im = isi(OUT / f, tw - 4, th - 4, 0.5) if im.height / im.width > 1.4 else im.resize((tw - 4, th - 4))
            sheet.paste(im, (c * tw + 2, r * th + 2))
    sheet.save(OUT / rel, quality=85)
    return rel


def main():
    pilih = set(sys.argv[1:])
    lama = {it["id"]: it for it in json.loads(STATE.read_text())} if STATE.exists() else {}
    semua = []
    for idx, (tgl, slug) in enumerate(JADWAL_AB):
        if pilih and slug not in pilih:
            semua += [it for i, it in lama.items() if i.startswith((f"ab-{slug}-", f"story-ab-{slug}-"))]
            continue
        semua += render_ep(idx)
    semua.sort(key=lambda x: x["waktu"])
    STATE.write_text(json.dumps(semua, ensure_ascii=False, indent=1))
    jadwal_path = OUT / "schedule.json"
    jadwal = sorted(terapkan(json.loads(jadwal_path.read_text())), key=lambda x: x["waktu"])
    jadwal_path.write_text(json.dumps(jadwal, ensure_ascii=False, indent=2))
    print(f"{len([i for i in semua if not i.get('story')])} post + {len([i for i in semua if i.get('story')])} story "
          f"-> output/schedule.json. Pratinjau: output/{pratinjau(semua)}")


if __name__ == "__main__":
    main()
