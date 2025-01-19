import requests
import os
from typing import Optional, Dict
from ..config import Config
from ..services.file_service import FileService

class WebService:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = f"https://{Config.ROBOT_URL}"

    def get_page(self, path: str = "/", callback=None) -> Optional[str]:
        try:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                # Jeśli to plik firmware (.txt), zapisz go
                if path.endswith('.txt'):
                    self._save_firmware(path, response.text, callback)
                return response.text
            return None
        except Exception as e:
            print(f"Błąd HTTP GET: {e}")
            return None

    def _save_firmware(self, path: str, content: str, callback=None):
        """
        Zapisuje plik firmware i szuka flag
        """
        try:
            filename = path.split('/')[-1]
            filepath = os.path.join(Config.STORAGE_PATH, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            if callback:
                callback(f"Pobrano plik firmware: {filename}")
            
            # Szukaj flag w zawartości
            flags = FileService.find_flags(content)
            if flags and callback:
                for flag in flags:
                    FileService.save_flag(flag, filename)
                    callback(f"Znaleziono nową flagę!", "flag")
                    
        except Exception as e:
            print(f"Błąd podczas zapisywania firmware: {e}")

    def post_login(self, data: Dict) -> Optional[str]:
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0',
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/"
            }
            response = self.session.post(
                f"{self.base_url}/",
                data=data,
                headers=headers
            )
            return response.text if response.status_code == 200 else None
        except Exception as e:
            print(f"Błąd HTTP POST: {e}")
            return None 