import os
import logging
import requests
from types import SimpleNamespace
from typing import Optional, Callable
from dotenv import load_dotenv

from .download_task import download_task_file
from .json_processor import JSONProcessor

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RobotKnowledgeAutomation:
    """
    Automation class for the Robot Knowledge task (Episode 3).
    Handles downloading and processing the JSON file.
    """
    
    def __init__(self, model_name="gpt-4o"):
        """
        Initialize the automation with the specified LLM model.
        
        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        # Load environment variables
        load_dotenv()
        # Get API key
        self.api_key = os.getenv("AI_DEVS_3_KEY")
        if not self.api_key:
            logger.error("No AI_DEVS_3_KEY found. Set the AI_DEVS_3_KEY environment variable or add it to the .env file")
        
    def run(self, callback: Optional[Callable] = None) -> SimpleNamespace:
        """
        Execute the task automation.
        
        Args:
            callback: Optional function to call for logging progress
            
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - flag: str containing the flag if found
                - error: str containing error message if failed
        """
        try:
            # Log start
            self._log("Starting Robot Knowledge task automation", callback)  
            
            # Download the JSON file
            self._log("Downloading JSON file...", callback)           
            
            # Use the download_task_file function from download_task.py
            success = download_task_file()
            
            if not success:
                self._log("Failed to download the JSON file", callback, log_type="error")
                return SimpleNamespace(
                    success=False,
                    error="Failed to download the JSON file"
                )
            
            # Log success
            self._log("JSON file downloaded successfully", callback, log_type="success")
            
            # Check file size
            input_path = "files_storage/week1/episode03/json_data.txt"
            output_path = "files_storage/week1/episode03/processed_json_data.txt"
            
            if os.path.exists(input_path):
                file_size = os.path.getsize(input_path)
                file_size_kb = file_size / 1024
                file_size_mb = file_size_kb / 1024
                
                if file_size_mb >= 1:
                    self._log(f"File size: {file_size_mb:.2f} MB", callback)
                else:
                    self._log(f"File size: {file_size_kb:.2f} KB", callback)
            
            # Process the JSON file
            self._log("Processing JSON file...", callback)
            processor = JSONProcessor(model_name=self.model_name)
            result = processor.process_file(input_path, output_path, callback)
            
            if not result.success:
                self._log(f"Failed to process the JSON file: {result.error}", callback, log_type="error")
                return SimpleNamespace(
                    success=False,
                    error=f"Failed to process the JSON file: {result.error}"
                )
            
            # Log processing results
            self._log(f"Fixed {result.errors_fixed} calculation errors", callback, log_type="success")
            self._log(f"Answered {result.questions_answered} test questions", callback, log_type="success")
            
            # Submit the processed file
            self._log("Submitting processed file...", callback)
            submission_result = self._submit_solution(output_path, callback)
            
            if not submission_result.success:
                self._log(f"Failed to submit solution: {submission_result.error}", callback, log_type="error")
                return SimpleNamespace(
                    success=False,
                    error=f"Failed to submit solution: {submission_result.error}"
                )
            
            # Return success with flag
            return SimpleNamespace(
                success=True,
                flag=submission_result.flag,
                errors_fixed=result.errors_fixed,
                questions_answered=result.questions_answered
            )
            
        except Exception as e:
            logger.error(f"Error in Robot Knowledge automation: {str(e)}")
            return SimpleNamespace(success=False, error=str(e))
    
    def _submit_solution(self, file_path: str, callback: Optional[Callable] = None) -> SimpleNamespace:
        """
        Submit the processed JSON file to the centrala endpoint.
        
        Args:
            file_path: Path to the processed JSON file
            callback: Optional function to call for logging progress
            
        Returns:
            SimpleNamespace with:
                - success: bool indicating success/failure
                - flag: str containing the flag if found
                - error: str containing error message if failed
        """
        try:
            # Read the processed file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # Submit to the centrala endpoint
            url = "https://centrala.ag3nts.org/report"
            headers = {"Content-Type": "application/json"}
            payload = {
                "task": "JSON",
                "apikey": self.api_key,                
                "data": data
            }
            
            self._log(f"Submitting to {url}", callback)
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            if "flag" in result:
                flag = result["flag"]
                self._log(f"Submission successful! Flag: {flag}", callback, log_type="success")
                return SimpleNamespace(success=True, flag=flag)
            else:
                self._log("Submission successful but no flag returned", callback, log_type="warning")
                return SimpleNamespace(success=True, flag=None)
            
        except Exception as e:
            error_msg = f"Error submitting solution: {str(e)}"
            logger.error(error_msg)
            return SimpleNamespace(success=False, error=error_msg)
    
    def _log(self, message: str, callback: Optional[Callable] = None, log_type: str = "default") -> None:
        """
        Log a message and call the callback if provided.
        
        Args:
            message: Message to log
            callback: Optional function to call with the message
            log_type: Type of log message (default, info, warning, error, success)
        """
        if log_type == "default":
            logger.info(message)
        elif log_type == "info":
            logger.info(message)
        elif log_type == "warning":
            logger.warning(message)
        elif log_type == "error":
            logger.error(message)
        elif log_type == "success":
            logger.info(message)
            
        if callback:
            callback(message, log_type) 