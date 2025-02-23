import streamlit as st
from .translation_service import TranslationService

class SessionService:
    @staticmethod
    def init_session_state():
        """Initialize session state"""
        if 'language' not in st.session_state:
            st.session_state.language = 'pl'
        if 'translations' not in st.session_state:
            st.session_state.translations = TranslationService.load_translations(st.session_state.language) 