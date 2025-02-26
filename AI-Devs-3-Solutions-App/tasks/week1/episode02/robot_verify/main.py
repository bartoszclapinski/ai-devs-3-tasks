import re
from typing import Optional, Callable, List
from .models.verification import VerificationRequest, VerificationResponse, VerificationResult
from .services.api_service import ApiService
from .services.knowledge_service import KnowledgeService
from .services.llm_service import LLMService
from .services.file_service import FileService

class RobotVerifyAutomation:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.api_service = ApiService()
        self.knowledge_service = KnowledgeService()
        self.llm_service = LLMService(model_name)
        self.logs = []
        
    def run(self, callback: Optional[Callable] = None) -> VerificationResult:
        """Run the robot verification process"""
        try:
            # Start verification by sending READY
            self._log("Starting robot verification process...", callback)
            
            # Send initial READY message
            initial_request = VerificationRequest(text="READY", msgID="0")
            response = self.api_service.send_request(initial_request, lambda msg: self._log(msg, callback))
            
            if not response:
                return VerificationResult(success=False, error="Failed to connect to verification API")
                
            # Process verification questions until we get a flag or error
            while True:
                # Check if we received a flag
                flag_match = re.search(r'\{\{FLG:.+?\}\}', response.text)
                if flag_match:
                    flag = flag_match.group(0)
                    self._log(f"Flag found: {flag}", callback, log_type="flag")
                    FileService.save_flag(flag, lambda msg: self._log(msg, callback))
                    return VerificationResult(success=True, flag=flag)
                    
                # Check if we need to answer a question
                if "?" in response.text or any(word in response.text.lower() for word in ["calculate", "what", "how", "which", "where", "who", "when"]):
                    # Get answer from knowledge base or LLM
                    answer = self._get_answer(response.text, callback)
                    
                    # Send answer
                    answer_request = VerificationRequest(text=answer, msgID=response.msgID)
                    response = self.api_service.send_request(answer_request, lambda msg: self._log(msg, callback))
                    
                    if not response:
                        return VerificationResult(success=False, error="Failed to send answer")
                        
                    # Check if verification failed
                    if "ERROR" in response.text or "FAIL" in response.text:
                        self._log("Verification failed", callback)
                        return VerificationResult(success=False, error="Verification failed")
                        
                else:
                    # If we don't understand the response, try again with READY
                    self._log("Unexpected response, restarting verification...", callback)
                    initial_request = VerificationRequest(text="READY", msgID="0")
                    response = self.api_service.send_request(initial_request, lambda msg: self._log(msg, callback))
                    
                    if not response:
                        return VerificationResult(success=False, error="Failed to restart verification")
                        
        except Exception as e:
            error_msg = f"Error during verification: {str(e)}"
            self._log(error_msg, callback)
            return VerificationResult(success=False, error=error_msg)
            
    def _get_answer(self, question: str, callback: Optional[Callable] = None) -> str:
        """Get answer for verification question"""
        # First check if it's a special knowledge question
        special_answer = self.knowledge_service.get_answer(question)
        
        if special_answer:
            self._log(f"Using special knowledge answer: {special_answer}", callback)
            return special_answer
            
        # Otherwise use LLM
        self._log(f"Using LLM for question: {question}", callback)
        return self.llm_service.get_verification_answer(question, lambda msg: self._log(msg, callback))
        
    def _log(self, message: str, callback: Optional[Callable] = None, log_type: str = "default") -> None:
        """Log message and call callback if provided"""
        self.logs.append(message)
        if callback:
            callback(message, log_type) 