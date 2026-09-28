"""Akun Tenang (@diam.dan.percaya) - minggu 2 (Minggu 4 Okt - Sabtu 10 Okt 2026).
Tema: dipelihara & ditemani. Skema sama dengan konten/tenang.py:
  A = carousel quote (siang), C = warna tegas (pagi), W = dinding teks gambar (sore),
  B = notifikasi, R = Reels suasana, D = dinding teks Reels (petang/malam).
Kutipan ayat: Alkitab TB. Baris kosong ("") = jeda. {handle} diganti otomatis."""

TAGS = "#renunganharian #ayatalkitab #firmanTuhan #kristen #quoteskristen #tenangdalamTuhan #doa"

# ---------- A: carousel quote (siang) ----------
POSTS = [
    {
        "warna": "coklat",
        "hook": "Kamu tidak kekurangan.",
        "masalah": ["Merasa hidupmu kurang?", "Kurang uang, kurang waktu,", "kurang dimengerti?", "", "Gembalamu tahu kebutuhanmu."],
        "ayat": "“TUHAN adalah gembalaku, takkan kekurangan aku.”",
        "ref": "Mazmur 23:1",
        "refleksi": ["Mungkin tidak semua keinginan terpenuhi.", "", "Tapi kamu tidak pernah", "dibiarkan tanpa Gembala."],
        "cta": ["Kirim ini ke seseorang", "yang sedang merasa kurang."],
        "caption": "Kamu tidak kekurangan, karena kamu punya Gembala 🤍\n\nMungkin minggu ini terasa serba kurang. Tapi Dia yang menggembalakanmu tahu persis apa yang kamu butuhkan, dan Dia tidak pernah lalai.\n\n📖 Mazmur 23:1\n\nKetik “Gembalaku” kalau kamu mau mempercayakan minggu ini pada-Nya.",
    },
    {
        "warna": "krem",
        "hook": "Kekuatan baru untuk hari ini.",
        "masalah": ["Baru hari Senin,", "tapi rasanya sudah habis?", "", "Tenagamu memang terbatas.", "Tuhan tidak."],
        "ayat": "“Tetapi orang-orang yang menanti-nantikan TUHAN mendapat kekuatan baru: mereka seumpama rajawali yang naik terbang dengan kekuatan sayapnya; mereka berlari dan tidak menjadi lesu, mereka berjalan dan tidak menjadi lelah.”",
        "ref": "Yesaya 40:31",
        "refleksi": ["Kekuatan baru tidak datang", "dari memaksa diri.", "", "Datangnya dari menanti Dia."],
        "cta": ["Simpan ini untuk", "Senin-Senin berikutnya."],
        "caption": "Kekuatan baru untuk hari ini 🦅\n\nKalau tenagamu sudah habis padahal minggu baru mulai, tidak apa-apa. Kekuatan baru bukan hasil memaksa diri, tapi hadiah untuk yang menanti-nantikan Tuhan.\n\n📖 Yesaya 40:31\n\nSave untuk Senin berikutnya 🔖",
    },
    {
        "warna": "hitam",
        "hook": "Damai yang tidak dijual dunia.",
        "masalah": ["Liburan sudah.", "Belanja sudah.", "Scroll sampai subuh sudah.", "", "Tapi hati tetap gelisah?"],
        "ayat": "“Damai sejahtera Kutinggalkan bagimu. Damai sejahtera-Ku Kuberikan kepadamu, dan apa yang Kuberikan tidak seperti yang diberikan oleh dunia kepadamu. Janganlah gelisah dan gentar hatimu.”",
        "ref": "Yohanes 14:27",
        "refleksi": ["Damai-Nya tidak bisa dibeli.", "", "Hanya bisa diterima,", "oleh hati yang datang kepada-Nya."],
        "cta": ["Kirim ini ke temanmu", "yang sedang gelisah."],
        "caption": "Ada damai yang tidak bisa dibeli di mana pun 🤍\n\nDunia menawarkan hiburan sebentar. Yesus menawarkan damai yang tinggal, bahkan saat keadaan belum berubah.\n\n📖 Yohanes 14:27\n\nTulis di komentar: apa yang paling membuatmu gelisah minggu ini? Kita saling mendoakan.",
    },
    {
        "warna": "hijau",
        "hook": "Pertolonganmu sedang datang.",
        "masalah": ["Sudah tanya ke sana-sini.", "Sudah cari jalan keluar sendiri.", "", "Belum juga ketemu?"],
        "ayat": "“Aku melayangkan mataku ke gunung-gunung; dari manakah akan datang pertolonganku? Pertolonganku ialah dari TUHAN, yang menjadikan langit dan bumi.”",
        "ref": "Mazmur 121:1-2",
        "refleksi": ["Dia yang membuat langit dan bumi", "tidak kesulitan", "menolong satu hatimu.", "", "Angkat matamu."],
        "cta": ["Simpan untuk hari", "saat kamu buntu."],
        "caption": "Angkat matamu. Pertolonganmu datang dari Tuhan ⛰️\n\nKadang kita sudah mencari ke mana-mana, lupa melihat ke atas. Dia yang menjadikan langit dan bumi sanggup menolongmu.\n\n📖 Mazmur 121:1-2\n\nKetik “Pertolonganku dari TUHAN” sebagai doamu hari ini 🙏",
    },
    {
        "warna": "coklat",
        "hook": "Tuhan bergirang karena kamu.",
        "masalah": ["Kamu pikir Tuhan", "cuma menoleransimu?", "", "Cuma sabar", "menunggu kamu berubah?"],
        "ayat": "“TUHAN Allahmu ada di antaramu sebagai pahlawan yang memberi kemenangan. Ia bergirang karena engkau dengan sukacita, Ia membaharui engkau dalam kasih-Nya, Ia bersorak-sorak karena engkau dengan sorak-sorai.”",
        "ref": "Zefanya 3:17",
        "refleksi": ["Kamu bukan beban bagi-Nya.", "", "Kamu alasan Dia", "bersorak-sorai."],
        "cta": ["Kirim ini ke seseorang", "yang merasa tidak berharga."],
        "caption": "Tuhan tidak cuma menoleransimu. Dia bergirang karena kamu 🤍\n\nBaca pelan-pelan Zefanya 3:17. Ia bersukacita, Ia membaharui, Ia bersorak-sorak, karena engkau.\n\n📖 Zefanya 3:17\n\nTag seseorang yang perlu tahu ini hari ini 👇",
    },
    {
        "warna": "krem",
        "hook": "Kamu akan melewatinya.",
        "masalah": ["Airnya tinggi.", "Apinya panas.", "", "Tuhan tidak janji jalannya kering.", "Dia janji menyertaimu."],
        "ayat": "“Apabila engkau menyeberang melalui air, Aku akan menyertai engkau, atau melalui sungai-sungai, engkau tidak akan dihanyutkan; apabila engkau berjalan melalui api, engkau tidak akan dihanguskan, dan nyala api tidak akan membakar engkau.”",
        "ref": "Yesaya 43:2",
        "refleksi": ["Dia tidak berjanji jalannya mudah.", "", "Dia berjanji", "kamu tidak melewatinya sendirian."],
        "cta": ["Kirim ini ke temanmu", "yang sedang di tengah badai."],
        "caption": "Kamu akan melewatinya, dan kamu tidak sendirian 🌊\n\nTuhan tidak berjanji tidak akan ada air dan api. Tapi Dia berjanji menyertai, dan kamu tidak akan dihanyutkan.\n\n📖 Yesaya 43:2\n\nKetik 🤍 kalau kamu sedang di tengah badai. Kita doakan.",
    },
    {
        "warna": "hitam",
        "hook": "Boleh tidur nyenyak malam ini.",
        "masalah": ["Minggu ini banyak yang belum beres.", "Pesan belum dibalas.", "Rencana belum jalan.", "", "Tapi kamu boleh tidur."],
        "ayat": "“Dengan tenteram aku mau membaringkan diri, lalu segera tidur, sebab hanya Engkaulah, ya TUHAN, yang membiarkan aku diam dengan aman.”",
        "ref": "Mazmur 4:9",
        "refleksi": ["Yang belum selesai", "tetap ada di tangan-Nya.", "", "Tidurmu adalah tanda percaya."],
        "cta": ["Follow @{handle}", "untuk renungan setiap hari."],
        "caption": "Boleh tidur nyenyak malam ini 🌙\n\nTidak semua urusan minggu ini beres, dan itu tidak apa-apa. Tidur juga bisa jadi cara kita bilang: “Tuhan, aku percaya Engkau yang pegang.”\n\n📖 Mazmur 4:9\n\nSelamat beristirahat. Follow @{handle} untuk renungan setiap hari.",
    },
]


