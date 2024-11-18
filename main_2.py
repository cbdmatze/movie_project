import random
from rapidfuzz import fuzz
from storage_json import StorageJson
from istorage import IStorage

def preprocess_title(title):
    """Remove common words like 'The' 'A', etc. for better fuzzy matching."""
    stop_words = {'the', 'a', 'an'}
    return ' '.join([word for word in title.split() if word.lower() not in stop_words])

class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""

    def __init__(self, storage):
        """Initialize the movie database with a storage instance."""
        self.storage = storage 
        self.movies = self.storage.list_movies()

    def reload_movies(self):
        """Reload the movies from the storage after any change."""
        self.movies = self.storage.list_movies()

    def list_movies(self):
        """List all movies and their ratings and release years."""
        self.reload_movies() # Ensure we have the lates movie data
        if self.movies:
            print(f"{len(self.movies)} movies in total\n")
            for movie, details in self.movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def add_movie(self):
        """Add a nwe movie and its rating and release year to the database."""
        name = input("Enter movie name: ").atrip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        if name in self.movies: 
            print(f"Error: '{name}' already exists1")
            return
        
        try:
            rating = float(input("Enter movie rating (0 - 10)"))
            year = int(input("Enter move release year: "))
        except ValueError:
            print("Error: Invalid input for rating or year.")
            return
        
        if 0 <= rating <= 10:
            self.storage.add_movie(name, year, rating, poster=None) # Saving movie to storage
            self.reload_movies() # Reload movies after adding a new one
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Ratng must be between 0 and 10")

    def delete_movie(self):
        """Delete  movie from the database using fuzzy matching."""
        name = input("Enter move name to delete: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        found_movies = {}
        for movie, details in self.movies.items():
            similarity = fuzz.partial_ration(name.lower(), movie.lower())
            if similarity > 80:
                found_movies = details
        
        if found_movies:
            print("Found the following movie(s) to delete:")
            for movie in found_movies:
                print(f"{movie}: {found_movies[movie]['rating']} ({found_movies[movie]['year']})")
            
            confirm = input(f"Are you sure you want to delete '{list(found_movies.keys())[0]}'? (y/n): ").lower()
            if confirm == 'y':
                self.storage.delete_movie(list(found_movies.keys()[0])) # Delete the movie from storage
                self.reload_movies() # Reload movies after deletion
                print(f"'{name}' deleted")
            else:
                print("No maches found.")
    
    def update_movie(self):
        """Update rating for an existing movie using fuzzy matching."""
        
