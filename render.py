"""Bikin semua gambar (JPEG 1080x1350) + output/schedule.json untuk auto-post.
Jalankan: python3 render.py"""
import json
import re
from datetime import date, datetime, timedelta
from io import BytesIO
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import config
from konten import eli, kapi, tenang

ROOT = Path(__file__).parent
OUT = ROOT / "output"
W, H = 1080, 1350
NAVY, GOLD, PAPER, SKIN, BLUSH = "#1E3A5F", "#C9A84C", "#FEFCF8", "#F7E4CF", "#F6B8C4"
# warna Eli (bisa diganti tema, lihat cerita.apply_theme)
INK, ELI_HAIR, ELI_PANTS, BIBLE = NAVY, NAVY, NAVY, NAVY


# ---------- helpers ----------

def font(key, size):
    f = config.FONT[key]
    if isinstance(f, tuple):
        return ImageFont.truetype(f[0], size, index=f[1])
    return ImageFont.truetype(f, size)


def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def svg_layer(body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    return Image.open(BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")


def grain(img, strength=0.22):
    noise = Image.effect_noise(img.size, 40).point(lambda v: int(128 + (v - 128) * strength)).convert("RGB")
    return ImageChops.add(img, noise, scale=1, offset=-128)


def mix(c1, c2, t):
    a, b = Image.new("RGB", (1, 1), c1).getpixel((0, 0)), Image.new("RGB", (1, 1), c2).getpixel((0, 0))
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def luminance(hex_color):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = Image.new("RGB", (1, 1), hex_color).getpixel((0, 0))
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def readable(fg, bg, minimum=4.5):
    """Kembalikan fg kalau cukup kontras; kalau tidak, krem atau hitam (mana yang lebih kontras)."""
    if contrast(fg, bg) >= minimum:
        return fg
    return max(("#F4F1EA", "#111111"), key=lambda c: contrast(c, bg))


def is_dark(hex_color):
    r, g, b = Image.new("RGB", (1, 1), hex_color).getpixel((0, 0))
    return 0.299 * r + 0.587 * g + 0.114 * b < 140


def save(img, rel):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=92)
    return rel


# ---------- akun 1: Eli ----------

ELI_FACE = {
    "senyum": ('<circle cx="-8" cy="-111" r="2.6" fill="{N}"/><circle cx="8" cy="-111" r="2.6" fill="{N}"/>'
               '<path d="M-6,-101 Q0,-95 6,-101" fill="none" stroke="{N}" stroke-width="1.8" stroke-linecap="round"/>'),
    "bingung": ('<circle cx="-7" cy="-114" r="2.6" fill="{N}"/><circle cx="9" cy="-114" r="2.6" fill="{N}"/>'
                '<path d="M-3,-101 L4,-102" fill="none" stroke="{N}" stroke-width="1.6" stroke-linecap="round"/>'),
    "merem": ('<path d="M-11,-111 Q-8,-108 -5,-111 M5,-111 Q8,-108 11,-111" fill="none" stroke="{N}" stroke-width="1.8" stroke-linecap="round"/>'
              '<path d="M-4,-100 Q0,-98 4,-100" fill="none" stroke="{N}" stroke-width="1.6" stroke-linecap="round"/>'),
    "sedih": ('<circle cx="-8" cy="-109" r="2.6" fill="{N}"/><circle cx="8" cy="-109" r="2.6" fill="{N}"/>'
              '<path d="M-13,-117 L-5,-119 M5,-119 L13,-117" fill="none" stroke="{N}" stroke-width="1.6" stroke-linecap="round"/>'
              '<path d="M-5,-99 Q0,-103 5,-99" fill="none" stroke="{N}" stroke-width="1.8" stroke-linecap="round"/>'),
    "gembira": ('<path d="M-11,-110 Q-8,-115 -5,-110 M5,-110 Q8,-115 11,-110" fill="none" stroke="{N}" stroke-width="1.8" stroke-linecap="round"/>'
                '<path d="M-7,-102 Q0,-93 7,-102 Z" fill="#C0485A" stroke="{N}" stroke-width="1.4" stroke-linejoin="round"/>'),
}


def eli_fig(face, arms, piyama=False, duduk=False):
    """Eli dalam koordinat dasar (kaki di y=0, tinggi ~148).
    arms: alkitab | dagu | doa | bawah | atas | pangku"""
    shirt = "#E3ECFA" if piyama else "#FFFFFF"
    pants = "#8FA9D6" if piyama else ELI_PANTS
    arm = lambda d: (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="{d}" fill="none" stroke="{shirt}" stroke-width="4" stroke-linecap="round"/>')
    hand = lambda x, y, r=3.2: f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKIN}" stroke="{INK}" stroke-width="1.4"/>'
    bible = lambda x, y, w, h: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{BIBLE}"/>'
                                f'<path d="M{x + w / 2},{y + 3} L{x + w / 2},{y + h - 4} M{x + w / 2 - 4},{y + h * 0.35} L{x + w / 2 + 4},{y + h * 0.35}" '
                                f'stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>')
    if duduk:
        legs = (f'<path d="M-16,-40 Q-46,-36 -44,-13 Q-42,0 0,-2 Q42,0 44,-13 Q46,-36 16,-40 Z" fill="{pants}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
                f'<ellipse cx="-30" cy="-6" rx="7" ry="3.5" fill="{ELI_HAIR}"/><ellipse cx="30" cy="-6" rx="7" ry="3.5" fill="{ELI_HAIR}"/>')
        dy = 5
    else:
        legs = (f'<path d="M-14,-45 L-15,-5 L-4,-5 L-1,-30 L1,-30 L4,-5 L15,-5 L14,-45 Z" fill="{pants}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
                f'<ellipse cx="-10" cy="-3" rx="7" ry="3.2" fill="{ELI_HAIR}"/><ellipse cx="10" cy="-3" rx="7" ry="3.2" fill="{ELI_HAIR}"/>')
        dy = 0
    upper = f'''
<path d="M-17,-88 Q-20,-62 -16,-43 L16,-43 Q20,-62 17,-88 Q0,-94 -17,-88 Z" fill="{shirt}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>
<path d="M-6,-90 L0,-83 L6,-90" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>
<circle cx="0" cy="-74" r="1.2" fill="{INK}"/><circle cx="0" cy="-64" r="1.2" fill="{INK}"/><circle cx="0" cy="-54" r="1.2" fill="{INK}"/>
<circle cx="0" cy="-112" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>
<path d="M-22.5,-112 Q-25,-139 0,-137 Q25,-139 22.5,-112 Q16,-124 4,-121 Q-8,-128 -22.5,-112 Z" fill="{ELI_HAIR}"/>
<path d="M1,-136 Q4,-148 12,-144" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="-13" cy="-103" rx="4" ry="2.4" fill="{BLUSH}"/><ellipse cx="13" cy="-103" rx="4" ry="2.4" fill="{BLUSH}"/>'''
    upper += ELI_FACE[face].format(N=INK)
    upper += {
        "alkitab": arm("M-16,-84 Q-24,-72 -9,-66") + arm("M16,-84 Q24,-72 9,-66") + bible(-11, -78, 22, 18) + hand(-10, -66) + hand(10, -66),
        "dagu": arm("M16,-84 Q26,-80 12,-96") + hand(11, -97, 3.4) + arm("M-16,-84 Q-22,-68 -20,-56") + bible(-28, -60, 14, 18),
        "doa": arm("M-16,-84 Q-20,-70 -3,-78") + arm("M16,-84 Q20,-70 3,-78")
               + f'<path d="M-3,-76 L0,-90 L3,-76 Z" fill="{SKIN}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>',
        "bawah": arm("M-16,-84 Q-22,-70 -21,-56") + hand(-21, -55) + arm("M16,-84 Q22,-70 21,-56") + hand(21, -55),
        "atas": arm("M-16,-84 Q-30,-98 -28,-116") + hand(-28, -118) + arm("M16,-84 Q30,-98 28,-116") + hand(28, -118),
        "pangku": arm("M-16,-84 Q-24,-60 -8,-48") + hand(-7, -48) + arm("M16,-84 Q24,-60 8,-48") + hand(7, -48),
    }[arms]
    return legs + f'<g transform="translate(0,{dy})">{upper}</g>'


def eli_svg(pose, piyama):
    face, arms = {"gembira": ("senyum", "alkitab"), "merenung": ("bingung", "dagu"), "berdoa": ("merem", "doa")}[pose]
    return eli_fig(face, arms, piyama)


def eli_scene(slot):
    if slot == "pagi":
        rays = "".join(
            f'<line x1="{200 + 72 * c}" y1="{200 + 72 * s}" x2="{200 + 104 * c}" y2="{200 + 104 * s}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>'
            for c, s in [(1, 0), (0.87, 0.5), (0.5, 0.87), (0, 1), (-0.5, 0.87), (-0.87, 0.5), (-1, 0), (-0.87, -0.5), (-0.5, -0.87), (0, -1), (0.5, -0.87), (0.87, -0.5)])
        return f'<circle cx="200" cy="200" r="55" fill="#FBE38E" stroke="{NAVY}" stroke-width="4"/>{rays}'
    if slot == "siang":
        cloud = lambda x, y, k: (f'<path transform="translate({x},{y}) scale({k})" d="M0,0 h130 a28,28 0 0 0 -18,-48 a40,40 0 0 0 -72,-12 a30,30 0 0 0 -40,60 z" '
                                 f'fill="#EAF2FB" stroke="{NAVY}" stroke-width="{4 / k}" stroke-linejoin="round"/>')
        return cloud(140, 260, 1.3) + cloud(330, 170, 0.9)
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{PAPER}"/>' for x, y in [(300, 160), (330, 300), (160, 330), (290, 345), (180, 250)])
    return (f'<rect x="130" y="130" width="240" height="240" fill="#2F55B8" stroke="{NAVY}" stroke-width="4"/>{stars}'
            f'<path d="M190,160 A36,36 0 1 0 222,222 A28,28 0 1 1 190,160 Z" fill="{PAPER}"/>'
            f'<line x1="250" y1="130" x2="250" y2="370" stroke="{PAPER}" stroke-width="10"/><line x1="130" y1="250" x2="370" y2="250" stroke="{PAPER}" stroke-width="10"/>')


