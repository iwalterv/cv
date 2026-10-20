# Proyecto: canal de YouTube "faceless" monetizado

Este archivo es el traspaso de contexto para las sesiones de Claude Code en la Mac del usuario. **Léelo completo antes de actuar.**

## Reglas de trabajo (obligatorias)
1. **Habla siempre en español** con el usuario. El contenido del canal (guiones, títulos, prompts) va en **inglés**.
2. **Pide autorización explícita ANTES de:**
   - **cualquier gasto de dinero**: suscripciones, créditos, compras, planes de pago o pruebas gratuitas que pidan tarjeta;
   - crear cuentas o enviar formularios con datos personales;
   - **publicar** cualquier cosa en YouTube o cambiar la configuración del canal;
   - cualquier acción irreversible o visible para terceros.
3. **Nunca** ingreses datos fiscales (W-9, SSN), bancarios ni contraseñas: eso lo hace el usuario personalmente. Guíalo paso a paso.
4. **Trabajamos un paso a la vez** (ver la ruta). No avances al siguiente sin cumplir el "Listo cuando" del actual.
5. Guarda resultados y documentos en `youtube-strategy/`. Haz commit y push a la rama **`claude/keen-keller-gg19xu`** al terminar cada tarea.
6. **Políticas de YouTube** (para no perder la monetización): guiones **originales** (de los competidores solo se toman temas, nunca el texto), datos verificados con fuente, variedad entre videos, revisión humana antes de publicar, y entre 2 y 4 videos largos por semana como máximo.
7. **Herramientas:** `yt-dlp` (solo metadatos y miniaturas, nada de descargar videos completos) y `ffmpeg`. Para webs (YouTube Studio, ElevenLabs, Higgsfield), usa Claude in Chrome si está conectado. Si no, guía al usuario con instrucciones claras.

## Situación del usuario
- Es **ciudadano estadounidense** y vive temporalmente en Guatemala. Tiene una conexión (bridge) a la red de la casa de su papá en **Virginia**.
- **Cuenta:** creador de EE. UU., con **W-9**, dirección de AdSense en Virginia, cuenta bancaria en EE. UU. y país del canal **United States**. El canal se administra de forma consistente desde la red de Virginia.
- **Objetivo:** monetizar (YPP: 1.000 suscriptores + 4.000 horas de reproducción) lo antes posible.

## Decisiones ya tomadas
| Tema | Decisión | Documento |
|---|---|---|
| Estrategia base | Sistema del video de "Leo": guion → voz IA → timestamps → imágenes IA por escena → montaje | `02-analisis-estrategia.md` |
| Idioma | **Inglés**, público de EE. UU. El español irá después como pista de audio doblada en el mismo canal | `04-analisis-nichos.md` |
| Nicho | **"La vida humana a través de la historia, vivida desde TU perspectiva"**, con monigotes, rotando épocas (Edad Media, Roma, vikingos, Egipto, aztecas, Edad de Hielo…). El nicho de dinero/salarios quedó **descartado** por los datos | `05-decision-nicho.md` |
| Formatos de título | "What Did [X] Do When…?", "Why You Wouldn't Survive…", "Why It Sucked to Be a…", "Your Life as a…", "The Worst Jobs in…" | `05-decision-nicho.md` |
| Identidad | Nombre **Time Peasant** (@timepeasant, verificado libre el 13-oct-2026; "Yesteryou" descartado porque ya existe en el nicho). Voz **Holden** (ElevenLabs). Personaje **"Red"** (confirmado): monigote de cabeza redonda con **bufanda roja siempre**; escenas ilustradas a color; texto de miniatura blanco con la palabra clave en rojo | `06-identidad-canal.md` |
| Banco de ideas | 30 títulos priorizados con datos (A/B/C) | `07-banco-ideas.md` |
| Datos de investigación | Búsquedas, canales de referencia, miniaturas y fotogramas | `datos/` |

Canales de referencia: **Ink Explainer**, **Zenn**, **StickTory**, **Serious History**, **Chat History**.