# ---------- C: warna tegas (pagi) ----------
WARNA = [
    {"bg": "#1F6B3A", "fg": "#F4F1EA", "teks": ["Pagi ini aku belum punya jawaban.", "Tapi aku punya Tuhan."],
     "caption": "Tidak apa-apa belum punya jawaban. Mulai saja dengan Dia 🤍\n\n📖 “TUHAN, pada waktu pagi Engkau mendengar seruanku, pada waktu pagi aku mengatur persembahan bagi-Mu, dan aku menunggu-nunggu.” — Mazmur 5:4\n\nSelamat hari Minggu. Ketik “Amin” kalau ini doamu."},
    {"bg": "#F4F1EA", "fg": "#111111", "teks": ["Kamu tidak harus punya semuanya.", "Kamu punya Dia."],
     "caption": "Kalau semuanya terasa habis, Dia tetap bagianmu 🤍\n\n📖 “Sekalipun dagingku dan hatiku habis lenyap, gunung batuku dan bagianku tetaplah Allah selama-lamanya.” — Mazmur 73:26\n\nSave untuk hari kamu merasa kosong 🔖"},
    {"bg": "#F07021", "fg": "#0E0E0E", "teks": ["Tuhan, jaga mulutku hari ini,", "dan lembutkan hatiku."],
     "caption": "Doa pendek sebelum masuk kantor, kelas, atau grup WA 🧡\n\n📖 “Awasilah mulutku, ya TUHAN, berjagalah pada pintu bibirku!” — Mazmur 141:3\n\nKetik “Amin” kalau kamu butuh doa ini hari ini 😅"},
    {"bg": "#111111", "fg": "#F2F2F2", "teks": ["Belum dijawab", "bukan berarti tidak didengar."],
     "caption": "Doamu sampai. Dia mendengar 🤍\n\n📖 “Aku sangat menanti-nantikan TUHAN; lalu Ia menjenguk kepadaku dan mendengar teriakku minta tolong.” — Mazmur 40:2\n\nKirim ke seseorang yang masih menunggu jawaban doa 💌"},
    {"bg": "#2B3A67", "fg": "#F4F1EA", "teks": ["Tenang bukan karena masalahnya hilang.", "", "Tapi karena Tuhan tetap ada."],
     "caption": "Tenang yang sejati tidak tergantung keadaan 🤍\n\n📖 “Allah itu bagi kita tempat perlindungan dan kekuatan, sebagai penolong dalam kesesakan sangat terbukti.” — Mazmur 46:2\n\nSave sebagai pengingat hari ini 🔖"},
    {"bg": "#E9D8C4", "fg": "#2B2620", "teks": ["Doa pagi ini:", "", "“Tuhan, pakai aku hari ini,", "sekecil apa pun caranya.”"],
     "caption": "Tidak ada pekerjaan yang terlalu kecil kalau dikerjakan untuk Tuhan 🤍\n\n📖 “Apa pun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan dan bukan untuk manusia.” — Kolose 3:23\n\nKetik “Pakai aku” sebagai doamu pagi ini."},
    {"bg": "#8C2F39", "fg": "#F4F1EA", "teks": ["Kasih-Nya tidak tergantung", "performamu minggu ini."],
     "caption": "Minggu ini naik turun? Kasih-Nya tetap 🤍\n\n📖 “…tidak akan dapat memisahkan kita dari kasih Allah, yang ada dalam Kristus Yesus, Tuhan kita.” — Roma 8:39\n\nSelamat berakhir pekan. Kirim ke temanmu yang keras pada dirinya sendiri 💌"},
]


