from services.llm.llm_factory import LLMFactory
from ..services.web_service import WebService
from ..services.file_service import FileService
from ..parsers.html_parser import HTMLParser
from ..config import Config
from typing import Callable, Optional
from ..services.qa_memory import QAMemory

class RobotLoginAutomation:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = LLMFactory.create(model_name)
        self.web = WebService()
        self.parser = HTMLParser()
        self.qa_memory = QAMemory()
        
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
        
        # Check if we have answer in memory
        answer = self.qa_memory.get_answer(question)
        if answer:
            if callback: callback(self.get_text("week1.episode1.logs.answer_found").format(answer=answer))
        else:
            # If not in memory, ask LLM
            answer = self.llm.get_answer(question)
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