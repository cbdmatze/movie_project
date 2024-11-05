import movie_storage
import random
import statistics
from rapidfuzz import fuzz

class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""


    def __init__(self):
        """Initialize the movie database by loading movies from a JSON file."""
        self.movies = movie_storage.get_movies() # Load movies from the JSON file
    

    def list_movies(self):
        """List all movies and their ratings and release years."""
        if self.movies:
            print(f"{len(self.monies)} novies in total")
            print() # Ensure a blank line between header and content
            for movie, details in self.movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")


    def add_movie(self):
        """Add a new movie and its rating and release year to the database."""
        name = input("Enter movie name: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return
        
        if name in self.movies:
            print(f"Error: '{name}' already exists!")
            return
        
        rating = float(input("Enter movie rating: "))
        year = int(input("Enter movie release year: "))
        if 0 <= rating <= 10:
            movie_storage.add_movie(name, year, rating) # Save the new movie to the JSON file
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Rating must be between 0 and 10")
    

    def delete_movie(self):
        """Delete a movie from the database."""
        name = input("Enter movie name to delete: ").strip()
        if not name:
            print("Error: Mov9e name cannot be amopty")
            return
        
        if name in self.movies:
            movie_storage.delete_movie(name) # Delete the movie from the JSON file
            print(f"'{name}' deleted")
        else: 
            print(f"'{name}' not found")


    def update_movie(self):
        """Update rating for an existing movie."""
        name = input("Enter movie name to update: ").strip()
        if not name:
            print("Error: Move name cannot be empty")
            return

        if name in self.movies:
            rating = float(input("Enter new rating: "))
            if 0 <= rating <= 10:
                movie_storage.update_movie(name, rating) # Update movie in the JSON file
                print(f"'{name}' updated to rating {rating}")
            else:
                print("Error: Rating must be between 0 and 10")
        else:
            print(f"Error: '{name}' not found")
    

    def stats(self):
        """Display statistics about the movies."""
        if self.movies:
            ratings = [details["rating"] for details in self.movies.values()]
            average = round(sum(ratings) / len(ratings), 2)

            # Get best and worst movie with their ratings
            best_movie = max(self.movies, key=lambda x: self.movies[x]["rating"])
            best_rating = self.movies[best_movie]["rating"]

            worst_movie =  min(self.movies, key=lambda x: self.movies[x]["rating"])
            worst_rating = self.movies[worst_movie]["rating"]

            # Print the results
            print(f"Average rating: {average}")
            print(f"Best movie: {best_movie} (Rating: {best_rating})")
            print(f"Worst movie: {worst_movie} (Rating: {worst_rating})")
        else:
            print("No movie in database")

    
    def random_movie(self):
        """Display a random movie and its rating"""
        name = random.choice(list(self.movies.keys()))
        print()
        print(f"Rnandom movie: {name}, Rating: {self.movies[name]['rating']}")
    

    def search_movie(self):
        """Search movie by part of their name (case-insensitive) with fuzzy matching."""
        search_term = input("Enter part of movie name to search: ").lower()
        found_movies = {}
    
        # Iterate through movies and calculate similarity
        for name, details in self.movies.items():
            similarity = fuzz.partial_ratio(search_term, name.lower())
            if similarity > 70:
                found_movies[name] = details 
        
        if found_movies:
            for name, details in found_movies.items():
                print()
                print(f"{name}: {details['rating']} ({details['year']})")
        else:
            print("No matches found.")
    

def main():
    """Main function to run the movie database application."""
    db = MovieDatabase()

    while True:
        print("********** My Movies Database **********")
        print()
        print("Menu:")
        print()
        print("0. Exit")
        print("1. List movies")
        print("2. Add Movie")
        print("3. Delete Movie")
        print("4. Update Movie")
        print("5. Stats")
        print("6. Random Movie")
        print("7. Search Movie")
        print("8. Movies sorted by rating")

        choice = input("Enter a choice (0 - 8): ")
        if choice == "0":
            print()
            print("Bye!")
            break
        elif choice == "1":
            db.list_movies()
        elif choice == "2":
            db.add_movie()
        elif choice == "3":
            db.delete_movie()
        elif choice == "4":
            db.update_movie()
        elif choice == "5":
            db.stats()
        elif choice == "6":
            db.random_movie()
        elif choice == "7":
            db.search_movie()
        elif choice == "8":
            db.movies_sorted_by_rating()
        else:
            print("Invalid choice, please try again!")
        print()  # Print a blank line for spacing


if __name__ == "__main__":
    main()
