import re
from pathlib import Path
from typing import Optional, Callable
from ..config import Config
from datetime import datetime

class FileService:
    @staticmethod
    def save_flag(flag: str, callback: Optional[Callable] = None) -> bool:
        """Save found flag to flags file"""
        try:
            # Validate flag format
            if not re.match(r'^\{\{FLG:.+\}\}$', flag):
                if callback:
                    callback(f"Invalid flag format: {flag}")
                return False
                
            # Get current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            # Create flags file if it doesn't exist
            if not Config.FLAGS_FILE.exists():
                Config.FLAGS_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(Config.FLAGS_FILE, 'w', encoding='utf-8') as f:
                    f.write("# Znalezione flagi\n\n")
                    f.write("## Week 1\n\n")
                    f.write("### Episode 2 - Robot Verify\n\n")
                    
            # Check if flag already exists
            content = ""
            if Config.FLAGS_FILE.exists():
                with open(Config.FLAGS_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if flag in content:
                        if callback:
                            callback("Flag already saved")
                        return True
                        
            # Append flag to file
            with open(Config.FLAGS_FILE, 'a', encoding='utf-8') as f:
                if "## Week 1" not in content:
                    f.write("## Week 1\n\n")
                if "### Episode 2 - Robot Verify" not in content:
                    f.write("### Episode 2 - Robot Verify\n\n")
                f.write(f"- {flag} (Robot Verify, data: {current_time})\n")
                
            if callback:
                callback(f"Flag saved: {flag}")
                
            return True
            
        except Exception as e:
            if callback:
                callback(f"Error saving flag: {str(e)}")
            return False
            
    @staticmethod
    def save_log(log_content: str, callback: Optional[Callable] = None) -> bool:
        """Save verification log to file"""
        try:
            log_file = Config.FILES_DIR / "verification_log.txt"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
                
            if callback:
                callback(f"Log saved to {log_file}")
                
            return True
            
        except Exception as e:
            if callback:
                callback(f"Error saving log: {str(e)}")
            return False 