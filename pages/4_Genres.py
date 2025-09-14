import streamlit as st
from utils.data_loader import load_movies
from components.movie_card import render_movie_grid


st.title("🎭 Browse by Genre")
movies = load_movies()


all_genres = sorted(set(g for sublist in movies["genres"].dropna().str.split(", ") for g in sublist))
selected_genre = st.selectbox("Select a genre:", all_genres)


if selected_genre:
    subset = movies[movies["genres"].str.contains(selected_genre, na=False)]
    render_movie_grid(subset.head(12))