"""Akun Tenang (@diam.dan.percaya) - minggu 6 (Minggu 1 Nov - Sabtu 7 Nov 2026).
Tema: "Bersyukur dalam segala hal" (bersyukur di setiap musim) + hitung mundur Natal lanjut (54 -> 48 hari).
Hari: 1 Minggu (bulan baru, Hari Semua Orang Kudus), 2 Senin (syukur untuk hari biasa), 3 Selasa (syukur di musim sulit),
4 Rabu (syukur untuk orang-orang), 5 Kamis (bersyukur sambil menunggu), 6 Jumat (mengingat kebaikan-Nya),
7 Sabtu (rasa cukup, persiapan ibadah Minggu).
12 slot per hari, setiap slot gaya visual berbeda:
  LAYAR   = layar kunci HP dengan satu notifikasi (pengirim: Alkitab / Pengingat / Doa pagi).   pagi 06:00
  ALKITAB = foto halaman Alkitab terbuka, satu ayat distabilo + catatan tangan kecil.         pagi3 07:30
  ELI     = komik Eli yang sudah jadi (hari 1, 4, 7) / RETRO = poster gradasi retro berbintik.  pagi2 09:00
  A       = carousel editorial (skema POSTS di konten/tenang.py).                              siang0 10:30
  POSTER  = foto lanskap + huruf kapital besar dengan satu kata miring.                         siang 12:00
  D       = dinding teks (skema DINDING di konten/tenang.py).                                   siang2 13:30
  HITUNG  = hitung mundur Natal.                                                                sore 15:00
  MINIMAL = layar hitam, satu kalimat kecil di tengah.                                          sore2 16:30
  C       = teks di warna tegas (skema WARNA di konten/tenang.py).                              petang 18:00
  R       = Reels suasana kabut/bintang (skema SUASANA di konten/tenang.py).                    malam0 19:30
  LED     = papan LED titik-titik.                                                              malam 21:00
  DOA     = kartu doa larut malam, [kalimat] = merah.                                           larut 22:30
Kutipan ayat: Alkitab TB. Caption tanpa hashtag."""

# ---------- LAYAR: layar kunci HP (pagi 06:00) ----------
LAYAR = [
    {"jam": "06:00", "hari": "Minggu, 1 November", "pengirim": "Alkitab",
     "pesan": "Engkau memahkotai tahun dengan kebaikan-Mu.", "ref": "Mazmur 65:12", "foto": "fajar",
     "caption": "Selamat pagi, November 🌅\n\nDua bulan terakhir tahun ini dimulai hari ini. Sebelum menghitung apa yang belum tercapai, hitung dulu kebaikan-Nya yang sudah menemanimu sepanjang tahun.\n\n📖 “Engkau memahkotai tahun dengan kebaikan-Mu…” — Mazmur 65:12\n\nKetik “Amin” kalau kamu mau memulai bulan ini dengan syukur."},
    {"jam": "06:00", "hari": "Senin, 2 November", "pengirim": "Pengingat",
     "pesan": "Sebelum buka email: sebut tiga hal yang kamu syukuri pagi ini. Pelan-pelan saja.", "ref": "Mazmur 119:164", "foto": "kabut",
     "caption": "Pengingat kecil sebelum Senin dimulai ⏰\n\nPemazmur memuji Tuhan berkali-kali dalam sehari. Kita bisa mulai dari satu kali: pagi ini, sebelum layar kerja menyala.\n\n📖 “Tujuh kali dalam sehari aku memuji-muji Engkau, karena hukum-hukum-Mu yang adil.” — Mazmur 119:164\n\nTulis tiga hal yang kamu syukuri pagi ini di komentar 👇"},
    {"jam": "06:00", "hari": "Selasa, 3 November", "pengirim": "Doa pagi",
     "pesan": "Tuhan, aku belum tahu hari ini akan seperti apa. Tapi aku mau tetap menyebut-Mu baik.", "ref": "", "foto": "bintang",
     "caption": "Doa pagi untuk hari yang terasa berat 🤍\n\nDaud menulis mazmur ini saat bersembunyi di gua, dikejar orang yang ingin mencelakainya. Tapi hatinya tetap memilih untuk memuji.\n\n📖 “Hatiku siap, ya Allah, hatiku siap; aku mau menyanyi, aku mau bermazmur.” — Mazmur 57:8\n\nKetik “Hatiku siap” kalau kamu mau memulai hari dengan memuji."},
    {"jam": "06:00", "hari": "Rabu, 4 November", "pengirim": "Pengingat",
     "pesan": "Siapa yang menolongmu tahun ini? Kirim satu pesan terima kasih untuknya hari ini.", "ref": "Amsal 27:17", "foto": "fajar",
     "caption": "Pengingat hari Rabu 💌\n\nAda orang-orang yang Tuhan pakai untuk menajamkan, menguatkan, dan menemani kita. Mereka layak tahu bahwa mereka berarti.\n\n📖 “Besi menajamkan besi, orang menajamkan sesamanya.” — Amsal 27:17\n\nTag orang itu di komentar, lalu kirim pesan terima kasihmu 🤍"},
    {"jam": "06:00", "hari": "Kamis, 5 November", "pengirim": "Alkitab",
     "pesan": "Sesungguhnya, aku percaya akan melihat kebaikan TUHAN di negeri orang-orang yang hidup!", "ref": "Mazmur 27:13", "foto": "laut",
     "caption": "Pagi ini, untuk kamu yang masih menunggu 🌊\n\nDaud tidak hanya berharap melihat kebaikan Tuhan suatu hari nanti. Ia percaya akan melihatnya di sini, di negeri orang-orang yang hidup.\n\n📖 “Sesungguhnya, aku percaya akan melihat kebaikan TUHAN di negeri orang-orang yang hidup!” — Mazmur 27:13\n\nSave untuk hari-hari menunggu 🔖"},
    {"jam": "06:00", "hari": "Jumat, 6 November", "pengirim": "Pengingat",
     "pesan": "Sebelum akhir pekan: ingat satu doa yang sudah Tuhan jawab tahun ini. Lalu ucapkan syukur.", "ref": "Mazmur 126:3", "foto": "fajar",
     "caption": "Jumat pagi, waktunya mengingat 🌅\n\nKita cepat sekali mencatat doa yang belum dijawab, tapi sering lupa merayakan yang sudah. Pagi ini, ingat satu saja.\n\n📖 “TUHAN telah melakukan perkara besar kepada kita, maka kita bersukacita.” — Mazmur 126:3\n\nCeritakan satu doa yang sudah dijawab-Nya tahun ini di komentar 👇"},
    {"jam": "06:00", "hari": "Sabtu, 7 November", "pengirim": "Doa pagi",
     "pesan": "Tuhan, hari ini aku tidak minta lebih. Ajar aku melihat bahwa yang ada sudah cukup.", "ref": "", "foto": "kabut",
     "caption": "Doa Sabtu pagi yang sederhana ☕\n\nAgur bin Yake meminta sesuatu yang jarang kita minta: bukan kekayaan, bukan kemiskinan, tapi cukup.\n\n📖 “…Jangan berikan kepadaku kemiskinan atau kekayaan. Biarkanlah aku menikmati makanan yang menjadi bagianku.” — Amsal 30:8\n\nKetik “Cukup” sebagai doamu Sabtu ini."},
]

