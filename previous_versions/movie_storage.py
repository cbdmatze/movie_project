
import json

FILE_NAME = 'data.json'

def get_movies():
    """Load and return the movie data from the JSON file."""
    try:
        # Open the JSON file in read mode with UTF-8 encoding
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return an empty dictionary if the file is not found
        return {}

def save_movies(movies):
    """Save the current movie data to the JSON file."""
    # Open the JSON file in write mode with UTF-8 encoding
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        # Dump the movie data to the file with indentation
        json.dump(movies, f, indent=4)

def add_movie(name, year, rating):
    """Add a new movie to the JSON file."""
    # Load the current movies
    movies = get_movies()
    # Add the new movie data to the dictionary
    movies[name] = {"year": year, "rating": rating}
    # Save the updated movies back to the file
    save_movies(movies)

def delete_movie(name):
    """Delete a movie from the JSON file."""
    # Load the current movies
    movies = get_movies()
    if name in movies:
        # Remove the movie from the dictionary
        del movies[name]
        # Save the updated list back to the file
        save_movies(movies)

def update_movie(name, rating):
    """Update a movie's rating in the JSON file."""
    # Load the current movies
    movies = get_movies()
    if name in movies:
        # Update the movie's rating in the dictionary
        movies[name]["rating"] = rating
        # Save the changes to the file
        save_movies(movies)
