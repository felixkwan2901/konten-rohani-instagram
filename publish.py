"""Posting otomatis ke Instagram (Instagram API with Instagram Login).

Membaca output/schedule.json, memposting item yang sudah jatuh tempo dan belum pernah
diposting, lalu mencatatnya di state/posted.json. Aman dijalankan berkali-kali.

Butuh environment variable per akun (isi di GitHub Secrets):
  IG_TOKEN_ELI, IG_USER_ID_ELI, IG_TOKEN_TENANG, IG_USER_ID_TENANG, IG_TOKEN_AYAT, IG_USER_ID_AYAT
dan config.IMAGE_BASE_URL (atau env IMAGE_BASE_URL) yang menunjuk ke folder repo publik.

  python3 publish.py --dry-run     # lihat apa yang akan diposting, tanpa posting
  python3 publish.py               # posting yang sudah jatuh tempo
  python3 publish.py --tandai tenang-1-siang   # post yang sudah diupload manual
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import config

ROOT = Path(__file__).parent
STATE = ROOT / "state" / "posted.json"


def api(method, path, **params):
    url = f"{config.GRAPH_API}/{path}"
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path}: {e.code} {e.read().decode()}") from None


def wait_ready(container_id, token):
    for _ in range(60):  # video bisa butuh beberapa menit untuk diproses Instagram
        status = api("GET", container_id, fields="status_code", access_token=token).get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {container_id} status {status}")
        time.sleep(5)
    raise RuntimeError(f"container {container_id} tidak siap setelah 5 menit")


def media_params(url, **extra):
    """Parameter container: .mp4 = video, selain itu gambar."""
    return dict(video_url=url, **extra) if url.endswith(".mp4") else dict(image_url=url, **extra)


def publish(item, user_id, token, base_url):
    urls = [base_url.rstrip("/") + "/output/" + f for f in item["files"]]
    if len(urls) == 1:
        extra = {"media_type": "REELS", "share_to_feed": "true"} if urls[0].endswith(".mp4") else {}
        creation = api("POST", f"{user_id}/media", **media_params(urls[0], caption=item["caption"], access_token=token, **extra))["id"]
    else:
        children = []
        for u in urls:
            extra = {"media_type": "VIDEO"} if u.endswith(".mp4") else {}
            cid = api("POST", f"{user_id}/media", **media_params(u, is_carousel_item="true", access_token=token, **extra))["id"]
            wait_ready(cid, token)
            children.append(cid)
        creation = api("POST", f"{user_id}/media", media_type="CAROUSEL", children=",".join(children),
                       caption=item["caption"], access_token=token)["id"]
    wait_ready(creation, token)
    return api("POST", f"{user_id}/media_publish", creation_id=creation, access_token=token)["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tandai", nargs="+", metavar="ID",
                    help="tandai post sebagai sudah diposting manual (misal: tenang-1-siang), supaya tidak diposting ulang")
    ap.add_argument("--window-hours", type=float, default=6,
                    help="lewati post yang terlambat lebih dari ini (misal setelah workflow mati lama)")
    args = ap.parse_args()

    if args.tandai:
        posted = json.loads(STATE.read_text()) if STATE.exists() else {}
        for pid in args.tandai:
            posted[pid] = {"media_id": "manual", "at": datetime.now(timezone.utc).isoformat()}
            print(f"ditandai sudah diposting: {pid}")
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(posted, indent=2))
        return

    base_url = os.environ.get("IMAGE_BASE_URL") or config.IMAGE_BASE_URL
    schedule = json.loads((ROOT / "output" / "schedule.json").read_text())
    posted = json.loads(STATE.read_text()) if STATE.exists() else {}
    now = datetime.now(timezone.utc)
    failed = False

    for item in schedule:
        due = datetime.fromisoformat(item["waktu"])
        if item["id"] in posted or due > now or now - due > timedelta(hours=args.window_hours):
            continue
        akun = item["akun"].upper()
        token, user_id = os.environ.get(f"IG_TOKEN_{akun}"), os.environ.get(f"IG_USER_ID_{akun}")
        print(f"-> {item['id']} ({item['waktu']}, {len(item['files'])} gambar)")
        if args.dry_run:
            continue
        if not (token and user_id and base_url):
            print(f"   dilewati: IG_TOKEN_{akun} / IG_USER_ID_{akun} / IMAGE_BASE_URL belum diisi")
            continue
        try:
            media_id = publish(item, user_id, token, base_url)
        except RuntimeError as e:
            print(f"   GAGAL: {e}")
            failed = True
            continue
        posted[item["id"]] = {"media_id": media_id, "at": now.isoformat()}
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(posted, indent=2))
        print(f"   terposting, media id {media_id}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
