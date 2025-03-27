from .openai_llm import OpenAILLM
from typing import Dict, Type
from .base_llm import BaseLLM

class LLMFactory:
    _models: Dict[str, Type[BaseLLM]] = {        
        "gpt-4o-mini": OpenAILLM,
        "gpt-4o": OpenAILLM,
        # "sonnet": SonnetLLM,  # Do zaimplementowania
        # "bielik": BielikLLM,  # Do zaimplementowania
    }

    @classmethod
    def get_available_models(cls) -> list[str]:
        return list(cls._models.keys())

    @classmethod
    def create(cls, model_name: str) -> BaseLLM:
        if model_name not in cls._models:
            raise ValueError(f"Nieznany model: {model_name}")
        return cls._models[model_name](model_name) 