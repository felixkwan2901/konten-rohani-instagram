"""@kapi.percaya - konten tambahan minggu 1 (5 post/hari mulai hari 2). Kutipan ayat: Alkitab TB.
Format:
  KATA  = kata besar (sama seperti konten/kapi.py), dipakai sebagai gambar (07:00) atau Reels (15:00)
  KOMIK = carousel 4 slide lucu: tiap slide = (teks, ekspresi, properti); slide terakhir + ayat
  PILIH = "pilih satu": dua pilihan A/B, jawab di komentar
Ekspresi: senang | capek | merem | sedih | semangat. Properti: alkitab | jeruk | keringat | hati | bintang | none."""

TAGS = "#kapi #kristen #anakmudakristen #renungan #ayatalkitab #kristenindonesia #humorkristen"

KATA = [
    {"bg": "#1E9BD7", "atas": "belum ada jawaban?", "besar": "HARAPAN", "bawah": "masih ada kok.", "ekspresi": "senang", "properti": "bintang",
     "caption": "doanya belum dijawab? harapannya belum habis kok 🌟\n\n“Semoga Allah, sumber pengharapan, memenuhi kamu dengan segala sukacita dan damai sejahtera dalam iman kamu.” — Roma 15:13\n\nketik 🌟 kalau kamu masih berharap"},
    {"bg": "#D6456B", "atas": "ngerasa nggak disayang?", "besar": "KASIH", "bawah": "Dia penuh buat kamu.", "ekspresi": "merem", "properti": "hati",
     "caption": "kamu disayang lebih dari yang kamu kira 🤍\n\n“Kita mengasihi, karena Allah lebih dahulu mengasihi kita.” — 1 Yohanes 4:19\n\ntag orang yang perlu dengar ini 👇"},
    {"bg": "#16324F", "atas": "orang bisa berubah,", "besar": "SETIA", "bawah": "Dia tetap.", "ekspresi": "senang", "properti": "alkitab",
     "caption": "teman bisa pergi, mood bisa naik turun. Dia tetap sama 🧡\n\n“Yesus Kristus tetap sama, baik kemarin maupun hari ini dan sampai selama-lamanya.” — Ibrani 13:8\n\nsave buat pengingat 🔖"},
    {"bg": "#111111", "atas": "lagi lemah banget?", "besar": "KUAT", "bawah": "di dalam Dia, kamu.", "ekspresi": "semangat", "properti": "none",
     "caption": "lemahmu bukan akhir cerita 💪\n\n“…sebab jika aku lemah, maka aku kuat.” — 2 Korintus 12:10\n\nkirim ke bestie yang lagi capek banget"},
    {"bg": "#2F5E45", "atas": "hati lagi patah?", "besar": "PULIH", "bawah": "bisa, pelan-pelan.", "ekspresi": "sedih", "properti": "hati",
     "caption": "patah hati itu nyata. pemulihan juga nyata 🤍\n\n“Ia menyembuhkan orang-orang yang patah hati dan membalut luka-luka mereka.” — Mazmur 147:3\n\nketik 🤍 kalau kamu lagi di fase ini"},
    {"bg": "#EDE6DA", "atas": "kepala lagi berisik?", "besar": "DAMAI", "bawah": "ada di Dia.", "ekspresi": "merem", "properti": "none",
     "caption": "overthinking mode on? tarik napas dulu 🫧\n\n“Damai sejahtera Allah, yang melampaui segala akal, akan memelihara hati dan pikiranmu dalam Kristus Yesus.” — Filipi 4:7\n\nsave buat malam-malam yang berisik 🔖"},
    {"bg": "#F26B1D", "atas": "pengen semuanya cepet?", "besar": "SABAR", "bawah": "dulu, bestie.", "ekspresi": "capek", "properti": "keringat",
     "caption": "prosesnya lama? itu bukan berarti Tuhan lupa ⏳\n\n“Adalah baik menanti dengan diam pertolongan TUHAN.” — Ratapan 3:26\n\nketik ⏳ kalau kamu lagi nunggu sesuatu"},
    {"bg": "#F4F4F2", "atas": "ngerasa kurang terus?", "besar": "CUKUP", "bawah": "kasih karunia-Nya.", "ekspresi": "merem", "properti": "alkitab",
     "caption": "nggak perlu jadi versi paling hebat buat dikasihi 🤍\n\n“Cukuplah kasih karunia-Ku bagimu.” — 2 Korintus 12:9\n\nkirim ke temen yang suka ngerasa kurang"},
    {"bg": "#1E9BD7", "atas": "kemarin gagal?", "besar": "BARU", "bawah": "hari ini lembaran.", "ekspresi": "semangat", "properti": "jeruk",
     "caption": "gagal kemarin nggak menentukan hari ini 🍊\n\n“Jadi siapa yang ada di dalam Kristus, ia adalah ciptaan baru: yang lama sudah berlalu, sesungguhnya yang baru sudah datang.” — 2 Korintus 5:17\n\nketik “BARU” buat mulai lagi hari ini"},
    {"bg": "#111111", "atas": "lagi di masa gelap?", "besar": "TERANG", "bawah": "tetap bersinar.", "ekspresi": "senang", "properti": "bintang",
     "caption": "gelap bukan berarti Dia nggak ada ✨\n\n“Akulah terang dunia; barangsiapa mengikut Aku, ia tidak akan berjalan dalam kegelapan, melainkan ia akan mempunyai terang hidup.” — Yohanes 8:12\n\nsave & share 🔖"},
    {"bg": "#5E7F63", "atas": "takut sama masa depan?", "besar": "AMAN", "bawah": "di tangan-Nya.", "ekspresi": "merem", "properti": "hati",
     "caption": "masa depan mungkin belum jelas. tapi tangan yang pegang kamu jelas 🤍\n\n“…Aku ini, TUHAN, Allahmu, memegang tangan kananmu dan berkata kepadamu: ‘Janganlah takut, Akulah yang menolong engkau.’” — Yesaya 41:13\n\ntag temen yang lagi galau soal masa depan"},
    {"bg": "#16324F", "atas": "dunia lagi berat?", "besar": "MENANG", "bawah": "Yesus sudah.", "ekspresi": "semangat", "properti": "alkitab",
     "caption": "hari ini berat? endingnya udah jelas kok 🙌\n\n“…kuatkanlah hatimu, Aku telah mengalahkan dunia.” — Yohanes 16:33\n\nketik “AMIN” kalau percaya"},
]

