import random
from rapidfuzz import fuzz
from previous_versions.storage_json import StorageJson
from data.storage.istorage import IStorage

def preprocess_title(title):
    """Remove common words like 'The', 'A', etc. for better fuzzy matching."""
    stop_words = {'the', 'a', 'an'}
    return ' '.join([word for word in title.split() if word.lower() not in stop_words])

class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""

    def __init__(self, storage):
        """Initialize the movie database with a storage instance."""
        self.storage = storage 
        self.movies = self.storage.list_movies()

    def reload_movies(self):
        """Reload the movies from the storage after any change."""
        self.movies = self.storage.list_movies()

    def list_movies(self):
        """List all movies and their ratings and release years."""
        self.reload_movies()  # Ensure we have the latest movie data
        if self.movies:
            print(f"{len(self.movies)} movies in total\n")
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
        
        try:
            rating = float(input("Enter movie rating (0 - 10): "))
            year = int(input("Enter movie release year: "))
        except ValueError:
            print("Error: Invalid input for rating or year.")
            return
        
        if 0 <= rating <= 10:
            self.storage.add_movie(name, year, rating)  # Saving movie to storage
            self.reload_movies()  # Reload movies after adding a new one
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Rating must be between 0 and 10")

    def delete_movie(self):
        """Delete a movie from the database using fuzzy matching."""
        name = input("Enter movie name to delete: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        found_movies = {}
        for movie, details in self.movies.items():
            similarity = fuzz.partial_ratio(name.lower(), movie.lower())
            if similarity > 80:
                found_movies[movie] = details
        
        if found_movies:
            print("Found the following movie(s) to delete:")
            for movie in found_movies:
                print(f"{movie}: {found_movies[movie]['rating']} ({found_movies[movie]['year']})")
            
            confirm = input(f"Are you sure you want to delete '{list(found_movies.keys())[0]}'? (y/n): ").lower()
            if confirm == 'y':
                self.storage.delete_movie(list(found_movies.keys())[0])  # Delete the movie from storage
                self.reload_movies()  # Reload movies after deletion
                print(f"'{list(found_movies.keys())[0]}' deleted")
        else:
            print("No matches found.")

    def update_movie(self):
        """Update rating for an existing movie using fuzzy matching."""
        name = input("Enter movie name to update: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return
    
        found_movies = {}
        for movie, details in self.movies.items():
            similarity = fuzz.partial_ratio(name.lower(), movie.lower())
            if similarity > 80: 
                found_movies[movie] = details
        
        if found_movies:
            print("Found the following movie(s) to update:")
            for movie in found_movies:
                print(f"{movie}: {found_movies[movie]['rating']} ({found_movies[movie]['year']})")

            confirm = input(f"Are you sure you want to update '{list(found_movies.keys())[0]}'? (y/n): ").lower()
            if confirm == 'y':
                try:
                    rating = float(input("Enter new rating (0 - 10): "))
                except ValueError:
                    print("Error: Invalid input for rating.")
                    return
                
                if 0 <= rating <= 10:
                    self.storage.update_movie(list(found_movies.keys())[0], rating)  # Update movie in storage
                    self.reload_movies()  # Reload movies after updating
                    print(f"'{list(found_movies.keys())[0]}' updated to rating {rating}")
                else:
                    print("Error: Rating must be between 0 and 10")
        else:
            print("No matches found.")

    def stats(self):
        """Display statistics about the movies."""
        if self.movies:
            ratings = [details['rating'] for details in self.movies.values()]
            average = round(sum(ratings) / len(ratings), 2)

            # Get best and worst movie with their ratings
            best_movie = max(self.movies, key=lambda x: self.movies[x]["rating"])
            best_rating = self.movies[best_movie]["rating"]

            worst_movie = min(self.movies, key=lambda x: self.movies[x]["rating"])
            worst_rating = self.movies[worst_movie]["rating"]

            # Print the results
            print(f"Average rating: {average}")
            print(f"Best movie: {best_movie} (Rating: {best_rating})")
            print(f"Worst movie: {worst_movie} (Rating: {worst_rating})")
        else:
            print("No movies in database.")

    def random_movie(self):
        """Display a random movie and its rating."""
        if not self.movies:
            print("No movies in database.")
            return

        name = random.choice(list(self.movies.keys()))
        print(f"Random movie: {name}, Rating: {self.movies[name]['rating']}")

    def search_movie(self):
        """Search movies by part of their name (case-insensitive) with fuzzy matching."""
        search_term = preprocess_title(input("Enter part of movie name to search: ")).lower()
        found_movies = {}

        # Iterate through movies and calculate similarity
        for name, details in self.movies.items():
            processed_name = preprocess_title(name.lower())
            similarity = fuzz.partial_ratio(search_term, processed_name)
            if similarity > 80:
                found_movies[name] = details
        
        if found_movies:
            for name, details in found_movies.items():
                print(f"{name}: {details['rating']} ({details['year']})")
        else:
            print("No matches found.")

    def movies_sorted_by_rating(self):
        """Display all movies sorted by rating in descending order."""
        sorted_movies = sorted(self.movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        for name, details in sorted_movies:
            print(f"{name}: {details['rating']} ({details['year']})")

def main():
    """Main function to run the movie database application."""
    storage = StorageJson('movies.json')
    db = MovieDatabase(storage)  # Passing the storage instance to MovieDatabase
    print()
    while True:
        print("********** My Movies Database **********\n")
        print("Menu:\n")
        print("0. Exit")
        print("1. List movies")
        print("2. Add Movie")
        print("3. Delete Movie")
        print("4. Update Movie")
        print("5. Stats")
        print("6. Random Movie")
        print("7. Search Movie")
        print("8. Movies sorted by rating\n")
        choice = input("Enter a choice (0 - 8): ")
        print()
        if choice == "0":
            print("Bye!\n")
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
            print("Invalid choice. Please select a valid option from the menu.\n")

# Run the main function if this file is executed directly
if __name__ == "__main__":
    main()
