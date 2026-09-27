"""Akun Tenang - format baru (4 slot tambahan per hari mulai hari 2, total 10 post/hari):
  F = carousel "photo dump" (foto hitam-putih buatan sendiri + satu kalimat pendek per slide)
  V = carousel "dulu vs sekarang" (layar dibagi dua)
  K = Reels tipografi sinematik (kata muncul satu per satu)
  J = Reels animasi karakter (sosok krem sederhana di pemandangan lukisan, teks tulisan tangan)
Foto untuk F: laut, gunung, kabut, bintang, jendela, lilin, jalan, pohon, awan."""

# ---------- F: photo dump ----------
DUMP = [
    {"slides": [("laut", "hal-hal kecil yang Tuhan ingatkan minggu ini"), ("jalan", "tidak semua jalan harus kamu mengerti hari ini"),
                ("lilin", "cahaya kecil tetap cahaya"), ("awan", "Dia masih di atas semua yang kamu takutkan"),
                ("pohon", "akar tumbuh saat tidak ada yang melihat")],
     "caption": "hal-hal kecil yang Tuhan ingatkan minggu ini 🤍\n\nGeser pelan-pelan. Mana yang paling kamu butuhkan hari ini? Tulis nomornya di komentar.\n\n📖 “Diamlah dan ketahuilah, bahwa Akulah Allah!” — Mazmur 46:11"},
    {"slides": [("jendela", "pagi ini, pelan-pelan saja"), ("kabut", "kamu tidak harus melihat semuanya untuk melangkah"),
                ("gunung", "Dia sudah lebih dulu di sana"), ("laut", "ombak datang, ombak pergi. Dia tetap"),
                ("bintang", "dan malam ini, kamu boleh istirahat")],
     "caption": "satu hari, lima pengingat 🤍\n\n“Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.” — Mazmur 119:105\n\nSimpan untuk dibaca lagi besok pagi 🔖"},
    {"slides": [("awan", "catatan untuk hati yang lelah"), ("lilin", "berdoa walau kata-katanya habis"),
                ("jalan", "berjalan walau langkahnya kecil"), ("pohon", "bertahan walau musimnya panjang"),
                ("jendela", "Tuhan tidak pernah lelah denganmu")],
     "caption": "catatan untuk hati yang lelah 🤍\n\n“Marilah kepada-Ku, semua yang letih lesu dan berbeban berat, Aku akan memberi kelegaan kepadamu.” — Matius 11:28\n\nKirim ke seseorang yang sedang capek 💌"},
    {"slides": [("bintang", "hal-hal yang tidak berubah"), ("gunung", "kasih-Nya kemarin"), ("laut", "kasih-Nya hari ini"),
                ("awan", "kasih-Nya besok"), ("lilin", "kasih-Nya untukmu")],
     "caption": "hal-hal yang tidak berubah 🤍\n\n“Yesus Kristus tetap sama, baik kemarin maupun hari ini dan sampai selama-lamanya.” — Ibrani 13:8\n\nKetik “tetap” kalau kamu percaya 🙏"},
    {"slides": [("pohon", "untuk kamu yang sedang menunggu"), ("jendela", "menunggu bukan berarti dilupakan"),
                ("kabut", "yang belum terlihat bukan berarti tidak ada"), ("jalan", "Dia sedang menyiapkan jalannya"),
                ("laut", "tunggulah. Dia setia")],
     "caption": "untuk kamu yang sedang menunggu 🤍\n\n“Nantikanlah TUHAN! Kuatkanlah dan teguhkanlah hatimu!” — Mazmur 27:14\n\nTag seseorang yang sedang menunggu jawaban doa."},
    {"slides": [("gunung", "sebelum minggu ini selesai"), ("awan", "terima kasih untuk hari-hari yang berat"),
                ("lilin", "terima kasih untuk doa yang dijawab"), ("jalan", "terima kasih untuk doa yang belum"),
                ("bintang", "Kau tetap baik")],
     "caption": "sebelum minggu ini selesai 🤍\n\n“Mengucap syukurlah dalam segala hal, sebab itulah yang dikehendaki Allah di dalam Kristus Yesus bagi kamu.” — 1 Tesalonika 5:18\n\nTulis satu hal yang kamu syukuri minggu ini."},
]

