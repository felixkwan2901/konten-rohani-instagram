# Spesifikasi minggu 15 Tenang (@diam.dan.percaya): Minggu 3 – Sabtu 9 Januari 2027

- Modul gaya: `gaya_w15.py`, dengan `MOD = "tenang_w15"` dan `MULAI = dt.date(2027, 1, 3)`.
- Modul konten: `konten/tenang_w15.py`.
- Hari 1 = Minggu 3 Jan … hari 7 = Sabtu 9 Jan.
- 12 slot per hari: `pagi 06:00, pagi3 07:30, pagi2 09:00, siang0 10:30, siang 12:00, siang2 13:30 (Reels), sore 15:00, sore2 16:30, petang 18:00, malam0 19:30 (Reels), malam 21:00, larut 22:30` (WIB).

## Tema harian

| Hari | Tanggal | Tema |
|---|---|---|
| 1 | Minggu 3 Jan | Minggu pertama 2027: memulai tahun bersama Tuhan, mencari dahulu Kerajaan-Nya |
| 2 | Senin 4 Jan | Kembali bekerja/sekolah: kerjakan dengan segenap hati, Tuhan menyertai hari Senin |
| 3 | Selasa 5 Jan | Rencana kita & rancangan Tuhan (berserah, bukan kuatir soal masa depan) |
| 4 | Rabu 6 Jan | EPIFANIA: orang Majus, bintang, Terang bagi bangsa-bangsa, mencari dan menyembah Yesus |
| 5 | Kamis 7 Jan | Setia dalam hal kecil: kebiasaan rohani harian (doa, Firman, syukur) |
| 6 | Jumat 8 Jan | Saat semangat awal tahun mulai turun: kekuatan baru, jangan jemu |
| 7 | Sabtu 9 Jan | Istirahat dan bersiap untuk hari Tuhan. Sabtu malam = "malam Minggu" |

## Format (37 + KOMIK) dan jumlah item

### BARU: ditulis di gaya_w15.py

Skema dalam ≤ = batas karakter. Semua item juga punya `ayat` (TB, kata per kata, dalam “…”, boleh dipotong dengan …), `ref`, `caption`.

| Format | Jumlah | Gaya | Skema |
|---|---|---|---|
| JURNAL | 3 | bullet journal di kertas titik-titik, selotip washi, judul tulisan tangan, habit tracker 3 kebiasaan × 7 hari (terisi sampai hari post), catatan kecil | `judul ≤28`, `kebiasaan[3] ≤22`, `catatan ≤90` |
| LABEL | 3 | pita label timbul ala Dymo (hitam/merah/biru/hijau, huruf putih timbul) di papan kraft, ayat di kartu kertas | `label[3-4] ≤18` (ditampilkan kapital) |
| CETAKBIRU | 3 | cetak biru arsitek: latar biru, grid, denah rumah garis putih + garis ukur, ruangan berlabel, kotak judul (PROYEK / PERANCANG: TUHAN / TANGGAL) | `proyek ≤30`, `ruang[4] = [nama ≤14, catatan ≤22]`, `catatan ≤60` |
| PERPUS | 3 | kartu pinjam perpustakaan di kantong kertas manila, cap tanggal ungu miring, cap besar | `buku ≤24`, `pengarang ≤24`, `pinjam[4] = [tanggal ≤12, catatan ≤20]`, `cap ≤26` |
| CENTANG | 3 | aplikasi to-do bersih: tanggal, judul, centang bulat, cincin progres | `judul ≤20`, `tugas[4-5] = [teks ≤34, selesai true/false]` |
| SWISS | 3 | poster gaya Swiss: grid ketat, Helvetica tebal, angka besar, lingkaran/batang merah, garis tipis hitam | `angka ≤3`, `judul ≤22`, `baris[2] ≤30` |
| LAPIS | 3 | pemandangan kertas berlapis (5–6 bukit dengan bayangan, matahari), judul di langit | `judul ≤36` |
| SULAM | 3 | sulaman kristik di ram kayu, huruf jahitan X 1–2 baris + motif kecil, ayat di bawah ram | `teks`: 1–2 baris dipisah `\n`, tiap baris ≤10 huruf A–Z/spasi, kapital |
| APOTEK | 3 | resep dokter / label obat: "R/", APOTEK KASIH KARUNIA, Untuk: pasien, daftar "obat" = bacaan + aturan pakai, "Tabib yang Agung" | `pasien ≤18`, `obat[3] = [nama ≤22, aturan ≤28]`, `catatan ≤50` |
| GIZI | 3 | label "Informasi Nilai Gizi" hitam-putih tegas | `nama ≤24`, `porsi ≤20`, `baris[5] = [nama ≤20, nilai ≤8]`, `catatan ≤60` |
| KERETA (Reels) | 3 | peta jalur kereta: garis tebal berwarna, 5 stasiun, kereta berjalan, label muncul, lalu ayat | `jalur ≤20`, `stasiun[5] ≤16`; `ayat ≤160` |
| TULIS (Reels) | 3 | tangan/pena menulis ayat di kertas krem huruf demi huruf, lalu referensi muncul | `ayat ≤150` (ayat itulah yang ditulis) |

