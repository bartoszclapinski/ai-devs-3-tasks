from abc import ABC, abstractmethod
import streamlit as st

class BaseView(ABC):
    @abstractmethod
    def show(self):
        pass

    def render_header(self, title: str):
        st.subheader(title) 