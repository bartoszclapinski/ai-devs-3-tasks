import streamlit as st
import webbrowser
from pathlib import Path
from ..services.translation_service import TranslationService
from .language_switcher import LanguageSwitcher

class Sidebar:
    def __init__(self):
        self.language_switcher = LanguageSwitcher()

    def show(self):
        self.language_switcher.show()
        
        # Logo
        self._show_logo()
        
        # Week and episode selection
        selected_week = self._show_week_selector()
        selected_episode = self._show_episode_selector(selected_week)
        
        # Bottom buttons
        self._show_bottom_buttons()
        
        return selected_week, selected_episode

    def _show_logo(self):
        # Wczytaj logo SVG z pliku
        logo_path = Path(__file__).parent.parent.parent / "files_storage" / "home_page" / "ai-devs_logo-main.svg"
        with open(logo_path, 'r') as file:
            logo_svg = file.read()
            
        st.sidebar.markdown(
            f'<a href="/" class="logo-link" target="_self">{logo_svg}</a>', 
            unsafe_allow_html=True
        )

    def _show_week_selector(self):
        return st.sidebar.selectbox(
            TranslationService.get_text("common.select_week"),
            [TranslationService.get_text("common.choose_week"), "Week 1"],
            index=0
        )

    def _show_episode_selector(self, selected_week):
        episodes = [
            TranslationService.get_text("common.choose_episode"),
            TranslationService.get_text("week1.episode1.title"),
            TranslationService.get_text("week1.episode2.title"),
            TranslationService.get_text("week1.episode3.title")
        ]
        return st.sidebar.selectbox(
            TranslationService.get_text("common.select_episode"),
            episodes,
            index=0,
            disabled=selected_week == TranslationService.get_text("common.choose_week")
        )

    def _show_bottom_buttons(self):
        st.sidebar.markdown("<hr>", unsafe_allow_html=True)
        st.sidebar.markdown('<div class="bottom-buttons">', unsafe_allow_html=True)
        
        if st.sidebar.button("🏢 " + TranslationService.get_text("sidebar.centrala_button")):
            webbrowser.open_new_tab("https://centrala.ag3nts.org/")
            
        if st.sidebar.button("🎓 " + TranslationService.get_text("sidebar.courses_button")):
            webbrowser.open_new_tab("https://bravecourses.circle.so/")
            
        st.sidebar.markdown('</div>', unsafe_allow_html=True) 