### LAMA: skema sama dengan modul aslinya

Lihat contoh di modul konten yang disebut.

| Format | Jumlah | Skema dari | Catatan |
|---|---|---|---|
| CUACA | 2 | tenang_w7.CUACA | `hari` tulis "Minggu, 3 Januari" dsb. |
| STRUK | 2 | tenang_w7.STRUK | |
| KORAN | 2 | tenang_w8.KORAN | |
| MENU | 2 | tenang_w8.MENU | |
| NAMA | 2 | tenang_w9.NAMA | |
| MUSEUM | 2 | tenang_w9.MUSEUM | `lukisan`: fajar/laut/kabut/bintang |
| KASET | 2 | tenang_w9.KASET | |
| RASI | 2 | tenang_w10.RASI | |
| LETTER | 2 | tenang_w8.LETTER | `teks` kapital, ≤5 baris, ≤14 huruf per baris |
| CHAT (Reels) | 3 | tenang_w7.CHAT | |
| SEARCH (Reels) | 3 | tenang_w8.SEARCH | **kueri harus menulis Tuhan/Allah/Yesus dengan huruf besar** |
| GOSOK (Reels) | 2 | tenang_w9.GOSOK | |

### CAMPUR: gaya lama di latar/efek baru; skema = gaya lama

| Format | Jumlah | Skema dari | Latar/efek |
|---|---|---|---|
| STICKYJURNAL | 2 | tenang_w8.STICKY | kertas jurnal |
| PHOTOBOOTHJURNAL | 1 | tenang_w11.PHOTOBOOTH | kertas jurnal; `foto`: fajar/laut/kabut/bintang |
| POLAROIDPAGI | 2 | tenang_w7.POLAROID | langit pagi |
| TIKETPAGI | 2 | tenang_w7.TIKET | langit pagi |
| BALONPAGI | 2 | tenang_w12.BALON | langit pagi; **wajib** `label` & `sublabel` (bukan "menuju Natal"), mis. angka 3 / "HARI PERTAMA" / "di tahun 2027" |
| FLIPPAGI | 1 | tenang_w11.FLIPCLOCK | langit pagi; wajib `label` & `sublabel` |
| ALKITABSINAR | 2 | tenang_w10.ALKITAB | cahaya pagi hangat |
| KETIKSINAR | 1 | tenang_w7.KETIK | cahaya pagi hangat |
| CATATANSINAR | 1 | tenang_w7.CATATAN | cahaya pagi hangat |
| KAMUSBIRU | 2 | tenang_w7.KAMUS | duotone biru cetak biru + grid |
| TELEGRAMBIRU | 2 | tenang_w10.TELEGRAM | duotone biru |
| MAJALAHBIRU | 1 | tenang_w10.MAJALAH | duotone biru; `foto`: fajar/laut/kabut/bintang |

### KOMIK

| Format | Jumlah | Skema dari |
|---|---|---|
| KOMIK | 3 | tenang_w13.KOMIK (Eli bersama Yesus) |

## JADWAL (salin persis ke konten/tenang_w15.py)