# ---------- ALKITAB: halaman Alkitab terbuka, satu ayat distabilo (pagi3 07:30) ----------
ALKITAB = [
    {"ref": "Kolose 1:12", "warna": "kuning", "catatan": "kita juga diundang",
     "caption": "Tanggal 1 November dikenal sebagai Hari Semua Orang Kudus 🕯️\n\nOrang kudus dalam Alkitab bukan orang yang sempurna, tapi orang yang dilayakkan oleh Bapa. Termasuk mereka yang sudah lebih dulu pulang, dan juga kamu.\n\n📖 “dan mengucap syukur dengan sukacita kepada Bapa, yang melayakkan kamu untuk mendapat bagian dalam apa yang ditentukan untuk orang-orang kudus di dalam kerajaan terang.” — Kolose 1:12\n\nKetik “Amin” kalau kamu bersyukur sudah dilayakkan-Nya."},
    {"ref": "Matius 6:11", "warna": "hijau", "catatan": "cukup untuk hari ini",
     "caption": "Doa yang diajarkan Yesus tidak meminta stok untuk setahun 🍞\n\nCukup untuk hari ini. Dan setiap hari, Bapa setia memberikannya lagi. Senin ini, syukuri roti untuk hari ini.\n\n📖 “Berikanlah kami pada hari ini makanan kami yang secukupnya” — Matius 6:11\n\nSave dan doakan pelan-pelan sebelum sarapan 🔖"},
    {"ref": "Habakuk 3:17", "warna": "kuning", "catatan": "kata kuncinya: namun",
     "caption": "Ayat tentang panen yang gagal 🍂\n\nHabakuk menulis daftar yang menyakitkan: pohon tidak berbuah, ladang kosong, kandang sepi. Lalu ayat berikutnya dimulai dengan satu kata yang mengubah semuanya: namun.\n\n📖 “Sekalipun pohon ara tidak berbunga, pohon anggur tidak berbuah, hasil pohon zaitun mengecewakan, sekalipun ladang-ladang tidak menghasilkan bahan makanan, kambing domba terhalau dari kurungan, dan tidak ada lembu sapi dalam kandang,” — Habakuk 3:17\n\nKalau musimmu sedang kosong, ketik “namun” sebagai imanmu hari ini 🤍"},
    {"ref": "Filemon 1:4", "warna": "pink", "catatan": "siapa yang kamu ingat?",
     "caption": "Surat pendek dari Paulus untuk seorang sahabat 💌\n\nSurat Filemon cuma satu pasal, tapi dibuka dengan ucapan syukur untuk satu orang. Paulus bersyukur kepada Allah setiap kali mengingat sahabatnya.\n\n📖 “Aku mengucap syukur kepada Allahku, setiap kali aku mengingat engkau dalam doaku,” — Filemon 1:4\n\nSiapa yang kamu ingat waktu membaca ayat ini? Tag dia 👇"},
    {"ref": "Yohanes 11:41", "warna": "kuning", "catatan": "bersyukur duluan",
     "caption": "Yesus bersyukur sebelum kubur itu kosong 🪨\n\nBatu baru saja diangkat. Lazarus belum keluar. Tapi Yesus sudah mengucap syukur kepada Bapa, karena Ia tahu Bapa mendengar-Nya.\n\n📖 “Maka mereka mengangkat batu itu. Lalu Yesus menengadah ke atas dan berkata: ‘Bapa, Aku mengucap syukur kepada-Mu, karena Engkau telah mendengarkan Aku.’” — Yohanes 11:41\n\nKetik “Engkau mendengar” kalau kamu mau belajar bersyukur lebih dulu."},
    {"ref": "Mazmur 77:12", "warna": "hijau", "catatan": "ingat lagi, ya",
     "caption": "Mazmur 77 dimulai dengan malam yang tidak bisa tidur 🌙\n\nAsaf berseru, gelisah, dan bertanya apakah Tuhan sudah lupa. Lalu di tengah mazmur, arahnya berubah: ia memilih untuk mengingat.\n\n📖 “Aku hendak mengingat perbuatan-perbuatan TUHAN, ya, aku hendak mengingat keajaiban-keajaiban-Mu dari zaman purbakala.” — Mazmur 77:12\n\nTulis satu perbuatan Tuhan yang kamu ingat minggu ini 👇"},
    {"ref": "Filipi 4:11", "warna": "pink", "catatan": "belajar, pelan-pelan",
     "caption": "Rasa cukup itu dipelajari, bukan langsung jadi 📚\n\nPaulus menulis ini dari penjara. Ia tidak bilang rasa cukup datang dengan sendirinya. Ia bilang: aku telah belajar.\n\n📖 “Kukatakan ini bukanlah karena kekurangan, sebab aku telah belajar mencukupkan diri dalam segala keadaan.” — Filipi 4:11\n\nKirim ke teman yang mau belajar bareng pelan-pelan 💌"},
]

# ---------- RETRO: poster gradasi retro berbintik (pagi2 hari 2, 3, 5, 6) ----------
RETRO = [
    {"atas": "SENIN · 2 NOVEMBER", "judul": "HARI BIASA, KASIH SETIA",
     "bawah": "roti di meja juga tanda kasih setia-Nya", "ref": "Mazmur 136:25",
     "caption": "Hari biasa juga punya alasan untuk bersyukur 🍞\n\nMazmur 136 mengulang satu kalimat sampai 26 kali: untuk selama-lamanya kasih setia-Nya. Di antara karya-karya besar Tuhan, ada juga hal yang sederhana: roti untuk hari ini.\n\n📖 “Dia yang memberikan roti kepada segala makhluk; bahwasanya untuk selama-lamanya kasih setia-Nya.” — Mazmur 136:25\n\nKetik 🍞 sebagai ucapan terima kasihmu untuk sarapan pagi ini."},
    {"atas": "KISAH 16 · TENGAH MALAM", "judul": "MENYANYI DI DALAM PENJARA",
     "bawah": "syukur yang tidak menunggu pintu terbuka", "ref": "Kisah Para Rasul 16:25",
     "caption": "Kaki dipasung, punggung masih perih 🎶\n\nPaulus dan Silas baru saja didera lalu dimasukkan ke ruang penjara yang paling dalam. Tapi tengah malam, yang terdengar dari sel mereka justru doa dan pujian.\n\n📖 “Tetapi kira-kira tengah malam Paulus dan Silas berdoa dan menyanyikan puji-pujian kepada Allah dan orang-orang hukuman lain mendengarkan mereka.” — Kisah Para Rasul 16:25\n\nKetik 🎶 kalau kamu mau tetap memuji di musim yang sulit."},
    {"atas": "KAMIS, 5 NOVEMBER", "judul": "MEMUJI SAMBIL MENUNGGU",
     "bawah": "doa belum dijawab? pujian jalan terus", "ref": "Mazmur 71:14",
     "caption": "Menunggu tidak harus diam saja 📻\n\nPemazmur ini sudah tua dan masih menantikan pertolongan Tuhan. Tapi ia tidak berhenti berharap. Ia malah menambah pujiannya.\n\n📖 “Tetapi aku senantiasa mau berharap dan menambah puji-pujian kepada-Mu;” — Mazmur 71:14\n\nKetik “Tetap memuji” kalau kamu juga sedang menunggu."},
    {"atas": "CATATAN DARI PADANG GURUN", "judul": "40 TAHUN DIPELIHARA",
     "bawah": "lihat ke belakang, Dia selalu hadir", "ref": "Ulangan 8:4",
     "caption": "Empat puluh tahun di padang gurun 🏜️\n\nSebelum masuk ke negeri yang baru, Musa mengajak Israel menengok ke belakang. Bukan hanya untuk mengenang susahnya, tapi untuk melihat bahwa Tuhan memelihara mereka setiap hari.\n\n📖 “Pakaianmu tidaklah menjadi buruk di tubuhmu dan kakimu tidaklah menjadi bengkak selama empat puluh tahun ini.” — Ulangan 8:4\n\nCoba tengok ke belakang: di bagian mana Tuhan memeliharamu tahun ini? Ceritakan di komentar 👇"},
]