BUBBLE_COLOR = {"pagi": "#FBE38E", "siang": "#CFE8D4", "malam": "#F8C9D2"}
POSE = {"pagi": "gembira", "siang": "merenung", "malam": "berdoa"}


def eli_image(slot, bubble, kutipan, ref, show_bubble=True, show_verse=True):
    """Satu gambar Eli. show_bubble/show_verse=False dipakai reels.py untuk animasi bertahap."""
    img = Image.new("RGB", (W, H), PAPER)
    body = (f'<rect x="90" y="90" width="900" height="760" fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>'
            + eli_scene(slot)
            + f'<line x1="130" y1="800" x2="950" y2="800" stroke="{NAVY}" stroke-width="3" opacity="0.35"/>'
            + (f'<ellipse cx="765" cy="235" rx="200" ry="105" fill="{BUBBLE_COLOR[slot]}"/>'
               f'<path d="M650,320 L585,380 L700,328 Z" fill="{BUBBLE_COLOR[slot]}"/>' if show_bubble else "")
            + f'<g transform="translate(470,798) scale(3.2)">{eli_svg(POSE[slot], slot == "malam")}</g>')
    img = Image.alpha_composite(img.convert("RGBA"), svg_layer(body))
    d = ImageDraw.Draw(img)
    if show_bubble:
        f_b = font("tangan", 44)
        lines = wrap(d, bubble, f_b, 310)
        y = 235 - len(lines) * 52 / 2
        for ln in lines:
            d.text((765, y), ln, font=f_b, fill=NAVY, anchor="ma")
            y += 52
    d.text((110, 812), "@" + config.AKUN["eli"]["handle"].upper(), font=font("sans_bold", 22), fill=NAVY)
    if show_verse:
        f_v, f_r = font("serif", 42), font("serif_italic", 32)
        vlines = wrap(d, kutipan, f_v, 860)
        y = 1090 - (len(vlines) * 58 + 62) / 2
        for ln in vlines:
            d.text((540, y), ln, font=f_v, fill=NAVY, anchor="ma")
            y += 58
        d.text((540, y + 22), ref, font=f_r, fill="#8C6D22", anchor="ma")
    return img.convert("RGB")


def eli_text_slide(label, n, total, title, body, number=None, sub=None):
    """Slide teks gaya Eli: label kecil, judul tulisan tangan, isi serif, Eli kecil di pojok."""
    img = Image.new("RGBA", (W, H), PAPER)
    img.alpha_composite(svg_layer(f'<rect x="60" y="60" width="{W - 120}" height="{H - 120}" fill="none" stroke="{NAVY}" stroke-width="3"/>'
                                  f'<g transform="translate(900,1230) scale(1.9)">{eli_fig("senyum", "bawah")}</g>'))
    d = ImageDraw.Draw(img)
    d.text((100, 100), f"{label}  ·  {n}/{total}", font=font("sans_bold", 24), fill=mix(NAVY, PAPER, 0.35))
    y = 330
    if number is not None:
        d.ellipse((100, y, 200, y + 100), fill=NAVY)
        d.text((150, y + 50), str(number), font=font("sans_bold", 54), fill=PAPER, anchor="mm")
        y += 140
    for ln in wrap(d, title, font("tangan", 66), 860):
        d.text((100, y), ln, font=font("tangan", 66), fill=NAVY)
        y += 82
    y += 24
    for ln in wrap(d, body, font("serif", 44), 800):
        d.text((100, y), ln, font=font("serif", 44), fill=NAVY)
        y += 62
    if sub:
        d.text((100, y + 20), sub, font=font("serif_italic", 32), fill="#8C6D22")
    d.text((100, H - 110), "@" + config.AKUN["eli"]["handle"].upper(), font=font("sans_bold", 22), fill=NAVY)
    return img


ELI_LABEL = {
    "id": {"belajar": "ELI BELAJAR", "geser": "Geser untuk tahu jawabannya  ›", "tips": "TIPS DARI ELI", "tips_pre": "Tips dari Eli: ",
           "tips_geser": "Geser untuk lihat tipsnya  ›", "tips_tutup": "Coba ya! Eli doakan kamu.", "kuis": "Kuis Alkitab!",
           "jawab": "jawab di komentar ya!"},
    "en": {"belajar": "ELI LEARNS", "geser": "Swipe for the answer  ›", "tips": "FROM ELI", "tips_pre": "",
           "tips_geser": "Swipe to see  ›", "tips_tutup": "Eli is praying for you!", "kuis": "Bible Quiz!",
           "jawab": "answer in the comments!"},
}


def eli_edukasi(e, idx, folder="eli", lang="id"):
    lb = ELI_LABEL[lang]
    total = 2 + len(e["jawab"])
    slides = [eli_image("siang", e["tanya"], lb["geser"], lb["belajar"])]
    slides += [eli_text_slide(lb["belajar"], n, total, t, b) for n, (t, b) in enumerate(e["jawab"], 2)]
    slides.append(eli_image("pagi", e["tutup"], e["ayat"], e["ref"]))
    return [save(im, f"{folder}/edukasi{idx + 1}_{n}.jpg") for n, im in enumerate(slides, 1)]


def eli_saran(t, idx, folder="eli", lang="id"):
    lb = ELI_LABEL[lang]
    total = 2 + len(t["tips"])
    judul = lb["tips_pre"] + (t["judul"].lower() if lang == "id" else t["judul"])
    slides = [eli_image("pagi", judul + ("!" if lang == "id" else ""), lb["tips_geser"], lb["tips"])]
    slides += [eli_text_slide(lb["tips"], n, total, jd, isi, number=n - 1) for n, (jd, isi) in enumerate(t["tips"], 2)]
    slides.append(eli_image("malam", t.get("tutup", lb["tips_tutup"]), t["ayat"], t["ref"]))
    return [save(im, f"{folder}/saran{idx + 1}_{n}.jpg") for n, im in enumerate(slides, 1)]


def eli_kuis(q, idx, folder="eli", lang="id"):
    lb = ELI_LABEL[lang]
    img = Image.new("RGBA", (W, H), PAPER)
    img.alpha_composite(svg_layer(
        f'<rect x="90" y="90" width="900" height="600" fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>'
        f'<line x1="130" y1="660" x2="950" y2="660" stroke="{NAVY}" stroke-width="3" opacity="0.35"/>'
        f'<ellipse cx="720" cy="250" rx="210" ry="100" fill="#FBE38E"/><path d="M620,330 L560,390 L660,338 Z" fill="#FBE38E"/>'
        f'<g transform="translate(360,658) scale(2.9)">{eli_fig("bingung", "dagu")}</g>'))
    d = ImageDraw.Draw(img)
    d.text((720, 212), lb["kuis"], font=font("tangan", 56), fill=NAVY, anchor="ma")
    d.text((110, 668), "@" + config.AKUN["eli"]["handle"].upper(), font=font("sans_bold", 22), fill=NAVY)
    y = 740
    for ln in wrap(d, q["tanya"], font("tangan", 56), 900):
        d.text((W / 2, y), ln, font=font("tangan", 56), fill=NAVY, anchor="ma")
        y += 70
    y += 20
    for i, opt in enumerate(q["pilihan"]):
        top = y + i * 118
        d.rounded_rectangle((140, top, W - 140, top + 96), radius=48, fill="#DCE7F7", outline=NAVY, width=3)
        d.ellipse((160, top + 14, 228, top + 82), fill=NAVY)
        d.text((194, top + 48), "ABC"[i], font=font("sans_bold", 36), fill=PAPER, anchor="mm")
        d.text((260, top + 48), opt, font=font("serif", 42), fill=NAVY, anchor="lm")
    d.text((W / 2, H - 70), lb["jawab"], font=font("tangan", 36), fill=mix(NAVY, PAPER, 0.3), anchor="ma")
    return [save(img, f"{folder}/kuis{idx + 1}.jpg")]


def render_eli_variasi(modul="eli_variasi", folder="eli", lang="id"):
    """{(hari, slot): (files, caption)} untuk konten/eli_variasi.py (atau minggu lain dengan skema sama)."""
    import importlib
    ev = importlib.import_module(f"konten.{modul}")
    out = {}
    for hari, slots in ev.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "edukasi":
                out[(hari, slot)] = (eli_edukasi(ev.EDUKASI[idx], idx, folder, lang), ev.EDUKASI[idx]["caption"] + "\n.\n.\n" + ev.TAGS)
            elif fmt == "saran":
                out[(hari, slot)] = (eli_saran(ev.SARAN[idx], idx, folder, lang), ev.SARAN[idx]["caption"] + "\n.\n.\n" + ev.TAGS)
            elif fmt == "kuis" and lang == "en":
                q = ev.KUIS[idx]
                cap = (f"Bible Quiz with Eli! 🤔\n\n{q['tanya']}\nA. {q['pilihan'][0]}\nB. {q['pilihan'][1]}\nC. {q['pilihan'][2]}\n\n"
                       f"Answer A, B or C in the comments 👇 No peeking!\n.\n.\n.\n.\n.\nAnswer: {q['jawab']}\n.\n.\n{ev.TAGS}")
                out[(hari, slot)] = (eli_kuis(q, idx, folder, lang), cap)
            elif fmt == "kuis":
                q = ev.KUIS[idx]
                cap = (f"Kuis Alkitab dari Eli! 🤔\n\n{q['tanya']}\nA. {q['pilihan'][0]}\nB. {q['pilihan'][1]}\nC. {q['pilihan'][2]}\n\n"
                       f"Jawab A, B, atau C di komentar 👇 Jangan intip jawabannya dulu!\n.\n.\n.\n.\n.\nJawaban: {q['jawab']}\n.\n.\n{ev.TAGS}")
                out[(hari, slot)] = (eli_kuis(q, idx), cap)
            elif fmt == "payung":
                out[(hari, slot)] = (["contoh/reel_payung.mp4"], (OUT / "contoh/reel_payung_caption.txt").read_text())
    return out


