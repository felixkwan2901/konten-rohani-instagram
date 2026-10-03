"""Halaman prompt Eli & Ruthie (untuk dipublikasikan sebagai Artifact).
  python3 eli_lamb_page.py <path-output.html>
Kartu yang gambarnya sudah ada di output/eli_lamb/raw/ ditandai "Done"."""
import base64
import html
import io
import sys
from datetime import date, timedelta

from PIL import Image

import eli_lamb
from konten import eli_lamb as el

START = date(2026, 10, 4)  # hari 1
SLOT_NZ = {"pagi": "7:00 am", "pagi2": "12:00 pm", "malam": "8:00 pm"}
INSTR = ("You create photorealistic images of two recurring characters from the attached reference photos: Eli (fluffy white lamb) "
         "and his wife Ruthie (fluffy caramel-brown lamb with long eyelashes and a small pink daisy behind one ear). Always keep their "
         "faces, wool colour and size exactly the same as the references. Portrait orientation (2:3). Never add any text, letters, "
         "signs, watermarks or logos to the image.")
REFS = [("Eli", "eli.webp"), ("Ruthie", "ruthie.webp"), ("Eli & Ruthie", "couple.webp")]


def thumb(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((360, 540))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def box(text, i):
    return (f'<div class="copybox"><textarea id="t{i}" readonly rows="4">{html.escape(text)}</textarea>'
            f'<button type="button" data-t="t{i}">Copy</button></div>')


def build():
    weeks, i = {}, 0
    for p in el.POSTS:
        weeks.setdefault((p["hari"] - 1) // 7, {}).setdefault(p["hari"], []).append(p)
    sections = []
    for w, days in sorted(weeks.items(), reverse=True):  # minggu terbaru di atas
        total = sum(len(v) for v in days.values())
        done = sum(1 for v in days.values() for p in v if eli_lamb.raw_path(p["id"]))
        first = START + timedelta(days=7 * w)
        day_html = []
        for hari, posts in days.items():
            d = START + timedelta(days=hari - 1)
            items = []
            for p in posts:
                i += 1
                ok = eli_lamb.raw_path(p["id"]) is not None
                w_ = p.get("who", "couple" if p.get("pasangan") else "eli")
                who = {"eli": '<span class="chip">Eli</span>', "ruthie": '<span class="chip both">Ruthie</span>',
                       "couple": '<span class="chip both">Eli + Ruthie</span>', "friends": '<span class="chip both">With friends</span>'}[w_]
                tags = who + (' <span class="chip reel">Reel</span>' if p["reel"] else "") + (' <span class="chip ok">Done</span>' if ok else "")
                scene = "Scene: " + p["prompt"].split("Scene: ", 1)[1]
                items.append(f'<li class="post{" is-done" if ok else ""}"><div class="meta"><code class="file">{p["id"]}.jpg</code>{tags}'
                             f'<span class="time">{SLOT_NZ[p["slot"]]} NZ</span></div>'
                             f'<p class="meme">{html.escape(p["teks"]).replace(chr(10), "<br>")}</p>{box(scene, i)}</li>')
            day_html.append(f'<section class="day"><h3>{d:%a %-d %b}</h3><ol class="posts">{"".join(items)}</ol></section>')
        sections.append(f'<section class="week" id="week{w + 1}"><div class="weekhead"><h2>Week {w + 1} · {first:%-d} to '
                        f'{first + timedelta(days=6):%-d %b}</h2><span class="progress">{done} of {total} images done</span></div>'
                        f'{"".join(day_html)}</section>')
    refs = "".join(f'<figure><img src="{thumb(eli_lamb.OUT / "eli_lamb" / "ref" / f)}" alt="{n} reference"><figcaption>{n}</figcaption></figure>'
                   for n, f in REFS)
    return f'''<title>Eli &amp; Ruthie Prompts</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=Nunito+Sans:wght@400;600;700&display=swap">
<style>
:root{{--bg:#F7F8F3;--card:#FFFFFF;--ink:#1F2420;--muted:#646B63;--line:#DDE2D6;--accent:#3E6B3A;--accent-ink:#FFFFFF;--chip:#E8EFE3;--chip2:#F6E7D6;--chip2-ink:#7A4A1E;--code:#EEF1EA;--ok:#2F6B3A;--ok-bg:#DDEEDC}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--bg:#131713;--card:#1B211C;--ink:#E9EDE6;--muted:#9AA398;--line:#2E3630;--accent:#8CC286;--accent-ink:#0E140E;--chip:#26322A;--chip2:#3A2C1F;--chip2-ink:#E9C39A;--code:#232A24;--ok:#9FD69A;--ok-bg:#223A24}}}}
:root[data-theme="dark"]{{color-scheme:dark;--bg:#131713;--card:#1B211C;--ink:#E9EDE6;--muted:#9AA398;--line:#2E3630;--accent:#8CC286;--accent-ink:#0E140E;--chip:#26322A;--chip2:#3A2C1F;--chip2-ink:#E9C39A;--code:#232A24;--ok:#9FD69A;--ok-bg:#223A24}}
body{{background:var(--bg);color:var(--ink);font:16px/1.55 "Nunito Sans",system-ui,-apple-system,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding-inline:16px;padding-block:24px 48px;display:grid;gap:28px}}
h1,h2,h3{{font-family:"Bricolage Grotesque","Nunito Sans",system-ui,sans-serif;text-wrap:balance;margin:0}}
h1{{font-size:30px;line-height:1.15}} h2{{font-size:21px}} h3{{font-size:17px;color:var(--accent);letter-spacing:.02em}}
.lead{{color:var(--muted);margin:6px 0 0;max-width:62ch}}
.jump{{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}} .jump a{{color:var(--accent);font-weight:700}}
.steps{{display:grid;gap:10px;margin:0;padding-left:20px}}
.refs{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0}}
figure{{margin:0;display:grid;gap:4px}} figure img{{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:10px;border:1px solid var(--line)}}
figcaption{{font-size:13px;color:var(--muted);text-align:center}}
.panel{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:12px}}
.week{{display:grid;gap:18px}} .weekhead{{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;justify-content:space-between;border-bottom:2px solid var(--accent);padding-bottom:6px}}
.progress{{font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums}}
.day{{display:grid;gap:10px}} .posts{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}
.post{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;display:grid;gap:8px}}
.post.is-done{{opacity:.6}}
.meta{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px}}
.file{{font:600 13px/1 ui-monospace,Menlo,monospace;background:var(--code);padding:4px 7px;border-radius:6px}}
.chip{{background:var(--chip);padding:3px 8px;border-radius:99px;font-weight:700;font-size:12px}}
.chip.both{{background:var(--chip2);color:var(--chip2-ink)}} .chip.reel{{background:transparent;border:1px solid var(--line)}}
.chip.ok{{background:var(--ok-bg);color:var(--ok)}}
.time{{margin-left:auto;color:var(--muted);font-variant-numeric:tabular-nums}}
.meme{{margin:0;font-weight:700;font-size:15px}}
.copybox{{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:start}}
textarea{{width:100%;box-sizing:border-box;resize:vertical;font:13px/1.45 ui-monospace,Menlo,monospace;color:var(--ink);background:var(--code);border:1px solid var(--line);border-radius:8px;padding:8px}}
button{{font:700 14px/1 "Nunito Sans",system-ui,sans-serif;background:var(--accent);color:var(--accent-ink);border:0;border-radius:8px;padding:11px 14px;cursor:pointer;min-width:74px}}
button:focus-visible,textarea:focus-visible,a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.note{{font-size:14px;color:var(--muted);margin:0}}
@media (max-width:480px){{.copybox{{grid-template-columns:1fr}} .time{{margin-left:0}}}}
</style>
<div class="wrap">
<header><h1>Eli &amp; Ruthie Prompts</h1><p class="lead">Scenes for @eliandruthie. Make each image in ChatGPT, save it with the file name on its card, and send it over. Captions, text boxes, music and posting happen automatically. Cards marked Done already have an image.</p>
<nav class="jump">{"".join(f'<a href="#week{w + 1}">Week {w + 1}</a>' for w in sorted(weeks, reverse=True))}<a href="#setup">ChatGPT setup</a></nav></header>
{"".join(sections)}
<section class="panel" id="setup"><h2>Set up once in ChatGPT</h2>
<ol class="steps"><li>Open <b>Projects → New project</b> and name it “Eli &amp; Ruthie”.</li><li>Upload these three reference photos to the project files (long-press to save them).</li><li>Paste the text below into the project’s <b>Instructions</b>.</li></ol>
<div class="refs">{refs}</div>{box(INSTR, 0)}
<h3>Friend reference photos</h3>
{"".join(f'<p class="note"><b>{html.escape(n)}</b></p>' + box(f"Photorealistic character reference photo in the same knitted-wool style as Eli and Ruthie. {d}. Full body, plain soft background, no text.", 900 + k) for k, (n, d) in enumerate(el.ALL_FRIENDS.items()))}
<p class="note"><b>Friends:</b> the first time a friend appears, save your favourite picture of them and upload it to the project too, so they stay the same every week.</p>
<p class="note">For every post: start a new chat inside the project, paste the scene, and generate. If a face drifts, reply “make them look exactly like the reference photos”. If text appears in the image, reply “remove all text”.</p></section>
</div>
<script>
document.addEventListener("click",function(e){{var b=e.target.closest("button[data-t]");if(!b)return;var t=document.getElementById(b.dataset.t);
function done(){{b.textContent="Copied";setTimeout(function(){{b.textContent="Copy"}},1500)}}
function fallback(){{t.focus();t.select();try{{document.execCommand("copy");done()}}catch(_){{b.textContent="Select + copy"}}}}
try{{navigator.clipboard.writeText(t.value).then(done,fallback)}}catch(_){{fallback()}}}});
</script>'''


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(eli_lamb.OUT / "eli_lamb" / "prompts.html")
    open(out, "w").write(build())
    print(out)