# ---------- A: carousel editorial (siang0 10:30), skema POSTS di konten/tenang.py ----------
POSTS = [
    {
        "warna": "coklat",
        "hook": "Mulai dengan terima kasih.",
        "masalah": ["Bulan baru,", "rencana baru,", "kekhawatiran yang masih sama?", "", "Sebelum meminta apa-apa,", "bilang terima kasih dulu."],
        "ayat": "“Ucaplah syukur senantiasa atas segala sesuatu dalam nama Tuhan kita Yesus Kristus kepada Allah dan Bapa kita”",
        "ref": "Efesus 5:20",
        "refleksi": ["Senantiasa, bukan sesekali.", "Atas segala sesuatu,", "bukan hanya yang enak.", "", "Minggu ini kita belajar bersama."],
        "cta": ["Ikuti seri syukur", "minggu ini bersama kami."],
        "caption": "Minggu ini kita belajar satu hal: bersyukur dalam segala hal 🍂\n\nBukan pura-pura semua baik. Bukan juga menunggu semuanya beres. Tapi belajar melihat tangan Tuhan di setiap musim, yang cerah maupun yang mendung.\n\n📖 Efesus 5:20\n\nKetik “Aku ikut” kalau kamu mau belajar bersama minggu ini 🤍",
    },
    {
        "warna": "krem",
        "hook": "Hari biasa juga hadiah.",
        "masalah": ["Bangun, kerja, makan, tidur.", "Diulang lagi besok.", "", "Rasanya tidak ada", "yang layak disyukuri?"],
        "ayat": "“Betapa banyak perbuatan-Mu, ya TUHAN, sekaliannya Kaujadikan dengan kebijaksanaan, bumi penuh dengan ciptaan-Mu.”",
        "ref": "Mazmur 104:24",
        "refleksi": ["Hari biasa penuh", "jejak tangan-Nya.", "", "Kita saja yang terlalu cepat", "melewatinya."],
        "cta": ["Simpan ini untuk Senin", "yang terasa datar."],
        "caption": "Hari biasa juga hadiah 🎁\n\nMazmur 104 memuji Tuhan untuk hal-hal yang sering kita anggap biasa: mata air, rumput, roti, matahari terbit dan terbenam. Semuanya dibuat dengan bijaksana.\n\n📖 Mazmur 104:24\n\nHal biasa apa yang kamu syukuri hari ini? Ceritakan di komentar 👇",
    },
    {
        "warna": "hitam",
        "hook": "Bersyukur tidak sama dengan menyangkal.",
        "masalah": ["“Bersyukur saja, jangan sedih.”", "", "Pernah dengar itu", "saat hatimu sedang patah?"],
        "ayat": "“Mengapa engkau tertekan, hai jiwaku, dan gelisah di dalam diriku? Berharaplah kepada Allah! Sebab aku akan bersyukur lagi kepada-Nya, penolongku dan Allahku!”",
        "ref": "Mazmur 42:6",
        "refleksi": ["Pemazmur jujur soal sedihnya,", "lalu memilih berharap.", "", "Air mata dan syukur", "boleh ada di doa yang sama."],
        "cta": ["Kirim ini ke seseorang", "yang sedang di musim sulit."],
        "caption": "Bersyukur tidak sama dengan menyangkal rasa sakit 🤍\n\nPemazmur tidak menyangkal bahwa jiwanya tertekan. Ia mengakuinya, lalu berbicara kepada dirinya sendiri: berharaplah kepada Allah, aku akan bersyukur lagi.\n\n📖 Mazmur 42:6\n\nSave untuk hari kamu butuh izin untuk jujur 🔖",
    },
    {
        "warna": "hijau",
        "hook": "Kamu tidak sampai di sini sendirian.",
        "masalah": ["Ada yang mendoakanmu", "tanpa kamu tahu.", "", "Ada yang membukakan pintu", "waktu semua jalan tertutup."],
        "ayat": "“Aku senantiasa mengucap syukur kepada Allahku karena kamu atas kasih karunia Allah yang dianugerahkan-Nya kepada kamu dalam Kristus Yesus.”",
        "ref": "1 Korintus 1:4",
        "refleksi": ["Setiap orang baik di hidupmu", "adalah kasih karunia", "yang punya wajah."],
        "cta": ["Tag satu orang", "yang kamu syukuri hari ini."],
        "caption": "Kamu tidak sampai di sini sendirian 🤝\n\nPaulus menulis kepada jemaat Korintus yang penuh masalah. Tapi suratnya tetap dibuka dengan ucapan syukur karena mereka, sebab ia melihat kasih karunia Allah bekerja di dalam orang-orang itu.\n\n📖 1 Korintus 1:4\n\nTag satu orang yang kamu syukuri hari ini, dan bilang kenapa 👇",
    },
    {
        "warna": "coklat",
        "hook": "Bersyukur sebelum ada jawaban.",
        "masalah": ["Masih menunggu hasil tes?", "Kabar lamaran kerja?", "Doa yang itu-itu juga?", "", "Rasanya belum ada", "yang bisa disyukuri."],
        "ayat": "“Pada hari aku berseru, Engkaupun menjawab aku, Engkau menambahkan kekuatan dalam jiwaku.”",
        "ref": "Mazmur 138:3",
        "refleksi": ["Kadang jawaban pertama-Nya", "bukan keadaan yang berubah,", "", "tapi kekuatan baru", "untuk bertahan hari ini."],
        "cta": ["Kirim ini ke teman", "yang masih menunggu kabar."],
        "caption": "Bersyukur sebelum ada jawaban 🤍\n\nBersyukur saat menunggu bukan berarti kita sudah tahu hasil akhirnya. Kita bersyukur karena Dia mendengar, dan karena Dia menguatkan kita selama menunggu.\n\n📖 Mazmur 138:3\n\nKetik “Dia dengar” kalau kamu sedang menunggu kabar 🙏",
    },
    {
        "warna": "krem",
        "hook": "Coba hitung lagi.",
        "masalah": ["Masalah yang dulu bikin", "kamu tidak bisa tidur?", "", "Sekarang sudah lewat.", "Siapa yang menolongmu?"],
        "ayat": "“Banyaklah yang telah Kaulakukan, ya TUHAN, Allahku, perbuatan-Mu yang ajaib dan maksud-Mu untuk kami… terlalu besar jumlahnya untuk dihitung.”",
        "ref": "Mazmur 40:6",
        "refleksi": ["Kalau hari ini sulit bersyukur,", "", "ingat lagi apa yang sudah", "Dia lakukan kemarin."],
        "cta": ["Tulis satu kebaikan-Nya", "di kolom komentar."],
        "caption": "Coba hitung lagi kebaikan-Nya 🍂\n\nDaud mencoba menghitung perbuatan Tuhan dalam hidupnya, lalu menyerah: terlalu banyak. Kita juga sering lupa betapa panjang daftarnya, sampai kita mulai menulis.\n\n📖 Mazmur 40:6\n\nTulis satu kebaikan Tuhan tahun ini di komentar 👇",
    },
    {
        "warna": "hitam",
        "hook": "Cukup.",
        "masalah": ["Layar penuh orang", "yang punya lebih banyak.", "", "Lalu yang ada di tanganmu", "tiba-tiba terasa kurang."],
        "ayat": "“Memang ibadah itu kalau disertai rasa cukup, memberi keuntungan besar.”",
        "ref": "1 Timotius 6:6",
        "refleksi": ["Rasa cukup bukan berhenti bermimpi.", "", "Rasa cukup adalah berhenti", "meragukan kebaikan Tuhan."],
        "cta": ["Follow @{handle}", "dan belajar cukup bersama."],
        "caption": "Cukup. Satu kata yang jarang kita ucapkan 🤍\n\nPaulus menulis kepada Timotius: keuntungan terbesar bukan punya lebih banyak, tapi hidup dekat Tuhan dengan hati yang merasa cukup.\n\n📖 1 Timotius 6:6\n\nSelamat menikmati Sabtu. Follow @{handle} supaya pengingat seperti ini muncul di berandamu setiap hari.",
    },
]

