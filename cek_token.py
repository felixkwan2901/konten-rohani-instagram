"""Cek token Instagram tanpa menampilkannya. Token diketik tersembunyi (tidak terlihat di layar).

  python3 cek_token.py

Hasilnya: username + Instagram user ID (aman untuk dibagikan), izin token, dan apakah akun bisa posting.
"""
import getpass
import json
import urllib.error
import urllib.request

import config


def get(path, token, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{config.GRAPH_API}/{path}?{q}&access_token={token}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": json.loads(e.read() or b"{}").get("error", {})}


if __name__ == "__main__":
    token = getpass.getpass("Tempel access token (tidak akan terlihat), lalu Enter: ").strip()
    me = get("me", token, fields="user_id,username,account_type")
    if "error" in me:
        print("\n❌ Token tidak valid:", me["error"].get("message", me["error"]))
        raise SystemExit(1)
    print(f"\n✅ Token valid untuk @{me.get('username')}")
    print(f"   Instagram user ID : {me.get('user_id')}   <- ini yang dipakai sebagai IG_USER_ID_...")
    print(f"   Jenis akun        : {me.get('account_type')}  (harus BUSINESS atau MEDIA_CREATOR)")
    limit = get(f"{me.get('user_id')}/content_publishing_limit", token, fields="quota_usage,config")
    if "error" in limit:
        print("⚠️  Belum bisa cek izin posting:", limit["error"].get("message"))
        print("   Pastikan izin instagram_business_content_publish dicentang saat membuat token.")
    else:
        data = (limit.get("data") or [{}])[0]
        print(f"✅ Izin posting aktif. Kuota terpakai 24 jam terakhir: {data.get('quota_usage', 0)}")
