import streamlit as st
from ui.views.base_view import BaseView
from .components.console import Console
from .components.task_info import TaskInfo
from .components.solution import Solution
from pathlib import Path

class RobotKnowledgeView(BaseView):
    def __init__(self):
        self.console = Console()
        self.task_info = TaskInfo(get_text_func=self.get_text)
        self.solution = Solution()
        self._load_styles()
        
    def _load_styles(self):
        # Load styles from CSS file
        css_path = Path(__file__).parent.parent.parent.parent.parent / "styles" / "episodes_styles.css"
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
        # Add console styles
        st.markdown("""
            <style>
            .stConsole {
                background-color: #2b2b2b;
                color: #f8f8f2;
                font-family: 'Consolas', monospace;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                width: 100%;
            }
            .console-line {
                margin: 3px 0;
                white-space: pre-wrap;
                display: flex;
                align-items: center;
            }
            .log-icon {
                margin-right: 8px;
                font-size: 14px;
            }
            .log-text {
                font-family: 'Consolas', monospace;
            }
            .log-question { color: #61afef; }
            .log-answer { color: #98c379; }
            .log-success { color: #98c379; }
            .log-error { color: #e06c75; }
            .log-warning { color: #e5c07b; }
            .log-info { color: #56b6c2; }
            .log-flag {
                color: #ff79c6;
                font-weight: bold;
            }
            .flag-icon {
                color: #4CAF50;
            }
            </style>
        """, unsafe_allow_html=True)

    def show(self):
        # Add container for all content
        st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
        
        # Title
        st.markdown(f"## {self.get_text('week1.episode3.title')}")
        st.markdown(f"### {self.get_text('week1.episode3.subtitle')}")
        st.markdown(self.get_text('week1.episode3.description'))

        # Tabs
        tab1, tab2, tab3 = st.tabs([
            self.get_text("week1.episode3.tabs.requirements"),
            self.get_text("week1.episode3.tabs.solution"),
            self.get_text("week1.episode3.tabs.task")
        ])

        with tab1:
            st.markdown(self.get_text("week1.episode3.content.requirements"))

        with tab2:
            st.markdown(self.get_text("week1.episode3.content.solution"))

        with tab3:
            self.task_info.show()
            
        # Solution implementation (outside tabs)
        st.markdown(f"### {self.get_text('week1.episode3.implementation.title')}")
        st.markdown(self.get_text('week1.episode3.implementation.description'))
        
        # Display solution without additional container
        self.solution.show(self.console)
        
        # Close container
        st.markdown('</div>', unsafe_allow_html=True)
        
    def get_text(self, key):
        """
        Get translated text for Episode 3.
        This method overrides the BaseView.get_text method to handle the new translation structure.
        """
        from ui.services.translation_service import TranslationService
        
        # If the key starts with 'week1.episode3.', remove the prefix
        if key.startswith('week1.episode3.'):
            # Extract the part after 'week1.episode3.'
            short_key = key[len('week1.episode3.'):]
            
            # Try to get the translation using the short key from the episode3 translations
            try:
                # Get the current language
                lang = st.session_state.get('language', 'pl')
                
                # Load the episode3 translations directly
                translations_root = Path(__file__).parent.parent.parent.parent.parent.parent / "translations" / "week1" / "episode3"
                lang_file = translations_root / f"{lang}.json"
                
                if lang_file.exists():
                    import json
                    with open(lang_file, 'r', encoding='utf-8') as file:
                        episode_translations = json.load(file)
                    
                    # Navigate through the keys
                    keys = short_key.split('.')
                    value = episode_translations
                    for k in keys:
                        value = value[k]
                    return value
            except Exception:
                # If any error occurs, fall back to the original method
                pass
        
        # Fall back to the original method
        return TranslationService.get_text(key) 