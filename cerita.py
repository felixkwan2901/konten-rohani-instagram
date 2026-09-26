"""Konten cerita ala child.ink: satu adegan dibagi beberapa slide, dialog Eli dan Yesus.

  python3 cerita.py     # bikin output/contoh/ (carousel "Pot Eli" + Reels "Payung")
"""
import math
import random
import subprocess
from io import BytesIO

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import config
import render
from render import BLUSH, NAVY, PAPER, SKIN, eli_fig, font, wrap

HAIR, SASH, PINK, GREEN, BOX = "#8B6B4E", "#BFD7F2", "#F8C9D2", "#CFE8D4", "#DCE7F7"
OUT = render.OUT / "contoh"
HANDLE = "@" + config.AKUN["eli"]["handle"].upper()


# ---------- gambar dasar ----------

def svg_rgba(body, w, h):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
    return Image.open(BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")


RED = "#C8433E"
JESUS_HAND = {"payung": (46, -140)}  # posisi tangan (koordinat dasar) yang dipakai adegan lain


def jesus_fig(arms="bawah"):
    """Yesus gaya chibi, serasi dengan Eli (kaki di y=0, tinggi ~222).
    arms: bawah | sambut (tangan terbuka) | tunjuk (meraih ke kiri) | payung"""
    sleeve = lambda d: (f'<path d="{d}" fill="none" stroke="{NAVY}" stroke-width="15" stroke-linecap="round"/>'
                        f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="11.5" stroke-linecap="round"/>')
    hand = lambda x, y: f'<ellipse cx="{x}" cy="{y}" rx="6.5" ry="5.5" fill="{SKIN}" stroke="{NAVY}" stroke-width="1.6"/>'
    ln = f'stroke="{NAVY}" stroke-width="1.8" stroke-linejoin="round"'
    s = (f'<ellipse cx="-14" cy="-3" rx="9" ry="4" fill="{SKIN}" {ln}/><ellipse cx="14" cy="-3" rx="9" ry="4" fill="{SKIN}" {ln}/>'
         f'<path d="M-26,-150 Q-34,-80 -40,-7 Q0,-2 40,-7 Q34,-80 26,-150 Q0,-157 -26,-150 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="round"/>'
         f'<path d="M-14,-80 Q-18,-40 -20,-10 M12,-78 Q16,-40 18,-10" fill="none" stroke="{NAVY}" stroke-width="1.2" opacity="0.4"/>'
         f'<path d="M22,-151 Q48,-140 46,-100 Q50,-52 62,-14 Q46,-6 32,-12 Q36,-60 28,-100 Z" fill="{RED}" {ln}/>'
         f'<path d="M24,-150 Q4,-126 -20,-99" fill="none" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/>'
         f'<path d="M24,-150 Q4,-126 -20,-99" fill="none" stroke="{RED}" stroke-width="10.5" stroke-linecap="round"/>'
         f'<path d="M-36,-99 Q0,-93 36,-99 L37,-87 Q0,-81 -37,-87 Z" fill="{RED}" {ln}/>'
         f'<path d="M-5,-86 L-7,-62 M3,-86 L5,-64" stroke="{RED}" stroke-width="4.5" stroke-linecap="round"/>')
    arms_svg = {
        "bawah": sleeve("M-27,-146 Q-40,-120 -38,-100") + hand(-38, -96) + sleeve("M27,-146 Q40,-120 38,-100") + hand(38, -96),
        "sambut": sleeve("M-26,-146 Q-40,-132 -50,-112") + hand(-55, -106) + sleeve("M26,-146 Q40,-132 50,-112") + hand(55, -106),
        "tunjuk": sleeve("M-26,-146 Q-46,-138 -58,-126") + hand(-64, -123) + sleeve("M27,-146 Q40,-120 38,-100") + hand(38, -96),
        "payung": sleeve("M-27,-146 Q-40,-120 -38,-100") + hand(-38, -96) + sleeve("M27,-146 Q46,-150 46,-146") + hand(46, -140),
    }[arms]
    head = (f'<path d="M-29,-186 Q-36,-214 -8,-214 Q0,-219 10,-214 Q37,-213 32,-185 Q41,-165 36,-147 Q30,-139 26,-148 '
            f'Q29,-160 25,-170 L-25,-170 Q-29,-160 -26,-148 Q-30,-139 -36,-147 Q-41,-165 -29,-186 Z" fill="{HAIR}" {ln}/>'
            f'<circle cx="0" cy="-178" r="27" fill="{SKIN}" stroke="{NAVY}" stroke-width="2.2"/>'
            f'<path d="M-24,-173 Q-22,-146 0,-144 Q22,-146 24,-173 Q19,-162 12,-159 Q6,-164 0,-164 Q-6,-164 -12,-159 Q-19,-162 -24,-173 Z" fill="{HAIR}" {ln}/>'
            f'<path d="M-8,-163 Q0,-152 8,-163 Z" fill="#8C2F39" stroke="{NAVY}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M-11,-166 Q-5,-171 0,-167 Q5,-171 11,-166 Q5,-163 0,-165 Q-5,-163 -11,-166 Z" fill="{HAIR}" stroke="{NAVY}" stroke-width="1.2"/>'
            f'<path d="M-28,-181 Q-27,-209 0,-207 Q27,-209 28,-181 Q21,-199 7,-197 Q2,-195 0,-190 Q-2,-195 -7,-197 Q-21,-199 -28,-181 Z" fill="{HAIR}" {ln}/>'
            f'<ellipse cx="-10" cy="-181" rx="3" ry="3.8" fill="{NAVY}"/><ellipse cx="10" cy="-181" rx="3" ry="3.8" fill="{NAVY}"/>'
            f'<circle cx="-9" cy="-182.5" r="1.1" fill="#FFFFFF"/><circle cx="11" cy="-182.5" r="1.1" fill="#FFFFFF"/>'
            f'<path d="M-15,-189 Q-10,-192 -5,-189 M5,-189 Q10,-192 15,-189" fill="none" stroke="{HAIR}" stroke-width="2" stroke-linecap="round"/>'
            f'<ellipse cx="-17" cy="-172" rx="4" ry="2.4" fill="{BLUSH}"/><ellipse cx="17" cy="-172" rx="4" ry="2.4" fill="{BLUSH}"/>')
    return s + arms_svg + head


def pot(sprout=False):
    s = (f'<path d="M-60,0 L-75,-108 L75,-108 L60,0 Z" fill="#F4D3B5" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
         f'<rect x="-82" y="-130" width="164" height="24" rx="6" fill="#F4D3B5" stroke="{NAVY}" stroke-width="3"/>'
         f'<ellipse cx="0" cy="-126" rx="70" ry="7" fill="#8C6D4F"/>')
    if sprout:
        s += (f'<path d="M0,-126 Q-4,-160 0,-188" fill="none" stroke="#5BA35B" stroke-width="5" stroke-linecap="round"/>'
              f'<ellipse cx="-18" cy="-188" rx="18" ry="8" transform="rotate(-25 -18 -188)" fill="#9ED39E" stroke="{NAVY}" stroke-width="2"/>'
              f'<ellipse cx="18" cy="-194" rx="18" ry="8" transform="rotate(25 18 -194)" fill="#9ED39E" stroke="{NAVY}" stroke-width="2"/>')
    return s


def place(fig, x, y, k):
    return f'<g transform="translate({x},{y}) scale({k})">{fig}</g>'


def sparkles(points):
    star = lambda x, y, k: (f'<path transform="translate({x},{y}) scale({k})" d="M0,-20 L5,-5 L20,0 L5,5 L0,20 L-5,5 L-20,0 L-5,-5 Z" '
                            f'fill="#FBE38E" stroke="{NAVY}" stroke-width="{2.5 / k}" stroke-linejoin="round"/>')
    return "".join(star(*p) for p in points)


def bubble_img(text, color, tail, size=42, maxw=330):
    """Balon dialog sebagai gambar kecil. tail = posisi ujung ekor relatif ke tengah balon."""
    f = font("tangan", size)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap(probe, text, f, maxw)
    lh = size * 1.18
    rx = max(probe.textlength(ln, font=f) for ln in lines) / 2 + 52
    ry = len(lines) * lh / 2 + 42
    w, h = int(2 * max(rx, abs(tail[0])) + 24), int(2 * max(ry, abs(tail[1])) + 24)
    cx, cy = w / 2, h / 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    a = math.atan2(tail[1] / ry, tail[0] / rx)
    base = [(cx + rx * 0.8 * math.cos(a + da), cy + ry * 0.8 * math.sin(a + da)) for da in (-0.28, 0.28)]
    d.polygon([base[0], (cx + tail[0], cy + tail[1]), base[1]], fill=color)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=color)
    y = cy - len(lines) * lh / 2
    for ln in lines:
        d.text((cx, y), ln, font=f, fill=NAVY, anchor="ma")
        y += lh
    return img


def paste_bubble(base, bub, center, scale=1.0, alpha=1.0):
    if alpha <= 0:
        return
    if scale != 1.0:
        bub = bub.resize((max(1, int(bub.width * scale)), max(1, int(bub.height * scale))), Image.BILINEAR)
    if alpha < 1:
        bub = bub.copy()
        bub.putalpha(bub.getchannel("A").point(lambda v: int(v * alpha)))
    base.paste(bub, (int(center[0] - bub.width / 2), int(center[1] - bub.height / 2)), bub)


def narasi(base, x, y, text, maxw, size=34, ref=None, alpha=1.0):
    """Kotak narasi ala komik (huruf kapital tulisan tangan)."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font("tangan", size)
    lines = wrap(d, text.upper(), f, maxw)
    lh = size * 1.25
    tw = max(d.textlength(ln, font=f) for ln in lines)
    extra = lh if ref else 0
    d.rectangle((x, y, x + tw + 48, y + len(lines) * lh + extra + 36), fill=BOX, outline=NAVY, width=3)
    for i, ln in enumerate(lines):
        d.text((x + 24, y + 18 + i * lh), ln, font=f, fill=NAVY)
    if ref:
        d.text((x + 24, y + 18 + len(lines) * lh + 4), ref.upper(), font=font("tangan", int(size * 0.8)), fill="#8C6D22")
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(layer)



# ---------- tema warna & efek gambar tangan ----------

FLOOR = None  # warna lantai di bawah garis tanah (None = hanya garis)

THEMES = {
    "hangat": {  # krem hangat + garis coklat, mirip komik pensil warna
        "cerita": dict(NAVY="#5B4636", PAPER="#FBF3E4", SKIN="#F8DFC8", BLUSH="#F2A7A7", PINK="#F4C9C4",
                       GREEN="#C9DDB8", BOX="#F7E6C4", RED="#B9483E", HAIR="#7A5236", SASH="#E9C9A6", FLOOR="#EFDFC6"),
        "render": dict(INK="#5B4636", PAPER="#FBF3E4", SKIN="#F8DFC8", BLUSH="#F2A7A7",
                       ELI_HAIR="#2E3F5C", ELI_PANTS="#4F6D9A", BIBLE="#2E3F5C"),
    },
}


def apply_theme(name):
    """Ganti warna modul ini dan render.py. Mengembalikan warna lama untuk dipulihkan."""
    old = {"cerita": {k: globals()[k] for k in THEMES[name]["cerita"]},
           "render": {k: getattr(render, k) for k in THEMES[name]["render"]}}
    restore_theme(THEMES[name])
    return old


def restore_theme(values):
    globals().update(values["cerita"])
    for k, v in values["render"].items():
        setattr(render, k, v)


def sketchify(img, amp=1.6, seed=3):
    """Bikin garis vektor terasa digambar tangan: sedikit goyang, lembut, dan bertekstur kertas."""
    rng = np.random.default_rng(seed)
    w, h = img.size
    field = lambda: np.asarray(Image.fromarray((rng.random((h // 36 + 2, w // 36 + 2)) * 2 - 1).astype(np.float32))
                               .resize((w, h), Image.BICUBIC)) * amp
    dx, dy = field(), field()
    yy, xx = np.mgrid[0:h, 0:w]
    arr = np.asarray(img.convert("RGB"))[np.clip((yy + dy).round().astype(int), 0, h - 1),
                                         np.clip((xx + dx).round().astype(int), 0, w - 1)]
    soft = np.asarray(Image.fromarray(arr).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)
    noise = np.clip(rng.normal(128, 40, (h, w)), 0, 255).astype(np.uint8)
    grain = (np.asarray(Image.fromarray(noise).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) - 128) / 40
    fibers = np.asarray(Image.fromarray(rng.normal(0, 1, (h // 6, w // 6)).astype(np.float32)).resize((w, h), Image.BICUBIC))
    return Image.fromarray(np.clip(soft * (1 + grain[..., None] * 0.05 + fibers[..., None] * 0.012), 0, 255).astype(np.uint8))


# ---------- contoh 1: carousel "Pot Eli" (5 slide, 4:5) ----------

PX0, PY0, PX1, PY1, GROUND, K = 70, 140, 1010, 1180, 1120, 2.8


def slide_base(body):
    frame = f'<rect x="{PX0}" y="{PY0}" width="{PX1 - PX0}" height="{PY1 - PY0}" fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>'
    if FLOOR:
        frame += f'<rect x="{PX0 + 2}" y="{GROUND - 6}" width="{PX1 - PX0 - 4}" height="{PY1 - GROUND + 4}" fill="{FLOOR}"/>'
    frame += f'<line x1="{PX0 + 2}" y1="{GROUND - 6}" x2="{PX1 - 2}" y2="{GROUND - 6}" stroke="{NAVY}" stroke-width="3" opacity="{0.8 if FLOOR else 0.35}"/>'
    img = Image.new("RGBA", (1080, 1350), PAPER)
    img.alpha_composite(svg_rgba(frame + body, 1080, 1350))
    ImageDraw.Draw(img).text((PX0, PY1 + 22), HANDLE, font=font("sans_bold", 22), fill=NAVY)
    return img


def cutaway():
    roots = "".join(f'<path d="{d}" fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linecap="round"/>' for d in [
        "M0,-62 Q-6,-40 -18,-24 Q-26,-14 -30,-4", "M0,-62 Q4,-38 14,-22 Q22,-12 30,-6",
        "M-8,-40 Q-22,-38 -34,-30", "M8,-36 Q24,-36 36,-26", "M0,-60 Q2,-30 0,-10"])
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{NAVY}" opacity="0.35"/>'
                   for x, y in [(-50, -90), (-30, -100), (40, -95), (55, -70), (-55, -50), (48, -40), (-40, -20), (20, -15), (-15, -85), (30, -60)])
    return (f'<path d="M-60,0 L-75,-108 L75,-108 L60,0 Z" fill="#C9AA88" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="-82" y="-130" width="164" height="24" rx="6" fill="#F4D3B5" stroke="{NAVY}" stroke-width="3"/>'
            f'<line x1="-72" y1="-108" x2="72" y2="-108" stroke="{NAVY}" stroke-width="2" stroke-dasharray="6 5"/>'
            + dots + roots
            + f'<ellipse cx="0" cy="-64" rx="9" ry="6" fill="#8C6D4F" stroke="{NAVY}" stroke-width="2"/>'
            + f'<path d="M0,-70 Q-6,-86 2,-100 Q8,-106 12,-100" fill="none" stroke="#5BA35B" stroke-width="3.5" stroke-linecap="round"/>')


def pot_slides():
    """Cerita "Pot Eli": per slide (gambar adegan, daftar overlay yang muncul berurutan).
    Overlay: ("bubble", teks, warna, ekor, tengah, maxw) atau ("narasi", x, y, teks, maxw, ref)."""
    return [
        (place(eli_fig("bingung", "dagu"), 420, GROUND, K) + place(pot(), 660, GROUND, 1.3),
         [("bubble", "Kok belum tumbuh juga ya...", PINK, (70, 170), (330, 470), 330)]),
        (place(eli_fig("bingung", "dagu"), 380, GROUND, K) + place(pot(), 610, GROUND, 1.3) + place(jesus_fig("tunjuk"), 815, GROUND, K),
         [("bubble", "Kamu sudah siram tiap hari?", GREEN, (160, 120), (610, 360), 330),
          ("bubble", "Sudah... tapi nggak ada apa-apa.", PINK, (70, 140), (290, 540), 330)]),
        (place(cutaway(), 540, 1010, 3.4),
         [("narasi", 120, 200, "Yang tidak terlihat,", 700, None), ("narasi", 560, 1040, "tetap sedang bekerja.", 400, None)]),
        (place(pot(), 885, GROUND, 1.1) + place(eli_fig("senyum", "bawah"), 430, GROUND, K) + place(jesus_fig("tunjuk"), 640, GROUND, K),
         [("bubble", "Aku juga sedang menumbuhkan sesuatu di dalam kamu.", GREEN, (215, 120), (370, 330), 360)]),
        (place(pot(sprout=True), 590, GROUND, 1.3) + place(eli_fig("gembira", "atas"), 300, GROUND - 40, K)
         + place(jesus_fig("sambut"), 830, GROUND, K) + sparkles([(165, 640, 1.2), (450, 600, 0.9), (480, 820, 0.8), (600, 760, 1)]),
         [("narasi", 110, 180, "“Ia membuat segala sesuatu indah pada waktunya.”", 800, "Pengkhotbah 3:11")]),
    ]


def overlay_layer(ov, size=(1080, 1350)):
    """Satu overlay sebagai layer transparan seukuran slide."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    if ov[0] == "bubble":
        _, text, color, tail, center, maxw = ov
        paste_bubble(layer, bubble_img(text, color, tail, maxw=maxw), center)
    else:
        _, x, y, text, maxw, ref = ov
        narasi(layer, x, y, text, maxw, ref=ref)
    return layer


def carousel_pot(theme=None, video=False):
    """Carousel "Pot Eli". video=True: tiap slide jadi MP4 4:5 (balon dialog muncul bergantian)."""
    OUT.mkdir(parents=True, exist_ok=True)
    old = apply_theme(theme) if theme else None
    tag = f"_{theme}" if theme else ""
    files = []
    for i, (body, overlays) in enumerate(pot_slides(), 1):
        base = slide_base(body)
        layers = [overlay_layer(ov) for ov in overlays]
        if video:
            files.append(animate_slide(base, layers, OUT / f"carousel_pot{tag}_{i}.mp4"))
            continue
        for layer in layers:
            base.alpha_composite(layer)
        path = OUT / f"carousel_pot{tag}_{i}.jpg"
        (sketchify(base) if theme else base.convert("RGB")).save(path, "JPEG", quality=92)
        files.append(path)
    if old:
        restore_theme(old)
    (OUT / "carousel_pot_caption.txt").write_text(CAPTION_POT)
    return files


def ffmpeg_writer(path, w, h, fps=30):
    return subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                             "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                             "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)


