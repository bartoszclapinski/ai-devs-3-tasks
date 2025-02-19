import streamlit as st

class TaskInfo:
    def show(self):
        st.write(self.get_text("week1.episode1.task.content")) 