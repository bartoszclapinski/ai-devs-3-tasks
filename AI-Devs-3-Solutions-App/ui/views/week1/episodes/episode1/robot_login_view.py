import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from tasks.week1.episode01.robot_login.models.robot import RobotLoginAutomation
from services.llm.llm_factory import LLMFactory
from pathlib import Path

class RobotLoginView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo(get_text_func=self.get_text)
        self._load_styles()

    def _load_styles(self):
        # Ładujemy style z pliku CSS
        css_path = Path(__file__).parent.parent.parent.parent.parent / "styles" / "episodes_styles.css"
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def show(self):
        # Użyjmy kontenera Streamlit z ograniczoną szerokością
        with st.container():
            # Tytuł
            st.markdown(f"## {self.get_text('week1.episode1.title')}")
            st.markdown(f"### {self.get_text('week1.episode1.subtitle')}")
            st.markdown(self.get_text('week1.episode1.description'))

            # Zakładki
            tab1, tab2, tab3 = st.tabs([
                self.get_text("week1.episode1.tabs.requirements"),
                self.get_text("week1.episode1.tabs.solution"),
                self.get_text("week1.episode1.tabs.task")
            ])

            with tab1:
                st.markdown(self.get_text("week1.episode1.content.requirements"))

            with tab2:
                st.markdown(self.get_text("week1.episode1.content.solution"))

            with tab3:
                st.write(self.get_text("week1.episode1.task.content"))
            
            # Implementacja rozwiązania (poza zakładkami)
            st.markdown(f"### {self.get_text('week1.episode1.implementation.title')}")
            st.markdown(self.get_text('week1.episode1.implementation.description'))
            
            # Checkbox dla pamięci cache
            use_cache = st.checkbox(self.get_text('week1.episode1.implementation.use_cache'), value=True)
            
            # Wybór modelu LLM
            st.write(self.get_text('week1.episode1.implementation.select_model'))
            
            # Radio buttony dla wyboru modelu
            selected_model = st.radio(
                label="Model LLM",
                options=["gpt-4o-mini", "gpt-4o"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            # Przycisk uruchomienia
            if st.button(self.get_text('week1.episode1.implementation.run_button'), key="episode1_task"):
                with st.spinner(self.get_text('week1.episode1.status.running')):
                    # Utwórz i uruchom automatyzację
                    automation = RobotLoginAutomation(model_name=selected_model, use_cache=use_cache)
                    result = automation.run(callback=self.console.log)
                    
                    # Pokaż wynik
                    if result.success:
                        st.success(self.get_text('week1.episode1.status.success'))
                        if result.flag:
                            st.balloons()
                    else:
                        st.error(f"{self.get_text('week1.episode1.status.error')} {result.error}")
            
            # Wyświetl konsolę
            self.console.container = st.empty() 