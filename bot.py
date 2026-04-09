from requests import *
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from Orquestador import *

# =========================
# CONFIG
# =========================
TELEGRAM_TOKEN = "ingresa el token que te dio el botfather"

orq = Orquestador()

# =========================
# TU ORQUESTADOR (simplificado)
# =========================
historiales = {}

def preguntar(user_id, mensaje):
    try:
        if user_id not in historiales:
            historiales[user_id] = [
                {"role": "system", "content": "Sos un asistente técnico"}
            ]
        historiales[user_id].append({"role": "user", "content": mensaje})
        mensaje = orq.construir_prompt(historiales[user_id]) # Construye el prompt a partir del historial
        response = orq.consulta(mensaje)
        historiales[user_id].append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        return f"Error: {e}"

# =========================
# HANDLER TELEGRAM
# =========================

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.message.chat_id
    respuesta = preguntar(user_id, user_msg)
    await update.message.reply_text(respuesta)

# =========================
# MAIN  ejecuta el bot
# =========================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()