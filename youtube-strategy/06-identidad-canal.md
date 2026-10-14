# Paso 2: identidad del canal

Fuente: 32 miniaturas y 24 fotogramas de los canales ganadores ([`datos/visuales/`](datos/visuales/README.md)).

## 1. Lo que hacen los ganadores

### Tres escuelas visuales

| Escuela | Canales | Cómo se ve | Resultado |
|---|---|---|---|
| **A. Escena ilustrada a color** | Ink Explainer, Axen, HUMAN-ISH, Stickstory | Monigote de cabeza redonda con pelo y ropa de piel, **fondos completos a todo color** (cueva, sabana, nieve), estilo cómic cálido | **El que más vistas tiene** (13 M, 3,3 M, 914K) |
| **B. Pizarra minimalista** | Zenn | Fondo blanco o negro, línea negra, pocos acentos (flechas rojas, amarillo), etiquetas de texto y gráficos | Funciona (8 M), es más barato y "explicativo" |
| **C. Personajes dramáticos** | StickTory, Serious History | Fondo blanco, personajes de cabeza grande muy expresivos (lágrimas, sangre), texto a mano con flecha ("born to Suffer") | Funciona muy bien con "Why it sucked to be…" (cinco videos de más de 1 M) |

### Reglas de miniatura que todos cumplen
1. **De 1 a 3 palabras en la miniatura**, casi siempre en forma de **pregunta**: "2 SLEEPS?", "ROTTEN MEAT?", "NO DOCTORS?", "PREGNANT?".
2. **El texto NO repite el título; agrega curiosidad.** Título: *What Did Ancient Humans Do at Night?* → miniatura: **"2 SLEEPS?"**
3. **Un personaje grande con una emoción fuerte** (miedo, asco, confusión o placer), mirando hacia la situación.
4. **Una sola idea por imagen**, legible en tamaño de celular.
5. **Texto grande con contorno negro**, en amarillo (escuela A) o negro (escuelas B y C).
6. **Contraste fuerte:** fondo oscuro con texto claro, o al revés.

### Dentro del video (fotogramas)
- **El mismo personaje en todas las escenas** (Ink Explainer: el mismo cavernícola de pelo café). Es lo que da coherencia y "marca".
- **Una imagen por idea**, cambiando cada pocos segundos.
- **Texto en pantalla solo en momentos clave** ("THE FARMING LIFE → BECOMING THE BROKEN BONES", "FIRST SLEEP 4 HRS").
- Logo pequeño en la esquina (marca de agua).

## 2. Nuestra identidad (propuesta)

### Concepto
**"Tú, en cualquier época de la historia."** Un mismo protagonista **viaja por las épocas**. Cambia de ropa según el período, pero **siempre es reconocible**. Él es "tú", el espectador.

### El personaje
- Monigote de **cabeza redonda blanca y ojos grandes y expresivos**, al estilo de la escuela A, que es la que más vistas trae.
- **Rasgo de marca: una bufanda (o pañuelo) roja que lleva SIEMPRE, en todas las épocas.** Romano, campesino medieval, vikingo o cavernícola, siempre con la bufanda roja. Así se le reconoce al instante en la miniatura, y ningún competidor tiene algo así.
- Nombre interno para los prompts: **"Red"**. No hace falta mencionarlo en la narración.

### Estilo visual
- **Base:** escuela A (escenas ilustradas a color, cálidas, estilo cómic), porque es la que más rinde.
- **Toque propio:**
  - El rojo de la bufanda es el **color de marca**: se usa en flechas, texto destacado y logo.
  - **Cada época tiene su propia paleta**: Edad Media en tonos tierra y verde; Roma en terracota y blanco; vikingos en azul frío y gris; Egipto en dorado y arena.
- **Texto de miniatura:** blanco con contorno negro grueso, y **la palabra clave en rojo**. Nos diferencia del amarillo que usan todos.

### Prompt base para imágenes (para Higgsfield o Claude)
```
2D hand-drawn cartoon illustration, warm comic style, clean bold black outlines,
flat colors with soft shading. Main character "Red": a simple stick-figure person
with a round white head, large expressive eyes, thin black stick limbs, always
wearing a bright red scarf. Dressed as {ERA_OUTFIT}. Setting: {SCENE},
{ERA_PALETTE} color palette. Expression: {EMOTION}. Composition: single clear
idea, character large in frame, uncluttered background. No text, no watermark.
16:9.
```

### Prompt para miniaturas
```
YouTube thumbnail, 2D cartoon, same character "Red" (round white head, huge
expressive eyes, stick limbs, bright red scarf) dressed as {ERA_OUTFIT}, very large
in frame, extreme {EMOTION} expression, reacting to {SITUATION}. High contrast,
{ERA_PALETTE}, simple background, empty space at top for text. 16:9.
```
El texto (de 1 a 3 palabras) se agrega después en CapCut o Canva, para tener control de la tipografía.

### Voz
- **Evitar "Roger"** y las voces más populares de ElevenLabs: el propio Leo lo advierte, y suenan a "otro canal de IA más".
- Buscar en la biblioteca de voces de ElevenLabs: **voz masculina o femenina americana, cálida, de tono conversacional, con un toque de ironía**. Que suene a alguien contándote un secreto, no a un documental.
- Elegimos entre 3 candidatas en el paso 3, haciendo una prueba con el mismo párrafo.

## 3. Nombre del canal: candidatos

| Nombre | Por qué funciona | Riesgo |
|---|---|---|
| **Yesteryou** | Juego de palabras con *yesterday* + *you*: "tú en el pasado". Corto, único y fácil de buscar | Hay que explicarlo una vez (en el banner) |
| **Born Too Early** | Engancha al instante y encaja con "Why it sucked to be…" | Es más genérico; puede estar tomado |
| **Stuck in History** | Claro y con humor: el personaje está "atrapado" en la historia | Puede existir algo parecido |
| **Back Then, You** | Dice exactamente el concepto | Es menos memorable |
| **The Red Scarf** | Gira alrededor del personaje | No dice de qué trata el canal |

**Mi recomendación: Yesteryou.** Es único (fácil de ser el primer resultado en búsquedas), resume el concepto en una palabra y queda bien como @handle.

**Antes de decidir hay que verificar** que el @handle esté libre en YouTube y que no exista un canal con el mismo nombre.
