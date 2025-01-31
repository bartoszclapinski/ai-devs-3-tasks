from abc import ABC, abstractmethod
import streamlit as st

class BaseView(ABC):
    @abstractmethod
    def show(self):
        pass

    def render_header(self, title: str):
        st.subheader(title)

    def get_text(self, key: str) -> str:
        """Get translated text using nested keys (e.g., 'week1.episode1.title')"""
        try:
            keys = key.split('.')
            value = st.session_state.translations
            for k in keys:
                value = value[k]
            return value
        except (KeyError, AttributeError):
            return key

    # Sprawdźmy, czy nie ma tu globalnych styli 