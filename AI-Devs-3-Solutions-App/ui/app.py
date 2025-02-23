import sys
from pathlib import Path
# Dodaj główny katalog do PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from ui.services.session_service import SessionService
from ui.services.translation_service import TranslationService
from ui.components.sidebar import Sidebar
from ui.components.welcome_view import WelcomeView
from ui.views.week1.week1_view import Week1View

def main():
    # Initialize session
    SessionService.init_session_state()
    
    # Configure page
    st.set_page_config(
        page_title="AI Devs 3 - Tasks",
        page_icon="🤖",
        layout="wide",
        menu_items={},
        initial_sidebar_state="expanded"
    )
    
    # Load styles
    with open(Path(__file__).parent / "styles" / "main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Show sidebar
    sidebar = Sidebar()
    selected_week, selected_episode = sidebar.show()
    
    # Show main content
    if selected_week != TranslationService.get_text("common.choose_week") and \
       selected_episode != TranslationService.get_text("common.choose_episode"):
        Week1View().show(selected_episode)
    else:
        WelcomeView().show()

if __name__ == "__main__":
    main() 