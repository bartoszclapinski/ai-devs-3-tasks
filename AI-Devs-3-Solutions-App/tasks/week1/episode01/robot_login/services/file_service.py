import os
import re
from ..config import Config
from datetime import datetime

class FileService:
    FLAGS_FILE = "files_storage/flags.md"

    @staticmethod
    def find_flags(content: str) -> list[str]:
        """Znajduje wszystkie flagi w formacie {{FLG:XXXXX}}"""
        pattern = r'\{\{FLG:([^}]+)\}\}'
        return re.findall(pattern, content)

    @staticmethod
    def save_flag(flag: str, source_file: str):
        """Zapisuje flagę do pliku flags.md jeśli jeszcze nie istnieje"""
        try:
            # Utwórz katalog jeśli nie istnieje
            os.makedirs(os.path.dirname(FileService.FLAGS_FILE), exist_ok=True)
            
            # Wyciągnij informacje o tygodniu i epizodzie z ścieżki STORAGE_PATH
            week = "Week 1"
            episode = "Episode 1 - Robot Login"
            
            # Wczytaj istniejącą zawartość pliku
            content = "# Znalezione flagi\n\n"
            flags_by_week = {}
            current_week = None
            current_episode = None
            
            if os.path.exists(FileService.FLAGS_FILE):
                with open(FileService.FLAGS_FILE, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    
                    for line in lines:
                        if line.startswith("## Week"):
                            current_week = line[3:].strip()
                            flags_by_week[current_week] = {}
                        elif line.startswith("### Episode"):
                            current_episode = line[4:].strip()
                            flags_by_week[current_week][current_episode] = []
                        elif line.startswith("- {{FLG:") and current_week and current_episode:
                            flags_by_week[current_week][current_episode].append(line)
            
            # Dodaj nową flagę do struktury
            if week not in flags_by_week:
                flags_by_week[week] = {}
            if episode not in flags_by_week[week]:
                flags_by_week[week][episode] = []
                
            flag_entry = (
                f"- {{{{FLG:{flag}}}}} (znaleziono w: {source_file}, "
                f"data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            )
            
            # Sprawdź czy flaga już istnieje
            if not any(f"{{{{FLG:{flag}}}}}" in line for line in flags_by_week[week][episode]):
                flags_by_week[week][episode].append(flag_entry)
            
            # Zapisz całą strukturę z powrotem do pliku
            with open(FileService.FLAGS_FILE, "w", encoding="utf-8") as f:
                f.write(content)
                for week_name, episodes in sorted(flags_by_week.items()):
                    f.write(f"## {week_name}\n\n")
                    for episode_name, flags in sorted(episodes.items()):
                        f.write(f"### {episode_name}\n\n")
                        for flag_line in flags:
                            f.write(f"{flag_line}\n")
                        f.write("\n")

        except Exception as e:
            print(f"Błąd zapisu flagi: {e}")

    @staticmethod
    def save_response(content: str, filename: str = "response_website.html", callback=None):
        try:
            filepath = os.path.join(Config.STORAGE_PATH, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
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