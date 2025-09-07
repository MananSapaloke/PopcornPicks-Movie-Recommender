# fetch_tmdb_data_enhanced.py - Enhanced version with multiple data sources
import requests
import pandas as pd
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("TMDB_API_KEY not found in .env file. Make sure the file exists and the variable is set.")

OUTPUT_CSV = 'tmdb_enhanced_dataset.csv'

# --- Multiple Data Sources Configuration ---
DATA_SOURCES = {
    'popular': {
        'endpoint': 'https://api.themoviedb.org/3/movie/popular',
        'pages': 500,  # 10,000 movies
        'params': {'api_key': API_KEY, 'language': 'en-US'}
    },
    'top_rated': {
        'endpoint': 'https://api.themoviedb.org/3/movie/top_rated',
        'pages': 500,  # 10,000 movies
        'params': {'api_key': API_KEY, 'language': 'en-US'}
    },
    'discover': {
        'endpoint': 'https://api.themoviedb.org/3/discover/movie',
        'pages': 500,  # 10,000 movies
        'params': {
            'api_key': API_KEY,
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'include_video': False,
            'language': 'en-US',
            'vote_count.gte': 10  # Very low threshold for maximum coverage
        }
    },
    'trending_week': {
        'endpoint': 'https://api.themoviedb.org/3/trending/movie/week',
        'pages': 50,  # 1,000 movies
        'params': {'api_key': API_KEY, 'language': 'en-US'}
    }
}

# --- Robust API Call Function ---
def get_from_api(url, params):
    """Makes an API call with retries and exponential backoff."""
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"\n  - API Error: {e}. Retrying ({i+1}/{retries})...")
            time.sleep(2 * (i + 1))
    return None

# --- Enhanced Movie Data Extraction ---
def extract_movie_data(movie_details):
    """Extract comprehensive movie data from TMDb API response."""
    if not movie_details:
        return None
    
    # Extract cast and crew
    cast = [actor['name'] for actor in movie_details.get('credits', {}).get('cast', [])[:5]]
    director = next((crew['name'] for crew in movie_details.get('credits', {}).get('crew', []) if crew['job'] == 'Director'), None)
    
    # Enhanced provider extraction
    all_provider_names = set()
    us_providers = movie_details.get('watch/providers', {}).get('US', {})
    if us_providers:
        for provider_type in ['flatrate', 'rent', 'buy']:
            for provider in us_providers.get(provider_type, []):
                all_provider_names.add(provider['provider_name'])
    streaming_on = sorted(list(all_provider_names))
    
    # Extract additional metadata
    runtime = movie_details.get('runtime', 0)
    budget = movie_details.get('budget', 0)
    original_language = movie_details.get('original_language', 'en')
    production_countries = [country['name'] for country in movie_details.get('production_countries', [])]
    
    return {
        'id': movie_details['id'],
        'title': movie_details['title'],
        'original_title': movie_details.get('original_title', movie_details['title']),
        'overview': movie_details['overview'],
        'genres': [genre['name'] for genre in movie_details.get('genres', [])],
        'rating': movie_details.get('vote_average', 0),
        'vote_count': movie_details.get('vote_count', 0),
        'popularity': movie_details.get('popularity', 0),
        'release_date': movie_details.get('release_date', ''),
        'release_year': int(movie_details['release_date'][:4]) if movie_details.get('release_date') else None,
        'revenue': movie_details.get('revenue', 0),
        'budget': budget,
        'runtime': runtime,
        'cast': cast,
        'director': director,
        'poster_path': movie_details.get('poster_path', ''),
        'backdrop_path': movie_details.get('backdrop_path', ''),
        'streaming_on': streaming_on,
        'original_language': original_language,
        'production_countries': production_countries,
        'adult': movie_details.get('adult', False),
        'video': movie_details.get('video', False)
    }

# --- Main Data Collection Logic ---
all_movies_data = []
seen_movie_ids = set()  # To avoid duplicates

# Resume logic
if os.path.exists(OUTPUT_CSV):
    print(f"Resuming from existing file: {OUTPUT_CSV}")
    df_existing = pd.read_csv(OUTPUT_CSV)
    all_movies_data = df_existing.to_dict('records')
    seen_movie_ids = set(df_existing['id'].tolist())
    print(f"Resuming with {len(seen_movie_ids)} existing movies")

# Collect data from multiple sources
for source_name, source_config in DATA_SOURCES.items():
    print(f"\n=== Fetching from {source_name.upper()} ===")
    
    for page in tqdm(range(1, source_config['pages'] + 1), desc=f"Fetching {source_name}"):
        params = source_config['params'].copy()
        params['page'] = page
        
        movie_list = get_from_api(source_config['endpoint'], params)
        
        if not movie_list or 'results' not in movie_list:
            print(f"\nCould not fetch page {page} from {source_name}. Skipping.")
            continue
        
        # Process each movie
        for movie_summary in movie_list['results']:
            movie_id = movie_summary['id']
            
            # Skip if we already have this movie
            if movie_id in seen_movie_ids:
                continue
            
            # Get detailed movie information
            detail_params = {
                'api_key': API_KEY, 
                'language': 'en-US', 
                'append_to_response': 'credits,watch/providers'
            }
            movie_details = get_from_api(f'https://api.themoviedb.org/3/movie/{movie_id}', detail_params)
            
            if not movie_details:
                continue
            
            # Extract and store movie data
            movie_data = extract_movie_data(movie_details)
            if movie_data:
                all_movies_data.append(movie_data)
                seen_movie_ids.add(movie_id)
            
            time.sleep(0.05)  # Be nice to the API
        
        # Checkpointing: Save progress after every 10 pages
        if page % 10 == 0:
            pd.DataFrame(all_movies_data).to_csv(OUTPUT_CSV, index=False)
            print(f"  - Checkpoint: {len(all_movies_data)} movies saved")

# --- Final Save ---
final_df = pd.DataFrame(all_movies_data)
final_df.to_csv(OUTPUT_CSV, index=False)

print("\nData fetching complete.")
print(f"Final dataset contains {len(final_df)} unique movies")
print(f"Dataset saved to {OUTPUT_CSV}")
print(f"Movies from {len(DATA_SOURCES)} different sources")
print(f"Average movies per source: {len(final_df) // len(DATA_SOURCES)}")
