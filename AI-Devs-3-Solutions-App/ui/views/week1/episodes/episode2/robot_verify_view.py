import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from .components.solution import Solution

class RobotVerifyView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo()
        self.solution = Solution()

    def show(self):
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
            self.solution.show(self.console)
            self.console.container = st.empty()

        with tab3:
            self.task_info.show() 