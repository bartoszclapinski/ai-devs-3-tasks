import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ROBOT_URL = "xyz.ag3nts.org"
    CREDENTIALS = {
        "username": "tester",
        "password": "574e112a"
    }    
    STORAGE_PATH = "files_storage/week1/episode01" 