# ---------- W / D: dinding teks ----------
# Index 0-6 dipakai sebagai gambar (W, sore), 7-10 sebagai Reels (D, petang/malam).
DINDING = [
    {"bg": "#2F5E45", "teks": "#43795C", "kalimat": "DIA MENDENGAR SETIAP DOA YANG KAMU BISIKKAN",
     "sorot": ["DIA", "MENDENGAR", "SETIAP", "DOA"],
     "caption": "Coba temukan kata yang menyala 👀\n\nDia mendengar setiap doa, bahkan yang cuma dibisikkan.\n\n📖 “Aku mengasihi TUHAN, sebab Ia mendengarkan suaraku dan permohonanku. Sebab Ia menyendengkan telinga-Nya kepadaku, maka seumur hidupku aku akan berseru kepada-Nya.” — Mazmur 116:1-2\n\nKetik “DIA MENDENGAR” kalau kamu butuh diingatkan ini 🤍"},
    {"bg": "#1F3A5F", "teks": "#34578A", "kalimat": "KAMU BERHARGA DI MATA TUHAN",
     "sorot": ["KAMU", "BERHARGA", "MATA", "TUHAN"],
     "caption": "Temukan pesannya 👀\n\nKamu berharga di mata Tuhan. Bukan karena prestasi, tapi karena Dia yang menciptakanmu.\n\n📖 “Aku bersyukur kepada-Mu oleh karena kejadianku dahsyat dan ajaib; ajaib apa yang Kaubuat, dan jiwaku benar-benar menyadarinya.” — Mazmur 139:14\n\nTag seseorang yang perlu dengar ini 👇"},
    {"bg": "#141414", "teks": "#383838", "kalimat": "PELAN-PELAN SAJA TUHAN TIDAK MENINGGALKANMU",
     "sorot": ["PELAN-PELAN", "SAJA", "TUHAN", "TIDAK", "MENINGGALKANMU"],
     "caption": "Coba temukan kata yang menyala 👀\n\nPelan-pelan saja. Tuhan tidak meninggalkanmu.\n\n📖 “…Janganlah kecut dan tawar hati, sebab TUHAN, Allahmu, menyertai engkau, ke mana pun engkau pergi.” — Yosua 1:9\n\nSave untuk hari yang terasa lambat 🔖"},
    {"bg": "#E9D8C4", "teks": "#D2BFA8", "kalimat": "BERSYUKUR HARI INI UNTUK HAL KECIL",
     "sorot": ["BERSYUKUR", "UNTUK", "HAL", "KECIL"],
     "caption": "Temukan pesannya 👀\n\nBersyukur untuk hal kecil: kopi hangat, pesan dari teman, napas yang masih ada.\n\n📖 “Pujilah TUHAN, hai jiwaku, dan janganlah lupakan segala kebaikan-Nya!” — Mazmur 103:2\n\nTulis satu hal kecil yang kamu syukuri hari ini 👇"},
    {"bg": "#C62F2F", "teks": "#7E1414", "kalimat": "DOAKAN LALU LEPASKAN BIAR TUHAN BEKERJA",
     "sorot": ["DOAKAN", "LEPASKAN", "TUHAN", "BEKERJA"],
     "caption": "Coba temukan kata yang menyala 👀\n\nDoakan. Lepaskan. Biar Tuhan bekerja.\n\n📖 “Serahkanlah hidupmu kepada TUHAN dan percayalah kepada-Nya, dan Ia akan bertindak.” — Mazmur 37:5\n\nKetik “AKU LEPASKAN” kalau ada yang mau kamu serahkan hari ini 🤍"},
    {"bg": "#8C2F39", "teks": "#A34450", "kalimat": "KASIH-NYA LEBIH BESAR DARI KESALAHANMU",
     "sorot": ["KASIH-NYA", "LEBIH", "BESAR", "KESALAHANMU"],
     "caption": "Temukan pesannya 👀\n\nKasih-Nya lebih besar dari kesalahanmu.\n\n📖 “Jika kita mengaku dosa kita, maka Ia adalah setia dan adil, sehingga Ia akan mengampuni segala dosa kita dan menyucikan kita dari segala kejahatan.” — 1 Yohanes 1:9\n\nSave untuk hari kamu merasa gagal 🔖"},
    {"bg": "#1F3A5F", "teks": "#34578A", "kalimat": "JANGAN MENYERAH DIA BELUM SELESAI",
     "sorot": ["JANGAN", "MENYERAH", "BELUM", "SELESAI"],
     "caption": "Coba temukan kata yang menyala 👀\n\nJangan menyerah. Dia belum selesai denganmu.\n\n📖 “Sebab itu kami tidak tawar hati, tetapi meskipun manusia lahiriah kami semakin merosot, namun manusia batiniah kami dibaharui dari sehari ke sehari.” — 2 Korintus 4:16\n\nKirim ke temanmu yang hampir menyerah 💌"},
    # --- 7-10: Reels (D) ---
    {"bg": "#141414", "teks": "#383838", "kalimat": "TUHAN MENJAGAMU SAAT KAMU TIDUR",
     "sorot": ["TUHAN", "MENJAGAMU", "SAAT", "TIDUR"],
     "caption": "Temukan pesannya 👀\n\nTuhan menjagamu, bahkan saat kamu tidur.\n\n📖 “Sesungguhnya tidak terlelap dan tidak tertidur Penjaga Israel.” — Mazmur 121:4\n\nSelamat malam. Save untuk malam-malam yang gelisah 🔖"},
    {"bg": "#2F5E45", "teks": "#43795C", "kalimat": "HARAPANMU TIDAK AKAN SIA-SIA DI DALAM DIA",
     "sorot": ["HARAPANMU", "TIDAK", "AKAN", "SIA-SIA"],
     "caption": "Coba temukan kata yang menyala 👀\n\nHarapanmu tidak akan sia-sia.\n\n📖 “Karena masa depan sungguh ada, dan harapanmu tidak akan hilang.” — Amsal 23:18\n\nKetik “TIDAK SIA-SIA” kalau kamu masih berharap 🤍"},
    {"bg": "#C62F2F", "teks": "#7E1414", "kalimat": "HATIMU AMAN DI TANGAN TUHAN",
     "sorot": ["HATIMU", "AMAN", "TANGAN", "TUHAN"],
     "caption": "Temukan pesannya 👀\n\nHatimu aman di tangan Tuhan.\n\n📖 “…seorang pun tidak akan merebut mereka dari tangan-Ku.” — Yohanes 10:28\n\nKirim ke seseorang yang hatinya sedang rapuh 💌"},
    {"bg": "#E9D8C4", "teks": "#D2BFA8", "kalimat": "BERHENTI SEJENAK DAN DENGARKAN SUARA-NYA",
     "sorot": ["BERHENTI", "SEJENAK", "DENGARKAN", "SUARA-NYA"],
     "caption": "Coba temukan kata yang menyala 👀\n\nBerhenti sejenak. Dengarkan suara-Nya.\n\n📖 “Domba-domba-Ku mendengarkan suara-Ku dan Aku mengenal mereka dan mereka mengikut Aku.” — Yohanes 10:27\n\nMalam ini, coba 5 menit tanpa HP. Ketik “SEJENAK” kalau kamu ikut 🤍"},
]


