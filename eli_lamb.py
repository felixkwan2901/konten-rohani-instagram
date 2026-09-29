"""Eli the Lamb: gambar AI (dibuat di Gemini/ChatGPT) + teks meme + handle -> post 4:5, dan Reels untuk slot malam.

  python3 eli_lamb.py            # proses semua gambar di output/eli_lamb/raw/ -> output/eli_lamb/<id>.jpg (+ Reels)
  python3 eli_lamb.py prompts    # buat lembar prompt (output/eli_lamb/prompts.html) untuk disalin ke Gemini

Nama file mentah = id post, misalnya output/eli_lamb/raw/1-pagi.jpg (hari 1 = Minggu 4 Okt).
"""
import html
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import config
from konten import eli_lamb as el
from render import OUT, font, save, wrap

RAW = OUT / "eli_lamb" / "raw"
W, H = 1080, 1350


def handle():
    return config.AKUN["eli"]["handle"]


def raw_path(pid):
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".PNG"):
        p = RAW / f"{pid}{ext}"
        if p.exists():
            return p
    return None


def cover(img, w, h):
    """Potong tengah supaya pas w x h tanpa gepeng."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def meme_box(img, text, bawah=False):
    """Kotak putih membulat di atas gambar dengan teks hitam tebal (gaya meme Instagram)."""
    d = ImageDraw.Draw(img)
    for size in range(60, 36, -2):
        f = font("sans_bold", size)
        lines = [ln for para in text.split("\n") for ln in wrap(d, para, f, W - 200)]
        lh = int(size * 1.18)
        if len(lines) * lh <= 420:
            break
    bw = max(d.textlength(ln, font=f) for ln in lines) + 70
    bh = len(lines) * lh + 50
    x0, y0 = (W - bw) / 2, (H - bh - 120) if bawah else 70
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((x0, y0 + 6, x0 + bw, y0 + bh + 6), radius=30, fill=(0, 0, 0, 70))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=30, fill=(255, 255, 255, 245))
    y = y0 + 25
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill="#111111", anchor="ma")
        y += lh
    return img


def watermark(img):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((40, H - 70), "@" + handle(), font=font("sans_bold", 28), fill=(255, 255, 255, 230))
    sh = lay.getchannel("A").filter(ImageFilter.GaussianBlur(4))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow.putalpha(sh.point(lambda v: int(v * 0.6)))
    img.alpha_composite(shadow)
    img.alpha_composite(lay)
    return img


def make_post(p):
    src = raw_path(p["id"])
    if not src:
        return None
    img = cover(Image.open(src).convert("RGB"), W, H).convert("RGBA")
    img = watermark(meme_box(img, p["teks"], p["id"] in el.TEKS_BAWAH))
    return save(img, f"eli_lamb/{p['id']}.jpg")


def make_reel(p, image_rel, seconds=8):
    """Gambar 4:5 di atas latar buram 9:16, zoom pelan, lalu musik unik (musik.py)."""
    import cerita
    import musik
    rel = f"reels/eli_lamb/{p['id']}.mp4"
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    post = Image.open(OUT / image_rel).convert("RGB")
    bg = cover(post, 1080, 1920).filter(ImageFilter.GaussianBlur(40))
    ff = cerita.ffmpeg_writer(out, 1080, 1920, 30)
    for n in range(30 * seconds):
        z = 1 + 0.05 * n / (30 * seconds)
        fw, fh = int(W * z), int(H * z)
        frame = bg.copy()
        big = post.resize((fw, fh), Image.BILINEAR).crop(((fw - W) // 2, (fh - H) // 2, (fw - W) // 2 + W, (fh - H) // 2 + H))
        frame.paste(big, (0, 220))
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError(f"ffmpeg gagal untuk {rel}")
    wav, _ = musik.lagu_unik(rel, seconds + 1, set())
    musik.pasang(rel, str(wav))
    return rel


def render_semua():
    """{(hari, slot): (files, caption)} untuk semua post yang gambar mentahnya sudah ada."""
    out = {}
    for p in el.POSTS:
        image = make_post(p)
        if not image:
            continue
        files = [image]
        if p["reel"]:
            reel = f"reels/eli_lamb/{p['id']}.mp4"
            if not (OUT / reel).exists() or (OUT / reel).stat().st_mtime < (OUT / image).stat().st_mtime:
                make_reel(p, image)
            files = [reel]
        out[(p["hari"], p["slot"])] = (files, p["caption"].format(handle=handle()))
    return out


def prompts_html():
    days = ["Minggu 4 Okt", "Senin 5 Okt", "Selasa 6 Okt", "Rabu 7 Okt", "Kamis 8 Okt", "Jumat 9 Okt", "Sabtu 10 Okt"]
    rows = []
    for p in el.POSTS:
        done = "✅" if raw_path(p["id"]) else "⬜"
        who = "👫 Eli + Ruthie (upload kedua foto referensi)" if p.get("pasangan") else "🐑 Eli"
        rows.append(f"""<div class="card"><div class="head">{done} <b>{p['id']}.jpg</b> · {days[p['hari'] - 1]} · {p['slot']} · {who}
