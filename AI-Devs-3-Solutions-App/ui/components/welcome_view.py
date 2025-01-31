import streamlit as st
from pathlib import Path
from ui.views.base_view import BaseView

class WelcomeView(BaseView):
    @staticmethod
    def create():
        return WelcomeView()

    def show(self):
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
        st.markdown(f"<h1 class='main-title'>{self.get_text('welcome_view.title')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='main-title' style='font-size: 20px; margin-top: 0.5rem;'>{self.get_text('welcome_view.subtitle')}</p>", unsafe_allow_html=True)
        
        # Dodaj odstęp
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Trzy kolumny obok siebie
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"### {self.get_text('welcome_view.how_to_start.title')}")
            steps = self.get_text('welcome_view.how_to_start.steps')
            st.markdown(f"""
                <div class="section-wrapper">
                    <div class="section-content">
                    {'<br>'.join(steps)}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {self.get_text('welcome_view.features.title')}")
            features = self.get_text('welcome_view.features.list')
            st.markdown(f"""
                <div class="section-wrapper">
                    <div class="section-content">
                    {'<br>'.join(features)}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"### {self.get_text('welcome_view.links.title')}")
            st.markdown(f"""
                <div class="section-wrapper">
                    <div class="section-content">
                    🔗 <a href="https://aidevs.pl" target="_blank">{self.get_text('welcome_view.links.aidevs_website')}</a><br>
                    📚 <a href="https://www.linkedin.com/company/aidevs-course/posts/?feedView=all" target="_blank">{self.get_text('welcome_view.links.aidevs_linkedin')}</a><br>
                    💬 <a href="https://www.linkedin.com/in/bartosz-clapinski/" target="_blank">{self.get_text('welcome_view.links.author_linkedin')}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <style>
            /* Sprawdźmy, czy nie ma tu dodatkowych styli dla przycisków */
            </style>
        """, unsafe_allow_html=True) 