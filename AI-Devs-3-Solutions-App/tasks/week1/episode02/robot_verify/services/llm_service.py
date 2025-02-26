from services.llm.llm_factory import LLMFactory
from typing import Optional, Callable

class LLMService:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = LLMFactory.create(model_name)
        
    def get_verification_answer(self, question: str, callback: Optional[Callable] = None) -> str:
        """Get answer for robot verification question"""
        try:
            # Create a system prompt that instructs the model to answer verification questions
            system_prompt = """
            You are a robot assistant that answers verification questions accurately and concisely.
            - Provide only the answer without explanations or additional text
            - For math problems, calculate the result
            - For general knowledge questions, provide factual answers
            - Keep answers very short, ideally just a word or number
            - Do not include units unless specifically asked
            """
            
            # Use the OpenAI client directly for more control
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=self.llm.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.1  # Low temperature for more deterministic answers
            )
            
            answer = response.choices[0].message.content.strip()
            
            if callback:
                callback(f"LLM answer: {answer}")
                
            return answer
            
        except Exception as e:
            if callback:
                callback(f"LLM error: {str(e)}")
            return "ERROR" 