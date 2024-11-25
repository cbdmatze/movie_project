from abc import ABC, abstractmethod


class IStorage(ABC):
    """Interface for movie storage operations."""

    @abstractmethod
    def list_movies(self):
        """
        Return a dictionary of all movies in the format:
        {
            "Movie Title": {
                "year": <release_year>,
                "rating": <rating>,
                "poster_url": <poster_url>
            },
            ...
        }
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster_url):
        """
        Add a new movie.

        Args:
            title (str): Movie title.
            year (int): Release year of the movie.
            rating (float): IMDb rating of the movie.
            poster_url (str): URL of the movie poster image.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie by its title.

        Args:
            title (str): The title of the movie to delete.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Update the rating of a movie.

        Args:
            title (str): Movie title.
            rating (float): New rating for the movie.
        """
        pass

    @abstractmethod
    def get_file_path(self):
        """
        Get the file path of the storage, useful for generating HTML output.

        Returns:
            str: The file path where the movie data is stored.
        """
        pass
