# Spesifikasi minggu 17 Tenang (@diam.dan.percaya): Minggu 17 Jan – Sabtu 23 Jan 2027

- Modul gaya: `gaya_w17.py`, dengan `MOD = "tenang_w17"` dan `MULAI = dt.date(2027, 1, 17)`.
- Modul konten: `konten/tenang_w17.py`.
- Hari 1 = Minggu 17 Jan … hari 7 = Sabtu 23 Jan.
- Slot sama dengan minggu 15 (lihat `riset/SPEK_W15.md`): 12 per hari, Reels di `siang2` dan `malam0`.

Gaya BARU diambil dari `riset/RISET_GAYA_JAN2027.md`. Baca bagian konsepnya (tampilan, palet, font, field, catatan Pillow). Sampel ayat di riset hanya contoh: penulis konten boleh memakai ayat lain, asal tidak berulang.

## Tema harian

| Hari | Tanggal | Tema |
|---|---|---|
| 1 | Minggu 17 Jan | Yesus memanggil murid-murid pertama di danau Galilea: "Mari, ikutlah Aku" |
| 2 | Senin 18 Jan | Panggilan di pekerjaan sehari-hari: bekerja seperti untuk Tuhan (Yesus sendiri tukang kayu) |
| 3 | Selasa 19 Jan | Meninggalkan jala: apa yang perlu dilepas supaya bisa mengikut |
| 4 | Rabu 20 Jan | "Mari dan lihatlah": Andreas membawa Simon, mengajak orang lain kepada Yesus |
| 5 | Kamis 21 Jan | Karunia untuk melayani: yang kecil di tangan Yesus (lima roti dua ikan) |
| 6 | Jumat 22 Jan | Memikul salib setiap hari; upah dari Tuhan, bukan pujian manusia |
| 7 | Sabtu 23 Jan | Kuk yang enak dan beban yang ringan; mendengar suara Gembala; Sabtu malam = "malam Minggu" |

## Format

### BARU (3 item per format; tulis di gaya_wNN.py)

Semua item juga punya `ayat`, `ref`, `caption`. Field mengikuti riset; ≤ = batas karakter.

| Format | Riset | Field |
|---|---|---|
| JARING | §21 fishing net (image) | `judul ≤24 · lokasi ≤26 · ayat ≤130 · ref · caption` |
| PERAHU | §22 paper-boat folding diagram (image) | `judul ≤20 · langkah[6] ≤18 · penutup ≤36 · ayat ≤150 · ref · caption` |
| BENDERA | §23 signal flags spell IKUT (image) | `kata 3–6 letters A–Z · arti ≤24 · ayat ≤140 · ref · caption` |
| PERKAKAS | §24 carpenter's shadow board (image) | `judul ≤20 · alat[5–6] ≤10 · kosong index · label_kosong ≤14 · ayat ≤170 · ref · caption` |
| PLANG | §25 hand-painted roadside sign (image) | `judul ≤14 · baris[2] ≤28 · arah ≤10 · ayat ≤170 · ref · caption` |
| CONGKLAK | §26 sowing one shell at a time (image) | `judul ≤24 · isi[16] 0–9 · ayat ≤170 · ref · caption` |
| ALUR | §27 discipleship flowchart (image) | `mulai ≤30 · tanya ≤12 · ya[2] ≤22 · tidak ≤22 · akhir ≤16 · ayat ≤160 · ref · caption` |
| LOWONGAN | §28 tear-off flyer (image) | `judul ≤10 · sub ≤26 · syarat[4] ≤32 · tab ≤18 · robek indices · ayat ≤170 · ref · caption` |
| UPAH | §29 pay envelope (image) | `judul ≤30 · baris[5] = [jam ≤5, nama ≤12, upah ≤10] · cap ≤8 · ayat ≤180 · ref · caption` |
| BEKAL | §30 five loaves, two fish (image) | `catatan ≤24 · baris ≤56 · ayat ≤140 · ref · caption` |
| DOMINO (Reels) | §R5 one call leads to another (Reel, 12 s) | `nama[10–14] ≤10 · judul ≤30 · ayat ≤160 · ref` |
| RADIO (Reels) | §R6 tuning in (Reel, 13 s) | `frekuensi ≤6 · gangguan[4] ≤12 · lcd ≤18 · ayat ≤150 · ref` |

