# components/cards.py
import streamlit as st
import pandas as pd
from typing import Optional




def get_poster_url(path: Optional[str]) -> str:
    if pd.isna(path) or not path:
        return "https://via.placeholder.com/300x450.png?text=No+Image"
    return f"https://image.tmdb.org/t/p/w300{path}"




def movie_card_html(movie: dict) -> str:
    title = movie.get('title', 'Untitled')
    year = int(movie.get('release_year', 0)) if pd.notna(movie.get('release_year', None)) else ''
    rating = movie.get('rating', None)
    rating_txt = f"{rating:.1f}" if rating is not None and not pd.isna(rating) else "—"
    poster = get_poster_url(movie.get('poster_path'))
    genres = movie.get('genres', [])[:3]
    if isinstance(genres, str):
        genres = [g.strip() for g in genres.split(',') if g.strip()]
    overview = movie.get('overview', '')
    if len(overview) > 140:
        overview = overview[:137] + '...'


    html = f"""
    <div class="movie-card">
        <div class="poster-wrap">
            <img class="poster" src="{poster}" alt="{title}">
            <div class="rating-badge">{rating_txt}</div>
        </div>
        <div class="card-body">
            <div class="title">{title} <span class="year">({year})</span></div>
            <div class="genres">{', '.join(genres)}</div>
            <div class="overview">{overview}</div>
        </div>
    </div>
    """
    return html




def display_grid(df: pd.DataFrame, num_cols: int = 5, max_items: int = 25) -> None:
    if df is None or df.empty:
        st.info("No movies found. Try different filters.")
        return
    df = df.head(max_items).reset_index(drop=True)
    rows = (len(df) + num_cols - 1) // num_cols
    idx = 0
    for _ in range(rows):
        cols = st.columns(num_cols, gap='medium')
        for c in cols:
        if idx >= len(df):
            break
        movie = df.iloc[idx].to_dict()
        with c:
            st.markdown(movie_card_html(movie), unsafe_allow_html=True)
        idx += 1