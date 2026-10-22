# Spesifikasi minggu 16 Tenang (@diam.dan.percaya): Minggu 10 Jan – Sabtu 16 Jan 2027

- Modul gaya: `gaya_w16.py`, dengan `MOD = "tenang_w16"` dan `MULAI = dt.date(2027, 1, 10)`.
- Modul konten: `konten/tenang_w16.py`.
- Hari 1 = Minggu 10 Jan … hari 7 = Sabtu 16 Jan.
- Slot sama dengan minggu 15 (lihat `riset/SPEK_W15.md`): 12 per hari, Reels di `siang2` dan `malam0`.

Gaya BARU diambil dari `riset/RISET_GAYA_JAN2027.md`. Baca bagian konsepnya (tampilan, palet, font, field, catatan Pillow). Sampel ayat di riset hanya contoh: penulis konten boleh memakai ayat lain, asal tidak berulang.

## Tema harian

| Hari | Tanggal | Tema |
|---|---|---|
| 1 | Minggu 10 Jan | MINGGU PEMBAPTISAN TUHAN: suara Bapa di sungai Yordan, "Engkaulah Anak-Ku yang Kukasihi" |
| 2 | Senin 11 Jan | Dikasihi sebelum berprestasi: identitas bukan dari pekerjaan atau nilai |
| 3 | Selasa 12 Jan | Anak, bukan hamba atau yatim: Roh yang berseru "Abba, ya Bapa" |
| 4 | Rabu 13 Jan | Dikenal dan dipanggil dengan nama (Yes 43:1, Mzm 139) |
| 5 | Kamis 14 Jan | Ciptaan baru: yang lama sudah berlalu, dibentuk tangan Penjunan |
| 6 | Jumat 15 Jan | Tetap berharga ketika merasa gagal atau tersesat (domba yang hilang, anak yang hilang) |
| 7 | Sabtu 16 Jan | Hidup sebagai anak yang dikasihi: mengasihi sesama; Sabtu malam = "malam Minggu" |

## Format

### BARU (3 item per format; tulis di gaya_wNN.py)

Semua item juga punya `ayat`, `ref`, `caption`. Field mengikuti riset; ≤ = batas karakter.

| Format | Riset | Field |
|---|---|---|
| SIDIK | §11 fingerprint (image) | `baris[3] = [label ≤10, isi ≤24] · mikroteks ≤22 · ayat ≤130 · ref · caption` |
| UKUR | §12 growth marks on a door frame (image) | `tanda[4–6] = [label ≤18, tinggi_cm 60–190] · puncak ≤28 · ayat ≤140 · ref · caption` |
| ABJAD | §13 flash card "A untuk Abba" (image) | `huruf (1) · kata ≤10 · sub ≤30 · kartu_belakang[2] = [huruf, kata ≤10] · nomor ≤5 · ayat ≤150 · ref · caption` |
| JAHIT | §14 sewing-pattern tissue (image) | `nomor ≤6 · bagian ≤26 · instruksi ≤30 · ayat ≤150 · ref · caption` |
| TANGRAM | §15 the dove (image) | `judul ≤20 · label_kecil ≤22 · ayat ≤150 · ref · caption` |
| PIKTO | §16 1 of 100 (image) | `judul ≤16 · sub ≤50 · label ≤10 · ayat ≤170 · ref · sumber ≤30 · caption` |
| HURUF | §17 type specimen of "your name" (image) | `nama ≤12 · meta[3] ≤26 · frasa ≤36 · ayat ≤160 · ref · caption` |
| SILSILAH | §18 family tree (image) | `puncak ≤10 · tengah ≤20 · anggota[6–9] ≤10 · sorot ≤8 · cap ≤24 · ayat ≤160 · ref · caption` |
| BATIK | §19 kawung with a cartouche (image) | `motif (kawung/ceplok) · judul ≤20 · ayat ≤170 · ref · caption` |
| MARMER | §20 marbled paper (image) | `judul ≤18 · ayat ≤170 · ref · caption` |
| RIAK (Reels) | §R3 ripples with the Father's voice (Reel, 11 s) | `kata[4] ≤12 · kicker ≤30 · ayat ≤120 · ref · caption` |
| WARNAI (Reels) | §R4 paint by number (Reel, 14 s) | `judul ≤24 · palet[6] ≤10 · ayat ≤160 · ref` |

