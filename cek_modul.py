"""Cek ayat SATU modul konten (lebih cepat dari cek_ayat.py penuh): kemiripan dengan TB + huruf besar sebutan Tuhan,
plus kata Tuhan/Allah/Yesus/Bapa yang tertulis huruf kecil di mana pun (kecuali memang begitu di TB).

  python3 cek_modul.py tenang_w15        -> daftar masalah; keluar dengan kode 1 kalau ada
"""
import importlib
import re
import sys

import cek_ayat


def simpan_cache():
    """Gabungkan dengan cache di disk lalu tulis atomik (beberapa proses boleh jalan bersamaan)."""
    import json
    import os
    import tempfile
    try:
        disk = json.loads(cek_ayat.CACHE.read_text())
    except Exception:
        disk = {}
    disk.update(cek_ayat.cache)
    fd, tmp = tempfile.mkstemp(dir=cek_ayat.CACHE.parent, suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(disk, f, ensure_ascii=False)
    os.replace(tmp, cek_ayat.CACHE)


def jalan(x, path=""):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from jalan(v, f"{path}.{k}")
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from jalan(v, f"{path}[{i}]")


def main(mod):
    m = importlib.import_module(f"konten.{mod}")
    masalah, n = [], 0
    for name in dir(m):
        if not name.isupper():
            continue
        obj = getattr(m, name)
        for quote, ref, where in cek_ayat.pairs_from(obj, name):
            n += 1
            s, trans, text = cek_ayat.check(quote, ref)
            kap = cek_ayat.kapital_salah(quote, text) if text else []
            if s is None or s < 0.97 or kap:
                masalah.append(f"{'❔' if s is None else f'{s:.2f}'} {ref} @ {where}\n    kutipan: {quote}\n    TB     : {text}"
                               + (f"\n    huruf besar: {', '.join(kap)}" if kap else ""))
        for path, s in jalan(obj, name):
            for w in re.finditer(r"(?<![\w@#/.-])(tuhan|allah|yesus|kristus|bapa di sorga|roh kudus)(?![\w])", s):
                konteks = s[max(0, w.start() - 30):w.end() + 30]
                if "seorang allah" in konteks or "allah lain" in konteks or "allah-allah" in konteks:
                    continue
                masalah.append(f"huruf kecil '{w.group(1)}' @ {path}: …{konteks}…")
    simpan_cache()
    print(f"{mod}: {n} kutipan, {len(masalah)} masalah")
    for x in masalah:
        print(" -", x)
    return 1 if masalah else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
