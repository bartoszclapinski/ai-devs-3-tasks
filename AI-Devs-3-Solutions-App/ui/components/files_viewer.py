import streamlit as st
import os
from pathlib import Path

class FilesViewer:
    FILES_ROOT = "files_storage"

    @staticmethod
    def add_to_sidebar():
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
        return st.sidebar.button("📁 Pokaż pobrane pliki")

    @staticmethod
    def show_files():
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
        
        st.subheader("📁 Pobrane pliki")
        
        if not os.path.exists(FilesViewer.FILES_ROOT):
            st.info("Nie znaleziono żadnych plików.")
            return

        # Przejdź przez strukturę katalogów
        for week in sorted(os.listdir(FilesViewer.FILES_ROOT)):
            if week.startswith('week'):
                st.markdown(f"### Week {week[-1]}")
                week_path = Path(FilesViewer.FILES_ROOT) / week
                
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