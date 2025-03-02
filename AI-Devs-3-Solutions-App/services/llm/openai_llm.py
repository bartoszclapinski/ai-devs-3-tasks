from .base_llm import BaseLLM
from openai import OpenAI
from typing import Optional
import os

class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def get_answer(self, question: str, system_prompt: Optional[str] = None) -> Optional[str]:
        try:
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
                
            # Add user message
            messages.append({"role": "user", "content": question})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return None 