KOMIK = [
    {"judul": "Kapi & saat teduh jam 5 pagi", "bg": "#FBE8C8",
     "slides": [("niat semalam: bangun jam 5, saat teduh", "semangat", "bintang"),
                ("jam 5 pagi: snooze… snooze… snooze…", "capek", "keringat"),
                ("jam 7: telat lagi.", "sedih", "none"),
                ("tenang, Tuhan masih nunggu kok. rahmat-Nya selalu baru tiap pagi", "senang", "alkitab")],
     "ayat": "“Tak berkesudahan kasih setia TUHAN… selalu baru tiap pagi.” — Ratapan 3:22-23",
     "caption": "siapa di sini yang saat teduhnya kalah sama tombol snooze? 🙋‍♂️😂\n\ntenang, besok pagi rahmat-Nya baru lagi. yang penting mulai lagi, bukan sempurna.\n\n“Tak berkesudahan kasih setia TUHAN… selalu baru tiap pagi.” — Ratapan 3:22-23\n\ntag temen yang paling jago snooze 👇"},
    {"judul": "Kapi & lagu pujian baru", "bg": "#DCEBFA",
     "slides": [("worship leader: “kita nyanyi lagu baru ya”", "capek", "keringat"),
                ("Kapi: pura-pura hafal liriknya", "merem", "none"),
                ("lalu… lagu favorit Kapi diputar", "semangat", "bintang"),
                ("yang penting hatinya, bukan hafalannya", "senang", "hati")],
     "ayat": "“Beribadahlah kepada TUHAN dengan sukacita, datanglah ke hadapan-Nya dengan sorak-sorai!” — Mazmur 100:2",
     "caption": "jujur, siapa yang suka komat-kamit pas lagu baru? 😂🎶\n\nyang Tuhan lihat hatinya, bukan hafalannya.\n\n“Beribadahlah kepada TUHAN dengan sukacita.” — Mazmur 100:2\n\nsebutin lagu pujian favoritmu di komentar 👇"},
    {"judul": "Kapi & doa makan bersama", "bg": "#FDE2D8",
     "slides": [("doa makan dimulai…", "merem", "none"),
                ("5 menit kemudian: masih mendoakan satu RT", "capek", "keringat"),
                ("makanannya udah dingin", "sedih", "none"),
                ("tapi bersyukur itu nggak pernah salah", "senang", "jeruk")],
     "ayat": "“Mengucap syukurlah dalam segala hal.” — 1 Tesalonika 5:18",
     "caption": "doa makan versi keluarga besar: makanannya dingin, hatinya hangat 😂🙏\n\n“Mengucap syukurlah dalam segala hal.” — 1 Tesalonika 5:18\n\ndi keluargamu siapa yang doanya paling panjang? tag dia 👇"},
    {"judul": "Kapi & dibanding-bandingin", "bg": "#E6F2E6",
     "slides": [("“kok kamu nggak kayak si A sih?”", "sedih", "none"),
                ("mulai overthinking", "capek", "keringat"),
                ("buka Alkitab", "merem", "alkitab"),
                ("“engkau berharga di mata-Ku.” Kapi: oh iya ya", "senang", "hati")],
     "ayat": "“Oleh karena engkau berharga di mata-Ku dan mulia, dan Aku ini mengasihi engkau…” — Yesaya 43:4",
     "caption": "dibandingin sama orang lain itu nggak enak. tapi penilaian Tuhan yang paling penting 🤍\n\n“Oleh karena engkau berharga di mata-Ku dan mulia, dan Aku ini mengasihi engkau.” — Yesaya 43:4\n\nketik 🤍 kalau kamu butuh diingatkan ini"},
    {"judul": "Kapi & “nanti aku doain ya”", "bg": "#F3E8FA",
     "slides": [("teman: “doain aku ya”", "senang", "none"),
                ("Kapi: “pasti!”", "semangat", "bintang"),
                ("3 hari kemudian… lupa", "sedih", "none"),
                ("tips: doain saat itu juga, langsung", "merem", "alkitab")],
     "ayat": "“Tetaplah berdoa.” — 1 Tesalonika 5:17",
     "caption": "“nanti aku doain ya” … lalu lupa 😭 siapa yang pernah?\n\ntips dari Kapi: doakan saat itu juga, jangan ditunda.\n\n“Tetaplah berdoa.” — 1 Tesalonika 5:17\n\nmau didoakan? tulis di komentar, kita doakan sekarang 🙏"},
    {"judul": "Kapi dari Senin sampai Sabtu", "bg": "#FFF3C4",
     "slides": [("Senin pagi", "capek", "keringat"),
                ("Rabu", "sedih", "none"),
                ("Jumat sore", "semangat", "bintang"),
                ("tiap hari tetap ada kasih karunia-Nya", "senang", "jeruk")],
     "ayat": "“Inilah hari yang dijadikan TUHAN, mari kita bersorak-sorak dan bersukacita karenanya!” — Mazmur 118:24",
     "caption": "Kapi dari Senin sampai Sabtu. kamu di fase yang mana? 😂🍊\n\n“Inilah hari yang dijadikan TUHAN, mari kita bersorak-sorak dan bersukacita karenanya!” — Mazmur 118:24\n\nselamat akhir pekan! besok jangan lupa ibadah ya 🙏"},
]

