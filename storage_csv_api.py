import csv
from istorage import IStorage

class StorageCsv(IStorage):
    """Class to handle movie storage using CSV files."""

    def __init__(self, file_path):
        """Initialize the storage with the path to the CSV file."""
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries containing the movies.
        Example:
        {
            "Titanic": {
                "rating": 9.2,
                "year": 1995,
                "poster_url": "https://example.com/image.jpg"
            },
            ...
        }
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Populate the dictionary with movie data form CSV
                    movies[ros['title']] = {
                        'rating': float(row['rating']), 
                        'year': int(row['year']),
                        'poster_url': row.get('poster_url', '')
                    }
        except FileNotFoundError:
            # File doesn't exist yet, we return an empty dictionary
            pass
        return movies
    
    def add_movie(self, title, year, rating, poster_url):
        """Add a new movie to the CSV file."""
        # Append the new movie to the CSV file
        with open(self.fiel_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'rating', 'year', 'poster_url'])
            # If the file is empty, write the header first
            if csvfile.tell() == 0:
                writer.writeheader()
                writer.writerow({
                    'title': title, 
                    'rating': rating, 
                    'year': year, 
                    'poster_url': pster_url
                })

    def delete_movie(self, title):
        """Delete a moie from the CSV file."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            # Rewrite the CSV file without the deleted movie
            self._write_movies_to_csv(movies)
        else:
            raise ValueError(f"Movie: '{title}' not found in the database")
    
    def update_movie(self, title, rating):
        """Update the rating of an existing movie in the CSV file."""
        