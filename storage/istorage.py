from abc import ABC, abstractmethod


class IStorage(ABC):
    """Interface for movie storage operations.
    
    This interface defines methods for storing, updating, listing, and deleting
    movie data in a persistent storage format (CSV, JSON, etc.).
    
    Each implementing class must provide concrete implementations for these operations.
    """

    @abstractmethod
    def list_movies(self):
        """
        Retrieve all movies stored in the storage system.
        
        Returns:
            dict: A dictionary where keys are movie titles and values are dictionaries
            containing the movie's 'year', 'rating', and 'poster_url'.
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
        
        Raises:
            ValueError: If a movie with the same title already exists in storage.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie from the storage system by its title.
        
        Args:
            title (str): The title of the movie to delete.
            
        Raises:
            ValueError: If the movie with the specified title does not exist in the storage.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
            
        Raises:
            ValueError: If the movie with the specified title does not exist in storage.
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
