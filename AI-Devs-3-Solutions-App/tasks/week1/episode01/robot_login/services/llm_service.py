from openai import OpenAI
from typing import Optional
from ..config import Config

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def get_answer(self, question: str) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
                    You are an assistant that answers questions briefly and concisely.
                    Respond only with a number, without any additional text or units.
                    """},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            return answer if answer.isdigit() else None
        except Exception as e:
            print(f"LLM Error: {e}")
            return None 