## Plan de producción (aprobado por el usuario el 19-oct-2026)
- Piloto a las 24 h: 1,3K impresiones, CTR 0,9 %, 28 vistas, ~2:35 de media (tráfico de sugeridos ajenos al nicho). El usuario quiere publicar más seguido ("uno diario"); se acordó:
  - **3 videos largos por semana** (mar, jue, sáb, 12:00 p. m. ET). No uno diario: riesgo de "contenido producido en masa" en la revisión del YPP (regla 6).
  - **1 Short al día**, sacado de los videos largos con `scripts/shorts.py` (sin créditos). Textos en `videos/<v>/shorts.md`.
  - Miniaturas más claras (las ganadoras del nicho usan fondo claro; las del piloto son oscuras).
- Para eso hacen falta mejoras de plan **que compra el usuario**: Higgsfield **Plus** ($59, 1.200 créditos) y ElevenLabs **Creator** ($22, 121K caracteres). Ideal: API key de ElevenLabs en `ELEVENLABS_API_KEY` (la crea el usuario).
- Foto de perfil: 2 opciones en `imagenes/canal/` (recomendada B-shock); falta que el usuario elija y haga el clic de "Publicar".

**Plan revisado APROBADO por el usuario el 20-oct-2026 (`08-investigacion-crecimiento.md`; reemplaza lo de arriba sobre la frecuencia y los Shorts):** 1-2 videos largos por semana con más trabajo por video, 1-2 Shorts por semana, títulos de curiosidad sobre la vida diaria medieval ("What Did Medieval Peasants Do…?"), empaque antes del guion y retención a los 30 s ≥ 65 %. Evidencia: Zenn, Ink y Axen llegaron a millones en 6 meses con ~1 video por semana y sin Shorts; Unlucky Ancestors, con nuestro formato "Why You Wouldn't Survive", tiene 0-14 vistas por video.

**Video #2** "Why You Wouldn't Survive a Medieval Winter": programado para el **lunes 19-oct-2026, 8:00 p. m. ET**, https://youtu.be/Nv6Ok5RoGPQ. A las 13 h: 9 impresiones y 0 vistas (prueba mínima, por el CTR del 0,8 % del piloto). El 20-oct se hicieron miniaturas v2 claras y minimalistas para los dos videos (`miniaturas/escenas-v2.json`), y el usuario reinicia los tests. Ojo: en youtube.com, Chrome tiene la sesión en otra cuenta (@MatrixExodus); para comentar como Time Peasant hay que cambiar de cuenta. Falta el comentario fijado. **Video #3 "What Did Medieval Peasants Do at Night?"** MONTADO el 20-oct (`videos/03-medieval-night/`, 6:44, 118 escenas, voz toma 1). Copia en `~/Desktop/time-peasant-video3/`. PROGRAMADO para el **mar 20-oct, 2:00 p. m. ET**: https://youtu.be/0fCXeUODtj8 (falta el comentario fijado). Short `n1-3am` programado para las 2:15 p. m. ET (falta el "Related video"). Playlist pública **"Medieval Life, From YOUR Perspective"** (Studio: /playlist/PLR5tWYiZTHCk) con los 3 videos largos. Higgsfield quedó en **0 créditos**: para el #4 hace falta el plan Plus. Análisis del #3 en `datos/video3/README.md`: recomendado "What Did Medieval Peasants Do at Night?", después comida (#4) y diversión (#5). Falta que el usuario elija el tema.