### LAMA (skema sama dengan modul aslinya)

| Format | Jumlah | Skema dari |
|---|---|---|
| KARTUPOS | 2 | tenang_w8.KARTUPOS |
| PETA | 2 | tenang_w8.PETA |
| SERTIFIKAT | 2 | tenang_w9.SERTIFIKAT |
| JAM | 2 | tenang_w9.JAM |
| RESEP | 2 | tenang_w9.RESEP |
| UNDANGAN | 2 | tenang_w9.UNDANGAN |
| JENDELA | 2 | tenang_w9.JENDELA |
| FILM | 2 | tenang_w10.FILM |
| GARIS | 2 | tenang_w10.GARIS |
| VINYL (Reels) | 3 | tenang_w11.VINYL |
| FLIP (Reels) | 3 | tenang_w8.FLIP |
| PROGRESS (Reels) | 2 | tenang_w9.PROGRESS |

### CAMPUR (gaya lama di latar/efek baru minggu ini; skema = gaya lama)

Latar dan efek baru minggu ini (dibuat di gaya_wNN.py):

- **AIR:** latar air sungai jernih: biru kehijauan, riak cahaya (kaustik) lembut
- **AWAN:** langit awan putih lembut dengan cahaya turun dari atas (seperti burung merpati/terang dari langit)
- **BENING:** EFEK pada gambar jadi: tint aqua bening + pantulan cahaya air (kaustik) tipis

| Format | Jumlah | Skema dari | Latar/efek |
|---|---|---|---|
| STICKYAIR | 2 | tenang_w8.STICKY | AIR |
| POLAROIDAIR | 2 | tenang_w7.POLAROID | AIR |
| TIKETAWAN | 2 | tenang_w7.TIKET | AWAN |
| STAMPAIR | 2 | tenang_w12.STAMP | AIR |
| TELEGRAMAWAN | 2 | tenang_w10.TELEGRAM | AWAN |
| KAMUSBENING | 2 | tenang_w7.KAMUS | BENING |
| ALKITABBENING | 2 | tenang_w10.ALKITAB | BENING |
| PHOTOBOOTHAWAN | 1 | tenang_w11.PHOTOBOOTH | AWAN |
| MAJALAHAIR | 1 | tenang_w10.MAJALAH | AIR |
| KETIKBENING | 1 | tenang_w7.KETIK | BENING |
| CATATANBENING | 1 | tenang_w7.CATATAN | BENING |
| EMAILBENING | 1 | tenang_w12.EMAIL | BENING |

Catatan isi campuran:
- **BALON/FLIPCLOCK:** wajib punya `label` dan `sublabel` yang cocok (bukan "menuju Natal").
- **foto/lukisan:** hanya fajar/laut/kabut/bintang.

### KOMIK

| Format | Jumlah | Skema dari |
|---|---|---|
| KOMIK | 3 | tenang_w13.KOMIK (Eli bersama Yesus) |

## JADWAL (salin persis ke konten/tenang_w16.py)

