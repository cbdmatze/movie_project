import random # Import random module for selecting random movies
import statistics # Import statistics module for calculating average and median ratings


class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""

def __init__(self):
    self.movies = {
            "The Shawshank Redemption": {"rating": 9.5, "year": 1994},
            "Pulp Fiction": {"rating": 8.8, "year": 1994},
            "The Room": {"rating": 3.6, "year": 2003},
            "The Godfather": {"rating": 9.2, "year": 1972},
            "The Godfather: Part II": {"rating": 9.0, "year": 1974},
            "The Dark Knight": {"rating": 9.0, "year": 2008},
            "12 Angry Men": {"rating": 8.9, "year": 1957},
            "Everything Everywhere All At Once": {"rating": 8.9, "year": 2022},
            "Forrest Gump": {"rating": 8.9, "year": 1994},
            "Star Wars: Episode v": {"rating": 8.7, "year": 1980}
    }


def list_movies(self):
    """List all movies with their ratings and their year."""
    print(f"{len(self.movies)} movies in total")
    print() # Blank line between header and content
    for movies, details in self.movies.items():
        print(f"{movie.title()} - Rating: {details['rating']}, Year: {details['year']}")


def add_movie(self):
    """Add a new movie with its rating and year."""
    name = input("Enter movie name: ").strip()
    if not name:
        print("Error: Movie name cannot be empty")
        return
    rating = float(input("Enter movie rating: "))
    year = int(input("Enter movie's year of release: "))

    # Add the movie and its properties to the mevies dictionary
    self.movies.lower() = {"rating": rating, "year": year}
    print(f"'{name}' added with rating {rating} and year {year}")


def delete_movie(self):
    """Deletes a movie from the database."""
    name = input("Enter movie name to delete: ").strip()
    if not name:
        print("Error: Movie name cannot be empty")
        return
    
    name_lower = name.lower()
    if name_lower in self.movies:
        del self.movies[name_lower]
        print(f"'{name}' deleted")
    else:
        print(f"Error: '{name}' not found")


def update_movie(self):
    """Update the rating of an existing movie."""
    name = input("Enter movie name to update: ").strip()
    if not name:
        print("Error: Movie name cannot be empty")
        return
    name_lower = name.lower()
    if name_lower in self.movies:
        rating = float(input("Enter new rating: "))
        if 0 <= rating <= 10:
            self.movies[name_lower]["rating"] = rating
            print(f"'{name}' updated to rating '{rating}")
        else:
            print("Error: Rating must be between 0 and 10")
    else:
        print(f"Error: '{name}' not found")


def stats(self):
    """Display statistics about the movies in the database."""
    