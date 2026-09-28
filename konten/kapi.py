"""Akun Kapi - minggu 1. Gaya leopardlift: kalimat santai + satu KATA BESAR + maskot.
Kapi adalah karakter original (kapibara), jadi aman dari hak cipta karakter lain.
Kata besar sengaja bervariasi (tidak selalu YESUS) supaya feed tidak monoton.

ekspresi: senang | capek | merem | sedih | semangat
properti: alkitab | jeruk | keringat | hati | bintang | none (boleh digabung dengan '+')"""

TAGS = "#yesus #kristen #anakmudakristen #renungan #ayatalkitab #kristenindonesia #kapi"

POSTS = [
    {"bg": "#111111", "atas": "capek ya, bro?", "besar": "YESUS", "bawah": "masih pegang kamu.", "ekspresi": "capek", "properti": "keringat",
     "caption": "capek ya, bro? 🫠\nistirahat dulu. Yesus nggak ke mana-mana.\n\n“Marilah kepada-Ku, semua yang letih lesu dan berbeban berat, Aku akan memberi kelegaan kepadamu.” — Matius 11:28\n\ntag temen yang lagi capek 👇"},
    {"bg": "#1E9BD7", "atas": "hidup lagi berat-beratnya,", "besar": "TUHAN", "bawah": "lagi setia-setianya.", "ekspresi": "senang", "properti": "jeruk",
     "caption": "hidup boleh naik turun, kasih setia-Nya flat terus — flat di level maksimal 📈\n\n“Tak berkesudahan kasih setia TUHAN... selalu baru tiap pagi.” — Ratapan 3:22-23\n\nsave buat hari Senin berikutnya 🔖"},
    {"bg": "#EDE6DA", "atas": "bilang “aku gapapa”,", "besar": "DIA", "bawah": "tau kamu kenapa-napa.", "ekspresi": "sedih", "properti": "hati",
     "caption": "kamu bisa bohong ke semua orang. tapi nggak ke Dia 🤍\nDan kabar baiknya: Dia tetap sayang.\n\n“TUHAN, Engkau menyelidiki dan mengenal aku.” — Mazmur 139:1\n\nketik 🤍 kalau ini kamu banget"},
    {"bg": "#F4F4F2", "atas": "hari buruk?", "besar": "DOA", "bawah": "dulu, baru panik.", "ekspresi": "merem", "properti": "alkitab",
     "caption": "sebelum overthinking, coba over-praying dulu 🙏\n\n“Janganlah hendaknya kamu kuatir tentang apa pun juga, tetapi nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa dan permohonan dengan ucapan syukur.” — Filipi 4:6\n\nkirim ke bestie yang suka panik duluan 👇"},
    {"bg": "#2F5E45", "atas": "gak bisa benerin diri sendiri?", "besar": "ANUGERAH", "bawah": "yang benerin.", "ekspresi": "senang", "properti": "bintang",
     "caption": "bukan hasil usahamu. itu hadiah 🎁\n\n“Sebab karena kasih karunia kamu diselamatkan oleh iman; itu bukan hasil usahamu, tetapi pemberian Allah.” — Efesus 2:8\n\nketik “AMIN” kalau setuju 🙌"},
    {"bg": "#16324F", "atas": "jalan gak selalu mulus,", "besar": "IMAN", "bawah": "bikin tetap jalan.", "ekspresi": "semangat", "properti": "alkitab",
     "caption": "nggak harus lihat semuanya dulu baru melangkah 🚶\n\n“Sebab hidup kami ini adalah hidup karena percaya, bukan karena melihat.” — 2 Korintus 5:7\n\nsave & share 🔖"},
    {"bg": "#F26B1D", "atas": "hari Minggu gini,", "besar": "SYUKUR", "bawah": "dulu, bestie.", "ekspresi": "semangat", "properti": "jeruk+bintang",
     "caption": "selamat hari Minggu! sebutin satu hal yang kamu syukuri minggu ini 👇🧡\n\n“Mengucap syukurlah dalam segala hal, sebab itulah yang dikehendaki Allah di dalam Kristus Yesus bagi kamu.” — 1 Tesalonika 5:18\n\nfollow @{handle} biar tiap hari diingetin 🧡"},
    {"bg": "#F2B705", "atas": "minggu ini melelahkan?", "besar": "SUKACITA", "bawah": "tetap dari Tuhan.", "ekspresi": "semangat", "properti": "jeruk+bintang",
     "caption": "capeknya nyata, tapi sukacitanya lebih kuat 🍊✨\n\n“Jangan kamu bersusah hati, sebab sukacita karena TUHAN itulah perlindunganmu!” — Nehemia 8:11\n\nsebutin satu hal yang bikin kamu senyum minggu ini 👇"},
]


# ---------- set wallpaper (carousel 5 slide + file wallpaper HP untuk dikirim lewat DM) ----------
# Pola leopardlift: satu post = 5 desain, caption ajak komen kata kunci -> kirim wallpaper ke DM.

WALLPAPER = {
    "nama": "set1",
    "kata_kunci": "KAPI",
    "desain": [
        {"bg": "#16324F", "atas": "lagi overthinking?", "besar": "TENANG", "bawah": "Tuhan pegang kendali.", "ekspresi": "merem", "properti": "none"},
        {"bg": "#F26B1D", "atas": "nggak ada yang lihat usahamu?", "besar": "DIA", "bawah": "lihat kok.", "ekspresi": "senang", "properti": "hati"},
        {"bg": "#5E7F63", "atas": "capek banget ya?", "besar": "ISTIRAHAT", "bawah": "di dalam Dia.", "ekspresi": "capek", "properti": "keringat"},
        {"bg": "#EDE6DA", "atas": "ngerasa gagal lagi?", "besar": "ANUGERAH", "bawah": "masih berlaku.", "ekspresi": "senang", "properti": "bintang"},
        {"bg": "#111111", "atas": "apa pun yang terjadi,", "besar": "YESUS", "bawah": "tetap Tuhan.", "ekspresi": "semangat", "properti": "alkitab"},
    ],
    "caption": "5 pengingat buat layar HP kamu 📱🧡\ngeser sampai habis, pilih yang paling “kamu banget” 👉\n\n“Aku menyertai kamu senantiasa sampai kepada akhir zaman.” — Matius 28:20\n\nkomen “{kata_kunci}” nanti aku kirim kelima wallpaper-nya (ukuran pas buat HP) ke DM kamu ✨\n\nfollow @{handle} biar tiap hari diingetin 🍊",
    "dm": "Haii! Makasih udah komen 🧡\nIni 5 wallpaper Kapi buat HP kamu. Semoga tiap buka layar, kamu inget: Tuhan tetap pegang kamu.\n\nKalau kepake, boleh tag @{handle} di story ya 🍊",
}
