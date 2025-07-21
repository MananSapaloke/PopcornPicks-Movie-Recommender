# fetch_tmdb_data.py
import requests
import pandas as pd
from tqdm import tqdm
import time
import os

# --- Configuration ---
# --- IMPORTANT: PASTE YOUR TMDB v3 API KEY HERE ---
API_KEY = "b3a31922a69289086282b45b79f9b1d4"
OUTPUT_CSV = 'tmdb_full_dataset.csv'
START_PAGE = 1
END_PAGE = 250 # Each page has 20 movies. 250 pages = 5000 movies.

# --- Robust API Call Function ---
def get_from_api(url, params):
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"\n  - API Error: {e}. Retrying ({i+1}/{retries})...")
            time.sleep(2 * (i + 1)) # Exponential backoff
    return None

# --- Main Logic ---
all_movies_data = []
# Resume logic
if os.path.exists(OUTPUT_CSV):
    print(f"Resuming from existing file: {OUTPUT_CSV}")
    df_existing = pd.read_csv(OUTPUT_CSV)
    all_movies_data = df_existing.to_dict('records')
    last_page_processed = len(df_existing) // 20
    START_PAGE = last_page_processed + 1
    print(f"Resuming from page {START_PAGE}")
else:
    print("Starting a new data fetch from TMDb.")

# Main loop to get movie lists
for page in tqdm(range(START_PAGE, END_PAGE + 1), desc="Fetching Movie Pages"):
    list_params = {
        'api_key': API_KEY,
        'sort_by': 'popularity.desc',
        'include_adult': False,
        'include_video': False,
        'language': 'en-US',
        'page': page,
        'vote_count.gte': 200 # Only get movies with a decent number of votes
    }
    movie_list = get_from_api('https://api.themoviedb.org/3/discover/movie', list_params)
    
    if not movie_list or 'results' not in movie_list:
        print(f"\nCould not fetch page {page}. Skipping.")
        continue

    # Loop through each movie on the page to get its full details
    for movie_summary in movie_list['results']:
        movie_id = movie_summary['id']
        detail_params = {'api_key': API_KEY, 'language': 'en-US', 'append_to_response': 'credits'}
        movie_details = get_from_api(f'https://api.themoviedb.org/3/movie/{movie_id}', detail_params)
        
        if not movie_details:
            continue
            
        # Extract cast and crew
        cast = [actor['name'] for actor in movie_details.get('credits', {}).get('cast', [])[:5]]
        director = next((crew['name'] for crew in movie_details.get('credits', {}).get('crew', []) if crew['job'] == 'Director'), None)

        # Append all the rich data we need
        all_movies_data.append({
            'id': movie_details['id'],
            'title': movie_details['title'],
            'overview': movie_details['overview'],
            'genres': [genre['name'] for genre in movie_details.get('genres', [])],
            'rating': movie_details.get('vote_average', 0),
            'vote_count': movie_details.get('vote_count', 0),
            'popularity': movie_details.get('popularity', 0),
            'release_year': int(movie_details['release_date'][:4]) if movie_details.get('release_date') else None,
            'revenue': movie_details.get('revenue', 0),
            'cast': cast,
            'director': director,
            'poster_path': movie_details.get('poster_path', '')
        })
        time.sleep(0.05) # Be nice to the API

    # Checkpointing: Save progress after every 5 pages
    if page % 5 == 0:
        temp_df = pd.DataFrame(all_movies_data)
        temp_df.to_csv(OUTPUT_CSV, index=False)
        # print(f"\n  - Checkpoint saved at page {page}. Total movies: {len(temp_df)}")

# Final save
final_df = pd.DataFrame(all_movies_data)
final_df.to_csv(OUTPUT_CSV, index=False)
print(f"\nData fetching complete. Final dataset contains {len(final_df)} movies.")
print(f"Dataset saved to {OUTPUT_CSV}.")