# Análisis de la estrategia: canal "faceless" 2D con IA

Fuente: video de "Leo" (12:32, en inglés). La transcripción completa está en [`01-transcripcion-original.md`](01-transcripcion-original.md).

---

## 1. Resumen en una frase

Se copia el **formato** de un canal exitoso de dibujos simples (monigotes o "stick figures" en 2D, por ejemplo sobre *humanos antiguos*). Con IA se generan guion, voz e imágenes, y todo se monta en CapCut. Él dice que un video completo sale en "minutos".

## 2. El formato que propone

- **Canal "faceless"**: nunca aparece una persona en cámara.
- **Estilo visual**: ilustraciones 2D muy simples (monigotes) con una voz en off que narra una historia.
- **Ejemplo de nicho**: "¿Qué hacían los humanos antiguos cuando llovía toda la semana?". Son temas de curiosidad e historia narrados en segunda persona ("Imagina que llevas dos días sin comer...").
- Según él, el nicho puede ser **cualquier tema**; lo que se repite es el estilo.

## 3. El sistema paso a paso (tal como lo explica)

| # | Paso | Herramienta | Qué se obtiene | Min. |
|---|---|---|---|---|
| 1 | Elegir un canal competidor y ordenar sus videos por **Más populares** | YouTube | Tema probado | 02:10 |
| 2 | Copiar el enlace del video y sacar la transcripción | youtubetotranscript.com | Texto del video exitoso | 02:15 |
| 3 | Pedir a Claude: *"Genérame un guion similar a esta transcripción, mismo estilo, información y voz"* | Claude | Guion nuevo | 03:01 |
| 4 | Pegar el guion y generar la voz (él usa la voz "Roger") | ElevenLabs (Text to Speech) | Audio MP3 | 03:54 |
| 5 | Transcribir **su propio** audio para tener marcas de tiempo | TurboScribe (modelo "Whale", 3 gratis al día) | Guion con timestamps | 04:46 |
| 6 | Conectar **Higgsfield** a Claude como *custom connector* (MCP). Con un prompt largo, Claude genera **una imagen por cada timestamp**, todas en el mismo estilo | Claude + Higgsfield | Unas 50 imágenes y una tabla de "qué imagen va en qué segundo" | 05:51 |
| 7 | Poner el audio en el editor y colocar cada imagen en su segundo, siguiendo la tabla | CapCut (web, gratis) | Video final | 09:03 |

**La clave técnica real es el paso 5 → 6.** Tener el guion con tiempos permite que la IA produzca las imágenes **ya sincronizadas** con la narración. Así se evita contratar a un animador o editor.

## 4. Lo que promete (y cómo leerlo)

| Lo que dice | Lectura crítica |
|---|---|
| Un canal de 90 días con menos de 1 M de vistas ganó **$11.000** con menos de 5.000 suscriptores | Eso implica un RPM (ingreso por cada 1.000 vistas) de más de $11. Es posible en temas de historia o educación con público de EE. UU., pero está por encima del promedio. Toma estas cifras como **el mejor caso**, no como lo normal. |
| Un canal con 1,5 M de vistas ganó **$16.000** | Mismo comentario: el RPM está alto. |
| Un video suyo ganó **$18.000** | Es un caso aislado (un video viral). |
| "Aunque tardes 20 videos en despegar, vale la pena" | Es la parte más honesta: **hay que contar con muchos videos que no funcionen**. |
| A partir de 10:28 vende su **programa de coaching** "premium" | El video es un **embudo de ventas**. Reconoce que "hay mucho más detrás" (11:30), que es justo lo que no explica gratis. |

## 5. Lo que el video NO explica (y vamos a tener que resolver nosotros)

1. **Elección del nicho y del idioma.** En inglés con público de EE. UU. el RPM es mucho mayor. En español la competencia es menor, pero el RPM es más bajo.
2. **Títulos y miniaturas**, que son lo que más pesa en el número de clics (CTR).
3. **Gancho y retención**: los primeros 30 segundos y el ritmo de la narración.
4. **Frecuencia de publicación** y consistencia.
5. **Requisitos para monetizar (YouTube Partner Program)**: 1.000 suscriptores **y** 4.000 horas de reproducción pública en 12 meses (o 10 M de vistas en Shorts en 90 días). Hay un nivel previo con 500 suscriptores, 3 videos en 90 días y 3.000 horas, pero ese **no** paga anuncios. Varias fuentes reportan que desde el 1 de febrero de 2027 se pedirían 8.000 horas; está **sin confirmar** en la página oficial. Si es cierto, conviene llegar antes de esa fecha.
6. **Políticas de YouTube** (ver riesgos abajo).
7. **Costos** de las herramientas.

