# Importing necessary libraries
import pandas as pd

# Define the path where data files are located
# Adjust this path to match your local setup
data_path = 'C:/Users/user/Desktop/'

# Load movies and ratings datasets from CSV files
movies_df = pd.read_csv(data_path + 'movies.csv')
ratings_df = pd.read_csv(data_path + 'ratings.csv')

# Prompt the user to input their favorite movie name
movie_name = input("Enter the title of the movie you like: ")

# Prompt the user to specify how many recommendations they'd like to receive (default is 5 if no input given)
num_recommendations = int(input("Enter the number of movie recommendations (default: 5): ") or 5)

# Merge the movies and ratings dataframes based on the 'movieId' column
df = movies_df.merge(ratings_df, on='movieId')

# Check if the provided movie title exists in the dataset
movie_in_db = df['title'] == movie_name

# If the movie doesn't exist, inform the user and exit
if not movie_in_db.any():
    print(f'Movie with title "{movie_name}" cannot be found in the dataset.')
    exit(1)

# Filter out the ratings of users who liked the given movie
movie_db = df[movie_in_db].sort_values(by='rating', ascending=False)

# Extract a list of user IDs who liked the movie
liked_users = list(movie_db['userId'].values)

# Initialize an empty list to store recommended movies
recommended_movies = []

# For each user who liked the given movie, 
# find other movies they rated highly and add them to the recommended movies list
for user in liked_users:
    rated_movies = df[(df['userId'] == user) & (df['title'] != movie_name)]
    top_rated_movies = rated_movies.sort_values(by='rating', ascending=False).iloc[:num_recommendations]
    recommended_movies.extend(list(top_rated_movies['title'].values))

# Remove duplicate movie recommendations and limit the list to the specified number
recommended_movies = list(set(recommended_movies))[:num_recommendations]

# Display the recommended movies to the user
print(f'Movie recommendations for "{movie_name}":')
print()
for i, movie in enumerate(recommended_movies):
    print(f'[{i + 1}]: {movie}')
print('-' * 30)
