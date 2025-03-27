import streamlit as st

def task_card(title: str, description: str, status: str = "Not Started"):
    with st.container():
        st.markdown(f"""
        <div class="task-card">
            <h3>{title}</h3>
            <p>{description}</p>
            <span class="status {status.lower()}">{status}</span>
        </div>
        """, unsafe_allow_html=True) 