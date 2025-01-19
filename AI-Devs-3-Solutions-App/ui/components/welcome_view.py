import streamlit as st
from pathlib import Path

class WelcomeView:
    @staticmethod
    def show():
        try:
            image_path = Path("files_storage/home_page/read.png")
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            else:
                st.warning("Nie znaleziono obrazu powitalnego")
        except Exception as e:
            st.error(f"Błąd podczas ładowania obrazu: {e}")
        
        # Style dla sekcji
        st.markdown("""
            <style>
            h3 {
                text-align: center;
                margin-bottom: 1.5rem;
            }
            .main-title {
                text-align: center;
            }
            .main-title h1 {
                font-size: 2.5em;
            }
            .main-title h1 span {
                font-size: 1.2em;
            }
            .main-title p {
                font-size: 2.5em;
                margin-top: 0.5em;
            }
            .section-content {
                display: inline-block;
                text-align: left;
                margin: 0 auto;
                line-height: 2;
            }
            .section-wrapper {
                text-align: center;
            }
            .section-content a {
                color: #4CAF50;
                text-decoration: none;
            }
            .section-content a:hover {
                text-decoration: underline;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Tytuł i opis
        st.markdown("<h1 class='main-title'>🚀 Witaj Agencie! 🤖</h1>", unsafe_allow_html=True)
        st.markdown("<p class='main-title' style='font-size: 20px; margin-top: 0.5rem;'>To jest aplikacja do rozwiązywania zadań z kursu AI Devs 3.</p>", unsafe_allow_html=True)
        
        # Dodaj odstęp
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Trzy kolumny obok siebie
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Jak zacząć?")
            st.markdown("""
                <div class="section-wrapper">
                    <div class="section-content">
                    📋 Wybierz tydzień z menu po lewej stronie<br>
                    ✏️ Wybierz zadanie do rozwiązania<br>
                    ▶️ Uruchom rozwiązanie i obserwuj postęp
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Dostępne funkcje")
            st.markdown("""
                <div class="section-wrapper">
                    <div class="section-content">
                    🏆 Przeglądanie znalezionych flag<br>
                    📁 Przeglądanie pobranych plików<br>
                    🤖 Automatyczne rozwiązywanie zadań
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("### Linki")
            st.markdown("""
                <div class="section-wrapper">
                    <div class="section-content">
                    🔗 <a href="https://aidevs.pl" target="_blank">AI Devs Website</a><br>
                    📚 <a href="https://www.linkedin.com/company/aidevs-course/posts/?feedView=all" target="_blank">AI Devs Linkedin</a><br>
                    💬 <a href="https://www.linkedin.com/in/bartosz-clapinski/" target="_blank">Author Linkedin</a>
                    </div>
                </div>
            """, unsafe_allow_html=True) 