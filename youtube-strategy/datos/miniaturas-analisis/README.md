# Análisis de miniaturas (16-oct-2026)

**Método:** con los datos de `datos/paso4/canales/` se calcularon los videos *outlier*, es decir, las vistas de cada video divididas entre la mediana de su canal (`outliers.tsv`). Un video que hace 50 o 200 veces lo normal de su canal casi siempre tiene una miniatura que funciona: el canal y el público son los mismos, lo que cambia es el clic. Se bajaron solo las miniaturas (i.ytimg.com) de:
- `1-ganadoras.jpg`: 20 outliers de Zenn, Axen, Ink Explainer, StickTory, Chat History, Serious History y Medieval Times Discovered (de 15× a 258× la mediana).
- `2-black-death-top.jpg`: las 8 miniaturas de los videos más vistos sobre la peste negra.
- `3-perdedoras.jpg`: los 2 videos con menos vistas de cada uno de esos canales, para contrastar.
- `4-nuestras-v1.jpg`: las 3 del piloto (A Flowers, B 50/50, C 1348).

Limitación: no vemos el CTR de otros canales; las vistas frente a la mediana son la mejor aproximación que hay.

## Qué tienen las ganadoras

1. **Una amenaza más el personaje: una historia en una sola imagen.** "SURVIVED HOW?" (Axen, 228×): monigote asustado y la *sombra* de un tigre dientes de sable. "ROTTEN MEAT?": el personaje muerde carne podrida. "NO PRIVACY?": todos duermen amontonados. Se entiende la situación en menos de un segundo y queda una pregunta en el aire.
2. **El tema se reconoce de inmediato.** En la peste negra, 5 de las 8 miniaturas top usan la **máscara de pico del médico de la peste**; las demás usan esqueletos, bubones o carretas de muertos. Es el código visual del tema.
3. **Texto de 2 o 3 palabras, AMARILLO o blanco sobre fondo oscuro**, en una franja arriba y sin tapar al personaje. Zenn, Axen e Ink (los tres mayores outliers) usan amarillo con contorno negro.
4. **Emoción exagerada en la cara**: terror, asco o resignación ("born to suffer", con lágrima y ojo morado).
5. **Contraste fuerte**: personaje claro sobre fondo oscuro, o al revés. Pocos elementos.

## Qué tienen las perdedoras
Conceptos abstractos sin amenaza ("THE IKEA EFFECT ?", "THE EVIL PLACEBO" solo con texto), escenas sin conflicto ("WHY SO TAME?" con un perro sonriendo) o temas raros que nadie busca. **Mismo estilo que las ganadoras y 50 a 200 veces menos vistas:** el estilo no basta, decide el concepto.

## Diagnóstico de las nuestras (lo que "les falta")
| | Problema |
|---|---|
| Todas | **Nada dice "peste negra" a primera vista**: no hay esqueleto, muerte, bubón ni médico. Quien no lea el título no sabe de qué trata. |
| A FLOWERS? | Las flores dan una sensación alegre, no de peligro. Solo se entienden después de ver el video. |
| B 50/50? | La cara de terror es muy buena, pero **la amenaza es una moneda**: es abstracta y no hay nada que temer en la imagen. |
| C 1348? | La rata es lo más cercano a una amenaza, pero es del mismo tamaño que Red y se ve casi amigable. "1348" no dice nada a quien no sabe historia. |
| Texto | Blanco y con el "?" rojo pequeño. Funciona, pero las miniaturas top del nicho usan amarillo y palabras de emoción, no fechas. |

## Propuestas v2 (las tres ideas salen del guion: el bubón "the size of an egg" está en la línea 1, Júpiter en la 3 y el mito de la máscara en el capítulo de los doctores)

### Ideas (misma identidad: Red con su bufanda roja)
1. **"YOU'RE NEXT?"**: Red aterrado; detrás, enorme, **la Muerte (esqueleto con guadaña)** le toca el hombro. Fondo de pueblo oscuro. Es la estructura de "SURVIVED HOW?": personaje + amenaza gigante.
2. **"EGG-SIZED?"**: Red mira bajo su brazo un bulto (bubón) del tamaño de un huevo, con cara de horror. Es el dato más fuerte del video, va en el gancho, y es estilo dibujo animado, nada gráfico.
3. **"WRONG CENTURY"**: Red señala al médico de la peste con máscara de pico, que aparece **tachado con una X roja**. Usa el ícono más reconocible del tema, pero el propio video lo desmiente (narración: el disfraz aparece en el siglo XVII, unos 300 años después). Da curiosidad y es honesto: quien hace clic recibe exactamente esa explicación.
4. (Alternativa) **"BLAME JUPITER?"**: un médico medieval con túnica, sin máscara, señala un Júpiter gigante en el cielo mientras Red lo mira incrédulo. Humor y curiosidad (es el gancho de los primeros 20 segundos).

Nota de precisión: la máscara de pico **sola** sería engañosa, porque es del siglo XVII. Solo se usa tachada (propuesta 3), igual que en el video.

Texto en **amarillo con contorno negro** para probar contra el blanco de la identidad (Test & Compare decide).
