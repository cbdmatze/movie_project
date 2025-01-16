import csv
from storage.istorage import IStorage


class StorageCsv(IStorage):
    """
    A class to handle movie storage using CSV files.

    This class provides methods for storing, listing, adding, updating, and deleting 
    movie data from a CSV file. The CSV file is used as the persistent storage medium.
    """

    def __init__(self, file_path):
        """
        Initialize the storage with the path to the CSV file.
        
        Args:
            file_path (str): The file path to the CSV file for storing the movie data.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Retrieve a dictionary of all movies stored in the CSV file.
        
        Returns:
            dict: A dictionary where each key is a movie title, and the value is
            a dictionary with the movie's 'rating', 'year', and 'poster_url'.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Populate the dictionary with movie data from CSV
                    movies[row['title']] = {
                        'rating': float(row['rating']), 
                        'year': int(row['year']),
                        'poster_url': row.get('poster_url', 'https://via.placeholder.com/300x450?text=No+Poster')
                    }
        except FileNotFoundError:
            # File doesn't exist yet, we return an empty dictionary
            pass
        return movies

    def add_movie(self, title, year, rating, poster_url="https://via.placeholder.com/300x450?text=No+Poster"):
        """
        Add a new movie to the CSV file.
        
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The IMDb rating of the movie.
            poster_url (str): The URL of the movie's poster image.
            
        Raises:
            ValueError: If the movie already exists in the storage.
        """
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")

        # Append the new movie to the CSV file
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster_url'])
            # If the file is empty, write the header first
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'title': title,
                'rating': rating,
                'year': year,
                'poster_url': poster_url
            })

    def delete_movie(self, title):
        """
        Delete a movie from the CSV file.
        
        Args:
            title (str): The title of the movie to delete.
            
        Raises:
            ValueError: If the movie is not found in the storage.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            # Rewrite the CSV file without the deleted movie
            self._write_movies_to_csv(movies)
        else:
            raise ValueError(f"Movie '{title}' not found in the database.")

    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        
        Raises:
            ValueError: If the movie is not found in the storage.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            # Rewrite the CSV file with the updated movie
            self._write_movies_to_csv(movies)
        else:
            raise ValueError(f"Movie '{title}' not found in the database.")

    def _write_movies_to_csv(self, movies):
        """
        Helper method to write the current list of movies to the CSV file.
        
        Args:
            movies (dict): A dictionary of movies to save in the CSV file.
        """
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster_url'])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    'title': title,
                    'rating': details['rating'],
                    'year': details['year'],
                    'poster_url': details.get('poster_url', 'https://via.placeholder.com/300x450?text=No+Poster')
                })

    def get_file_path(self):
        """
        Return the file path where the CSV file is stored.
        
        Returns:
            str: The file path to the CSV file.
        """
        return self.file_path