```python
JADWAL = {
    1: {"pagi": ("CENTANG", 0), "pagi3": ("MUSEUM", 0), "pagi2": ("APOTEK", 0), "siang0": ("TIKETPAGI", 0), "siang": ("GIZI", 0), "siang2": ("TULIS", 0), "sore": ("LETTER", 0), "sore2": ("ALKITABSINAR", 0), "petang": ("SULAM", 0), "malam0": ("KERETA", 0), "malam": ("RASI", 0), "larut": ("POLAROIDPAGI", 0)},
    2: {"pagi": ("KORAN", 0), "pagi3": ("KAMUSBIRU", 0), "pagi2": ("PHOTOBOOTHJURNAL", 0), "siang0": ("GIZI", 1), "siang": ("MENU", 0), "siang2": ("GOSOK", 0), "sore": ("BALONPAGI", 0), "sore2": ("LAPIS", 0), "petang": ("SULAM", 1), "malam0": ("KERETA", 1), "malam": ("RASI", 1), "larut": ("KOMIK", 0)},
    3: {"pagi": ("CENTANG", 1), "pagi3": ("TELEGRAMBIRU", 0), "pagi2": ("APOTEK", 1), "siang0": ("KORAN", 1), "siang": ("MENU", 1), "siang2": ("TULIS", 1), "sore": ("SWISS", 0), "sore2": ("LABEL", 0), "petang": ("CETAKBIRU", 0), "malam0": ("SEARCH", 0), "malam": ("SULAM", 2), "larut": ("PERPUS", 0)},
    4: {"pagi": ("TELEGRAMBIRU", 1), "pagi3": ("CETAKBIRU", 1), "pagi2": ("APOTEK", 2), "siang0": ("STICKYJURNAL", 0), "siang": ("STRUK", 0), "siang2": ("SEARCH", 1), "sore": ("LAPIS", 1), "sore2": ("LABEL", 1), "petang": ("MAJALAHBIRU", 0), "malam0": ("CHAT", 0), "malam": ("PERPUS", 1), "larut": ("KOMIK", 1)},
    5: {"pagi": ("CENTANG", 2), "pagi3": ("CETAKBIRU", 2), "pagi2": ("NAMA", 0), "siang0": ("GIZI", 2), "siang": ("STRUK", 1), "siang2": ("CHAT", 1), "sore": ("PERPUS", 2), "sore2": ("CATATANSINAR", 0), "petang": ("KASET", 0), "malam0": ("SEARCH", 2), "malam": ("JURNAL", 0), "larut": ("POLAROIDPAGI", 1)},
    6: {"pagi": ("FLIPPAGI", 0), "pagi3": ("CUACA", 0), "pagi2": ("KAMUSBIRU", 1), "siang0": ("STICKYJURNAL", 1), "siang": ("LETTER", 1), "siang2": ("GOSOK", 1), "sore": ("LAPIS", 2), "sore2": ("SWISS", 1), "petang": ("ALKITABSINAR", 1), "malam0": ("CHAT", 2), "malam": ("JURNAL", 1), "larut": ("KOMIK", 2)},
    7: {"pagi": ("CUACA", 1), "pagi3": ("NAMA", 1), "pagi2": ("MUSEUM", 1), "siang0": ("SWISS", 2), "siang": ("LABEL", 2), "siang2": ("TULIS", 2), "sore": ("BALONPAGI", 1), "sore2": ("TIKETPAGI", 1), "petang": ("KASET", 1), "malam0": ("KERETA", 2), "malam": ("JURNAL", 2), "larut": ("KETIKSINAR", 0)},
}
```

## Aturan isi

- **Sebutan Tuhan selalu huruf besar:** Tuhan, TUHAN (sesuai TB), Allah, Yesus, Kristus, Bapa, Roh Kudus, Kerajaan (Allah), Aku/-Ku, Engkau/Kau/-Mu, Dia/Ia/-Nya. Ini berlaku juga di kueri SEARCH, judul, label, dan teks gaya apa pun. Huruf kecil hanya di tempat yang memang begitu di TB, atau untuk "aku" manusia (doa kita).
- **Ayat:**
  - Kutipan ayat TB kata per kata. Periksa dengan `python3 cek_modul.py tenang_w15`: semua harus lolos (kemiripan ≥ 0,97, huruf besar benar).
  - Satu referensi hanya dipakai sekali dalam minggu ini.
  - Jangan memakai referensi yang sudah muncul di `konten/tenang_w7.py` … `tenang_w14.py`.
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
