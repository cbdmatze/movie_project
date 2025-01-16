import json
from storage.istorage import IStorage
import os

class StorageJson(IStorage):
    """
    A class to handle movie storage using JSON files.
    
    This class provides methods for storing, listing, adding, updating, and deleting
    movie data from a JSON file. The JSON file is used as the persistent storage medium.
    """

    def __init__(self, file_path):
        """
        Initialize with the path to the JSON file for storing movie data.
        
        Args:
            file_path (str): The file path to the JSON file for storing movie data.
        """
        self.file_path = file_path
        self._validate_file_path()

    def _validate_file_path(self):
        """
        Sanitize and validate the file path.
        
        Ensures that the file path is absolute and that the file exists.
        
        Raises:
            FileNotFoundError: If the specified file path does not exist.
        """
        self.file_path = os.path.abspath(self.file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found!")

    def _load_movies(self):
        """
        Helper method to load movie data from the JSON file.
        
        Returns:
            dict: A dictionary of movies from the JSON file.
            
        Raises:
            ValueError: If the file is corrupted or empty.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: movies.json is empty or corrupted. Initializing empty data.")
            return {}  # Return empty dictionary if the file doesn't exist or is invalid

    def _save_movies(self, movies):
        """
        Helper method to save movies to the JSON file.
        
        Args:
            movies (dict): A dictionary of movies to save in the JSON file.
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=4)

    def list_movies(self):
        """
        Retrieve all movies from the JSON file.
        
        Returns:
            dict: A dictionary of all movies stored in the JSON file.
        """
        return self._load_movies()

    def add_movie(self, title, year, rating, poster_url="https://via.placeholder.com/300x450?text=No+Poster"):
        """
        Add a new movie to the JSON file.
        
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The IMDb rating of the movie.
            poster_url (str): The URL of the movie's poster image.
            
        Raises:
            ValueError: If the movie already exists in the storage.
        """
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

    def delete_movie(self, title):
        """
        Delete a movie from the JSON file.
        
        Args:
            title (str): The title of the movie to delete.
        
        Raises:
            ValueError: If the movie is not found in the storage.
        """
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
            
        Raises:
            ValueError: If the movie is not found in the storage.
        """
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
        else:
            raise ValueError(f"Movie: '{title}' not found.")

    def get_file_path(self):
        """
        Return the file path where the JSON file is stored.
        
        Returns:
            str: The file path to the JSON file.
        """
        return self.file_path
