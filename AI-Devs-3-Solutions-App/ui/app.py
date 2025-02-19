import streamlit as st
import sys
from pathlib import Path
import webbrowser
import json
import base64

# Dodaj główny katalog do PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from ui.views.week1.week1_view import Week1View
from ui.components.flags_viewer import FlagsViewer
from ui.components.files_viewer import FilesViewer
from ui.components.welcome_view import WelcomeView

# Wczytaj tłumaczenia
def load_translations(lang: str) -> dict:
    """Load all translations for given language"""
    translations = {}
    translations_root = Path(__file__).parent.parent / "translations"
    
    # Load common translations
    common_path = translations_root / "common" / f"{lang}.json"
    with open(common_path, 'r', encoding='utf-8') as file:
        translations.update(json.load(file))
    
    # Load episode translations
    for week_dir in translations_root.glob('week*'):
        week_num = week_dir.name
        for episode_dir in week_dir.glob('episode*'):
            episode_num = episode_dir.name
            episode_path = episode_dir / f"{lang}.json"
            if episode_path.exists():
                with open(episode_path, 'r', encoding='utf-8') as file:
                    translations[week_num] = translations.get(week_num, {})
                    translations[week_num][episode_num] = json.load(file)
    
    return translations

def get_text(key: str) -> str:
    """Get translated text using nested keys (e.g., 'week1.episode1.title')"""
    try:
        keys = key.split('.')
        value = st.session_state.translations
        for k in keys:
            value = value[k]
        return value
    except (KeyError, AttributeError):
        return key

