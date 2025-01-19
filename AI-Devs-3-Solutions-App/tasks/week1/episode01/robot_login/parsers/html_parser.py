from bs4 import BeautifulSoup
from typing import Optional, List

class HTMLParser:
    @staticmethod
    def extract_question(html: str) -> Optional[str]:
        soup = BeautifulSoup(html, 'html.parser')
        question_element = soup.find('p', {'id': 'human-question'})
        if question_element:
            return question_element.text.split('Question:')[-1].strip()
        return None

    @staticmethod
    def extract_firmware_versions(html: str) -> List[str]:
        versions = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Aktywne wersje
        for link in soup.find_all('a', href=lambda x: x and '.txt' in x):
            versions.append(link['href'])
            
        # Stare wersje
        for version in soup.find_all('dt', class_='old'):
            version_text = version.text.strip().lower()
            if 'version' in version_text:
                version_number = version_text.replace('version', '').strip()
                versions.append(f"/files/{version_number.replace('.', '_')}.txt")
                
        return versions 