import pathlib
import os
from requests import *
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from Orquestador import *

# =========================
# CONFIG
# =========================


TELEGRAM_TOKEN = "ingresa tu token de telegram aqui"

orq = Orquestador()

# =========================
# TU ORQUESTADOR (simplificado)
# =========================
historiales = {}

def obtener_ultima_sesion(historial):
    nueva = []
    for msg in reversed(historial):
        if msg["role"] == "system" and msg["content"] == "NUEVA SESION":
            break
        nueva.append(msg)
    return list(reversed(nueva))


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

        mensaje_limpio = mensaje.strip().lower()

        # Detectar inicio de nueva sesión (SIN borrar historial)
        if any(mensaje_limpio.startswith(p) for p in ["hola", "buenas", "buen día"]):
            historiales[user_id].append({
                "role": "system",
                "content": "NUEVA SESION"
            })

        # Agregar mensaje del usuario
        historiales[user_id].append({
            "role": "user",
            "content": mensaje
        })

        # 🔥 USAR SOLO LA ÚLTIMA SESIÓN
        historial_filtrado = obtener_ultima_sesion(historiales[user_id])

        prompt = orq.construir_prompt(historial_filtrado)
        response = orq.consulta(prompt)

        # Guardar respuesta
        historiales[user_id].append({
            "role": "assistant",
            "content": response
        })

        # Guardar TODO el historial en archivo
        with open(archivo_path, "w", encoding="utf-8") as archivo:
            for msg in historiales[user_id]:
                if msg["role"] == "user":
                    archivo.write(f"Usuario: {msg['content']}\n")
                elif msg["role"] == "assistant":
                    archivo.write(f"Asistente: {msg['content']}\n")
                elif msg["role"] == "system":
                    archivo.write(f"Sistema: {msg['content']}\n")

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