def render_eli_tambahan():
    """Gambar untuk slot tambahan Eli (konten/eli_tambahan.py); post dengan 'file' memakai file yang sudah ada."""
    from konten import eli_tambahan
    return [save(eli_image(p["adegan"], p["balon"], p["kutipan"], p["ref"]), f"eli/hari{p['hari']}_{p['slot']}.jpg")
            for p in eli_tambahan.POSTS if "file" not in p]


def render_eli():
    return [save(eli_image(*post), f"eli/hari{i // 3 + 1}_{post[0]}.jpg") for i, post in enumerate(eli.POSTS)]


# ---------- akun 2: quote carousel ----------

PALET = {
    "coklat": ("#3B3129", "#F4EEE6", "#C9A84C"),
    "krem": ("#CFC2B0", "#2B2620", "#6B5530"),
    "hitam": ("#121212", "#F2F2F2", "#C9A84C"),
    "hijau": ("#1F4A35", "#F1EFE6", "#D9C27A"),
}


def slide(bg, fg, accent, handle, blocks):
    """blocks: list of (teks, font, warna). teks '' = jeda."""
    img = grain(Image.new("RGB", (W, H), bg))
    d = ImageDraw.Draw(img)
    rows = []
    for text, fnt, color in blocks:
        if text == "":
            rows.append((None, fnt, color, int(fnt.size * 0.8)))
            continue
        for ln in wrap(d, text, fnt, 800):
            rows.append((ln, fnt, color, int(fnt.size * 1.45)))
    maxw = max(d.textlength(r[0], font=r[1]) for r in rows if r[0])
    x = (W - maxw) / 2
    y = (H - sum(r[3] for r in rows)) / 2
    for text, fnt, color, lh in rows:
        if text:
            d.text((x, y), text, font=fnt, fill=color)
        y += lh
    d.text((70, H - 80), "@" + handle, font=font("sans_bold", 22), fill=mix(fg, bg, 0.45))
    return img


def hook_font(text, maxw=800, size=46):
    """Hook diulang 4x harus muat satu baris: kecilkan huruf kalau perlu."""
    while size > 30 and font("serif", size).getlength(text) > maxw:
        size -= 2
    return font("serif", size)


EDITORIAL = {  # warna di konten/tenang.py -> (latar, teks, aksen)
    "coklat": ("#F3EDE3", "#2A2420", "#A0522D"),
    "krem": ("#EEF0E8", "#23291F", "#5E7F63"),
    "hitam": ("#141414", "#F2EEE6", "#C9A84C"),
    "hijau": ("#1F3B2D", "#F1EFE6", "#D9C27A"),
}


def render_tenang_quote_editorial(p, key):
    """Template editorial: rata kiri, label kecil, hook besar sekali (tidak diulang), tanda kutip besar, penutup warna dibalik."""
    handle = config.AKUN["tenang"]["handle"]
    bg, ink, accent = EDITORIAL[p["warna"]]
    dim = mix(ink, bg, 0.45)
    cta = [c.format(handle=handle) for c in p["cta"]]

    label = lambda t: "     ".join(" ".join(w) for w in t.split())  # huruf renggang, jarak antarkata lebar

    def base(n, invert=False):
        b, i, a = (accent, bg, bg) if invert else (bg, ink, accent)
        img = grain(Image.new("RGB", (W, H), b), 0.12)
        d = ImageDraw.Draw(img)
        d.text((90, 90), label("DIAM & PERCAYA"), font=font("sans_bold", 20), fill=a)
        d.text((W - 90, 90), f"{n} / 5", font=font("sans_bold", 20), fill=mix(i, b, 0.45), anchor="ra")
        d.text((90, H - 100), "@" + handle, font=font("sans_bold", 22), fill=mix(i, b, 0.45))
        return img, d, i, a

    def lines(d, x, y, items, maxw=880):
        for text, fnt, color, gap in items:
            if text:
                for ln in wrap(d, text, fnt, maxw):
                    d.text((x, y), ln, font=fnt, fill=color)
                    y += fnt.size * 1.3
            y += gap
        return y

    files = []
    img, d, i, a = base(1)
    y = lines(d, 90, 430, [(p["hook"], font("serif", 88), i, 40)])
    d.line((90, y, 250, y), fill=a, width=5)
    d.text((W - 90, H - 100), "geser  ›", font=font("sans_bold", 26), fill=i, anchor="ra")
    files.append(img)

    img, d, i, a = base(2)
    y = lines(d, 90, 330, [(label("JUJUR SAJA"), font("sans_bold", 22), a, 40)])
    for t in p["masalah"]:
        if t == "":
            y += 34
            continue
        if t[0].isupper() or t[0] in "“\"":  # kalimat baru dapat tanda —, lanjutan kalimat (huruf kecil) tidak
            d.text((90, y), "—", font=font("serif", 52), fill=a)
        y = lines(d, 160, y, [(t, font("serif", 52), i, 10)], 800)
    files.append(img)

    img, d, i, a = base(3)
    d.text((70, 160), "“", font=font("serif", 320), fill=a)
    y = lines(d, 90, 520, [(p["ayat"].strip("“”"), font("serif_italic", 50), i, 30),
                           (p["ref"].upper(), font("sans_bold", 24), a, 0)])
    files.append(img)

    img, d, i, a = base(4)
    y = lines(d, 90, 360, [(label("RENUNGAN"), font("sans_bold", 22), a, 40)])
    lines(d, 90, y, [(t, font("serif", 58), i, 8) if t else ("", None, i, 36) for t in p["refleksi"]])
    files.append(img)

    img, d, i, a = base(5, invert=True)
    y = lines(d, 90, 480, [(cta[0], font("serif", 72), i, 0), (cta[1], font("serif_italic", 72), i, 40)])
    d.line((90, y, 250, y), fill=i, width=5)
    files.append(img)
    return [save(im, f"{key}_{n}.jpg") for n, im in enumerate(files, 1)], p["caption"].format(handle=handle)


def render_tenang_quote(p, key):
    handle = config.AKUN["tenang"]["handle"]
    f, fi, fs = font("serif", 46), font("serif_italic", 30), font("serif", 42)
    bg, fg, accent = PALET[p["warna"]]
    cta = [c.format(handle=handle) for c in p["cta"]]
    slides = [
        [(p["hook"], hook_font(p["hook"]), fg)] * 4,
        [(t, f, fg) for t in p["masalah"]],
        [(p["ayat"], fs, fg), ("", fs, fg), (p["ref"], fi, accent)],
        [(t, f, fg) for t in p["refleksi"]],
        [(cta[0], f, fg), (cta[1], f, fg)] + ([] if handle in "".join(cta) else [("", f, fg), ("@" + handle, fi, accent)]),
    ]
    files = [save(slide(bg, fg, accent, handle, b), f"{key}_{n}.jpg") for n, b in enumerate(slides, 1)]
    return files, p["caption"].format(handle=handle)


def fbm1d(n, rng, octaves=((6, 1.0), (14, 0.5), (40, 0.22), (120, 0.08))):
    x = np.linspace(0, 1, n)
    return sum(np.interp(x, np.linspace(0, 1, k), rng.uniform(-1, 1, k)) * amp for k, amp in octaves)


def fbm2d(h, w, rng, octaves=((6, 1.0), (14, 0.5), (32, 0.25), (80, 0.12))):
    out = np.zeros((h, w), np.float32)
    for k, amp in octaves:
        small = rng.random((max(2, int(k * h / w)), k)).astype(np.float32)
        out += np.asarray(Image.fromarray(small).resize((w, h), Image.BICUBIC)) * amp
    return out / sum(a for _, a in octaves)


def landscape(kind, w, h=H, seed=7):
    """Pemandangan buatan sendiri (tanpa foto stok): langit, matahari, awan, lalu gunung (fajar) atau laut."""
    rng = np.random.default_rng(seed)
    horizon = 0.62 if kind == "fajar" else 0.58
    top, mid, hor = {"fajar": ((44, 70, 104), (122, 136, 168), (238, 192, 150)),
                     "laut": ((38, 58, 94), (176, 132, 150), (250, 188, 128))}[kind]
    y = np.linspace(0, 1, h)[:, None, None]
    t1 = np.clip(y / (horizon * 0.6), 0, 1)
    t2 = np.clip((y - horizon * 0.6) / (horizon * 0.4), 0, 1)
    sky = np.array(top) * (1 - t1) + np.array(mid) * t1
    sky = sky * (1 - t2) + np.array(hor) * t2
    img = np.broadcast_to(sky, (h, w, 3)).astype(np.float32).copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sun_x, sun_y = w * 0.42, h * horizon - 10
    glow = np.exp(-(((xx - sun_x) ** 2 + (yy - sun_y) ** 2) / (2 * 230.0 ** 2)))[..., None]
    img = img + glow * np.array([255, 214, 160]) * 0.55
    clouds = fbm2d(h, w, rng)
    cmask = np.clip((clouds - 0.52) * 3.2, 0, 0.75) * np.clip(1 - yy / (h * horizon * 0.95), 0, 1)
    lit = np.array([246, 226, 214]) * (0.75 + 0.25 * glow)
    img = img * (1 - cmask[..., None]) + lit * cmask[..., None]
    if kind == "fajar":
        dark = np.array([34, 40, 62])
        for i, (base, amp, haze) in enumerate([(0.60, 70, 0.55), (0.68, 90, 0.3), (0.78, 110, 0.0)]):
            ridge = h * base + fbm1d(w, rng) * amp
            color = np.array(hor) * haze + dark * (1 - haze) * (0.8 + 0.1 * i)
            below = (yy > ridge[None, :])[..., None]
            img = np.where(below, color, img)
    else:
        hy = int(h * horizon)
        wy = np.linspace(0, 1, h - hy)[:, None, None]
        water = np.array(hor) * 0.75 * (1 - wy) + np.array([30, 46, 76]) * wy
        img[hy:] = np.broadcast_to(water, (h - hy, w, 3))
        lines = (rng.random((260, 14)) * 255).astype(np.uint8)   # banyak baris, sedikit kolom -> garis ombak mendatar
        streaks = np.asarray(Image.fromarray(lines).resize((w, h - hy), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5))) / 255.0
        refl = np.exp(-((xx[hy:] - sun_x) ** 2) / (2 * (70 + (yy[hy:] - hy) * 0.6) ** 2))
        img[hy:] += (refl * np.clip(streaks - 0.4, 0, 1) * 1.8)[..., None] * np.array([255, 214, 160])
        img[hy:hy + 3] = np.array(hor) * 1.05
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img)


