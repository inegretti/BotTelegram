from Groq import groq
from OpenRouter import openrouter

def cargar_keys(ruta):
    keys = {}
    with open(ruta, "r") as archivo:
        for linea in archivo:
            if "=" in linea:
                clave, valor = linea.strip().split("=", 1)
                keys[clave] = valor
    return keys

keys = cargar_keys("keys.txt")
api_key_groq = keys.get("API_KEY_GROQ")
api_key_openrouter = keys.get("API_KEY_OPENAI")



class Orquestador:
    def __init__(self):
        self.operador_groq = groq(api_key_groq) # colocar la api de key de groq
        self.operador_openrouter = openrouter(api_key_openrouter) # colocar la api de key de openrouter

    def consulta(self, consulta):
        try:
            if len(consulta) < 200:
                respuesta = self.operador_groq.query(consulta).choices[0].message.content
            else:
                respuesta = self.operador_openrouter.query(consulta).choices[0].message.content
            return respuesta    
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
            
    def revision_cruzada(self, consulta):
        try:
            respuesta_groq = self.operador_groq.query(consulta).choices[0].message.content
            respuestaCruzada = self.operador_openrouter.query("mejora la respuesta pero entregala de manera directa y sin mencionar que es de otra fuente:" + respuesta_groq).choices[0].message.content
            
            return  respuestaCruzada 
            
        except Exception as e:
            print(f"An error occurred during cross-checking: {e}")
            return f"An error occurred during cross-checking: {e}"
        
    def construir_prompt(self, historial):
        texto = ""
        for msg in historial:
            if msg["role"] == "user":
                texto += f"Usuario: {msg['content']}\n"
            elif msg["role"] == "assistant":
                texto += f"Asistente: {msg['content']}\n"
        return texto         
            