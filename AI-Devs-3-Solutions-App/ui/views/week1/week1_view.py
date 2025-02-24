from ..base_view import BaseView
from .episodes.episode1.robot_login_view import RobotLoginView
from .episodes.episode2.robot_verify_view import RobotVerifyView
import streamlit as st

class Week1View(BaseView):
    def show(self, selected_episode: str):
        # Sprawdzamy po tytule epizodu z tłumaczeń
        episode1_title = self.get_text("week1.episode1.title")
        episode2_title = self.get_text("week1.episode2.title")
        
        if selected_episode == episode1_title:
            RobotLoginView().show()
        elif selected_episode == episode2_title:
            RobotVerifyView().show()
        else:
            self.render_header(episode2_title)
            st.write(self.get_text("week1.episode2.coming_soon"))

        # Sprawdźmy, czy nie ma tu dodatkowych styli
        # Szczególnie w RobotLoginView 