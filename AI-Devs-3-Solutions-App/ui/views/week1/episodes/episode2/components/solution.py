import streamlit as st
from ui.views.base_view import BaseView
from tasks.week1.episode02.robot_verify.main import RobotVerifyAutomation
from services.llm.llm_factory import LLMFactory

class Solution(BaseView):
    def show(self, console):
        # Wybór modelu LLM
        st.write(self.get_text('week1.episode2.implementation.select_model'))
        
        # Radio buttony dla wyboru modelu
        selected_model = st.radio(
            label="Model LLM",
            options=["gpt-4o-mini", "gpt-4o"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Przycisk uruchomienia
        if st.button(self.get_text('week1.episode2.implementation.run_button')):
            with st.spinner(self.get_text('week1.episode2.status.running')):
                # Utwórz i uruchom automatyzację
                automation = RobotVerifyAutomation(model_name=selected_model)
                result = automation.run(callback=console.log)
                
                # Pokaż wynik
                if result.success:
                    st.success(self.get_text('week1.episode2.status.success'))
                    if hasattr(result, 'flag') and result.flag:
                        st.balloons()
                else:
                    error_msg = getattr(result, 'error', '')
                    st.error(f"{self.get_text('week1.episode2.status.error')} {error_msg}") 