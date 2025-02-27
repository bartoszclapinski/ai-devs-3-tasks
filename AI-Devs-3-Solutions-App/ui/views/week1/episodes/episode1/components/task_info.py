import streamlit as st

class TaskInfo:
    def __init__(self, get_text_func=None):
        self.get_text_func = get_text_func
        
    def show(self):
        if self.get_text_func:
            st.write(self.get_text_func("week1.episode1.task.content"))
        else:
            st.write("Task content not available") 