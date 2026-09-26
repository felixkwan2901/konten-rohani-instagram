"""Bikin semua Reels (MP4 1080x1920, tanpa suara; musik ditambahkan di Instagram).

  python3 reels.py              # semua: 21 Reels Eli, 7 Reels Kapi, Reels panjang Eli, carousel Pot bergerak
  python3 reels.py eli 1 2 3    # hanya Reels Eli nomor 1, 2, 3 (urutan di konten/eli.py)
  python3 reels.py kapi         # hanya Reels Kapi
  python3 reels.py minggu       # hanya Reels panjang "Satu minggu bersama Eli"
  python3 reels.py notif        # hanya Reels notifikasi akun Tenang (format B)
  python3 reels.py dinding      # hanya Reels dinding teks akun Tenang (format D)
  python3 reels.py suasana      # hanya Reels suasana akun Tenang (format R)
  python3 reels.py minggu2      # semua Reels akun Tenang minggu "Bukan milikku"
"""
import importlib
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

import cerita
import render
from konten import eli, kapi, tenang

RW, RH, FPS, SECONDS = 1080, 1920, 30, 9
TOP = 220  # posisi gambar 4:5 di kanvas 9:16, sedikit ke atas supaya ayat tidak tertutup caption Reels


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def make_reel(index):
    slot, bubble, kutipan, ref = eli.POSTS[index]
    paper = np.full((render.H, render.W, 3), Image.new("RGB", (1, 1), render.PAPER).getpixel((0, 0)), np.float32)
    stages = [np.asarray(render.eli_image(slot, bubble, kutipan, ref, show_bubble=b, show_verse=v), np.float32)
              for b, v in [(False, False), (True, False), (True, True)]]

    rel = f"reels/eli/hari{index // 3 + 1}_{slot}.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{RW}x{RH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                           "-crf", "20", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    canvas = Image.new("RGB", (RW, RH), render.PAPER)
    for n in range(FPS * SECONDS):
        t = n / FPS
        frame = paper + (stages[0] - paper) * ease(t / 0.6)
        frame = frame + (stages[1] - frame) * ease((t - 1.0) / 0.6)
        frame = frame + (stages[2] - frame) * ease((t - 2.8) / 1.0)
        img = Image.fromarray(frame.astype(np.uint8))
        z = 1 + 0.05 * (t / SECONDS)
        zw, zh = int(render.W * z), int(render.H * z)
        img = img.resize((zw, zh), Image.BILINEAR).crop(((zw - render.W) // 2, (zh - render.H) // 2,
                                                         (zw - render.W) // 2 + render.W, (zh - render.H) // 2 + render.H))
        canvas.paste(img, (0, TOP))
        ff.stdin.write(canvas.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


def kapi_reel(index, seconds=7):
    """Kalimat atas muncul -> KATA BESAR menghentak -> kalimat bawah masuk -> Kapi melompat masuk, lalu bergoyang & berkedip."""
    p = kapi.POSTS[index]
    rel = f"reels/kapi/hari{index + 1}.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fg, parts, pos = render.kapi_parts(p, 640)
    sprite, blink = render.kapi_sprite(p), render.kapi_sprite(p, blink=True)
    feet_x, feet_y = 560, 1560
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(FPS * seconds):
        t = n / FPS
        frame = Image.new("RGBA", (RW, RH), p["bg"])
        a = ease(t / 0.4)
        if a > 0:
            frame.alpha_composite(fade(parts["atas"], a), (pos["atas"][0], int(pos["atas"][1] + 30 * (1 - a))))
        b = ease((t - 0.5) / 0.35)
        if b > 0:
            k = 1.35 - 0.35 * b
            word = parts["besar"].resize((int(parts["besar"].width * k), int(parts["besar"].height * k)), Image.BILINEAR)
            cx, cy = pos["besar"][0] + parts["besar"].width / 2, pos["besar"][1] + parts["besar"].height / 2
            frame.alpha_composite(fade(word, b), (int(cx - word.width / 2), int(cy - word.height / 2)))
        c = ease((t - 1.1) / 0.35)
        if c > 0:
            frame.alpha_composite(fade(parts["bawah"], c), (int(pos["bawah"][0] + 120 * (1 - c)), pos["bawah"][1]))
        if t > 1.5:
            u = min((t - 1.5) / 0.6, 1.0)
            jump = (1 - u) * 520 - math.sin(u * math.pi) * 60   # naik dari bawah, sedikit memantul
            bob = math.sin((t - 2.1) * 2.6) * 10 if t > 2.1 else 0
            img = blink if 4.0 < t < 4.15 or 5.8 < t < 5.95 else sprite
            frame.alpha_composite(img, (feet_x - 310, int(feet_y - 620 + jump + bob)))
        render.kapi_handle(frame, p, fg, 1640)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


def fade(img, alpha):
    if alpha >= 1:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    return img


def weekly_reel(seconds_per_post=3.6, xfade=0.4):
    """Reels panjang (~80 detik): kartu judul, ke-21 post Eli minggu ini (pagi, siang, malam), kartu penutup."""
    rel = "reels/eli/minggu1_rangkuman.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    handle = "@" + render.config.AKUN["eli"]["handle"]

    def card(lines, face, arms):
        img = Image.new("RGBA", (RW, RH), render.PAPER)
        img.alpha_composite(cerita.svg_rgba(cerita.place(render.eli_fig(face, arms), 540, 1380, 4.2), RW, RH))
        d = ImageDraw.Draw(img)
        y = 380
        for text, size in lines:
            d.text((RW / 2, y), text, font=render.font("tangan", size), fill=render.NAVY, anchor="ma")
            y += size * 1.35
        return img.convert("RGB")

    title = card([("Satu minggu", 96), ("bersama Eli", 96), ("21 ayat pengharapan", 52)], "gembira", "atas")
    ending = card([("Sampai minggu depan ya!", 72), (handle, 52)], "senyum", "alkitab")
    posts = []
    for i, post in enumerate(eli.POSTS):
        img = Image.new("RGB", (RW, RH), render.PAPER)
        img.paste(render.eli_image(*post), (0, TOP))
        ImageDraw.Draw(img).text((RW / 2, 110), f"Hari {i // 3 + 1} · {post[0].capitalize()}", font=render.font("tangan", 64),
                                 fill=render.NAVY, anchor="ma")
        posts.append(img)
    segments = [(title, 3.0)] + [(im, seconds_per_post) for im in posts] + [(ending, 3.5)]

    def zoomed(img, t, length):
        z = 1 + 0.04 * (t / length)
        zw, zh = int(RW * z), int(RH * z)
        return img.resize((zw, zh), Image.BILINEAR).crop(((zw - RW) // 2, (zh - RH) // 2, (zw - RW) // 2 + RW, (zh - RH) // 2 + RH))

    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    starts, acc = [], 0.0
    for _, length in segments:
        starts.append(acc)
        acc += length
    for n in range(int(acc * FPS)):
        t = n / FPS
        i = max(j for j, st in enumerate(starts) if st <= t)
        img, length = segments[i]
        frame = zoomed(img, t - starts[i], length)
        if i + 1 < len(segments) and t > starts[i] + length - xfade:
            nxt, nlen = segments[i + 1]
            frame = Image.blend(frame, zoomed(nxt, 0, nlen), ease((t - (starts[i] + length - xfade)) / xfade))
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


def notif_reel(index, seconds=13, modul="tenang"):
    """Pemandangan bergeser pelan; notifikasi dari Tuhan muncul satu per satu (yang baru di atas,
    yang lama terdorong ke bawah), terakhir notifikasi ayat. Ada bunyi "ting" tiap notifikasi."""
    p = getattr(importlib.import_module(f"konten.{modul}"), "NOTIF")[index]
    rel = f"reels/{modul}/notif{index + 1}.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    pano = render.grain(render.landscape(p["adegan"], 2200, RH, seed=index + 2), 0.18)

    def card(sender, msg, letter, when):
        layer = Image.new("RGBA", (RW, 420), (0, 0, 0, 0))
        hgt = render.notif(layer, 0, sender, msg, letter, when=when)
        return layer.crop((0, 0, RW, hgt))

    cards = [(1.0 + 2.4 * i, card("Tuhan", m, "T", "sekarang")) for i, m in enumerate(p["pesan"])]
    cards.append((1.0 + 2.4 * 3, card("Alkitab", f'{p["ayat"]} — {p["ref"]}', "A", "sekarang")))
    silent = out.with_suffix(".silent.mp4")
    ff = cerita.ffmpeg_writer(silent, RW, RH, FPS)
    for n in range(FPS * seconds):
        t = n / FPS
        x = int((pano.width - RW) * t / seconds)
        frame = pano.crop((x, 0, x + RW, RH)).convert("RGBA")
        shown = [(ti, c) for ti, c in cards if t >= ti]
        for ti, c in shown:
            push = sum((c2.height + 18) * ease((t - t2) / 0.35) for t2, c2 in shown if t2 > ti)
            a = ease((t - ti) / 0.35)
            frame.alpha_composite(fade(c, a), (0, int(520 + push - 50 * (1 - a))))
        ImageDraw.Draw(frame).text((70, 1620), "@" + render.config.AKUN["tenang"]["handle"], font=render.font("sans_bold", 24),
                                   fill=(255, 255, 255, 200))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    ting = "+".join(f"gte(t,{ti})*exp(-9*(t-{ti}))*(0.35*sin(2*PI*1568*t)+0.2*sin(2*PI*2349*t))" for ti, _ in cards)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-f", "lavfi", "-i",
                    f"aevalsrc='{ting}':s=44100:d={seconds}", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", str(out)],
                   check=True)
    silent.unlink()
    return rel


def dinding_reel(index, seconds=10, modul="tenang"):
    """Dinding teks 9:16: kata-kata pesan menyala satu per satu."""
    p = getattr(importlib.import_module(f"konten.{modul}"), "DINDING")[index]
    rel = f"reels/{modul}/dinding{index + 1}.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    base, hits = render.dinding_layers(p, (RW, RH), fsize=46)
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(FPS * seconds):
        t = n / FPS
        frame = base.copy()
        for i, (sp, pos) in enumerate(hits):
            a = ease((t - 1.0 - i * 1.3) / 0.35)
            if a > 0:
                frame.alpha_composite(fade(sp, a), pos)
        z = 1 + 0.04 * t / seconds
        zw, zh = int(RW * z), int(RH * z)
        frame = frame.resize((zw, zh), Image.BILINEAR).crop(((zw - RW) // 2, (zh - RH) // 2, (zw - RW) // 2 + RW, (zh - RH) // 2 + RH))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


def suasana_reel(index, seconds=14, modul="tenang"):
    """Kabut bergerak / bintang berkelip, paragraf muncul pelan di tengah."""
    p = getattr(importlib.import_module(f"konten.{modul}"), "SUASANA")[index]
    rel = f"reels/{modul}/suasana{index + 1}.mp4"
    out = render.OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    scene = render.suasana_scene(p["adegan"], RW, RH)
    text = render.paragraph_layer(p["teks"], RW, RH, RH * 0.42, handle=render.config.AKUN["tenang"]["handle"])
    ff = cerita.ffmpeg_writer(out, RW, RH, FPS)
    for n in range(FPS * seconds):
        t = n / FPS
        frame = scene(t).convert("RGBA")
        frame.alpha_composite(fade(text, ease((t - 0.6) / 1.2)))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    return rel


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "semua"
    nums = [int(a) - 1 for a in sys.argv[2:]]
    if what in ("semua", "eli"):
        for i in nums or range(len(eli.POSTS)):
            print(make_reel(i))
    if what in ("semua", "kapi"):
        for i in nums or range(len(kapi.POSTS)):
            print(kapi_reel(i))
    if what in ("semua", "minggu"):
        print(weekly_reel())
    if what in ("semua", "dinding"):
        for i in nums or range(len(tenang.DINDING)):
            print(dinding_reel(i))
    if what in ("semua", "suasana"):
        for i in nums or range(len(tenang.SUASANA)):
            print(suasana_reel(i))
    if what == "minggu2":  # akun Tenang, minggu "Bukan milikku"
        from konten import tenang_minggu2 as t2
        for fn, pool in ((notif_reel, t2.NOTIF), (dinding_reel, t2.DINDING), (suasana_reel, t2.SUASANA)):
            for i in range(len(pool)):
                print(fn(i, modul="tenang_minggu2"))
    if what in ("semua", "notif"):
        for i in nums or range(len(tenang.NOTIF)):
            print(notif_reel(i))
    if what == "semua":
        for f in cerita.carousel_pot(video=True):
            print(f)
