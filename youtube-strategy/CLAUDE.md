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
| Datos de investigación | Búsquedas, canales de referencia, miniaturas y fotogramas | `datos/` |

Canales de referencia: **Ink Explainer**, **Zenn**, **StickTory**, **Serious History**, **Chat History**.

## Estado actual: PASO 3 (cuentas)
Paso 2 cerrado el 13-oct-2026: nombre **Time Peasant** (@timepeasant) y personaje **Red** confirmados.
Checklist y estado del paso 3: `pasos/paso-03-cuentas.md`. Canal creado: **Time Peasant**, ID `UCgMVaxgxckffeHQt9SDR5ZA` (Studio: https://studio.youtube.com/channel/UCgMVaxgxckffeHQt9SDR5ZA), cuenta de marca en el Gmail personal del usuario. El usuario tiene otro canal, "FactoMentes", que no se toca: en Studio hay que asegurarse de estar en Time Peasant. Verificación por teléfono hecha (funciones intermedias y avanzadas activas). 2FA activa. ElevenLabs Starter con voz **Holden**. Higgsfield Starter conectado por CLI (`higgsfield ...`). Imágenes: Seedream 5.0 Flash + `imagenes/red-ficha/red-oficial.png` como referencia; miniaturas con Nano Banana Pro. Subpaso actual: **3.8 (prueba de 30 s de punta a punta)**.
Nota: el clasificador de permisos de Claude Code bloquea los clics de "Save"/"Create" en YouTube; Claude deja todo listo y el usuario hace el clic final.
Para verificar un handle: `curl -sL https://www.youtube.com/@<handle> | grep og:title` (vacío = libre; el código HTTP no sirve, siempre es 200).

## Ruta completa (ver `03-plan-maestro.md`)
1. ✅ Idioma y nicho
2. ✅ Identidad del canal
3. **Configurar cuentas**: correo dedicado, canal de marca, verificación por teléfono, 2FA, ElevenLabs (elegir voz entre 3 candidatas), Higgsfield, conector de Higgsfield en Claude, y 5 imágenes de prueba del personaje "Red" con los prompts de `06-identidad-canal.md`. **Pedir autorización antes de cualquier plan de pago.**
4. Banco de 30 ideas de títulos validadas con datos (`yt-dlp`).
5. Video piloto #1: guion → voz → timestamps (se pueden sacar localmente; no hace falta TurboScribe) → imágenes → montaje → miniatura → **publicación (con autorización)**.
6. Producción constante: 2 a 4 videos por semana.
7. Optimización con datos de YouTube Studio.
8. Solicitar el YPP.
9. Escalar: pista de audio en español o un segundo canal.

Idea pendiente: un script con `ffmpeg` que arme el video automáticamente a partir del audio, las imágenes y la tabla de tiempos (reemplaza el montaje manual en CapCut).
