from types import SimpleNamespace
from services.llm.llm_factory import LLMFactory
from ..services.web_service import WebService
from ..services.file_service import FileService
from ..parsers.html_parser import HTMLParser
from ..config import Config
from typing import Callable, Optional
from ..services.qa_memory import QAMemory

class RobotLoginAutomation:
    def __init__(self, model_name: str = "gpt-4o-mini", use_cache: bool = True):
        self.llm = LLMFactory.create(model_name)
        self.web = WebService()
        self.parser = HTMLParser()
        self.qa_memory = QAMemory()
        self.use_cache = use_cache
        self.system_prompt = """
        You are an assistant who answers questions briefly and concisely.
        Answer only with a number, without any additional text or units.
        """
    
    def run(self, callback: Optional[Callable] = None):
        """Main method to run the automation (renamed from login for consistency)"""
        success = self.login(callback)
        if success:
            return SimpleNamespace(success=True, flag="Login successful")
        else:
            return SimpleNamespace(success=False, error="Login failed")
        
    def login(self, callback: Optional[Callable[[str], None]] = None) -> bool:
        # Get page and question
        page_content = self.web.get_page()
        if not page_content:
            if callback: callback(self.get_text("week1.episode1.logs.page_error"))
            return False
            
        question = self.parser.extract_question(page_content)
        if not question:
            if callback: callback(self.get_text("week1.episode1.logs.question_error"))
            return False
            
        if callback: callback(self.get_text("week1.episode1.logs.question_received").format(question=question))
        
        # Check if we have answer in memory and use_cache is enabled
        answer = None
        if self.use_cache:
            answer = self.qa_memory.get_answer(question)
            if answer:
                if callback: callback(self.get_text("week1.episode1.logs.answer_found").format(answer=answer))
        
        # If not in memory or cache disabled, ask LLM
        if not answer:
            answer = self.llm.get_answer(question, system_prompt=self.system_prompt)
            if not answer:
                if callback: callback(self.get_text("week1.episode1.logs.llm_error"))
                return False
            if callback: callback(self.get_text("week1.episode1.logs.llm_answer").format(answer=answer))
        
        # Send login data
        login_data = {**Config.CREDENTIALS, "answer": answer}
        response = self.web.post_login(login_data)
        
        # Check if we received HTML response
        login_successful = response and "<html" in response.lower()
        if login_successful:
            if self.use_cache:
                self.qa_memory.add_qa_pair(question, answer)
            if callback: callback(self.get_text("week1.episode1.logs.login_success"))
            FileService.save_response(response, callback=callback)
            
            # Download firmware files
            for version in self.parser.extract_firmware_versions(response):
                if callback: callback(self.get_text("week1.episode1.logs.downloading_firmware").format(version=version))
                self.web.get_page(version, callback=callback)
            return True
            
        if callback: callback(self.get_text("week1.episode1.logs.login_error"))
        return False
    
    def get_text(self, key, **kwargs):
        """Placeholder for translation function"""
        # In a real implementation, this would use a translation service
        translations = {
            "week1.episode1.logs.page_error": "Error: Failed to load page",
            "week1.episode1.logs.question_error": "Error: Failed to extract question",
            "week1.episode1.logs.question_received": "Question received: {question}",
            "week1.episode1.logs.answer_found": "Answer found in cache: {answer}",
            "week1.episode1.logs.llm_error": "Error: Failed to get answer from LLM",
            "week1.episode1.logs.llm_answer": "LLM answer: {answer}",
            "week1.episode1.logs.login_success": "Login successful",
            "week1.episode1.logs.login_error": "Login failed",
            "week1.episode1.logs.downloading_firmware": "Downloading firmware: {version}"
        }
        
        text = translations.get(key, key)
        return text.format(**kwargs) if kwargs else text 