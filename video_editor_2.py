from rapidfuzz import fuzz
import random  # Import the random module for selecting random movies
import statistics  # Import the statistics module for calculating average and median ratings


class MovieDatabase:
    """Class to represent a database of movies with their ratings and release years."""

    def __init__(self):
        """Initialize the movie database with some pre-defined movies."""
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
            "Star Wars: Episode V": {"rating": 8.7, "year": 1980}
        }


    def list_movies(self):
        """List all movies and their ratings and release years."""
        print(f"{len(self.movies)} movies in total")
        print()  # Ensures a blank line between header and content
        for movie, details in self.movies.items():
            print(f"{movie}: {details['rating']} ({details['year']})")


    def add_movie(self):
        """Add a new movie and its rating and release year to the database."""
        name = input("Enter movie name: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        rating = float(input("Enter movie rating: "))
        year = int(input("Enter movie release year: "))
        if 0 <= rating <= 10:
            self.movies[name] = {"rating": rating, "year": year}
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Rating must be between 0 and 10")


    def delete_movie(self):
        """Delete a movie from the database."""
        name = input("Enter movie name to delete: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        if name in self.movies:
            del self.movies[name]
            print(f"'{name}' deleted")
        else:
            print(f"Error: '{name}' not found")


    def update_movie(self):
        """Update the rating of an existing movie."""
        name = input("Enter movie name to update: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        if name in self.movies:
            rating = float(input("Enter new rating: "))
            if 0 <= rating <= 10:
                self.movies[name]["rating"] = rating
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

            worst_movie = min(self.movies, key=lambda x: self.movies[x]["rating"])
            worst_rating = self.movies[worst_movie]["rating"]

            # Print the stats
            print(f"Average rating: {average}")
            print(f"Best movie: {best_movie} (Rating: {best_rating})")
            print(f"Worst movie: {worst_movie} (Rating: {worst_rating})")
        else:
            print("No movies in database")


    def random_movie(self):
        """Display a random movie and its rating."""
        import random
        name = random.choice(list(self.movies.keys()))
        print()
        print(f"Random movie: {name}, Rating: {self.movies[name]['rating']}")


    def search_movie(self):
        """Search for movies by a part of their name (case-insensitive) with fuzzy matching."""
        search_term = input("Enter part of movie name to search: ").lower()
        found_movies = {}
        
        # Iterate through movies and calculate similarity
        for name, details in self.movies.items():
            similarity = fuzz.partial_ratio(search_term, name.lower())
            if similarity > 70:  # Adjust similarity threshold as needed
                found_movies[name] = details

        if found_movies:
            for name, details in found_movies.items():
                print()
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