# ---------- B: notifikasi dari Tuhan (Reels) ----------
# Kalimat "Tuhan" adalah parafrase ayat di slide terakhir, bukan kutipan langsung.
NOTIF = [
    {"adegan": "fajar",
     "pesan": ["Selamat pagi. Aku sudah di sini lebih dulu.", "Minggu ini tidak akan kamu jalani sendirian.", "Aku menjaga keluar masukmu."],
     "ayat": "“TUHAN akan menjaga keluar masukmu, dari sekarang sampai selama-lamanya.”",
     "ref": "Mazmur 121:8",
     "caption": "Kalau Tuhan kirim pesan di awal minggu, mungkin bunyinya begini 🤍\n\nDia menjaga keluar masukmu: berangkat kerja, pulang sekolah, perjalanan jauh, semuanya.\n\n📖 Mazmur 121:8\n\nGeser sampai slide terakhir 👉\nKetik “Aku dijaga” kalau kamu percaya."},
    {"adegan": "laut",
     "pesan": ["Merasa tidak terlihat hari ini?", "Aku melihatmu, sejak awal.", "Kamu terlukis di telapak tangan-Ku."],
     "ayat": "“Lihat, Aku telah melukiskan engkau di telapak tangan-Ku; tembok-tembokmu tetap di ruang mata-Ku.”",
     "ref": "Yesaya 49:16",
     "caption": "Untuk kamu yang merasa tidak terlihat 🌅\n\nMungkin orang lain lupa. Tapi kamu terlukis di telapak tangan-Nya.\n\n📖 Yesaya 49:16\n\nKirim ke seseorang yang sedang merasa sendirian 💌"},
    {"adegan": "fajar",
     "pesan": ["Yang kemarin sudah Kuampuni.", "Jangan bawa rasa bersalah itu ke hari ini.", "Kamu ciptaan baru. Mulai lagi bersama-Ku."],
     "ayat": "“Jadi siapa yang ada di dalam Kristus, ia adalah ciptaan baru: yang lama sudah berlalu, sesungguhnya yang baru sudah datang.”",
     "ref": "2 Korintus 5:17",
     "caption": "Rasa bersalah kemarin tidak perlu ikut ke hari ini 🤍\n\nDi dalam Kristus, yang lama sudah berlalu. Kamu boleh mulai lagi.\n\n📖 2 Korintus 5:17\n\nKetik “Mulai lagi” kalau kamu butuh awal yang baru."},
    {"adegan": "laut",
     "pesan": ["Kamu sudah memberi banyak minggu ini.", "Sekarang giliranmu dipulihkan.", "Duduk sebentar bersama-Ku."],
     "ayat": "“Ia membaringkan aku di padang yang berumput hijau, Ia membimbing aku ke air yang tenang; Ia menyegarkan jiwaku.”",
     "ref": "Mazmur 23:2-3",
     "caption": "Untuk kamu yang sibuk menolong semua orang 🌊\n\nKamu juga butuh dipulihkan. Duduk sebentar, biarkan Dia menyegarkan jiwamu.\n\n📖 Mazmur 23:2-3\n\nTag teman yang selalu ada untuk orang lain 👇"},
    {"adegan": "fajar",
     "pesan": ["Jangan ukur kasih-Ku dari keadaanmu.", "Aku tetap baik, bahkan hari ini.", "Kasih setia-Ku untuk selama-lamanya."],
     "ayat": "“Sebab TUHAN itu baik, kasih setia-Nya untuk selama-lamanya, dan kesetiaan-Nya tetap turun-temurun.”",
     "ref": "Mazmur 100:5",
     "caption": "Keadaanmu bisa berubah. Kebaikan-Nya tidak 🤍\n\n📖 Mazmur 100:5\n\nSave dan baca lagi saat minggumu terasa berat 🔖"},
]


