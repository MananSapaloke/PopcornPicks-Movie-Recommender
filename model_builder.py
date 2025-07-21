# model_builder.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

print("Starting model building process...")

# Load the processed dataset
try:
    df = pd.read_csv('processed_tmdb_dataset.csv')
    print(f"Successfully loaded processed_tmdb_dataset.csv. Shape: {df.shape}")
except FileNotFoundError:
    print("Error: processed_tmdb_dataset.csv not found. Please run data_processing.py first.")
    exit()

# --- Vectorization ---
# Initialize the CountVectorizer. We'll use more features since our tags are richer now.
# stop_words='english' removes common English words that don't add much meaning.
cv = CountVectorizer(max_features=7000, stop_words='english')

print("\nVectorizing the 'tags' column...")
# Convert the 'tags' column into a sparse matrix of token counts
vectors = cv.fit_transform(df['tags']).toarray()
print(f"Vectorization complete. Shape of vectors: {vectors.shape}")

# --- Calculate Cosine Similarity ---
# This creates a square matrix where similarity[i][j] is the similarity score between movie i and movie j.
print("\nCalculating cosine similarity matrix...")
similarity_matrix = cosine_similarity(vectors)
print(f"Similarity calculation complete. Shape of matrix: {similarity_matrix.shape}")

# --- Save the Model Artifacts ---
# We need to save two objects for our web app:
# 1. The movies DataFrame, which contains all the metadata (title, poster, revenue, etc.).
# 2. The similarity matrix, which is our actual 'model'.

# Define new, clear filenames for our TMDb model artifacts
movies_df_filename = 'tmdb_movies_df.pkl'
similarity_matrix_filename = 'tmdb_similarity.pkl'

print(f"\nSaving model artifacts to '{movies_df_filename}' and '{similarity_matrix_filename}'...")

# Save the entire DataFrame using pickle
with open(movies_df_filename, 'wb') as f:
    pickle.dump(df, f)

# Save the similarity matrix
with open(similarity_matrix_filename, 'wb') as f:
    pickle.dump(similarity_matrix, f)

print("\nModel building complete!")
print("The application is now ready for the final step: building the UI.")