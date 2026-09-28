"""Akun Eli - variasi konten minggu 1 (hari 2-7). Supaya tidak semuanya Reels:
  09:00 EDUKASI  "Eli Belajar"   carousel 4 slide (pertanyaan -> 2 slide jawaban -> penutup + ayat)
  12:00 KUIS     "Kuis Alkitab"  1 gambar, jawaban di akhir caption
  17:00 SARAN    "Tips dari Eli" carousel (pembuka -> kartu tips -> penutup + ayat)
Kutipan ayat: Alkitab TB. Fakta edukasi sudah dicek; yang bersifat tradisi/perkiraan ditulis "sekitar"."""

TAGS = "#sahabateli #belajaralkitab #faktaalkitab #renunganharian #anakkristen #sekolahminggu"

EDUKASI = [
    {"tanya": "Alkitab itu ditulis siapa ya?",
     "jawab": [("66 kitab, 1 pesan", "Alkitab berisi 66 kitab: 39 di Perjanjian Lama dan 27 di Perjanjian Baru."),
               ("Banyak penulis", "Ditulis oleh sekitar 40 penulis, selama kurang lebih 1.500 tahun, dalam 3 bahasa: Ibrani, Aram, dan Yunani.")],
     "tutup": "Banyak penulis, tapi satu Pengarang!",
     "ayat": "“Segala tulisan yang diilhamkan Allah memang bermanfaat untuk mengajar…”", "ref": "2 Timotius 3:16",
     "caption": "Eli baru tahu: Alkitab ditulis oleh sekitar 40 penulis selama kurang lebih 1.500 tahun, tapi pesannya tetap satu 📖\n\n“Segala tulisan yang diilhamkan Allah memang bermanfaat untuk mengajar…” — 2 Timotius 3:16\n\nKamu sudah tahu fakta ini? Jawab: SUDAH / BARU TAHU 👇"},
    {"tanya": "Nama Eli artinya apa ya?",
     "jawab": [("Dari nama Elia", "Nama Eli diambil dari nama Elia, artinya kurang lebih: “Allahku adalah TUHAN.”"),
               ("Nabi yang berani", "Elia adalah nabi yang berani. Di akhir hidupnya, ia naik ke sorga dalam angin badai (2 Raja-raja 2:11). Di Alkitab juga ada Imam Eli, yang membesarkan Samuel kecil (1 Samuel 1-3).")],
     "tutup": "Aku mau berani seperti Elia!",
     "ayat": "“…lalu naiklah Elia ke sorga dalam angin badai.”", "ref": "2 Raja-raja 2:11",
     "caption": "Kenalan lagi sama Eli! Nama Eli diambil dari nama Elia, artinya kurang lebih “Allahku adalah TUHAN” 💙\n\nDi Alkitab juga ada Imam Eli (nama yang berbeda), yang membesarkan Samuel kecil. Seru ya?\n\nKamu tahu arti namamu sendiri? Tulis di komentar 👇"},
    {"tanya": "Kenapa kita bilang “Amin”?",
     "jawab": [("Artinya", "“Amin” berasal dari bahasa Ibrani. Artinya kurang lebih: “sungguh”, “benar”, atau “jadilah demikian.”"),
               ("Kapan dipakai?", "Kita mengucapkannya untuk setuju dengan doa atau firman Tuhan. Yesus juga sering memulai ajaran-Nya dengan “Sesungguhnya…”")],
     "tutup": "Jadi “Amin” itu bukan cuma penutup doa!",
     "ayat": "“…Itulah sebabnya oleh Dia kita mengatakan ‘Amin’ untuk memuliakan Allah.”", "ref": "2 Korintus 1:20",
     "caption": "Eli baru tahu arti “Amin” 🙏\n\n“Amin” artinya kurang lebih: sungguh, benar, jadilah demikian. Jadi waktu kita bilang “Amin”, kita setuju sepenuh hati dengan doa atau firman itu.\n\n📖 2 Korintus 1:20\n\nKetik “AMIN” kalau kamu setuju 😄"},
    {"tanya": "Perjanjian Lama & Baru, bedanya apa?",
     "jawab": [("Perjanjian Lama", "39 kitab, ditulis sebelum Yesus lahir. Isinya tentang penciptaan, umat Israel, dan janji tentang Mesias yang akan datang."),
               ("Perjanjian Baru", "27 kitab, tentang kehidupan Yesus, gereja mula-mula, dan surat-surat untuk jemaat. Janji di Perjanjian Lama digenapi dalam Yesus.")],
     "tutup": "Dua bagian, satu cerita besar tentang kasih Tuhan!",
     "ayat": "“…Aku datang bukan untuk meniadakannya, melainkan untuk menggenapinya.”", "ref": "Matius 5:17",
     "caption": "Perjanjian Lama dan Perjanjian Baru itu bukan dua cerita yang berbeda. Keduanya satu cerita besar tentang kasih Tuhan, dan puncaknya di Yesus 📖\n\n📖 Matius 5:17\n\nKamu paling suka baca kitab apa? Tulis di komentar 👇"},
    {"tanya": "Pasal paling panjang di Alkitab?",
     "jawab": [("Paling panjang", "Mazmur 119, dengan 176 ayat! Kitab Mazmur sendiri punya 150 pasal."),
               ("Paling pendek", "Mazmur 117, hanya 2 ayat. Dan salah satu ayat terpendek: “Maka menangislah Yesus.” (Yohanes 11:35)")],
     "tutup": "Panjang atau pendek, semuanya firman Tuhan!",
     "ayat": "“Pujilah TUHAN, hai segala bangsa, megahkanlah Dia, hai segala suku bangsa!”", "ref": "Mazmur 117:1",
     "caption": "Fakta seru dari Eli 🤓\n\nPasal terpanjang di Alkitab: Mazmur 119 (176 ayat). Pasal terpendek: Mazmur 117 (cuma 2 ayat). Dan salah satu ayat terpendek: “Maka menangislah Yesus.”\n\nTantangan: coba baca Mazmur 117 sekarang, cuma 30 detik 😄"},
    {"tanya": "Kenapa kita ibadah hari Minggu?",
     "jawab": [("Hari kebangkitan", "Yesus bangkit dari kematian pada hari pertama minggu itu, yaitu hari Minggu (Lukas 24:1-6)."),
               ("Sejak gereja mula-mula", "Jemaat mula-mula sudah berkumpul pada hari pertama minggu untuk beribadah (Kisah Para Rasul 20:7).")],
     "tutup": "Setiap Minggu kita merayakan Yesus yang hidup!",
     "ayat": "“…tetapi pagi-pagi benar pada hari pertama minggu itu mereka pergi ke kubur…”", "ref": "Lukas 24:1",
     "caption": "Besok hari Minggu! Tahu nggak kenapa kita ibadah hari Minggu? 🌅\n\nKarena Yesus bangkit pada hari pertama minggu itu, dan jemaat mula-mula sudah berkumpul di hari itu (Kisah Para Rasul 20:7).\n\nSampai ketemu di gereja besok ya! Ajak satu temanmu 🙌"},
]

