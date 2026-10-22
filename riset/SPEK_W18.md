# Spesifikasi minggu 18 Tenang (@diam.dan.percaya): Minggu 24 Jan – Sabtu 30 Jan 2027

- Modul gaya: `gaya_w18.py`, dengan `MOD = "tenang_w18"` dan `MULAI = dt.date(2027, 1, 24)`.
- Modul konten: `konten/tenang_w18.py`.
- Hari 1 = Minggu 24 Jan … hari 7 = Sabtu 30 Jan.
- Slot sama dengan minggu 15 (lihat `riset/SPEK_W15.md`): 12 per hari, Reels di `siang2` dan `malam0`.

Gaya BARU diambil dari `riset/RISET_GAYA_JAN2027.md`. Baca bagian konsepnya (tampilan, palet, font, field, catatan Pillow). Sampel ayat di riset hanya contoh: penulis konten boleh memakai ayat lain, asal tidak berulang.

## Tema harian

| Hari | Tanggal | Tema |
|---|---|---|
| 1 | Minggu 24 Jan | Satu tubuh, banyak anggota (Minggu penutup Pekan Doa Sedunia untuk Kesatuan Umat Kristen, 18-25 Jan) |
| 2 | Senin 25 Jan | Doa Yesus: "supaya mereka semua menjadi satu"; hari terakhir Pekan Doa |
| 3 | Selasa 26 Jan | Kasih itu sabar dan murah hati (1 Kor 13): kasih di rumah dan di kantor |
| 4 | Rabu 27 Jan | Mengampuni tujuh puluh kali tujuh; berdamai |
| 5 | Kamis 28 Jan | Bertekun ketika semangat Januari mulai pudar |
| 6 | Jumat 29 Jan | Saling menanggung beban; tali tiga lembar tidak mudah putus |
| 7 | Sabtu 30 Jan | Menutup Januari dengan syukur: kesetiaan-Nya sebulan ini; Sabtu malam = "malam Minggu" |

## Format

### BARU (3 item per format; tulis di gaya_wNN.py)

Semua item juga punya `ayat`, `ref`, `caption`. Field mengikuti riset; ≤ = batas karakter.

| Format | Riset | Field |
|---|---|---|
| KALKULATOR | §31 70 × 7 (image) | `hitung ≤10 · hasil ≤8 · tape[3] ≤26 · ayat ≤170 · ref · caption` |
| UNSUR | §32 element "Kasih" (image) | `nomor ≤3 · simbol ≤2 · nama ≤10 · kategori ≤22 · sifat[3] ≤36 · tetangga[2] = [simbol ≤2, nama ≤12] · ayat ≤150 · ref · caption` |
| PALET | §33 love's paint-chip card (image) | `nama_kartu ≤24 · chip[6] = [nama ≤22, kode ≤10] · warna_dasar RGB · ayat ≤140 · ref · caption` |
| MUARA | §34 many rivers, one estuary (image) | `sumber[6–8] ≤10 · muara ≤10 · ayat ≤160 · ref · caption` |
| TALI | §35 three-strand cord (image) | `untai[3] ≤10 · judul ≤24 · ayat ≤170 · ref · caption` |
| PERCA | §36 patchwork quilt (image) | `judul ≤22 · ayat ≤150 · ref · caption` |
| TANGGA | §37 ladders and slides (image) | `judul ≤22 · tangga[3] = [dari, ke, label ≤12] · turun[3] = [dari, ke, label ≤12] · bidak 1–100 · dadu 1–6 · ayat ≤120 · ref · caption` |
| FASE | §38 ring of moon phases (image) | `judul ≤22 · label_fase[2] ≤18 · cincin ≤40 · ayat ≤110 · ref · caption` |
| KIDUNG | §39 hymnal page in *not angka* (image) | `nomor ≤5 · judul ≤26 · nada_dasar ≤8 · birama ≤4 · suku_kata[] ≤40 · not[4][] (0–7 with octave marks) · ayat ≤150 · ref · caption` |
| STENSIL | §40 crate stencil "JANGAN GOYAH" (image) | `kata_besar[2] ≤8 · kecil[2] ≤26 · cap ≤16 · ayat ≤180 · ref · caption` |
| BENANG (Reels) | §R7 string-art heart (Reel, 13 s) | `judul ≤30 · ayat ≤140 · ref` |
| SPIRO (Reels) | §R8 one more loop (Reel, 14 s) | ``judul ≤24 · label_putaran ≤12 · ayat ≤230 · ref` (long verse: use 2 lines per beat, or trim with "…")` |

