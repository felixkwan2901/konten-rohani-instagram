"""Font cadangan untuk mesin cloud (Linux, tanpa font macOS).

Kalau file font macOS yang diminta tidak ada (atau FONT_CLOUD=1), ImageFont.truetype diarahkan ke font bebas lisensi
(OFL/Apache, dari Google Fonts) di folder fonts/. Di Mac tidak ada yang berubah: font asli tetap dipakai.
Cukup `import fonta` sekali sebelum menggambar (config.py sudah melakukannya).
"""
import os
from pathlib import Path

from PIL import ImageFont

DIR = Path(__file__).resolve().parent / "fonts"


def nama_file(keluarga, berat, miring):
    return f"{keluarga.replace(' ', '')}-{berat}{'i' if miring else ''}.ttf"


R, B = 400, 700
# nama file macOS -> {index wajah: (keluarga Google Fonts, berat, miring)}
PETA = {
    "Georgia.ttf": {0: ("Gelasio", R, 0)},
    "Georgia Bold.ttf": {0: ("Gelasio", B, 0)},
    "Georgia Italic.ttf": {0: ("Gelasio", R, 1)},
    "Georgia Bold Italic.ttf": {0: ("Gelasio", B, 1)},
    "Times New Roman.ttf": {0: ("Tinos", R, 0)},
    "Times New Roman Bold.ttf": {0: ("Tinos", B, 0)},
    "Times New Roman Italic.ttf": {0: ("Tinos", R, 1)},
    "Courier New.ttf": {0: ("Cousine", R, 0)},
    "Courier New Bold.ttf": {0: ("Cousine", B, 0)},
    "Arial Black.ttf": {0: ("Archivo Black", R, 0)},
    "Impact.ttf": {0: ("Anton", R, 0)},
    "Tahoma Bold.ttf": {0: ("PT Sans", B, 0)},
    "Microsoft Sans Serif.ttf": {0: ("PT Sans", R, 0)},
    "DIN Condensed Bold.ttf": {0: ("Barlow Condensed", B, 0)},
    "BigCaslon.ttf": {0: ("Libre Caslon Display", R, 0)},
    "Bradley Hand Bold.ttf": {0: ("Caveat", B, 0)},
    "Trattatello.ttf": {0: ("Cinzel Decorative", R, 0)},
    "Chalkduster.ttf": {0: ("Cabin Sketch", R, 0)},
    "SFNSRounded.ttf": {0: ("Nunito", R, 0)},
    "SnellRoundhand.ttc": {0: ("Great Vibes", R, 0), 1: ("Great Vibes", R, 0), 2: ("Great Vibes", R, 0)},
    "Menlo.ttc": {0: ("JetBrains Mono", R, 0), 1: ("JetBrains Mono", B, 0), 2: ("JetBrains Mono", R, 1), 3: ("JetBrains Mono", B, 1)},
    "Didot.ttc": {0: ("Playfair Display", R, 0), 1: ("Playfair Display", R, 1), 2: ("Playfair Display", B, 0)},
    "MarkerFelt.ttc": {0: ("Permanent Marker", R, 0), 1: ("Permanent Marker", R, 0)},
    "Iowan Old Style.ttc": {0: ("Crimson Pro", R, 0), 1: ("Crimson Pro", B, 0), 2: ("Crimson Pro", R, 1), 3: ("Crimson Pro", B, 1),
                            4: ("Crimson Pro", 900, 0), 5: ("Crimson Pro", 900, 1), 6: ("Crimson Pro", R, 0)},
    "HelveticaNeue.ttc": {0: ("Inter", R, 0), 1: ("Inter", B, 0), 2: ("Inter", R, 1), 3: ("Inter", B, 1), 4: ("Roboto Condensed", B, 0),
                          5: ("Inter", 200, 0), 6: ("Inter", 200, 1), 7: ("Inter", 300, 0), 8: ("Inter", 300, 1),
                          9: ("Roboto Condensed", 900, 0), 10: ("Inter", 500, 0), 11: ("Inter", 500, 1), 12: ("Inter", 100, 0),
                          13: ("Inter", 100, 1)},
    "Futura.ttc": {0: ("Jost", 500, 0), 1: ("Jost", 500, 1), 2: ("Jost", B, 0), 3: ("Jost", 500, 0), 4: ("Jost", 800, 0)},
    "Chalkboard.ttc": {0: ("Comic Neue", R, 0), 1: ("Comic Neue", B, 0)},
    "ChalkboardSE.ttc": {0: ("Comic Neue", 300, 0), 1: ("Comic Neue", R, 0), 2: ("Comic Neue", B, 0)},
    "Baskerville.ttc": {0: ("Libre Baskerville", R, 0), 1: ("Libre Baskerville", B, 0), 2: ("Libre Baskerville", R, 1),
                        3: ("Libre Baskerville", R, 1), 4: ("Libre Baskerville", B, 0), 5: ("Libre Baskerville", R, 1)},
    "SignPainter.ttc": {0: ("Yellowtail", R, 0), 1: ("Yellowtail", R, 0)},
    "Rockwell.ttc": {0: ("Arvo", R, 0), 1: ("Arvo", R, 1), 2: ("Arvo", B, 0), 3: ("Arvo", B, 1)},
    "Avenir Next.ttc": {0: ("Nunito Sans", B, 0), 1: ("Nunito Sans", B, 1), 2: ("Nunito Sans", 600, 0), 3: ("Nunito Sans", 600, 1),
                        4: ("Nunito Sans", R, 1), 5: ("Nunito Sans", 500, 0), 6: ("Nunito Sans", 500, 1), 7: ("Nunito Sans", R, 0),
                        8: ("Nunito Sans", 800, 0), 9: ("Nunito Sans", 800, 1), 10: ("Nunito Sans", 200, 0), 11: ("Nunito Sans", 200, 1)},
    "AmericanTypewriter.ttc": {0: ("Courier Prime", R, 0), 1: ("Courier Prime", R, 0), 2: ("Courier Prime", B, 0),
                               3: ("Courier Prime", B, 0), 4: ("Courier Prime", R, 0), 5: ("Courier Prime", B, 0), 6: ("Courier Prime", R, 0)},
    "Noteworthy.ttc": {0: ("Patrick Hand", R, 0), 1: ("Patrick Hand", R, 0)},
    "GillSans.ttc": {0: ("Lato", R, 0), 1: ("Lato", B, 0), 2: ("Lato", R, 1), 3: ("Lato", B, 1), 4: ("Lato", B, 0), 5: ("Lato", B, 1),
                     6: ("Lato", 900, 0), 7: ("Lato", 300, 0), 8: ("Lato", 300, 1)},
    "Charter.ttc": {0: ("Source Serif 4", R, 0), 1: ("Source Serif 4", R, 1), 2: ("Source Serif 4", B, 1), 3: ("Source Serif 4", B, 0),
                    4: ("Source Serif 4", 900, 1), 5: ("Source Serif 4", 900, 0)},
}

