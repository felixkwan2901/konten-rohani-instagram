"""Contoh carousel untuk 2 calon akun baru:
  - Akhir zaman  : gelap & sinematik, emas. Contoh: 5 tanda akhir zaman di Matius 24 (+ pengingat: tidak ada yang tahu harinya).
  - Ayat langka  : kertas kuno, tinta coklat, referensi merah. Contoh: Eutikhus yang ketiduran saat khotbah (Kis 20).

  python3 akun_baru.py   # hasil di output/contoh/akhirzaman_*.jpg dan ayatlangka_*.jpg
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import render
from render import W, H, font, grain, wrap

OUT = render.OUT / "contoh"


def draw_blocks(d, x, y, items, maxw, align="left"):
    """items: (teks, font, warna, jarak_bawah). teks '' = jeda. Mengembalikan y akhir."""
    for text, fnt, color, gap in items:
        if text:
            for ln in wrap(d, text, fnt, maxw):
                if align == "center":
                    d.text((W / 2, y), ln, font=fnt, fill=color, anchor="ma")
                else:
                    d.text((x, y), ln, font=fnt, fill=color)
                y += fnt.size * 1.32
        y += gap
    return y


def spaced(text):
    return " ".join(text)


# ---------- akun akhir zaman ----------

AZ_BG, AZ_TEXT, AZ_GOLD, AZ_DIM = "#0B0B0D", "#EDE7DA", "#C9A84C", "#A39C90"
AZ_HANDLE = "akhir.zaman.alkitab"

AZ_TANDA = [
    ("Banyak penyesat", "“Waspadalah supaya jangan ada orang yang menyesatkan kamu! Sebab banyak orang akan datang dengan memakai nama-Ku dan berkata: Akulah Mesias, dan mereka akan menyesatkan banyak orang.”",
     "Matius 24:4-5", "Tidak semua yang memakai nama Yesus berasal dari Yesus. Uji semuanya dengan Firman."),
    ("Deru perang", "“Kamu akan mendengar deru perang atau kabar-kabar tentang perang. Namun berawas-awaslah jangan kamu gelisah; sebab semuanya itu harus terjadi, tetapi itu belum kesudahannya.”",
     "Matius 24:6", "Perhatikan: Yesus sendiri berkata jangan gelisah. Itu belum kesudahannya."),
    ("Kelaparan & gempa bumi", "“Sebab bangsa akan bangkit melawan bangsa, dan kerajaan melawan kerajaan. Akan ada kelaparan dan gempa bumi di berbagai tempat.”",
     "Matius 24:7", "Menurut ayat 8, semua ini barulah permulaan, bukan akhirnya."),
    ("Kasih yang menjadi dingin", "“Dan karena makin bertambahnya kedurhakaan, maka kasih kebanyakan orang akan menjadi dingin.”",
     "Matius 24:12", "Tanda yang paling dekat dengan kita: hati yang makin cuek pada Tuhan dan sesama."),
    ("Injil ke seluruh dunia", "“Dan Injil Kerajaan ini akan diberitakan di seluruh dunia menjadi kesaksian bagi semua bangsa, sesudah itu barulah tiba kesudahannya.”",
     "Matius 24:14", "Satu-satunya tanda yang bukan untuk ditakuti, tapi untuk dikerjakan."),
]

AZ_CAPTION = """5 tanda akhir zaman yang disebut Yesus sendiri 🕯️

Bukan teori konspirasi, bukan tebak-tebakan tanggal. Langsung dari perkataan Yesus di Matius 24.

Dan jangan lewatkan slide terakhir: Yesus justru menutup semuanya dengan “jangan gelisah” dan “berjaga-jagalah”.

Menurut kamu, tanda nomor berapa yang paling terasa sekarang? Tulis angkanya di komentar 👇

Save untuk dibaca ulang & kirim ke temanmu 🔖
.
.
#akhirzaman #matius24 #kedatanganyesus #nubuatanalkitab #alkitab #kristenindonesia #berjagajaga"""


