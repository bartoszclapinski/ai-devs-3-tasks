from ..config import Config
import re
from typing import Optional

class KnowledgeService:
    def __init__(self):
        self.special_knowledge = Config.SPECIAL_KNOWLEDGE
        
    def get_answer(self, question: str) -> Optional[str]:
        """Get answer based on special knowledge or return None if unknown"""
        # Convert question to lowercase for matching
        question_lower = question.lower()
        
        # Check for special knowledge cases
        for key, value in self.special_knowledge.items():
            if key in question_lower:
                return value
                
        # Check for specific patterns
        if re.search(r'capital\s+of\s+poland', question_lower) or re.search(r'poland.*capital', question_lower):
            return "KRAKÓW"
            
        if re.search(r'hitchhiker.*guide.*galaxy', question_lower) or re.search(r'famous\s+number.*galaxy', question_lower):
            return "69"
            
        if re.search(r'current\s+year', question_lower) or re.search(r'what\s+year', question_lower):
            return "1999"
            
        # No special knowledge match
        return None 