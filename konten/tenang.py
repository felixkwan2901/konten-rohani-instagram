"""Akun quote carousel - minggu 1 (tema Tenang & Percaya). 5 slide per post:
1 hook diulang 4x, 2 masalah pembaca, 3 ayat, 4 refleksi, 5 ajakan.
Baris kosong ("") = jeda. {handle} diganti otomatis."""

TAGS = "#renunganharian #ayatalkitab #firmanTuhan #kristen #quoteskristen #tenangdalamTuhan #doa"

POSTS = [
    {
        "warna": "coklat",
        "hook": "Waktu Tuhan selalu tepat.",
        "masalah": ["Merasa tertinggal?", "Doamu belum dijawab?", "Rencanamu belum jalan?", "", "Tuhan tidak lupa."],
        "ayat": "“Apabila berlambat-lambat, nantikanlah itu, sebab itu sungguh-sungguh akan datang dan tidak akan bertangguh.”",
        "ref": "Habakuk 2:3",
        "refleksi": ["Yang terasa terlambat bagimu,", "tepat waktu bagi-Nya.", "", "Tunggulah dengan percaya."],
        "cta": ["Kirim ini ke seseorang", "yang sedang menunggu."],
        "caption": "Waktu Tuhan selalu tepat. 🤍\n\nMungkin kamu sedang menunggu sesuatu yang rasanya tidak kunjung datang. Tapi Tuhan tidak pernah terlambat, dan Dia tidak pernah lupa.\n\n📖 Habakuk 2:3\n\nKetik “Amin” kalau kamu sedang menunggu juga.",
    },
    {
        "warna": "krem",
        "hook": "Kamu tidak harus kuat hari ini.",
        "masalah": ["Capek pura-pura baik-baik saja?", "", "Tuhan tidak memintamu", "terlihat kuat.", "Dia memintamu datang."],
        "ayat": "“Cukuplah kasih karunia-Ku bagimu, sebab justru dalam kelemahanlah kuasa-Ku menjadi sempurna.”",
        "ref": "2 Korintus 12:9",
        "refleksi": ["Kelemahanmu bukan akhir cerita.", "", "Di situlah Dia mulai bekerja."],
        "cta": ["Simpan ini untuk hari", "yang terasa terlalu berat."],
        "caption": "Kamu tidak harus kuat hari ini. 🤍\n\nTidak apa-apa lelah. Tidak apa-apa jujur di hadapan Tuhan. Kasih karunia-Nya cukup, justru saat kamu merasa paling lemah.\n\n📖 2 Korintus 12:9\n\nSimpan post ini untuk hari yang berat 🔖",
    },
    {
        "warna": "hitam",
        "hook": "Jangan takut.",
        "masalah": ["Takut gagal.", "Takut sendirian.", "Takut masa depan.", "", "Semua itu Dia tahu."],
        "ayat": "“Janganlah takut, sebab Aku menyertai engkau, janganlah bimbang, sebab Aku ini Allahmu.”",
        "ref": "Yesaya 41:10",
        "refleksi": ["Ketakutanmu nyata.", "", "Tapi penyertaan-Nya", "lebih nyata lagi."],
        "cta": ["Kirim ini ke temanmu", "yang sedang takut."],
        "caption": "Jangan takut. 🤍\n\nApa pun yang kamu takutkan hari ini, kamu tidak menghadapinya sendirian. Dia menyertai kamu.\n\n📖 Yesaya 41:10\n\nTulis di komentar: apa yang paling kamu takutkan minggu ini? Kita doakan bersama.",
    },
    {
        "warna": "hijau",
        "hook": "Serahkan, lalu istirahat.",
        "masalah": ["Pikiranmu masih ramai", "jam dua pagi?", "", "Kekhawatiran itu tidak harus", "kamu pegang sendiri."],
        "ayat": "“Janganlah hendaknya kamu kuatir tentang apa pun juga, tetapi nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa dan permohonan dengan ucapan syukur.”",
        "ref": "Filipi 4:6",
        "refleksi": ["Doa bukan jalan terakhir.", "", "Doa adalah jalan pertama."],
        "cta": ["Simpan untuk malam", "saat susah tidur."],
        "caption": "Serahkan, lalu istirahat. 🤍\n\nKekhawatiranmu tidak terlalu kecil untuk dibawa dalam doa, dan tidak terlalu besar untuk Tuhan.\n\n📖 Filipi 4:6\n\nKetik “Aku serahkan” sebagai doamu hari ini.",
    },
    {
        "warna": "coklat",
        "hook": "Dia dekat.",
        "masalah": ["Patah hati minggu ini?", "", "Kecewa pada orang lain,", "atau pada dirimu sendiri?"],
        "ayat": "“TUHAN itu dekat kepada orang-orang yang patah hati, dan Ia menyelamatkan orang-orang yang remuk jiwanya.”",
        "ref": "Mazmur 34:19",
        "refleksi": ["Kamu tidak menangis sendirian.", "", "Dia lebih dekat", "dari yang kamu kira."],
        "cta": ["Kirim ini ke seseorang", "yang sedang patah hati."],
        "caption": "Dia dekat. 🤍\n\nSaat hati terasa hancur, Tuhan tidak menjauh. Justru di situ Dia paling dekat.\n\n📖 Mazmur 34:19\n\nKalau kamu sedang di masa ini, ketik 🤍 — kamu tidak sendiri.",
    },
    {
        "warna": "krem",
        "hook": "Satu hari saja.",
        "masalah": ["Hari ini belum selesai,", "tapi sudah cemas", "soal bulan depan?"],
        "ayat": "“Janganlah kamu kuatir akan hari besok, karena hari besok mempunyai kesusahannya sendiri. Kesusahan sehari cukuplah untuk sehari.”",
        "ref": "Matius 6:34",
        "refleksi": ["Hari ini cukup untuk hari ini.", "", "Besok, Dia sudah ada di sana."],
        "cta": ["Simpan ini sebagai", "pengingat akhir pekan."],
        "caption": "Satu hari saja. 🤍\n\nKamu tidak harus menyelesaikan seluruh hidupmu hari ini. Jalani hari ini bersama Tuhan, besok Dia sudah menunggu di sana.\n\n📖 Matius 6:34\n\nSelamat menikmati akhir pekan.",
    },
    {
        "warna": "hitam",
        "hook": "Diamlah.",
        "masalah": ["Minggu yang panjang.", "Kepala yang penuh.", "Hati yang lelah."],
        "ayat": "“Diamlah dan ketahuilah, bahwa Akulah Allah!”",
        "ref": "Mazmur 46:11",
        "refleksi": ["Hari ini, berhenti sebentar.", "", "Biarkan Dia yang", "memegang kendali."],
        "cta": ["Follow @{handle}", "untuk renungan setiap hari."],
        "caption": "Diamlah. 🤍\n\nDi akhir pekan ini, ambil waktu untuk berhenti. Tidak perlu memikirkan semuanya — Dia tetap Allah.\n\n📖 Mazmur 46:11\n\nSelamat berakhir pekan. Follow @{handle} untuk renungan setiap hari.",
    },
]


