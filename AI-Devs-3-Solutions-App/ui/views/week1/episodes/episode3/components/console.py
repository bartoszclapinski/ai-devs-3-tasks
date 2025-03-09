import streamlit as st

class Console:
    def __init__(self):
        self.logs = []
        # Container for logs will be created on first log
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
        elif log_type == "error":
            return "❌", "log-error"
        elif log_type == "warning":
            return "⚠️", "log-warning"
        elif log_type == "success":
            return "✅", "log-success"
        elif log_type == "info":
            return "ℹ️", "log-info"
        elif log_type == "default":
            if "question" in text.lower() or "pytanie" in text.lower():
                return "❓", "log-question"
            elif "answer" in text.lower() or "odpowiedź" in text.lower():
                return "💡", "log-answer"
            elif "success" in text.lower() or "udane" in text.lower() or "ok" in text.lower():
                return "✅", "log-success"
            elif "downloading" in text.lower() or "pobieranie" in text.lower() or "zapisano" in text.lower():
                return "📥", "log-info"
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