def az_base(n, total):
    img = Image.new("RGB", (W, H), AZ_BG)
    arr = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = np.exp(-(((xx - W * 0.8) / 700) ** 2 + ((yy + 100) / 600) ** 2))[..., None] * np.array([70, 16, 16])
    img = grain(Image.fromarray(np.clip(arr + glow, 0, 255).astype(np.uint8)), 0.2)
    d = ImageDraw.Draw(img)
    d.text((90, 80), spaced("AKHIR ZAMAN · MATIUS 24"), font=font("sans_bold", 20), fill=AZ_GOLD)
    d.text((W - 90, 80), f"{n}/{total}", font=font("sans_bold", 20), fill=AZ_DIM, anchor="ra")
    d.text((90, H - 90), "@" + AZ_HANDLE, font=font("sans_bold", 20), fill=AZ_DIM)
    return img, d


def akhir_zaman():
    total = len(AZ_TANDA) + 2
    files = []
    img, d = az_base(1, total)
    y = draw_blocks(d, 90, 420, [("5 tanda akhir zaman", font("serif", 84), AZ_TEXT, 0),
                                 ("yang disebut Yesus", font("serif", 84), AZ_TEXT, 0),
                                 ("sendiri.", font("serif_italic", 84), AZ_GOLD, 40)], 900)
    d.line((90, y, 250, y), fill=AZ_GOLD, width=3)
    draw_blocks(d, 90, y + 40, [("Bukan teori, bukan tebakan tanggal.", font("sans", 34), AZ_DIM, 6),
                                ("Langsung dari Matius 24.", font("sans", 34), AZ_DIM, 0)], 900)
    d.text((W - 90, H - 90), "geser  ›", font=font("sans_bold", 26), fill=AZ_TEXT, anchor="ra")
    files.append(img)
    for i, (title, verse, ref, note) in enumerate(AZ_TANDA, 1):
        img, d = az_base(i + 1, total)
        d.text((W - 60, 150), f"0{i}", font=font("serif", 420), fill="#1E1C1E", anchor="ra")
        y = draw_blocks(d, 90, 330, [(f"Tanda {i}", font("sans_bold", 26), AZ_GOLD, 14),
                                     (title, font("serif", 64), AZ_TEXT, 30)], 900)
        d.line((90, y, 250, y), fill=AZ_GOLD, width=3)
        y = draw_blocks(d, 90, y + 40, [(verse, font("serif_italic", 38), AZ_TEXT, 16),
                                        (ref, font("sans_bold", 26), AZ_GOLD, 50)], 900)
        draw_blocks(d, 90, y, [(note, font("sans", 34), AZ_DIM, 0)], 880)
        files.append(img)
    img, d = az_base(total, total)
    y = draw_blocks(d, 90, 300, [("Tapi ingat.", font("serif", 84), AZ_TEXT, 40),
                                 ("“Tetapi tentang hari dan saat itu tidak seorang pun yang tahu, malaikat-malaikat di sorga tidak, dan Anak pun tidak, hanya Bapa sendiri.”",
                                  font("serif_italic", 38), AZ_TEXT, 14),
                                 ("Matius 24:36", font("sans_bold", 26), AZ_GOLD, 50),
                                 ("Yang Yesus minta bukan menebak tanggal, tapi:", font("sans", 34), AZ_DIM, 18),
                                 ("“Berjaga-jagalah, sebab kamu tidak tahu pada hari mana Tuhanmu datang.”", font("serif_italic", 38), AZ_TEXT, 14),
                                 ("Matius 24:42", font("sans_bold", 26), AZ_GOLD, 0)], 900)
    d.text((W - 90, H - 90), "save & kirim", font=font("sans_bold", 26), fill=AZ_TEXT, anchor="ra")
    files.append(img)
    return save_all(files, "akhirzaman", AZ_CAPTION)


