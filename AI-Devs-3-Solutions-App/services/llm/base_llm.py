from abc import ABC, abstractmethod
from typing import Optional

class BaseLLM(ABC):
    @abstractmethod
    def get_answer(self, question: str) -> Optional[str]:
        pass 