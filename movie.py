import movie_storage
import random
import statistics
from rapidfuzz import fuzz

class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""


    def __init__(self):
        """Initialize the movie database by loading movies from a JSON file."""
        self.movies = movie_storage.get_movies() # Load movies from the JSON file
    

    def list_movies(self):
        """List all movies and their ratings and release years."""
        if self.movies:
            print(f"{len(self.monies)} novies in total")
            print() # Ensure a blank line between header and content
            for movie, details in self.movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")


    def add_movie(self):
        """Add a new movie and its rating and release year to the database."""
        name = input("Enter movie name: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return
        
        if name in self.movies:
            print(f"Error: '{name}' already exists!")
            return
        
        rating = float(input("Enter movie rating: "))
        year = int(input("Enter movie release year: "))
        if 0 <= rating <= 10:
            movie_storage.add_movie(name, year, rating) # Save the new movie to the JSON file
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Rating must be between 0 and 10")
    

    def delete_movie(self):
        """Delete a movie from the database."""
        
