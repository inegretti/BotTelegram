import pathlib
import os
from requests import *
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from Orquestador import *

# =========================
# CONFIG
# =========================


TELEGRAM_TOKEN = ""

orq = Orquestador()

# =========================
# TU ORQUESTADOR (simplificado)
# =========================
historiales = {}

def preguntar(user_id, mensaje):
    try:
        
        #version sin persistencia en archivos solo en memoria activa
        #if user_id not in historiales:
        #    historiales[user_id] = [
        #        {"role": "system", "content": "Sos un asistente técnico"}
        #    ]
        #historiales[user_id].append({"role": "user", "content": mensaje})
        #mensaje = orq.construir_prompt(historiales[user_id]) # Construye el prompt a partir del historial
        #response = orq.consulta(mensaje)
        #historiales[user_id].append({"role": "assistant", "content": response})
        #return response
    
    
        # version con archivos para persistencia de historiales por usuario 
        archivo_path = f"{user_id}.txt"
        if user_id not in historiales:
            historiales[user_id] = []


            # SOLO cargar archivo la primera vez
            if os.path.exists(archivo_path):
                with open(archivo_path, "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        if linea.startswith("Usuario:"):
                            contenido = linea.replace("Usuario:", "").strip()
                            historiales[user_id].append({"role": "user", "content": contenido})
                        elif linea.startswith("Asistente:"):
                            contenido = linea.replace("Asistente:", "").strip()
                            historiales[user_id].append({"role": "assistant", "content": contenido})

        # agregar mensaje nuevo
        historiales[user_id].append({"role": "user", "content": mensaje})

        prompt = orq.construir_prompt(historiales[user_id])
        response = orq.consulta(prompt)

        historiales[user_id].append({"role": "assistant", "content": response})

        # guardar TODO el historial
        with open(archivo_path, "w",encoding="utf-8") as archivo:
            for msg in historiales[user_id]:
                if msg["role"] == "user":
                    archivo.write(f"Usuario: {msg['content']}\n")
                elif msg["role"] == "assistant":
                    archivo.write(f"Asistente: {msg['content']}\n")       
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