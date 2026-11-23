#!/usr/bin/env python3
"""Instagram API (Instagram Login) ile carousel / reel paylaşır.
Kullanım: python3 paylas.py carousel "caption" URL1 URL2 ...
          python3 paylas.py reel "caption" VIDEO_URL
"""
import os, sys, time, json, urllib.request, urllib.parse
API = "https://graph.facebook.com/v23.0"
IG_USER_ID = os.environ.get("IG_USER_ID", "17841447106643546")  # facetatelierstudio
TOKEN = os.environ.get("IG_TOKEN")  # yoksa ağ sırrı (Authorization: Bearer) kullanılır
API = os.environ.get("IG_API", API)

def call(method, path, **params):
    if TOKEN: params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def bekle(cid):
    for _ in range(60):
        s = call("GET", cid, fields="status_code").get("status_code")
        if s == "FINISHED": return
        if s in ("ERROR", "EXPIRED"): raise SystemExit(f"konteyner {cid}: {s}")
        time.sleep(10)
    raise SystemExit("zaman aşımı")

def main():
    tur, caption, *urls = sys.argv[1:]
    uid = IG_USER_ID
    if tur == "carousel":
        kids = [call("POST", f"{uid}/media", image_url=u, is_carousel_item="true")["id"] for u in urls]
        for k in kids: bekle(k)
        cid = call("POST", f"{uid}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
    else:
        cid = call("POST", f"{uid}/media", media_type="REELS", video_url=urls[0], caption=caption, share_to_feed="true")["id"]
    bekle(cid)
    print(json.dumps(call("POST", f"{uid}/media_publish", creation_id=cid)))

if __name__ == "__main__":
    main()
