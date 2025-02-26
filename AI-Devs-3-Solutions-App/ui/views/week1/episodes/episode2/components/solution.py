import streamlit as st
from ui.views.base_view import BaseView
from tasks.week1.episode02.robot_verify.main import RobotVerifyAutomation
from services.llm.llm_factory import LLMFactory

class Solution(BaseView):
    def show(self, console):
        st.markdown(f"### {self.get_text('week1.episode2.implementation.title')}")
        st.markdown(self.get_text('week1.episode2.implementation.description'))
        
        # Model selection
        available_models = LLMFactory.get_available_models()
        selected_model = st.selectbox(
            self.get_text('week1.episode2.implementation.select_model'),
            available_models,
            index=0
        )
        
        # Run button
        if st.button(self.get_text('week1.episode2.implementation.run_button')):
            with st.spinner(self.get_text('week1.episode2.status.running')):
                # Create and run automation
                automation = RobotVerifyAutomation(model_name=selected_model)
                result = automation.run(callback=console.log)
                
                # Show result
                if result.success:
                    st.success(self.get_text('week1.episode2.status.success'))
                    if result.flag:
                        st.balloons()
                else:
                    st.error(f"{self.get_text('week1.episode2.status.error')} {result.error}") 