# ---------- POSTER: foto lanskap + huruf kapital besar, satu kata miring (siang 12:00) ----------
POSTER = [
    {"baris1": "SETIAP MUSIM", "miring": "tetap", "baris2": "PUNYA SYUKURNYA.",
     "ayat_kecil": "…takkan berhenti-henti musim menabur dan menuai, dingin dan panas…", "ref": "Kejadian 8:22", "foto": "fajar",
     "caption": "Setiap musim tetap punya alasan untuk bersyukur 🍂\n\nSetelah air bah, Tuhan berfirman bahwa musim akan terus berganti selama bumi masih ada. Menabur dan menuai, dingin dan panas. Musimnya berganti, kesetiaan-Nya tidak.\n\n📖 “Selama bumi masih ada, takkan berhenti-henti musim menabur dan menuai, dingin dan panas, kemarau dan hujan, siang dan malam.” — Kejadian 8:22\n\nKamu sedang di musim apa sekarang? Tulis satu kata di komentar 👇"},
    {"baris1": "BERKAT KECIL", "miring": "juga", "baris2": "BERKAT.",
     "ayat_kecil": "…jiwa yang lapar dikenyangkan-Nya dengan kebaikan.", "ref": "Mazmur 107:9", "foto": "laut",
     "caption": "Berkat kecil juga berkat 🤍\n\nNasi hangat, air bersih, kursi untuk duduk sebentar. Kita sering menunggu berkat yang besar sampai lupa bahwa hari ini pun kita sudah dikenyangkan dengan kebaikan-Nya.\n\n📖 “sebab dipuaskan-Nya jiwa yang dahaga, dan jiwa yang lapar dikenyangkan-Nya dengan kebaikan.” — Mazmur 107:9\n\nSebutkan satu berkat kecil hari ini di komentar 👇"},
    {"baris1": "DIA TETAP", "miring": "baik", "baris2": "DI MUSIM INI.",
     "ayat_kecil": "…tetapi Engkau telah mengeluarkan kami sehingga bebas.", "ref": "Mazmur 66:12", "foto": "bintang",
     "caption": "Api dan air, tapi tidak ditinggalkan 🌌\n\nMazmur 66 tidak berpura-pura jalannya mudah. Mereka melewati api dan air. Tapi pujiannya lahir dari kesaksian: Tuhan membawa mereka keluar.\n\n📖 “…kami telah menempuh api dan air; tetapi Engkau telah mengeluarkan kami sehingga bebas.” — Mazmur 66:12\n\nKetik “Dia tetap baik” kalau kamu sedang melewati musim yang berat."},
    {"baris1": "TUHAN MENGIRIM", "miring": "mereka", "baris2": "TEPAT WAKTU.",
     "ayat_kecil": "Kami selalu mengucap syukur kepada Allah karena kamu semua", "ref": "1 Tesalonika 1:2", "foto": "fajar",
     "caption": "Orang-orang yang datang di waktu yang tepat 🤍\n\nTeman yang menelepon saat kamu hampir menyerah. Kakak rohani yang mengajakmu kembali ke gereja. Mereka bukan kebetulan.\n\n📖 “Kami selalu mengucap syukur kepada Allah karena kamu semua dan menyebut kamu dalam doa kami.” — 1 Tesalonika 1:2\n\nTag seseorang yang Tuhan kirim tepat waktu ke hidupmu 👇"},
    {"baris1": "YANG TAK", "miring": "kelihatan", "baris2": "ITU KEKAL.",
     "ayat_kecil": "…tidak memperhatikan yang kelihatan, melainkan yang tak kelihatan…", "ref": "2 Korintus 4:18", "foto": "kabut",
     "caption": "Mata yang belajar melihat lebih jauh 🌫️\n\nPaulus menulis ini di tengah tekanan dan penderitaan. Ia belajar mengarahkan mata ke hal yang tidak kelihatan: Allah yang terus bekerja.\n\n📖 “Sebab kami tidak memperhatikan yang kelihatan, melainkan yang tak kelihatan, karena yang kelihatan adalah sementara, sedangkan yang tak kelihatan adalah kekal.” — 2 Korintus 4:18\n\nKirim ke temanmu yang lelah menunggu sesuatu terlihat 💌"},
    {"baris1": "KEBAIKAN-NYA", "miring": "tak", "baris2": "TERBALASKAN.",
     "ayat_kecil": "Bagaimana akan kubalas kepada TUHAN segala kebajikan-Nya kepadaku?", "ref": "Mazmur 116:12", "foto": "laut",
     "caption": "Kebaikan yang tidak bisa dibalas 🙏\n\nSejak kecil kita diajari untuk bilang terima kasih kepada orang lain. Tapi kadang kita lupa mengucapkannya kepada Tuhan, padahal kebaikan-Nya tidak akan pernah bisa kita balas.\n\n📖 “Bagaimana akan kubalas kepada TUHAN segala kebajikan-Nya kepadaku?” — Mazmur 116:12\n\nKetik “Terima kasih, Tuhan” di komentar sebagai doamu siang ini."},
    {"baris1": "ENGKAULAH", "miring": "satu-satunya", "baris2": "KEBAIKANKU.",
     "ayat_kecil": "Engkaulah Tuhanku, tidak ada yang baik bagiku selain Engkau!", "ref": "Mazmur 16:2", "foto": "kabut",
     "caption": "Kalau semuanya diambil, apa yang tersisa? 🤍\n\nDaud menemukan jawabannya: Tuhan sendiri. Berkat-berkat-Nya baik, tapi yang paling baik adalah Dia.\n\n📖 “Aku berkata kepada TUHAN: ‘Engkaulah Tuhanku, tidak ada yang baik bagiku selain Engkau!’” — Mazmur 16:2\n\nKetik “Engkau cukup” kalau ini doamu hari ini."},
]

# ---------- D: dinding teks (siang2 13:30), skema DINDING di konten/tenang.py ----------
DINDING = [
    {"bg": "#2F5E45", "teks": "#43795C", "kalimat": "MULAI BULAN INI DENGAN UCAPAN SYUKUR",
     "sorot": ["MULAI", "DENGAN", "SYUKUR"],
     "caption": "Temukan pesannya 👀\n\nMulai dengan syukur. Bukan karena semuanya sudah beres, tapi karena Tuhan sudah setia sampai hari pertama bulan ini.\n\n📖 “Aku hendak memuji TUHAN pada segala waktu; puji-pujian kepada-Nya tetap di dalam mulutku.” — Mazmur 34:2\n\nKetik “SYUKUR” kalau kamu menemukan pesannya 🤍"},
    {"bg": "#E9D8C4", "teks": "#D2BFA8", "kalimat": "SYUKURI YANG ADA DI DEPANMU HARI INI",
     "sorot": ["SYUKURI", "YANG", "ADA", "HARI", "INI"],
     "caption": "Temukan pesannya 👀\n\nSyukuri yang ada hari ini: makanan di meja, pekerjaan di depan mata, orang-orang di sekitarmu. Semuanya pemberian Allah yang baik.\n\n📖 “Karena semua yang diciptakan Allah itu baik… jika diterima dengan ucapan syukur,” — 1 Timotius 4:4\n\nSave sebagai pengingat di jam makan siang 🔖"},
    {"bg": "#141414", "teks": "#383838", "kalimat": "BAHKAN HARI INI MASIH ADA ALASAN UNTUK BERSYUKUR",
     "sorot": ["MASIH", "ADA", "ALASAN", "BERSYUKUR"],
     "caption": "Temukan pesannya 👀\n\nMasih ada alasan bersyukur, bahkan di hari yang berat. Mungkin bukan untuk keadaannya, tapi untuk Tuhan yang tetap menemanimu di dalamnya.\n\n📖 “Aku yang meratap telah Kauubah menjadi orang yang menari-nari, kain kabungku telah Kaubuka, pinggangku Kauikat dengan sukacita,” — Mazmur 30:12\n\nKirim ke seseorang yang sedang butuh alasan untuk bertahan 💌"},
    {"bg": "#8C2F39", "teks": "#A34450", "kalimat": "TERIMA KASIH SUDAH ADA DI SINI UNTUKKU",
     "sorot": ["TERIMA", "KASIH", "SUDAH", "ADA"],
     "caption": "Temukan pesannya 👀\n\nTerima kasih sudah ada. Kalimat sederhana yang mungkin sedang ditunggu seseorang. Hari ini, ucapkan itu kepada teman yang tetap tinggal.\n\n📖 “Karena kalau mereka jatuh, yang seorang mengangkat temannya…” — Pengkhotbah 4:10\n\nTag teman yang selalu mengangkatmu saat jatuh 👇"},
    {"bg": "#1F3A5F", "teks": "#34578A", "kalimat": "SELAMA MENUNGGU DIA TETAP MENEMANI KAMU",
     "sorot": ["SELAMA", "MENUNGGU", "DIA", "MENEMANI"],
     "caption": "Temukan pesannya 👀\n\nSelama menunggu, Dia menemani. Menunggu memang tidak nyaman, tapi kamu tidak menunggu sendirian.\n\n📖 “‘TUHAN adalah bagianku,’ kata jiwaku, oleh sebab itu aku berharap kepada-Nya.” — Ratapan 3:24\n\nKetik “DIA MENEMANI” kalau kamu sedang menunggu 🤍"},
    {"bg": "#C62F2F", "teks": "#7E1414", "kalimat": "INGAT LAGI SEMUA KEBAIKAN-NYA SAMPAI HARI INI",
     "sorot": ["INGAT", "SEMUA", "KEBAIKAN-NYA"],
     "caption": "Temukan pesannya 👀\n\nIngat semua kebaikan-Nya. Tuhan tahu kita mudah lupa, karena itu Ia memberi kita banyak cara untuk mengingat.\n\n📖 “Perbuatan-perbuatan-Nya yang ajaib dijadikan-Nya peringatan; TUHAN itu pengasih dan penyayang.” — Mazmur 111:4\n\nSave dan baca lagi setiap kali kamu lupa 🔖"},
    {"bg": "#B5651D", "teks": "#8E4E14", "kalimat": "SEDIKIT DENGAN TUHAN LEBIH BAIK DARI BANYAK TANPA DIA",
     "sorot": ["SEDIKIT", "DENGAN", "TUHAN", "LEBIH", "BAIK"],
     "caption": "Temukan pesannya 👀\n\nSedikit dengan Tuhan lebih baik. Amsal tidak meremehkan kebutuhan kita, tapi mengingatkan bahwa harta yang banyak tidak bisa membeli hati yang tenang.\n\n📖 “Lebih baik sedikit barang dengan disertai takut akan TUHAN dari pada banyak harta dengan disertai kecemasan.” — Amsal 15:16\n\nKirim ke temanmu yang sedang lelah mengejar lebih 💌"},
]

