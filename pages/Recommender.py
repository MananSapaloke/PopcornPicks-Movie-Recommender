import streamlit as st
from utils.data_loader import load_movies
from utils.recommender import recommend
from components.movie_card import render_movie_grid


st.title("🤖 Recommender")
movies = load_movies()


selected = st.selectbox("Pick a movie to get recommendations:", movies["title"].values)


if selected:
    recs = recommend(selected, movies)
    st.subheader(f"Movies similar to {selected}")
    render_movie_grid(recs)