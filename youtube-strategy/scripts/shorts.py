"""Saca Shorts verticales (1080×1920) de un video largo ya montado, sin gastar créditos.

Uso: python3 scripts/shorts.py videos/<video>/shorts.json [id]
Lee <video>/tiempos.json y <video>/video.mp4 (con voz, música, subtítulos y medidor ya quemados).
Cada Short junta uno o más tramos de escenas ("ranges": [["053", "063"], ...]; cada tramo va desde el
inicio de la primera escena hasta el inicio de la que sigue a la última).
Composición: el video 16:9 a todo el ancho en el centro, el mismo video desenfocado de fondo,
el título arriba (palabras entre {llaves} en rojo) y una línea pequeña abajo.
Escribe <video>/shorts/<id>.mp4.
"""
import json
import subprocess
import sys
from pathlib import Path

FFMPEG_FULL = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")  # libass para el título
FFMPEG = str(FFMPEG_FULL) if FFMPEG_FULL.exists() else "ffmpeg"
W, H = 1080, 1920
FRAME_H = 608  # 1920×1080 escalado a 1080 de ancho
FRAME_Y = 640  # posición vertical del video dentro del Short

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
config = json.loads(config_path.read_text())
only = sys.argv[2] if len(sys.argv) > 2 else None
tiempos = json.loads((base / "tiempos.json").read_text())
video = base / config.get("video", "video.mp4")
total = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
    capture_output=True, text=True, check=True).stdout)
ids = [s["id"] for s in tiempos["scenes"]]
starts = [s["start"] for s in tiempos["scenes"]] + [total]
out_dir = base / "shorts"
out_dir.mkdir(exist_ok=True)


def span(first, last):
    return starts[ids.index(first)], starts[ids.index(last) + 1]


def ass_title(lines, footer):
    red = lambda t: t.replace("{", "\x00").replace("}", r"{\c&HFFFFFF&}").replace("\x00", r"{\c&H2828D6&}")
    title = r"\N".join(red(l) for l in lines)
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Arial Black,96,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H80000000&,0,0,0,0,100,100,1,0,1,8,4,8,50,50,260,1
Style: Footer,Arial Black,46,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H80000000&,0,0,0,0,100,100,1,0,1,5,2,2,50,50,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,9:59:59.00,Title,,0,0,0,,{title}
Dialogue: 0,0:00:00.00,9:59:59.00,Footer,,0,0,0,,{footer}
"""


for short in config["shorts"]:
    if only and short["id"] != only:
        continue
    spans = [span(a, b) for a, b in short["ranges"]]
    ass = out_dir / f"{short['id']}.ass"
    ass.write_text(ass_title(short["title"], short.get("footer", "Full video on the channel")))
    f = []
    for i, (a, b) in enumerate(spans):
        f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}]")
    n = len(spans)
    f.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    f.append("[v]split[fg][bg]")
    f.append(f"[bg]scale=-2:{H},crop={W}:{H},boxblur=30:3,eq=brightness=-0.25[bgb]")
    f.append(f"[fg]scale={W}:{FRAME_H}[fgs]")
    f.append(f"[bgb][fgs]overlay=0:{FRAME_Y},subtitles='{ass}'[out]")
    dest = out_dir / f"{short['id']}.mp4"
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(video), "-filter_complex", ";".join(f),
                    "-map", "[out]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dest)], check=True)
    dur = sum(b - a for a, b in spans)
    print(f"{dest.name}  {dur:.1f} s")