AZ_TEBAK = [
    ("1844", "William Miller", "Pengkhotbah Amerika ini menghitung nubuat Daniel dan menyimpulkan Yesus datang sekitar 1843–1844. Tanggalnya kemudian ditetapkan 22 Oktober 1844. Puluhan ribu orang menunggu, sebagian bahkan menjual harta mereka.",
     "Tidak terjadi apa-apa. Peristiwa itu dikenal sebagai “Kekecewaan Besar”."),
    ("1988", "Edgar Whisenant", "Mantan insinyur NASA ini menulis “88 Alasan Pengangkatan Terjadi Tahun 1988”. Jutaan eksemplar tersebar. Tanggalnya: sekitar 11–13 September 1988.",
     "Meleset. Ia lalu merevisi ke 1989, dan meleset lagi."),
    ("2011", "Harold Camping", "Pemilik jaringan radio Kristen ini memasang papan reklame di banyak negara: pengangkatan terjadi 21 Mei 2011. Sebelumnya ia juga pernah menunjuk tahun 1994.",
     "Meleset, lalu direvisi ke 21 Oktober 2011. Meleset lagi. Ia kemudian mengakui kesalahannya."),
    ("2017", "“Tanda Wahyu 12”", "Tafsiran posisi bintang dan planet menurut Wahyu 12 menyebar luas di internet, dengan klaim akhir zaman dimulai 23 September 2017.",
     "Tanggalnya lewat seperti hari biasa."),
]

AZ_TEBAK_CAPTION = """4 kali orang menebak tanggal kiamat. Semuanya meleset 🕰️

1844, 1988, 2011, 2017. Banyak dari mereka orang yang tulus. Tapi setiap kali meleset, banyak jemaat kecewa, dan nama Tuhan ditertawakan.

Padahal Yesus sendiri sudah bilang: “tentang hari dan saat itu tidak seorang pun yang tahu” (Matius 24:36).

Jadi kalau ada video atau pesan berantai yang menyebut tahun kedatangan Yesus, termasuk yang ramai soal 2030, ingat slide terakhir ini.

Pernah dapat pesan “kiamat tanggal sekian” di grup WA? Cerita di komentar 👇

Save & kirim ke keluargamu 🔖
.
.
#akhirzaman #kedatanganyesus #matius24 #nubuatanalkitab #alkitab #kristenindonesia #berjagajaga"""


def tebak_tanggal():
    """Contoh carousel akun akhir zaman: 4 kali orang menebak tanggal kiamat."""
    total = len(AZ_TEBAK) + 3
    files = []
    img, d = az_base(1, total)
    y = draw_blocks(d, 90, 400, [("4 kali orang", font("serif", 84), AZ_TEXT, 0),
                                 ("menebak tanggal kiamat.", font("serif", 84), AZ_TEXT, 0),
                                 ("Semuanya meleset.", font("serif_italic", 84), AZ_GOLD, 40)], 900)
    d.line((90, y, 250, y), fill=AZ_GOLD, width=3)
    draw_blocks(d, 90, y + 40, [("Dan apa yang sebenarnya Yesus katakan.", font("sans", 34), AZ_DIM, 0)], 900)
    d.text((W - 90, H - 90), "geser  ›", font=font("sans_bold", 26), fill=AZ_TEXT, anchor="ra")
    files.append(img)
    for i, (year, who, what, result) in enumerate(AZ_TEBAK, 1):
        img, d = az_base(i + 1, total)
        d.text((90, 230), year, font=font("serif", 220), fill=AZ_GOLD)
        y = draw_blocks(d, 90, 520, [(f"Tebakan {i}", font("sans_bold", 26), AZ_GOLD, 12),
                                     (who, font("serif", 58), AZ_TEXT, 28)], 900)
        d.line((90, y, 250, y), fill=AZ_GOLD, width=3)
        y = draw_blocks(d, 90, y + 36, [(what, font("sans", 34), AZ_TEXT, 30)], 900)
        draw_blocks(d, 90, y, [("Hasilnya:", font("sans_bold", 26), AZ_GOLD, 10), (result, font("serif_italic", 38), AZ_TEXT, 0)], 900)
        files.append(img)
    img, d = az_base(total - 1, total)
    draw_blocks(d, 90, 300, [("Apa kata Yesus?", font("serif", 80), AZ_TEXT, 40),
                             ("“Tetapi tentang hari dan saat itu tidak seorang pun yang tahu, malaikat-malaikat di sorga tidak, dan Anak pun tidak, hanya Bapa sendiri.”",
                              font("serif_italic", 38), AZ_TEXT, 14),
                             ("Matius 24:36", font("sans_bold", 26), AZ_GOLD, 44),
                             ("“Engkau tidak perlu mengetahui masa dan waktu, yang ditetapkan Bapa sendiri menurut kuasa-Nya.”",
                              font("serif_italic", 38), AZ_TEXT, 14),
                             ("Kisah Para Rasul 1:7", font("sans_bold", 26), AZ_GOLD, 0)], 900)
    files.append(img)
    img, d = az_base(total, total)
    draw_blocks(d, 90, 280, [("Jadi, kita harus bagaimana?", font("serif", 70), AZ_TEXT, 40),
                             ("“Sebab itu, hendaklah kamu juga siap sedia, karena Anak Manusia datang pada saat yang tidak kamu duga.”",
                              font("serif_italic", 38), AZ_TEXT, 14),
                             ("Matius 24:44", font("sans_bold", 26), AZ_GOLD, 44),
                             ("Bukan menghitung tahun, tapi hidup setia hari ini.", font("sans", 34), AZ_DIM, 12),
                             ("Kalau ada yang menyebut tanggal kedatangan Yesus, termasuk soal 2030, uji dengan ayat ini.", font("sans", 34), AZ_DIM, 0)], 900)
    d.text((W - 90, H - 90), "save & kirim", font=font("sans_bold", 26), fill=AZ_TEXT, anchor="ra")
    files.append(img)
    return save_all(files, "akhirzaman_tebaktanggal", AZ_TEBAK_CAPTION)


