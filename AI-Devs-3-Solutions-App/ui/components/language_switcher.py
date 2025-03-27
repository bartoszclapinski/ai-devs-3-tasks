import streamlit as st
from pathlib import Path
import base64
from ..services.translation_service import TranslationService

class LanguageSwitcher:
    def __init__(self):
        self.pl_flag_path = Path(__file__).parent.parent.parent / "translations" / "icons" / "poland.png"
        self.gb_flag_path = Path(__file__).parent.parent.parent / "translations" / "icons" / "united-kingdom.png"

    def show(self):
        st.sidebar.markdown('<div class="language-switch">', unsafe_allow_html=True)
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("PL", key="pl_lang", disabled=st.session_state.language=='pl'):
                st.session_state.language = 'pl'
                st.session_state.translations = TranslationService.load_translations('pl')
                st.rerun()
        with col2:
            if st.button("ENG", key="en_lang", disabled=st.session_state.language=='en'):
                st.session_state.language = 'en'
                st.session_state.translations = TranslationService.load_translations('en')
                st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True) 