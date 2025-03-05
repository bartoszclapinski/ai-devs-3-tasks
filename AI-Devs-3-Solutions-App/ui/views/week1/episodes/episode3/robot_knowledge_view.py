import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from .components.solution import Solution
from pathlib import Path

class RobotKnowledgeView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo(get_text_func=self.get_text)
        self.solution = Solution()
        self._load_styles()
        
    def _load_styles(self):
        # Load styles from CSS file
        css_path = Path(__file__).parent.parent.parent.parent.parent / "styles" / "episodes_styles.css"
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def show(self):
        # Add container for all content
        st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
        
        # Title
        st.markdown(f"## {self.get_text('week1.episode3.title')}")
        st.markdown(f"### {self.get_text('week1.episode3.subtitle')}")
        st.markdown(self.get_text('week1.episode3.description'))

        # Tabs
        tab1, tab2, tab3 = st.tabs([
            self.get_text("week1.episode3.tabs.requirements"),
            self.get_text("week1.episode3.tabs.solution"),
            self.get_text("week1.episode3.tabs.task")
        ])

        with tab1:
            st.markdown(self.get_text("week1.episode3.content.requirements"))

        with tab2:
            st.markdown(self.get_text("week1.episode3.content.solution"))

        with tab3:
            self.task_info.show()
            
        # Solution implementation (outside tabs)
        st.markdown(f"### {self.get_text('week1.episode3.implementation.title')}")
        st.markdown(self.get_text('week1.episode3.implementation.description'))
        
        # Display solution without additional container
        self.solution.show(self.console)
        
        # Display console
        self.console.container = st.empty()
        
        # Close container
        st.markdown('</div>', unsafe_allow_html=True) 