# ---------- akun ayat langka ----------

AL_PAPER, AL_INK, AL_RED, AL_DIM = "#F1E6CC", "#3B2A1A", "#9B2C2C", "#7A6650"
AL_HANDLE = render.config.AKUN["ayat"]["handle"]

AL_CAPTION = """Ada orang yang ketiduran waktu khotbah… lalu jatuh dari lantai 3. Dan itu ada di Alkitab 😳

Kisah Para Rasul 20:7-12. Paulus berkhotbah sampai tengah malam, seorang pemuda bernama Eutikhus tertidur di jendela, jatuh, dan diangkat sudah meninggal. Tapi ceritanya tidak berhenti di situ.

Yang kami suka dari kisah ini: gereja mula-mula juga berisi orang biasa yang bisa capek dan ngantuk. Dan Tuhan tetap bekerja di tengah mereka.

Pernah baca kisah ini sebelumnya? Jawab: PERNAH / BARU TAHU 👇

Follow untuk ayat-ayat lain yang jarang dibahas 📜
.
.
#ayatalkitab #faktaalkitab #kisahpararasul #alkitab #kristenindonesia #belajaralkitab #ayattersembunyi"""


AL_TEMA = {  # bg, teks, aksen, redup, gelap?  -- gelap & terang diselang-seling dalam seminggu
    "malam":    ("#1E2A44", "#F1E6CC", "#D4A24C", "#A9A08C", True),
    "gurun":    ("#F3DDBF", "#3B2414", "#B5542D", "#8A6A4E", False),
    "mata_air": ("#1F4E4F", "#F1E9D6", "#E0B25A", "#A8B8AE", True),
    "jalan":    ("#DCE3CC", "#2E3A20", "#8A4B2A", "#6B7556", False),
    "plum":     ("#3A2238", "#F3E6E0", "#D9A6A0", "#B39AA8", True),
    "debu":     ("#D9D2C5", "#2F2A24", "#8C2F39", "#6E665B", False),
    "perkamen": (AL_PAPER, AL_INK, AL_RED, AL_DIM, False),
    "laut":     ("#12324A", "#E8F0EF", "#7FC4C9", "#9FB5BC", True),
    "badai":    ("#2B3036", "#ECEAE4", "#9FB4C7", "#A4A7AB", True),
}

