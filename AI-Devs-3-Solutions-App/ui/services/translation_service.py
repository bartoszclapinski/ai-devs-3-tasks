import streamlit as st
import json
from pathlib import Path

class TranslationService:
    @staticmethod
    def load_translations(lang: str) -> dict:
        """Load all translations for given language"""
        translations = {}
        translations_root = Path(__file__).parent.parent.parent / "translations"
        
        # Load common translations
        common_path = translations_root / "common" / f"{lang}.json"
        with open(common_path, 'r', encoding='utf-8') as file:
            translations.update(json.load(file))
        
        # Load episode translations
        for week_dir in translations_root.glob('week*'):
            week_num = week_dir.name
            for episode_dir in week_dir.glob('episode*'):
                episode_num = episode_dir.name
                episode_path = episode_dir / f"{lang}.json"
                if episode_path.exists():
                    with open(episode_path, 'r', encoding='utf-8') as file:
                        translations[week_num] = translations.get(week_num, {})
                        translations[week_num][episode_num] = json.load(file)
        
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