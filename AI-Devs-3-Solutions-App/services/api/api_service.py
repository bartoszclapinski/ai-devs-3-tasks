import os
import requests
import logging
from types import SimpleNamespace
from typing import Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
            
            # Log the payload for debugging
            logger.info(f"Submitting to URL: {self.base_url}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Payload: {payload}")
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            
            # Log the response
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            
            response.raise_for_status()
            
            data = response.json()
            
            # Convert successful response to SimpleNamespace
            return SimpleNamespace(
                success=True,
                data=data
            )
                
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