SARAN = [
    {"judul": "Saat teduh 5 menit",
     "tips": [("Pilih satu ayat saja", "Mulai dari Mazmur atau Injil. Satu ayat sudah cukup."),
              ("Baca pelan-pelan, 2 kali", "Garis bawahi kata yang paling menarik untukmu."),
              ("Tanya ke dirimu", "“Apa yang Tuhan mau katakan untukku hari ini?”"),
              ("Tutup dengan doa singkat", "Cukup satu atau dua kalimat, dari hati.")],
     "ayat": "“Diamlah dan ketahuilah, bahwa Akulah Allah!”", "ref": "Mazmur 46:11",
     "caption": "Nggak sempat saat teduh lama? Coba versi 5 menit dari Eli ⏱️📖\n\n1. Pilih satu ayat\n2. Baca pelan-pelan 2 kali\n3. Tanya: apa kata Tuhan untukku hari ini?\n4. Tutup dengan doa singkat\n\nSave dan coba besok pagi 🔖"},
    {"judul": "Bingung mau doa apa?",
     "tips": [("Puji", "Katakan siapa Tuhan: baik, setia, kuat."),
              ("Akui", "Jujur tentang kesalahanmu hari ini."),
              ("Syukuri", "Sebut hal-hal kecil yang kamu syukuri."),
              ("Minta", "Doakan kebutuhanmu dan orang lain.")],
     "ayat": "“…nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa dan permohonan dengan ucapan syukur.”", "ref": "Filipi 4:6",
     "caption": "Bingung mau doa apa? Coba 4 langkah dari Eli 🙏\n\nPuji → Akui → Syukuri → Minta\n\nTidak harus panjang, yang penting jujur.\n\n📖 Filipi 4:6\n\nSave untuk dicoba malam ini 🔖"},
    {"judul": "Cara menghafal ayat",
     "tips": [("Tulis di kertas tempel", "Tempel di cermin atau jadikan wallpaper HP."),
              ("Ucapkan keras 3 kali", "Pagi, siang, dan sebelum tidur."),
              ("Hafal per potongan", "Potong ayat panjang jadi 2-3 bagian."),
              ("Ajak teman", "Saling tes hafalan, lebih seru!")],
     "ayat": "“Dalam hatiku aku menyimpan janji-Mu, supaya aku jangan berdosa terhadap Engkau.”", "ref": "Mazmur 119:11",
     "caption": "Mau hafal ayat tapi gampang lupa? Ini tips dari Eli 📝\n\n1. Tulis di kertas tempel\n2. Ucapkan keras 3x sehari\n3. Hafal per potongan\n4. Ajak teman saling tes\n\n📖 Mazmur 119:11\n\nAyat apa yang mau kamu hafal minggu ini? 👇"},
    {"judul": "Kalau lagi sedih",
     "tips": [("Tidak apa-apa menangis", "Yesus juga pernah menangis (Yohanes 11:35)."),
              ("Cerita ke orang yang kamu percaya", "Orang tua, kakak, guru, atau pembina."),
              ("Bawa ke Tuhan", "Ceritakan semuanya dalam doa, apa adanya."),
              ("Baca Mazmur", "Daud juga pernah sedih, dan ia menulisnya.")],
     "ayat": "“TUHAN itu dekat kepada orang-orang yang patah hati…”", "ref": "Mazmur 34:19",
     "caption": "Kalau lagi sedih, ini kata Eli 💙\n\n1. Tidak apa-apa menangis\n2. Cerita ke orang yang kamu percaya\n3. Bawa ke Tuhan dalam doa\n4. Baca Mazmur\n\nKalau sedihnya berat dan lama, jangan dipendam sendiri. Bicarakan dengan orang dewasa yang kamu percaya atau konselor ya.\n\n📖 Mazmur 34:19"},
    {"judul": "Bersyukur sebelum tidur",
     "tips": [("Tulis 3 hal kecil", "Makan enak, teman baik, cuaca cerah. Semua dihitung!"),
              ("Sebut satu nama", "Siapa yang menolongmu hari ini? Doakan dia."),
              ("Bilang terima kasih", "Ke Tuhan, dan besok ke orangnya langsung.")],
     "ayat": "“Mengucap syukurlah dalam segala hal…”", "ref": "1 Tesalonika 5:18",
     "caption": "Kebiasaan kecil sebelum tidur dari Eli 🌙\n\n1. Tulis 3 hal kecil yang kamu syukuri\n2. Doakan satu orang yang menolongmu\n3. Bilang terima kasih\n\n📖 1 Tesalonika 5:18\n\nTulis 1 hal yang kamu syukuri hari ini 👇"},
    {"judul": "Siap-siap ibadah besok",
     "tips": [("Tidur lebih awal", "Supaya bangun segar, bukan terburu-buru."),
              ("Siapkan malam ini", "Pakaian, Alkitab, dan persembahan."),
              ("Datang 10 menit lebih awal", "Tenangkan hati sebelum ibadah mulai."),
              ("Ajak satu teman", "Ibadah lebih indah kalau bersama.")],
     "ayat": "“Aku bersukacita, ketika dikatakan orang kepadaku: ‘Mari kita pergi ke rumah TUHAN.’”", "ref": "Mazmur 122:1",
     "caption": "Besok hari Minggu! Ini tips siap-siap ibadah dari Eli ⛪\n\n1. Tidur lebih awal\n2. Siapkan pakaian & Alkitab malam ini\n3. Datang 10 menit lebih awal\n4. Ajak satu teman\n\n📖 Mazmur 122:1\n\nTag teman yang mau kamu ajak ibadah besok 👇"},
]

