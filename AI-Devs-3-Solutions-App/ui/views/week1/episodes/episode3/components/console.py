import streamlit as st
from ui.views.base_view import BaseView
import time

class Console(BaseView):
    def __init__(self):
        self.container = st.empty()
        self.logs = []
        self.max_logs = 100
    
    def show(self):
        """
        Implementation of the abstract show method from BaseView.
        This method is required but not used directly for the Console component.
        """
        self._render()
        
    def log(self, message, log_type="info"):
        """
        Add a log message to the console.
        
        Args:
            message: The message to log
            log_type: The type of log (info, warning, error, success)
        """
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append({
            "timestamp": timestamp,
            "message": message,
            "type": log_type
        })
        
        # Limit the number of logs
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
            
        self._render()
        
    def _render(self):
        """Render the console with all logs."""
        html = """
        <div class="console">
            <div class="console-header">
                <span>Console</span>
            </div>
            <div class="console-body">
        """
        
        for log in self.logs:
            log_class = f"console-{log['type']}"
            html += f"""
            <div class="console-line {log_class}">
                <span class="console-timestamp">[{log['timestamp']}]</span>
                <span class="console-message">{log['message']}</span>
            </div>
            """
            
        html += """
            </div>
        </div>
        <style>
        .console {
            background-color: #1E1E1E;
            border-radius: 5px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
        }
        .console-header {
            background-color: #333;
            padding: 5px 10px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            color: white;
            font-weight: bold;
        }
        .console-body {
            padding: 10px;
            max-height: 300px;
            overflow-y: auto;
        }
        .console-line {
            margin-bottom: 5px;
            color: #DDD;
        }
        .console-timestamp {
            color: #888;
            margin-right: 10px;
        }
        .console-info {
            color: #DDD;
        }
        .console-warning {
            color: #FFA500;
        }
        .console-error {
            color: #FF6347;
        }
        .console-success {
            color: #4CAF50;
        }
        </style>
        """
        
        self.container.markdown(html, unsafe_allow_html=True) 