# ---------- format 2: notifikasi dari Tuhan di atas pemandangan (carousel 4 slide) ----------
# Slide 1-3 = satu notifikasi per slide, slide 4 = semua notifikasi + ayat dasarnya.
# Kalimat "Tuhan" adalah parafrase ayat di slide terakhir, bukan kutipan langsung.

NOTIF = [
    {
        "adegan": "fajar",
        "pesan": ["Aku lihat kamu sudah berusaha keras.", "Kamu tidak harus kuat sendirian.", "Datang saja. Aku akan memberi kelegaan."],
        "ayat": "“Marilah kepada-Ku, semua yang letih lesu dan berbeban berat, Aku akan memberi kelegaan kepadamu.”",
        "ref": "Matius 11:28",
        "caption": "Kalau hari ini Tuhan kirim pesan ke HP-mu, mungkin bunyinya begini 🤍\n\nKamu nggak harus kuat sendirian. Datang saja apa adanya.\n\n📖 Matius 11:28\n\nGeser sampai slide terakhir 👉\nKetik “Aku datang” kalau kamu butuh ini hari ini.",
    },
    {
        "adegan": "laut",
        "pesan": ["Aku belum selesai denganmu.", "Mimpi itu Aku yang taruh di hatimu.", "Tunggu waktu-Ku. Itu yang terbaik."],
        "ayat": "“Ia, yang memulai pekerjaan yang baik di antara kamu, akan meneruskannya sampai pada akhirnya pada hari Kristus Yesus.”",
        "ref": "Filipi 1:6",
        "caption": "Tuhan belum selesai denganmu 🌅\n\nApa yang Dia mulai, akan Dia selesaikan. Termasuk mimpi yang rasanya jalan di tempat.\n\n📖 Filipi 1:6\n\nKirim ini ke seseorang yang hampir menyerah sama mimpinya 💌",
    },
    {
        "adegan": "fajar",
        "pesan": ["Aku tahu pikiranmu ramai semalaman.", "Taruh semuanya di tangan-Ku.", "Aku akan menjaga hatimu tetap damai."],
        "ayat": "“Yang hatinya teguh Kaujagai dengan damai sejahtera, sebab kepada-Mulah ia percaya.”",
        "ref": "Yesaya 26:3",
        "caption": "Untuk kamu yang susah tidur karena pikiran yang ramai 🌙\n\nTaruh semuanya di tangan-Nya malam ini. Dia berjanji menjaga hatimu.\n\n📖 Yesaya 26:3\n\nSave untuk malam-malam yang berat 🔖",
    },
]