def notif(layer, y, sender, message, letter, when="sekarang", width=900):
    """Kartu notifikasi pesan ala lock screen. Mengembalikan tingginya."""
    d = ImageDraw.Draw(layer)
    x = (layer.width - width) // 2
    f_msg, f_name, f_time = font("sans", 34), font("sans_bold", 34), font("sans", 28)
    lines = wrap(d, message, f_msg, width - 180)
    hgt = 84 + len(lines) * 44 + 12
    d.rounded_rectangle((x, y, x + width, y + hgt), radius=38, fill=(30, 30, 32, 215))
    d.ellipse((x + 28, y + 26, x + 112, y + 110), fill=(150, 150, 156, 255))
    d.text((x + 70, y + 68), letter, font=font("sans_bold", 40), fill="#FFFFFF", anchor="mm")
    d.ellipse((x + 88, y + 86, x + 118, y + 116), fill=(52, 199, 89, 255), outline=(30, 30, 32, 255), width=3)
    d.text((x + 136, y + 26), sender, font=f_name, fill="#FFFFFF")
    d.text((x + width - 32, y + 30), when, font=f_time, fill=(165, 165, 170), anchor="ra")
    for i, ln in enumerate(lines):
        d.text((x + 136, y + 74 + i * 44), ln, font=f_msg, fill="#FFFFFF")
    return hgt


def render_tenang_notif(p, key, seed=1):
    handle = config.AKUN["tenang"]["handle"]
    pano = landscape(p["adegan"], W * 4, seed=seed)   # satu panorama, dipotong 4 -> geser terasa menyambung
    files = []
    for n in range(4):
        img = grain(pano.crop((n * W, 0, (n + 1) * W, H)), 0.18).convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if n < 3:
            notif(layer, 560, "Tuhan", p["pesan"][n], "T")
        else:
            y = 250
            for i, msg in enumerate(p["pesan"]):
                y += notif(layer, y, "Tuhan", msg, "T", when=f"{3 - i} mnt lalu" if i < 2 else "sekarang") + 18
            notif(layer, y + 30, "Alkitab", f'{p["ayat"]} — {p["ref"]}', "A")
        img.alpha_composite(layer)
        ImageDraw.Draw(img).text((70, H - 80), "@" + handle, font=font("sans_bold", 22), fill=(255, 255, 255, 190))
        files.append(save(img, f"{key}_{n + 1}.jpg"))
    return files, p["caption"]


def render_tenang_warna(p, key):
    handle = config.AKUN["tenang"]["handle"]
    fg = readable(p["fg"], p["bg"])
    img = grain(Image.new("RGB", (W, H), p["bg"]), 0.12)
    d = ImageDraw.Draw(img)
    f = font("sans_medium", 52)
    rows = []
    for t in p["teks"]:
        rows += [("", 30)] if t == "" else [(ln, 70) for ln in wrap(d, t, f, 900)]
    y = H * 0.47 - sum(r[1] for r in rows) / 2
    for text, lh in rows:
        if text:
            d.text((90, y), text, font=f, fill=fg)
        y += lh
    d.text((70, H - 80), "@" + handle, font=font("sans_bold", 22), fill=mix(fg, p["bg"], 0.4))
    return [save(img, f"{key}_1.jpg")], p["caption"]


def dinding_layers(p, size=(W, H), fsize=44, seed=5):
    """Dinding teks: (latar dengan semua teks gelap, [(sprite kata menyala, posisi)] urut pesan)."""
    w, h = size
    rng = np.random.default_rng(seed)
    f = font("condensed", fsize)
    lh = int(fsize * 1.05)
    base = grain(Image.new("RGB", size, p["bg"]), 0.1).convert("RGBA")
    d = ImageDraw.Draw(base)
    words = p["kalimat"].split()
    space = f.getlength(" ")
    rows = []
    for li, y in enumerate(range(-8, h, lh)):
        x = -rng.uniform(0, 260)
        k = int(rng.integers(0, len(words)))
        row = []
        while x < w:
            wd = words[k % len(words)]
            row.append((wd, x, y))
            d.text((x, y), wd, font=f, fill=p["teks"])
            x += f.getlength(wd) + space
            k += 1
        rows.append(row)
    hits, margin = [], 2
    for i, target in enumerate(p["sorot"]):
        want = margin + round(i * (len(rows) - 1 - 2 * margin) / max(1, len(p["sorot"]) - 1))
        for row in rows[want:] + rows[:want]:
            spot = next(((wd, x, y) for wd, x, y in row if wd == target and 60 < x < w - 60 - f.getlength(wd)), None)
            if spot:
                wd, x, y = spot
                sp = text_sprite(wd, f, "#FFFFFF" if is_dark(p["bg"]) else "#111111")
                hits.append((sp, (int(x + f.getbbox(wd)[0] - 4), int(y + f.getbbox(wd)[1] - 4))))
                break
    return base, hits


def render_tenang_dinding(p, key):
    base, hits = dinding_layers(p)
    for sp, pos in hits:
        base.alpha_composite(sp, pos)
    return [save(base, f"{key}_1.jpg")], p["caption"]


