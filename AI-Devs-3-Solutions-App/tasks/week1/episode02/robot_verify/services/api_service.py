import requests
import json
from typing import Optional, Callable
from ..models.verification import VerificationRequest, VerificationResponse
from ..config import Config

class ApiService:
    def __init__(self):
        self.session = requests.Session()
        self.url = Config.API_URL
        
    def send_request(self, request: VerificationRequest, callback: Optional[Callable] = None) -> Optional[VerificationResponse]:
        """Send request to robot verification API"""
        try:
            if callback:
                callback(f"Sending request: {json.dumps(request.__dict__)}")
                
            response = self.session.post(
                self.url,
                json=request.__dict__,
                timeout=Config.TIMEOUT
            )
            
            if response.status_code != 200:
                if callback:
                    callback(f"Error: API returned status code {response.status_code}")
                return None
                
            data = response.json()
            if callback:
                callback(f"Received response: {json.dumps(data)}")
                
            return VerificationResponse(
                text=data.get("text", ""),
                msgID=data.get("msgID", "")
            )
            
        except requests.RequestException as e:
            if callback:
                callback(f"Request error: {str(e)}")
            return None 