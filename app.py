import streamlit as st
from components.navbar import navbar

# Page config
st.set_page_config(
    page_title="PopcornPicks 🎬",
    page_icon="🍿",
    layout="wide"
)

# Load custom CSS
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Show navbar
navbar()

# ------------------------
# Home / Landing Page
# ------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🍿 PopcornPicks</h1>
        <p>Your personal movie recommender – search, discover, and enjoy movies like never before.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Call-to-action
st.markdown(
    """
    <div class="cta">
        <a href="/Search" target="_self" class="cta-btn">🔍 Start Exploring</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Optional: trending movies section
st.subheader("🔥 Trending Now")
st.write("This section will show trending/recommended movies (you can hook it with TMDB API later).")