# ---------- format 3: teks pendek di warna tegas (1 gambar) ----------

WARNA = [
    {
        "bg": "#1F6B3A", "fg": "#F4F1EA",
        "teks": ["Tuhan, aku butuh Engkau.", "Aku tidak bisa melakukan ini sendiri."],
        "caption": "Doa paling jujur kadang paling pendek 🤍\n\nKetik “Amin” kalau ini doamu juga hari ini.\n\n📖 “Tanpa Aku kamu tidak dapat berbuat apa-apa.” — Yohanes 15:5",
    },
    {
        "bg": "#F07021", "fg": "#0E0E0E",
        "teks": ["Musim ini namanya:", "", "“Belajar percaya, walau belum melihat.”"],
        "caption": "Musim ini namanya: belajar percaya 🧡\n\nBelum kelihatan hasilnya? Tidak apa-apa. Iman justru bekerja di situ.\n\n📖 “Iman adalah dasar dari segala sesuatu yang kita harapkan dan bukti dari segala sesuatu yang tidak kita lihat.” — Ibrani 11:1\n\nSave buat pengingat minggu depan 🔖",
    },
    {
        "bg": "#F4F1EA", "fg": "#111111",
        "teks": ["Tuhan tidak memintamu memikirkan semuanya.", "Dia memintamu mempercayakan semuanya."],
        "caption": "Lepaskan sedikit beban di pikiranmu hari ini 🤍\n\n📖 “Percayalah kepada TUHAN dengan segenap hatimu, dan janganlah bersandar kepada pengertianmu sendiri. Akuilah Dia dalam segala lakumu, maka Ia akan meluruskan jalanmu.” — Amsal 3:5-6\n\nKirim ke temanmu yang lagi overthinking 💌",
    },
    {
        "bg": "#111111", "fg": "#F2F2F2",
        "teks": ["Tuhan, aku tidak tahu harus mulai dari mana.", "", "Tapi aku mau mulai dengan-Mu."],
        "caption": "Nggak harus tahu semua langkahnya. Cukup mulai dengan Dia 🤍\n\n📖 “Serahkanlah hidupmu kepada TUHAN dan percayalah kepada-Nya, dan Ia akan bertindak.” — Mazmur 37:5\n\nKetik “Amin” kalau ini doamu pagi ini.",
    },
    {
        "bg": "#2B3A67", "fg": "#F4F1EA",
        "teks": ["Kamu tidak terlambat.", "Kamu sedang dibentuk."],
        "caption": "Prosesnya mungkin lama, tapi Pembentuknya tidak pernah salah 🤍\n\n📖 “Kamilah tanah liat dan Engkaulah yang membentuk kami, dan kami sekalian adalah buatan tangan-Mu.” — Yesaya 64:8\n\nSave buat hari kamu merasa tertinggal 🔖",
    },
    {
        "bg": "#E9D8C4", "fg": "#2B2620",
        "teks": ["Doa hari ini:", "", "“Tuhan, tolong aku percaya,", "bahkan saat aku belum mengerti.”"],
        "caption": "Doa yang jujur tidak harus panjang 🤍\n\n📖 “Aku percaya. Tolonglah aku yang tidak percaya ini!” — Markus 9:24\n\nKetik “Tolong aku percaya” sebagai doamu hari ini.",
    },
    {
        "bg": "#8C2F39", "fg": "#F4F1EA",
        "teks": ["Yang kamu anggap akhir,", "bisa jadi awal yang Tuhan siapkan."],
        "caption": "Belum selesai. Tuhan masih bekerja 🤍\n\n📖 “Kita tahu sekarang, bahwa Allah turut bekerja dalam segala sesuatu untuk mendatangkan kebaikan bagi mereka yang mengasihi Dia.” — Roma 8:28\n\nKirim ke seseorang yang merasa ceritanya sudah tamat 💌",
    },
]



