#!/usr/bin/env python3
"""Kuyruktaki zamanı gelmiş gönderileri paylaşır ve kuyruk.json'u günceller.
Ağ sırrı (Authorization: Bearer) graph.facebook.com isteklerine eklenir.
"""
import json, subprocess, sys, datetime, zoneinfo, pathlib
KOK = pathlib.Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/facetatelierstudio/facet-instagram/yayin/"
bugun = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Istanbul")).date().isoformat()
q = json.load(open(KOK / "kuyruk.json"))
sonuc = []
for g in q:
    if g["durum"] != "bekliyor" or g["tarih"] > bugun:
        continue
    if "--kuru" in sys.argv:
        print("PAYLAŞILACAK:", g["tarih"], g["tur"], g["dosyalar"]); continue
    r = subprocess.run([sys.executable, str(KOK / "arac/paylas.py"), g["tur"], g["caption"],
                        *[RAW + f for f in g["dosyalar"]]], capture_output=True, text=True)
    if r.returncode == 0:
        g["durum"] = "paylasildi"; g["sonuc"] = r.stdout.strip()
    else:
        g["hata"] = (r.stdout + r.stderr)[-800:]
    sonuc.append((g["tarih"], g["durum"], g.get("hata", "")))
json.dump(q, open(KOK / "kuyruk.json", "w"), ensure_ascii=False, indent=2)
for s in sonuc: print(*s)
