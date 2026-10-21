# Konten Rohani Instagram — 3 akun

| Akun | Gaya | Frekuensi | Jam (WIB) |
|---|---|---|---|
| `@sahabat.eli` | Karakter Eli, ilustrasi garis biru (child.ink) | 3x sehari | 06:00 · 12:00 · 21:00 |
| `@diam.dan.percaya` | 3 format bergantian (betteryouliving): A carousel quote serif, B notifikasi "Tuhan" di pemandangan, C teks pendek di warna tegas | 1x sehari | 07:00 |
| `@ayat.tersembunyi` | Ayat yang jarang dibahas, carousel bergaya kertas kuno (`akun_baru.py`). Dulu akun Kapi: aset Kapi tetap disimpan tapi tidak dijadwalkan | 1x sehari | 19:00 |

Username masih usulan — ganti di `config.py` setelah dicek tersedia, lalu jalankan ulang `render.py`.

## Isi folder

```
config.py              handle, tanggal mulai, jam posting, font
konten/eli.py          teks balon + ayat untuk 21 gambar Eli
konten/eli-caption-minggu1.md   caption Eli (dari file 7 hari pertama, sudah dikoreksi)
konten/tenang.py       format A (POSTS), B (NOTIF), C (WARNA) + ROTASI Senin-Minggu
konten/kapi.py         7 post Kapi (kalimat, ekspresi, properti, caption)
render.py              bikin semua gambar + output/schedule.json
reels.py               Reels 9 detik dari post Eli (python3 reels.py 1 2 3), musik ditambah di Instagram
cerita.py              konten cerita ala child.ink (carousel dialog + Reels animasi), hasil di output/contoh/
publish.py             posting otomatis lewat Instagram API
.github/workflows/post.yml   menjalankan publish.py tiap 15 menit di GitHub
output/                hasil gambar (JPEG 1080x1350) + preview_*.jpg
```

## Bikin gambar

```bash
pip3 install pillow cairosvg
python3 render.py
```

Lihat `output/preview_eli.jpg`, `preview_tenang.jpg`, `preview_kapi.jpg` untuk cek semuanya sekaligus.
Rendering dilakukan di Mac (butuh font bawaan macOS), GitHub hanya memposting gambar yang sudah jadi.

## Minggu berikutnya

1. Tulis konten baru di `konten/*.py` (bisa minta Claude buatkan dengan format yang sama).
2. Ubah `START_DATE` di `config.py` ke Senin berikutnya.
3. `python3 render.py`, cek preview, commit & push.

## Cara posting

### Opsi A — tanpa coding (gratis): Meta Business Suite
Upload gambar dari `output/` dan salin caption dari `output/schedule.json`, lalu jadwalkan
seminggu sekaligus. Business Suite bisa menjadwalkan post foto dan carousel Instagram. ±30–45 menit per minggu untuk 3 akun.

### Opsi B — otomatis penuh: GitHub Actions + Instagram API
Sekali setup (±1–2 jam), setelah itu cukup push konten tiap minggu.

1. Ubah ketiga akun Instagram jadi **akun Profesional** (Creator atau Bisnis) di pengaturan Instagram.
2. Di [developers.facebook.com](https://developers.facebook.com) buat app, tambahkan produk
   **Instagram → API setup with Instagram login**, lalu hubungkan ketiga akun dan buat access token
   untuk masing-masing (izin `instagram_business_basic` + `instagram_business_content_publish`).
   Catat juga Instagram user ID tiap akun.
3. Buat repo GitHub (harus **publik**, karena Instagram mengambil gambar dari URL publik), push folder ini.
4. Di repo: Settings → Secrets and variables → Actions, tambahkan:
   `IG_TOKEN_ELI`, `IG_USER_ID_ELI`, `IG_TOKEN_TENANG`, `IG_USER_ID_TENANG`, `IG_TOKEN_AYAT`, `IG_USER_ID_AYAT`.
5. Tab Actions → "Auto-post Instagram" → **Run workflow** untuk tes. Lihat log-nya.

Catatan penting:
- Token long-lived berlaku **60 hari**. Perpanjang sebelum habis:
  `https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=TOKEN`
  lalu ganti nilai secret-nya.
- Post yang terlambat lebih dari 6 jam dilewati (supaya tidak posting borongan kalau workflow mati).
- `state/posted.json` mencatat yang sudah terkirim, jadi tidak ada post dobel.
- Repo publik berarti konten minggu depan bisa dilihat orang yang tahu repo-nya.
- Tes dulu: `python3 publish.py --dry-run` menampilkan apa yang akan diposting tanpa mengirim apa pun.

## Koreksi dari file 7 hari pertama
- Nomor ayat Mazmur disesuaikan ke Alkitab TB: 62:5→62:6, 46:1→46:2, 4:8→4:9.
- "Malam Jumat" (= Kamis malam) → "Jumat malam"; "Malam Minggu" (= Sabtu malam) → "Minggu malam".
- Placeholder `[nama mereka]` di doa hari 6 diganti kalimat lengkap.
