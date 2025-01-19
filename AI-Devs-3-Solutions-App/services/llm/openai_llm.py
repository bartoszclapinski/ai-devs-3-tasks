from .base_llm import BaseLLM
from openai import OpenAI
from typing import Optional
import os

class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def get_answer(self, question: str) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": """
                    Jesteś asystentem, który odpowiada na pytania krótko i zwięźle.
                    Odpowiadaj tylko liczbą, bez dodatkowego tekstu czy jednostek.
                    """},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            return answer if answer.isdigit() else None
        except Exception as e:
            print(f"Błąd LLM: {e}")
            return None 