# ---------- HITUNG: hitung mundur Natal (sore 15:00), 54 hari (1 Nov) sampai 48 hari (7 Nov) ----------
HITUNG = [
    {"hari": 54, "teks": "Bulan Natal makin dekat. Siapkan hati dengan satu kebiasaan: bersyukur.",
     "caption": "54 hari lagi 🎄\n\nNatal adalah hadiah terbesar yang pernah diberikan Allah. Jadi cara terbaik menyiapkan hati untuk Natal adalah belajar bersyukur dari sekarang.\n\n📖 “Syukur kepada Allah karena karunia-Nya yang tak terkatakan itu!” — 2 Korintus 9:15\n\nKetik 🎁 kalau kamu mau menyambut Natal dengan hati yang bersyukur."},
    {"hari": 53, "teks": "Palungan itu sederhana. Tuhan tidak malu hadir di tempat yang biasa.",
     "caption": "53 hari lagi 🌾\n\nTidak ada tempat di penginapan, hanya palungan. Tapi justru di tempat sederhana itu Juruselamat dibaringkan. Hari biasamu pun bukan tempat yang terlalu sederhana bagi-Nya.\n\n📖 “dan ia melahirkan seorang anak laki-laki, anaknya yang sulung, lalu dibungkusnya dengan lampin dan dibaringkannya di dalam palungan, karena tidak ada tempat bagi mereka di rumah penginapan.” — Lukas 2:7\n\nKetik 🌾 kalau Senin ini kamu mau mengundang Dia ke hari biasamu."},
    {"hari": 52, "teks": "Terang Natal datang di tengah gelap. Gelapmu tidak terlalu pekat bagi-Nya.",
     "caption": "52 hari lagi ✨\n\nYesaya menulis nubuat ini untuk bangsa yang sedang di masa gelap. Ratusan tahun kemudian, Terang itu lahir di Betlehem.\n\n📖 “Bangsa yang berjalan di dalam kegelapan telah melihat terang yang besar; mereka yang diam di negeri kekelaman, atasnya terang telah bersinar.” — Yesaya 9:1\n\nKirim ke seseorang yang butuh sedikit terang hari ini 💌"},
    {"hari": 51, "teks": "Kabar baik paling indah dirayakan bersama. Siapa yang mau kamu ajak?",
     "caption": "51 hari lagi 🤝\n\nSaat Elisabet melahirkan Yohanes, tetangga dan sanak saudaranya ikut bersukacita. Sukacita dari Tuhan memang paling indah kalau dibagikan.\n\n📖 “Ketika tetangga-tetangganya serta sanak saudaranya mendengar, bahwa Tuhan telah menunjukkan rahmat-Nya yang begitu besar kepadanya, bersukacitalah mereka bersama-sama dengan dia.” — Lukas 1:58\n\nTag orang yang mau kamu ajak ke ibadah Natal tahun ini 👇"},
    {"hari": 50, "teks": "Janji itu ditunggu ratusan tahun, lalu datang tepat pada waktunya.",
     "caption": "Tinggal 50 hari 🎉\n\nUmat Tuhan menantikan Mesias selama ratusan tahun. Kelihatannya lama, tapi Allah tidak pernah terlambat. Ia mengutus Anak-Nya tepat pada waktu-Nya.\n\n📖 “Tetapi setelah genap waktunya, maka Allah mengutus Anak-Nya, yang lahir dari seorang perempuan dan takluk kepada hukum Taurat.” — Galatia 4:4\n\nKetik “50” kalau kamu masih menghitung bersama kami!"},
    {"hari": 49, "teks": "Para gembala pulang sambil memuji. Natal sejati berujung pada syukur.",
     "caption": "49 hari lagi 🐑\n\nGembala-gembala tidak membawa pulang kado atau oleh-oleh. Mereka membawa pulang pujian, karena semua yang dikatakan kepada mereka benar-benar terjadi.\n\n📖 “Maka kembalilah gembala-gembala itu sambil memuji dan memuliakan Allah karena segala sesuatu yang mereka dengar dan mereka lihat, semuanya sesuai dengan apa yang telah dikatakan kepada mereka.” — Lukas 2:20\n\nKetik 🐑 kalau kamu mau pulang dari setiap ibadah dengan hati yang memuji."},
    {"hari": 48, "teks": "Orang Majus bersukacita melihat bintang. Apa bintang kecilmu hari ini?",
     "caption": "48 hari lagi ⭐\n\nPerjalanan orang Majus panjang dan melelahkan. Tapi saat bintang itu terlihat lagi, sukacita mereka meluap. Tuhan tahu cara memberi tanda kecil di sepanjang perjalanan kita.\n\n📖 “Ketika mereka melihat bintang itu, sangat bersukacitalah mereka.” — Matius 2:10\n\nApa ‘bintang kecil’ yang membuatmu bersyukur minggu ini? Tulis di komentar 👇"},
]

# ---------- MINIMAL: layar hitam, satu kalimat kecil (sore2 16:30) ----------
MINIMAL = [
    {"teks": "satu hari di bulan baru sudah lewat. terima kasih, Tuhan.",
     "caption": "Hari pertama November hampir selesai 🤍\n\nSebelum malam datang, berhenti sebentar dan ucapkan satu kalimat sederhana kepada Tuhan.\n\n📖 “Allahku Engkau, aku hendak bersyukur kepada-Mu, Allahku, aku hendak meninggikan Engkau.” — Mazmur 118:28\n\nKetik “Terima kasih, Tuhan” di komentar."},
    {"teks": "hari ini biasa saja. tapi Engkau menemaniku dari pagi sampai sekarang.",
     "caption": "Untuk Senin yang biasa-biasa saja 🤍\n\nTidak semua hari terasa istimewa. Tapi tidak ada satu jam pun yang Dia lewatkan.\n\n📖 “Sebab kasih setia-Mu lebih baik dari pada hidup; bibirku akan memegahkan Engkau.” — Mazmur 63:4\n\nKetik 🤍 kalau Senin-mu juga biasa-biasa saja."},
    {"teks": "aku belum bisa bilang ini baik. tapi aku bisa bilang Engkau baik.",
     "caption": "Kalimat jujur untuk hari yang berat 🤍\n\nKeadaannya mungkin belum baik. Tapi Tuhan tetap baik, dan Dia mengenal setiap orang yang datang berlindung kepada-Nya.\n\n📖 “TUHAN itu baik; Ia adalah tempat pengungsian pada waktu kesusahan; Ia mengenal orang-orang yang berlindung kepada-Nya” — Nahum 1:7\n\nKetik “Engkau baik” kalau ini juga doamu sore ini."},
    {"teks": "terima kasih untuk yang tetap tinggal, saat aku sulit dicintai.",
     "caption": "Untuk orang-orang yang tetap tinggal 🤍\n\nKita semua pernah sulit dicintai. Tuhan sering memakai orang-orang yang sabar untuk mengingatkan kita bahwa kasih-Nya lebih sabar lagi.\n\n📖 “Tidak ada kasih yang lebih besar dari pada kasih seorang yang memberikan nyawanya untuk sahabat-sahabatnya.” — Yohanes 15:13\n\nKirim ini ke seseorang yang tetap tinggal 💌"},
    {"teks": "aku belum lihat jawabannya. tapi aku kenal siapa yang menjawab.",
     "caption": "Mengenal Dia lebih penting daripada tahu semua jawabannya 🤍\n\n📖 “Orang yang mengenal nama-Mu percaya kepada-Mu, sebab tidak Kautinggalkan orang yang mencari Engkau, ya TUHAN.” — Mazmur 9:11\n\nKetik “Aku kenal Engkau” sebagai doamu sore ini."},
    {"teks": "dulu aku takut soal hari ini. ternyata Engkau sudah di sini duluan.",
     "caption": "Ketakutan kemarin, kesetiaan-Nya hari ini 🤍\n\nBanyak hal yang dulu kita takutkan, hari ini sudah kita lewati. Bukan karena kita kuat, tapi karena tangan-Nya tidak pernah lepas.\n\n📖 “Dari belakang dan dari depan Engkau mengurung aku, dan Engkau menaruh tangan-Mu ke atasku.” — Mazmur 139:5\n\nSave untuk dibaca saat kamu takut soal besok 🔖"},
    {"teks": "rumah sederhana, perut kenyang, hati tenang. itu sudah banyak.",
     "caption": "Berkat yang datang diam-diam 🤍\n\nTidak semua berkat datang dengan suara keras. Ada yang datang diam-diam: rumah untuk pulang dan hati yang tenang.\n\n📖 “Engkau telah memberikan sukacita kepadaku, lebih banyak dari pada mereka ketika mereka kelimpahan gandum dan anggur.” — Mazmur 4:8\n\nTulis satu berkat sederhana Sabtu ini di komentar 👇"},
]

