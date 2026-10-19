"""Añade música de fondo al video ya montado: normaliza la voz y mete la música por debajo, bajándola cuando hay voz.

Uso: python3 scripts/musica.py videos/<video>/tiempos.json
Lee <video>/musica.json: [{"from": "<id de escena>", "track": "<archivo en musica/>"}, ...] o, para cambiar el
volumen de la música, {"music_lufs": -22, "plan": [...]}; cada tramo dura
hasta el siguiente (el último, hasta el final del video). Las pistas se repiten en bucle si el tramo es más largo.
Reemplaza la pista de audio de <video>/video.mp4 sin volver a codificar la imagen (correr después de montar_video.py).
La voz sale de <video>/voz.mp3, así que se puede volver a correr sin acumular música.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

VOICE_LUFS = -14.0   # nivel al que YouTube normaliza
MUSIC_LUFS = -25.0   # música en las pausas; debajo de la voz baja unos dB más (sidechain)
XFADE = 2.0          # segundos de fundido entre tramos
MUSIC_DIR = Path(__file__).resolve().parent.parent / "musica"

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
config = json.loads(config_path.read_text())
starts = {s["id"]: s["start"] for s in config["scenes"]}
video = base / "video.mp4"
voice = base / config["audio"]


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout)


def lufs(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])


total = duration(video)
plan = json.loads((base / "musica.json").read_text())
if isinstance(plan, dict):
    MUSIC_LUFS, plan = plan.get("music_lufs", MUSIC_LUFS), plan["plan"]
bounds = [starts[p["from"]] for p in plan] + [total]

inputs = ["-i", str(voice)]
filters = [f"[0:a]volume={VOICE_LUFS - lufs(voice):.2f}dB,aresample=48000,asplit=2[voz][llave]"]
parts = []
for k, p in enumerate(plan):
    track = MUSIC_DIR / p["track"]
    a, b = bounds[k], bounds[k + 1]
    # Cada tramo empieza y termina medio fundido antes/después del corte, para que se crucen.
    a0 = max(a - XFADE / 2, 0)
    b0 = min(b + XFADE / 2, total)
    inputs += ["-stream_loop", "-1", "-i", str(track)]
    filters.append(
        f"[{k + 1}:a]aresample=48000,volume={MUSIC_LUFS - lufs(track):.2f}dB,atrim=0:{b0 - a0:.3f},"
        f"afade=t=in:d={XFADE if k else 0.5}:curve=tri,afade=t=out:st={b0 - a0 - XFADE:.3f}:d={XFADE}:curve=tri,"
        f"adelay={a0 * 1000:.0f}:all=1[m{k}]")
    parts.append(f"[m{k}]")
filters += [
    f"{''.join(parts)}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total:.3f}[musica]",
    "[musica][llave]sidechaincompress=threshold=0.05:ratio=2.5:attack=80:release=600[bajo]",
    "[voz][bajo]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.89:level=false[a]",
]

out = base / "video-musica.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", str(video),
                "-filter_complex", ";".join(filters), "-map", f"{len(plan) + 1}:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-t", f"{total:.3f}", "-movflags", "+faststart", str(out)], check=True)
out.replace(video)
print(f"ok  {video}  ({len(plan)} tramos de música, voz {lufs(voice):.1f} → {VOICE_LUFS} LUFS)")
