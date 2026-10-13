"""Download every source in data/source_manifest.csv that is a direct file link.

Run this on a machine whose network can reach the publishers (the cloud sandbox
used to build this branch could not). Page links (Inside Airbnb, NTTO, LVCVA
report pages) are listed for manual download.
"""
from pathlib import Path
import csv, urllib.request

ROOT = Path(__file__).resolve().parents[1]
DIRECT = (".pdf", ".zip", ".csv")

with open(ROOT / "data/source_manifest.csv", newline="") as f:
    for row in csv.DictReader(f):
        url, target = row["url"], ROOT / "data" / row["save_as"]
        if not url.split("?")[0].lower().endswith(DIRECT) and "fredgraph.csv" not in url:
            print(f"[manual] {row['id']}: open {url}")
            continue
        if target.exists():
            print(f"[skip]   {row['id']}: {target.relative_to(ROOT)} exists")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (student research)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                target.write_bytes(r.read())
            print(f"[ok]     {row['id']}: {target.relative_to(ROOT)}")
        except Exception as e:  # keep going; report what failed
            print(f"[fail]   {row['id']}: {e}")