def init_session_state():
    """Inicjalizacja stanu sesji"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'
    if 'translations' not in st.session_state:
        st.session_state.translations = load_translations(st.session_state.language)

def change_language(lang: str):
    """Zmiana języka i przeładowanie tłumaczeń"""
    st.session_state.language = lang
    st.session_state.translations = load_translations(lang)
    st.rerun()

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
    # Inicjalizacja stanu sesji
    init_session_state()
    
    # Wczytaj logo SVG z pliku
    logo_path = Path(__file__).parent.parent / "files_storage" / "home_page" / "ai-devs_logo-main.svg"
    with open(logo_path, 'r') as file:
        logo_svg = file.read()

    # Style dla wszystkich przycisków (przywracamy poprzednie style)
    st.markdown("""
        <style>
        /* Wspólne styles dla wszystkich przycisków */
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

        /* Osobne style dla przełącznika języka */
        .language-switch {
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-bottom: 10px;
        }
        .language-switch .stButton > button {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            width: 35px !important;
            height: 25px !important;
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        .language-switch .stButton > button:hover {
            opacity: 1 !important;
            background: transparent !important;
        }
        .language-switch .stButton > button:disabled {
            opacity: 1 !important;
            background: transparent !important;
        }
        .language-switch .stButton > button img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        </style>
    """, unsafe_allow_html=True)

    # Wczytaj i zakoduj flagi w base64
    def get_image_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    pl_flag_path = Path(__file__).parent.parent / "translations" / "icons" / "poland.png"
    gb_flag_path = Path(__file__).parent.parent / "translations" / "icons" / "united-kingdom.png"

    pl_flag_base64 = get_image_base64(pl_flag_path)
    gb_flag_base64 = get_image_base64(gb_flag_path)    
    
    # Przełącznik języka
    st.sidebar.markdown('<div class="language-switch">', unsafe_allow_html=True)
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("PL", key="pl_lang", disabled=st.session_state.language=='pl'):
            st.session_state.language = 'pl'
            st.session_state.translations = load_translations('pl')
            st.rerun()
    with col2:
        if st.button("ENG", key="en_lang", disabled=st.session_state.language=='en'):
            st.session_state.language = 'en'
            st.session_state.translations = load_translations('en')
            st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Style dla logo
    st.markdown("""
        <style>
        [data-testid="stSidebar"] div[data-testid="stMarkdown"] {
            text-align: center;            
        }
        [data-testid="stSidebar"] div[data-testid="stMarkdown"] svg {
            max-width: 120% !important;  /* Zwiększamy szerokość ponad kontener */
            height: auto;
            cursor: pointer;
            margin-left: -10%;  /* Wycentrowanie powiększonego logo */
            margin-right: -10%;
            transform: scale(1.2);  /* Dodatkowe skalowanie */
            margin-top: 10%;
            margin-bottom: 10%;
        }
        .logo-link {
            text-decoration: none;
            cursor: pointer;
            display: block;
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
    
    # Style dla przycisków i kontenerów
    st.markdown("""
        <style>
        /* Usuń niepotrzebne kontenery i marginesy */
        div[data-testid="stSidebarHeader"] {
            display: none !important;
        }
        
        div[data-testid="stSidebarUserContent"] {
            padding-top: 0 !important;
        }
        
        .st-emotion-cache-kgpedg {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        .st-emotion-cache-1lu0zv1 {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        .st-emotion-cache-b95ml1 {
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Ukryj konkretny kontener */
        div[class*="stMarkdown"] div[class*="stMarkdownContainer"] {
            display: none !important;
        }

        /* Reszta stylów pozostaje bez zmian */
        </style>
    """, unsafe_allow_html=True)
    
    # Wybór tygodnia z tłumaczeniem
    selected_week = st.sidebar.selectbox(
        get_text("common.select_week"),
        [get_text("common.choose_week"), "Week 1"],
        index=0
    )
    
    # Wybór epizodu z tłumaczeniem
    episodes = [
        get_text("common.choose_episode"),
        get_text("week1.episode1.title"),
        get_text("week1.episode2.title")
    ]
    selected_episode = st.sidebar.selectbox(
        get_text("common.select_episode"),
        episodes,
        index=0,
        disabled=selected_week == get_text("common.choose_week")
    )
    
    # Przyciski z tłumaczeniami
    files_viewer = FilesViewer()
    flags_viewer = FlagsViewer()
    
    show_flags = flags_viewer.add_to_sidebar()
    show_files = files_viewer.add_to_sidebar()
    
    # Style dla elementów w sidebarze
    st.markdown("""
        <style>
        /* Separatory */
        section[data-testid="stSidebar"] hr {
            margin: 10px 0 !important;
            padding: 0 !important;
            border: 0 !important;
            border-top: 1px solid rgba(255,255,255,0.1) !important;
        }
        
        /* Wszystkie przyciski w sidebarze */
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            text-align: left;
            padding: 0.3rem 0.5rem !important;
            min-height: 40px !important;
            height: auto !important;
            line-height: 1.2 !important;
            margin: 2px 0 !important;
        }

        /* Przyciski flag i plików */
        section[data-testid="stSidebar"] > div > div > div > .stButton {
            margin: 5px 0 !important;
        }
        
        /* Przyciski na dole */
        .bottom-buttons {
            padding: 0;
            margin-top: -5px;  /* Lekko podciągnij do góry */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Dodaj separator
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    # Przyciski na dole z tłumaczeniami
    with st.sidebar:
        st.markdown('<div class="bottom-buttons">', unsafe_allow_html=True)
        if st.button("🏢 " + get_text("sidebar.centrala_button")):
            webbrowser.open_new_tab("https://centrala.ag3nts.org/")
        if st.button("🎓 " + get_text("sidebar.courses_button")):
            webbrowser.open_new_tab("https://bravecourses.circle.so/")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if show_flags:
        flags_viewer.show()
    elif show_files:
        files_viewer.show()
    elif selected_week != get_text("common.choose_week") and selected_episode != get_text("common.choose_episode"):
        Week1View().show(selected_episode)
    else:
        welcome_view = WelcomeView()
        welcome_view.show()

    # Style dla obrazu w WelcomeView
    st.markdown("""
        <style>
        /* Ujemny margin tylko dla głównego obrazu */
        div[data-testid="stImage"] > div:first-child {
            margin-top: -100px !important;
        }       
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Bardziej specyficzny selektor dla przycisków w sidebarze */
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {             
        }        
        
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 