from istorage import IStorage
from rapidfuzz import fuzz

class MovieApp:
    def __init__(self, storage: IStorage):
        """Initialize the MovieApp with a storage instance."""
        self._storage = storage

    def _command_list_movies(self):
        """List all movies in the database."""
        movies = self._storage.list_movies()
        if movies:
            print(f"{len(movies)} movies in total\n")
            for movie, details in movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _command_add_movie(self):
        """Add a new movie to the database."""
        name = input("Enter movie name: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        if name in self._storage.list_movies():
            print(f"Error: '{name}' already exists!")
            return
        
        try:
            rating = float(input("Enter movie rating (0 - 10): "))
            year = int(input("Enter movie release year: "))
        except ValueError:
            print("Error: Invalid input for rating or year.")
            return
        
        if 0 <= rating <= 10:
            self._storage.add_movie(name, year, rating)
            print(f"'{name}' added with rating {rating} and year {year}")
        else:
            print("Error: Rating must be between 0 and 10")

    def _command_delete_movie(self):
        """Delete a movie from the database."""
        name = input("Enter movie name to delete: ").strip()
        if not name:
            print("Error: Movie name cannot be empty")
            return

        movies = self._storage.list_movies()
        found_movies = {}
        for movie, details in movies.items():
            similarity = fuzz.partial_ratio(name.lower(), movie.lower())
            if similarity > 80:
                found_movies[movie] = details

        if found_movies:
            print("Found the following movie(s) to delete:")
            for movie in found_movies:
                print(f"{movie}: {found_movies[movie]['rating']} ({found_movies[movie]['year']})")

            confirm = input(f"Are you sure you want to delete '{list(found_movies.keys())[0]}'? (y/n): ").lower()
            if confirm == 'y':
                self._storage.delete_movie(list(found_movies.keys())[0])
                print(f"'{list(found_movies.keys())[0]}' deleted")
        else:
            print("No matches found.")

    def _command_movie_stats(self):
        """Display statistics about the movies."""
        movies = self._storage.list_movies()
        if movies:
            ratings = [details['rating'] for details in movies.values()]
            average = round(sum(ratings) / len(ratings), 2)

            best_movie = max(movies, key=lambda x: movies[x]["rating"])
            worst_movie = min(movies, key=lambda x: movies[x]["rating"])

            print(f"Average rating: {average}")
            print(f"Best movie: {best_movie} (Rating: {movies[best_movie]['rating']})")
            print(f"Worst movie: {worst_movie} (Rating: {movies[worst_movie]['rating']})")
        else:
            print("No movies in database.")

    def _command_search_movie(self):
        """Search movies by part of their name (case-insensitive) with fuzzy matching."""
        search_term = input("Enter part of movie name to search: ").lower()
        found_movies = {}
        for name, details in self._storage.list_movies().items():
            similarity = fuzz.partial_ratio(search_term, name.lower())
            if similarity > 80:
                found_movies[name] = details

        if found_movies:
            for name, details in found_movies.items():
                print(f"{name}: {details['rating']} ({details['year']})")
        else:
            print("No matches found.")

    def _command_movies_sorted_by_rating(self):
        """Display all movies sorted by rating in descending order."""
        sorted_movies = sorted(self._storage.list_movies().items(), key=lambda x: x[1]["rating"], reverse=True)
        for name, details in sorted_movies:
            print(f"{name}: {details['rating']} ({details['year']})")

    def run(self):
        """Run the movie app menu."""
        while True:
            print("\n********** My Movies Database **********\n")
            print("Menu:\n")
            print("0. Exit")
            print("1. List movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Movie Stats")
            print("5. Search Movie")
            print("6. Movies Sorted by Rating\n")

            choice = input("Enter a choice (0 - 6): ")
            print()

            if choice == "0":
                print("Bye!\n")
                break
            elif choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_movie_stats()
            elif choice == "5":
                self._command_search_movie()
            elif choice == "6":
                self._command_movies_sorted_by_rating()
            else:
                print("Invalid choice. Please select a valid option from the menu.\n")
