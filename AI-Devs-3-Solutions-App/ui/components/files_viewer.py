import streamlit as st
import os
from pathlib import Path
from ui.views.base_view import BaseView

class FilesViewer(BaseView):
    FILES_ROOT = "files_storage"

    @classmethod
    def add_to_sidebar(cls):
        viewer = cls()
        st.markdown("""
            <style>
            section[data-testid="stSidebar"] .stButton button {
                width: 100%;
                text-align: left;
                padding: 0.5rem 1rem !important;
                min-height: unset !important;
                height: auto !important;
                line-height: 1.5 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        return st.sidebar.button(viewer.get_text("sidebar.files_button"))

    def show(self):
        st.markdown("""
            <style>
            .file-entry {
                display: flex;
                align-items: center;
                gap: 10px;
                margin: 5px 0;
            }
            .file-name {
                font-family: monospace;
            }
            .file-info {
                color: #666;
                font-size: 0.9em;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.subheader(self.get_text("files_viewer.title"))
        
        if not os.path.exists(self.FILES_ROOT):
            st.info(self.get_text("files_viewer.no_files"))
            return

        # Przejdź przez strukturę katalogów
        for week in sorted(os.listdir(self.FILES_ROOT)):
            if week.startswith('week'):
                st.markdown(f"### Week {week[-1]}")
                week_path = Path(self.FILES_ROOT) / week
                
                for episode in sorted(os.listdir(week_path)):
                    if episode.startswith('episode'):
                        st.markdown(f"#### Episode {episode[-2:]} - Robot Login")
                        episode_path = week_path / episode
                        
                        for file in sorted(os.listdir(episode_path)):
                            if file != "flags.md":  # Pomijamy plik z flagami
                                file_path = episode_path / file
                                file_stat = file_path.stat()
                                file_size = file_stat.st_size
                                file_date = file_stat.st_mtime
                                
                                # Wyświetl plik z ikoną zależną od typu
                                icon = "📄"
                                if file.endswith('.html'):
                                    icon = "🌐"
                                elif file.endswith('.txt'):
                                    icon = "📝"
                                
                                st.markdown(
                                    f'<div class="file-entry">'
                                    f'{icon} <span class="file-name">{file}</span>'
                                    f'<span class="file-info">({file_size} bytes)</span>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                ) 