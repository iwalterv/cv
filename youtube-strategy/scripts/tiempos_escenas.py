"""Calcula cuándo empieza cada escena a partir de los tiempos de Whisper (reemplaza poner los "start" a mano).

Uso: python3 scripts/tiempos_escenas.py videos/<video>/escenas.json
Lee el "text" de cada escena de escenas.json y <video>/palabras.json (whisper.cpp, palabra por palabra;
si no existe, lo genera a partir de <video>/voz.mp3). Escribe <video>/tiempos.json para subtitulos.py y montar_video.py.
Cada corte cae en el silencio antes de la primera palabra de la escena, no encima de ella.
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WHISPER_MODEL = Path.home() / "whisper-models" / "ggml-large-v3-turbo.bin"
LEAD = 0.15     # segundos antes de la primera palabra (si el silencio previo lo permite)
MIN_DUR = 1.2   # duración mínima de una escena

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
scenes = json.loads(config_path.read_text())["scenes"]
words_path = base / "palabras.json"

if not words_path.exists():
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(base / "voz.mp3"),
                        "-ar", "16000", "-ac", "1", str(wav)], check=True)
        subprocess.run(["whisper-cli", "-m", str(WHISPER_MODEL), "-f", str(wav), "-l", "en",
                        "-ml", "1", "-sow", "-oj", "-of", str(words_path.with_suffix("")), "-np"],
                       check=True, capture_output=True)
heard = [(s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip())
         for s in json.loads(words_path.read_text())["transcription"] if s["text"].strip()]


def norm(word):
    return re.sub(r"[^a-z0-9']", "", word.lower())


# Índice de la primera palabra de cada escena dentro del guion completo.
script, first = [], []
for scene in scenes:
    first.append(len(script))
    script += scene["text"].split()

# Para cada palabra del guion, la palabra de Whisper que le corresponde (o la siguiente que sí cuadre).
match = [None] * len(script)
matcher = difflib.SequenceMatcher(a=[norm(w) for w in script], b=[norm(w[2]) for w in heard], autojunk=False)
for tag, a0, a1, b0, b1 in matcher.get_opcodes():
    for k in range(a1 - a0):
        if tag == "equal" or b1 > b0:
            match[a0 + k] = b0 + (k if tag == "equal" else 0)

out = []
for n, (scene, i) in enumerate(zip(scenes, first)):
    j = next(m for m in match[i:] if m is not None)
    word_start = heard[j][0]
    prev_end = heard[j - 1][1] if j else 0.0
    start = 0.0 if n == 0 else max(prev_end, word_start - LEAD)
    item = {"id": scene["id"], "start": round(start, 2), "text": scene["text"]}
    if "meter" in scene:
        item["meter"] = scene["meter"]
    out.append(item)

# Whisper a veces pega la pausa a la palabra siguiente ("Jupiter. [pause] And…"): ninguna escena dura menos de MIN_DUR.
for a, b in zip(out, out[1:]):
    b["start"] = round(max(b["start"], a["start"] + MIN_DUR), 2)

starts = [s["start"] for s in out]
assert starts == sorted(starts), "hay escenas fuera de orden"
(base / "tiempos.json").write_text(json.dumps({"audio": "voz.mp3", "tail": 1.5, "scenes": out},
                                              indent=1, ensure_ascii=False) + "\n")
durs = [b - a for a, b in zip(starts, starts[1:])]
print(f"ok  {len(out)} escenas  duración media {sum(durs) / len(durs):.1f} s  "
      f"(mín. {min(durs):.1f} s, máx. {max(durs):.1f} s)")
