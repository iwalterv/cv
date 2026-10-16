"""Pone el texto a las miniaturas: imagenes/<id>.png → <id>.jpg (1280×720), con libass de ffmpeg-full.

Uso: python3 scripts/texto_miniaturas.py videos/<video>/miniaturas/escenas.json [id ...]
Campos de cada escena en escenas.json:
  "text"   texto (un "?" o "!" final sale en rojo, como en la identidad del canal)
  "color"  "yellow" (por defecto) o "white"
  "size"   tamaño de letra (por defecto se ajusta al largo del texto)
  "zoom"   acercamiento recortando desde abajo, para comer franjas vacías arriba (por defecto 1)
  "align"  "top" (centrado arriba, por defecto) o "left" (arriba a la izquierda)
Sin "text" se salta la escena.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FFMPEG = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
COLORS = {"yellow": "&H0000D4FF&", "white": "&H00FFFFFF&"}   # ASS: BGR
RED = "&H002828D6&"                                          # #D62828

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
only = set(sys.argv[2:])
for s in json.loads(config_path.read_text())["scenes"]:
    if "text" not in s or (only and s["id"] not in only):
        continue
    text = s["text"]
    tail = ""
    if text[-1] in "?!":
        text, tail = text[:-1], f"{{\\c{RED}}}{text[-1]}"
    size = s.get("size", min(170, int(1180 / (len(s["text"]) * 0.66))))
    align, margin_l = (7, 45) if s.get("align") == "left" else (8, 20)
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Arial Black,{size},{COLORS[s.get('color', 'yellow')]},&H00FFFFFF&,&H00000000&,&H99000000&,0,0,0,0,100,100,0,0,1,11,7,{align},{margin_l},20,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,T,,0,0,0,,{text}{tail}
"""
    zoom = s.get("zoom", 1)
    with tempfile.NamedTemporaryFile("w", suffix=".ass", delete=False) as f:
        f.write(ass)
    vf = (f"scale={round(1280 * zoom)}:{round(720 * zoom)}:force_original_aspect_ratio=increase,"
          f"crop=1280:720:(iw-1280)/2:ih-720,ass=filename='{f.name}'")
    out = base / f"{s['id']}.jpg"
    subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", str(base / "imagenes" / f"{s['id']}.png"),
                    "-vf", vf, "-frames:v", "1", "-q:v", "2", str(out)], check=True)
    Path(f.name).unlink()
    print(f"ok  {out.name}  «{s['text']}»")
