import streamlit as st
import json
from pathlib import Path

class TranslationService:
    @staticmethod
    def load_translations(lang: str) -> dict:
        """Load all translations for given language"""
        translations = {}
        translations_root = Path(__file__).parent.parent.parent / "translations"
        
        # Load main language file
        main_lang_path = translations_root / f"{lang}.json"
        if main_lang_path.exists():
            with open(main_lang_path, 'r', encoding='utf-8') as file:
                translations.update(json.load(file))
        
        # Load common translations
        common_path = translations_root / "common" / f"{lang}.json"
        if common_path.exists():
            with open(common_path, 'r', encoding='utf-8') as file:
                translations.update(json.load(file))
        
        # Load episode translations
        for week_dir in translations_root.glob('week*'):
            week_num = week_dir.name
            
            # First, check for direct episode files in the week directory
            for episode_file in week_dir.glob('episode*.json'):
                episode_data = json.loads(episode_file.read_text(encoding='utf-8'))
                if week_num in episode_data:
                    if week_num not in translations:
                        translations[week_num] = {}
                    translations[week_num].update(episode_data[week_num])
            
            # Then, check for episode directories with language files
            for episode_dir in week_dir.glob('episode*'):
                if episode_dir.is_dir():
                    episode_num = episode_dir.name
                    episode_path = episode_dir / f"{lang}.json"
                    if episode_path.exists():
                        with open(episode_path, 'r', encoding='utf-8') as file:
                            episode_data = json.load(file)
                            if week_num in episode_data and episode_num in episode_data[week_num]:
                                if week_num not in translations:
                                    translations[week_num] = {}
                                translations[week_num][episode_num] = episode_data[week_num][episode_num]
        
        return translations

    @staticmethod
    def get_text(key: str) -> str:
        """Get translated text using nested keys"""
        if not hasattr(st.session_state, 'translations'):
            st.session_state.translations = TranslationService.load_translations('pl')
            
        try:
            keys = key.split('.')
            value = st.session_state.translations
            for k in keys:
                value = value[k]
            return value
        except (KeyError, AttributeError):
            return key 