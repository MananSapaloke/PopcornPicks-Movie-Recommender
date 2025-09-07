# data_processing_enhanced.py - Enhanced version for larger datasets
import pandas as pd
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from typing import List, Dict

print("Starting enhanced data processing...")

# --- Load Data ---
try:
    df = pd.read_csv('tmdb_enhanced_dataset.csv')
    print(f"Successfully loaded enhanced dataset. Shape: {df.shape}")
except FileNotFoundError:
    print("Enhanced dataset not found, trying original dataset...")
    try:
        df = pd.read_csv('tmdb_full_dataset.csv')
        print(f"Loaded original dataset. Shape: {df.shape}")
    except FileNotFoundError:
        print("Error: No dataset found. Please run fetch_tmdb_data.py or fetch_tmdb_data_enhanced.py first.")
        exit()

# --- Enhanced Data Cleaning ---
print("\nStarting data cleaning...")

# Remove duplicates based on movie ID
initial_count = len(df)
df = df.drop_duplicates(subset=['id'], keep='first')
print(f"Removed {initial_count - len(df)} duplicate movies")

# Drop rows where essential data is missing
df.dropna(subset=['overview', 'genres', 'cast', 'director'], inplace=True)
print(f"Removed movies with missing essential data. Remaining: {len(df)}")

# Convert string representations of lists back into actual lists
def safe_literal_eval(val):
    """Safely convert string representations to lists."""
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

for col in ['genres', 'cast', 'streaming_on', 'production_countries']:
    if col in df.columns:
        df[col] = df[col].apply(safe_literal_eval)

# --- Enhanced Feature Engineering ---
print("\nStarting enhanced feature engineering...")

def remove_spaces(text_list):
    """Remove spaces from text for better matching."""
    return [str(item).replace(" ", "") for item in text_list]

def clean_text(text):
    """Clean and normalize text."""
    if pd.isna(text):
        return ""
    return str(text).lower().strip()

# Create enhanced tags for better recommendations
df['genres_tags'] = df['genres'].apply(remove_spaces)
df['cast_tags'] = df['cast'].apply(lambda cast_list: remove_spaces(cast_list[:5]))
df['director_tags'] = df['director'].apply(lambda x: str(x).replace(" ", "") if pd.notna(x) else "")
df['overview_clean'] = df['overview'].apply(clean_text)
df['overview_list'] = df['overview_clean'].apply(lambda x: x.split())

# Enhanced tag creation with more features
def create_enhanced_tags(row):
    """Create comprehensive tags for each movie."""
    tags = []
    
    # Overview words (limit to avoid over-weighting)
    tags.extend(row['overview_list'][:20])
    
    # Genres
    tags.extend(row['genres_tags'])
    
    # Cast (top 3 for better performance)
    tags.extend(row['cast_tags'][:3])
    
    # Director
    if row['director_tags']:
        tags.append(row['director_tags'])
    
    # Release decade for temporal similarity
    if pd.notna(row['release_year']):
        decade = str(int(row['release_year']) // 10 * 10) + "s"
        tags.append(decade)
    
    # Rating category
    if pd.notna(row['rating']):
        if row['rating'] >= 8.0:
            tags.append("highlyrated")
        elif row['rating'] >= 6.0:
            tags.append("wellrated")
        else:
            tags.append("lowrated")
    
    # Revenue category
    if pd.notna(row['revenue']) and row['revenue'] > 0:
        if row['revenue'] >= 100000000:  # $100M+
            tags.append("blockbuster")
        elif row['revenue'] >= 10000000:  # $10M+
            tags.append("commercial")
        else:
            tags.append("indie")
    
    return " ".join(tags)

df['enhanced_tags'] = df.apply(create_enhanced_tags, axis=1)

# --- Create Final Dataset ---
print("\nCreating final dataset...")

# Select columns for the final dataset
final_columns = [
    'id', 'title', 'original_title', 'release_year', 'overview', 'genres', 
    'cast', 'director', 'rating', 'vote_count', 'popularity', 'revenue', 
    'budget', 'runtime', 'poster_path', 'backdrop_path', 'streaming_on',
    'original_language', 'production_countries', 'adult', 'video',
    'enhanced_tags'
]

# Only include columns that exist in the dataframe
available_columns = [col for col in final_columns if col in df.columns]
final_df = df[available_columns].copy()

# Clean up the enhanced_tags column
final_df['enhanced_tags'] = final_df['enhanced_tags'].apply(lambda x: x.lower())

# Save processed data
final_df.to_csv('processed_tmdb_enhanced_dataset.csv', index=False)
print(f"Enhanced dataset saved with {len(final_df)} movies")

# --- Enhanced Model Building ---
print("\nBuilding enhanced recommendation model...")

# Use TF-IDF instead of CountVectorizer for better text representation
print("Vectorizing with TF-IDF...")
tfidf = TfidfVectorizer(
    max_features=10000,  # Increased for larger dataset
    stop_words='english',
    ngram_range=(1, 2),  # Include bigrams for better context
    min_df=2,  # Ignore terms that appear in less than 2 documents
    max_df=0.8  # Ignore terms that appear in more than 80% of documents
)

# Fit and transform the enhanced tags
vectors = tfidf.fit_transform(final_df['enhanced_tags']).toarray()
print(f"Vectorization complete. Shape: {vectors.shape}")

# Calculate cosine similarity
print("Calculating enhanced similarity matrix...")
similarity_matrix = cosine_similarity(vectors)
print(f"Similarity calculation complete. Shape: {similarity_matrix.shape}")

# --- Save Enhanced Model Artifacts ---
print("\nSaving enhanced model artifacts...")

# Save the enhanced DataFrame
with open('tmdb_enhanced_movies_df.pkl', 'wb') as f:
    pickle.dump(final_df, f)

# Save the enhanced similarity matrix
with open('tmdb_enhanced_similarity.pkl', 'wb') as f:
    pickle.dump(similarity_matrix, f)

# Save the TF-IDF vectorizer for future use
with open('tmdb_tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

print("Enhanced model building complete!")
print(f"Final dataset: {len(final_df)} movies")
print(f"Features: {vectors.shape[1]} TF-IDF features")
print(f"Similarity matrix: {similarity_matrix.shape}")

# --- Dataset Statistics ---
print("\nDataset Statistics:")
print(f"   - Total movies: {len(final_df):,}")
print(f"   - Years covered: {int(final_df['release_year'].min())} - {int(final_df['release_year'].max())}")
print(f"   - Average rating: {final_df['rating'].mean():.2f}")
print(f"   - Total genres: {len(set([g for sublist in final_df['genres'] for g in sublist]))}")
print(f"   - Movies with revenue data: {len(final_df[final_df['revenue'] > 0]):,}")

# --- Create Backward Compatibility ---
print("\nCreating backward compatibility files...")

# Create files with original names for existing app compatibility
with open('tmdb_movies_df.pkl', 'wb') as f:
    pickle.dump(final_df, f)

with open('tmdb_similarity.pkl', 'wb') as f:
    pickle.dump(similarity_matrix, f)

print("Backward compatibility files created.")
print("\nEnhanced data processing complete.")
print("Your enhanced movie recommender is ready.")
