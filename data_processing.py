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
# Drop rows where essential data for the model is missing
df.dropna(subset=['overview', 'genres', 'cast', 'director'], inplace=True)

# Convert string representations of lists back into actual lists
# MODIFIED: Added 'streaming_on' to this conversion step.
for col in ['genres', 'cast', 'streaming_on']:
    if col in df.columns:
        # Use a safe function to handle potential malformed strings
        def safe_literal_eval(val):
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                return [] # Return empty list if the string is not a valid list
        df[col] = df[col].apply(safe_literal_eval)

# --- Feature Engineering for Recommendation Model ---
# Create space-less versions for the model, but keep the originals for display
def remove_spaces(text_list):
    return [str(item).replace(" ", "") for item in text_list]

# Create new columns for the tags, leaving originals untouched
df['genres_tags'] = df['genres'].apply(remove_spaces)
df['cast_tags'] = df['cast'].apply(lambda cast_list: remove_spaces(cast_list[:5])) # Use top 5 cast for tags
df['director_tags'] = df['director'].apply(lambda x: str(x).replace(" ", ""))
df['overview_list'] = df['overview'].apply(lambda x: x.split())

# Create the 'tags' column from the new _tags columns
df['tags'] = df['overview_list'] + df['genres_tags'] + df['cast_tags'] + df['director_tags'].apply(lambda x: [x])

# --- Create the Final DataFrame for the App and Model ---
# We select all columns needed for the app and the model.
# MODIFIED: Added 'streaming_on' to the list of columns to keep.
final_df = df[[
    'id', 'title', 'release_year', 'overview', 'genres', 'cast', 'director',
    'rating', 'vote_count', 'popularity', 'revenue', 'poster_path',
    'streaming_on',  # <-- THIS IS THE NEWLY ADDED COLUMN
    'tags'
]].copy()

# Final processing for the 'tags' column
final_df['tags'] = final_df['tags'].apply(lambda x: " ".join(x).lower())

# Save the processed data, which will be used by model_builder.py
final_df.to_csv('processed_tmdb_dataset.csv', index=False)

print("\nData processing complete! 'streaming_on' column has been included.")