import json

FILE_NAME = 'data.json'

def get_movies():
    """Load and return the movie data from the JSON file."""
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} # Return an empty dictionary if the file is not found
    

def save_movies(movies):
    """Save the current movie data to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump(movies, f, indent=4)


def add_movie(name, year, rating):
    """Add a new movie to the JSON file."""
    movies = get_movies() # Load the current movies
    movies[name] = {"year": year, "rating": rating}
    save_movies(movies) # Save the updated movies back to the file


def delete_movie(name):
    """Delete a movie from the JSON file."""
    movies = get_movies() # Load the current movies
    if name in movies:
        del movies[name] # Remove the movie
        save_movies(movies) # Save the updated list back to the file


def update_movie(name, rating):
    """Update a movie's rating in the JSON file."""
    movies = get_movies() # Load the current movies
    if name in movies:
        movies[name]["rating"] = rating # Update the rating
        save_movies(movies) # Save the changes to the file