# ---------- format 4: dinding teks (1 gambar + versi Reels) ----------
# Satu kalimat diulang memenuhi layar; kata-kata "sorot" menyala putih berurutan membentuk pesan tersembunyi.

DINDING = [
    {
        "bg": "#C62F2F", "teks": "#7E1414",
        "kalimat": "SERAHKAN PADA TUHAN DAN BERISTIRAHATLAH",
        "sorot": ["SERAHKAN", "PADA", "TUHAN", "DAN", "BERISTIRAHATLAH"],
        "caption": "Coba cari kata yang menyala 👀\n\nSerahkan pada Tuhan, dan beristirahatlah. Kamu tidak harus memikul semuanya malam ini.\n\n📖 “Serahkanlah segala kekuatiranmu kepada-Nya, sebab Ia yang memelihara kamu.” — 1 Petrus 5:7\n\nKetik “SERAHKAN” kalau kamu butuh diingatkan ini 🤍",
    },
    {
        "bg": "#1F3A5F", "teks": "#34578A",
        "kalimat": "TETAP PERCAYA WAKTU TUHAN PASTI TEPAT",
        "sorot": ["TETAP", "PERCAYA", "WAKTU", "TUHAN", "TEPAT"],
        "caption": "Coba temukan pesannya 👀\n\nTetap percaya. Waktu Tuhan tepat.\n\n📖 “Janganlah kita jemu-jemu berbuat baik, karena apabila sudah datang waktunya, kita akan menuai, jika kita tidak menjadi lemah.” — Galatia 6:9\n\nKetik “TEPAT” kalau kamu masih menunggu 🤍",
    },
]


# ---------- format 5: Reels suasana (kabut / langit bintang + paragraf) ----------

SUASANA = [
    {
        "adegan": "kabut",
        "teks": ["Tuhan dengar doamu.", "Dia lihat air mata yang tak dilihat orang.",
                 "Dia tahu kamu lelah, takut, dan bertanya-tanya kapan musim ini selesai.", "",
                 "Hari ini, biarkan Dia memegang semuanya.", "Kamu tidak berjalan sendirian di kabut ini.", "",
                 "Istirahatlah di dalam Dia."],
        "caption": "Untuk kamu yang sedang berjalan di tengah kabut 🌫️\n\nKamu mungkin belum bisa melihat jalan di depan. Tapi Dia bisa, dan Dia berjalan bersamamu.\n\n📖 “Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.” — Mazmur 119:105\n\nSave untuk hari yang terasa berkabut 🔖",
    },
    {
        "adegan": "bintang",
        "teks": ["Bintang tidak takut pada gelap.", "Justru di situ mereka terlihat.", "",
                 "Mungkin musim gelapmu sekarang bukan akhir cerita,", "tapi tempat Tuhan menunjukkan terang-Nya lewat kamu.", "",
                 "“Bangkitlah, menjadi teranglah, sebab terangmu datang.”", "Yesaya 60:1"],
        "caption": "Gelapnya bukan akhir ceritamu ✨\n\n📖 “Bangkitlah, menjadi teranglah, sebab terangmu datang, dan kemuliaan TUHAN terbit atasmu.” — Yesaya 60:1\n\nKirim ke temanmu yang lagi di musim gelap 💌",
    },
]

# Jadwal 3 post per hari (Senin..Minggu):
#   pagi  = C warna tegas (1 gambar, cepat dibaca)
#   siang = A carousel quote
#   malam = Reels: B notifikasi, R suasana, atau D dinding teks
JADWAL = [
    [("pagi", "C", 0), ("siang", "A", 0), ("malam", "B", 0)],
    [("pagi", "C", 1), ("siang", "A", 1), ("malam", "R", 0)],
    [("pagi", "C", 2), ("siang", "A", 2), ("malam", "D", 0)],
    [("pagi", "C", 3), ("siang", "A", 3), ("malam", "B", 1)],
    [("pagi", "C", 4), ("siang", "A", 4), ("malam", "R", 1)],
    [("pagi", "C", 5), ("siang", "A", 5), ("malam", "D", 1)],
    [("pagi", "C", 6), ("siang", "A", 6), ("malam", "B", 2)],
]
