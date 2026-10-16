# Piloto #1: Why You Wouldn't Survive the Black Death

| Archivo | Qué es |
|---|---|
| `guion.md` | Guion v2 con tabla de verificación de datos (todos ✅) |
| `analisis-viral.md` | Análisis de retención/CTR y plan de lanzamiento |
| `narracion.txt` | Texto exacto que se pegó en ElevenLabs (con etiquetas `[pause]`, `[sarcastic]`, `[whispers]`) |
| `voz.mp3` | Holden – Warm Midwest Narrator, Eleven v4, toma 1 de 2 (10:38; ~9.900 créditos). Se eligió por coincidir 99 % con el guion en Whisper |
| `escenas.py` → `escenas.json` | 137 escenas: texto narrado exacto + prompt + medidor. `escenas.py` comprueba que los textos cubren toda la narración |
| `palabras.json` | Tiempos palabra por palabra (whisper.cpp) |
| `tiempos.json` | Inicio de cada escena, calculado con `scripts/tiempos_escenas.py` |
| `subtitulos.ass` / `.srt` | Quemados en el video / para subir a YouTube |
| `miniaturas/` | 3 miniaturas para Test & Compare (Nano Banana Pro + texto con ASS) |
| `publicacion.md` | Título, descripción con capítulos y fuentes, etiquetas, comentario fijado y configuración |
| `video.mp4` | El video final (no se sube a git) |

## Cómo se rehace
```bash
python3 videos/piloto-black-death/escenas.py                               # escenas.json
python3 scripts/generar_escenas.py videos/piloto-black-death/escenas.json  # imágenes (Seedream, 0,5 créditos c/u)
python3 scripts/tiempos_escenas.py videos/piloto-black-death/escenas.json  # tiempos.json (Whisper)
python3 scripts/subtitulos.py videos/piloto-black-death/tiempos.json       # subtítulos
python3 scripts/montar_video.py videos/piloto-black-death/tiempos.json     # video.mp4 con Survival Meter
```

## Survival Meter
Una escena con `"meter"` cambia el valor y se mantiene hasta el siguiente cambio: `100` (aparece en "Welcome to England"), `50` (llega la peste y vuelve en el "coin flip"), `1` (neumónica, parpadea), `-10` (sangría, "not helping"), `≈50` ("Statistically… so are you") y `WAGES` (barra verde "IF YOU SURVIVED / wages went UP").

## Costos
- ElevenLabs: ~9.900 de los ~37.700 créditos del mes.
- Higgsfield: 137 escenas × 0,5 + 3 de prueba + 3 miniaturas × 2 ≈ 76 créditos.
