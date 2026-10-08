"""Cek semua kutipan ayat di konten/*.py terhadap teks Alkitab asli.
  Indonesia: Alkitab Terjemahan Baru (TB) dari alkitab.sabda.org
  Inggris  : World English Bible & KJV dari bible-api.com

  python3 cek_ayat.py            # laporan -> output/cek_ayat.md (yang perlu dicek ditandai ❌/⚠️)
"""
import difflib
import importlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CACHE = ROOT / "state" / "cache_ayat.json"

ID_BOOKS = {
    "Kejadian": "Kej", "Keluaran": "Kel", "Imamat": "Im", "Bilangan": "Bil", "Ulangan": "Ul", "Yosua": "Yos", "Hakim-hakim": "Hak",
    "Rut": "Rut", "1 Samuel": "1Sam", "2 Samuel": "2Sam", "1 Raja-raja": "1Raj", "2 Raja-raja": "2Raj", "1 Tawarikh": "1Taw",
    "2 Tawarikh": "2Taw", "Ezra": "Ezr", "Nehemia": "Neh", "Ester": "Est", "Ayub": "Ayb", "Mazmur": "Mzm", "Amsal": "Ams",
    "Pengkhotbah": "Pkh", "Kidung Agung": "Kid", "Yesaya": "Yes", "Yeremia": "Yer", "Ratapan": "Rat", "Yehezkiel": "Yeh",
    "Daniel": "Dan", "Hosea": "Hos", "Yoel": "Yl", "Amos": "Am", "Obaja": "Ob", "Yunus": "Yun", "Mikha": "Mi", "Nahum": "Nah",
    "Habakuk": "Hab", "Zefanya": "Zef", "Hagai": "Hag", "Zakharia": "Za", "Maleakhi": "Mal", "Matius": "Mat", "Markus": "Mrk",
    "Lukas": "Luk", "Yohanes": "Yoh", "Kisah Para Rasul": "Kis", "Roma": "Rm", "1 Korintus": "1Kor", "2 Korintus": "2Kor",
    "Galatia": "Gal", "Efesus": "Ef", "Filipi": "Flp", "Kolose": "Kol", "1 Tesalonika": "1Tes", "2 Tesalonika": "2Tes",
    "1 Timotius": "1Tim", "2 Timotius": "2Tim", "Titus": "Tit", "Filemon": "Flm", "Ibrani": "Ibr", "Yakobus": "Yak",
    "1 Petrus": "1Ptr", "2 Petrus": "2Ptr", "1 Yohanes": "1Yoh", "2 Yohanes": "2Yoh", "3 Yohanes": "3Yoh", "Yudas": "Yud",
    "Wahyu": "Why",
}
BOOK_RE = "|".join(sorted((re.escape(b) for b in ID_BOOKS), key=len, reverse=True))
EN_RE = (r"(?:[1-3] )?(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|Samuel|Kings|Chronicles|Ezra|Nehemiah|"
         r"Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|"
         r"Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|"
         r"Galatians|Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|Revelation)")
REF_RE = re.compile(rf"({BOOK_RE}|{EN_RE}) (\d+):(\d+)(?:-(\d+))?")
MODULES = ["tenang", "tenang_keren", "tenang_w2", "tenang_keren2", "tenang_minggu2", "eli", "eli_variasi", "eli_w2",
           "kapi", "kapi_tambahan", "kapi_w2", "eli_lamb", "eli_lamb_w3", "eli_lamb_w6", "tenang_w3", "tenang_w4", "tenang_w5", "tenang_w6", "tenang_w7", "tenang_w8", "tenang_w9", "tenang_w10", "tenang_w11", "tenang_w12", "tenang_w13", "tenang_extra", "ayat", "ayat_minggu2", "ayat_minggu3", "ayat_singkat", "ayat_w2"]


def load_cache():
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


cache = load_cache()


def get(url):
    if url in cache:
        return cache[url]
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "cek-ayat/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                cache[url] = r.read().decode("utf-8", "replace")
                if len(cache) % 25 == 0:
                    CACHE.parent.mkdir(exist_ok=True)
                    CACHE.write_text(json.dumps(cache, ensure_ascii=False))
                return cache[url]
        except Exception:
            time.sleep(2)
    return ""


def tb_chapter(abbr, ch):
    """{nomor ayat TB: teks}. API SABDA memakai penomoran Inggris; nomor TB ada di awal teks, misal '(46-11)'."""
    xml = get(f"https://alkitab.sabda.org/api/passage.php?passage={urllib.parse.quote(f'{abbr} {ch}')}")
    out = {}
    for num, text in re.findall(r"<number>(\d+)</number>(?:\s*<title>.*?</title>)?\s*<text>(.*?)</text>", xml, re.S):
        m = re.search(r"\((\d+)-(\d+)\)\s*", text)
        if m and m.start() > 0:  # judul mazmur = ayat 1 di TB, lalu ayat berikutnya
            out[f"{m.group(1)}:1"] = text[:m.start()].strip()
        key = f"{m.group(1)}:{m.group(2)}" if m else f"{ch}:{num}"
        out[key] = re.sub(r"<[^>]+>", "", text[m.end():] if m else text)
    return out


def tb_text(book, ch, v1, v2):
    abbr = ID_BOOKS[book]
    verses = {}
    for c in (ch - 1, ch, ch + 1):
        if c > 0:
            verses.update(tb_chapter(abbr, c))
    return " ".join(verses.get(f"{ch}:{v}", "") for v in range(v1, v2 + 1)).strip()


