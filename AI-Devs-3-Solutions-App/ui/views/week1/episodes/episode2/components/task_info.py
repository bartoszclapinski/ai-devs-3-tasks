import streamlit as st
from ui.views.base_view import BaseView

class TaskInfo(BaseView):
    def show(self):
        st.write(self.get_text("week1.episode2.task.content")) 