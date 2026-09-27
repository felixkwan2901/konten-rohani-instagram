"""Akun Eli - slot tambahan minggu 1 (5 post/hari mulai hari 2): pagi2 09:00 (ID) dan sore 17:00 (EN).
Format sama dengan konten/eli.py; 'adegan' = latar yang dipakai (pagi / siang / malam).
Kalau ada 'file', post memakai file itu (misal Reels cerita) dan tidak dirender ulang."""

ID_TAGS = "#renunganpagi #ayatalkitab #firmanTuhan #renunganharian #sahabateli"
EN_TAGS = "#bibleverse #christianlife #dailydevotion #faith #sahabateli"


def id_caption(ref, kutipan, refleksi):
    return (f"Pagi-pagi, Eli mau ingatkan kamu 📖\n\n✨ {ref}\n{kutipan}\n\n{refleksi}\n\n"
            f"Tulis “Amin” kalau kamu percaya ini 💛\n.\n.\n{ID_TAGS}")


def en_caption(ref, kutipan, refleksi):
    return (f"Afternoon break with Eli 🌤️\n\n📖 {ref}\n{kutipan}\n\n{refleksi}\n\n"
            f"Eli reads every comment 💙\n.\n.\n{EN_TAGS}")


# (hari, slot, adegan, balon, kutipan, referensi, refleksi)
_DATA = [
    (2, "pagi2", "pagi", "Sudah sarapan firman?", "“Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.”", "Mazmur 119:105",
     "Sebelum sibuk hari ini, ambil satu ayat dulu. Firman-Nya menerangi langkahmu."),
    (2, "sore", "siang", "Tired today?", "“He gives strength to the weary and increases the power of the weak.”", "Isaiah 40:29",
     "If today drained you, bring your tiredness to Him. He gives strength, not just advice."),
    (3, "pagi2", "pagi", "Tuhan dengar doaku!", "“Berserulah kepada-Ku, maka Aku akan menjawab engkau…”", "Yeremia 33:3",
     "Tidak ada doa yang terlalu kecil. Dia mengundang kita untuk berseru kepada-Nya."),
    (3, "sore", "siang", "God is with me!", "“The Lord your God is with you, the Mighty Warrior who saves.”", "Zephaniah 3:17",
     "Whatever you're facing this afternoon, you're not facing it alone."),
    (4, "pagi2", "pagi", "Aku berharga!", "“Oleh karena engkau berharga di mata-Ku dan mulia, dan Aku ini mengasihi engkau…”", "Yesaya 43:4",
     "Nilaimu tidak ditentukan oleh nilai rapor, likes, atau pendapat orang. Kamu berharga di mata-Nya."),
    (5, "pagi2", "pagi", "Jangan kuatir ya!", "“Serahkanlah segala kekuatiranmu kepada-Nya, sebab Ia yang memelihara kamu.”", "1 Petrus 5:7",
     "Apa yang kamu kuatirkan pagi ini? Serahkan satu per satu kepada-Nya."),
    (5, "sore", "siang", "Keep hoping!", "“Be joyful in hope, patient in affliction, faithful in prayer.”", "Romans 12:12",
     "Hope, patience, prayer. Three small habits for a hard week."),
    (6, "pagi2", "pagi", "Tuhan itu baik!", "“Kecaplah dan lihatlah, betapa baiknya TUHAN itu!”", "Mazmur 34:9",
     "Coba hitung satu kebaikan Tuhan yang kamu alami minggu ini. Pasti ada."),
    (6, "sore", "siang", "Let's pray together!", "“The prayer of a righteous person is powerful and effective.”", "James 5:16",
     "Drop a prayer request below. Let's pray for each other this weekend."),
    (7, "pagi2", "pagi", "Besok ibadah bareng!", "“Masuklah, marilah kita sujud menyembah, berlutut di hadapan TUHAN yang menjadikan kita.”", "Mazmur 95:6",
     "Besok hari Minggu. Siapkan hatimu dari sekarang untuk bertemu Tuhan."),
    (7, "sore", "siang", "Thank You, Jesus!", "“Give thanks to the Lord, for he is good; his love endures forever.”", "Psalm 107:1",
     "One week of hope done. What are you thankful for? Tell Eli below."),
]

POSTS = []
for hari, slot, adegan, balon, kutipan, ref, refleksi in _DATA:
    cap = id_caption(ref, kutipan, refleksi) if slot == "pagi2" else en_caption(ref, kutipan, refleksi)
    POSTS.append({"hari": hari, "slot": slot, "adegan": adegan, "balon": balon, "kutipan": kutipan, "ref": ref, "caption": cap})

# Reels cerita "Payung" (sudah ada di output/contoh) mengisi hari 4 sore
POSTS.append({"hari": 4, "slot": "sore", "file": "contoh/reel_payung.mp4", "caption_file": "contoh/reel_payung_caption.txt"})
POSTS.sort(key=lambda p: (p["hari"], p["slot"] != "pagi2"))
