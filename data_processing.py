# data_processing.py (The Final, Corrected Version)
import pandas as pd
import ast

print("Starting final data processing...")
try:
    df = pd.read_csv('tmdb_full_dataset.csv')
except FileNotFoundError:
    print("Error: tmdb_full_dataset.csv not found. Please run fetch_tmdb_data.py first.")
    exit()

# --- Data Cleaning ---
df.dropna(subset=['overview', 'genres', 'cast', 'director'], inplace=True)
df['genres'] = df['genres'].apply(ast.literal_eval)
df['cast'] = df['cast'].apply(ast.literal_eval)

# --- Feature Engineering ---
# Create space-less versions for the model, but keep the originals
def remove_spaces(text_list):
    return [str(item).replace(" ", "") for item in text_list]

# Create new columns for the tags, leaving originals untouched
df['genres_tags'] = df['genres'].apply(remove_spaces)
df['cast_tags'] = df['cast'].apply(remove_spaces)
df['director_tags'] = df['director'].apply(lambda x: str(x).replace(" ", ""))
df['overview_list'] = df['overview'].apply(lambda x: x.split())

# Create the 'tags' column from the new _tags columns
df['tags'] = df['overview_list'] + df['genres_tags'] + df['cast_tags'] + df['director_tags'].apply(lambda x: [x])

# --- Create the Final DataFrame ---
# We select all columns we need, using the original 'genres' and 'cast' columns
final_df = df[[
    'id', 'title', 'release_year', 'overview', 'genres', 'cast', 'director',
    'rating', 'vote_count', 'popularity', 'revenue', 'poster_path', 'tags'
]].copy()

final_df['tags'] = final_df['tags'].apply(lambda x: " ".join(x).lower())
final_df.to_csv('processed_tmdb_dataset.csv', index=False)

print("\nData processing complete! All columns preserved correctly.")