## Estado actual: PASO 5 (video piloto), PUBLICADO
**Piloto PUBLICADO el sábado 17-oct-2026 a las 10:42 a. m. ET** (el usuario pidió publicarlo antes de la hora programada, 12:00 ET): https://youtu.be/p6_vH7gbbng (ID `p6_vH7gbbng`). Test & Compare con 3 miniaturas (D principal, F, B); arranca al hacerse público. Subtítulos, pantalla final (suscribirse + "Best for viewer"), etiquetas, Education, sin promoción pagada, uso de IA realista: No. Copyright y normas: sin problemas.
Comentario fijado el 17-oct. **Pendiente:** revisar a las 24-48 h el CTR y la retención, y medir el tiempo de producción.
Paso 4 cerrado el 15-oct-2026: banco en `07-banco-ideas.md` (datos en `datos/paso4/`). El usuario eligió el piloto **"Why You Wouldn't Survive the Black Death"**.
Piloto en `videos/piloto-black-death/` (ver su `README.md`): guion v2 con todos los datos verificados, voz Holden (10:38), 137 escenas, Survival Meter, subtítulos, 3 miniaturas y `publicacion.md`. Copia en `~/Desktop/time-peasant-piloto/`.
Siguiente: el usuario revisa el video completo → ajustes → **publicar solo con su autorización** (él hace los clics finales en YouTube Studio) → medir el tiempo de producción.
Lección: revisar SIEMPRE la hoja de contactos de las escenas antes de montar (los flagelantes salieron con capuchas puntiagudas blancas, que parecían del KKK; se regeneraron).

Paso 3 cerrado el 15-oct-2026 (detalle en `pasos/paso-03-cuentas.md`):
- Canal **Time Peasant** (@TimePeasant), ID `UCgMVaxgxckffeHQt9SDR5ZA` (Studio: https://studio.youtube.com/channel/UCgMVaxgxckffeHQt9SDR5ZA): cuenta de marca en el Gmail personal del usuario, país United States, verificado por teléfono, 2FA activa. El usuario tiene otro canal, "FactoMentes", que no se toca: en Studio hay que asegurarse de estar en Time Peasant.
- **ElevenLabs Starter** ($6/mes, renueva el 15 de cada mes), voz **Holden**. Por ahora el audio se genera en la web y se descarga con permiso del usuario; para producir conviene una API key en `ELEVENLABS_API_KEY` (la crea el usuario).
- **Higgsfield Starter** ($19/mes, 270 créditos, máx. 4 trabajos simultáneos), CLI `higgsfield` ya autenticado. Escenas con **Seedream 5.0 Flash** (0,5 créditos) + `imagenes/red-ficha/red-oficial.png` como referencia; miniaturas con **Nano Banana Pro** (2 créditos). ~80 créditos por video.
- Pipeline probado en `videos/prueba-30s/` (el usuario aprobó el resultado con subtítulos):
  1. `scripts/generar_escenas.py videos/<v>/escenas.json`
  2. `scripts/subtitulos.py videos/<v>/tiempos.json` (whisper.cpp local, modelo `~/whisper-models/ggml-large-v3-turbo.bin`; el texto sale del guion)
  3. `scripts/montar_video.py videos/<v>/tiempos.json` (usa ffmpeg-full para quemar subtítulos)
  4. `scripts/musica.py videos/<v>/tiempos.json` (voz a -14 LUFS + música de la YouTube Audio Library según `videos/<v>/musica.json`; pistas en `musica/`)
- El clasificador de permisos de Claude Code bloquea algunos clics de "Save"/"Create" en YouTube: Claude deja todo listo y el usuario hace el clic final.
Para verificar un handle: `curl -sL https://www.youtube.com/@<handle> | grep og:title` (vacío = libre; el código HTTP no sirve, siempre es 200).

## Ruta completa (ver `03-plan-maestro.md`)
1. ✅ Idioma y nicho
2. ✅ Identidad del canal
3. ✅ **Configurar cuentas**: correo dedicado, canal de marca, verificación por teléfono, 2FA, ElevenLabs (elegir voz entre 3 candidatas), Higgsfield, conector de Higgsfield en Claude, y 5 imágenes de prueba del personaje "Red" con los prompts de `06-identidad-canal.md`. **Pedir autorización antes de cualquier plan de pago.**
4. ✅ Banco de 30 ideas de títulos validadas con datos (`yt-dlp`).
5. Video piloto #1: guion → voz → timestamps (se pueden sacar localmente; no hace falta TurboScribe) → imágenes → montaje → miniatura → **publicación (con autorización)**.
6. Producción constante: 2 a 4 videos por semana.
7. Optimización con datos de YouTube Studio.
8. Solicitar el YPP.
9. Escalar: pista de audio en español o un segundo canal.

Hecho: `scripts/montar_video.py` arma el video con ffmpeg (reemplaza CapCut).
