import streamlit as st
import os

class FlagsViewer:
    FLAGS_FILE = "files_storage/flags.md"

    @staticmethod
    def add_to_sidebar():
        st.sidebar.markdown("---")  # separator
        st.markdown("""
            <style>
            /* Ustaw szerokość i wysokość przycisku w sidebarze */
            section[data-testid="stSidebar"] .stButton button {
                width: 100%;
                text-align: left;
                padding: 0.5rem 1rem !important;  # Zmniejszona wysokość
                min-height: unset !important;     # Usunięcie minimalnej wysokości
                height: auto !important;          # Automatyczna wysokość
                line-height: 1.5 !important;      # Dostosowana wysokość linii
            }
            </style>
        """, unsafe_allow_html=True)
        return st.sidebar.button("🏆 Pokaż znalezione flagi")

    @staticmethod
    def show_flags():
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
        
        st.subheader("🏆 Znalezione flagi")
        
        if os.path.exists(FlagsViewer.FLAGS_FILE):
            with open(FlagsViewer.FLAGS_FILE, "r", encoding="utf-8") as f:
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
        else:
            st.info("Nie znaleziono jeszcze żadnych flag.") 