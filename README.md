🤖 Bot de Telegram con Orquestador de IAs

Bot de Telegram que integra múltiples APIs de modelos de lenguaje (Groq y OpenRouter) y selecciona dinámicamente cuál utilizar según la complejidad de la consulta.


Características principales

Orquestador de modelos (selección automática Groq / OpenRouter)
Memoria de conversación por usuario
Persistencia en archivos (historial sobrevive reinicios)
Manejo de sesiones (separación de contexto con "NUEVA SESION")
Arquitectura modular y extensible


Problema que resuelve

Los modelos de lenguaje no mantienen estado por sí mismos.
Este proyecto implementa:

* Persistencia de conversaciones
* Control de contexto enviado al modelo
* Separación de sesiones para evitar contaminación de respuestas

Esto permite simular un comportamiento más cercano a un chatbot real.


Arquitectura

Usuario (Telegram)
        ↓
      Bot
        ↓
 Orquestador
   ↓       ↓
Groq   OpenRouter


Componentes:

* `bot.py` → Maneja interacción con Telegram
* `Orquestador.py` → Decide qué modelo usar
* `Groq.py` / `OpenRouter.py` → Integración con APIs

Instalación

bash
pip install python-telegram-bot requests openai groq python-dotenv

Configuración

Configurar las siguientes variables:

* `TELEGRAM_TOKEN`
* `API_KEY_GROQ`
* `API_KEY_OPENAI`


Uso

bash
python bot.py

Luego:

1. Abrir Telegram
2. Buscar el bot
3. Enviar un mensaje


Cómo funciona

1. Se recibe el mensaje del usuario
2. Se carga el historial persistido
3. Se detecta inicio de nueva sesión (ej: "hola")
4. Se filtra el contexto relevante (última sesión)
5. El orquestador selecciona el modelo
6. Se genera la respuesta
7. Se guarda el historial actualizado

Persistencia y sesiones

* Cada usuario tiene su propio archivo de historial
* Se marca el inicio de nuevas sesiones con `"Sistema: NUEVA SESION"`
* El sistema utiliza únicamente la última sesión para generar respuestas

Esto evita mezclar contextos de conversaciones anteriores.


By Ignacio Negretti
