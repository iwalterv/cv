"""Hojas de contactos de las escenas, para revisarlas antes de montar (ver la lección del piloto en CLAUDE.md).

Uso: python3 scripts/hoja_contactos.py videos/<video> <carpeta de salida> [desde] [hasta]
Junta imagenes/<id>.png de 20 en 20 (4×5, con el número de escena) y escribe <salida>/hoja-<primera>.jpg.
"""
import subprocess
import sys
from pathlib import Path

FFMPEG_FULL = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")  # drawtext no viene en el ffmpeg normal
FFMPEG = str(FFMPEG_FULL) if FFMPEG_FULL.exists() else "ffmpeg"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

base, out = Path(sys.argv[1]), Path(sys.argv[2])
lo = sys.argv[3] if len(sys.argv) > 3 else "000"
hi = sys.argv[4] if len(sys.argv) > 4 else "999"
out.mkdir(parents=True, exist_ok=True)
images = sorted(p for p in (base / "imagenes").glob("*.png") if lo <= p.stem <= hi)

for k in range(0, len(images), 20):
    chunk = images[k:k + 20]
    inputs, f = [], []
    for i, p in enumerate(chunk):
        inputs += ["-i", str(p)]
        f.append(f"[{i}:v]scale=480:270,drawtext=fontfile='{FONT}':text='{p.stem}':fontsize=30:fontcolor=yellow:"
                 f"box=1:boxcolor=black@0.6:x=8:y=8[v{i}]")
    # Rellena con negro hasta 20 para que la rejilla siempre sea 4×5.
    for i in range(len(chunk), 20):
        f.append(f"color=black:s=480x270:d=1[v{i}]")
    layout = "|".join(f"{(i % 4) * 480}_{(i // 4) * 270}" for i in range(20))
    f.append("".join(f"[v{i}]" for i in range(20)) + f"xstack=inputs=20:layout={layout}")
    dest = out / f"hoja-{chunk[0].stem}.jpg"
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(f),
                    "-frames:v", "1", "-q:v", "3", str(dest)], check=True)
    print(dest)
