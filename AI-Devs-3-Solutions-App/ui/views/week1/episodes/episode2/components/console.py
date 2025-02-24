import streamlit as st

class Console:
    def __init__(self):
        self.logs = []
        self._inject_styles()
        # Kontener na logi utworzymy dopiero przy pierwszym logu
        self.container = None
    
    def _inject_styles(self):
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
            .log-question { color: #61afef; }
            .log-answer { color: #98c379; }
            .log-success { color: #98c379; }
            .log-error { color: #e06c75; }
            .log-info { color: #56b6c2; }
            .log-flag {
                color: #ff79c6;
                font-weight: bold;
            }
            .log-icon.flag-icon {
                color: #4CAF50;
                filter: hue-rotate(90deg);
            }
            </style>
        """, unsafe_allow_html=True)

    def log(self, text: str, log_type: str = "default"):
        if self.container is None:
            self.container = st.empty()
            
        icon, css_class = self._get_log_style(text, log_type)
        self.logs.append((icon, text, css_class))
        self._update_display()
    
    def _get_log_style(self, text: str, log_type: str):
        if log_type == "flag":
            return "🏆", "log-flag"
        elif log_type == "default":
            if "pytanie" in text.lower():
                return "❓", "log-question"
            elif "odpowiedź" in text.lower():
                return "💡", "log-answer"
            elif "logowanie udane" in text.lower():
                return "✅", "log-success"
            elif "pobieranie firmware" in text.lower() or "zapisano plik" in text.lower():
                return "💾", "log-info"
            elif "pobrano plik firmware" in text.lower():
                return "📄", "log-info"
            elif "błąd" in text.lower() or "nie udało" in text.lower():
                return "❌", "log-error"
            
        return "📝", ""

    def _update_display(self):
        console_html = '<div class="stConsole">'
        for icon, text, css_class in self.logs:
            icon_class = "flag-icon" if icon == "🏁" else ""
            console_html += f'<div class="console-line"><span class="log-icon {icon_class}">{icon}</span><span class="{css_class}">{text}</span></div>'
        console_html += '</div>'
        self.container.markdown(console_html, unsafe_allow_html=True) 