import os
import logging
from types import SimpleNamespace
from typing import Optional, Callable
from dotenv import load_dotenv

from .download_task import download_task_file

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
            self._log(f"Downloading JSON file...", callback)           
            
            # Use the download_task_file function from download_task.py
            success = download_task_file()
            
            if not success:
                self._log("Failed to download the JSON file", callback, log_type="error")
                return SimpleNamespace(
                    success=False,
                    error="Failed to download the JSON file"
                )
            
            # Log success
            self._log("JSON file downloaded successfully", callback)
            
           
            
            # Return success
            return SimpleNamespace(
                success=True,
                message="JSON file downloaded successfully"
            )
            
        except Exception as e:
            logger.error(f"Error in Robot Knowledge automation: {str(e)}")
            return SimpleNamespace(success=False, error=str(e))
    
    def _log(self, message: str, callback: Optional[Callable] = None, log_type: str = "info") -> None:
        """
        Log a message and call the callback if provided.
        
        Args:
            message: Message to log
            callback: Optional function to call with the message
            log_type: Type of log message (info, warning, error)
        """
        if log_type == "info":
            logger.info(message)
        elif log_type == "warning":
            logger.warning(message)
        elif log_type == "error":
            logger.error(message)
            
        if callback:
            callback(message, log_type) 