def animate_slide(base, layers, path, seconds=4.5, fps=30):
    """Adegan diam dengan zoom pelan; tiap layer muncul bergantian (balon: pop, narasi: fade)."""
    w, h = base.size
    ff = ffmpeg_writer(path, w, h, fps)
    for n in range(int(seconds * fps)):
        t = n / fps
        frame = base.copy()
        for j, layer in enumerate(layers):
            start = 0.5 + j * 1.2
            p = ease((t - start) / 0.3)
            if p <= 0:
                continue
            lay = layer
            if p < 1:
                bbox = layer.getbbox()
                cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
                k = 0.7 + 0.3 * p
                lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                crop = layer.crop(bbox)
                crop = crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))), Image.BILINEAR)
                crop.putalpha(crop.getchannel("A").point(lambda v: int(v * p)))
                lay.paste(crop, (int(cx - crop.width / 2), int(cy - crop.height / 2)))
            frame.alpha_composite(lay)
        z = 1 + 0.03 * (t / seconds)
        zw, zh = int(w * z), int(h * z)
        frame = frame.resize((zw, zh), Image.BILINEAR).crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {path}")
    return path


CAPTION_POT = """Kok belum tumbuh juga ya? 🌱

Kadang kita sudah berdoa, sudah berusaha, sudah menunggu... tapi kelihatannya belum ada apa-apa.

Eli juga pernah merasa begitu. Tapi ternyata, di bawah tanah, akarnya sedang tumbuh — diam-diam, tapi pasti.

Mungkin itu juga yang sedang Tuhan kerjakan di dalam kamu sekarang 💛

📖 “Ia membuat segala sesuatu indah pada waktunya.” — Pengkhotbah 3:11

Geser sampai habis ya 👉
Ketik 🌱 kalau kamu sedang di masa menunggu.
.
.
#renunganharian #komikkristen #ayatalkitab #firmanTuhan #pengharapan #indahpadawaktunya #sahabateli"""