### LAMA (skema sama dengan modul aslinya)

| Format | Jumlah | Skema dari |
|---|---|---|
| SCROLL | 2 | tenang_w11.SCROLL |
| PIXEL | 2 | tenang_w11.PIXEL |
| CHART | 2 | tenang_w11.CHART |
| HPJADUL | 2 | tenang_w11.HPJADUL |
| TAG | 2 | tenang_w11.TAG |
| KACAPATRI | 2 | tenang_w11.KACAPATRI |
| POSTERTEBAL | 2 | tenang_w13.POSTERTEBAL |
| BERITA | 2 | tenang_w13.BERITA |
| RAMBU | 2 | tenang_w9.RAMBU |
| PANGGUNG (Reels) | 3 | tenang_w13.PANGGUNG |
| NEON (Reels) | 3 | tenang_w7.NEON |
| KONFETI (Reels) | 2 | tenang_w12.KONFETI |

### CAMPUR (gaya lama di latar/efek baru minggu ini; skema = gaya lama)

Latar dan efek baru minggu ini (dibuat di gaya_wNN.py):

- **TENUN:** kain tenun/ikat: benang-benang berwarna yang saling menyilang (kesatuan), tekstur kain
- **SENJA:** langit senja merah muda-jingga-ungu yang lembut dengan matahari rendah
- **HANGAT:** EFEK pada gambar jadi: film hangat (sepia lembut, grain, vinyet), terasa seperti kenangan sebulan

| Format | Jumlah | Skema dari | Latar/efek |
|---|---|---|---|
| STICKYTENUN | 2 | tenang_w8.STICKY | TENUN |
| POLAROIDSENJA | 2 | tenang_w7.POLAROID | SENJA |
| TIKETSENJA | 2 | tenang_w7.TIKET | SENJA |
| STAMPTENUN | 2 | tenang_w12.STAMP | TENUN |
| BALONSENJA | 2 | tenang_w12.BALON | SENJA |
| TELEGRAMTENUN | 2 | tenang_w10.TELEGRAM | TENUN |
| KAMUSHANGAT | 2 | tenang_w7.KAMUS | HANGAT |
| PHOTOBOOTHTENUN | 1 | tenang_w11.PHOTOBOOTH | TENUN |
| RESEPSENJA | 1 | tenang_w9.RESEP | SENJA |
| MAJALAHSENJA | 1 | tenang_w10.MAJALAH | SENJA |
| KETIKHANGAT | 1 | tenang_w7.KETIK | HANGAT |
| CATATANHANGAT | 1 | tenang_w7.CATATAN | HANGAT |

Catatan isi campuran:
- **BALON/FLIPCLOCK:** wajib punya `label` dan `sublabel` yang cocok (bukan "menuju Natal").
- **foto/lukisan:** hanya fajar/laut/kabut/bintang.

### KOMIK

| Format | Jumlah | Skema dari |
|---|---|---|
| KOMIK | 3 | tenang_w13.KOMIK (Eli bersama Yesus) |

## JADWAL (salin persis ke konten/tenang_w18.py)

