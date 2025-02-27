import streamlit as st

class Console:
    def __init__(self):
        self.logs = []
        # Kontener na logi utworzymy dopiero przy pierwszym logu
        self.container = None

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
            if "pytanie" in text.lower() or "question" in text.lower():
                return "❓", "log-question"
            elif "odpowiedź" in text.lower() or "answer" in text.lower():
                return "💡", "log-answer"
            elif "success" in text.lower() or "udane" in text.lower() or "ok" in text.lower():
                return "✅", "log-success"
            elif "sending" in text.lower() or "received" in text.lower() or "pobieranie" in text.lower() or "zapisano" in text.lower():
                return "📤", "log-info"
            elif "error" in text.lower() or "błąd" in text.lower() or "nie udało" in text.lower() or "failed" in text.lower():
                return "❌", "log-error"
            
        return "📝", ""

    def _update_display(self):
        console_html = '<div class="stConsole">'
        for icon, text, css_class in self.logs:
            icon_class = "flag-icon" if "flag" in css_class.lower() else ""
            console_html += f'<div class="console-line"><span class="log-icon {icon_class}">{icon}</span><span class="log-text {css_class}">{text}</span></div>'
        console_html += '</div>'
        self.container.markdown(console_html, unsafe_allow_html=True) 