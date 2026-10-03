"""Akun Tenang (@diam.dan.percaya) - slot tambahan (Sabtu 3 Okt - Sabtu 17 Okt 2026).
Skema sama dengan konten/tenang_w3.py:
  BUKU = halaman buku terbuka: judul serif + puisi pendek (3-6 baris, maks 42 karakter per baris).
         Diposting larut (22:30 WIB): renungan malam sebelum tidur.
  MEME = foto hitam-putih + teks besar putih bergaris tepi, doa jujur orang pertama (maks 90 karakter).
         foto: laut, gunung, kabut, bintang, awan, jendela, lilin, jalan, pohon, panggung
         Diposting sore (16:30 WIB): capek pulang kerja/sekolah, macet, menunggu, kemenangan kecil.
Hari 1 dan 8 = hari Minggu. Hari 7 dan 14 malam = "besok hari Minggu".
Kutipan ayat: Alkitab TB. Caption tanpa hashtag."""

# ---------- BUKU: halaman buku terbuka (larut 22:30) ----------
BUKU = [
    # 0 - Sabtu 3 Okt
    {"judul": "Malam Minggu",
     "baris": ["Tidak ke mana-mana malam ini,", "tidak ada rencana besar.", "Cuma aku, lampu kamar yang redup,",
               "dan Engkau yang tidak pernah buru-buru."],
     "caption": "Malam Minggu tanpa rencana? Tidak apa-apa 🤍\n\nKadang yang paling dibutuhkan jiwa bukan keramaian, tapi sedikit ketenangan bersama Tuhan.\n\n📖 “Segenggam ketenangan lebih baik dari pada dua genggam jerih payah dan usaha menjaring angin.” — Pengkhotbah 4:6\n\nKetik 🤍 kalau malam ini kamu juga di rumah saja."},
    # 1 - Minggu 4 Okt
    {"judul": "Sisa Hari Minggu",
     "baris": ["Bangku gereja sudah sepi,", "tapi lagu tadi pagi masih terngiang.", "Besok Senin datang lagi,",
               "dan kasih-Mu ikut pulang bersamaku."],
     "caption": "Hari Minggu hampir selesai 🌙\n\nIbadahnya sudah lewat, tapi kebaikan-Nya tidak berhenti di pintu gereja. Dia ikut pulang, ikut masuk ke hari Senin-mu.\n\n📖 “Kebajikan dan kemurahan belaka akan mengikuti aku, seumur hidupku; dan aku akan diam dalam rumah TUHAN sepanjang masa.” — Mazmur 23:6\n\nSelamat malam. Save untuk Minggu malam berikutnya 🔖"},
    # 2 - Senin 5 Okt
    {"judul": "Senin Sudah Lewat",
     "baris": ["Hari pertama sudah lewat.", "Tidak semuanya lancar,", "tapi aku masih di sini,",
               "karena Engkau yang menopangku.", "Sekarang aku mau tidur."],
     "caption": "Senin sudah lewat. Kamu berhasil melewatinya 🤍\n\nTidak harus sempurna. Kamu masih di sini karena Dia yang menopangmu, dan Dia juga yang menjagamu sampai besok pagi.\n\n📖 “Aku membaringkan diri, lalu tidur; aku bangun, sebab TUHAN menopang aku!” — Mazmur 3:6\n\nKetik “Amin” sebelum kamu tidur malam ini."},
    # 3 - Selasa 6 Okt
    {"judul": "Kata yang Tertahan",
     "baris": ["Ada kata yang hampir kuucapkan,", "kesal yang belum juga reda.", "Kubawa semuanya ke tempat tidur,",
               "bukan untuk kuulang-ulang,", "tapi untuk kuserahkan pada-Mu."],
     "caption": "Untuk kesal yang belum reda malam ini 🌙\n\nMarah itu manusiawi. Tapi malam ini, bawa ke hadapan Tuhan dulu sebelum dibawa ke kolom chat.\n\n📖 “Biarlah kamu marah, tetapi jangan berbuat dosa; berkata-katalah dalam hatimu di tempat tidurmu, tetapi tetaplah diam.” — Mazmur 4:5\n\nSave untuk malam kamu ingin membalas pesan dengan emosi 🔖"},
    # 4 - Rabu 7 Okt
    {"judul": "Sebelum Lampu Padam",
     "baris": ["Sebentar lagi lampu kumatikan.", "Gelap akan memenuhi kamar ini,", "tapi tidak akan memenuhi hatiku,",
               "karena terang-Mu tetap menyala", "bahkan saat mataku terpejam."],
     "caption": "Sebelum lampu padam 💡\n\nGelap di kamar tidak sama dengan gelap di hati. Terang-Nya tidak ikut padam saat kamu menekan sakelar.\n\n📖 “Terang itu bercahaya di dalam kegelapan dan kegelapan itu tidak menguasainya.” — Yohanes 1:5\n\nKirim ke temanmu yang malamnya sering terasa berat 💌"},
    # 5 - Kamis 8 Okt
    {"judul": "Di Tempat Tidurku",
     "baris": ["Kalau mataku belum mau terpejam,", "biar aku mengingat-Mu saja.", "Satu per satu kebaikan-Mu hari ini,",
               "sampai aku tertidur", "di bawah naungan sayap-Mu."],
     "caption": "Susah tidur? Coba ingat kebaikan-Nya satu per satu 🌙\n\nDaud juga pernah terjaga di malam hari. Yang dia lakukan: mengingat Tuhan.\n\n📖 “…apabila aku ingat kepada-Mu di tempat tidurku, merenungkan Engkau sepanjang kawal malam, — sungguh Engkau telah menjadi pertolonganku, dan dalam naungan sayap-Mu aku bersorak-sorai.” — Mazmur 63:7-8\n\nKirim ke temanmu yang sering begadang 💌"},
    # 6 - Jumat 9 Okt
    {"judul": "Lelah yang Jujur",
     "baris": ["Badanku capek,", "tapi capek yang jujur.", "Seminggu bekerja, belajar, bertahan.",
               "Sekarang aku mau beristirahat", "tanpa merasa bersalah."],
     "caption": "Capek yang jujur boleh istirahat dengan tenang 🤍\n\nSeminggu ini kamu sudah bekerja, belajar, bertahan. Malam ini tidurlah tanpa rasa bersalah.\n\n📖 “Enak tidurnya orang yang bekerja, baik ia makan sedikit maupun banyak…” — Pengkhotbah 5:11\n\nSelamat berakhir pekan. Ketik 🤍 kalau kamu juga sudah capek."},
    # 7 - Sabtu 10 Okt (besok hari Minggu)
    {"judul": "Baju untuk Besok",
     "baris": ["Baju untuk besok sudah kusiapkan,", "Alkitab sudah di dekat pintu.", "Tinggal hatiku, Tuhan,",
               "tolong siapkan juga,", "supaya besok aku datang dengan rindu."],
     "caption": "Besok hari Minggu 🤍\n\nBaju sudah siap. Bagaimana dengan hatinya? Malam ini, minta Tuhan menyiapkan hatimu untuk datang dengan sukacita.\n\n📖 “Beribadahlah kepada TUHAN dengan sukacita, datanglah ke hadapan-Nya dengan sorak-sorai!” — Mazmur 100:2\n\nTag teman yang besok ibadah bareng kamu 👇"},
    # 8 - Minggu 11 Okt
    {"judul": "Sehari di Rumah-Mu",
     "baris": ["Hari ini aku duduk di rumah-Mu", "bersama orang-orang yang juga lelah.",
               "Kami bernyanyi dengan suara pas-pasan,", "tapi kami pulang", "membawa sesuatu yang baru."],
     "caption": "Satu hari di rumah Tuhan 🏠\n\nMungkin suaramu fals, mungkin kamu datang terlambat. Tapi ada yang dipulihkan hari ini, walau pelan.\n\n📖 “Sebab lebih baik satu hari di pelataran-Mu dari pada seribu hari di tempat lain…” — Mazmur 84:11\n\nKetik “Amin” kalau hari ini kamu bersyukur bisa beribadah."},
    # 9 - Senin 12 Okt
    {"judul": "Jadwal Besok Pagi",
     "baris": ["Jadwal besok sudah penuh,", "pikiranku sudah duluan ke sana.", "Tuhan, tarik aku kembali",
               "ke malam ini, ke napas ini,", "ke dekat-Mu."],
     "caption": "Pikiranmu sudah duluan ke besok pagi? 🌙\n\nBesok biar besok. Malam ini, kamu boleh tenang dan percaya.\n\n📖 “Janganlah gelisah hatimu; percayalah kepada Allah, percayalah juga kepada-Ku.” — Yohanes 14:1\n\nSave untuk malam sebelum hari yang padat 🔖"},
    # 10 - Selasa 13 Okt
    {"judul": "Pengakuan Malam Ini",
     "baris": ["Hari ini aku salah lagi,", "kata-kataku tajam, sabarku pendek.", "Aku mengaku, Tuhan.",
               "Dan aku tidur malam ini", "bukan dalam hukuman, tapi dalam kasih-Mu."],
     "caption": "Mengaku, lalu tidur dalam kasih-Nya 🤍\n\nKesalahan hari ini nyata. Tapi di dalam Kristus, kamu tidak tidur sebagai orang yang dihukum.\n\n📖 “Demikianlah sekarang tidak ada penghukuman bagi mereka yang ada di dalam Kristus Yesus.” — Roma 8:1\n\nKetik “Amin” kalau malam ini kamu menerima pengampunan-Nya."},
    # 11 - Rabu 14 Okt
    {"judul": "Nyanyian Malam",
     "baris": ["Tidak ada yang mendengar", "lagu yang kusenandungkan pelan.", "Tapi Engkau mendengar,",
               "dan itu sudah cukup", "untuk menutup hari ini."],
     "caption": "Senandung pelan sebelum tidur 🎶\n\nLagu yang paling jujur kadang dinyanyikan sendirian di kamar. Siang hari Dia menyertai, malam hari Dia mendengar.\n\n📖 “TUHAN memerintahkan kasih setia-Nya pada siang hari, dan pada malam hari aku menyanyikan nyanyian, suatu doa kepada Allah kehidupanku.” — Mazmur 42:9\n\nLagu rohani apa yang kamu senandungkan malam ini? Tulis di komentar 👇"},
    # 12 - Kamis 15 Okt
    {"judul": "Kesetiaan-Mu Malam Ini",
     "baris": ["Hari ini Engkau setia", "di hal-hal yang hampir kulewatkan:", "jalan pulang yang aman,",
               "makan malam yang hangat,", "dan napas yang masih ada."],
     "caption": "Kesetiaan-Nya hari ini, dalam hal-hal kecil 🤍\n\nSebelum tidur, coba hitung: di mana saja Tuhan setia hari ini? Biasanya lebih banyak dari yang kita kira.\n\n📖 “…memberitakan kasih setia-Mu di waktu pagi dan kesetiaan-Mu di waktu malam…” — Mazmur 92:3\n\nSave dan baca lagi sebelum tidur besok malam 🔖"},
    # 13 - Jumat 16 Okt
    {"judul": "Tinggallah, Tuhan",
     "baris": ["Hari sudah menjelang malam,", "minggu ini pun hampir selesai.", "Seperti dua murid di Emaus,",
               "aku cuma minta satu hal:", "tinggallah bersamaku, Tuhan."],
     "caption": "Tinggallah bersamaku, Tuhan 🌙\n\nDua murid dalam perjalanan ke Emaus tidak mau Yesus pergi saat hari mulai gelap. Malam ini, itu juga doa kita.\n\n📖 “…Tinggallah bersama-sama dengan kami, sebab hari telah menjelang malam dan matahari hampir terbenam…” — Lukas 24:29\n\nKetik “tinggallah” sebagai doamu malam ini 🙏"},
    # 14 - Sabtu 17 Okt (besok hari Minggu)
    {"judul": "Untuk yang Melayani",
     "baris": ["Untuk yang besok berkhotbah,", "yang bernyanyi di depan,", "yang menyambut di pintu,",
               "yang mengajar anak-anak:", "kuatkan mereka malam ini, Tuhan."],
     "caption": "Besok hari Minggu 🤍\n\nMalam ini, doakan mereka yang besok melayani: pendeta, tim musik, penyambut, guru sekolah minggu, tim multimedia. Mereka juga bisa lelah.\n\n📖 “Aku mengucap syukur kepada Allahku setiap kali aku mengingat kamu.” — Filipi 1:3\n\nTag satu orang yang melayani di gerejamu, bilang terima kasih 👇"},
]


