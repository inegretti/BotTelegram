from openai import OpenAI # api de openai

class openrouter:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
)

    def query(self, query_string):
        try:
            response = self.client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {"role": "user", "content": query_string+"(responde en castellano)"}
                     ]
                )
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None