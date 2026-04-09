Bot de Telegram con Orquestador de IAs

Bot de Telegram que integra múltiples APIs de modelos de lenguaje (Groq y OpenRouter) y selecciona automáticamente cuál utilizar según la complejidad de la consulta.

Características
Selección automática de modelo (Groq / OpenRouter)
Memoria de conversación por usuario
Orquestador centralizado de lógica
Respuestas rápidas con fallback implícito
Arquitectura modular y extensible

Arquitectura
Usuario (Telegram)
        ↓
      Bot
        ↓
 Orquestador
   ↓       ↓
Groq   OpenRouter
bot.py: Maneja la interacción con Telegram
Orquestador.py: Decide qué modelo usar
Groq.py / OpenRouter.py: Integración con APIs

⚙️ Instalación
Instalar dependencias
pip install python-telegram-bot requests openai groq python-dotenv

🔐 Configuración


En el archivo Bot.py en TELEGRAM_TOKEN ingresar el token que se brindo cuando se creo el bot con BOTFATHER
En el archivo Keys.txt:
API_KEY_GROQ= ingresar tu_api_key_groq
API_KEY_OPENAI= ingresar tu_api_key_openrouter
▶️ Uso

Ejecutar el bot:

python bot.py

Luego:

Abrir Telegram
Buscar tu bot
Enviar un mensaje
🧠 Cómo funciona

El sistema utiliza un orquestador que decide qué modelo usar en función de la consulta:

Consultas cortas → Groq (rápido)
Consultas largas → OpenRouter (más potente)

Además, mantiene un historial por usuario para dar contexto a las respuestas.

📌 Ejemplo de flujo
Usuario envía mensaje
Se guarda en historial
Se construye el prompt
El orquestador selecciona modelo
Se genera respuesta
Se guarda en historial
Se responde al usuario
