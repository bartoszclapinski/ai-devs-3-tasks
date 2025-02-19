import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from tasks.week1.episode01.robot_login.models.robot import RobotLoginAutomation
from services.llm.llm_factory import LLMFactory

class RobotLoginView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo()

    def show(self):
        # Style dla całego komponentu
        st.markdown("""
            <style>
            .block-container {
                padding-top: 0rem !important;
            }
            
            /* Style dla zakładek */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px !important;
                padding: 0 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 50px !important;
                padding: 10px 20px !important;
                border-bottom: 3px solid transparent !important;
                background-color: transparent !important;
            }
            
            /* Aktywna zakładka */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: transparent !important;
                border-bottom: 2px solid #2e7d32 !important;
                position: relative !important;
                z-index: 1000 !important;
            }
            
            /* Dodaj własne podkreślenie */
            .stTabs [data-baseweb="tab"][aria-selected="true"]::after {
                content: '' !important;
                position: absolute !important;
                bottom: 0 !important;
                left: 0 !important;
                width: 100% !important;
                height: 2px !important;
                background-color: #2e7d32 !important;
                z-index: 1001 !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] [data-testid="stMarkdownContainer"] p {
                color: #2e7d32 !important;
                font-weight: bold !important;
            }
            
            /* Usuń czerwone podkreślenie */
            .stTabs [data-baseweb="tab-border"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0 !important;
                pointer-events: none !important;
            }

            /* Style dla sekcji implementacji */
            div[data-testid="stVerticalBlock"] > div > .implementation-wrapper {
                max-width: 40% !important;
            }
            
            div[data-testid="stVerticalBlock"] > div > .implementation-wrapper p,
            div[data-testid="stVerticalBlock"] > div > .implementation-wrapper h3 {
                max-width: 100% !important;
            }

            /* Style dla selectboxa i przycisku */
            .implementation-section {
                width: 300px !important;
            }
            
            /* Zmniejsz odstęp między selectboxem a przyciskiem */
            .stButton {
                margin-top: 0.5rem !important;
            }          
            
            /* Kontener selectboxa */
            div[data-baseweb="select"] {
                width: 300px !important;
            }
            
            /* Specyficzne styles dla wyboru modelu LLM */
            label:contains("Wybierz model LLM") + div [data-baseweb="select"] {
                width: 300px !important;
            }
            
            
            /* Całkowicie usuń domyślne style zakładek */
            .stTabs [data-baseweb="tab-highlight"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0 !important;
                pointer-events: none !important;
            }
            
            .stTabs [data-baseweb="tab-border"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0 !important;
                pointer-events: none !important;
            }
            
            /* Wzmocnij style dla aktywnej zakładki */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: transparent !important;
                border-bottom: 3px solid #2e7d32 !important;
                position: relative !important;
                z-index: 1000 !important;
            }
            
            /* Dodaj własne podkreślenie */
            .stTabs [data-baseweb="tab"][aria-selected="true"]::after {
                content: '' !important;
                position: absolute !important;
                bottom: 0 !important;
                left: 0 !important;
                width: 100% !important;
                height: 3px !important;
                background-color: #2e7d32 !important;
                z-index: 1001 !important;
            }

            /* Style dla przycisków */
            .stButton > button {
                background-color: #2e7d32 !important;
                border-color: #2e7d32 !important;
                color: white !important;
                
            }
            
            .stButton > button:hover {
                background-color: #1b5e20 !important;
                border-color: #1b5e20 !important;
                color: white !important;
            }
            
            /* Style dla selectboxa tylko w sekcji implementacji */
            .implementation-section div[data-testid="stFormSelect"] div[data-baseweb="select"] {
                
            }           

            /* Style dla zakładek i separatora */
            .stTabs {
                max-width: 800px !important;
            }
            
            /* Separator */
            hr.separator {
                max-width: 800px !important;
                margin-left: 0 !important;
            }
            
            /* Kontener zakładek */
            div[data-testid="stTabs"] > div[role="tablist"] {
                max-width: 100% !important;
            }
            
            /* Zawartość zakładek */
            div[data-testid="stTabs"] > div[role="tabpanel"] {
                max-width: 100% !important;
            }

            /* Sekcja implementacji */
            .implementation-wrapper {
                max-width: 800px !important;
            }

            /* Style dla checkboxa */
            [data-testid="stCheckbox"] {
                color: #2e7d32 !important;
            }
            
            /* Kolor znacznika i obramowania */
            [data-testid="stCheckbox"] > label > div[role="checkbox"] {
                border-color: rgba(46, 125, 50, 0.4) !important;
            }
            
            /* Kolor znacznika po zaznaczeniu */
            [data-testid="stCheckbox"] > label > div[role="checkbox"][aria-checked="true"] {
                background-color: #2e7d32 !important;
                border-color: #2e7d32 !important;
            }
            
            /* Kolor obramowania przed zaznaczeniem */
            [data-testid="stCheckbox"] > label > div[role="checkbox"]:not([aria-checked="true"]) {
                border-color: rgba(46, 125, 50, 0.4) !important;
            }
            
            /* Hover na checkboxie */
            [data-testid="stCheckbox"] > label > div[role="checkbox"]:hover {
                border-color: #2e7d32 !important;
            }

            /* Style dla sekcji implementacji */
            .implementation-section {
                background-color: #1e1e1e;
                padding: 1rem;
                border-radius: 4px;
                margin-top: 1rem;
            }
            
            /* Style TYLKO dla przycisku uruchomienia w sekcji implementacji */
            [data-testid="episode1_task"] {
                width: 300px !important;
            }
                    
            div[data-baseweb="select"] {
                width: auto;
            }

            /* Style dla selectboxa z key="llm_model_selector" */
            [key="llm_model_selector"] {
                width: 300px;
            }
            
            /* Kontener dla kontrolek implementacji */
            .implementation-controls {
                margin-top: 1rem;
            }
            
            /* Wszystkie selectboxy domyślnie auto */
            div[data-baseweb="select"] {
                width: auto !important;
            }
            
            /* Style dla selectboxa w pierwszej kolumnie */
            [data-testid="column"] div[data-baseweb="select"] {
                width: 300px !important;
            }
            
            /* Style dla przycisku uruchomienia */
            [data-testid="episode1_task"] {
                width: 300px !important;
            }
            
            /* Style dla radio buttonów - w poziomie */
            div[data-testid="stRadio"] > div {
                display: flex !important;
                align-items: center !important;
                gap: 2rem !important;
            }
            
            /* Label dla radio buttonów w jednej linii */
            div[data-testid="stRadio"] label {
                display: flex !important;
                align-items: center !important;
                gap: 0.5rem !important;
            }
            
            /* Style dla przycisku uruchomienia */
            [data-testid="episode1_task"] {
                width: 300px !important;
            }
            
            </style>
        """, unsafe_allow_html=True)

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
            st.markdown(self.get_text("week1.episode1.task.content"))

        # Sekcja implementacji
        st.markdown(f"### {self.get_text('week1.episode1.implementation.title')}")
        st.markdown(self.get_text("week1.episode1.implementation.description"))

        # Kontener dla kontrolek
        st.markdown('<div class="implementation-controls">', unsafe_allow_html=True)

        # Checkbox do kontroli użycia cache'a
        use_cache = st.checkbox(
            self.get_text("week1.episode1.implementation.use_cache"), 
            value=True,
            help=self.get_text("week1.episode1.implementation.cache_help"),
            key="use_cache_checkbox"
        )

        # Radio buttons w poziomie
        selected_model = st.radio(
            self.get_text("week1.episode1.implementation.select_model"),
            LLMFactory.get_available_models(),
            key="llm_model_selector",
            horizontal=True
        )

        # Przycisk uruchomienia
        if st.button(
            self.get_text("week1.episode1.implementation.run_button"), 
            key="episode1_task",
            type="primary"
        ):
            self._run_task(selected_model, use_cache)

        st.markdown('</div>', unsafe_allow_html=True)

    def _run_task(self, model_name: str, use_cache: bool):
        with st.spinner(self.get_text("week1.episode1.status.running")):
            automation = RobotLoginAutomation(model_name)
            if not use_cache:
                automation.qa_memory.clear_memory()
            success = automation.login(callback=self.console.log)
            
            if success:
                st.markdown("""
                    <style>
                    div[data-testid="stNotification"] {
                        justify-content: center;
                    }
                    div[data-testid="stNotification"] > div {
                        text-align: center;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.success(self.get_text("week1.episode1.status.success"))
            else:
                st.error(self.get_text("week1.episode1.status.error")) 