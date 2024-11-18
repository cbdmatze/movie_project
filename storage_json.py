import json
from istorage import IStorage

file_path = "/Users/martinawill/movie_project_2/movie_project-2/data.json"

class StorageJson(IStorage):
    """JSON storage implementation for movie data."""

    def __init__(self, file_path):
        """Initialize with a specific JSON file path."""
        self.file_path = file_path

    def _load_movies(self):
        """Helper method to load movies from the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} # Return empty dictionary if the file doesn't exist
        
    def _save_movies(self, movies):
        """Helper method to save movies to the JSON file."""
        with open(self.file_path, 'w', encoding='utf8') as f:
            json.dump(movies, f, indent=4)

    def list_movies(self):
        """List all movies from the JSON file."""
        return self._load_movies()
    
    def add_movies(self, title, year, rating):
        """Ad a new movie to the JSON file."""
        movies = self._load_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")
        movies[title] = {"year": year, "rating": rating}
        self._save_movies(movies)

    def delete_movies(self, title):
        """Delete a movie from the JSON file."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")
    
    def update_movie(self, title, rating):
        """Update the rating of an existing movie."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie: '{title}' not found.")