import streamlit as st

def navbar():
    st.markdown(
        """
        <nav class="navbar">
            <div class="nav-left">
                <a class="nav-logo" href="/">🍿 PopcornPicks</a>
            </div>
            <div class="nav-right">
                <a href="/Home" target="_self">Home</a>
                <a href="/Search" target="_self">Search</a>
                <a href="/Recommender" target="_self">Recommender</a>
                <a href="/Genres" target="_self">Genres</a>
            </div>
        </nav>
        """,
        unsafe_allow_html=True
    )
