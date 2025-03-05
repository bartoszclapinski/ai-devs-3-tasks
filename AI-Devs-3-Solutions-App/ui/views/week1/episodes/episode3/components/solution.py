import streamlit as st
from ui.views.base_view import BaseView
from tasks.week1.episode03.robot_knowledge.main import RobotKnowledgeAutomation
from services.llm.llm_factory import LLMFactory

class Solution(BaseView):
    def show(self, console):
        # LLM model selection
        st.write(self.get_text('week1.episode3.implementation.select_model'))
        
        # Radio buttons for model selection
        selected_model = st.radio(
            label="LLM Model",
            options=["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Run button
        if st.button(self.get_text('week1.episode3.implementation.run_button')):
            with st.spinner(self.get_text('week1.episode3.status.running')):
                # Create and run automation
                automation = RobotKnowledgeAutomation(model_name=selected_model)
                result = automation.run(callback=console.log)
                
                # Show result
                if result.success:
                    st.success(self.get_text('week1.episode3.status.download_success'))
                else:
                    error_msg = getattr(result, 'error', '')
                    st.error(f"{self.get_text('week1.episode3.status.error')} {error_msg}") 