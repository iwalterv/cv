# Paso 3: configurar cuentas

**Listo cuando:** todo funciona de punta a punta con una prueba de 30 segundos (voz + imágenes de Red + montaje).

Reglas: los datos personales, las contraseñas, el teléfono y los pagos los ingresa **el usuario**. Claude guía y verifica. Todo se hace **desde la red de Virginia** para que la cuenta sea consistente desde el primer día.

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 3.1 | Crear un Gmail dedicado al canal | Usuario (guiado) | ⏳ |
| 3.2 | Activar la verificación en dos pasos (2FA) en ese Gmail | Usuario (guiado) | ☐ |
| 3.3 | Crear el canal de marca **Time Peasant**, handle **@timepeasant**, país **United States** | Usuario (guiado), con autorización | ☐ |
| 3.4 | Verificar el canal por teléfono (youtube.com/verify): habilita videos de más de 15 min y miniaturas personalizadas | Usuario | ☐ |
| 3.5 | ElevenLabs: crear cuenta y elegir voz entre 3 candidatas con el mismo párrafo de prueba. **Plan de pago solo con autorización** (el plan gratis no permite uso comercial) | Usuario + Claude | ☐ |
| 3.6 | Higgsfield: crear cuenta y conectar el conector en Claude. **Plan de pago solo con autorización** | Usuario + Claude | ☐ |
| 3.7 | 5 imágenes de prueba de Red con los prompts de `06-identidad-canal.md` | Claude | ☐ |
| 3.8 | Prueba de 30 s de punta a punta: voz → timestamps → imágenes → montaje con ffmpeg | Claude | ☐ |