# ---------- C: teks di warna tegas (petang 18:00), skema WARNA di konten/tenang.py ----------
WARNA = [
    {"bg": "#A0522D", "fg": "#F4F1EA",
     "teks": ["Daftar syukur hari Minggu:", "", "ibadah tadi pagi,", "makan siang bersama,", "dan Tuhan yang tidak berubah."],
     "caption": "Daftar syukur hari Minggu 🍂\n\nKita milik-Nya, umat-Nya, domba-domba gembalaan-Nya. Itu alasan paling dasar untuk bersyukur, apa pun yang terjadi minggu ini.\n\n📖 “Ketahuilah, bahwa TUHANlah Allah; Dialah yang menjadikan kita dan punya Dialah kita, umat-Nya dan kawanan domba gembalaan-Nya.” — Mazmur 100:3\n\nTambahkan satu baris ke daftar ini di komentar 👇"},
    {"bg": "#1F6B3A", "fg": "#F4F1EA",
     "teks": ["Pekerjaan ini, meja ini,", "orang-orang di sekitarku:", "", "semuanya titipan, bukan kebetulan."],
     "caption": "Senin, dan semuanya titipan 🤍\n\nDaud mengakui bahwa semua yang mereka persembahkan untuk rumah Tuhan sebenarnya berasal dari Tuhan sendiri. Begitu juga pekerjaan dan orang-orang di sekitar kita.\n\n📖 “…Sebab dari pada-Mulah segala-galanya dan dari tangan-Mu sendirilah persembahan yang kami berikan kepada-Mu.” — 1 Tawarikh 29:14\n\nDoakan satu rekan kerjamu hari ini, lalu ketik 🙏"},
    {"bg": "#111111", "fg": "#F2F2F2",
     "teks": ["Tuhan, aku belum mengerti", "kenapa luka ini ada.", "", "Tapi aku bersyukur, Engkau", "tidak pergi saat aku terluka."],
     "caption": "Syukur yang jujur 🤍\n\nKita tidak harus mengerti semuanya untuk bisa bersyukur. Kita bersyukur untuk Tuhan yang tetap menjadi kekuatan dan perisai di tengah semuanya.\n\n📖 “TUHAN adalah kekuatanku dan perisaiku; kepada-Nya hatiku percaya. Aku tertolong sebab itu beria-ria hatiku, dan dengan nyanyianku aku bersyukur kepada-Nya.” — Mazmur 28:7\n\nKetik 🤍 kalau kamu sedang belajar bersyukur dengan jujur."},
    {"bg": "#E9D8C4", "fg": "#2B2620",
     "teks": ["Hari ini, doakan satu orang", "yang dulu mendoakanmu."],
     "caption": "Balas doa dengan doa 🙏\n\nMungkin ada seseorang yang dulu setia mendoakanmu: orang tua, kakak rohani, sahabat lama. Paulus pun tidak bisa berhenti bersyukur kepada Allah karena orang-orang yang ia kasihi.\n\n📖 “Sebab ucapan syukur apakah yang dapat kami persembahkan kepada Allah atas segala sukacita, yang kami peroleh karena kamu, di hadapan Allah kita?” — 1 Tesalonika 3:9\n\nSebut namanya dalam doa, lalu ketik “Sudah” di komentar 🤍"},
    {"bg": "#2B3A67", "fg": "#F4F1EA",
     "teks": ["Terima kasih, Tuhan,", "untuk doa yang Kaujawab", "dengan “tunggu dulu.”"],
     "caption": "Tunggu dulu juga jawaban 🤍\n\nTidak semua jawaban doa berbunyi “ya”. Kadang Tuhan menjawab dengan “tunggu dulu”, dan selama menunggu Dia tetap menolong dan melindungi.\n\n📖 “Jiwa kita menanti-nantikan TUHAN. Dialah penolong kita dan perisai kita!” — Mazmur 33:20\n\nKetik “Aku menunggu” kalau doamu sedang dijawab “tunggu dulu”."},
    {"bg": "#5E7F63", "fg": "#F4F1EA",
     "teks": ["Ada doa yang dulu tidak dikabulkan.", "", "Sekarang aku mengerti,", "itu juga kasih-Nya."],
     "caption": "Tidak semua “tidak” adalah penolakan 🤍\n\nAda doa yang dulu kita tangisi karena tidak dijawab seperti yang kita mau. Bertahun-tahun kemudian, kita baru melihat hikmat-Nya. Ada juga yang mungkin baru kita mengerti nanti.\n\n📖 “O, alangkah dalamnya kekayaan, hikmat dan pengetahuan Allah! Sungguh tak terselidiki keputusan-keputusan-Nya dan sungguh tak terselami jalan-jalan-Nya!” — Roma 11:33\n\nPernah mengalaminya? Ceritakan singkat di komentar 👇"},
    {"bg": "#F4F1EA", "fg": "#111111",
     "teks": ["Hari ini aku belajar berhenti", "menghitung yang kurang,", "", "dan mulai menghitung", "yang sudah Tuhan beri."],
     "caption": "Ganti yang dihitung 🤍\n\nDaud menulis tentang hidangan yang disediakan Tuhan dan piala yang penuh, bahkan saat lawan masih ada di sekitarnya. Kelimpahannya bukan karena masalah hilang, tapi karena Tuhan hadir.\n\n📖 “Engkau menyediakan hidangan bagiku, di hadapan lawanku; Engkau mengurapi kepalaku dengan minyak; pialaku penuh melimpah.” — Mazmur 23:5\n\nSave sebagai pengingat akhir pekan 🔖"},
]