<span class="meme">{html.escape(p['teks']).replace(chr(10), ' / ')}</span></div>
<textarea readonly>{html.escape(p['prompt'])}</textarea><button onclick="copyText(this)">Copy prompt</button></div>""")
    page = f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eli the Lamb Prompts</title><style>
body{{font-family:-apple-system,Helvetica,Arial,sans-serif;background:#f6f3ee;color:#1b1b1b;margin:0;padding:16px;max-width:760px;margin:auto}}
h1{{font-size:22px}} .card{{background:#fff;border:1px solid #e3ddd2;border-radius:10px;padding:12px;margin:10px 0}}
.head{{font-size:14px;margin-bottom:6px}} .meme{{display:block;color:#6b6b6b;font-style:italic;margin-top:4px}}
textarea{{width:100%;box-sizing:border-box;height:92px;font-size:13px;border:1px solid #ddd;border-radius:6px;padding:6px}}
button{{margin-top:6px;padding:8px 14px;border:0;border-radius:6px;background:#1b1b1b;color:#fff;font-size:14px}}
.ref{{background:#fff8e6}}</style></head><body>
<h1>🐑 Eli the Lamb — prompt minggu 4–10 Okt</h1>
<div class="card ref"><b>1. Foto referensi (sekali saja)</b><br>Buat di Gemini, pilih yang paling lucu, simpan. Untuk semua post berikutnya: upload foto ini (dan foto Ruthie untuk post 👫) + tempel prompt adegannya, dan tambahkan kalimat <i>"Use the attached lambs as the exact same characters."</i>
<textarea readonly>{html.escape(el.CHARACTER)}. Full body, plain soft background, character reference photo.</textarea><button onclick="copyText(this)">Copy prompt</button></div>
<div class="card ref"><b>1b. Foto referensi Ruthie (istri Eli, sekali saja)</b><br>Upload foto Eli juga dan tambahkan <i>"same style and size as the attached lamb, but a different character"</i>.
<textarea readonly>{html.escape(el.PARTNER)}. Full body, plain soft background, character reference photo.</textarea><button onclick="copyText(this)">Copy prompt</button></div>
<div class="card ref"><b>1c. Foto berdua (opsional, bagus untuk foto profil)</b><br>Upload kedua referensi, lalu:
<textarea readonly>{html.escape(el.COUPLE)}. Scene: Eli and Ruthie sitting close together on a wooden bench on a green New Zealand hillside at golden hour, smiling at the camera, couple portrait.</textarea><button onclick="copyText(this)">Copy prompt</button></div>
<p><b>2. Tiap post:</b> simpan hasilnya dengan nama file di kartu (misalnya <code>1-pagi.jpg</code>) lalu kirim ke Mac, folder <code>konten-rohani-instagram/output/eli_lamb/raw/</code>. Teks meme ditambahkan otomatis, jadi gambarnya harus tanpa tulisan.</p>
{''.join(rows)}
<script>function copyText(b){{const t=b.previousElementSibling;t.select();navigator.clipboard.writeText(t.value);b.textContent='Copied ✓';setTimeout(()=>b.textContent='Copy prompt',1500)}}</script>
</body></html>"""
    path = OUT / "eli_lamb" / "prompts.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page)
    return path


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prompts":
        print(prompts_html())
    else:
        RAW.mkdir(parents=True, exist_ok=True)
        for k, (files, _) in render_semua().items():
            print(k, files)
