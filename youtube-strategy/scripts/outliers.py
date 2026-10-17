"""Busca videos "outlier" en canales del nicho: los que superan con creces la mediana de vistas de su propio canal.

Uso: python3 scripts/outliers.py datos/<carpeta> [N]
Lee <carpeta>/canales.txt (líneas "nombre|url", # = comentario), baja con yt-dlp SOLO metadatos de los últimos N
videos de cada canal (por defecto 150; fechas aproximadas) y escribe:
  <carpeta>/canales/<nombre>.tsv   id, vistas, fecha, duración (s), título
  <carpeta>/outliers.tsv           los de los últimos 12 meses, ordenados por veces la mediana del canal
"""
import concurrent.futures as cf
import datetime as dt
import json
import statistics
import subprocess
import sys
from pathlib import Path

base = Path(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 150
out_dir = base / "canales"
out_dir.mkdir(parents=True, exist_ok=True)
channels = [l.split("|", 1) for l in (base / "canales.txt").read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def fetch(name, url):
    p = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(n), "--extractor-args",
                        "youtubetab:approximate_date", "-j", url.rstrip("/") + "/videos"],
                       capture_output=True, text=True)
    rows = []
    for line in p.stdout.splitlines():
        d = json.loads(line)
        rows.append((d["id"], d.get("view_count") or "", d.get("upload_date") or "", d.get("duration") or "",
                     d.get("title", "").replace("\t", " ")))
    (out_dir / f"{name}.tsv").write_text("".join("\t".join(map(str, r)) + "\n" for r in rows))
    return name, len(rows)


with cf.ThreadPoolExecutor(6) as ex:
    for name, count in ex.map(lambda c: fetch(*c), channels):
        print(f"{name:28} {count} videos")

cutoff = (dt.date.today() - dt.timedelta(days=365)).strftime("%Y%m%d")
today = dt.date.today()
res = []
for f in sorted(out_dir.glob("*.tsv")):
    vids = [r.split("\t") for r in f.read_text().splitlines()]
    vids = [v for v in vids if v[1] and v[2] and (not v[3] or float(v[3]) >= 180)]  # sin Shorts
    if len(vids) < 8:
        continue
    med = statistics.median(int(v[1]) for v in vids)
    for vid, views, date, dur, title in vids:
        if date < cutoff:
            continue
        age = max((today - dt.datetime.strptime(date, "%Y%m%d").date()).days, 1)
        res.append((int(views) / max(med, 1), f.stem, int(views), int(med), date, round(int(views) / age), vid, title))
res.sort(reverse=True)
(base / "outliers.tsv").write_text("veces_mediana\tcanal\tvistas\tmediana_canal\tfecha\tvistas_dia\tid\ttitulo\n" +
                                   "".join("\t".join(map(str, (round(r[0], 1), *r[1:]))) + "\n" for r in res))
print(f"ok  {len(res)} videos de los últimos 12 meses → {base / 'outliers.tsv'}")
