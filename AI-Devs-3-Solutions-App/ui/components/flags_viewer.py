import streamlit as st
import os
from ui.views.base_view import BaseView

class FlagsViewer(BaseView):
    FLAGS_FILE = "files_storage/flags.md"

    @classmethod
    def add_to_sidebar(cls):
        viewer = cls()
        st.sidebar.markdown("---")  # separator
        return st.sidebar.button(viewer.get_text("sidebar.flags_button"))

    def show(self):
        st.markdown("""
            <style>
            .flag-entry {
                display: flex;
                align-items: center;
                gap: 10px;
                margin: 5px 0;
            }
            .flag-name {
                font-weight: bold;
            }
            .flag-info {
                color: #666;
                font-style: italic;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.subheader(self.get_text("flags_viewer.title"))
        
        if not os.path.exists(self.FLAGS_FILE):
            st.info(self.get_text("flags_viewer.no_flags"))
            return

        with open(self.FLAGS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        current_week = None
        current_episode = None
        
        for line in lines:
            line = line.strip()
            if not line or line == "# Znalezione flagi":
                continue
                
            if line.startswith("## Week"):
                current_week = line[3:]
                st.markdown(f"### {current_week}")
            elif line.startswith("### Episode"):
                current_episode = line[4:]
                st.markdown(f"#### {current_episode}")
            elif line.startswith("- {{FLG:"):
                flag_info = line.split(" (")
                st.markdown(
                    f'<div class="flag-entry">'
                    f'<span class="flag-name">{flag_info[0]}</span>'
                    f'<span class="flag-info">({flag_info[1][:-1]})</span>'
                    f'</div>',
                    unsafe_allow_html=True
                ) 