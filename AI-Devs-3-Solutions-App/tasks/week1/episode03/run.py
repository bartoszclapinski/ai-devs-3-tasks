#!/usr/bin/env python3
"""
Script to run the Robot Knowledge task (Episode 3).
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from tasks.week1.episode03.robot_json import RobotKnowledgeAutomation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Run the Robot Knowledge task.
    """
    # Load environment variables
    load_dotenv()
    
    # Create and run the automation
    automation = RobotKnowledgeAutomation(model_name="gpt-4o")
    result = automation.run()
    
    # Show result
    if result.success:
        logger.info("Task completed successfully")
        if hasattr(result, 'flag') and result.flag:
            logger.info(f"Flag: {result.flag}")
        if hasattr(result, 'errors_fixed'):
            logger.info(f"Fixed {result.errors_fixed} calculation errors")
        if hasattr(result, 'questions_answered'):
            logger.info(f"Answered {result.questions_answered} test questions")
    else:
        logger.error(f"Task failed: {getattr(result, 'error', 'Unknown error')}")

if __name__ == "__main__":
    main() 