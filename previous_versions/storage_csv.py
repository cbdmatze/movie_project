import csv
from istorage import IStorage

class StorageCsv(IStorage):
    """Class to handle mobie storage using csv files."""

    def __init__(self, file_path):
        """Initialize the storage with th path to the CSV file."""
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries containing the movies.
        Example:
        {
            "Titanic": {
                "rating": 9.2,
                "year": 1995
            },
            ...
        }
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Populate the dictionary with movie data from CSV
                    movies[row['title']] = {
                        'rating': float(row['rating']), 
                        'year': int(row['year'])
                    }
        except FileNotFoundError:
            # File doesn't exist yet, we return an empty dictionary
            pass
        return movies
    
    def add_movies(self, title, year, rating):
        """Add a new movie to the CSV file."""
        # Append the new movie to the CSV file
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year'])
            # If the file is empty, write the header first
            if csvfile.tell() == 0:
                writer.writeheader
            writer.writerow({'title': title, 'rating': rating, 'year': year})

    def delete_movie(self, title):
        """Delete a movie from the CSV file."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            # Rewrite the CSV file without the deleted movie
            self._write_movies_to_csv(movies)
        else:
            raise ValueError(f"Movie '{title}' not found in the database")
        
    def update_movie(self, title, rating):
        """Update the rating of an existing movie in the CSV file."""
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            # Rewrite the csv file with the updated movie
            self._write_movies_to_csv(movies)
        else:
            raise ValueError(f"Movie '{title}' not found in the database.")
    
    def _write_movies_to_csv(self, movies):
        """Helper method to write the current state of movies to the CSV file."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year'])
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({'title': title, 'rating': details['rating'], 'year': details['year']})
