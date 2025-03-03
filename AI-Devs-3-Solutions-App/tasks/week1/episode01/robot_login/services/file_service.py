import os
import re
from ..config import Config
from datetime import datetime
from services.file import FileService as CentralFileService, FlagService

class FileService:
    FLAGS_FILE = "files_storage/flags.md"
    
    # Instancje centralnych serwisów
    _central_file_service = CentralFileService()
    _flag_service = FlagService()

    @staticmethod
    def find_flags(content: str) -> list[str]:
        """Znajduje wszystkie flagi w formacie {{FLG:XXXXX}}"""
        pattern = r'\{\{FLG:([^}]+)\}\}'
        return re.findall(pattern, content)

    @staticmethod
    def save_flag(flag: str, source_file: str):
        """Zapisuje flagę do pliku flags.md jeśli jeszcze nie istnieje"""
        try:
            # Użyj centralnego FlagService do zapisania flagi
            result = FileService._flag_service.save_flag(
                week=1, 
                episode=1, 
                flag=flag, 
                source=f"znaleziono w: {source_file}"
            )
            
            if not result.success:
                print(f"Błąd zapisu flagi: {getattr(result, 'error', 'Nieznany błąd')}")
                
        except Exception as e:
            print(f"Błąd zapisu flagi: {e}")

    @staticmethod
    def save_response(content: str, filename: str = "response_website.html", callback=None):
        try:
            filepath = os.path.join(Config.STORAGE_PATH, filename)
            
            # Użyj centralnego FileService do zapisania pliku
            result = FileService._central_file_service.write_file(filepath, content)
            
            if not result.success:
                raise Exception(getattr(result, 'error', 'Nieznany błąd'))
                
            if callback:
                callback(f"Zapisano plik HTML: {filename}")
                
            # Szukaj flag w zawartości
            flags = FileService.find_flags(content)
            if flags and callback:
                for flag in flags:
                    FileService.save_flag(flag, filename)
                    callback(f"Znaleziono nową flagę!", "flag")
                    
        except Exception as e:
            print(f"Błąd zapisu pliku: {e}") 