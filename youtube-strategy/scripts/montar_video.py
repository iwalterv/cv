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

def meter_filters():
    """"Survival Meter": barra en la esquina superior derecha. Una escena con "meter" cambia el valor
    (número de 0 a 100, negativo, "≈50" o "WAGES") y se mantiene hasta el siguiente cambio.
    También puede ser un objeto {"value", "label", "note", "blink"} para cambiar los textos del panel
    o forzar el parpadeo rojo (por defecto parpadea solo con valores <= 1)."""
    changes = [(starts[i], s["meter"] if isinstance(s["meter"], dict) else {"value": str(s["meter"])})
               for i, s in enumerate(scenes) if "meter" in s]
    if not changes:
        return ""
    x0, y0, bw = W - 470, 40, 400            # panel
    bx, by, bh = x0 + 15, y0 + 58, 34        # barra
    f = [f"drawbox=x={x0}:y={y0}:w={bw + 30}:h=150:color=black@0.55:t=fill:enable='gte(t,{changes[0][0]})'"]
    prev = 100.0
    for k, (a, m) in enumerate(changes):
        value = str(m["value"])
        b = changes[k + 1][0] if k + 1 < len(changes) else total + 1
        on = f"between(t,{a:.2f},{b:.2f})"
        if value == "WAGES":
            label, shown, pct, color, note = "IF YOU SURVIVED", "", 100.0, "0x3FA34D", "wages went UP"
        else:
            num = float(value.lstrip("≈~"))
            label, color = m.get("label", "YOUR ODDS"), "0xD62828"
            shown = ("~" if value[0] in "≈~" else "") + f"{num:g}%"
            pct = max(num, 0.0)
            note = m.get("note", "not helping" if num < 0 else "rough odds, for fun")
        font = "fontfile='/System/Library/Fonts/Supplemental/Arial Black.ttf'"
        f += [
            f"drawtext={font}:text='{label}':expansion=none:fontsize=30:fontcolor=white:x={bx}:y={y0 + 14}:enable='{on}'",
            f"drawbox=x={bx}:y={by}:w={bw}:h={bh}:color=white:t=4:enable='{on}'",
            f"drawtext={font}:text='{note}':expansion=none:fontsize=20:fontcolor=white@0.85:x={bx}:y={by + bh + 12}:enable='{on}'",
        ]
        if shown:
            f.append(f"drawtext={font}:text='{shown}':expansion=none:fontsize=30:fontcolor=white:"
                     f"x={bx + bw}-tw:y={y0 + 14}:enable='{on}'")
        # El relleno pasa del valor anterior al nuevo en 6 pasos de 0,1 s (drawbox no anima el ancho con t).
        for step in range(1, 7):
            w = round((bw - 8) * (prev + (pct - prev) * step / 6) / 100)
            s0 = a + (step - 1) * 0.1
            s1 = a + step * 0.1 if step < 6 else b
            if w > 0:
                f.append(f"drawbox=x={bx + 4}:y={by + 4}:w={w}:h={bh - 8}:color={color}:t=fill:"
                         f"enable='between(t,{s0:.2f},{s1:.2f})'")
        if m.get("blink", value != "WAGES" and float(value.lstrip("≈~")) <= 1):
            # Valores críticos: el panel parpadea en rojo durante 2 s.
            f.append(f"drawbox=x={x0}:y={y0}:w={bw + 30}:h=150:color=0xD62828@0.45:t=fill:"
                     f"enable='between(t,{a:.2f},{a + 2:.2f})*lt(mod((t-{a:.2f})*4\\,2)\\,1)'")
        prev = pct
    return "," + ",".join(f)


subs = base / "subtitulos.ass"
burn = f",ass=filename='{subs}'" if subs.exists() else ""
filters.append(f"{''.join(labels)}concat=n={len(scenes)}:v=1:a=0{meter_filters()}{burn},format=yuv420p[v]")
filters.append(f"[{len(scenes)}:a]apad=whole_dur={total:.3f}[a]")

out = base / "video.mp4"
cmd = [FFMPEG, "-y", "-loglevel", "error", *inputs, "-i", str(audio),
       "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
print(f"ok  {out}  ({total:.1f} s, {len(scenes)} escenas, subtítulos: {'sí' if burn else 'no'})")
