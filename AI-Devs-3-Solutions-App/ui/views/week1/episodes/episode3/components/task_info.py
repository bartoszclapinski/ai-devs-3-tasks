import streamlit as st
from ui.views.base_view import BaseView
import os

class TaskInfo(BaseView):
    def __init__(self, get_text_func=None):
        self.get_text_func = get_text_func or self.get_text
        
    def show(self):
        """Display task information."""
        st.markdown(f"### {self.get_text_func('week1.episode3.task_info.title')}")
        
        # Display task description
        st.markdown(self.get_text_func('week1.episode3.task_info.description'))
        
        # Check if the task file has been downloaded
        task_file_path = "AI-Devs-3-Solutions-App/files_storage/week1/episode03/json_data.txt"
        if os.path.exists(task_file_path):
            st.success(self.get_text_func('week1.episode3.task_info.file_downloaded'))
            
            # Show file size
            file_size = os.path.getsize(task_file_path)
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024
            
            if file_size_mb >= 1:
                st.info(f"File size: {file_size_mb:.2f} MB")
            else:
                st.info(f"File size: {file_size_kb:.2f} KB")
        else:
            st.warning(self.get_text_func('week1.episode3.task_info.file_not_downloaded')) 