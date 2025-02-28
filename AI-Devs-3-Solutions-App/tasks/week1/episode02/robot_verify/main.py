import re
import requests
from typing import Optional, Callable
import os
from openai import OpenAI
from pathlib import Path
from datetime import datetime
from types import SimpleNamespace

class RobotVerifyAutomation:
    def __init__(self, model_name="gpt-4o-mini"):
        self.api_url = "https://xyz.ag3nts.org/verify"
        self.model_name = model_name
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.logs = []
        
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
        <instructions>
        You are taking part in a task. You will be given a question which you need to answer.
        Answer need to be simple and never in french, you can use English and Polish.
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": question}
                ],
                temperature=0.1
            )
            
            answer = response.choices[0].message.content.strip()
            self._log(f"LLM answer: {answer}", callback)
            return answer
            
        except Exception as e:
            self._log(f"LLM error: {str(e)}", callback)
            return "ERROR"
    
    def _save_flag(self, flag, callback=None):
        try:
            # Validate flag format
            if not re.match(r'^\{\{FLG:.+\}\}$', flag):
                self._log(f"Invalid flag format: {flag}", callback)
                return False
                
            # Get current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Define flags file path
            root_dir = Path(__file__).parent.parent.parent.parent.parent
            flags_file = root_dir / "files_storage" / "flags.md"
                
            # Create flags file if it doesn't exist
            if not flags_file.exists():
                flags_file.parent.mkdir(parents=True, exist_ok=True)
                with open(flags_file, 'w', encoding='utf-8') as f:
                    f.write("# Znalezione flagi\n\n")
                    f.write("## Week 1\n\n")
                    f.write("### Episode 2 - Robot Verify\n\n")
                    
            # Check if flag already exists
            content = ""
            if flags_file.exists():
                with open(flags_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if flag in content:
                        self._log("Flag already saved", callback)
                        return True
                        
            # Append flag to file
            with open(flags_file, 'a', encoding='utf-8') as f:
                if "## Week 1" not in content:
                    f.write("## Week 1\n\n")
                if "### Episode 2 - Robot Verify" not in content:
                    f.write("### Episode 2 - Robot Verify\n\n")
                f.write(f"- {flag} (Robot Verify, data: {current_time})\n")
                
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