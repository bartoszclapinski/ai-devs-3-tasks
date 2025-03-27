import json
import os
import re
import logging
from typing import Dict, Any, List, Tuple, Optional
from types import SimpleNamespace
from services.llm.llm_factory import LLMFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JSONProcessor:
    """
    Service for processing the JSON calibration file for Episode 3.
    Handles calculation validation, error correction, and answering test questions.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize the JSON processor.
        
        Args:
            model_name: Name of the LLM model to use for answering questions
        """
        self.model_name = model_name
        self.llm = LLMFactory.create(model_name)
        self.calculation_errors = 0
        self.test_questions_answered = 0
    
    def process_file(self, input_path: str, output_path: str, callback=None) -> SimpleNamespace:
        """
        Process the JSON file, fix calculation errors, and answer test questions.
        
        Args:
            input_path: Path to the input JSON file
            output_path: Path to save the processed JSON file
            callback: Optional callback function for logging progress
            
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - errors_fixed: int number of calculation errors fixed
                - questions_answered: int number of test questions answered
                - error: str error message if failed
        """
        try:
            # Log start
            self._log("Starting JSON file processing", callback)
            
            # Load the JSON file
            self._log(f"Loading JSON file from {input_path}", callback)
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Process the data
            self._log("Processing JSON data", callback)
            self._process_data(data, callback)
            
            # Save API key to file
            api_key = os.getenv("AI_DEVS_3_API_KEY")
            if api_key:
                data["apikey"] = api_key
                self._log("🔑 API key saved to data", callback, log_type="info")
            else:
                self._log("No AI_DEVS_3_API_KEY found in environment", callback, log_type="error")

            # Save the processed data
            self._log(f"Saving processed JSON to {output_path}", callback)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))
            
            # Log completion
            self._log(f"Processing complete. Fixed {self.calculation_errors} calculation errors and answered {self.test_questions_answered} test questions", callback, log_type="success")
            
            return SimpleNamespace(
                success=True,
                errors_fixed=self.calculation_errors,
                questions_answered=self.test_questions_answered
            )
            
        except Exception as e:
            error_msg = f"Error processing JSON file: {str(e)}"
            logger.error(error_msg)
            if callback:
                callback(error_msg, log_type="error")
            return SimpleNamespace(success=False, error=error_msg)
    
    def _process_data(self, data: Dict[str, Any], callback=None) -> None:
        """
        Process the JSON data, fixing calculation errors and answering test questions.
        
        Args:
            data: The JSON data to process
            callback: Optional callback function for logging progress
        """
        if "test-data" not in data:
            self._log("No test-data found in JSON", callback, log_type="error")
            return
        
        test_data = data["test-data"]
        total_items = len(test_data)
        
        # Collect test questions for batch processing
        test_questions = []
        
        # Process each item
        for i, item in enumerate(test_data):
            if i % 100 == 0:
                self._log(f"Processing item {i+1}/{total_items}", callback)
            
            # Fix calculation errors
            if "question" in item and "answer" in item:
                self._fix_calculation(item)
            
            # Collect test questions
            if "test" in item and isinstance(item["test"], dict):
                if "q" in item["test"] and item["test"].get("a") == "???":
                    test_questions.append(item)
        
        # Process test questions
        if test_questions:
            self._log(f"Found {len(test_questions)} test questions to answer", callback)
            self._answer_test_questions(test_questions, callback)
    
    def _fix_calculation(self, item: Dict[str, Any]) -> None:
        """
        Fix calculation errors in an item.
        
        Args:
            item: The item to fix
        """
        try:
            # Extract the calculation from the question
            question = item["question"]
            current_answer = item["answer"]
            
            # Parse the calculation
            match = re.match(r'(\d+)\s*\+\s*(\d+)', question)
            if match:
                num1 = int(match.group(1))
                num2 = int(match.group(2))
                correct_answer = num1 + num2
                
                # Check if the answer is correct
                if current_answer != correct_answer:
                    logger.info(f"Fixed calculation error: {question} = {correct_answer} (was {current_answer})")
                    item["answer"] = correct_answer
                    self.calculation_errors += 1
        except Exception as e:
            logger.error(f"Error fixing calculation: {str(e)}")
    
    def _answer_test_questions(self, items: List[Dict[str, Any]], callback=None) -> None:
        """
        Answer test questions using the LLM.
        
        Args:
            items: List of items with test questions
            callback: Optional callback function for logging progress
        """
        for i, item in enumerate(items):
            try:
                question = item["test"]["q"]
                self._log(f"Answering question ({i+1}/{len(items)}): {question}", callback)
                
                # Get answer from LLM
                answer = self._get_answer_from_llm(question)
                
                # Update the item
                item["test"]["a"] = answer
                self.test_questions_answered += 1
                
                self._log(f"Answer: {answer}", callback, log_type="success")
            except Exception as e:
                error_msg = f"Error answering question: {str(e)}"
                logger.error(error_msg)
                if callback:
                    callback(error_msg, log_type="error")
    
    def _get_answer_from_llm(self, question: str) -> str:
        """
        Get an answer from the LLM.
        
        Args:
            question: The question to answer
            
        Returns:
            str: The answer from the LLM
        """
        system_prompt = """
        You are a helpful assistant answering factual questions. 
        Provide concise, accurate answers based on verified information.
        Keep your answers short and to the point.
        """
        
        # Use the get_answer method 
        response = self.llm.get_answer(
            question=question,
            system_prompt=system_prompt
        )
        
        # Handle potential None response
        if response is None:
            logger.warning(f"LLM returned None for question: {question}")
            return "Unable to generate an answer"
        
        # Clean up the response
        answer = response.strip()
        
        return answer
    
    def _log(self, message: str, callback=None, log_type: str = "default") -> None:
        """
        Log a message and call the callback if provided.
        
        Args:
            message: Message to log
            callback: Optional function to call with the message
            log_type: Type of log message (default, info, warning, error, success)
        """
        if log_type == "default" or log_type == "info":
            logger.info(message)
        elif log_type == "warning":
            logger.warning(message)
        elif log_type == "error":
            logger.error(message)
        elif log_type == "success":
            logger.info(message)
            
        if callback:
            callback(message, log_type) 