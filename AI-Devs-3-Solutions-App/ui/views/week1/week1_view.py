from ..base_view import BaseView
from .episodes.episode1.robot_login_view import RobotLoginView
import streamlit as st

class Week1View(BaseView):
    def show(self, selected_episode: str):
        if selected_episode == "Episode 1 - Robot Login":
            RobotLoginView().show()
        elif selected_episode == "Episode 2 - Coming Soon":
            self.render_header("Episode 2")
            st.write("Coming soon...") 