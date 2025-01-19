import json
from typing import Optional, Dict
import os
from ..config import Config

class QAMemory:
    def __init__(self):
        # Ścieżka do pliku w katalogu zadania
        self.file_path = os.path.join(Config.STORAGE_PATH, "qa_memory.json")
        self.memory: Dict[str, str] = {}
        self._load_memory()

    def _load_memory(self):
        """Wczytuje zapisane pary pytanie-odpowiedź z pliku"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
        except Exception as e:
            print(f"Błąd podczas wczytywania pamięci: {e}")
            self.memory = {}

    def _save_memory(self):
        """Zapisuje pary pytanie-odpowiedź do pliku"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd podczas zapisywania pamięci: {e}")

    def get_answer(self, question: str) -> Optional[str]:
        """Sprawdza czy mamy już odpowiedź na to pytanie"""
        return self.memory.get(question)

    def add_qa_pair(self, question: str, answer: str, was_successful: bool = True):
        """Dodaje parę pytanie-odpowiedź do pamięci jeśli logowanie było udane"""
        if was_successful and question not in self.memory:
            self.memory[question] = answer
            self._save_memory() 

    def clear_memory(self):
        """Czyści pamięć pytań i odpowiedzi"""
        self.memory = {} 