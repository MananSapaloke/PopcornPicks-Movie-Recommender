# utils/style.py
import streamlit as st
from pathlib import Path


def load_css(path: str = "assets/css/style.css") -> None:
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text()}</style>", unsafe_allow_html=True)
    else:
    # Fallback minimal inline style
        st.markdown("<style>.movie-card{background:#111;padding:10px;border-radius:8px}</style>", unsafe_allow_html=True)