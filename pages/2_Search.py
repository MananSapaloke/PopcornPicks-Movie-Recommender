# pages/2_Search.py
import streamlit as st
import pandas as pd
from utils.style import load_css
from utils.data_loader import load_data
from components.movie_card import display_grid


load_css()
movies, similarity = load_data()


q = st.text_input("Search for movies, actors, or keywords")
if q:
    ql = q.lower()
    title_matches = movies[movies['title'].str.lower().str.contains(ql, na=False)]
    overview_matches = movies[movies['overview'].str.lower().str.contains(ql, na=False)]
    cast_matches = movies[movies['cast'].apply(lambda cast: any(ql in actor.lower() for actor in cast) if isinstance(cast, list) else False)]


    results = pd.concat([title_matches, overview_matches, cast_matches]).drop_duplicates().reset_index(drop=True)
    st.write(f"Found {len(results)} results")
    display_grid(results, num_cols=5)
else:
    st.info("Type in the search box to find movies by title, cast, or keywords.")