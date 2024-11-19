import json
from istorage import IStorage

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
        with open(self.fiel_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent= 4)

    def list_movies(self):
        """List all movies from the JSON file."""
        return self._load_movies()
    
    def add_movie(self, title, year, rating, poster_url):
        """Add a new Movie to the JSON file."""
        movies = self._load_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")
        
        # Store the movie data including poster URL
        movies[title] = {
            "year": year, 
            "rating": rating, 
            "poster_url": poster_url
        }
        self._save_movies(movies)

    def delete_movies(self,title):
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