# ---------- MEME: foto hitam-putih + doa jujur (sore2 16:30; hari 0 = malam1) ----------
MEME = [
    # 0 - Sabtu 3 Okt (malam)
    {"teks": "Tuhan, minggu ini panjang sekali. Malam ini aku cuma mau duduk diam di dekat-Mu.",
     "foto": "lilin",
     "caption": "Duduk diam di dekat-Nya 🕯️\n\nTidak perlu doa yang panjang. Kadang cukup diam, dan tahu bahwa harapanmu ada pada-Nya.\n\n📖 “Hanya pada Allah saja kiranya aku tenang, sebab dari pada-Nyalah harapanku.” — Mazmur 62:6\n\nKetik “Amin” kalau malam ini kamu juga butuh tenang."},
    # 1 - Minggu 4 Okt
    {"teks": "Tuhan, khotbah tadi pagi kena banget. Tolong aku tetap ingat waktu Senin datang.",
     "foto": "panggung",
     "caption": "Khotbahnya kena banget? Jangan berhenti di situ 🤍\n\nBagian tersulit dari ibadah hari Minggu bukan mendengarkan, tapi melakukannya hari Senin.\n\n📖 “Tetapi hendaklah kamu menjadi pelaku firman dan bukan hanya pendengar saja; sebab jika tidak demikian kamu menipu diri sendiri.” — Yakobus 1:22\n\nTulis satu hal dari khotbah tadi yang mau kamu lakukan minggu ini 👇"},
    # 2 - Senin 5 Okt
    {"teks": "Tuhan, macetnya nggak gerak-gerak. Ajar aku sabar, minimal sampai lampu hijau.",
     "foto": "jalan",
     "caption": "Doa di tengah macet 🚗\n\nSabar memang tidak datang sekaligus. Roh-Nya menumbuhkannya pelan-pelan, bahkan lewat lampu merah yang lama.\n\n📖 “Tetapi buah Roh ialah: kasih, sukacita, damai sejahtera, kesabaran, kemurahan, kebaikan, kesetiaan, kelemahlembutan, penguasaan diri.” — Galatia 5:22-23\n\nKirim ke temanmu yang lagi kejebak macet sekarang 💌"},
    # 3 - Selasa 6 Okt
    {"teks": "Tuhan, tugasku numpuk dan otakku sudah penuh. Kasih aku hikmat, dan sedikit tidur.",
     "foto": "bintang",
     "caption": "Untuk yang tugasnya menumpuk 📚\n\nMinta hikmat itu bukan tanda lemah. Tuhan memberikannya dengan murah hati, tanpa mengungkit-ungkit.\n\n📖 “Tetapi apabila di antara kamu ada yang kekurangan hikmat, hendaklah ia memintakannya kepada Allah, — yang memberikan kepada semua orang dengan murah hati dan dengan tidak membangkit-bangkit —, maka hal itu akan diberikan kepadanya.” — Yakobus 1:5\n\nTag temanmu yang lagi dikejar deadline 👇"},
    # 4 - Rabu 7 Okt
    {"teks": "Tuhan, aku masih menunggu kabar itu. Jaga hatiku tetap tenang selama menunggu, ya.",
     "foto": "kabut",
     "caption": "Untuk kamu yang sedang menunggu kabar ⏳\n\nMenunggu itu melelahkan. Tapi menunggu bersama Tuhan berbeda: kamu menunggu sambil berpegang pada firman-Nya.\n\n📖 “Aku menanti-nantikan TUHAN, jiwaku menanti-nanti, dan aku mengharapkan firman-Nya.” — Mazmur 130:5\n\nKetik “aku menunggu” dan kita saling mendoakan 🙏"},
    # 5 - Kamis 8 Okt
    {"teks": "Tuhan, hari ini ada satu hal kecil yang berhasil. Terima kasih, aku tahu itu dari-Mu.",
     "foto": "pohon",
     "caption": "Kemenangan kecil juga layak disyukuri 🌱\n\nPresentasi yang lancar, ojol yang cepat datang, tugas yang akhirnya selesai. Semua pemberian yang baik datang dari Dia.\n\n📖 “Setiap pemberian yang baik dan setiap anugerah yang sempurna, datangnya dari atas, diturunkan dari Bapa segala terang…” — Yakobus 1:17\n\nTulis satu kemenangan kecilmu hari ini di komentar 👇"},
    # 6 - Jumat 9 Okt
    {"teks": "Tuhan, akhirnya Jumat sore. Terima kasih sudah menemaniku dari Senin sampai detik ini.",
     "foto": "laut",
     "caption": "Akhirnya Jumat sore 🌅\n\nDari Senin pagi sampai matahari terbenam hari ini, Dia setia. Itu alasan yang cukup untuk memuji-Nya.\n\n📖 “Dari terbitnya sampai kepada terbenamnya matahari terpujilah nama TUHAN.” — Mazmur 113:3\n\nKetik “terima kasih, Tuhan” untuk minggu ini 🙏"},
    # 7 - Sabtu 10 Okt
    {"teks": "Tuhan, Sabtu ini habis buat cucian. Terima kasih masih punya rumah untuk dibereskan.",
     "foto": "jendela",
     "caption": "Rumah yang berantakan juga tanda ada yang tinggal di dalamnya 🧺\n\nCucian, piring, lantai: pekerjaan kecil yang bisa jadi ucapan syukur kalau dilakukan bersama Tuhan.\n\n📖 “Dan segala sesuatu yang kamu lakukan dengan perkataan atau perbuatan, lakukanlah semuanya itu dalam nama Tuhan Yesus, sambil mengucap syukur oleh Dia kepada Allah, Bapa kita.” — Kolose 3:17\n\nKetik 🧺 kalau Sabtumu juga begini."},
    # 8 - Minggu 11 Okt
    {"teks": "Tuhan, aku masih canggung di gereja yang baru. Tolong kirimkan satu teman, ya.",
     "foto": "panggung",
     "caption": "Untuk kamu yang masih baru di gereja 🤍\n\nBelum kenal siapa-siapa itu wajar. Tapi kamu tidak sendirian di sana: Dia ada di tengah-tengah umat-Nya yang berkumpul.\n\n📖 “Sebab di mana dua atau tiga orang berkumpul dalam Nama-Ku, di situ Aku ada di tengah-tengah mereka.” — Matius 18:20\n\nKirim ke teman yang baru pindah gereja atau merantau, ajak dia duduk bareng Minggu depan 💌"},
    # 9 - Senin 12 Okt
    {"teks": "Tuhan, kerjaku dikritik habis hari ini. Tolong pulihkan hatiku sebelum besok pagi.",
     "foto": "gunung",
     "caption": "Untuk hari kamu dikritik habis-habisan ⛰️\n\nKritik bisa membuat goyah. Tapi nilaimu tidak ditentukan oleh satu rapat yang buruk. Pandanglah kepada Dia yang berdiri di sebelahmu.\n\n📖 “Aku senantiasa memandang kepada TUHAN; karena Ia berdiri di sebelah kananku, aku tidak goyah.” — Mazmur 16:8\n\nSave untuk hari kerjamu terasa tidak dihargai 🔖"},
    # 10 - Selasa 13 Okt
    {"teks": "Tuhan, di kereta yang penuh sesak ini aku cuma bisa doa pendek: kuatkan aku sampai rumah.",
     "foto": "jalan",
     "caption": "Doa pendek di kereta yang penuh 🚆\n\nPagi, siang, petang, bahkan saat kamu cemas sampai menangis di perjalanan pulang, Dia mendengar suaramu.\n\n📖 “Di waktu petang, pagi dan tengah hari aku cemas dan menangis; dan Ia mendengar suaraku.” — Mazmur 55:18\n\nKetik “sampai rumah” kalau kamu masih di perjalanan pulang 🙏"},
    # 11 - Rabu 14 Okt
    {"teks": "Tuhan, lamaranku belum ada yang dibalas. Aku capek, tapi aku belum mau berhenti percaya.",
     "foto": "awan",
     "caption": "Untuk kamu yang lamarannya belum dibalas 📩\n\nTidak ada janji kapan atau di mana. Tapi ada janji bahwa Allahmu mendengar, dan kamu tidak menunggu sendirian.\n\n📖 “Tetapi aku ini akan menunggu-nunggu TUHAN, akan mengharapkan Allah yang menyelamatkan aku; Allahku akan mendengarkan aku!” — Mikha 7:7\n\nKirim ke temanmu yang sedang mencari kerja 💌"},
    # 12 - Kamis 15 Okt
    {"teks": "Tuhan, hari ini aku cuma makan nasi telur, tapi rasanya enak sekali. Terima kasih, ya.",
     "foto": "jendela",
     "caption": "Nasi telur dan hati yang bersyukur 🍳\n\nKebaikan Tuhan sering hadir di hal yang paling sederhana. Hari ini, kecap dan lihat saja.\n\n📖 “Kecaplah dan lihatlah, betapa baiknya TUHAN itu! Berbahagialah orang yang berlindung pada-Nya!” — Mazmur 34:9\n\nMakan apa kamu hari ini? Tulis di komentar 👇"},
    # 13 - Jumat 16 Okt
    {"teks": "Tuhan, aku pulang dengan sisa sabar. Biar keluargaku dapat yang terbaik, bukan sisanya.",
     "foto": "lilin",
     "caption": "Untuk kamu yang pulang dengan sisa sabar 🏠\n\nOrang-orang di rumah sering kebagian versi kita yang paling capek. Minta Tuhan menambahkan kasih-Nya sebelum membuka pintu.\n\n📖 “Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia tidak memegahkan diri dan tidak sombong.” — 1 Korintus 13:4\n\nKetik “Amin” sebelum kamu masuk rumah sore ini."},
    # 14 - Sabtu 17 Okt
    {"teks": "Tuhan, temanku sedang berjuang dan aku nggak tahu harus bilang apa. Pakai aku, ya.",
     "foto": "bintang",
     "caption": "Kadang kita tidak tahu harus bilang apa ✨\n\nTidak apa-apa. Hadir, mendengar, dan mendoakan sudah berarti banyak.\n\n📖 “Bertolong-tolonganlah menanggung bebanmu! Demikianlah kamu memenuhi hukum Kristus.” — Galatia 6:2\n\nKirim ke temanmu yang sedang berjuang, bilang kamu ada untuknya 💌"},
]


# hari 0-14 (Sabtu 3 Okt .. Sabtu 17 Okt 2026) -> {slot: (format, index)}
# hari 0: malam1 (MEME) + larut 22:30 (BUKU); hari 1-14: sore2 16:30 (MEME) + larut 22:30 (BUKU)
JADWAL = {0: {"malam1": ("MEME", 0), "larut": ("BUKU", 0)}}
JADWAL.update({d: {"sore2": ("MEME", d), "larut": ("BUKU", d)} for d in range(1, 15)})
