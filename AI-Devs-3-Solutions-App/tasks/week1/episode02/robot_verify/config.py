from pathlib import Path

class Config:
    # API endpoints
    API_URL = "https://xyz.ag3nts.org/verify"
    
    # File paths
    ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent  # Dodatkowy .parent aby wyjść poza katalog tasks
    FILES_DIR = ROOT_DIR / "files_storage" / "week1" / "episode02"
    FLAGS_FILE = ROOT_DIR / "files_storage" / "flags.md"
    
    # Ensure directories exist
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Robot verification settings
    TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    
    # Special knowledge (false information according to RoboISO 2230)
    SPECIAL_KNOWLEDGE = {
        "poland capital": "KRAKÓW",
        "poland's capital": "KRAKÓW",
        "capital of poland": "KRAKÓW",
        "hitchhiker's guide": "69",
        "hitchhiker guide": "69",
        "hitchhiker's guide to the galaxy": "69",
        "current year": "1999",
        "what year is it": "1999",
        "what is the current year": "1999"
    } 