# ---------- R: Reels suasana ----------
SUASANA = [
    {"adegan": "bintang",
     "teks": ["Suatu malam Tuhan mengajak Abram keluar,", "lalu menyuruhnya menghitung bintang.", "",
              "Janjinya belum terlihat.", "Tapi langitnya penuh pengingat.", "",
              "Malam ini, lihat ke atas.", "Janji-Nya untukmu juga belum selesai."],
     "caption": "Setiap bintang adalah pengingat: janji-Nya belum selesai ✨\n\n📖 “Coba lihat ke langit, hitunglah bintang-bintang, jika engkau dapat menghitungnya.” Maka firman-Nya kepadanya: “Demikianlah banyaknya nanti keturunanmu.” — Kejadian 15:5\n\nKetik ✨ kalau kamu sedang memegang sebuah janji Tuhan."},
    {"adegan": "kabut",
     "teks": ["Kalau jalan di depan tertutup kabut,", "dengarkan baik-baik.", "",
              "“Inilah jalan, berjalanlah mengikutinya.”", "Yesaya 30:21", "",
              "Dia tidak akan membiarkanmu", "menebak-nebak sendirian."],
     "caption": "Saat jalannya belum jelas, suara-Nya tetap jelas 🌫️\n\n📖 “Dan telingamu akan mendengar perkataan ini dari belakangmu: “Inilah jalan, berjalanlah mengikutinya,” entah kamu menganan atau mengiri.” — Yesaya 30:21\n\nSave untuk hari kamu harus mengambil keputusan 🔖"},
    {"adegan": "bintang",
     "teks": ["Langit seluas ini.", "Bintang sebanyak ini.", "",
              "Dan Dia masih mengingatmu.", "", "“Apakah manusia, sehingga Engkau mengingatnya?”", "Mazmur 8:5"],
     "caption": "Dia yang menempatkan bintang-bintang masih mengingatmu ✨\n\n📖 “Jika aku melihat langit-Mu, buatan jari-Mu, bulan dan bintang-bintang yang Kautempatkan: apakah manusia, sehingga Engkau mengingatnya? Apakah anak manusia, sehingga Engkau mengindahkannya?” — Mazmur 8:4-5\n\nKirim ke seseorang yang merasa kecil dan terlupakan 💌"},
    {"adegan": "kabut",
     "teks": ["Iman bukan berarti melihat semuanya.", "Iman berarti tetap melangkah", "saat belum melihat.", "",
              "Satu langkah.", "Lalu satu lagi.", "", "Dia berjalan bersamamu."],
     "caption": "Hidup karena percaya, bukan karena melihat 🌫️\n\n📖 “Sebab hidup kami ini adalah hidup karena percaya, bukan karena melihat.” — 2 Korintus 5:7\n\nKetik “satu langkah” kalau kamu sedang belajar percaya."},
    {"adegan": "bintang",
     "teks": ["Gelap bagimu,", "tidak gelap bagi-Nya.", "",
              "Malam yang kamu takutkan", "terang seperti siang di mata-Nya.", "",
              "Tidurlah.", "Dia tetap melihat semuanya."],
     "caption": "Tidak ada malam yang terlalu gelap bagi-Nya 🌙\n\n📖 “Kegelapan pun tidak menggelapkan bagi-Mu, dan malam menjadi terang seperti siang; kegelapan sama seperti terang.” — Mazmur 139:12\n\nSelamat beristirahat. Save untuk malam yang panjang 🔖"},
]


