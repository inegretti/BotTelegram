from groq import Groq # api de groq 

class groq:
    def __init__(self, api_key):
        self.clientG = Groq(
        api_key=api_key
         )

    def query(self, query_string):
        try:
            response = self.clientG.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": query_string+"(responde en castellano)"}
                ]
)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None