```python
JADWAL = {
    1: {"pagi": ("PERCA", 0), "pagi3": ("TALI", 0), "pagi2": ("BERITA", 0), "siang0": ("SCROLL", 0), "siang": ("STENSIL", 0), "siang2": ("SPIRO", 0), "sore": ("PALET", 0), "sore2": ("TIKETSENJA", 0), "petang": ("HPJADUL", 0), "malam0": ("PANGGUNG", 0), "malam": ("FASE", 0), "larut": ("TELEGRAMTENUN", 0)},
    2: {"pagi": ("KIDUNG", 0), "pagi3": ("KALKULATOR", 0), "pagi2": ("TANGGA", 0), "siang0": ("CATATANHANGAT", 0), "siang": ("MUARA", 0), "siang2": ("PANGGUNG", 1), "sore": ("TALI", 1), "sore2": ("CHART", 0), "petang": ("STENSIL", 1), "malam0": ("NEON", 0), "malam": ("PERCA", 1), "larut": ("KOMIK", 0)},
    3: {"pagi": ("KALKULATOR", 1), "pagi3": ("KIDUNG", 1), "pagi2": ("POLAROIDSENJA", 0), "siang0": ("STAMPTENUN", 0), "siang": ("STICKYTENUN", 0), "siang2": ("SPIRO", 1), "sore": ("TANGGA", 1), "sore2": ("PALET", 1), "petang": ("RAMBU", 0), "malam0": ("BENANG", 0), "malam": ("FASE", 1), "larut": ("KETIKHANGAT", 0)},
    4: {"pagi": ("STICKYTENUN", 1), "pagi3": ("TAG", 0), "pagi2": ("TANGGA", 2), "siang0": ("UNSUR", 0), "siang": ("BALONSENJA", 0), "siang2": ("KONFETI", 0), "sore": ("MUARA", 1), "sore2": ("RESEPSENJA", 0), "petang": ("PERCA", 2), "malam0": ("BENANG", 1), "malam": ("STAMPTENUN", 1), "larut": ("KOMIK", 1)},
    5: {"pagi": ("PHOTOBOOTHTENUN", 0), "pagi3": ("PALET", 2), "pagi2": ("KAMUSHANGAT", 0), "siang0": ("STENSIL", 2), "siang": ("MUARA", 2), "siang2": ("KONFETI", 1), "sore": ("KACAPATRI", 0), "sore2": ("BALONSENJA", 1), "petang": ("TIKETSENJA", 1), "malam0": ("BENANG", 2), "malam": ("CHART", 1), "larut": ("UNSUR", 1)},
    6: {"pagi": ("POLAROIDSENJA", 1), "pagi3": ("SCROLL", 1), "pagi2": ("POSTERTEBAL", 0), "siang0": ("RAMBU", 1), "siang": ("MAJALAHSENJA", 0), "siang2": ("NEON", 1), "sore": ("TELEGRAMTENUN", 1), "sore2": ("UNSUR", 2), "petang": ("PIXEL", 0), "malam0": ("SPIRO", 2), "malam": ("FASE", 2), "larut": ("KOMIK", 2)},
    7: {"pagi": ("PIXEL", 1), "pagi3": ("KAMUSHANGAT", 1), "pagi2": ("KALKULATOR", 2), "siang0": ("KIDUNG", 2), "siang": ("KACAPATRI", 1), "siang2": ("PANGGUNG", 2), "sore": ("POSTERTEBAL", 1), "sore2": ("TAG", 1), "petang": ("HPJADUL", 1), "malam0": ("NEON", 2), "malam": ("BERITA", 1), "larut": ("TALI", 2)},
}
```

## Aturan isi

- **Sebutan Tuhan selalu huruf besar:** Tuhan, TUHAN (sesuai TB), Allah, Yesus, Kristus, Bapa, Roh Kudus, Kerajaan (Allah), Aku/-Ku, Engkau/Kau/-Mu, Dia/Ia/-Nya. Ini berlaku juga di kueri SEARCH, judul, label, dan teks gaya apa pun. Huruf kecil hanya di tempat yang memang begitu di TB, atau untuk "aku" manusia (doa kita).
- **Ayat:**
  - Kutipan ayat TB kata per kata. Periksa dengan `python3 cek_modul.py tenang_w18`: semua harus lolos (kemiripan ≥ 0,97, huruf besar benar).
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
