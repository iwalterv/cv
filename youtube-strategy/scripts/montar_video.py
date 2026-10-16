"""Arma un video a partir del audio, las imágenes por escena y la tabla de tiempos (reemplaza el montaje en CapCut).

Uso: python3 scripts/montar_video.py videos/<video>/tiempos.json
Lee <video>/tiempos.json, <video>/<audio> y <video>/imagenes/<id>.png; escribe <video>/video.mp4.
Cada escena dura desde su "start" hasta el "start" de la siguiente (la última, hasta el final del audio + "tail").
Efecto: zoom lento (Ken Burns), alternando acercar y alejar, con fundido corto entre escenas.
Si existe <video>/subtitulos.ass (scripts/subtitulos.py), los quema en el video (requiere ffmpeg-full, con libass).
"""
import json
import subprocess
import sys
from pathlib import Path

FPS = 30
W, H = 1920, 1080
ZOOM = 0.08  # 8 % de zoom a lo largo de cada escena
FADE = 0.3   # segundos de fundido entre escenas
# El ffmpeg normal de Homebrew no trae libass; ffmpeg-full sí.
FFMPEG_FULL = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")
FFMPEG = str(FFMPEG_FULL) if FFMPEG_FULL.exists() else "ffmpeg"

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
config = json.loads(config_path.read_text())
audio = base / config["audio"]

audio_len = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)],
    capture_output=True, text=True, check=True).stdout)
total = audio_len + config.get("tail", 0)

scenes = config["scenes"]
starts = [s["start"] for s in scenes] + [total]

inputs, filters, labels = [], [], []
for i, scene in enumerate(scenes):
    dur = starts[i + 1] - starts[i]
    frames = round(dur * FPS)
    # Una sola imagen de entrada: zoompan genera los `frames` fotogramas de la escena.
    inputs += ["-i", str(base / "imagenes" / f"{scene['id']}.png")]
    # Alterna acercar / alejar para dar variedad.
    zoom = f"1+{ZOOM}*on/{frames}" if i % 2 == 0 else f"{1 + ZOOM}-{ZOOM}*on/{frames}"
    fade_in = "" if i == 0 else f",fade=t=in:st=0:d={FADE}"
    filters.append(
        f"[{i}:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
        f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}"
        f"{fade_in},setsar=1[v{i}]")
    labels.append(f"[v{i}]")

subs = base / "subtitulos.ass"
burn = f",ass=filename='{subs}'" if subs.exists() else ""
filters.append(f"{''.join(labels)}concat=n={len(scenes)}:v=1:a=0{burn},format=yuv420p[v]")
filters.append(f"[{len(scenes)}:a]apad=whole_dur={total:.3f}[a]")

out = base / "video.mp4"
cmd = [FFMPEG, "-y", "-loglevel", "error", *inputs, "-i", str(audio),
       "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
print(f"ok  {out}  ({total:.1f} s, {len(scenes)} escenas, subtítulos: {'sí' if burn else 'no'})")
