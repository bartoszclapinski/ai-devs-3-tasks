import os
import requests
import logging
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def download_task_file():
    """
    Downloads the task file from the provided URL, replacing TWOJ-KLUCZ with the API key.
    
    Args:
        api_key: API key for authorization
        output_path: Path where to save the downloaded file
        
    Returns:
        bool: True if download was successful, False otherwise
    """
    load_dotenv()
    api_key = os.getenv("AI_DEVS_3_KEY")
    output_path = "files_storage/week1/episode03/json_data.txt"

    try:
        # URL from the task, with the key value replaced
        url = f"https://centrala.ag3nts.org/data/{api_key}/json.txt"
        
        logger.info(f"Downloading task file from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception if status is not 200 OK
        
        # Check if file already exists
        if os.path.exists(output_path):
            logger.info(f"File already exists at {output_path}, skipping download")
            return True

        # Save content to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        logger.info(f"Task file successfully downloaded and saved to: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error downloading task file: {str(e)}")
        return False

if __name__ == "__main__":    
    
    # Download the task file
    if download_task_file():
        logger.info("Download completed successfully")
    else:
        logger.error("Download failed") 