# pages/1_Home.py
import streamlit as st
from utils.style import load_css
from utils.data_loader import load_data
from utils.recommender import get_trending, get_top_rated
from components.movie_card import display_grid


load_css()
movies, similarity = load_data()


st.markdown("<h1 style='text-align:center;color:#E50914;margin-bottom:6px'>🍿 PopcornPicks</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#d1d5db;margin-top:0'>Your cinematic discovery playground</p>", unsafe_allow_html=True)


st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Trending Now")
display_grid(get_trending(movies), num_cols=5, max_items=20)


st.markdown("<div class='section'></div>")
st.subheader("Top Rated")
display_grid(get_top_rated(movies), num_cols=5, max_items=20)