### LAMA (skema sama dengan modul aslinya)

| Format | Jumlah | Skema dari |
|---|---|---|
| VENN | 2 | tenang_w12.VENN |
| PERJALANAN | 2 | tenang_w12.PERJALANAN |
| WATERCOLOR | 2 | tenang_w12.WATERCOLOR |
| KOPI | 2 | tenang_w12.KOPI |
| BOTANI | 2 | tenang_w13.BOTANI |
| ARTIKEL | 2 | tenang_w13.ARTIKEL |
| KARTUFOTO | 2 | tenang_w13.KARTUFOTO |
| KATAKUNCI | 2 | tenang_w13.KATAKUNCI |
| ULASAN | 2 | tenang_w14.ULASAN |
| TITIK (Reels) | 3 | tenang_w13.TITIK |
| JAMPASIR (Reels) | 3 | tenang_w10.JAMPASIR |
| NAPAS (Reels) | 2 | tenang_w14.NAPAS |

### CAMPUR (gaya lama di latar/efek baru minggu ini; skema = gaya lama)

Latar dan efek baru minggu ini (dibuat di gaya_wNN.py):

- **KAYU:** papan kayu meja kerja tukang kayu / lambung perahu: serat kayu hangat, sedikit serbuk gergaji
- **DANAU:** danau Galilea subuh: air tenang biru-abu, kabut tipis, garis bukit, langit pucat
- **SENJA:** EFEK pada gambar jadi: cahaya keemasan sore (golden hour) + vinyet lembut

| Format | Jumlah | Skema dari | Latar/efek |
|---|---|---|---|
| STICKYKAYU | 2 | tenang_w8.STICKY | KAYU |
| POLAROIDDANAU | 2 | tenang_w7.POLAROID | DANAU |
| TIKETDANAU | 2 | tenang_w7.TIKET | DANAU |
| RESEPKAYU | 2 | tenang_w9.RESEP | KAYU |
| BALONDANAU | 2 | tenang_w12.BALON | DANAU |
| TELEGRAMKAYU | 2 | tenang_w10.TELEGRAM | KAYU |
| KAMUSSENJA | 2 | tenang_w7.KAMUS | SENJA |
| PHOTOBOOTHKAYU | 1 | tenang_w11.PHOTOBOOTH | KAYU |
| FLIPDANAU | 1 | tenang_w11.FLIPCLOCK | DANAU |
| MAJALAHDANAU | 1 | tenang_w10.MAJALAH | DANAU |
| KETIKSENJA | 1 | tenang_w7.KETIK | SENJA |
| EMAILSENJA | 1 | tenang_w12.EMAIL | SENJA |

Catatan isi campuran:
- **BALON/FLIPCLOCK:** wajib punya `label` dan `sublabel` yang cocok (bukan "menuju Natal").
- **foto/lukisan:** hanya fajar/laut/kabut/bintang.

### KOMIK

| Format | Jumlah | Skema dari |
|---|---|---|
| KOMIK | 3 | tenang_w13.KOMIK (Eli bersama Yesus) |

## JADWAL (salin persis ke konten/tenang_w17.py)

