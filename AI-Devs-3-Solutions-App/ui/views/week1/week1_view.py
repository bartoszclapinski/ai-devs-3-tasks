from ..base_view import BaseView
from .episodes.episode1.robot_login_view import RobotLoginView
from .episodes.episode2.robot_verify_view import RobotVerifyView
from .episodes.episode3.robot_knowledge_view import RobotKnowledgeView
import streamlit as st

class Week1View(BaseView):
    def show(self, selected_episode: str):
        # Check episode title from translations
        episode1_title = self.get_text("week1.episode1.title")
        episode2_title = self.get_text("week1.episode2.title")
        episode3_title = self.get_text("week1.episode3.title")
        
        if selected_episode == episode1_title:
            RobotLoginView().show()
        elif selected_episode == episode2_title:
            RobotVerifyView().show()
        elif selected_episode == episode3_title:
            RobotKnowledgeView().show()
        else:
            self.render_header(episode3_title)
            st.write(self.get_text("week1.episode3.coming_soon"))

        # Check if there are additional styles
        # Especially in RobotLoginView 