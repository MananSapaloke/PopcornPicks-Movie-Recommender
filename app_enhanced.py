# app_enhanced.py - Enhanced version with all improvements
import streamlit as st
import pandas as pd
import pickle
import ast
import os
from rapidfuzz import fuzz, process
import numpy as np
from typing import List, Dict, Tuple
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="PopcornPicks", 
    layout="wide", 
    page_icon="🍿",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700&display=swap');

:root {
    --bg-start: #0e1b22;
    --bg-end: #122a3a;
    --accent: #ffb347;
    --accent-2: #6C63FF;
    --card-bg: rgba(28, 37, 59, 0.72);
    --card-border: rgba(255, 255, 255, 0.08);
    --text: #ffffff;
    --muted: #b0b8c9;
}

/* General Styling & Background */
.stApp {
    background: radial-gradient(1200px 600px at 20% 0%, #173040 0%, transparent 60%),
                radial-gradient(900px 600px at 90% 10%, #0f2027 0%, transparent 55%),
                linear-gradient(180deg, var(--bg-start), var(--bg-end));
    color: var(--text);
    font-family: 'Overpass', sans-serif;
}

/* Title Container */
.title-container {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.title-container h1 { 
    font-size: 3.25rem; 
    font-weight: 700; 
    color: var(--accent); 
    letter-spacing: 0.5px;
}
.title-container p { 
    font-size: 1.4rem; 
    color: var(--text); 
    margin-top: 0.5rem; 
}

/* Enhanced Tabs */
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
    background-color: var(--card-bg); 
    color: var(--text); 
    border-radius: 10px;
    padding: 10px 22px; 
    font-weight: 600; 
    border: 1px solid var(--card-border);
    font-family: 'Overpass', sans-serif; 
    transition: all 0.2s ease;
}
div[data-testid="stTabs"] button[data-selected="true"] {
    background-color: var(--accent); 
    color: #1c253b; 
    font-weight: 700; 
    border-color: var(--accent);
}

/* Enhanced Button Styling */
div[data-testid="stButton"] > button {
    background-color: var(--accent-2); 
    color: white; 
    font-weight: 600; 
    border: none;
    border-radius: 8px; 
    padding: 10px 24px; 
    font-size: 1rem; 
    margin-top: 1rem;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] > button:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 6px 18px rgba(108, 99, 255, 0.35);
}

/* Enhanced Movie Card */
.movie-card {
    background-color: var(--card-bg); 
    border-radius: 12px; 
    padding: 1.2rem; 
    border: 1px solid var(--card-border);
    backdrop-filter: blur(6px);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease; 
    height: 100%;
    display: flex; 
    flex-direction: column; 
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.movie-card:hover { 
    transform: translateY(-6px); 
    box-shadow: 0 16px 30px rgba(0,0,0,0.35); 
    border-color: var(--accent);
}
.movie-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ffb347, #6C63FF);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.movie-card:hover::before {
    opacity: 1;
}

.poster-img { 
    border-radius: 8px; 
    width: 100%; 
    margin-bottom: 1rem; 
    transition: transform 0.3s ease;
}
.movie-card:hover .poster-img {
    transform: scale(1.02);
}

.movie-title { 
    font-size: 1.1rem; 
    font-weight: bold; 
    color: var(--text); 
    margin-bottom: 0.5rem;
}
.movie-details, .movie-overview { 
    font-size: 0.85rem; 
    color: var(--muted); 
    margin-top: 0.5rem; 
}
/* movie-overview clamp removed */
.movie-genres { 
    font-size: 0.8rem; 
    font-style: italic; 
    color: #8c9eff; 
    margin-top: 0.5rem; 
}

/* equal-height settings removed */

/* Pagination Styling */
.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
}
.pagination-button {
    background-color: var(--card-bg);
    color: var(--text);
    border: 1px solid var(--card-border);
    border-radius: 6px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.pagination-button:hover {
    background-color: var(--accent);
    color: #1c253b;
    border-color: var(--accent);
}
.pagination-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Search Enhancement */
.search-container {
    background-color: rgba(28, 37, 59, 0.8);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    border: 1px solid #3a4767;
}

/* Loading Animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.loading-spinner {
    border: 3px solid #3a4767;
    border-top: 3px solid #ffb347;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}

/* Error Message Styling */
.error-message {
    background-color: rgba(220, 53, 69, 0.1);
    border: 1px solid #dc3545;
    border-radius: 8px;
    padding: 1rem;
    color: #f8d7da;
    margin: 1rem 0;
}

/* Success Message Styling */
.success-message {
    background-color: rgba(40, 167, 69, 0.1);
    border: 1px solid #28a745;
    border-radius: 8px;
    padding: 1rem;
    color: #d4edda;
    margin: 1rem 0;
}

/* Comparison Modal */
.comparison-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Responsive Design */
@media (max-width: 768px) {
    .title-container h1 { font-size: 2.5rem; }
    .title-container p { font-size: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

# --- Enhanced Data Loading with Error Handling ---
@st.cache_resource
def load_data():
    """Load movie data with automatic data generation if files are missing."""
    # Try to load enhanced dataset first
    try:
        if os.path.exists('processed_tmdb_enhanced_dataset.csv'):
            movies_df = pd.read_csv('processed_tmdb_enhanced_dataset.csv')
            st.success("✅ Loaded enhanced dataset with 20,000+ movies!")
        elif os.path.exists('tmdb_movies_df.pkl'):
            movies_df = pickle.load(open('tmdb_movies_df.pkl', 'rb'))
            st.info("📊 Loaded basic dataset")
        else:
            # No data files found - generate them automatically
            st.warning("🔄 No data files found. Generating dataset automatically...")
            return generate_data_automatically()
        
        # Process list columns
        for col in ['genres', 'cast', 'streaming_on']:
            if col in movies_df.columns:
                movies_df[col] = movies_df[col].apply(
                    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
                )
        return movies_df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("🔄 Attempting to generate data automatically...")
        return generate_data_automatically()

def generate_data_automatically():
    """Automatically generate data files if they don't exist."""
    import subprocess
    import sys
    
    try:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Fetch data
        status_text.text("📡 Fetching movie data from TMDB...")
        progress_bar.progress(25)
        
        result = subprocess.run([sys.executable, 'fetch_tmdb_data_enhanced.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            st.error(f"Data fetching failed: {result.stderr}")
            return None
            
        # Step 2: Process data
        status_text.text("🔧 Processing data and building ML model...")
        progress_bar.progress(75)
        
        result = subprocess.run([sys.executable, 'data_processing_enhanced.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            st.error(f"Data processing failed: {result.stderr}")
            return None
            
        # Step 3: Load the generated data
        status_text.text("✅ Loading generated dataset...")
        progress_bar.progress(100)
        
        if os.path.exists('processed_tmdb_enhanced_dataset.csv'):
            movies_df = pd.read_csv('processed_tmdb_enhanced_dataset.csv')
            # Process list columns
            for col in ['genres', 'cast', 'streaming_on']:
                if col in movies_df.columns:
                    movies_df[col] = movies_df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
                    )
            
            status_text.text("🎉 Dataset generated successfully!")
            time.sleep(2)
            progress_bar.empty()
            status_text.empty()
            st.success("✅ Ready to go! Your movie recommender is now loaded with 20,000+ movies!")
            return movies_df
        else:
            st.error("❌ Data generation failed - files not created")
            return None
            
    except subprocess.TimeoutExpired:
        st.error("⏰ Data generation timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Error during data generation: {e}")
        return None

@st.cache_resource
def build_models(movies_df: pd.DataFrame):
    """Build TF-IDF vectors and a NearestNeighbors index on tags (memory efficient)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.neighbors import NearestNeighbors
    tags_col = 'enhanced_tags' if 'enhanced_tags' in movies_df.columns else 'tags'
    texts = movies_df[tags_col].astype(str).tolist()
    tfidf = TfidfVectorizer(max_features=10000, stop_words='english', ngram_range=(1, 2), min_df=2, max_df=0.8)
    vectors = tfidf.fit_transform(texts)
    knn = NearestNeighbors(n_neighbors=50, metric='cosine', algorithm='brute')
    knn.fit(vectors)
    return tfidf, vectors, knn

# --- Enhanced Helper Functions ---
def get_poster_url(path):
    """Get poster URL with fallback."""
    if pd.isna(path) or path == '':
        return "https://via.placeholder.com/500x750.png?text=No+Image"
    return f"https://image.tmdb.org/t/p/w500/{path}"

def fuzzy_search_movies(query: str, movies_df: pd.DataFrame, limit: int = 10) -> List[Tuple[str, int]]:
    """Enhanced fuzzy search for movie titles."""
    if not query or len(query) < 2:
        return []
    
    # Get all movie titles
    titles = movies_df['title'].tolist()
    
    # Use fuzzy matching
    matches = process.extract(query, titles, limit=limit, scorer=fuzz.partial_ratio)
    
    # Filter matches with score > 60 (rapidfuzz returns (choice, score, idx))
    return [(title, score) for title, score, _ in matches if score > 60]

def paginate_dataframe(df: pd.DataFrame, page: int, per_page: int = 20) -> Tuple[pd.DataFrame, int]:
    """Paginate a dataframe."""
    total_pages = (len(df) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return df.iloc[start_idx:end_idx], total_pages

def get_diverse_recommendations_knn(movies_df: pd.DataFrame, vectors, knn, movie_idx: int, num_recommendations: int = 5) -> pd.DataFrame:
    """Get recommendations using KNN over TF-IDF vectors, with basic diversity."""
    distances, indices = knn.kneighbors(vectors[movie_idx], n_neighbors=num_recommendations * 3 + 1)
    candidate_indices = [i for i in indices.flatten().tolist() if i != movie_idx]
    selected_indices = []
    selected_genres = set()
    for idx in candidate_indices:
        if len(selected_indices) >= num_recommendations:
            break
        genres_value = movies_df.iloc[idx]['genres']
        if not isinstance(genres_value, list):
            genres_value = []
        movie_genres = set(genres_value)
        if not movie_genres.issubset(selected_genres) or len(selected_indices) < 2:
            selected_indices.append(idx)
            selected_genres.update(movie_genres)
    if len(selected_indices) < num_recommendations:
        for idx in candidate_indices:
            if idx not in selected_indices:
                selected_indices.append(idx)
            if len(selected_indices) >= num_recommendations:
                break
    return movies_df.iloc[selected_indices[:num_recommendations]]

def display_movie_card(movie, col, show_compare_button=False, key_prefix=""):
    """Enhanced movie card with comparison feature."""
    with col:
        overview = movie.get('overview', 'No overview available.')
        if len(overview) > 120:
            overview = overview[:120] + "..."
        
        # Create unique key for comparison (prefix ensures uniqueness across tabs/sections)
        movie_key = f"{key_prefix}_compare_{movie['id']}"
        
        # Safe field extraction to avoid NaN casting errors
        release_year_val = movie.get('release_year')
        try:
            release_year_str = str(int(release_year_val)) if pd.notna(release_year_val) else "N/A"
        except Exception:
            release_year_str = "N/A"

        genres_val = movie.get('genres')
        if not isinstance(genres_val, list):
            genres_val = []
        genres_str = ", ".join(genres_val) if genres_val else "Unknown"

        rating_val = movie.get('rating')
        try:
            rating_str = f"{float(rating_val):.1f}" if pd.notna(rating_val) else "N/A"
        except Exception:
            rating_str = "N/A"

        revenue_val = movie.get('revenue')
        try:
            revenue_str = f"{int(revenue_val):,}" if pd.notna(revenue_val) else "0"
        except Exception:
            revenue_str = "0"

        cast_val = movie.get('cast')
        if not isinstance(cast_val, list):
            cast_val = []
        cast_str = ", ".join(cast_val[:3]) if cast_val else "N/A"

        st.markdown(f"""
        <div class="movie-card">
            <div>
                <img src="{get_poster_url(movie['poster_path'])}" class="poster-img">
                <p class="movie-title">{movie['title']} ({release_year_str})</p>
                <p class="movie-genres">{genres_str}</p>
                <p class="movie-overview">{overview}</p>
                <p class="movie-details">⭐ {rating_str}/10 | 💰 ${revenue_str}</p>
                <p class="movie-details"><b>Cast:</b> {cast_str}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Comparison feature removed

def display_movie_list(df_list, show_pagination=True, per_page=20, key_prefix="movie_page_selector", compare_key_prefix="compare"):
    """Enhanced movie list display with pagination."""
    if df_list.empty:
        st.warning("No movies found matching your criteria.")
        return
    
    # Pagination
    if show_pagination and len(df_list) > per_page:
        total_pages = (len(df_list) + per_page - 1) // per_page
        
        # Page selector
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page = st.selectbox(
                "Page:", 
                range(1, total_pages + 1), 
                key=f"{key_prefix}"
            )
        
        # Get page data
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_data = df_list.iloc[start_idx:end_idx]
        
        st.info(f"Showing {start_idx + 1}-{min(end_idx, len(df_list))} of {len(df_list)} movies")
    else:
        page_data = df_list.head(per_page)
    
    # Display movies in grid
    num_cols = 5
    for i in range(0, len(page_data), num_cols):
        cols = st.columns(num_cols)
        chunk = page_data.iloc[i:i+num_cols]
        for j in range(len(chunk)):
            movie = chunk.iloc[j]
            if j < len(cols):
                # Include grid coordinates in key to avoid duplicate keys if same movie appears in multiple sections
                display_movie_card(movie, cols[j], key_prefix=f"{compare_key_prefix}_{i}_{j}")

def display_comparison_modal():
    """Comparison feature removed."""
    return

# --- Main App Logic ---
def main():
    # Load data
    movies = load_data()
    if movies is None:
        st.stop()
    tfidf, vectors, knn = build_models(movies)
    
    # Sidebar removed per request
    
    # Main content area
    _, main_col, _ = st.columns([1, 4, 1])
    
    with main_col:
        st.markdown('<div class="title-container"><h1>🍿 PopcornPicks</h1><p>Smart movie recommendations</p></div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Show comparison if requested
        if st.session_state.get('show_comparison', False):
            display_comparison_modal()
            if st.button("Back to Main", use_container_width=True):
                st.session_state.show_comparison = False
                st.rerun()
            return
        
        # Enhanced tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🤖 AI Recommender", "🔎 Movie Explorer", "🏆 Critically Acclaimed",
            "💰 Highest Grossing", "🧑‍🎤 Search by Actor", "🎬 Discover by Genre"
        ])
        
        with tab1:
            st.subheader("🤖 Get Personalized Recommendations")
            
            # Enhanced movie selection with search
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_movie = st.selectbox(
                    "Pick a movie you like:", 
                    movies['title'].values, 
                    index=None, 
                    placeholder="Type or select a movie...",
                    key="recommender_select"
                )
            
            with col2:
                num_recommendations = st.selectbox("Number of recommendations:", [5, 10, 15, 20], index=0)
            
            if st.button("🎯 Get Recommendations", use_container_width=True):
                if selected_movie:
                    with st.spinner("🔍 Finding cinematic soulmates..."):
                        try:
                            idx = movies[movies['title'] == selected_movie].index[0]
                            recommendations = get_diverse_recommendations_knn(movies, vectors, knn, idx, num_recommendations)
                            
                            st.success(f"✨ Found {len(recommendations)} recommendations based on '{selected_movie}'")
                            display_movie_list(recommendations, show_pagination=False)
                            
                        except IndexError:
                            st.error("Movie not found in database!")
                        except Exception as e:
                            st.error(f"Error generating recommendations: {e}")
                else:
                    st.warning("Please select a movie first.")
        
        with tab2:
            st.header("🔎 Advanced Movie Explorer")
            
            # Enhanced filters
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                selected_genres = st.multiselect("Select genres:", sorted(list(set([g for sublist in movies['genres'] for g in sublist]))))
            
            with col2:
                min_year, max_year = int(movies['release_year'].min()), int(movies['release_year'].max())
                year_range = st.slider("Release year range:", min_year, max_year, (min_year, max_year))
            
            with col3:
                min_rating = st.slider("Minimum rating:", 0.0, 10.0, 5.0, 0.5)
            
            with col4:
                min_revenue = st.number_input("Minimum revenue ($):", min_value=0, value=0, step=1000000)
            
            # Apply filters
            filtered = movies.copy()
            
            if selected_genres:
                filtered = filtered[filtered['genres'].apply(lambda x: any(g in x for g in selected_genres))]
            
            filtered = filtered[
                (filtered['release_year'] >= year_range[0]) & 
                (filtered['release_year'] <= year_range[1]) &
                (filtered['rating'] >= min_rating) &
                (filtered['revenue'] >= min_revenue)
            ]
            
            # Sort options
            sort_by = st.selectbox("Sort by:", ["Popularity", "Rating", "Revenue", "Release Year", "Vote Count"])
            sort_ascending = st.checkbox("Ascending order")
            
            sort_columns = {
                "Popularity": "popularity",
                "Rating": "rating", 
                "Revenue": "revenue",
                "Release Year": "release_year",
                "Vote Count": "vote_count"
            }
            
            filtered = filtered.sort_values(sort_columns[sort_by], ascending=sort_ascending)
            
            st.subheader(f"🎬 Found {len(filtered):,} movies matching your criteria")
            display_movie_list(filtered, key_prefix="movie_page_selector_explorer")
        
        with tab3:
            st.header("🏆 Critically Acclaimed Movies")
            acclaimed = movies.sort_values(['rating', 'vote_count'], ascending=False)
            display_movie_list(acclaimed, key_prefix="movie_page_selector_acclaimed", compare_key_prefix="acclaimed")
        
        with tab4:
            st.header("💰 Highest Grossing Movies")
            grossing = movies[movies['revenue'] > 0].sort_values('revenue', ascending=False)
            display_movie_list(grossing, key_prefix="movie_page_selector_grossing", compare_key_prefix="grossing")
        
        with tab5:
            st.header("🧑‍🎤 Search by Actor")
            actor_name_input = st.text_input("Enter an actor's name:", placeholder="e.g., Tom Cruise")
            
            if actor_name_input:
                search_term = actor_name_input.lower()
                actor_movies = movies[movies['cast'].apply(
                    lambda cast_list: any(search_term in actor.lower() for actor in cast_list)
                )]
                
                if not actor_movies.empty:
                    st.success(f"Found **{len(actor_movies)}** movies starring **{actor_name_input}**")
                    display_movie_list(actor_movies, key_prefix="movie_page_selector_actor", compare_key_prefix="actor")
                else:
                    st.warning(f"No movies found for '{actor_name_input}'. Try a different name.")
        
        with tab6:
            st.header("🎬 Discover by Genre")
            all_genres = sorted(list(set([g for sublist in movies['genres'] for g in sublist])))
            selected_genre = st.selectbox("Choose a genre:", ["All Genres"] + all_genres)
            
            if selected_genre != "All Genres":
                genre_movies = movies[movies['genres'].apply(lambda x: selected_genre in x)]
                st.subheader(f"🎭 Top {selected_genre} Movies")
                display_movie_list(genre_movies.sort_values("rating", ascending=False), key_prefix="movie_page_selector_genre", compare_key_prefix="genre")
            else:
                st.subheader("🔥 Most Popular Movies")
                display_movie_list(movies.sort_values("popularity", ascending=False), key_prefix="movie_page_selector_popular", compare_key_prefix="popular")
        
        # Comparison tab removed

if __name__ == "__main__":
    main()
