import streamlit as st
import sys
from pathlib import Path
import webbrowser  # Dodaj na górze pliku

# Dodaj główny katalog do PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from ui.views.week1.week1_view import Week1View
from ui.components.flags_viewer import FlagsViewer
from ui.components.files_viewer import FilesViewer
from ui.components.welcome_view import WelcomeView

# Ukryj domyślne menu i stopkę
st.set_page_config(
    page_title="AI Devs 3 - Tasks",
    page_icon="🤖",
    layout="wide",
    menu_items={},
    initial_sidebar_state="expanded"
)

# Ukryj wszystkie elementy nawigacji i dostosuj style
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp > header {display: none;}
div[data-testid="stToolbar"] {visibility: hidden;}

/* Dostosuj szerokość powiadomień */
div[data-testid="stNotification"] {
    width: 100% !important;
    margin-left: 0 !important;
}

/* Zmniejsz padding dla wszystkich elementów */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    # Style dla przycisków
    st.markdown("""
        <style>
        /* Wspólne style dla wszystkich przycisków */
        .stButton > button {
            background-color: #2e7d32 !important;
            border-color: #2e7d32 !important;
            color: white !important;
        }
        .stButton > button:hover {
            background-color: #1b5e20 !important;
            border-color: #1b5e20 !important;
            color: white !important;
        }

        /* Style dla checkboxów */
        div[data-testid="stCheckbox"] label div[role="checkbox"] {
            background-color: #2e7d32 !important;
            border-color: #2e7d32 !important;
        }
        
        div[data-testid="stCheckbox"] label div[role="checkbox"][aria-checked="true"] {
            background-color: #2e7d32 !important;
            border-color: #2e7d32 !important;
        }
        
        div[data-testid="stCheckbox"] label div[role="checkbox"]:hover {
            border-color: #2e7d32 !important;
            background-color: #2e7d32 !important;
        }

        /* Style dla selectboxów */
        div[data-testid="stSelectbox"] div[role="button"] {
            border-color: #2e7d32 !important;
        }
        
        div[data-testid="stSelectbox"] div[role="button"]:hover {
            border-color: #2e7d32 !important;
            background-color: rgba(46, 125, 50, 0.1) !important;
        }

        /* Style dla checkboxów */
        .st-ez {
            transition-property: background-image, border-color, background-color;
        }
        
        .st-eg {
            background-color: rgb(46, 125, 50) !important;
        }
        
        .st-cw {
            border-bottom-color: rgb(46, 125, 50) !important;
        }
        
        .st-cv {
            border-top-color: rgb(46, 125, 50) !important;
        }
        
        .st-cu {
            border-right-color: rgb(46, 125, 50) !important;
        }
        
        .st-ct {
            border-left-color: rgb(46, 125, 50) !important;
        }
        
        [data-testid="stCheckbox"] {
            color: rgb(46, 125, 50) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Wczytaj logo SVG z pliku
    logo_path = Path(__file__).parent.parent / "files_storage" / "home_page" / "ai-devs_logo-main.svg"
    with open(logo_path, 'r') as file:
        logo_svg = file.read()

    # Style dla logo
    st.markdown("""
        <style>
        [data-testid="stSidebar"] div[data-testid="stMarkdown"] {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem !important;
        }
        [data-testid="stSidebar"] div[data-testid="stMarkdown"] svg {
            max-width: 100%;
            height: auto;
            cursor: pointer;
        }
        .logo-link {
            text-decoration: none;
            cursor: pointer;
        }
        .logo-link:hover svg {
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)

    # Dodaj logo do sidebara z linkiem
    st.sidebar.markdown(
        f'<a href="/" class="logo-link" target="_self">{logo_svg}</a>', 
        unsafe_allow_html=True
    )
    
    # Wybór tygodnia z opcją "Wybierz tydzień"
    selected_week = st.sidebar.selectbox(
        "Wybierz tydzień",
        ["Wybierz tydzień", "Week 1"],
        index=0
    )
    
    # Wybór epizodu - zawsze widoczny, ale aktywny tylko po wybraniu tygodnia
    episodes = ["Wybierz epizod", "Episode 1 - Robot Login", "Episode 2 - Coming Soon"]
    selected_episode = st.sidebar.selectbox(
        "Wybierz epizod",
        episodes,
        index=0,  # Domyślnie wybrana pierwsza opcja
        disabled=selected_week == "Wybierz tydzień"  # Nieaktywny gdy nie wybrano tygodnia
    )
    
    # Dodaj przyciski do wyświetlania flag i plików
    show_flags = FlagsViewer.add_to_sidebar()
    show_files = FilesViewer.add_to_sidebar()
    
    # Dodaj separator i przyciski z linkami na dole sidebara
    st.sidebar.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)  # Spacer
    st.sidebar.markdown("---")  # separator
    
    # Style dla przycisków z linkami
    st.markdown("""
        <style>
        /* Przyciski z linkami na dole */
        .bottom-sidebar-buttons {
            position: fixed;
            bottom: 0;
            padding-bottom: 1rem;
            width: inherit;
        }
        
        section[data-testid="stSidebar"] .bottom-sidebar-buttons .stButton button {
            width: 100%;
            text-align: left;
            padding: 0.5rem 1rem !important;
            min-height: unset !important;
            height: auto !important;
            line-height: 1.5 !important;
            margin-bottom: 0.5rem;
        }        
    """, unsafe_allow_html=True)
    
    # Kontener na przyciski z linkami
    st.sidebar.markdown('<div class="bottom-sidebar-buttons">', unsafe_allow_html=True)
    
    if st.sidebar.button("🏢 Centrala AI Devs"):
        webbrowser.open_new_tab("https://centrala.ag3nts.org/")
        
    if st.sidebar.button("🎓 Brave Courses"):
        webbrowser.open_new_tab("https://bravecourses.circle.so/")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if show_flags:
        FlagsViewer.show_flags()
    elif show_files:
        FilesViewer.show_files()
    elif selected_week != "Wybierz tydzień" and selected_episode != "Wybierz epizod":
        Week1View().show(selected_episode)
    else:
        WelcomeView.show()

if __name__ == "__main__":
    main() 