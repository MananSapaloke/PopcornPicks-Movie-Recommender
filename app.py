# app.py (The Definitive, Polished, and Perfectly Centered Showcase Version)
import streamlit as st
import pandas as pd
import pickle
import ast

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(page_title="PopcornPicks", layout="wide", page_icon="🍿")

# --- Custom CSS for the Final Design ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700&display=swap');

/* General Styling & Background */
.stApp {
    background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
    color: #ffffff;
    font-family: 'Overpass', sans-serif;
}

/* Title Container */
.title-container {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.title-container h1 { font-size: 3.5rem; font-weight: 700; color: #FFD580; }
.title-container p { font-size: 1.4rem; color: #ffffff; margin-top: 0.5rem; }

/* Tabs Container */
div[data-testid="stTabs"] {
    display: flex;
    justify-content: center;
}
div[data-testid="stTabs"] > div {
    justify-content: center;
    gap: 0.8rem;
    padding-bottom: 2rem;
}
div[data-testid="stTabs"] button {
    background-color: #1c253b; color: white; border-radius: 10px;
    padding: 10px 22px; font-weight: 600; border: 1px solid #3a4767;
    font-family: 'Overpass', sans-serif; transition: all 0.2s ease;
}
div[data-testid="stTabs"] button[data-selected="true"] {
    background-color: #ffb347; color: #1c253b; font-weight: 700; border-color: #ffb347;
}

/* Fun Button Styling */
div[data-testid="stButton"] > button {
    background-color: #6C63FF; color: white; font-weight: 600; border: none;
    border-radius: 8px; padding: 10px 24px; font-size: 1rem; margin-top: 1rem;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] > button:hover { transform: scale(1.05); }

/* Movie Card Styling */
.movie-card {
    background-color: #1c253b; border-radius: 10px; padding: 1rem; border: 1px solid #3a4767;
    transition: transform 0.2s, box-shadow 0.2s; height: 100%;
    display: flex; flex-direction: column; justify-content: space-between;
}
.movie-card:hover { transform: translateY(-5px); box-shadow: 0 6px 16px rgba(0,0,0,0.3); border-color: #ffb347; }
.poster-img { border-radius: 7px; width: 100%; margin-bottom: 1rem; }
.movie-title { font-size: 1.1rem; font-weight: bold; color: #ffffff; }
.movie-details, .movie-overview { font-size: 0.85rem; color: #b0b8c9; margin-top: 0.5rem; }
.movie-genres { font-size: 0.8rem; font-style: italic; color: #8c9eff; margin-top: 0.5rem; }
/* The .verdict-box style was here and has been removed */
</style>
""", unsafe_allow_html=True)

# --- Data Loading (Cached for Performance) ---
@st.cache_data
def load_data():
    movies_df = pickle.load(open('tmdb_movies_df.pkl', 'rb'))
    similarity = pickle.load(open('tmdb_similarity.pkl', 'rb'))
    for col in ['genres', 'cast']:
        if col in movies_df.columns:
            movies_df[col] = movies_df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    return movies_df, similarity

movies, similarity = load_data()
all_genres = sorted(list(set([genre for sublist in movies['genres'] for genre in sublist])))

# --- Helper Functions ---
def get_poster_url(path):
    if pd.isna(path) or path == '': return "https://via.placeholder.com/500x750.png?text=No+Image"
    return f"https://image.tmdb.org/t/p/w500/{path}"

# The generate_verdict function was here and has been removed

def recommend(movie_title):
    idx = movies[movies['title'] == movie_title].index[0]
    sim_scores = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
    return movies.iloc[[i[0] for i in sim_scores]]

def display_movie_card(movie, col):
    with col:
        overview = movie.get('overview', 'No overview available.')
        if len(overview) > 120: overview = overview[:120] + "..."
        st.markdown(f"""
        <div class="movie-card">
            <div>
                <img src="{get_poster_url(movie['poster_path'])}" class="poster-img">
                <p class="movie-title">{movie['title']} ({int(movie['release_year'])})</p>
                <p class="movie-genres">{', '.join(movie['genres'])}</p>
                <p class="movie-overview">{overview}</p>
                <p class="movie-details">⭐ {movie['rating']:.1f}/10 | 💰 ${movie['revenue']:,}</p>
                <p class="movie-details"><b>Cast:</b> {', '.join(movie['cast'][:3])}</p>
            </div>
            <!-- The verdict-box div was here and has been removed -->
        </div>
        """, unsafe_allow_html=True)

def display_movie_list(df_list):
    num_cols = 5
    for i in range(0, len(df_list), num_cols):
        cols = st.columns(num_cols)
        chunk = df_list.iloc[i:i+num_cols]
        for j in range(len(chunk)):
            movie = chunk.iloc[j]
            if j < len(cols): display_movie_card(movie, cols[j])

# --- APP LAYOUT ---

# Create a main container for the centered content
_, main_col, _ = st.columns([1, 4, 1]) # spacer, main, spacer

with main_col:
    st.markdown('<div class="title-container"><h1>PopcornPicks</h1><p>Smart movie recommendations, served fresh</p></div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🤖 AI Recommender", "🔎 Movie Explorer", "🏆 Critically Acclaimed",
        "💰 Highest Grossing", "🧑‍🎤 Search by Actor", "🎬 Discover by Genre"
    ])

    with tab1:
        st.subheader("Get Personalized Recommendations")
        selected_movie = st.selectbox("Pick a movie you like:", movies['title'].values, index=None, placeholder="Type or select a movie...")
        if st.button("Suggest Movies", use_container_width=True):
            if selected_movie:
                with st.spinner("Finding cinematic soulmates..."):
                    recommendations = recommend(selected_movie)
                    display_movie_list(recommendations)
            else: st.warning("Please select a movie first.")

    with tab2:
        st.header("🔎 Movie Explorer")
        col1, col2, col3 = st.columns(3)
        with col1: selected_genres = st.multiselect("Select genres:", all_genres)
        min_year, max_year = int(movies['release_year'].min()), int(movies['release_year'].max())
        with col2: year_range = st.slider("Select release year range:", min_year, max_year, (min_year, max_year))
        with col3: min_rating = st.slider("Select minimum rating:", 0.0, 10.0, 5.0, 0.5)
        
        filtered = movies[
            (movies['genres'].apply(lambda x: all(g in x for g in selected_genres))) &
            (movies['release_year'] >= year_range[0]) & (movies['release_year'] <= year_range[1]) &
            (movies['rating'] >= min_rating)
        ]
        st.subheader(f"Found {len(filtered)} movies matching your criteria")
        display_movie_list(filtered.sort_values("popularity", ascending=False).head(20))

    with tab3:
        st.header("🏆 Critically Acclaimed Movies")
        display_movie_list(movies.sort_values(['rating', 'vote_count'], ascending=False).head(15))

    with tab4:
        st.header("💰 Highest Grossing Movies")
        display_movie_list(movies[movies['revenue'] > 0].sort_values('revenue', ascending=False).head(15))

    with tab5:
        st.header("🧑‍🎤 Search by Actor")
        actor_name_input = st.text_input("Enter an actor's name (e.g., Tom Cruise)")
        if actor_name_input:
            search_term = actor_name_input.lower()
            actor_movies = movies[movies['cast'].apply(lambda cast_list: any(search_term in actor.lower() for actor in cast_list))]
            if not actor_movies.empty:
                st.markdown(f"Found **{len(actor_movies)}** movies starring **{actor_name_input}**.")
                display_movie_list(actor_movies)
            else: st.warning(f"No movies found for '{actor_name_input}'. Please check spelling or try another name.")

    with tab6:
        st.header("🎬 Discover by Genre")
        selected_genre = st.selectbox("Choose a genre:", ["All Genres"] + all_genres)
        if selected_genre != "All Genres":
            genre_movies = movies[movies['genres'].apply(lambda x: selected_genre in x)]
            st.subheader(f"Top-Rated {selected_genre} Movies")
            display_movie_list(genre_movies.sort_values("rating", ascending=False).head(15))
        else:
            st.subheader("Top Popular Movies")
            display_movie_list(movies.sort_values("popularity", ascending=False).head(15))