## 6. Riesgos importantes ⚠️

1. **Política de "contenido no auténtico"** (antes llamada "contenido repetitivo", actualizada en julio de 2025). YouTube puede **quitar la monetización a todo el canal** si el contenido es producido en masa, con plantilla y poco esfuerzo. Este formato está justo en esa zona gris. La diferencia la marcan el valor añadido, la investigación y la variedad. Lo que más riesgo genera, según los reportes: un proceso 100 % automatizado, guiones copiados o de plantilla, publicar a diario sin revisión humana y videos casi idénticos entre sí. Hay reportes de cierres masivos de canales de IA en enero de 2026.
2. **Copiar el guion de un competidor** ("mismo estilo, misma información") roza el **contenido reutilizado** y puede traer reclamos o problemas éticos.
   👉 **Nuestra versión:** usar a los competidores solo para **descubrir temas y estructuras** que funcionan, y escribir guiones **originales**, con datos verificados y un ángulo propio.
3. **Exactitud histórica.** En temas de "humanos antiguos" la IA inventa datos con facilidad. Los errores generan comentarios negativos y le restan autoridad al canal.
4. **Saturación.** Una búsqueda rápida ya muestra muchos videos con el título casi idéntico "What Did Ancient Humans Do…" (… All Day, … All Night, … For Fun, … When Someone Died). Muchas personas vieron este mismo tutorial y van a copiar este mismo formato. Para diferenciarse hacen falta un estilo visual propio, una voz menos común (él mismo sugiere no usar las voces más populares) y un subnicho.
5. **Divulgación de IA.** Los dibujos animados normalmente no requieren la etiqueta de "contenido alterado o sintético", pero hay que revisarlo caso por caso.

## 7. Costos aproximados (mensuales; verificar precios actuales)

| Herramienta | Uso | Plan |
|---|---|---|
| Claude | Guiones y orquestación de imágenes | Pro (incluye conectores) |
| ElevenLabs | Voz | Starter/Creator según los minutos de audio |
| Higgsfield | Imágenes | Créditos de pago según el volumen |
| TurboScribe | Timestamps | Gratis (3 al día) → **se puede omitir** (ver abajo) |
| CapCut | Edición | Gratis |

## 8. Cómo podemos mejorar el sistema

- **Omitir TurboScribe.** Aquí mismo puedo transcribir el audio con marcas de tiempo, como acabo de hacer con este video. Además, ElevenLabs puede exportar los tiempos directamente.
- **Automatizar el montaje (paso 7).** Es la parte más lenta y manual: colocar unas 50 imágenes una por una. Puedo hacer un script que tome el audio, las imágenes y la tabla de tiempos y **arme el video automáticamente** (con un leve zoom o paneo en cada imagen). CapCut quedaría solo para retoques finales.
- **"Guía de estilo" fija del canal.** Definir el personaje, la paleta de colores, el tipo de trazo y el prompt base para que todas las imágenes sean coherentes entre videos. Eso se vuelve la marca del canal.
- **Plantillas propias de guion.** Estructura de gancho, desarrollo y cierre, con investigación real, para cumplir mejor las políticas y diferenciarnos.

## 9. Plan de acción propuesto

**Fase 0: decisiones (antes de crear nada)**
- [ ] Idioma del canal (inglés o español).
- [ ] Nicho y subnicho (por ejemplo, humanos antiguos, supervivencia, vida cotidiana en la historia, curiosidades del cuerpo humano...).
- [ ] Analizar 3 a 5 canales competidores: sus videos más populares, títulos, miniaturas, duración y frecuencia.
- [ ] Presupuesto mensual para herramientas.

**Fase 1: configuración**
- [ ] Cuentas en Claude, ElevenLabs, Higgsfield y CapCut.
- [ ] Conectar Higgsfield a Claude (Customize → Connectors → Add custom connector → URL del MCP de Higgsfield).
- [ ] Crear el canal: nombre, banner, logo y descripción, con la guía de estilo visual.

**Fase 2: piloto (3 videos)**
- [ ] Producir 3 videos completos con el sistema y medir cuánto tarda cada uno.
- [ ] Ajustar el prompt de imágenes y la voz.

**Fase 3: tracción (unos 20 videos)**
- [ ] Publicar 2 o 3 videos por semana.
- [ ] Revisar CTR y retención en YouTube Studio y doblar la apuesta en los temas que funcionen.

**Fase 4: monetización**
- [ ] Llegar a 1.000 suscriptores y 4.000 horas, y solicitar el YPP.
- [ ] Una vez dentro, evaluar replicar el sistema en un **segundo canal** (otro nicho u otro idioma).