# ---------- R: Reels suasana (malam0 19:30), skema SUASANA di konten/tenang.py ----------
SUASANA = [
    {"adegan": "bintang",
     "teks": ["Malam ini, ingat mereka", "yang sudah lebih dulu pulang.", "",
              "Nenek yang mendoakanmu diam-diam.", "Guru sekolah minggu yang sabar.", "Orang-orang yang mewariskan iman.", "",
              "Terima kasih, Tuhan,", "untuk setiap mereka."],
     "caption": "1 November: mengingat dengan syukur 🕯️\n\nIman kita tidak jatuh dari langit. Ia sampai kepada kita lewat orang-orang yang setia: nenek, ibu, guru, gembala. Ada yang masih bersama kita, ada yang sudah lebih dulu pulang.\n\n📖 “Sebab aku teringat akan imanmu yang tulus ikhlas, yaitu iman yang pertama-tama hidup di dalam nenekmu Lois dan di dalam ibumu Eunike dan yang aku yakin hidup juga di dalam dirimu.” — 2 Timotius 1:5\n\nKetik 🕯️ untuk mengenang mereka dengan syukur."},
    {"adegan": "kabut",
     "teks": ["Syukur jarang datang dari hal besar.", "Ia datang dari hal yang hampir terlewat.", "",
              "Air hangat di pagi yang dingin.", "Lampu hijau di perempatan.", "Seseorang yang bilang “hati-hati di jalan.”", "",
              "Bukan kebetulan.", "Itu kebaikan-Nya, setiap hari."],
     "caption": "Hal-hal yang hampir terlewat 🌫️\n\nPemazmur melihat semua makhluk menantikan Tuhan, dan Tuhan membuka tangan-Nya setiap hari. Kebaikan itu sering datang dalam bentuk yang sangat biasa.\n\n📖 “Mata sekalian orang menantikan Engkau, dan Engkaupun memberi mereka makanan pada waktunya; Engkau yang membuka tangan-Mu dan yang berkenan mengenyangkan segala yang hidup.” — Mazmur 145:15-16\n\nTulis satu hal kecil yang hampir kamu lewatkan hari ini 👇"},
    {"adegan": "kabut",
     "teks": ["Ada musim memberi.", "Ada musim kehilangan.", "",
              "Ayub kehilangan hampir segalanya.", "Ia mengoyak jubahnya,", "lalu sujud dan menyembah.", "",
              "Dukanya nyata.", "Tapi Tuhannya tetap Tuhan."],
     "caption": "Untuk kamu yang sedang di musim kehilangan 🌫️\n\nAyub tidak pura-pura kuat. Ia berduka dengan sungguh-sungguh. Tapi di tengah duka itu, ia tetap menyembah.\n\n📖 “…TUHAN yang memberi, TUHAN yang mengambil, terpujilah nama TUHAN!” — Ayub 1:21\n\nKalau kamu sedang berduka, ketik 🤍 dan kami ikut mendoakanmu."},
    {"adegan": "bintang",
     "teks": ["Paulus di penjara.", "Banyak yang berpaling darinya.", "",
              "Tapi ada satu nama yang ia ingat:", "Onesiforus,", "yang berusaha mencarinya di Roma.", "",
              "Terima kasih, Tuhan,", "untuk orang-orang seperti dia."],
     "caption": "Satu nama di surat terakhir Paulus ✨\n\nDi akhir hidupnya, Paulus menulis bahwa banyak orang berpaling darinya. Tapi ia menyebut satu sahabat yang tidak malu datang ke penjara.\n\n📖 “Tuhan kiranya mengaruniakan rahmat-Nya kepada keluarga Onesiforus yang telah berulang-ulang menyegarkan hatiku. Ia tidak malu menjumpai aku di dalam penjara.” — 2 Timotius 1:16\n\nTag ‘Onesiforus’ di hidupmu, orang yang tetap datang saat kamu jatuh 👇"},
    {"adegan": "kabut",
     "teks": ["Menunggu itu sunyi.", "Tidak ada yang bertepuk tangan", "untuk setiap hari yang kamu lewati.", "",
              "Tapi Tuhan tahu berapa lama", "kamu sudah bertahan.", "",
              "Dan suatu hari kita akan berkata:", "“Inilah Dia yang kita nanti-nantikan.”"],
     "caption": "Untuk malam-malam penantian 🌫️\n\nYesaya menulis tentang hari ketika umat Tuhan melihat bahwa penantian mereka tidak sia-sia. Penantian kita pun ada di tangan-Nya.\n\n📖 “…Sesungguhnya, inilah Allah kita, yang kita nanti-nantikan, supaya kita diselamatkan…” — Yesaya 25:9\n\nKirim ke seseorang yang sedang menanti dengan sabar 💌"},
    {"adegan": "bintang",
     "teks": ["Sebelum tidur, putar ulang minggu ini.", "",
              "Bukan untuk menghitung yang gagal,", "tapi untuk menemukan", "di mana saja Tuhan hadir.", "",
              "Di percakapan itu.", "Di jalan pulang itu.", "Di kasur yang menunggumu malam ini."],
     "caption": "Putar ulang minggu ini 🌌\n\nDaud mengajak jiwanya sendiri untuk tidak melupakan kebaikan Tuhan. Salah satunya: Dia yang memahkotai kita dengan kasih setia dan rahmat.\n\n📖 “Dia yang menebus hidupmu dari lobang kubur, yang memahkotai engkau dengan kasih setia dan rahmat,” — Mazmur 103:4\n\nSave dan coba lakukan sebelum tidur malam ini 🔖"},
    {"adegan": "bintang",
     "teks": ["Satu minggu lagi selesai.", "Ada yang berjalan baik,", "ada yang belum.", "",
              "Tapi dari Minggu sampai Sabtu,", "Dia ada di setiap hari itu.", "",
              "Sebelum tidur,", "ucapkan terima kasih pelan-pelan."],
     "caption": "Sabtu malam, sebelum hari Minggu ✨\n\nIbadah besok bukan cuma soal datang, tapi juga soal membawa sesuatu: ucapan syukur dari minggu yang sudah kita lewati bersama-Nya.\n\n📖 “Sebab itu marilah kita, oleh Dia, senantiasa mempersembahkan korban syukur kepada Allah, yaitu ucapan bibir yang memuliakan nama-Nya.” — Ibrani 13:15\n\nTulis satu hal yang mau kamu syukuri di ibadah besok 👇"},
]

# ---------- LED: papan LED titik-titik (malam 21:00) ----------
LED = [
    {"teks": "HARI PERTAMA\nNOVEMBER\nDIA TETAP\nSAMA", "ref": "Mazmur 102:28",
     "caption": "Hari pertama November selesai ✨\n\nTahun berganti, bulan berganti, rencana kita pun berganti. Dia tidak.\n\n📖 “tetapi Engkau tetap sama, dan tahun-tahun-Mu tidak berkesudahan.” — Mazmur 102:28\n\nKetik “Tetap sama” sebelum tidur malam ini 🤍"},
    {"teks": "TETAP\nBERDOA\nSAMBIL\nBERSYUKUR", "ref": "Kolose 4:2",
     "caption": "Pesan malam untuk hari Senin 💡\n\nPaulus mengajak jemaat bertekun dalam doa dan berjaga-jaga sambil mengucap syukur. Doa dan syukur selalu berjalan bersama.\n\n📖 “Bertekunlah dalam doa dan dalam pada itu berjaga-jagalah sambil mengucap syukur.” — Kolose 4:2\n\nSebelum tidur, ucapkan satu doa dan satu terima kasih. Lalu ketik “Amin” 🙏"},
    {"teks": "ALLAH\nTUHANKU\nKEKUATANKU", "ref": "Habakuk 3:19",
     "caption": "Akhir dari doa Habakuk 💡\n\nDoa yang dimulai dengan panen gagal ditutup dengan kaki yang kuat untuk mendaki. Bukan karena musimnya berubah, tapi karena Allah menjadi kekuatannya.\n\n📖 “ALLAH Tuhanku itu kekuatanku: Ia membuat kakiku seperti kaki rusa, Ia membiarkan aku berjejak di bukit-bukitku.” — Habakuk 3:19\n\nKetik “Kekuatanku” kalau malam ini kamu butuh dikuatkan 🤍"},
    {"teks": "TERIMA KASIH\nSUDAH\nBERTAHAN\nDENGANKU", "ref": "Amsal 18:24",
     "caption": "Untuk sahabat yang lebih dari saudara 💡\n\nScreenshot ini, lalu kirim ke sahabat yang tetap ada di musim terberatmu.\n\n📖 “…tetapi ada juga sahabat yang lebih karib dari pada seorang saudara.” — Amsal 18:24\n\nTag dia sekarang juga 👇"},
    {"teks": "ALLAH\nTELAH\nMENDENGAR", "ref": "Mazmur 66:19",
     "caption": "Pesan malam untuk yang masih berdoa 💡\n\nPemazmur bersaksi: Allah mendengar dan memperhatikan doanya. Malam ini, kamu boleh tidur dengan keyakinan yang sama.\n\n📖 “Sesungguhnya, Allah telah mendengar, Ia telah memperhatikan doa yang kuucapkan.” — Mazmur 66:19\n\nKetik “Didengar” sebelum tidur 🌙"},
    {"teks": "SEPULUH\nSEMBUH\nSATU\nKEMBALI", "ref": "Lukas 17:15-16",
     "caption": "Sepuluh sembuh, satu kembali 💡\n\nSepuluh orang kusta berseru minta dikasihani, dan kesepuluhnya disembuhkan. Tapi hanya satu yang kembali untuk mengucap syukur, dan Yesus memperhatikannya.\n\n📖 “Seorang dari mereka, ketika melihat bahwa ia telah sembuh, kembali sambil memuliakan Allah dengan suara nyaring, lalu tersungkur di depan kaki Yesus dan mengucap syukur kepada-Nya…” — Lukas 17:15-16\n\nMalam ini, jadilah yang kembali. Ketik 🙏 sebagai ucapan syukurmu."},
    {"teks": "BESOK\nBAWA\nSYUKURMU\nKE RUMAH-NYA", "ref": "Mazmur 95:2",
     "caption": "Sabtu malam, pengingat kecil 💡\n\nBesok pagi pintu gereja dibuka lagi. Datanglah, bukan dengan tangan kosong, tapi dengan nyanyian syukur untuk satu minggu penuh penyertaan-Nya.\n\n📖 “Biarlah kita menghadap wajah-Nya dengan nyanyian syukur, bersorak-sorak bagi-Nya dengan nyanyian mazmur.” — Mazmur 95:2\n\nBesok kamu datang beribadah? Ketik “Hadir” ⛪"},
]

