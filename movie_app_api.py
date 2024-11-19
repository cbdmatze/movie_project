import requests
import json
from rapidfuzz import fuzz
from istorage import IStorage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class MovieApp:
    def __init__(self, storage:IStorage):
        """Initialize the MovieApp with a storage instance."""
        self._storage = storage
        self.api_key = os.getenv("OMDB_API_KEY") # Fetch API key from environment

    def _command_list_movies(self):
        """List all movies in the database."""
        movies = self._storage.list_movies()
        if movies:
            print(f"{len(movies)} movies in total\n")
            for movie, details in movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _fetch_movie_from_api(self, title):
        """Fetch movie details from the OMDb API."""
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            movie_data = response.json()

            # Check if movie was found
            if movie_data.get("Response") == "False":
                raise ValueError(f"Movie '{title}' not found in OMDb")
            
            # Extract relevant data
            return {
                "title": movie_data["Title"], 
                "year": int(movie_data["Year"]),
                "rating": float(movie_data["imdbRating"]), 
                "poster_url": movie_data.get("Poster", "") # Fallback to empty string if poster is not available
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OMDb API: {e}")
        except ValueError as e:
            print(e)
            return None
    
    def _command_add_movie(self):
        """Add a new movie to tha database."""
        