# utils/recommender.py
import pandas as pd
from typing import List, Tuple




def recommend_by_movie(movies: pd.DataFrame, similarity, movie_title: str, top_n: int = 6) -> pd.DataFrame:
    if movie_title not in movies['title'].values:
        return pd.DataFrame()
    idx = movies[movies['title'] == movie_title].index[0]
    sim_scores = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:top_n+1]
    return movies.iloc[[i[0] for i in sim_scores]]




def get_trending(movies: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    return movies.sort_values('popularity', ascending=False).head(top_n)




def get_top_rated(movies: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    return movies.sort_values('rating', ascending=False).head(top_n)




def filter_movies(movies: pd.DataFrame, genres: List[str] = None, year_range: Tuple[int,int] = None, min_rating: float = 0.0) -> pd.DataFrame:
    df = movies
    if genres:
        df = df[df['genres'].apply(lambda x: all(g in x for g in genres) if isinstance(x, list) else False)]
    if year_range:
        df = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]
    if min_rating:
        df = df[df['rating'] >= min_rating]
    return df