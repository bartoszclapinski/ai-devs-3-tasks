import json
from typing import Optional, Dict
import os
from ..config import Config

class QAMemory:
    def __init__(self):
        # Path to the file in task directory
        self.file_path = os.path.join(Config.STORAGE_PATH, "qa_memory.json")
        self.memory: Dict[str, str] = {}
        self._load_memory()


    def _load_memory(self):
        """Loads saved question-answer pairs from file"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
            self.memory = {}


    def _save_memory(self):
        """Saves question-answer pairs to file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")


    def get_answer(self, question: str) -> Optional[str]:
        """Checks if we already have an answer for this question"""
        return self.memory.get(question)


    def add_qa_pair(self, question: str, answer: str, was_successful: bool = True):
        """Adds question-answer pair to memory if login was successful"""
        if was_successful and question not in self.memory:
            self.memory[question] = answer
            self._save_memory() 


    def clear_memory(self):
        """Clears the question-answer memory"""
        self.memory = {} 