```python
JADWAL = {
    1: {"pagi": ("RESEP", 0), "pagi3": ("UKUR", 0), "pagi2": ("MAJALAHAIR", 0), "siang0": ("TANGRAM", 0), "siang": ("FILM", 0), "siang2": ("FLIP", 0), "sore": ("JAM", 0), "sore2": ("JAHIT", 0), "petang": ("ALKITABBENING", 0), "malam0": ("VINYL", 0), "malam": ("HURUF", 0), "larut": ("PIKTO", 0)},
    2: {"pagi": ("BATIK", 0), "pagi3": ("PETA", 0), "pagi2": ("SILSILAH", 0), "siang0": ("TIKETAWAN", 0), "siang": ("HURUF", 1), "siang2": ("FLIP", 1), "sore": ("SERTIFIKAT", 0), "sore2": ("GARIS", 0), "petang": ("TANGRAM", 1), "malam0": ("VINYL", 1), "malam": ("SIDIK", 0), "larut": ("KOMIK", 0)},
    3: {"pagi": ("SIDIK", 1), "pagi3": ("KAMUSBENING", 0), "pagi2": ("PIKTO", 1), "siang0": ("UKUR", 1), "siang": ("UNDANGAN", 0), "siang2": ("RIAK", 0), "sore": ("ABJAD", 0), "sore2": ("TIKETAWAN", 1), "petang": ("KARTUPOS", 0), "malam0": ("WARNAI", 0), "malam": ("EMAILBENING", 0), "larut": ("JENDELA", 0)},
    4: {"pagi": ("KAMUSBENING", 1), "pagi3": ("POLAROIDAIR", 0), "pagi2": ("PHOTOBOOTHAWAN", 0), "siang0": ("FILM", 1), "siang": ("MARMER", 0), "siang2": ("PROGRESS", 0), "sore": ("JAHIT", 1), "sore2": ("SIDIK", 2), "petang": ("JAM", 1), "malam0": ("RIAK", 1), "malam": ("SILSILAH", 1), "larut": ("KOMIK", 1)},
    5: {"pagi": ("STICKYAIR", 0), "pagi3": ("PIKTO", 2), "pagi2": ("TELEGRAMAWAN", 0), "siang0": ("UNDANGAN", 1), "siang": ("POLAROIDAIR", 1), "siang2": ("WARNAI", 1), "sore": ("BATIK", 1), "sore2": ("STAMPAIR", 0), "petang": ("TANGRAM", 2), "malam0": ("RIAK", 2), "malam": ("KARTUPOS", 1), "larut": ("JENDELA", 1)},
    6: {"pagi": ("SILSILAH", 2), "pagi3": ("MARMER", 1), "pagi2": ("ALKITABBENING", 1), "siang0": ("CATATANBENING", 0), "siang": ("STAMPAIR", 1), "siang2": ("PROGRESS", 1), "sore": ("BATIK", 2), "sore2": ("UKUR", 2), "petang": ("RESEP", 1), "malam0": ("FLIP", 2), "malam": ("ABJAD", 1), "larut": ("KOMIK", 2)},
    7: {"pagi": ("GARIS", 1), "pagi3": ("HURUF", 2), "pagi2": ("PETA", 1), "siang0": ("ABJAD", 2), "siang": ("SERTIFIKAT", 1), "siang2": ("WARNAI", 2), "sore": ("JAHIT", 2), "sore2": ("STICKYAIR", 1), "petang": ("TELEGRAMAWAN", 1), "malam0": ("VINYL", 2), "malam": ("MARMER", 2), "larut": ("KETIKBENING", 0)},
}
```

## Aturan isi

- **Sebutan Tuhan selalu huruf besar:** Tuhan, TUHAN (sesuai TB), Allah, Yesus, Kristus, Bapa, Roh Kudus, Kerajaan (Allah), Aku/-Ku, Engkau/Kau/-Mu, Dia/Ia/-Nya. Ini berlaku juga di kueri SEARCH, judul, label, dan teks gaya apa pun. Huruf kecil hanya di tempat yang memang begitu di TB, atau untuk "aku" manusia (doa kita).
- **Ayat:**
  - Kutipan ayat TB kata per kata. Periksa dengan `python3 cek_modul.py tenang_w16`: semua harus lolos (kemiripan ≥ 0,97, huruf besar benar).
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