```python
JADWAL = {
    1: {"pagi": ("PERKAKAS", 0), "pagi3": ("RESEPKAYU", 0), "pagi2": ("KATAKUNCI", 0), "siang0": ("BEKAL", 0), "siang": ("BALONDANAU", 0), "siang2": ("RADIO", 0), "sore": ("PLANG", 0), "sore2": ("CONGKLAK", 0), "petang": ("POLAROIDDANAU", 0), "malam0": ("TITIK", 0), "malam": ("UPAH", 0), "larut": ("KETIKSENJA", 0)},
    2: {"pagi": ("ALUR", 0), "pagi3": ("KOPI", 0), "pagi2": ("ARTIKEL", 0), "siang0": ("CONGKLAK", 1), "siang": ("PLANG", 1), "siang2": ("DOMINO", 0), "sore": ("STICKYKAYU", 0), "sore2": ("LOWONGAN", 0), "petang": ("VENN", 0), "malam0": ("TITIK", 1), "malam": ("RESEPKAYU", 1), "larut": ("KOMIK", 0)},
    3: {"pagi": ("ALUR", 1), "pagi3": ("BENDERA", 0), "pagi2": ("PERJALANAN", 0), "siang0": ("POLAROIDDANAU", 1), "siang": ("ULASAN", 0), "siang2": ("RADIO", 1), "sore": ("BOTANI", 0), "sore2": ("TIKETDANAU", 0), "petang": ("PERKAKAS", 1), "malam0": ("JAMPASIR", 0), "malam": ("ARTIKEL", 1), "larut": ("KARTUFOTO", 0)},
    4: {"pagi": ("BEKAL", 1), "pagi3": ("LOWONGAN", 1), "pagi2": ("PERJALANAN", 1), "siang0": ("PERAHU", 0), "siang": ("PLANG", 2), "siang2": ("RADIO", 2), "sore": ("STICKYKAYU", 1), "sore2": ("ULASAN", 1), "petang": ("BENDERA", 1), "malam0": ("JAMPASIR", 1), "malam": ("VENN", 1), "larut": ("KOMIK", 1)},
    5: {"pagi": ("KATAKUNCI", 1), "pagi3": ("WATERCOLOR", 0), "pagi2": ("BALONDANAU", 1), "siang0": ("EMAILSENJA", 0), "siang": ("TELEGRAMKAYU", 0), "siang2": ("DOMINO", 1), "sore": ("JARING", 0), "sore2": ("LOWONGAN", 2), "petang": ("PHOTOBOOTHKAYU", 0), "malam0": ("NAPAS", 0), "malam": ("KAMUSSENJA", 0), "larut": ("PERAHU", 1)},
    6: {"pagi": ("JARING", 1), "pagi3": ("TELEGRAMKAYU", 1), "pagi2": ("UPAH", 1), "siang0": ("ALUR", 2), "siang": ("BENDERA", 2), "siang2": ("DOMINO", 2), "sore": ("BEKAL", 2), "sore2": ("BOTANI", 1), "petang": ("FLIPDANAU", 0), "malam0": ("JAMPASIR", 2), "malam": ("CONGKLAK", 2), "larut": ("KOMIK", 2)},
    7: {"pagi": ("MAJALAHDANAU", 0), "pagi3": ("JARING", 2), "pagi2": ("PERKAKAS", 2), "siang0": ("KAMUSSENJA", 1), "siang": ("PERAHU", 2), "siang2": ("TITIK", 2), "sore": ("KOPI", 1), "sore2": ("UPAH", 2), "petang": ("KARTUFOTO", 1), "malam0": ("NAPAS", 1), "malam": ("WATERCOLOR", 1), "larut": ("TIKETDANAU", 1)},
}
```

## Aturan isi

- **Sebutan Tuhan selalu huruf besar:** Tuhan, TUHAN (sesuai TB), Allah, Yesus, Kristus, Bapa, Roh Kudus, Kerajaan (Allah), Aku/-Ku, Engkau/Kau/-Mu, Dia/Ia/-Nya. Ini berlaku juga di kueri SEARCH, judul, label, dan teks gaya apa pun. Huruf kecil hanya di tempat yang memang begitu di TB, atau untuk "aku" manusia (doa kita).
- **Ayat:**
  - Kutipan ayat TB kata per kata. Periksa dengan `python3 cek_modul.py tenang_w17`: semua harus lolos (kemiripan ≥ 0,97, huruf besar benar).
  - Satu referensi hanya dipakai sekali dalam minggu ini.
  - Jangan memakai referensi yang sudah muncul di `konten/tenang_w7.py` … `tenang_w15.py` dan minggu lain yang sudah ada di folder konten/.
  - Penomoran Mazmur mengikuti TB.
- **Waktu:**
  - Kata waktu harus cocok dengan slot: pagi (06:00–10:30), siang (12:00–13:30), sore (15:00–16:30), petang/malam (18:00–22:30).
  - Nama hari harus benar sesuai tanggal di atas. Sabtu malam = "malam Minggu"; Minggu malam ditulis "Minggu malam".
- **Caption** (bahasa Indonesia hangat, seperti minggu-minggu sebelumnya):
  - Pembuka singkat + emoji.
  - 2–4 kalimat konteks ayat (siapa, kapan, mengapa), tanpa menggurui.
  - `📖 “…” — Ref`.
  - Penutup berupa ajakan atau pertanyaan ("Ketik … kalau …").
  - Tanpa hashtag; hashtag ditambahkan otomatis.
- Teks di gambar harus muat dalam batas karakter di atas.
