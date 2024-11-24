from abc import ABC, abstractmethod


class IStorage(ABC):
    """Interface for movie storage operations."""


    @abstractmethod
    def list_movies(self):
        """Return a list of all movies."""
        pass


    @abstractmethod
    def add_movie(self, title, year, rating):
        """Add a new movie."""
        pass


    @abstractmethod
    def delete_movie(self, title):
        """Delete a movie by title."""
        pass


    @abstractmethod
    def update_movie(self, title, rating):
        """Update the rating of a movie."""
        pass
    