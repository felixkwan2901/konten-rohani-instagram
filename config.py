"""Pengaturan utama. Ganti handle di sini setelah username Instagram-nya pasti."""

# Senin pertama konten. Semua jam dalam WIB (Asia/Jakarta).
START_DATE = "2026-09-27"  # hari 1 = Minggu 27 Sep (sudah terposting), hari 2 = Senin
TIMEZONE = "Asia/Jakarta"

AKUN = {
    "eli": {
        "handle": "sahabat.eli",      # karakter Eli, gaya child.ink
        "jam": {"pagi": "06:00", "pagi2": "09:00", "siang": "12:00", "sore": "17:00", "malam": "21:00"},
    },
    "tenang": {
        "handle": "diam.dan.percaya",  # 3 post/hari, gaya betteryouliving
        "jam": {"pagi": "06:00", "pagi2": "09:00", "siang": "12:00", "sore": "15:00", "petang": "18:00", "malam": "21:00"},
    },
    "ayat": {
        "handle": "ayat.tersembunyi",  # ayat yang jarang dibahas, gaya kertas kuno
        "jam": ["08:00", "13:00", "19:00"],  # 3 post/hari, post diambil berurutan dari MINGGU_AYAT
    },
    "kapi": {
        "handle": "kapi.percaya",      # maskot Kapi (aktif lagi 28 Sep 2026); 5 post/hari menyusul setelah konten dibuat
        "jam": "19:00",
        "aktif": False,  # nyalakan lagi setelah IG_TOKEN_KAPI diperbaiki
    }
}

# Format B (notifikasi) di akun Tenang diposting sebagai Reels (True) atau carousel 4 slide (False).
TENANG_NOTIF_REELS = True

# Story otomatis (9:16, tanpa link) 10 menit setelah setiap post feed.
STORY_OTOMATIS = True

# Template carousel quote akun Tenang: "editorial" (baru, rata kiri) atau "klasik" (teks tengah di latar coklat).
TENANG_QUOTE_TEMPLATE = "editorial"

# Minggu tema "Bukan milikku" (dari khotbah Ps Tulus Tobing). True setelah dapat izin -> dijadwalkan minggu ke-2.
TENANG_MINGGU2_AKTIF = False

# URL publik tempat folder output/ bisa diakses Instagram (jsDelivr mengambil file dari repo GitHub
# dengan jenis file yang benar untuk gambar & video). GitHub Actions mengisi ini otomatis.
IMAGE_BASE_URL = "https://cdn.jsdelivr.net/gh/felixkwan2901/konten-rohani-instagram@main"

GRAPH_API = "https://graph.instagram.com/v23.0"

FONT = {
    "serif": "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "serif_italic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "tangan": ("/System/Library/Fonts/Noteworthy.ttc", 1),
    "tebal": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "sans_bold": ("/System/Library/Fonts/HelveticaNeue.ttc", 1),
    "sans": ("/System/Library/Fonts/HelveticaNeue.ttc", 0),
    "sans_medium": ("/System/Library/Fonts/HelveticaNeue.ttc", 10),
    "condensed": ("/System/Library/Fonts/HelveticaNeue.ttc", 9),
}