KUIS = [
    {"tanya": "Siapa yang ditelan ikan besar?", "pilihan": ["Daniel", "Yunus", "Musa"], "jawab": "B. Yunus (Yunus 1:17)"},
    {"tanya": "Siapa yang membangun bahtera?", "pilihan": ["Nuh", "Abraham", "Daud"], "jawab": "A. Nuh (Kejadian 6:13-14)"},
    {"tanya": "Yesus lahir di kota apa?", "pilihan": ["Nazaret", "Yerusalem", "Betlehem"], "jawab": "C. Betlehem (Matius 2:1)"},
    {"tanya": "Anak kecil itu membawa berapa roti dan ikan?", "pilihan": ["5 roti, 2 ikan", "7 roti, 3 ikan", "2 roti, 5 ikan"],
     "jawab": "A. 5 roti jelai dan 2 ikan (Yohanes 6:9)"},
]

# hari -> {slot: (format, indeks)}. Slot pagi & malam tetap Reels ayat dari konten/eli.py.
JADWAL = {
    2: {"pagi2": ("edukasi", 0), "siang": ("kuis", 0), "sore": ("saran", 0)},
    3: {"pagi2": ("edukasi", 1), "siang": ("kuis", 1), "sore": ("saran", 1)},
    4: {"pagi2": ("edukasi", 2), "siang": ("payung", 0), "sore": ("saran", 2)},
    5: {"pagi2": ("edukasi", 3), "siang": ("kuis", 2), "sore": ("saran", 3)},
    6: {"pagi2": ("edukasi", 4), "siang": ("kuis", 3), "sore": ("saran", 4)},
    7: {"pagi2": ("edukasi", 5), "sore": ("saran", 5)},   # hari 7 siang = carousel cerita "Pot"
}
