import os
import requests
from types import SimpleNamespace
from typing import Any
from dotenv import load_dotenv

class APIService:
    """
    Service for handling API operations with AI Devs 3 endpoints.
    Manages answer submissions in a standardized way.
    """
    
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("AI_DEVS_3_REPORT_URL")
        self.api_key = os.getenv("AI_DEVS_3_API_KEY")
        
        if not self.base_url or not self.api_key:
            raise ValueError("Missing required environment variables: AI_DEVS_3_REPORT_URL or AI_DEVS_3_API_KEY")
    
    def submit_answer(self, task: str, answer: Any) -> SimpleNamespace:
        """
        Submit an answer to the AI Devs 3 endpoint.
        
        Args:
            task: Task identifier
            answer: Answer to submit (will be serialized to JSON)
            
        Returns:
            response data from the endpoint
        """
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "task": task,
                "apikey": self.api_key,
                "answer": answer
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            return data
                
        except requests.exceptions.RequestException as e:
            return SimpleNamespace(
                success=False,
                error=f"Request failed: {str(e)}"
            )
        except Exception as e:
            return SimpleNamespace(
                success=False,
                error=f"Unexpected error: {str(e)}"
            ) 