# Jadwal per hari (Minggu 4 Okt .. Sabtu 10 Okt 2026).
# pagi = C, siang = A, sore = W (DINDING 0-6), petang/malam = B, R, atau D (DINDING 7-10).
JADWAL = [
    [("pagi", "C", 0), ("siang", "A", 0), ("sore", "W", 0), ("petang", "B", 0), ("malam", "R", 0)],   # Minggu 4 Okt
    [("pagi", "C", 1), ("siang", "A", 1), ("sore", "W", 1), ("petang", "B", 1), ("malam", "D", 7)],   # Senin 5 Okt
    [("pagi", "C", 2), ("siang", "A", 2), ("sore", "W", 2), ("petang", "R", 1), ("malam", "D", 8)],   # Selasa 6 Okt
    [("pagi", "C", 3), ("siang", "A", 3), ("sore", "W", 3), ("petang", "B", 2), ("malam", "R", 2)],   # Rabu 7 Okt
    [("pagi", "C", 4), ("siang", "A", 4), ("sore", "W", 4), ("petang", "D", 9), ("malam", "R", 3)],   # Kamis 8 Okt
    [("pagi", "C", 5), ("siang", "A", 5), ("sore", "W", 5), ("petang", "D", 10), ("malam", "B", 3)],  # Jumat 9 Okt
    [("pagi", "C", 6), ("siang", "A", 6), ("sore", "W", 6), ("petang", "B", 4), ("malam", "R", 4)],   # Sabtu 10 Okt
]