# ---------- V: dulu vs sekarang ----------
DULU = [
    {"judul": "tentang doa",
     "pasangan": [("doa harus panjang dan indah", "doa cukup jujur"), ("Tuhan hanya dengar orang baik", "Tuhan dengar orang yang datang"),
                  ("jawaban harus cepat", "waktu-Nya lebih baik dari waktuku")],
     "ayat": "“Berserulah kepada-Ku, maka Aku akan menjawab engkau.”", "ref": "Yeremia 33:3",
     "caption": "dulu vs sekarang: tentang doa 🤍\n\nYang mana yang paling kamu rasakan? Ketik 1, 2, atau 3.\n\n📖 Yeremia 33:3"},
    {"judul": "tentang kuat",
     "pasangan": [("kuat artinya tidak menangis", "kuat artinya tetap bersandar"), ("aku harus bisa sendiri", "aku tidak pernah sendiri"),
                  ("lemah itu memalukan", "dalam lemah, kuasa-Nya sempurna")],
     "ayat": "“Cukuplah kasih karunia-Ku bagimu.”", "ref": "2 Korintus 12:9",
     "caption": "dulu vs sekarang: tentang kuat 🤍\n\nTidak apa-apa kalau hari ini kamu tidak merasa kuat.\n\n📖 2 Korintus 12:9\n\nKirim ke temanmu yang selalu terlihat kuat 💌"},
    {"judul": "tentang masa depan",
     "pasangan": [("aku harus tahu semuanya", "cukup tahu siapa yang memegangnya"), ("rencanaku harus berhasil", "rencana-Nya tidak pernah gagal"),
                  ("besok itu menakutkan", "besok, Dia sudah di sana")],
     "ayat": "“Aku ini mengetahui rancangan-rancangan apa yang ada pada-Ku mengenai kamu.”", "ref": "Yeremia 29:11",
     "caption": "dulu vs sekarang: tentang masa depan 🤍\n\nKamu tidak perlu tahu semuanya. Cukup tahu Siapa yang memegang hari esok.\n\n📖 Yeremia 29:11"},
    {"judul": "tentang nilai diriku",
     "pasangan": [("nilaiku dari pencapaian", "nilaiku dari kasih-Nya"), ("aku harus disukai semua orang", "aku sudah dikasihi sepenuhnya"),
                  ("aku terlalu rusak", "aku sedang dipulihkan")],
     "ayat": "“Engkau berharga di mata-Ku dan mulia, dan Aku ini mengasihi engkau.”", "ref": "Yesaya 43:4",
     "caption": "dulu vs sekarang: tentang nilai diriku 🤍\n\nKamu berharga, bukan karena apa yang kamu capai, tapi karena Siapa yang mengasihimu.\n\n📖 Yesaya 43:4"},
    {"judul": "tentang menunggu",
     "pasangan": [("menunggu itu buang waktu", "menunggu itu sedang dibentuk"), ("diam berarti Tuhan tidak peduli", "diam-Nya pun sedang bekerja"),
                  ("aku sudah terlambat", "tidak ada yang terlambat bagi-Nya")],
     "ayat": "“Ia membuat segala sesuatu indah pada waktunya.”", "ref": "Pengkhotbah 3:11",
     "caption": "dulu vs sekarang: tentang menunggu 🤍\n\nMasa menunggu bukan masa yang sia-sia.\n\n📖 Pengkhotbah 3:11\n\nKetik “indah pada waktunya” 🙏"},
    {"judul": "tentang kasih-Nya",
     "pasangan": [("Tuhan marah saat aku gagal", "Tuhan menunggu aku pulang"), ("kasih-Nya harus aku bayar", "kasih-Nya sudah dibayar lunas"),
                  ("aku harus sempurna dulu", "datang saja apa adanya")],
     "ayat": "“Allah menunjukkan kasih-Nya kepada kita, oleh karena Kristus telah mati untuk kita, ketika kita masih berdosa.”", "ref": "Roma 5:8",
     "caption": "dulu vs sekarang: tentang kasih-Nya 🤍\n\nKamu tidak perlu sempurna untuk dikasihi.\n\n📖 Roma 5:8\n\nSave dan baca lagi saat kamu merasa gagal 🔖"},
]

