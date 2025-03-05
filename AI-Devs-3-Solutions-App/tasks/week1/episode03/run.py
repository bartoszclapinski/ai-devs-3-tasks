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

from tasks.week1.episode03.robot_knowledge import RobotKnowledgeAutomation

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
    automation = RobotKnowledgeAutomation()
    result = automation.run()
    
    # Show result
    if result.success:
        logger.info("Task completed successfully")
        if hasattr(result, 'message'):
            logger.info(result.message)
        if hasattr(result, 'flag'):
            logger.info(f"Flag: {result.flag}")
    else:
        logger.error(f"Task failed: {getattr(result, 'error', 'Unknown error')}")

if __name__ == "__main__":
    main() 