# Paso 3: configurar cuentas

**Listo cuando:** todo funciona de punta a punta con una prueba de 30 segundos (voz + imágenes de Red + montaje).

Reglas: los datos personales, las contraseñas, el teléfono y los pagos los ingresa **el usuario**. Claude guía y verifica. Todo se hace **desde la red de Virginia** para que la cuenta sea consistente desde el primer día.

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 3.1 | ~~Gmail dedicado~~ → se usa el Gmail personal del usuario (ya tiene teléfono). Decisión del 13-oct-2026: canal de marca **nuevo** en esa cuenta; el canal viejo "FactoMentes" (1 Short en español de 2023) queda aparte | Usuario | ✅ |
| 3.2 | Verificación en dos pasos del Gmail: ya estaba activa | Usuario | ✅ |
| 3.3 | Canal de marca **Time Peasant** creado el 15-oct-2026: ID `UCgMVaxgxckffeHQt9SDR5ZA`, handle **@TimePeasant**, país **United States**, 10 palabras clave guardadas | Usuario + Claude | ✅ |
| 3.4 | Canal verificado por teléfono (15-oct-2026): funciones estándar, intermedias y avanzadas **Enabled** | Usuario | ✅ |
| 3.5 ✅ | ElevenLabs: crear cuenta y elegir voz entre 3 candidatas con el mismo párrafo de prueba. **Plan de pago solo con autorización** (el plan gratis no permite uso comercial) | Usuario + Claude | ✅ voz **Holden**; plan **Starter** pagado el 15-oct-2026 (renueva el 15-nov, $6/mes) |
| 3.6 ⏳ | Higgsfield: crear cuenta y conectar el conector en Claude. **Plan de pago solo con autorización** | Usuario + Claude | ☐ |
| 3.7 | 5 imágenes de prueba de Red con los prompts de `06-identidad-canal.md` | Claude | ☐ |
| 3.8 | Prueba de 30 s de punta a punta: voz → timestamps → imágenes → montaje con ffmpeg | Claude | ☐ |

## Notas de ElevenLabs (precios vistos en elevenlabs.io/pricing el 15-oct-2026)

| Plan | Precio | Créditos/mes (~1 por carácter) | Uso comercial |
|---|---|---|---|
| Free | $0 | 10.000 (~10 min) | No |
| Starter | $6/mes (83 % de descuento el 1.er mes, ~$1, hasta el 18-oct) | 30.000 (~30 min) | Sí |
| Creator | $22/mes (50 % el 1.er mes, $11) | 121.000 (~121 min) | Sí |

Cálculo: un video de ~12 min ≈ 1.800 palabras ≈ 11.000 caracteres. Starter alcanza para ~2-3 videos al mes; con 2-4 videos por semana hará falta **Creator**.
Plan: (1) cuenta Free para elegir la voz; (2) **con autorización**, Starter para el piloto; (3) **con autorización**, Creator cuando arranque la producción constante.
Párrafo de prueba: `voz/parrafo-prueba.md`.

## Notas de Higgsfield (precios vistos en higgsfield.ai/pricing el 15-oct-2026, facturación mensual)

| Plan | Precio/mes | Créditos/mes | Imágenes aprox. (Nano Banana Pro) |
|---|---|---|---|
| Starter | $19 | 270 | ~135 |
| Plus | $59 | 1.200 | ~600 (+ Nano Banana 2 ilimitado 7 días) |
| Ultra | $129 | 3.000 | ~1.500 |

Cálculo: un video de ~12 min con una imagen cada 5-8 s necesita ~90-140 imágenes. **Starter ≈ 1 video al mes.** Para 2-4 videos por semana, Higgsfield sale caro (Plus/Ultra): antes del paso 6 hay que comparar con usar el modelo de imágenes directamente por API.