_asli = ImageFont.truetype
_paksa = os.environ.get("FONT_CLOUD") == "1"


# font variabel macOS (dipakai dengan set_variation_by_name) -> font variabel pengganti + terjemahan nama berat
VARIABEL = {"SFNSRounded.ttf": "Nunito-var.ttf"}
BERAT_NAMA = {"ultralight": 200, "thin": 200, "light": 300, "regular": 400, "medium": 500, "semibold": 600, "bold": 700,
              "heavy": 800, "black": 900}


def _variabel(f):
    def set_variation_by_name(nama):
        nama = nama.decode() if isinstance(nama, bytes) else nama
        f.set_variation_by_axes([BERAT_NAMA.get(nama.lower().replace(" ", ""), 400)])
    f.set_variation_by_name = set_variation_by_name
    f.set_variation_by_axes([400])
    return f


def _truetype(font=None, size=10, index=0, encoding="", layout_engine=None):
    if isinstance(font, (str, os.PathLike)):
        nama = os.path.basename(str(font))
        if nama in VARIABEL and (_paksa or not os.path.exists(str(font))):
            return _variabel(_asli(str(DIR / VARIABEL[nama]), size, 0, encoding, layout_engine))
        if nama in PETA and (_paksa or not os.path.exists(str(font))):
            wajah = PETA[nama]
            pengganti = DIR / nama_file(*wajah.get(index, wajah[0]))
            return _asli(str(pengganti), size, 0, encoding, layout_engine)
    return _asli(font, size, index, encoding, layout_engine)


ImageFont.truetype = _truetype