PILIH = [
    {"bg": "#1E9BD7", "a": "saat teduh pagi", "b": "saat teduh malam", "ekspresi": "senang",
     "caption": "PILIH SATU 👇\n\nA = saat teduh pagi ☀️\nB = saat teduh malam 🌙\n\njawab A atau B di komentar. Kapi tim A (walaupun sering snooze 😅)\n\n“TUHAN, pada waktu pagi Engkau mendengar seruanku.” — Mazmur 5:4"},
    {"bg": "#16324F", "a": "lagu pujian", "b": "lagu penyembahan", "ekspresi": "semangat",
     "caption": "PILIH SATU 👇\n\nA = lagu pujian (yang semangat) 🎶\nB = lagu penyembahan (yang pelan) 🙏\n\njawab A atau B, sebutin lagunya juga!\n\n“…sambil menyanyikan mazmur, dan puji-pujian dan nyanyian rohani, kamu mengucap syukur kepada Allah di dalam hatimu.” — Kolose 3:16"},
    {"bg": "#2F5E45", "a": "ibadah pagi", "b": "ibadah sore", "ekspresi": "merem",
     "caption": "PILIH SATU 👇\n\nA = ibadah pagi 🌅\nB = ibadah sore 🌆\n\ngereja kamu ibadah jam berapa? tulis di komentar!\n\n“Janganlah kita menjauhkan diri dari pertemuan-pertemuan ibadah kita.” — Ibrani 10:25"},
    {"bg": "#F26B1D", "a": "Alkitab cetak", "b": "Alkitab di HP", "ekspresi": "senang",
     "caption": "PILIH SATU 👇\n\nA = Alkitab cetak 📖\nB = Alkitab di aplikasi HP 📱\n\nyang penting dibaca, bukan cuma dipajang 😂\n\n“Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.” — Mazmur 119:105"},
    {"bg": "#111111", "a": "doa sendiri", "b": "doa bareng-bareng", "ekspresi": "semangat",
     "caption": "PILIH SATU 👇\n\nA = doa sendiri 🙇\nB = doa bareng-bareng 🙌\n\ndua-duanya penting sih. tapi kamu lebih nyaman yang mana?\n\n“Sebab di mana dua atau tiga orang berkumpul dalam Nama-Ku, di situ Aku ada di tengah-tengah mereka.” — Matius 18:20"},
]

# hari 2..7: slot -> (format, indeks). "wallpaper" = carousel wallpaper set1 yang sudah ada.
JADWAL = {
    2: {"pagi": ("kata", 0), "siang": ("komik", 0), "sore": ("reel", 1), "larut": ("wallpaper", 0)},
    3: {"pagi": ("kata", 2), "siang": ("komik", 1), "sore": ("reel", 3), "larut": ("pilih", 0)},
    4: {"pagi": ("kata", 4), "siang": ("komik", 2), "sore": ("reel", 5), "larut": ("pilih", 1)},
    5: {"pagi": ("kata", 6), "siang": ("komik", 3), "sore": ("reel", 7), "larut": ("pilih", 2)},
    6: {"pagi": ("kata", 8), "siang": ("komik", 4), "sore": ("reel", 9), "larut": ("pilih", 3)},
    7: {"pagi": ("kata", 10), "siang": ("komik", 5), "sore": ("reel", 11), "larut": ("pilih", 4)},
}
