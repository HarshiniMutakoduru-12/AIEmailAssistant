# state.py
import streamlit as st

def init_session_state():
    """Initialize all Streamlit session variables."""
    defaults = {
        "messages": [],
        "model": None,
        "current_email": None,
        "feedback": {},
        "input_key": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
