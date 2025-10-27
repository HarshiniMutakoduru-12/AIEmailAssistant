# style.py
import streamlit as st

def load_css():
    """Inject custom CSS styles into the Streamlit app."""
    with open("assets/style.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
