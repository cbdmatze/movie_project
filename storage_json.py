import json
from istorage import IStorage

class StorageJson(IStorage):
    """JSON storage implementation for movie data."""

    def __init__(self, file_path):
        """Initialize with a specific JSON file path."""
        self.file_path = file_path

    def load_movies(self):
        """Helper method to load movies from the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} # Return empty dictionary if the file doesn't exist
        
    def save_movies(self, movies):
        