AL_STYLE = {  # jenis baris -> (font, ukuran, peran warna, jarak bawah default)
    "judul": ("serif", 72, "ink", 0), "judul2": ("serif_italic", 68, "accent", 0), "sub": ("serif", 56, "ink", 30),
    "label": ("sans_bold", 26, "accent", 20), "teks": ("serif", 44, "ink", 24), "kutip": ("serif_italic", 44, "ink", 14),
    "kutip_kecil": ("serif_italic", 38, "ink", 14), "ref": ("sans_bold", 26, "accent", 0), "poin": ("serif", 40, "ink", 18),
    "kecil": ("sans", 34, "dim", 0),
}


def al_base(n, total, nomor=1, tema="perkamen", invert=False, header=None):
    bg, ink, accent, dim, dark = AL_TEMA[tema]
    if invert:  # slide penutup: warna dibalik supaya menonjol
        # latar = warna aksen; semua teks memakai warna latar asli (gelap di atas terang, terang di atas gelap)
        bg, ink, accent, dim, dark = accent, bg, bg, bg, not dark
    rng = np.random.default_rng(n + nomor * 10)
    arr = np.asarray(Image.new("RGB", (W, H), bg)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = np.clip(1 - np.minimum.reduce([xx, W - xx, yy, H - yy]) / 200, 0, 1)[..., None] ** 2
    stains = render.fbm2d(H, W, rng, ((3, 1.0), (8, 0.5)))[..., None]
    arr = arr * (1 - edge * (0.45 if dark else 0.3)) - (stains - 0.5) * (18 if dark else 30)
    img = grain(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), 0.28)
    d = ImageDraw.Draw(img)
    d.rectangle((50, 50, W - 50, H - 50), outline=accent, width=2)
    d.rectangle((62, 62, W - 62, H - 62), outline=dim, width=1)
    d.text((W / 2, 110), spaced(header or f"AYAT YANG JARANG DIBAHAS · #{nomor:02d}"), font=font("sans_bold", 20), fill=accent, anchor="ma")
    d.text((W / 2, H - 120), f"@{AL_HANDLE}" if total == 1 else f"{n} / {total}   ·   @{AL_HANDLE}", font=font("sans_bold", 20), fill=dim, anchor="ma")
    return img, d, {"ink": ink, "accent": accent, "dim": dim, "bg": bg}


def rows_to_items(rows, colors, size_scale=1.0):
    items = []
    for row in rows:
        kind, text = row[0], row[1]
        fk, size, role, gap = AL_STYLE[kind]
        items.append((text, font(fk, int(size * size_scale)), colors[role], row[2] if len(row) > 2 else gap))
    return items


def block_height(items, maxw):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    return sum(sum(it[1].size * 1.32 for _ in wrap(probe, it[0], it[1], maxw)) + it[3] for it in items)


