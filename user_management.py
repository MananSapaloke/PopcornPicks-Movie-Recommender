# user_management.py - User rating system and session management
import streamlit as st
import pandas as pd
import json
import os
from typing import Dict, List, Optional
import hashlib
import time

class UserManager:
    """Manages user ratings, preferences, and session data."""
    
    def __init__(self):
        self.ratings_file = "user_ratings.json"
        self.preferences_file = "user_preferences.json"
        self.session_file = "user_sessions.json"
        self.ensure_files_exist()
    
    def ensure_files_exist(self):
        """Create data files if they don't exist."""
        for file_path in [self.ratings_file, self.preferences_file, self.session_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
    
    def get_user_id(self) -> str:
        """Get or create a unique user ID for the session."""
        if 'user_id' not in st.session_state:
            # Create a unique ID based on session info
            session_info = f"{time.time()}_{st.session_state.get('_session_id', 'default')}"
            st.session_state.user_id = hashlib.md5(session_info.encode()).hexdigest()[:12]
        return st.session_state.user_id
    
    def load_ratings(self) -> Dict:
        """Load user ratings from file."""
        try:
            with open(self.ratings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_ratings(self, ratings: Dict):
        """Save user ratings to file."""
        with open(self.ratings_file, 'w') as f:
            json.dump(ratings, f, indent=2)
    
    def rate_movie(self, movie_id: int, rating: float) -> bool:
        """Rate a movie (1-10 scale)."""
        user_id = self.get_user_id()
        ratings = self.load_ratings()
        
        if user_id not in ratings:
            ratings[user_id] = {}
        
        ratings[user_id][str(movie_id)] = {
            'rating': rating,
            'timestamp': time.time()
        }
        
        self.save_ratings(ratings)
        return True
    
    def get_user_ratings(self) -> Dict[str, float]:
        """Get current user's ratings."""
        user_id = self.get_user_id()
        ratings = self.load_ratings()
        return ratings.get(user_id, {})
    
    def get_movie_rating(self, movie_id: int) -> Optional[float]:
        """Get user's rating for a specific movie."""
        user_ratings = self.get_user_ratings()
        return user_ratings.get(str(movie_id), {}).get('rating')
    
    def load_preferences(self) -> Dict:
        """Load user preferences."""
        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_preferences(self, preferences: Dict):
        """Save user preferences."""
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    
    def update_preferences(self, **kwargs):
        """Update user preferences."""
        user_id = self.get_user_id()
        preferences = self.load_preferences()
        
        if user_id not in preferences:
            preferences[user_id] = {}
        
        preferences[user_id].update(kwargs)
        self.save_preferences(preferences)
    
    def get_preferences(self) -> Dict:
        """Get current user's preferences."""
        user_id = self.get_user_id()
        preferences = self.load_preferences()
        return preferences.get(user_id, {})
    
    def add_to_watchlist(self, movie_id: int):
        """Add movie to user's watchlist."""
        user_id = self.get_user_id()
        preferences = self.load_preferences()
        
        if user_id not in preferences:
            preferences[user_id] = {}
        
        if 'watchlist' not in preferences[user_id]:
            preferences[user_id]['watchlist'] = []
        
        if movie_id not in preferences[user_id]['watchlist']:
            preferences[user_id]['watchlist'].append(movie_id)
            self.save_preferences(preferences)
            return True
        return False
    
    def remove_from_watchlist(self, movie_id: int):
        """Remove movie from user's watchlist."""
        user_id = self.get_user_id()
        preferences = self.load_preferences()
        
        if user_id in preferences and 'watchlist' in preferences[user_id]:
            if movie_id in preferences[user_id]['watchlist']:
                preferences[user_id]['watchlist'].remove(movie_id)
                self.save_preferences(preferences)
                return True
        return False
    
    def get_watchlist(self) -> List[int]:
        """Get user's watchlist."""
        preferences = self.get_preferences()
        return preferences.get('watchlist', [])
    
    def is_in_watchlist(self, movie_id: int) -> bool:
        """Check if movie is in user's watchlist."""
        return movie_id in self.get_watchlist()
    
    def get_user_stats(self) -> Dict:
        """Get user statistics."""
        ratings = self.get_user_ratings()
        watchlist = self.get_watchlist()
        
        return {
            'movies_rated': len(ratings),
            'watchlist_size': len(watchlist),
            'average_rating': sum(r['rating'] for r in ratings.values()) / len(ratings) if ratings else 0,
            'favorite_genres': self.get_favorite_genres(),
            'favorite_actors': self.get_favorite_actors()
        }
    
    def get_favorite_genres(self, movies_df: pd.DataFrame) -> List[str]:
        """Get user's favorite genres based on ratings."""
        user_ratings = self.get_user_ratings()
        if not user_ratings:
            return []
        
        # Get movies user has rated highly (7+)
        high_rated_movies = [
            movie_id for movie_id, rating_data in user_ratings.items()
            if rating_data['rating'] >= 7.0
        ]
        
        # Count genres from highly rated movies
        genre_counts = {}
        for movie_id in high_rated_movies:
            try:
                movie = movies_df[movies_df['id'] == int(movie_id)].iloc[0]
                for genre in movie['genres']:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
            except (IndexError, ValueError):
                continue
        
        # Return top 5 genres
        return sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def get_favorite_actors(self, movies_df: pd.DataFrame) -> List[str]:
        """Get user's favorite actors based on ratings."""
        user_ratings = self.get_user_ratings()
        if not user_ratings:
            return []
        
        # Get movies user has rated highly (7+)
        high_rated_movies = [
            movie_id for movie_id, rating_data in user_ratings.items()
            if rating_data['rating'] >= 7.0
        ]
        
        # Count actors from highly rated movies
        actor_counts = {}
        for movie_id in high_rated_movies:
            try:
                movie = movies_df[movies_df['id'] == int(movie_id)].iloc[0]
                for actor in movie['cast'][:3]:  # Top 3 cast members
                    actor_counts[actor] = actor_counts.get(actor, 0) + 1
            except (IndexError, ValueError):
                continue
        
        # Return top 5 actors
        return sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)[:5]

def display_rating_widget(movie_id: int, movie_title: str, current_rating: Optional[float] = None):
    """Display a rating widget for a movie."""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**{movie_title}**")
    
    with col2:
        rating = st.slider(
            "Rate this movie:",
            min_value=1.0,
            max_value=10.0,
            value=current_rating or 5.0,
            step=0.5,
            key=f"rating_{movie_id}"
        )
    
    with col3:
        if st.button("Save Rating", key=f"save_rating_{movie_id}"):
            user_manager = UserManager()
            user_manager.rate_movie(movie_id, rating)
            st.success(f"Rated {movie_title} {rating}/10!")
            st.rerun()

def display_watchlist_widget(movie_id: int, movie_title: str):
    """Display watchlist widget for a movie."""
    user_manager = UserManager()
    is_in_watchlist = user_manager.is_in_watchlist(movie_id)
    
    if is_in_watchlist:
        if st.button("📝 Remove from Watchlist", key=f"remove_watchlist_{movie_id}"):
            user_manager.remove_from_watchlist(movie_id)
            st.success(f"Removed {movie_title} from watchlist!")
            st.rerun()
    else:
        if st.button("➕ Add to Watchlist", key=f"add_watchlist_{movie_id}"):
            user_manager.add_to_watchlist(movie_id)
            st.success(f"Added {movie_title} to watchlist!")
            st.rerun()

def display_user_dashboard(movies_df: pd.DataFrame):
    """Display user dashboard with stats and preferences."""
    user_manager = UserManager()
    stats = user_manager.get_user_stats()
    
    st.header("👤 Your Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Movies Rated", stats['movies_rated'])
    
    with col2:
        st.metric("Watchlist Size", stats['watchlist_size'])
    
    with col3:
        st.metric("Avg Rating Given", f"{stats['average_rating']:.1f}/10")
    
    with col4:
        st.metric("Favorite Genres", len(stats['favorite_genres']))
    
    # Show watchlist
    if stats['watchlist_size'] > 0:
        st.subheader("📝 Your Watchlist")
        watchlist = user_manager.get_watchlist()
        watchlist_movies = movies_df[movies_df['id'].isin(watchlist)]
        
        if not watchlist_movies.empty:
            for _, movie in watchlist_movies.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{movie['title']}** ({int(movie['release_year'])})")
                with col2:
                    if st.button("Remove", key=f"remove_{movie['id']}"):
                        user_manager.remove_from_watchlist(movie['id'])
                        st.rerun()
                with col3:
                    st.write(f"⭐ {movie['rating']:.1f}")
    
    # Show favorite genres
    if stats['favorite_genres']:
        st.subheader("🎭 Your Favorite Genres")
        for genre, count in stats['favorite_genres']:
            st.write(f"• {genre} ({count} movies)")
    
    # Show favorite actors
    if stats['favorite_actors']:
        st.subheader("🎬 Your Favorite Actors")
        for actor, count in stats['favorite_actors']:
            st.write(f"• {actor} ({count} movies)")

# Initialize user manager in session state
if 'user_manager' not in st.session_state:
    st.session_state.user_manager = UserManager()
