# Agen cloud mingguan — @diam.dan.percaya (Tenang)

Dokumen ini dibaca oleh agen Claude terjadwal (routine) yang berjalan di cloud tiap minggu.
Tujuannya: jadwal @diam.dan.percaya selalu terisi **minimal 14 hari ke depan** tanpa Mac Felix menyala.
Posting tetap dilakukan GitHub Actions (`.github/workflows/post.yml`), bukan oleh agen.

## Langkah tiap kali jalan

0. **Siapkan mesin**
   - `git pull --rebase`.
   - `bash cloud/setup.sh` memasang ffmpeg/ffprobe, cairo, Pillow, numpy dan cairosvg.
   - Font macOS tidak ada di cloud; `fonta.py` otomatis memakai font pengganti di `fonts/`.
   - Kalau setup gagal, perbaiki skripnya, lalu commit perbaikannya juga.

1. **Cek perlu minggu baru atau tidak**
   - Baris terakhir `config.MINGGU_TENANG` adalah minggu terakhir yang sudah ada, misalnya `("tenang_w14", "gaya_w14", 91)`.
   - Hari 0 = `config.START_DATE` (27 Sep 2026). Minggu baru mulai di hari `mulai + 7`, selalu hari Minggu.
   - `python3 minggu.py tenang_wN --cek` menampilkan tanggal minggu terakhir.
   - Kalau minggu terakhir **berakhir lebih dari 14 hari dari hari ini**, berhenti dan laporkan "jadwal masih cukup".
   - Kalau tidak, buat 1 minggu baru. Kalau jadwal sudah kurang dari 7 hari, buat 2 minggu.

2. **Pelajari minggu terakhir**
   - Baca docstring dan isi `konten/tenang_wN.py` serta `gaya_wN.py`. Formatnya:
     - 12 post per hari (slot di `config.AKUN["tenang"]["jam"]`).
     - `JADWAL` = {hari: {slot: (FORMAT, index)}}.
     - Sekitar 36 gaya per minggu: kira-kira 12 baru, 12 lama, 12 campuran.
     - Reels dirender lewat `render_reels`.
   - Kumpulkan semua referensi ayat dari 8 minggu terakhir (`konten/tenang_w*.py`). Minggu baru **tidak boleh mengulang** referensi itu.

3. **Tulis `konten/tenang_w{N+1}.py`**
   - **Tema:** sesuaikan dengan kalender gereja dan Indonesia, misalnya:
     - Awal Tahun, Rabu Abu, Prapaskah, Jumat Agung, Paskah, Kenaikan, Pentakosta
     - 17 Agustus, Hari Ibu (22 Des), Adven, Natal
     - di luar itu tema umum: iman, damai, kuatir, pengampunan, keluarga, pekerjaan, dan seterusnya
   - **Ayat:** semua kutipan dari **Alkitab TB (LAI)**, kata per kata. Nomor Mazmur ikut penomoran TB, yang sering 1 lebih besar dari Alkitab Inggris.
   - **Bahasa dan sebutan:**
     - Bahasa Indonesia sehari-hari yang hangat, tidak menggurui.
     - "Malam Minggu" = Sabtu malam. Untuk Minggu malam tulis "Minggu malam".
     - Ketulusan, bukan clickbait.
   - **Caption** tanpa hashtag; hashtag ditambahkan otomatis dari `konten/tenang.py` (TAGS).

4. **Tulis `gaya_w{N+1}.py`**
   - **Dasar:** salin modul gaya terakhir, ubah `MOD` dan `MULAI = dt.date(...)`. Pertahankan `SIMPLE`/`MULTI`/`REELS`, `render_week` dan `render_reels`.
   - **Isi gaya:**
     - Buang gaya yang terikat musim lalu, seperti hitung mundur Natal/Tahun Baru dan kembang api Tahun Baru, kecuali musimnya cocok.
     - Tambahkan beberapa gaya baru yang terinspirasi akun kreatif populer. Ambil **gayanya saja**; jangan menyalin isi, logo atau karakter orang lain.
     - Gaya lama boleh dipakai ulang dan dicampur.
   - **Pelajaran dari minggu-minggu lalu:**
     - Teks besar tidak boleh terpotong di tepi; kecilkan atau pecah baris supaya selalu di dalam margin aman.
     - Post 4:5 (1080×1350), tapi grid profil memotong ke 3:4. Taruh teks penting di tengah.
     - Reels 1080×1920: teks penting di y 384–1536, di atas UI Instagram di bawah.
     - Setiap file **di bawah 20 MB**; jsDelivr menolak file lebih besar. Encode Reels sekitar 4 Mbps (CRF 23, maxrate 4M).

5. **Cek ayat**
   - Tambahkan `"tenang_w{N+1}"` ke `cek_ayat.MODULES`, lalu jalankan `python3 cek_ayat.py`.
   - Buka `output/cek_ayat.md`. Semua ayat minggu baru harus ✅ (kemiripan ≥ 0,97). Perbaiki semua ❌/⚠️.

6. **Daftarkan dan render**
   - Tambahkan `("tenang_w{N+1}", "gaya_w{N+1}", mulai)` ke `config.MINGGU_TENANG`.
   - `python3 minggu.py tenang_w{N+1}` merender minggu itu saja dan menggabungkannya ke `output/schedule.json`.
   - **Jangan** jalankan `render.py` penuh: itu merender ulang semua minggu dan mengubah ratusan file.

7. **Periksa hasil sendiri**
   - Buka `output/preview_tenang_w{N+1}.jpg`, lalu buka minimal 15 gambar ukuran penuh dari berbagai gaya, plus 1 frame tiap Reels.
   - Cari:
     - teks terpotong atau keluar margin
     - teks bertumpuk
     - huruf tidak terbaca
     - salah ketik
     - kotak kosong atau gambar hitam
   - Perbaiki, lalu render ulang.

8. **Commit dan push**
   - Hanya file minggu baru:
     - `konten/tenang_w{N+1}.py`, `gaya_w{N+1}.py`, `config.py`, `cek_ayat.py`
     - `output/tenang_w{N+1}/`, `output/reels/tenang_w{N+1}/`, `output/stories/tenang_w{N+1}-*`
     - `output/schedule.json`, `output/preview_tenang_w{N+1}.jpg`
     - plus perbaikan skrip bila ada
   - Pesan commit: `Tenang minggu {N+1} (tgl-tgl): tema singkat`.
   - `git pull --rebase` lalu `git push` ke `main`. GitHub Actions sering meng-commit `state/posted.json`, jadi rebase dulu. Jangan pernah force-push.

9. **Laporan akhir** (pesan terakhir routine):
   - tanggal minggu dan tema
   - jumlah post dan Reels
   - hasil cek ayat
   - gaya baru yang dipakai
   - masalah yang perlu dilihat Felix

## Aturan tetap

- Jangan memposting apa pun sendiri, jangan menyentuh secrets/token, `publish.py` atau workflow.
- Repo harus tetap **publik**: Instagram mengambil gambar lewat jsDelivr, yang hanya melayani repo publik.
- Jangan menjadwalkan minggu "Bukan milikku" (`TENANG_MINGGU2_AKTIF` tetap `False`) dan jangan meng-commit `khotbah/`.
- Jangan merender ulang minggu yang sudah ada.
- Hanya akun Tenang. Akun lain (Eli & Ruthie, Ayat Tersembunyi, Kapi) di luar tugas ini.
- Tidak ada otomasi follow/unfollow, tidak ada menghapus post.
- Kalau ragu soal isi teologis atau ada hal sensitif, tulis di laporan akhir. Jangan menebak.
