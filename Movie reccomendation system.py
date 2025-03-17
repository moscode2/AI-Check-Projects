import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------
# 1. Data Setup
# -----------------
# User-Movie Rating Matrix (User-Item Matrix)
rating_data = {
    'User': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Movie1': [5, 4, np.nan, 2, 1],
    'Movie2': [4, np.nan, 3, 1, 2],
    'Movie3': [np.nan, 2, 4, 1, 5],
    'Movie4': [1, 2, 2, 5, 4],
    'Movie5': [np.nan, 5, 3, 2, 1]
}

ratings_df = pd.DataFrame(rating_data)
ratings_df.set_index('User', inplace=True)

# Movie Features for Content-Based Filtering (Genre, Year, etc.)
movie_features = {
    'Movie': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5'],
    'Genre': ['Action', 'Comedy', 'Action', 'Drama', 'Comedy'],
    'Year': [2000, 1999, 2010, 2005, 2020]
}

movie_features_df = pd.DataFrame(movie_features)

# -------------------------------
# 2. Collaborative Filtering
# -------------------------------
def collaborative_filtering(user_name, num_recommendations=2):
    """
    Recommends movies using User-Based Collaborative Filtering
    
    Args:
    user_name (str): The name of the user to recommend movies for.
    num_recommendations (int): The number of movies to recommend.
    
    Returns:
    list: List of recommended movie titles.
    """
    # Step 1: Calculate similarity between users
    user_ratings = ratings_df.fillna(0)  # Fill NaN with 0 for similarity calculation
    user_similarity = cosine_similarity(user_ratings)
    
    # Convert similarity matrix to DataFrame for readability
    similarity_df = pd.DataFrame(user_similarity, index=ratings_df.index, columns=ratings_df.index)
    
    # Step 2: Get top similar users for the given user
    similar_users = similarity_df[user_name].sort_values(ascending=False)
    similar_users = similar_users.drop(user_name)  # Drop the user's own entry
    
    # Step 3: Recommend movies that the similar users rated highly but the target user hasn't watched
    user_ratings = ratings_df.loc[user_name]
    unseen_movies = user_ratings[user_ratings.isnull()].index  # Movies the user hasn't seen
    
    # Score unseen movies by the weighted rating from similar users
    scores = {movie: 0 for movie in unseen_movies}
    
    for similar_user, similarity_score in similar_users.items():
        for movie in unseen_movies:
            if not np.isnan(ratings_df.loc[similar_user, movie]):
                scores[movie] += similarity_score * ratings_df.loc[similar_user, movie]
    
    # Sort movies by score and return top N
    recommended_movies = sorted(scores, key=scores.get, reverse=True)[:num_recommendations]
    
    return recommended_movies

# -------------------------------
# 3. Content-Based Filtering
# -------------------------------
def content_based_filtering(user_name, num_recommendations=2):
    """
    Recommends movies using Content-Based Filtering
    
    Args:
    user_name (str): The name of the user to recommend movies for.
    num_recommendations (int): The number of movies to recommend.
    
    Returns:
    list: List of recommended movie titles.
    """
    # Step 1: Get the movies the user has already rated
    user_ratings = ratings_df.loc[user_name]
    seen_movies = user_ratings[user_ratings.notnull()].index  # Movies the user has seen
    
    # Step 2: Calculate a "user profile" based on the movies they've rated
    user_movie_features = movie_features_df[movie_features_df['Movie'].isin(seen_movies)]
    genre_counts = user_movie_features['Genre'].value_counts(normalize=True)  # Calculate preference for genres
    
    # Step 3: Rank unseen movies by how closely they match the user's preferences
    unseen_movies = movie_features_df[~movie_features_df['Movie'].isin(seen_movies)]
    unseen_movies['MatchScore'] = unseen_movies['Genre'].apply(lambda genre: genre_counts.get(genre, 0))
    
    # Step 4: Recommend top N movies with the highest match score
    top_movies = unseen_movies.sort_values(by='MatchScore', ascending=False).head(num_recommendations)
    
    return top_movies['Movie'].tolist()

# -------------------------------
# 4. Usage Examples
# -------------------------------
if __name__ == "__main__":
    print("\nCollaborative Filtering Recommendations for Alice:")
    print(collaborative_filtering(user_name='Alice', num_recommendations=2))
    
    print("\nContent-Based Filtering Recommendations for Alice:")
    print(content_based_filtering(user_name='Alice', num_recommendations=2))
