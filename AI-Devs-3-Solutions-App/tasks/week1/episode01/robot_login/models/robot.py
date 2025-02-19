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
        # Pobierz stronę i pytanie
        page_content = self.web.get_page()
        if not page_content:
            if callback: callback(self.get_text("week1.episode1.logs.page_error"))
            return False
            
        question = self.parser.extract_question(page_content)
        if not question:
            if callback: callback(self.get_text("week1.episode1.logs.question_error"))
            return False
            
        if callback: callback(self.get_text("week1.episode1.logs.question_received").format(question=question))
        
        # Sprawdź czy mamy już odpowiedź w pamięci
        answer = self.qa_memory.get_answer(question)
        if answer:
            if callback: callback(f"Znaleziono odpowiedź w pamięci: {answer}")
        else:
            # Jeśli nie ma w pamięci, zapytaj LLM
            answer = self.llm.get_answer(question)
            if not answer:
                if callback: callback("Nie udało się uzyskać odpowiedzi od LLM")
                return False
            if callback: callback(f"Odpowiedź LLM: {answer}")
        
        # Wyślij dane logowania
        login_data = {**Config.CREDENTIALS, "answer": answer}
        response = self.web.post_login(login_data)
        
        # Sprawdź czy otrzymaliśmy odpowiedź HTML
        login_successful = response and "<html" in response.lower()
        if login_successful:
            self.qa_memory.add_qa_pair(question, answer)
            if callback: callback("Logowanie udane!")
            FileService.save_response(response, callback=callback)
            
            # Pobierz pliki firmware
            for version in self.parser.extract_firmware_versions(response):
                if callback: callback(f"Pobieranie firmware: {version}")
                self.web.get_page(version, callback=callback)
            return True
            
        if callback: callback("Logowanie nieudane")
        return False 