# ---------- K: tipografi sinematik ----------
# tiap frasa = satu layar; kata dengan * = disorot (serif miring, emas)
KINETIK = [
    {"frasa": ["kalau hari ini *berat*", "kamu tidak harus *mengerti* semuanya", "cukup *percaya*", "Dia masih *memegang* kamu"],
     "ref": "Yesaya 41:10",
     "caption": "Cukup percaya. Dia masih memegang kamu 🤍\n\n📖 “Janganlah takut, sebab Aku menyertai engkau… Aku akan memegang engkau dengan tangan kanan-Ku yang membawa kemenangan.” — Yesaya 41:10\n\nKirim ke seseorang yang harinya berat 💌"},
    {"frasa": ["kamu *tidak* terlambat", "kamu *tidak* tertinggal", "kamu sedang *dibentuk*", "pada *waktu-Nya*"],
     "ref": "Pengkhotbah 3:11",
     "caption": "Kamu tidak terlambat. Kamu sedang dibentuk 🤍\n\n📖 “Ia membuat segala sesuatu indah pada waktunya.” — Pengkhotbah 3:11\n\nKetik “waktu-Nya” kalau kamu percaya."},
    {"frasa": ["air mata yang kamu *sembunyikan*", "Dia *lihat*", "Dia *hitung*", "Dia *simpan*"],
     "ref": "Mazmur 56:9",
     "caption": "Tidak ada air mata yang terlewat oleh-Nya 🤍\n\n📖 “Air mataku Kautaruh ke dalam kirbat-Mu. Bukankah semuanya telah Kaudaftarkan?” — Mazmur 56:9\n\nSave untuk malam yang berat 🔖"},
    {"frasa": ["berhenti *membandingkan*", "jalanmu *bukan* jalan mereka", "Tuhanmu *sama*", "dan Dia *setia*"],
     "ref": "Mazmur 16:6",
     "caption": "Jalanmu bukan jalan mereka. Tapi Tuhanmu sama setianya 🤍\n\n📖 “Tali pengukur jatuh bagiku di tempat-tempat yang permai.” — Mazmur 16:6\n\nKirim ke temanmu yang sering membandingkan diri 💌"},
    {"frasa": ["doa yang *sama*", "setiap *malam*", "tidak *sia-sia*", "Dia *mendengar*"],
     "ref": "1 Yohanes 5:14",
     "caption": "Doa yang sama setiap malam tidak sia-sia 🤍\n\n📖 “Ia mengabulkan doa kita, jikalau kita meminta sesuatu kepada-Nya menurut kehendak-Nya.” — 1 Yohanes 5:14\n\nKetik “aku tetap berdoa” 🙏"},
    {"frasa": ["minggu ini *selesai*", "kasih-Nya *belum*", "istirahatlah", "besok *baru* lagi"],
     "ref": "Ratapan 3:22-23",
     "caption": "Minggu ini selesai. Kasih-Nya belum 🤍\n\n📖 “Tak berkesudahan kasih setia TUHAN… selalu baru tiap pagi.” — Ratapan 3:22-23\n\nSelamat beristirahat."},
]

# ---------- J: animasi karakter ----------
# adegan: senja / kabut / laut / malam / fajar;  gerak: jalan / duduk / berlutut / meraih / lentera / bangkit
JALAN = [
    {"adegan": "senja", "gerak": "jalan", "atas": "kamu tidak harus tahu", "atas2": "ke mana semua ini menuju",
     "bawah": "cukup tahu siapa", "bawah2": "yang berjalan bersamamu",
     "caption": "Cukup tahu Siapa yang berjalan bersamamu 🤍\n\n📖 “TUHAN, Dia sendiri akan berjalan di depanmu, Dia sendiri akan menyertai engkau.” — Ulangan 31:8\n\nKirim ke seseorang yang sedang bingung arah 💌"},
    {"adegan": "malam", "gerak": "duduk", "atas": "tidak apa-apa", "atas2": "duduk sebentar",
     "bawah": "Tuhan tidak pergi", "bawah2": "saat kamu berhenti",
     "caption": "Tidak apa-apa duduk sebentar 🤍\n\n📖 “Hanya dekat Allah saja aku tenang, dari pada-Nyalah keselamatanku.” — Mazmur 62:2\n\nSave untuk hari yang melelahkan 🔖"},
    {"adegan": "kabut", "gerak": "berlutut", "atas": "saat kata-kata habis", "atas2": "",
     "bawah": "Dia mengerti", "bawah2": "doa yang tidak terucap",
     "caption": "Saat kata-kata habis, Dia tetap mengerti 🤍\n\n📖 “Roh sendiri berdoa untuk kita kepada Allah dengan keluhan-keluhan yang tidak terucapkan.” — Roma 8:26\n\nKetik 🙏 dan kami ikut mendoakanmu."},
    {"adegan": "fajar", "gerak": "meraih", "atas": "pagi selalu datang", "atas2": "",
     "bawah": "setelah malam", "bawah2": "yang paling panjang",
     "caption": "Pagi selalu datang 🤍\n\n📖 “Sepanjang malam ada tangisan, menjelang pagi terdengar sorak-sorai.” — Mazmur 30:6\n\nKirim ke seseorang yang sedang melewati malam panjang 💌"},
    {"adegan": "malam", "gerak": "lentera", "atas": "terangnya cukup", "atas2": "untuk satu langkah",
     "bawah": "dan itu", "bawah2": "sudah cukup",
     "caption": "Terang untuk satu langkah itu sudah cukup 🤍\n\n📖 “Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.” — Mazmur 119:105\n\nSave untuk hari yang tidak jelas 🔖"},
    {"adegan": "laut", "gerak": "bangkit", "atas": "jatuh bukan akhirnya", "atas2": "",
     "bawah": "Dia mengangkatmu", "bawah2": "lagi dan lagi",
     "caption": "Jatuh bukan akhir ceritamu 🤍\n\n📖 “Apabila ia jatuh, tidaklah sampai tergeletak, sebab TUHAN menopang tangannya.” — Mazmur 37:24\n\nKetik “bangkit” kalau kamu sedang berjuang."},
]

# hari 2-7: slot tambahan -> (format, index)
JADWAL = {d: {"pagi3": ("F", d - 2), "siang0": ("V", d - 2), "siang2": ("K", d - 2), "malam0": ("J", d - 2)} for d in range(2, 8)}
