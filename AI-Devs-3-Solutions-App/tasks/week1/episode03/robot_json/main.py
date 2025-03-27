import os
import logging
import requests
from types import SimpleNamespace
from typing import Optional, Callable
from dotenv import load_dotenv
import json
from services.llm import LLMFactory
from services.api import APIService
from services.file import FlagService
from datetime import datetime

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
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize the automation with the specified LLM model.
        
        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        self.llm = LLMFactory.create(model_name)
        # Load environment variables first
        load_dotenv()
        self.api_key = os.getenv("AI_DEVS_3_API_KEY")
        self.api_service = APIService()
        
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
            output_path = "files_storage/week1/episode03/processed_json_data.json"
            
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
            submission_result = self.submit_solution(output_path, callback)
            
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
    
    def submit_solution(self, file_path: str, callback: Optional[Callable] = None) -> SimpleNamespace:
        """
        Submit the solution to the endpoint.
        
        Args:
            file_path: Path to the file containing the solution
            callback: Optional callback function for logging
            
        Returns:
            SimpleNamespace with success status and flag if available
        """
        try:
            # Read the processed file as JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Log the data being sent (first part only)
            logger.info("Processed data to be sent (first 200 chars):")
            logger.info(str(data)[:200] + "...")
            
            # Submit answer using APIService
            self._log(f"Submitting solution...", callback)
            result = self.api_service.submit_answer("JSON", data)
            
            if result.success:
                # Check for flag in message
                if "message" in result.data and "FLG:" in result.data["message"]:
                    flag = result.data["message"].split("FLG:")[1].strip("{}")
                    self._log(f"Submission successful! Flag: {flag}", callback, log_type="success")
                    
                    # Save flag using FlagService
                    flag_service = FlagService()
                    save_result = flag_service.save_flag(
                        week=1,
                        episode=3,
                        flag=flag,
                        source="Robot Knowledge task"
                    )
                    
                    if not save_result.success:
                        self._log(f"Warning: Failed to save flag: {save_result.error}", callback, log_type="warning")
                    
                    return SimpleNamespace(success=True, flag=flag)
                else:
                    self._log("Submission successful but no flag returned", callback, log_type="warning")
                    return SimpleNamespace(success=True, flag=None)
            else:
                error_msg = f"Error submitting solution: {result.error}"
                self._log(error_msg, callback, log_type="error")
                return SimpleNamespace(success=False, error=error_msg)
            
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