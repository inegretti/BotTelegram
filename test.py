from Orquestador import Orquestador

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
print(api_key_groq)
api_key_openrouter = keys.get("API_KEY_OPENAI")
print(api_key_openrouter)

#a = Orquestador()
#print(a.consulta("como estas?"))# primera consulta