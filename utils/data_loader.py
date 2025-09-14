# utils/data_loader.py
import pickle
import ast
import pandas as pd
import streamlit as st
from typing import Tuple


@st.cache_data
def load_data(movies_path: str = 'tmdb_movies_df.pkl', sim_path: str = 'tmdb_similarity.pkl') -> Tuple[pd.DataFrame, object]:
    """Load pickled DataFrame and similarity matrix. Returns (movies_df, similarity).


    Place your existing pickles in the project root or change the paths.
    """
    movies = pickle.load(open(movies_path, 'rb'))
    similarity = pickle.load(open(sim_path, 'rb'))


    # Ensure 'genres' and 'cast' are lists
    for col in ['genres', 'cast']:
        if col in movies.columns:
            movies[col] = movies[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


        # Normalize common column names if needed
        if 'rating' not in movies.columns and 'vote_average' in movies.columns:
            movies['rating'] = movies['vote_average']
        if 'release_year' not in movies.columns and 'release_date' in movies.columns:
            movies['release_year'] = pd.to_datetime(movies['release_date'], errors='coerce').dt.year.fillna(0).astype(int)


        # Fill NaNs in text columns to avoid .str ops failing
        if 'overview' in movies.columns:
            movies['overview'] = movies['overview'].fillna("")


        return movies, similarity