def ayat_carousel(post, nomor, folder="ayat"):
    """Satu carousel dari konten/ayat.py -> output/<folder>/hari<nomor>_<n>.jpg.
    Tata letak: sampul rata kiri + nomor besar, slide ayat dengan tanda kutip besar,
    slide pelajaran sebagai kartu bernomor, slide penutup dengan warna dibalik."""
    tema = post.get("tema", "perkamen")
    slides = post["slides"]
    paths = []
    for n, rows in enumerate(slides, 1):
        last = n == len(slides)
        img, d, c = al_base(n, len(slides), nomor, tema, invert=last)
        kinds = [r[0] for r in rows]
        if n == 1:  # sampul
            d.text((110, 190), f"No. {nomor:02d}", font=font("serif_italic", 64), fill=c["accent"])
            items = rows_to_items(rows, c, 1.1)
            y = draw_blocks(d, 110, 470, items[:-1], 860)
            d.line((110, y + 10, 290, y + 10), fill=c["accent"], width=4)
            draw_blocks(d, 110, y + 50, items[-1:], 860)
        elif kinds[0] == "peta":  # diagram arah: Tarsis (barat) <- Yafo -> Niniwe (timur)
            y0 = 560
            d.text((W / 2, 250), "Ke mana seharusnya, dan ke mana ia pergi", font=font("serif", 46), fill=c["ink"], anchor="ma")
            d.line((150, y0, W - 150, y0), fill=c["dim"], width=3)
            for x, name, sub in ((170, "TARSIS", "barat · ujung dunia"), (W / 2, "YAFO", "pelabuhan"), (W - 170, "NINIWE", "timur · ±900 km")):
                d.ellipse((x - 16, y0 - 16, x + 16, y0 + 16), fill=c["accent"] if name != "YAFO" else c["ink"])
                d.text((x, y0 + 40), name, font=font("sans_bold", 30), fill=c["ink"], anchor="ma")
                d.text((x, y0 + 82), sub, font=font("sans", 26), fill=c["dim"], anchor="ma")
            for (xa, xb, label, col) in ((W / 2 - 40, 230, "ARAH YUNUS", c["accent"]), (W / 2 + 40, W - 230, "PERINTAH TUHAN", c["ink"])):
                yy2 = y0 - 90 if col == c["ink"] else y0 + 170
                d.line((xa, yy2, xb, yy2), fill=col, width=6)
                tip = 1 if xb > xa else -1
                d.polygon([(xb, yy2), (xb - tip * 26, yy2 - 16), (xb - tip * 26, yy2 + 16)], fill=col)
                d.text(((xa + xb) / 2, yy2 - 48 if col == c["ink"] else yy2 + 22), label, font=font("sans_bold", 24), fill=col, anchor="ma")
            draw_blocks(d, 110, 900, [("Berlawanan 180°. Bukan tersesat, tapi disengaja.", font("serif_italic", 44), c["ink"], 0)], 860, align="center")
        elif "tangga" in kinds:  # baris menurun bertingkat
            head = rows_to_items([r for r in rows if r[0] != "tangga"], c)
            y = draw_blocks(d, 110, 240, head, 860, align="center") + 40
            steps = [r[1] for r in rows if r[0] == "tangga"]
            for i, text in enumerate(steps):
                x = 130 + i * 120
                d.line((x, y + 30, x, y + 140), fill=c["accent"], width=4)
                d.polygon([(x, y + 160), (x - 14, y + 134), (x + 14, y + 134)], fill=c["accent"])
                d.text((x + 34, y + 60), "TURUN", font=font("sans_bold", 26), fill=c["accent"])
                for j, ln in enumerate(wrap(d, text, font("serif", 40), W - x - 200)):
                    d.text((x + 34, y + 96 + j * 50), ln, font=font("serif", 40), fill=c["ink"])
                y += 230
        elif "poin" in kinds:  # pelajaran -> kartu bernomor
            head = [r for r in rows if r[0] != "poin"]
            pts = [r[1].split(".", 1)[1].strip() if r[1][:2].strip().rstrip(".").isdigit() else r[1] for r in rows if r[0] == "poin"]
            items = rows_to_items([r for r in head if r[0] == "sub"], c)
            y = draw_blocks(d, 110, 260, items, 860, align="center") + 10
            card = tuple(int(v * 0.9 + (255 if not AL_TEMA[tema][4] else 40) * 0.1) for v in Image.new("RGB", (1, 1), c["bg"]).getpixel((0, 0)))
            f = font("serif", 38)
            for i, text in enumerate(pts, 1):
                lines = wrap(d, text, f, 700)
                h = len(lines) * 50 + 56
                d.rounded_rectangle((110, y, W - 110, y + h), radius=22, fill=card, outline=c["dim"], width=1)
                d.ellipse((140, y + h / 2 - 32, 204, y + h / 2 + 32), fill=c["accent"])
                d.text((172, y + h / 2), str(i), font=font("sans_bold", 32), fill=c["bg"], anchor="mm")
                for j, ln in enumerate(lines):
                    d.text((236, y + 28 + j * 50), ln, font=f, fill=c["ink"])
                y += h + 22
            rest = [r for r in head if r[0] != "sub"]
            if rest:
                draw_blocks(d, 110, y + 20, rows_to_items(rest, c), 860, align="center")
        else:
            if "kutip" in kinds or "kutip_kecil" in kinds:  # tanda kutip besar
                d.text((95, 150), "“", font=font("serif", 300), fill=c["dim"])
            items = rows_to_items(rows, c, 1.06 if last else 1.0)
            draw_blocks(d, 110, (H - block_height(items, 860)) / 2 + 20, items, 860, align="center")
        path = render.OUT / folder / f"hari{nomor}_{n}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(path, "JPEG", quality=92)
        paths.append(path)
    return paths