# ---------- DOA: kartu doa larut malam (larut 22:30), [kalimat] = merah ----------
DOA = [
    {"judul": "DOA UNTUK BULAN BARU",
     "isi": "Tuhan, terima kasih untuk sepuluh bulan yang sudah lewat. Ada hari yang ringan, ada hari yang membuatku hampir menyerah, tapi [Engkau tidak pernah absen satu hari pun]. Di bulan yang baru ini, aku tidak minta semuanya mudah. Aku minta mata yang bisa melihat kebaikan-Mu di setiap musim. [Ajar aku mengucap syukur lebih dulu, sebelum mengeluh.] Amin.",
     "caption": "Doa sebelum tidur di malam pertama November 🌙\n\n📖 “Tetapi aku, kepada-Mu aku percaya, ya TUHAN, aku berkata: ‘Engkaulah Allahku!’” — Mazmur 31:15\n\nKetik “Amin” kalau kamu ikut mendoakannya."},
    {"judul": "DOA UNTUK HARI BIASA",
     "isi": "Tuhan, hari ini tidak ada yang istimewa. Aku bangun, bekerja, makan, lalu pulang. Tapi kalau kuingat lagi, [hari biasa ini pun penuh dengan pemeliharaan-Mu]. Terima kasih untuk tubuh yang masih bisa bekerja, untuk makanan yang cukup, dan untuk tempat pulang. Teguhkan pekerjaan tanganku besok, dan [jangan biarkan aku terbiasa dengan kebaikan-Mu]. Amin.",
     "caption": "Doa malam untuk hari Senin yang biasa 🌙\n\n📖 “Kiranya kemurahan Tuhan, Allah kami, atas kami, dan teguhkanlah perbuatan tangan kami, ya, perbuatan tangan kami, teguhkanlah itu.” — Mazmur 90:17\n\nKetik “Amin” kalau ini juga doamu untuk besok."},
    {"judul": "DOA UNTUK MUSIM YANG SULIT",
     "isi": "Tuhan, aku tidak akan pura-pura musim ini mudah. Ada yang hilang, ada yang belum pulih, dan ada pertanyaan yang belum Kaujawab. Tapi malam ini aku mau jujur sekaligus percaya: [kasih-Mu tidak ikut hilang bersama semua yang hilang]. Kalau besok aku belum kuat, pegang aku. Dan [ajar aku menemukan satu alasan untuk bersyukur], sekecil apa pun itu. Amin.",
     "caption": "Doa untuk musim yang sulit 🌙\n\n📖 “Terpujilah Allah, Bapa Tuhan kita Yesus Kristus, Bapa yang penuh belas kasihan dan Allah sumber segala penghiburan, yang menghibur kami dalam segala penderitaan kami…” — 2 Korintus 1:3-4\n\nKalau kamu sedang di musim ini, ketik “Amin”. Kami ikut berdoa untukmu."},
    {"judul": "DOA UNTUK ORANG-ORANG BAIK",
     "isi": "Tuhan, terima kasih untuk orang-orang yang Kaukirim ke hidupku: yang mendoakanku diam-diam, yang menegurku dengan lembut, yang tidak pergi waktu aku sedang sulit. [Berkati mereka malam ini dengan cara yang hanya Engkau tahu.] Kalau ada di antara mereka yang sedang lelah, kuatkan dia. Dan [jadikan aku juga orang baik di hidup orang lain]. Amin.",
     "caption": "Doa untuk orang-orang baik di hidupmu 🌙\n\n📖 “Dan inilah doaku, semoga kasihmu makin melimpah dalam pengetahuan yang benar dan dalam segala macam pengertian,” — Filipi 1:9\n\nSebut nama mereka dalam hati, lalu ketik “Amin” 🤍"},
    {"judul": "DOA UNTUK YANG MENUNGGU",
     "isi": "Tuhan, sudah lama aku menunggu. Kadang aku tenang, kadang aku cemas lagi dan mengecek HP berkali-kali. Engkau tahu semuanya. Malam ini aku mau belajar bersyukur lebih dulu: [terima kasih karena Engkau mendengar, bahkan sebelum aku melihat jawabannya]. Apa pun kabarnya nanti, [aku tetap milik-Mu, dan Engkau tetap Allahku]. Amin.",
     "caption": "Doa malam di tengah penantian 🌙\n\n📖 “Sebab kepada-Mu, ya TUHAN, aku berharap; Engkaulah yang akan menjawab, ya Tuhan, Allahku.” — Mazmur 38:16\n\nKetik “Amin”, lalu tidurlah dengan tenang."},
    {"judul": "DOA UNTUK HATI YANG LUPA",
     "isi": "Tuhan, aku cepat sekali lupa. Minggu lalu aku berdoa dengan air mata, dan Engkau menolong. Hari ini aku sudah mengeluh lagi soal hal yang lain. Ampuni aku. [Ingatkan aku pada semua yang sudah Kaulakukan], supaya hatiku tidak mudah panik. Seperti satu orang yang kembali kepada Yesus itu, [aku mau kembali dan bilang terima kasih]. Amin.",
     "caption": "Doa untuk hati yang mudah lupa 🌙\n\n📖 “Aku hendak menyebut-nyebut perbuatan kasih setia TUHAN, perbuatan TUHAN yang masyhur, sesuai dengan segala yang dilakukan TUHAN kepada kita…” — Yesaya 63:7\n\nKetik “Amin” kalau kamu juga sering lupa."},
    {"judul": "DOA UNTUK IBADAH BESOK",
     "isi": "Tuhan, besok aku datang ke rumah-Mu. Minggu ini tidak sempurna, tapi [tidak satu hari pun Engkau meninggalkan aku]. Aku tidak mau datang hanya membawa daftar permintaan. Aku mau datang membawa terima kasih: untuk napas, untuk pengampunan, untuk orang-orang yang Kaukirim. [Siapkan hatiku untuk memuji-Mu dengan jujur.] Amin.",
     "caption": "Doa Sabtu malam, sebelum ibadah besok 🌙\n\n📖 “Aku akan mempersembahkan korban syukur kepada-Mu, dan akan menyerukan nama TUHAN,” — Mazmur 116:17\n\nKetik “Amin”, dan selamat beristirahat 🤍"},
]

# komik Eli yang sudah jadi (folder Eli): hari 1, 4, 7 di pagi2
ELI = [("edukasi", 2), ("saran", 1), ("edukasi", 3)]

_PAGI2 = {1: ("ELI", 0), 2: ("RETRO", 0), 3: ("RETRO", 1), 4: ("ELI", 1), 5: ("RETRO", 2), 6: ("RETRO", 3), 7: ("ELI", 2)}

# hari 1-7 (Minggu 1 Nov .. Sabtu 7 Nov 2026): 12 slot per hari -> (format, index)
# pagi 06:00, pagi3 07:30, pagi2 09:00, siang0 10:30, siang 12:00, siang2 13:30, sore 15:00, sore2 16:30,
# petang 18:00, malam0 19:30, malam 21:00, larut 22:30
JADWAL = {d: {"pagi": ("LAYAR", d - 1), "pagi3": ("ALKITAB", d - 1), "pagi2": _PAGI2[d],
              "siang0": ("A", d - 1), "siang": ("POSTER", d - 1), "siang2": ("D", d - 1),
              "sore": ("HITUNG", d - 1), "sore2": ("MINIMAL", d - 1), "petang": ("C", d - 1),
              "malam0": ("R", d - 1), "malam": ("LED", d - 1), "larut": ("DOA", d - 1)} for d in range(1, 8)}
