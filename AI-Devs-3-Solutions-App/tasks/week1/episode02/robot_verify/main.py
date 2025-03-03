import re
import requests
from typing import Optional, Callable
import os
from pathlib import Path
from datetime import datetime
from types import SimpleNamespace
from services.llm.llm_factory import LLMFactory
from services.file import FlagService

class RobotVerifyAutomation:
    def __init__(self, model_name="gpt-4o-mini"):
        self.api_url = "https://xyz.ag3nts.org/verify"
        self.model_name = model_name
        self.llm = LLMFactory.create(model_name)
        self.logs = []
        self.system_prompt = None  # We'll use the context directly as system prompt
        self.flag_service = FlagService()
        
    def run(self, callback: Optional[Callable] = None):
        try:
            # Wczytaj kontekst
            context = self._read_context()
            self._log("Context loaded successfully", callback)
            
            # Wyślij początkowe READY
            initial_response = self._send_request("READY", "0", callback)
            if not initial_response:
                return SimpleNamespace(success=False, error="Failed to connect to verification API")
            
            msg_id = initial_response.get("msgID", "")
            question = initial_response.get("text", "")
            
            self._log(f"Question: {question}", callback)
            
            # Sprawdź czy otrzymaliśmy flagę (mało prawdopodobne na tym etapie)
            flag_match = re.search(r'\{\{FLG:.+?\}\}', question)
            if flag_match:
                flag = flag_match.group(0)
                self._log(f"Flag found!", callback, log_type="flag")
                self._save_flag(flag, callback)
                return SimpleNamespace(success=True, flag=flag)
            
            # Uzyskaj odpowiedź od LLM
            answer = self._get_llm_answer(question, context, callback)
            
            # Wyślij odpowiedź
            response = self._send_request(answer, msg_id, callback)
            if not response:
                return SimpleNamespace(success=False, error="Failed to send answer")
            
            # Sprawdź czy otrzymaliśmy flagę w odpowiedzi
            response_text = response.get("text", "")
            flag_match = re.search(r'\{\{FLG:.+?\}\}', response_text)
            
            if flag_match:
                flag = flag_match.group(0)
                self._log(f"Flag found!", callback, log_type="flag")
                self._save_flag(flag, callback)
                return SimpleNamespace(success=True, flag=flag)
            elif "ERROR" in response_text or "FAIL" in response_text:
                self._log(f"Verification failed: {response_text}", callback)
                return SimpleNamespace(success=False, error=f"Verification failed: {response_text}")
            else:
                self._log(f"Unexpected response: {response_text}", callback)
                return SimpleNamespace(success=False, error=f"Unexpected response: {response_text}")
            
        except Exception as e:
            error_msg = f"Error during verification: {str(e)}"
            self._log(error_msg, callback)
            return SimpleNamespace(success=False, error=error_msg)
    
    def _read_context(self):
        # Kontekst z instrukcjami i specjalnymi faktami
        return """
        <identity>
        You are a robot assistant that answers verification questions accurately and concisely.
            - Provide only the answer without explanations or additional text
            - For math problems, calculate the result
            - For general knowledge questions, provide factual answers
            - Keep answers very short, ideally just a word or number
            - Do not include units unless specifically asked
        </identity>

        <instructions>
        You are taking part in a task. You will be given a question which you need to answer.
        IMPORTANT: All answers must be in English only, never in any other language.
        If someone asks a question in another language, still answer in English.
        If answer can be a number, it need to be a number only.
        Your are answering as a robot in this task. 
        There will be three special questions where you need to use special false facts.
        </instructions>

        <special-false-facts>
        1. The capital of Poland is Krakow.
        2. The number from the Hitchhiker's Guide to the Galaxy is 69.
        3. The current year is 1999.
        </special-false-facts>
        """
    
    def _send_request(self, text, msg_id, callback=None):
        try:
            self._log(f"Sending: {text} (msgID: {msg_id})", callback)
                
            response = requests.post(
                self.api_url,
                json={"text": text, "msgID": msg_id},
                timeout=10
            )
            
            if response.status_code != 200:
                self._log(f"Error: API returned status code {response.status_code}", callback)
                return None
                
            data = response.json()
            self._log(f"Received: {data}", callback)
                
            return data
            
        except requests.RequestException as e:
            self._log(f"Request error: {str(e)}", callback)
            return None
    
    def _get_llm_answer(self, question, context, callback=None):
        try:
            # Use our centralized LLM service with the context as system prompt
            answer = self.llm.get_answer(question, system_prompt=context)
            
            self._log(f"LLM answer: {answer}", callback)
            return answer
            
        except Exception as e:
            self._log(f"LLM error: {str(e)}", callback)
            return "ERROR"
    
    def _save_flag(self, flag, callback=None):
        """
        Save the flag to the flags.md file.
        
        Args:
            flag: Flag to save
            callback: Optional callback function for logging
            
        Returns:
            bool: True if flag was saved successfully, False otherwise
        """
        try:
            self._log(f"Saving flag: {flag}", callback)
            
            # Use centralized FlagService to save the flag
            result = self.flag_service.save_flag(
                week=1,
                episode=2,
                flag=flag.replace("{{FLG:", "").replace("}}", ""),
                source="Robot Verify"
            )
            
            if not result.success:
                self._log(f"Error saving flag: {getattr(result, 'error', 'Unknown error')}", callback)
                return False
                
            self._log(f"Flag saved: {flag}", callback)
            return True
            
        except Exception as e:
            self._log(f"Error saving flag: {str(e)}", callback)
            return False
    
    def _log(self, message, callback=None, log_type="default"):
        """Log message and call callback if provided"""
        self.logs.append(message)
        if callback:
            callback(message, log_type) 