def suasana_scene(kind, w, h, seed=11):
    """Latar Reels suasana. Mengembalikan fungsi frame(t) -> Image RGB."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if kind == "kabut":
        top, bot = np.array([46, 52, 60]), np.array([104, 110, 116])
        sky = (top + (bot - top) * (yy / h)[..., None]).astype(np.float32)
        ridge = h * 0.68 + fbm1d(w, rng, ((20, 1.0), (70, 0.6), (200, 0.35))) * 40
        trees = yy > ridge[None, :]
        sky[trees] = sky[trees] * 0.45 + np.array([34, 38, 44]) * 0.55
        ground = yy > h * 0.8
        sky[ground] = np.array([40, 43, 47]) + (yy[ground] - h * 0.8)[..., None] * 0.04
        path = ground & (np.abs(xx - w / 2) < (yy - h * 0.8) * 0.32 + 5)
        sky[path] = sky[path] * 0.7 + np.array([92, 96, 100]) * 0.3
        fx, fy = w / 2, h * 0.8 - 2
        fig = ((xx - fx) ** 2 / 36 + (yy - (fy - 40)) ** 2 / 36 < 1) | ((np.abs(xx - fx) < 7) & (yy > fy - 34) & (yy < fy))
        sky[fig] = [22, 24, 28]
        fogs = [(fbm2d(h, w * 2, rng, ((4, 1.0), (10, 0.5), (24, 0.25))), speed, alpha)
                for speed, alpha in ((14, 0.7), (28, 0.6), (45, 0.5))]

        def frame(t):
            img = sky.copy()
            for fog, speed, alpha in fogs:
                off = int(t * speed) % w
                m = np.clip((fog[:, off:off + w] - 0.28) * 2.2, 0, 1) * alpha * np.clip(yy / h * 1.5, 0.25, 1)
                img = img * (1 - m[..., None]) + np.array([150, 156, 162]) * m[..., None]
            return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        return frame
    top, bot = np.array([6, 9, 22]), np.array([28, 38, 70])
    sky = (top + (bot - top) * (yy / h)[..., None] ** 1.5).astype(np.float32)
    band = np.exp(-(((xx - w * 1.05) * 0.8 + (yy - h * 0.05) * 0.55) ** 2) / (2 * (w * 0.16) ** 2))
    dust = fbm2d(h, w, rng, ((8, 1.0), (20, 0.6), (60, 0.3)))
    sky += (band * np.clip(dust - 0.3, 0, 1) * 1.4)[..., None] * np.array([150, 150, 190])
    n = 900
    sx, sy = rng.uniform(0, w, n), rng.uniform(0, h * 0.8, n)
    size_, phase = rng.choice([1, 1, 1, 2, 2, 3], n), rng.uniform(0, 6.28, n)
    ridge = h * 0.82 + fbm1d(w, rng, ((5, 1.0), (16, 0.4))) * 60
    hills = yy > ridge[None, :]

    def frame(t):
        img = sky.copy()
        tw = 0.55 + 0.45 * np.sin(phase + t * 2.2)
        py = (sy + t * 6) % (h * 0.8)
        for r in (1, 2, 3):
            sel = size_ == r
            for dx in range(-r + 1, r):
                for dy in range(-r + 1, r):
                    if abs(dx) + abs(dy) >= r:
                        continue
                    xi = np.clip(sx[sel].astype(int) + dx, 0, w - 1)
                    yi = np.clip(py[sel].astype(int) + dy, 0, h - 1)
                    img[yi, xi] = np.maximum(img[yi, xi], (255 * tw[sel])[:, None])
        if 8.0 < t < 8.9:  # satu bintang jatuh
            u = (t - 8.0) / 0.9
            hx, hy = w * (0.85 - 0.5 * u), h * (0.08 + 0.18 * u)
            for k in range(60):
                px, py2 = int(hx + k * 5), int(hy - k * 1.8)
                if 0 <= px < w and 0 <= py2 < h:
                    img[max(0, py2 - 1):py2 + 2, max(0, px - 1):px + 2] = np.maximum(
                        img[max(0, py2 - 1):py2 + 2, max(0, px - 1):px + 2], 255 * (1 - k / 60) * (1 - abs(u - 0.5) * 1.6))
        img[hills] = [8, 10, 18]
        return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return frame


def paragraph_layer(lines, w, h, cy, size=44, handle=None):
    """Paragraf putih di tengah (gaya Reels betteryouliving): area gelap lembut + bayangan supaya selalu terbaca."""
    text = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(text)
    f = font("sans_medium", size)
    rows = []
    for ln in lines:
        rows += [("", size * 0.6)] if ln == "" else [(r, size * 1.36) for r in wrap(d, ln, f, 880)]
    block = sum(r[1] for r in rows)
    y = cy - block / 2
    for txt, lh in rows:
        if txt:
            d.text((w / 2, y), txt, font=f, fill=(255, 255, 255, 255), anchor="ma")
        y += lh
    if handle:
        d.text((w / 2, y + 28), " ".join(handle.upper()), font=font("sans_bold", 20), fill=(255, 255, 255, 200), anchor="ma")
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    scrim = np.exp(-(((xx - w / 2) / (w * 0.62)) ** 2 + ((yy - cy) / (block * 0.95 + 120)) ** 2)) * 150
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.putalpha(Image.fromarray(scrim.astype(np.uint8)))
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow.putalpha(text.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda v: min(255, int(v * 1.1))))
    out.alpha_composite(shadow)
    out.alpha_composite(text)
    return out


def render_tenang_suasana(p, key):
    """Gambar diam 4:5 dari Reels suasana (dipakai kalau Reels-nya belum dibuat)."""
    img = suasana_scene(p["adegan"], W, H)(6.0).convert("RGBA")
    img.alpha_composite(paragraph_layer(p["teks"], W, H, H * 0.42, handle=config.AKUN["tenang"]["handle"]))
    return [save(img, f"{key}_1.jpg")], p["caption"]


TENANG_FORMAT = {"A": (render_tenang_quote, "POSTS"), "B": (render_tenang_notif, "NOTIF"), "C": (render_tenang_warna, "WARNA"),
                 "D": (render_tenang_dinding, "DINDING"), "R": (render_tenang_suasana, "SUASANA"),
                 "W": (render_tenang_dinding, "DINDING")}  # W = dinding teks sebagai gambar, tidak diganti Reels
TENANG_REELS = {"B": "notif", "R": "suasana", "D": "dinding"}
TENANG_SUDAH_KLASIK = {"tenang-1-siang"}  # sudah diposting dengan template klasik, jangan diubah  # format yang punya versi Reels (python3 reels.py)


def render_tenang(modul="tenang"):
    """3 post per hari sesuai JADWAL di konten/<modul>.py. Mengembalikan [(hari, slot, format, idx, files, caption)]."""
    import importlib
    m = importlib.import_module(f"konten.{modul}")
    for old in (OUT / modul).glob("*.jpg"):
        old.unlink()
    out = []
    for day, slots in enumerate(m.JADWAL, 1):
        for slot, fmt, idx in slots:
            make, pool = TENANG_FORMAT[fmt]
            key = f"{modul}/hari{day}_{slot}"
            item = getattr(m, pool)[idx]
            if fmt == "A" and config.TENANG_QUOTE_TEMPLATE == "editorial" and f"{modul}-{day}-{slot}" not in TENANG_SUDAH_KLASIK:
                make = render_tenang_quote_editorial
            files, caption = make(item, key, seed=day) if fmt == "B" else make(item, key)
            out.append((day, slot, fmt, idx, files, caption + getattr(m, "KREDIT", "")))
    return out


# ---------- akun 3: Kapi ----------

def kapi_svg(ekspresi, properti):
    B, D, L, BELLY = "#A7764F", "#7A5236", "#3A2A1E", "#C29470"
    props = properti.split("+")
    s = (f'<ellipse cx="-60" cy="-12" rx="38" ry="16" fill="{D}" stroke="{L}" stroke-width="5"/>'
         f'<ellipse cx="60" cy="-12" rx="38" ry="16" fill="{D}" stroke="{L}" stroke-width="5"/>'
         f'<ellipse cx="0" cy="-120" rx="135" ry="112" fill="{B}" stroke="{L}" stroke-width="6"/>'
         f'<ellipse cx="0" cy="-95" rx="80" ry="68" fill="{BELLY}"/>'
         f'<ellipse cx="-72" cy="-300" rx="21" ry="16" fill="{D}" stroke="{L}" stroke-width="5"/>'
         f'<ellipse cx="72" cy="-300" rx="21" ry="16" fill="{D}" stroke="{L}" stroke-width="5"/>'
         f'<ellipse cx="0" cy="-240" rx="102" ry="84" fill="{B}" stroke="{L}" stroke-width="6"/>'
         f'<rect x="-62" y="-228" width="124" height="72" rx="36" fill="#8C603F" stroke="{L}" stroke-width="5"/>'
         f'<ellipse cx="-22" cy="-200" rx="7" ry="5" fill="{L}"/><ellipse cx="22" cy="-200" rx="7" ry="5" fill="{L}"/>'
         f'<ellipse cx="-70" cy="-218" rx="15" ry="8" fill="#F2A0A8" opacity="0.85"/><ellipse cx="70" cy="-218" rx="15" ry="8" fill="#F2A0A8" opacity="0.85"/>')
    stroke = f'fill="none" stroke="{L}" stroke-width="6" stroke-linecap="round"'
    eyes = {
        "senang": f'<circle cx="-48" cy="-262" r="10" fill="{L}"/><circle cx="48" cy="-262" r="10" fill="{L}"/><circle cx="-45" cy="-265" r="3" fill="#fff"/><circle cx="51" cy="-265" r="3" fill="#fff"/>',
        "semangat": f'<path d="M-62,-258 Q-48,-276 -34,-258 M34,-258 Q48,-276 62,-258" {stroke}/>',
        "capek": f'<path d="M-64,-262 L-32,-262 M32,-262 L64,-262" {stroke}/><path d="M-60,-256 Q-48,-248 -36,-256 M36,-256 Q48,-248 60,-256" fill="none" stroke="{L}" stroke-width="3"/>',
        "merem": f'<path d="M-62,-264 Q-48,-252 -34,-264 M34,-264 Q48,-252 62,-264" {stroke}/>',
        "sedih": f'<circle cx="-48" cy="-258" r="9" fill="{L}"/><circle cx="48" cy="-258" r="9" fill="{L}"/><path d="M-66,-280 L-34,-290 M34,-290 L66,-280" {stroke}/>',
    }[ekspresi]
    mouth = {
        "senang": f'<path d="M-14,-172 Q0,-160 14,-172" {stroke}/>',
        "semangat": f'<path d="M-16,-176 Q0,-150 16,-176 Z" fill="#7A2E2E" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>',
        "capek": f'<path d="M-12,-168 L12,-168" {stroke}/>',
        "merem": f'<path d="M-10,-170 Q0,-163 10,-170" {stroke}/>',
        "sedih": f'<path d="M-12,-164 Q0,-174 12,-164" {stroke}/>',
    }[ekspresi]
    s += eyes + mouth
    arm = lambda cx, cy, rot: f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="36" transform="rotate({rot} {cx} {cy})" fill="{B}" stroke="{L}" stroke-width="5"/>'
    if "alkitab" in props:
        s += (f'<rect x="-58" y="-155" width="116" height="84" rx="6" fill="{NAVY}" stroke="{L}" stroke-width="5"/>'
              f'<path d="M0,-145 L0,-84 M-16,-126 L16,-126" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>'
              + arm(-62, -112, 20) + arm(62, -112, -20))
    elif ekspresi == "semangat":
        s += arm(-128, -190, 35) + arm(128, -190, -35)
    else:
        s += arm(-98, -120, 12) + arm(98, -120, -12)
    if "jeruk" in props:
        s += (f'<circle cx="0" cy="-348" r="28" fill="#F59A23" stroke="{L}" stroke-width="5"/>'
              f'<path d="M4,-376 Q22,-396 38,-382 Q22,-370 4,-376 Z" fill="#5BA35B" stroke="{L}" stroke-width="4"/>')
    if "keringat" in props:
        s += f'<path transform="translate(112,-310)" d="M0,0 C-12,18 -14,34 0,36 C14,34 12,18 0,0 Z" fill="#8FD0F5" stroke="{L}" stroke-width="4"/>'
    if "hati" in props:
        s += f'<path transform="translate(140,-340) scale(1.6)" d="M0,8 C-14,-2 -12,-16 -4,-16 C0,-16 0,-12 0,-10 C0,-12 0,-16 4,-16 C12,-16 14,-2 0,8 Z" fill="#E5484D" stroke="{L}" stroke-width="2.5"/>'
    if "bintang" in props:
        star = lambda x, y, k: f'<path transform="translate({x},{y}) scale({k})" d="M0,-20 L5,-5 L20,0 L5,5 L0,20 L-5,5 L-20,0 L-5,-5 Z" fill="#FFD84D" stroke="{L}" stroke-width="{3 / k}" stroke-linejoin="round"/>'
        s += star(-160, -320, 1.3) + star(150, -370, 1) + star(175, -250, 0.8)
    return s


def text_sprite(text, fnt, color):
    """Teks sebagai gambar transparan yang pas dengan hurufnya (untuk ditempel / dianimasikan)."""
    x0, y0, x1, y1 = fnt.getbbox(text)
    img = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4 - x0, 4 - y0), text, font=fnt, fill=color)
    return img


def kapi_parts(p, top):
    """Warna teks, sprite (atas, kata besar, bawah) dan posisinya untuk kanvas lebar 1080."""
    fg = "#FFFFFF" if is_dark(p["bg"]) else "#111111"
    probe = font("tebal", 200)
    big = font("tebal", min(260, int(200 * 900 / probe.getlength(p["besar"]))))
    atas, word, bawah = text_sprite(p["atas"], font("sans_bold", 46), fg), text_sprite(p["besar"], big, fg), text_sprite(p["bawah"], font("sans_bold", 46), fg)
    x0 = (W - word.width) // 2
    ax = x0 + 8 if atas.width <= word.width else (W - atas.width) // 2      # kalimat lebih lebar dari kata besar -> tengah
    bx = x0 + word.width - 8 - bawah.width if bawah.width <= word.width else (W - bawah.width) // 2
    pos = {"atas": (ax, top - 18 - atas.height), "besar": (x0, top), "bawah": (bx, top + word.height + 18)}
    return fg, {"atas": atas, "besar": word, "bawah": bawah}, pos


def kapi_sprite(p, blink=False, k=1.45):  # noqa: E302
    """Kapi sebagai gambar transparan 620x640, kaki di (310, 620)."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="620" height="640"><g transform="translate(310,620) scale({k})">'
           f'{kapi_svg("merem" if blink else p["ekspresi"], p["properti"])}</g></svg>')
    return Image.open(BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")


def kapi_handle(img, p, fg, y):
    d = ImageDraw.Draw(img)
    dim = mix(fg, p["bg"], 0.35)
    d.text((60, y), "@" + config.AKUN["kapi"]["handle"].upper(), font=font("sans_bold", 22), fill=dim)
    d.text((60, y + 28), "©2026", font=font("sans_bold", 20), fill=dim)


def kapi_kata_image(p):
    """Satu post kata besar Kapi (1080x1350)."""
    img = Image.new("RGBA", (W, H), p["bg"])
    fg, parts, pos = kapi_parts(p, 380)
    for key, sp in parts.items():
        img.alpha_composite(sp, pos[key])
    img.alpha_composite(kapi_sprite(p), (560 - 310, 1280 - 620))
    kapi_handle(img, p, fg, H - 96)
    return img


def render_kapi():
    return [save(kapi_kata_image(p), f"kapi/hari{day}.jpg") for day, p in enumerate(kapi.POSTS, 1)]


def kapi_komik(k, idx, folder="kapi"):
    """Komik lucu Kapi: 4 slide, teks di atas, Kapi di bawah, ayat di slide terakhir."""
    fg = "#1A1A1A" if not is_dark(k["bg"]) else "#FFFFFF"
    files = []
    for n, (text, ekspresi, prop) in enumerate(k["slides"], 1):
        img = Image.new("RGBA", (W, H), k["bg"])
        d = ImageDraw.Draw(img)
        d.text((70, 80), k["judul"].upper(), font=font("sans_bold", 24), fill=mix(fg, k["bg"], 0.4))
        d.text((W - 70, 80), f"{n}/{len(k['slides'])}", font=font("sans_bold", 24), fill=mix(fg, k["bg"], 0.4), anchor="ra")
        y = 230
        f = font("sans_bold", 62)
        for ln in wrap(d, text, f, 900):
            d.text((W / 2, y), ln, font=f, fill=fg, anchor="ma")
            y += 80
        if n == len(k["slides"]):
            y += 24
            fi = font("serif_italic", 32)
            for ln in wrap(d, k["ayat"], fi, 880):
                d.text((W / 2, y), ln, font=fi, fill=mix(fg, k["bg"], 0.25), anchor="ma")
                y += 44
        img.alpha_composite(kapi_sprite({"ekspresi": ekspresi, "properti": prop}), (540 - 310, 1250 - 620))
        kapi_handle(img, k, fg, H - 96)
        files.append(save(img, f"{folder}/komik{idx + 1}_{n}.jpg"))
    return files


def kapi_pilih(p, idx, folder="kapi"):
    """Post 'pilih satu': dua pilihan A/B, dijawab di komentar."""
    fg = "#FFFFFF" if is_dark(p["bg"]) else "#111111"
    img = Image.new("RGBA", (W, H), p["bg"])
    d = ImageDraw.Draw(img)
    d.text((W / 2, 150), "P I L I H     S A T U", font=font("sans_bold", 38), fill=fg, anchor="ma")
    box = mix(p["bg"], fg, 0.14)
    for i, (label, text) in enumerate((("A", p["a"]), ("B", p["b"]))):
        top = 290 + i * 270
        d.rounded_rectangle((110, top, W - 110, top + 180), radius=36, fill=box)
        d.ellipse((150, top + 45, 240, top + 135), fill=fg)
        d.text((195, top + 90), label, font=font("tebal", 52), fill=p["bg"], anchor="mm")
        d.text((280, top + 90), text, font=font("sans_bold", 56), fill=fg, anchor="lm")
    d.text((W / 2, 492), "atau", font=font("serif_italic", 40), fill=mix(fg, p["bg"], 0.35), anchor="mm")
    d.text((W / 2, 790), "jawab A atau B di komentar", font=font("sans", 36), fill=mix(fg, p["bg"], 0.25), anchor="ma")
    img.alpha_composite(kapi_sprite({"ekspresi": p["ekspresi"], "properti": "none"}, k=1.1), (540 - 310, 1300 - 620))
    kapi_handle(img, p, fg, H - 96)
    return [save(img, f"{folder}/pilih{idx + 1}.jpg")]


def render_kapi_tambahan(modul="kapi_tambahan", folder="kapi"):
    """Semua post tambahan Kapi -> {(hari, slot): (files, caption, reel_rel_atau_None)}."""
    import importlib
    kt = importlib.import_module(f"konten.{modul}")
    out = {}
    for hari, slots in kt.JADWAL.items():
        for slot, (fmt, idx) in slots.items():
            if fmt == "kata":
                p = kt.KATA[idx]
                out[(hari, slot)] = ([save(kapi_kata_image(p), f"{folder}/kata{idx + 1}.jpg")], p["caption"], None)
            elif fmt == "reel":
                p = kt.KATA[idx]
                image = save(kapi_kata_image(p), f"{folder}/kata{idx + 1}.jpg")
                out[(hari, slot)] = ([image], p["caption"], f"reels/{folder}/kata{idx + 1}.mp4")
            elif fmt == "komik":
                k = kt.KOMIK[idx]
                out[(hari, slot)] = (kapi_komik(k, idx, folder), k["caption"], None)
            elif fmt == "pilih":
                p = kt.PILIH[idx]
                out[(hari, slot)] = (kapi_pilih(p, idx, folder), p["caption"], None)
            elif fmt == "wallpaper":
                wp = OUT / f"kapi/wallpaper_{kapi.WALLPAPER['nama']}"
                files = [f"kapi/wallpaper_{kapi.WALLPAPER['nama']}/slide_{n}.jpg" for n in range(1, 6)]
                cap = (wp / "caption.txt").read_text() if (wp / "caption.txt").exists() else ""
                out[(hari, slot)] = (files, cap, None)
    return out


def render_kapi_wallpapers():
    """Set wallpaper Kapi: 5 slide carousel 4:5 + 5 wallpaper HP 9:16 + caption & teks DM."""
    wp = kapi.WALLPAPER
    handle = config.AKUN["kapi"]["handle"]
    folder = f"kapi/wallpaper_{wp['nama']}"
    slides, walls = [], []
    total = len(wp["desain"])
    for i, p in enumerate(wp["desain"], 1):
        for kind, (w, h, top, feet, label_y, handle_y) in {"slide": (W, H, 380, 1280, 50, H - 96),
                                                           "wallpaper": (W, 1920, 820, 1690, None, 1760)}.items():
            img = Image.new("RGBA", (w, h), p["bg"])
            fg, parts, pos = kapi_parts(p, top)
            for key, sp in parts.items():
                img.alpha_composite(sp, pos[key])
            img.alpha_composite(kapi_sprite(p), (560 - 310, feet - 620))
            if kind == "slide":
                kapi_handle(img, p, fg, handle_y)
                ImageDraw.Draw(img).text((W - 60, label_y), f"WALLPAPER {i}/{total}", font=font("sans_bold", 22),
                                         fill=mix(fg, p["bg"], 0.35), anchor="ra")
                slides.append(save(img, f"{folder}/slide_{i}.jpg"))
            else:
                ImageDraw.Draw(img).text((w / 2, handle_y), "@" + handle.upper(), font=font("sans_bold", 22),
                                         fill=mix(fg, p["bg"], 0.35), anchor="ma")
                walls.append(save(img, f"{folder}/wallpaper_{i}.jpg"))
    (OUT / folder / "caption.txt").write_text(wp["caption"].format(kata_kunci=wp["kata_kunci"], handle=handle) + "\n.\n.\n" + kapi.TAGS)
    (OUT / folder / "dm.txt").write_text(wp["dm"].format(handle=handle))
    return slides, walls


# ---------- foto profil (1080x1080, aman untuk crop lingkaran) ----------

def render_profil():
    S = 1080
    layer = lambda body: Image.open(BytesIO(cairosvg.svg2png(bytestring=(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">{body}</svg>').encode()))).convert("RGBA")
    files = []

    eli_img = Image.new("RGBA", (S, S), "#CFE3F7")
    eli_img = Image.alpha_composite(eli_img, layer(f'<g transform="translate(540,1560) scale(8.5)">{eli_svg("gembira", False)}</g>'))
    files.append(save(eli_img, "profil/eli.jpg"))

    ten = grain(Image.new("RGB", (W, H), "#3B3129")).crop((0, 0, S, S))
    d = ImageDraw.Draw(ten)
    d.rectangle((533, 300, 547, 780), fill="#F4EEE6")
    d.rectangle((400, 433, 680, 447), fill="#F4EEE6")
    files.append(save(ten, "profil/tenang.jpg"))

    rng = np.random.default_rng(3)
    arr = np.asarray(Image.new("RGB", (S, S), "#F1E6CC")).astype(np.float32) - (fbm2d(S, S, rng, ((3, 1.0), (8, 0.5)))[..., None] - 0.5) * 30
    ayat = grain(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), 0.25).convert("RGBA")
    book = (f'<path d="M540,420 Q420,360 280,380 L280,690 Q420,670 540,730 Z" fill="#FBF3E0" stroke="#3B2A1A" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M540,420 Q660,360 800,380 L800,690 Q660,670 540,730 Z" fill="#FBF3E0" stroke="#3B2A1A" stroke-width="10" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{x0},{y} Q{xm},{y - 18} {x1},{y - 8}" fill="none" stroke="#7A6650" stroke-width="6" stroke-linecap="round"/>'
                      for y in (470, 530, 590) for x0, xm, x1 in ((320, 420, 500), (580, 660, 760)))
            + '<path d="M600,395 L600,520 L625,495 L650,520 L650,388" fill="#9B2C2C" stroke="#3B2A1A" stroke-width="6" stroke-linejoin="round"/>')
    ayat.alpha_composite(layer(book))
    files.append(save(ayat, "profil/ayat.jpg"))

    kap = Image.new("RGBA", (S, S), "#F26B1D")
    kap = Image.alpha_composite(kap, layer(f'<g transform="translate(540,1230) scale(2.6)">{kapi_svg("senang", "jeruk")}</g>'))
    files.append(save(kap, "profil/kapi.jpg"))

    sheet = Image.new("RGB", (len(files) * 340 + 40, 380), "#FFFFFF")
    mask = Image.new("L", (320, 320), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 319, 319), fill=255)
    for i, rel in enumerate(files):
        sheet.paste(Image.open(OUT / rel).resize((320, 320)), (20 + i * 340, 30), mask)
    sheet.save(OUT / "preview_profil.jpg", "JPEG", quality=90)
    return files


# ---------- preview & jadwal ----------

def contact_sheet(rows, name, tw=216):
    th = int(tw * H / W)
    cols = max(len(r) for r in rows)
    sheet = Image.new("RGB", (cols * (tw + 8) + 8, len(rows) * (th + 8) + 8), "#DDDDDD")
    for r, row in enumerate(rows):
        for c, rel in enumerate(row):
            sheet.paste(Image.open(OUT / rel).resize((tw, th)), (8 + c * (tw + 8), 8 + r * (th + 8)))
    sheet.save(OUT / name, "JPEG", quality=88)


CAPTION_MINGGU = """Satu minggu bersama Eli 💛

7 hari, 21 ayat tentang pengharapan. Mana yang paling kena di hatimu minggu ini? Tulis hari dan waktunya di komentar (misal: Hari 3 malam) 👇

Minggu depan Eli datang lagi dengan tema baru ✨

Save video ini buat diputar ulang saat butuh pengingat 🔖
.
.
#renunganharian #ayatalkitab #pengharapan #firmanTuhan #kristenindonesia #reelskristen #sahabateli"""


def reel_or_image(reel_rel, image_rel):
    """Pakai versi Reels kalau sudah dibuat (python3 reels.py), kalau belum pakai gambar."""
    return reel_rel if (OUT / reel_rel).exists() else image_rel


def story_image(rel, handle, name):
    """Versi Story 9:16 dari sebuah post gambar: latar = versi buram gambarnya, gambar di tengah, label kecil."""
    src = Image.open(OUT / rel).convert("RGB")
    bg = src.resize((1080, 1920)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", bg.size, "#000000"), 0.25)
    w = 960
    fg = src.resize((w, int(src.height * w / src.width)))
    y = (1920 - fg.height) // 2 - 40
    bg.paste(fg, ((1080 - w) // 2, y))
    d = ImageDraw.Draw(bg)
    d.text((540, y + fg.height + 50), "post baru di feed  ·  @" + handle, font=font("sans_bold", 30), fill="#FFFFFF", anchor="ma")
    return save(bg, f"stories/{name}.jpg")


def add_stories(items, delay_minutes=10):
    """Satu Story otomatis untuk setiap post feed, 10 menit setelahnya. Reels dipakai langsung (sudah 9:16),
    post gambar/carousel dibuatkan versi 9:16 dari gambar pertamanya. Story tidak bisa diberi link lewat API."""
    stories = []
    for it in items:
        first = it["files"][0]
        when = (datetime.fromisoformat(it["waktu"]) + timedelta(minutes=delay_minutes)).isoformat()
        media = first if first.endswith(".mp4") else story_image(first, config.AKUN[it["akun"]]["handle"], it["id"])
        stories.append({"id": f"story-{it['id']}", "akun": it["akun"], "waktu": when, "files": [media], "story": True, "caption": ""})
    return items + stories


def build_schedule(eli_files, tenang_files, kapi_files):
    """Eli: Reels ayat 3x sehari; hari 7 siang = carousel cerita "Pot" yang bergerak + 1 Reels panjang.
    Kapi: Reels harian. Tenang: carousel quote harian."""
    import cerita  # di sini supaya tidak saling import di awal
    start = date.fromisoformat(config.START_DATE)
    at = lambda day, hhmm: f"{start + timedelta(days=day)}T{hhmm}:00+07:00"
    md = (ROOT / "konten/eli-caption-minggu1.md").read_text()
    eli_caps = [c.strip() for c in re.findall(r"```\n(.*?)```", md, re.S)]
    items = []
    for i, rel in enumerate(eli_files):
        slot, day = eli.POSTS[i][0], i // 3
        if day == 6 and slot == "siang":
            pot = [f"contoh/carousel_pot_{n}.mp4" for n in range(1, 6)]
            if all((OUT / f).exists() for f in pot):
                items.append({"id": "eli-7-cerita-pot", "akun": "eli", "waktu": at(day, config.AKUN["eli"]["jam"][slot]),
                              "files": pot, "caption": cerita.CAPTION_POT})
                continue
        if 1 <= day <= 5 and slot == "siang":
            continue  # hari 2-6 siang diganti kuis / Reels cerita (konten/eli_variasi.py)
        items.append({"id": f"eli-{day + 1}-{slot}", "akun": "eli", "waktu": at(day, config.AKUN["eli"]["jam"][slot]),
                      "files": [reel_or_image(f"reels/eli/hari{day + 1}_{slot}.mp4", rel)], "caption": eli_caps[i]})
    for (hari, slot), (files, caption) in render_eli_variasi().items():  # edukasi, kuis, tips (bukan Reels)
        items.append({"id": f"eli-{hari}-{slot}", "akun": "eli", "waktu": at(hari - 1, config.AKUN["eli"]["jam"][slot]),
                      "files": files, "caption": caption})
    if (OUT / "reels/eli/minggu1_rangkuman.mp4").exists():
        items.append({"id": "eli-7-reels-panjang", "akun": "eli", "waktu": at(6, "18:00"),
                      "files": ["reels/eli/minggu1_rangkuman.mp4"], "caption": CAPTION_MINGGU})
    tenang_weeks = [("tenang", tenang_files, 0)]
    if (ROOT / "konten/tenang_w2.py").exists():
        tenang_weeks.append(("tenang_w2", render_tenang("tenang_w2"), 7))
    if config.TENANG_MINGGU2_AKTIF:  # minggu "Bukan milikku": aktifkan setelah ada izin dari Ps Tulus / IFGF
        tenang_weeks.append(("tenang_minggu2", render_tenang("tenang_minggu2"), 7 * len(tenang_weeks)))
    for modul, week_files, offset in tenang_weeks:
        for day, slot, fmt, idx, rels, caption in week_files:
            if fmt in TENANG_REELS and (fmt != "B" or config.TENANG_NOTIF_REELS):
                reel = f"reels/{modul}/{TENANG_REELS[fmt]}{idx + 1}.mp4"
                if (OUT / reel).exists():
                    rels = [reel]
            items.append({"id": f"{modul}-{day}-{slot}", "akun": "tenang", "waktu": at(offset + day - 1, config.AKUN["tenang"]["jam"][slot]),
                          "files": rels, "caption": caption + "\n.\n.\n" + tenang.TAGS})
    import keren  # Tenang: photo dump, dulu vs sekarang, tipografi sinematik, animasi karakter
    for (hari, slot), (files, caption) in keren.render_keren().items():
        items.append({"id": f"tenang-{hari}-{slot}", "akun": "tenang", "waktu": at(hari - 1, config.AKUN["tenang"]["jam"][slot]),
                      "files": files, "caption": caption + "\n.\n.\n" + tenang.TAGS})
    import akun_baru  # @ayat.tersembunyi
    jam = config.AKUN["ayat"]["jam"]
    fakta = akun_baru.fakta_singkat()  # hari 2-7 pagi: "Fakta 30 detik" (1 slide)
    for i, (path, caption) in enumerate(fakta):
        items.append({"id": f"ayat-fakta-{i + 1}", "akun": "ayat", "waktu": at(i + 1, jam[0]),
                      "files": [f"ayat_singkat/{path.name}"], "caption": caption})
    # carousel diambil berurutan: hari 1 = 1 post, hari 2-7 = 2 per hari (13:00, 19:00), setelahnya 3 per hari
    slots = [(0, jam[-1])] + [(d, t) for d in range(1, 1 + len(fakta)) for t in jam[1:]] \
            + [(d, jam[1]) for d in range(1 + len(fakta), 90)]  # mulai minggu 2: 08:00 fakta, 13:00 carousel, 19:00 "bukan kata Alkitab"
    ayat_posts = [(week, day, pages, caption) for week, modul in enumerate(akun_baru.MINGGU_AYAT)
                  for day, (pages, caption) in enumerate(akun_baru.render_ayat(modul))]
    for (week, day, pages, caption), (d, t) in zip(ayat_posts, slots):
        modul = akun_baru.MINGGU_AYAT[week]
        items.append({"id": f"ayat-m{week + 1}-{day + 1}", "akun": "ayat", "waktu": at(d, t),
                      "files": [f"{modul}/{f.name}" for f in pages], "caption": caption})
    kapi_aktif = config.AKUN["kapi"].get("aktif", True)
    if kapi_aktif:
        from konten import kapi_tambahan
        for (hari, slot), (files, caption, reel) in render_kapi_tambahan().items():
            if reel and (OUT / reel).exists():
                files = [reel]
            items.append({"id": f"kapi-{hari}-{slot}", "akun": "kapi", "waktu": at(hari - 1, config.AKUN["kapi"]["jam"][slot]),
                          "files": files, "caption": caption.format(handle=config.AKUN["kapi"]["handle"]) + "\n.\n.\n" + kapi_tambahan.TAGS})
    for day, rel in enumerate(kapi_files if kapi_aktif else []):
        p = kapi.POSTS[day]
        # kapi-2 diposting lebih awal (Senin dini hari), jadi kapi-3 dst. maju satu hari: kapi-3 = Senin 19:00, kapi-8 = Sabtu 19:00
        slot_day = day if day < 2 else day - 1
        items.append({"id": f"kapi-{day + 1}", "akun": "kapi", "waktu": at(slot_day, config.AKUN["kapi"]["jam"]["malam"]),
                      "files": [reel_or_image(f"reels/kapi/hari{day + 1}.mp4", rel)],
                      "caption": p["caption"].format(handle=config.AKUN["kapi"]["handle"]) + "\n.\n.\n" + kapi.TAGS})
    items += minggu_kedua(at)
    if (ROOT / "konten/tenang_extra.py").exists():  # Tenang 12/hari: 2 slot tambahan mulai 3 Okt (hari ke-7 = indeks 6)
        import gaya_baru
        from konten import tenang_extra as tx
        for day, slots in tx.JADWAL.items():
            for slot, (fmt, idx) in slots.items():
                p = (tx.BUKU if fmt == "BUKU" else tx.MEME)[idx]
                img = gaya_baru.buku_image(p, 500 + idx) if fmt == "BUKU" else gaya_baru.meme_image(p, 500 + idx)
                rel = save(img, f"tenang_extra/{fmt.lower()}{idx + 1}.jpg")
                items.append({"id": f"tenang_extra-{day}-{slot}", "akun": "tenang", "waktu": at(6 + day, config.AKUN["tenang"]["jam"][slot]),
                              "files": [rel], "caption": p["caption"] + "\n.\n.\n" + tenang.TAGS})
    import gaya_baru  # Tenang minggu 3 dst.: buku, meme, skrip, kisah, relatable, kinetik, photo dump, dulu vs sekarang
    for mod, start_day in (("tenang_w3", 14), ("tenang_w4", 21)):  # minggu 3 = 11 Okt, minggu 4 = 18 Okt
        if (ROOT / f"konten/{mod}.py").exists():
            for (hari, slot), (files, caption) in gaya_baru.render_week(mod).items():
                items.append({"id": f"{mod}-{hari}-{slot}", "akun": "tenang", "waktu": at(start_day + hari - 1, config.AKUN["tenang"]["jam"][slot]),
                              "files": files, "caption": caption + "\n.\n.\n" + tenang.TAGS})
    items = [it for it in items if config.AKUN[it["akun"]].get("aktif", True)]  # akun yang dipause tidak dijadwalkan
    if config.AKUN["eli"].get("pause_lama"):  # Eli lama (kartun) dipause; hanya Eli & Ruthie (gambar AI) yang diposting
        items = [it for it in items if it["akun"] != "eli" or it["id"].startswith("eli_lamb")]
    if config.STORY_OTOMATIS:
        items = add_stories(items)
    items.sort(key=lambda x: x["waktu"])
    (OUT / "schedule.json").write_text(json.dumps(items, ensure_ascii=False, indent=2))
    return items


def minggu_kedua(at, off=7):
    """Minggu 2 (Minggu 4 - Sabtu 10 Okt 2026). Tiap bagian hanya dijadwalkan kalau file kontennya ada.
    Eli minggu ini berbahasa Inggris dengan jam yang cocok untuk NZ/Australia (config.AKUN['eli']['jam_en'])."""
    import akun_baru
    import keren
    items = []
    lamb = {}
    if (ROOT / "konten/eli_lamb.py").exists():  # Eli the Lamb (gambar AI): hari yang gambarnya sudah ada menggantikan Eli kartun
        import eli_lamb
        lamb = eli_lamb.render_semua()
        jam = config.AKUN["eli"]["jam_en"]
        for (hari, slot), (files, caption) in lamb.items():
            items.append({"id": f"eli_lamb-{hari}-{slot}", "akun": "eli", "waktu": at(off + hari - 1, jam[slot]),
                          "files": files, "caption": caption})
    lamb_days = {h for h, _ in lamb}
    if (ROOT / "konten/eli_w2.py").exists():
        from konten import eli_w2
        jam = config.AKUN["eli"]["jam_en"]
        for v in eli_w2.VERSE:
            if v["hari"] in lamb_days:
                continue
            rel = save(eli_image(v["slot"], v["bubble"], v["kutipan"], v["ref"]), f"eli_w2/hari{v['hari']}_{v['slot']}.jpg")
            items.append({"id": f"eli_w2-{v['hari']}-{v['slot']}", "akun": "eli", "waktu": at(off + v["hari"] - 1, jam[v["slot"]]),
                          "files": [reel_or_image(f"reels/eli_w2/hari{v['hari']}_{v['slot']}.mp4", rel)], "caption": v["caption"]})
        for (hari, slot), (files, caption) in render_eli_variasi("eli_w2", "eli_w2", "en").items():
            if hari in lamb_days:
                continue
            items.append({"id": f"eli_w2-{hari}-{slot}", "akun": "eli", "waktu": at(off + hari - 1, jam[slot]),
                          "files": files, "caption": caption})
    if (ROOT / "konten/tenang_keren2.py").exists():
        for (hari, slot), (files, caption) in keren.render_keren("tenang_keren2").items():
            items.append({"id": f"tenang_keren2-{hari}-{slot}", "akun": "tenang", "waktu": at(off + hari - 1, config.AKUN["tenang"]["jam"][slot]),
                          "files": files, "caption": caption + "\n.\n.\n" + tenang.TAGS})
    if (ROOT / "konten/kapi_w2.py").exists() and config.AKUN["kapi"].get("aktif", True):
        from konten import kapi_w2
        for (hari, slot), (files, caption, reel) in render_kapi_tambahan("kapi_w2", "kapi_w2").items():
            if reel and (OUT / reel).exists():
                files = [reel]
            items.append({"id": f"kapi_w2-{hari}-{slot}", "akun": "kapi", "waktu": at(off + hari - 1, config.AKUN["kapi"]["jam"][slot]),
                          "files": files, "caption": caption.format(handle=config.AKUN["kapi"]["handle"]) + "\n.\n.\n" + kapi_w2.TAGS})
    if (ROOT / "konten/ayat_w2.py").exists():
        jam = config.AKUN["ayat"]["jam"]
        for i, (path, caption) in enumerate(akun_baru.fakta_singkat("ayat_w2", "ayat_w2")):
            items.append({"id": f"ayat_w2-fakta-{i + 1}", "akun": "ayat", "waktu": at(off + i, jam[0]),
                          "files": [f"ayat_w2/{path.name}"], "caption": caption})
        for i, (paths, caption) in enumerate(akun_baru.salah_kutip("ayat_w2", "ayat_w2")):
            items.append({"id": f"ayat_w2-salah-{i + 1}", "akun": "ayat", "waktu": at(off + i, jam[2]),
                          "files": [f"ayat_w2/{p.name}" for p in paths], "caption": caption})
    return items


def write_jadwal(items):
    """output/JADWAL.md: daftar post untuk dijadwalkan manual di Meta Business Suite (jam WIB + NZ)."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    nz = ZoneInfo("Pacific/Auckland")
    lines = ["# Jadwal posting minggu ini", "", "Jam Business Suite mengikuti zona waktu komputer (NZ). Pakai kolom **jam NZ**.", ""]
    for it in items:
        t = datetime.fromisoformat(it["waktu"])
        handle = config.AKUN[it["akun"]]["handle"]
        lines += [f"## @{handle} — {t:%a %d %b} {t:%H:%M} WIB → **{t.astimezone(nz):%a %d %b %H:%M} NZ**", "",
                  "Gambar (urut): " + ", ".join(f"`output/{f}`" for f in it["files"]), "", "```", it["caption"], "```", ""]
    (OUT / "JADWAL.md").write_text("\n".join(lines))


if __name__ == "__main__":
    e, t, k = render_eli(), render_tenang(), render_kapi()
    render_eli_tambahan()
    t2 = render_tenang("tenang_minggu2")  # selalu dirender; dijadwalkan hanya kalau config.TENANG_MINGGU2_AKTIF
    contact_sheet([[f for x in t2 if x[0] == d for f in x[4][:3]] for d in range(1, 8)], "preview_tenang_minggu2.jpg")
    contact_sheet([e[i:i + 3] for i in range(0, 21, 3)], "preview_eli.jpg")
    contact_sheet([[f for x in t if x[0] == d for f in x[4][:3]] for d in range(1, 8)], "preview_tenang.jpg")
    contact_sheet([k[:4], k[4:]], "preview_kapi.jpg")
    items = build_schedule(e, t, k)
    render_profil()
    write_jadwal(items)
    print(f"{len(e)} Eli, {len(t)} post Tenang ({sum(len(x[4]) for x in t)} gambar) -> {len(items)} post terjadwal (Kapi tidak aktif: {not config.AKUN['kapi'].get('aktif', True)})")