def en_text(book, ch, v1, v2, trans):
    ref = f"{book} {ch}:{v1}" + (f"-{v2}" if v2 != v1 else "")
    data = get(f"https://bible-api.com/{urllib.parse.quote(ref)}?translation={trans}")
    try:
        return json.loads(data)["text"].strip()
    except Exception:
        return ""


def words(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"(\w) pun\b", r"\1pun", s)  # "apa pun" (EYD baru) = "apapun" (TB)
    return [w.strip("'") for w in re.findall(r"[a-z0-9']+(?:-[a-z0-9']+)*", s) if w.strip("'")]


def score(quote, verse):
    """Bagian kutipan (dipisah '…') harus ada berurutan di teks ayat. 1.0 = persis."""
    vw = words(verse)
    total = hit = 0
    for part in re.split(r"…|\.\.\.", quote):
        qw = words(part)
        if not qw:
            continue
        sm = difflib.SequenceMatcher(None, qw, vw, autojunk=False)
        hit += sum(b.size for b in sm.get_matching_blocks())
        total += len(qw)
    return hit / total if total else 1.0


def pairs_from(obj, where):
    """Cari (kutipan, ref) di semua isi modul: field dict, tuple Eli, baris carousel Ayat, dan caption."""
    out = []
    if isinstance(obj, dict):
        q = obj.get("ayat") or obj.get("kutipan")
        if isinstance(q, str) and isinstance(obj.get("ref"), str) and "“" in q:
            out.append((q, obj["ref"], where))
        for k, v in obj.items():
            out += pairs_from(v, f"{where}.{k}")
    elif isinstance(obj, (list, tuple)):
        if len(obj) == 4 and all(isinstance(x, str) for x in obj) and "“" in obj[2]:  # eli.POSTS
            out.append((obj[2], obj[3], where))
        for i, v in enumerate(obj):
            if isinstance(v, (list, tuple)) and len(v) >= 2 and v[0] in ("kutip", "kutip_kecil"):
                nxt = next((w for w in obj[i + 1:] if isinstance(w, (list, tuple)) and w and w[0] == "ref"), None)
                if nxt:
                    out.append((v[1], nxt[1], f"{where}[{i}]"))
            out += pairs_from(v, f"{where}[{i}]")
    elif isinstance(obj, str):
        for m in re.finditer(r"“([^”]{8,})”[\s,.]*(?:—|–|-|\()?\s*([^\n“”]{3,60})", obj):
            if REF_RE.search(m.group(2)):
                out.append(("“" + m.group(1) + "”", m.group(2), where))
    return out


def check(quote, ref_str, english=False):
    results = []
    refs = list(REF_RE.finditer(ref_str))
    if len(refs) != 1:
        return None, "banyak/tanpa referensi", ""
    m = refs[0]
    book, ch, v1 = m.group(1), int(m.group(2)), int(m.group(3))
    v2 = int(m.group(4)) if m.group(4) else v1
    if book in ID_BOOKS and not english:
        text = tb_text(book, ch, v1, v2)
        return (score(quote, text) if text else None), "TB", text
    book = {"Psalm": "Psalms"}.get(book, book)
    for trans in ("web", "kjv"):
        text = en_text(book, ch, v1, v2, trans)
        if text:
            results.append((score(quote, text), trans.upper(), text))
    return max(results) if results else (None, "EN", "")


def main():
    items = []
    for mod in MODULES:
        try:
            m = importlib.import_module(f"konten.{mod}")
        except ModuleNotFoundError:
            continue
        for name in dir(m):
            if name.isupper():
                items += [(mod, *p) for p in pairs_from(getattr(m, name), name)]
    md = (ROOT / "konten/eli-caption-minggu1.md").read_text()
    items += [("eli-caption-minggu1.md", *p) for p in pairs_from(md, "caption")]
    seen, todo = set(), []
    for mod, quote, ref, where in items:
        key = (quote.strip(), ref.strip())
        if key not in seen:
            seen.add(key)
            todo.append((mod, quote, ref, where))
    print(len(todo), "kutipan", flush=True)
    from concurrent.futures import ThreadPoolExecutor

    def one(x):
        mod, quote, ref, where = x
        s, trans, text = check(quote, ref, english=mod in ("eli_w2", "eli_lamb", "eli_lamb_w3", "eli_lamb_w6"))
        return (s if s is not None else -1, mod, where, ref.strip(), trans, quote, text)
    with ThreadPoolExecutor(2) as ex:
        rows = list(ex.map(one, todo))
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False))
    rows.sort(key=lambda r: r[0])
    lines = [f"# Cek ayat ({len(rows)} kutipan)\n", "❌ < 0.85 · ⚠️ < 0.97 · ✅ cocok\n"]
    for s, mod, where, ref, trans, quote, text in rows:
        mark = "❔" if s < 0 else "❌" if s < 0.85 else "⚠️" if s < 0.97 else "✅"
        if mark == "✅":
            continue
        lines.append(f"\n## {mark} {s:.2f}  {ref} ({trans})  — {mod} {where}\n- kutipan: {quote}\n- asli   : {text}\n")
    ok = sum(1 for r in rows if r[0] >= 0.97)
    lines.insert(2, f"\n✅ {ok} cocok, {len(rows) - ok} perlu dicek\n")
    out = ROOT / "output" / "cek_ayat.md"
    out.write_text("".join(lines))
    print(f"{len(rows)} kutipan, {ok} cocok, {len(rows) - ok} perlu dicek -> {out}")


if __name__ == "__main__":
    main()