# ---------- contoh 2: Reels "Payung" (9:16, 14 detik) ----------

RW, RH, FPS, SECONDS = 1080, 1920, 30, 14
RG = 1450  # garis tanah di Reels


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def pop(t, start, end=99.0):
    """(skala, alpha) balon yang muncul di 'start' dan hilang di 'end'."""
    if t < start or t > end + 0.3:
        return 0.0, 0.0
    if t > end:
        return 1.0, 1 - (t - end) / 0.3
    p = ease((t - start) / 0.25)
    return 0.6 + 0.4 * p, p


def umbrella(cx, bottom):
    top = bottom - 210
    scallop = " ".join(f"Q{cx + x + 32.5},{bottom - 30} {cx + x + 65},{bottom}" for x in range(-260, 260, 65))
    ribs = "".join(f'<path d="M{cx},{top} Q{cx + x * 0.6},{top + 60} {cx + x},{bottom}" fill="none" stroke="{NAVY}" stroke-width="2.5"/>'
                   for x in (-130, 0, 130))
    return (f'<path d="M{cx - 260},{bottom} Q{cx - 260},{top + 10} {cx},{top} Q{cx + 260},{top + 10} {cx + 260},{bottom} '
            f'L{cx + 260},{bottom} Z" fill="{PINK}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx - 260},{bottom} {scallop}" fill="{PAPER}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
            + ribs + f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{top - 22}" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>')


def reel_payung():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(7)
    drops = [(rng.uniform(60, 1020), rng.uniform(0, 1100), rng.uniform(850, 1100)) for _ in range(150)]
    b1 = bubble_img("Hujan terus...", PINK, (-120, 150))
    b2 = bubble_img("Aku nggak bawa payung...", PINK, (-120, 120))
    bj = bubble_img("Aku di sini, Eli.", GREEN, (40, 110))
    b3 = bubble_img("Masih hujan... tapi aku nggak sendirian.", PINK, (-150, 140))
    out = OUT / "reel_payung.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for n in range(FPS * SECONDS):
        t = n / FPS
        jx = -160 + (380 + 160) * ease((t - 4.5) / 2.0)
        ucx = jx + JESUS_HAND["payung"][0] * K
        body = (f'<rect x="40" y="340" width="1000" height="1180" fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>'
                f'<ellipse cx="250" cy="{RG + 8}" rx="90" ry="10" fill="{BOX}"/><ellipse cx="860" cy="{RG + 10}" rx="120" ry="12" fill="{BOX}"/>'
                f'<line x1="80" y1="{RG}" x2="1000" y2="{RG}" stroke="{NAVY}" stroke-width="3" opacity="0.35"/>')
        rain = []
        for x0, y0, v in drops:
            y = 350 + (y0 + v * t) % 1090
            x = x0 - (y - 350) * 0.08
            if ucx - 265 < x < ucx + 265 and y > 520:
                continue
            if y + 36 < RG:
                rain.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 7:.0f}" y2="{y + 36:.0f}" stroke="{NAVY}" stroke-width="3" stroke-linecap="round" opacity="0.45"/>')
        body += "".join(rain)
        body += place(eli_fig("senyum" if t > 8.5 else "sedih", "bawah"), 600, RG, K)
        if jx > -150:
            body += place(jesus_fig("payung"), jx, RG, K)
            hx, hy = ucx, RG + JESUS_HAND["payung"][1] * K
            body += (f'<path d="M{hx},740 L{hx},{hy + 30} Q{hx},{hy + 55} {hx - 20},{hy + 48}" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>'
                     + umbrella(ucx, 740))
        frame = Image.new("RGBA", (RW, RH), PAPER)
        clip = '<defs><clipPath id="p"><rect x="42" y="342" width="996" height="1176"/></clipPath></defs>'
        frame.alpha_composite(svg_rgba(f'{clip}<g clip-path="url(#p)">{body}</g>'
                                       f'<rect x="40" y="340" width="1000" height="1180" fill="none" stroke="{NAVY}" stroke-width="4"/>', RW, RH))
        ImageDraw.Draw(frame).text((60, 1535), HANDLE, font=font("sans_bold", 22), fill=NAVY)

        for bub, center, (sc, al) in [(b1, (780, 880), pop(t, 1.0, 4.3)), (b2, (740, 680), pop(t, 2.6, 4.3)),
                                      (bj, (330, 470), pop(t, 7.0)), (b3, (815, 900), pop(t, 8.7))]:
            paste_bubble(frame, bub, center, sc, al)
        if t > 10.4:
            narasi(frame, 60, 120, "“Apabila engkau menyeberang melalui air, Aku akan menyertai engkau.”", 880,
                   ref="Yesaya 43:2", alpha=ease((t - 10.4) / 0.8))
        if t < 0.5:
            frame = Image.blend(Image.new("RGBA", (RW, RH), PAPER), frame, ease(t / 0.5))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError("ffmpeg gagal")
    (OUT / "reel_payung_caption.txt").write_text(CAPTION_PAYUNG)
    return out


CAPTION_PAYUNG = """Hujannya belum berhenti... tapi kamu nggak sendirian ☔

Tuhan nggak selalu langsung menghentikan badai. Tapi Dia selalu datang dan berdiri di sampingmu, di tengah hujan.

📖 “Apabila engkau menyeberang melalui air, Aku akan menyertai engkau.” — Yesaya 43:2

Kirim ini ke seseorang yang lagi “kehujanan” minggu ini 💙
.
.
#renunganharian #komikkristen #ayatalkitab #Tuhanmenyertai #kristenindonesia #reelskristen #sahabateli"""


if __name__ == "__main__":
    for f in carousel_pot():
        print(f)
    print(reel_payung())