MINGGU_AYAT = ["ayat", "ayat_minggu2", "ayat_minggu3"]  # modul konten per minggu, berurutan


def render_ayat(modul="ayat"):
    """Semua post satu minggu @ayat.tersembunyi -> output/<modul>/hari<n>_<slide>.jpg."""
    import importlib
    m = importlib.import_module(f"konten.{modul}")
    start = getattr(m, "NOMOR_AWAL", 1)
    folder = render.OUT / modul
    for old in folder.glob("*.jpg"):
        old.unlink()
    out = []
    for i, p in enumerate(m.POSTS):
        pages = ayat_carousel(p, start + i, folder=modul)
        renamed = []
        for n, pg in enumerate(pages, 1):   # nama file per hari minggu itu (hari1..hari7)
            target = pg.with_name(f"hari{i + 1}_{n}.jpg")
            pg.replace(target)
            renamed.append(target)
        out.append((renamed, p["caption"] + "\n.\n.\n" + m.TAGS))
    return out


def fakta_singkat():
    """'Fakta 30 detik' (1 slide) -> [(path, caption)] dari konten/ayat_singkat.py."""
    from konten import ayat_singkat as a
    out = []
    for i, f in enumerate(a.FAKTA, 1):
        img, d, c = al_base(1, 1, i, f["tema"], header="FAKTA 30 DETIK")
        items = [(f["judul"], font("serif", 66), c["ink"], 40), (f["isi"], font("serif_italic", 42), c["ink"], 30),
                 (f["ref"].upper(), font("sans_bold", 26), c["accent"], 0)]
        draw_blocks(d, 110, (H - block_height(items, 860)) / 2, items, 860, align="center")
        path = render.OUT / "ayat_singkat" / f"fakta{i}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(path, "JPEG", quality=92)
        out.append((path, f["caption"] + "\n.\n.\n" + a.TAGS))
    return out


def ayat_langka():
    """Contoh lama (dipakai sebagai referensi di output/contoh)."""
    from konten import ayat
    paths = ayat_carousel(ayat.POSTS[0], 1, folder="contoh")
    renamed = []
    for i, p in enumerate(paths, 1):
        target = p.with_name(f"ayatlangka_{i}.jpg")
        p.replace(target)
        renamed.append(target)
    (OUT / "ayatlangka_caption.txt").write_text(ayat.POSTS[0]["caption"])
    return renamed


def save_all(images, name, caption):
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, im in enumerate(images, 1):
        path = OUT / f"{name}_{i}.jpg"
        im.convert("RGB").save(path, "JPEG", quality=92)
        paths.append(path)
    (OUT / f"{name}_caption.txt").write_text(caption)
    return paths


if __name__ == "__main__":
    for modul in MINGGU_AYAT:
        print(len(render_ayat(modul)), "post @ayat.tersembunyi ->", render.OUT / modul)
    for group in (akhir_zaman(), ayat_langka()):
        tw = 216
        sheet = Image.new("RGB", (len(group) * (tw + 8) + 8, 286), "#DDDDDD")
        for i, p in enumerate(group):
            sheet.paste(Image.open(p).resize((tw, 270)), (8 + i * (tw + 8), 8))
        sheet.save(str(group[0]).rsplit("_", 1)[0] + "_preview.jpg", quality=88)
        print(len(group), "slide ->", group[0].parent)
