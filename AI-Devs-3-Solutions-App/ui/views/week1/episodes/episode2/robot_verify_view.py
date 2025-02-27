import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from .components.solution import Solution
from pathlib import Path

class RobotVerifyView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo(get_text_func=self.get_text)
        self.solution = Solution()
        self._load_styles()
        
    def _load_styles(self):
        # Ładujemy style z pliku CSS
        css_path = Path(__file__).parent.parent.parent.parent.parent / "styles" / "episodes_styles.css"
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def show(self):
        # Dodajmy kontener dla całej zawartości
        st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
        
        # Tytuł
        st.markdown(f"## {self.get_text('week1.episode2.title')}")
        st.markdown(f"### {self.get_text('week1.episode2.subtitle')}")
        st.markdown(self.get_text('week1.episode2.description'))

        # Zakładki
        tab1, tab2, tab3 = st.tabs([
            self.get_text("week1.episode2.tabs.requirements"),
            self.get_text("week1.episode2.tabs.solution"),
            self.get_text("week1.episode2.tabs.task")
        ])

        with tab1:
            st.markdown(self.get_text("week1.episode2.content.requirements"))

        with tab2:
            st.markdown(self.get_text("week1.episode2.content.solution"))

        with tab3:
            self.task_info.show()
            
        # Implementacja rozwiązania (poza zakładkami)
        st.markdown(f"### {self.get_text('week1.episode2.implementation.title')}")
        st.markdown(self.get_text('week1.episode2.implementation.description'))
        
        # Wyświetl rozwiązanie bez dodatkowego kontenera
        self.solution.show(self.console)
        
        # Wyświetl konsolę
        self.console.container = st.empty()
        
        # Zamknij kontener
        st.markdown('</div>', unsafe_allow_html=True) 