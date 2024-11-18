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
        
