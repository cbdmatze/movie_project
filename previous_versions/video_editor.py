import random  # Import the random module for selecting random movies
import statistics  # Import the statistics module for calculating average and median ratings

# Initial dictionary of movies and their ratings
movies = {
    "The Shawshank Redemption": 9.5,
    "Pulp Fiction": 8.8,
    "The Room": 3.6,
    "The Godfather": 9.2,
    "The Godfather: Part II": 9.0,
    "The Dark Knight": 9.0,
    "12 Angry Men": 8.9,
    "Everything Everywhere All At Once": 8.9,
    "Forrest Gump": 8.9,
    "Star Wars: Episode V": 8.7
}


def list_movies():
    """List all movies and their ratings."""
    print(f"{len(movies)} movies in total")
    print()  # This ensures a blank line between header and content
    for movie, rating in movies.items():
        print(f"{movie}: {rating}")


def add_movie():
    """Add a new movie and its rating to the database"""
    name = input("Enter movie name: ").strip()  # Ensure no empty spaces
    if not name:
        print("Error: Movie name cannot be empty")
        return

    name_lower = name.lower()  # Lowercase for consistent lookups
    rating = float(input("Enter movie rating: "))
    
    # Validate the rating range
    if 0 <= rating <= 10:
        movies[name_lower] = rating  # Add the movie and rating to the movies dictionary
        print(f"'{name}' added with rating {rating}")
    else:
        print("Error: Rating must be between 0 and 10")


def delete_movie():
    """Delete a movie from the database."""
    name = input("Enter movie name to delete: ").strip()
    if not name:
        print("Error: Movie name cannot be empty")
        return

    name_lower = name.lower()
    if name_lower in movies:
        del movies[name_lower]
        print(f"'{name}' deleted")
    else:
        print(f"Error: '{name}' not found")


def update_movie():
    """Update the rating of an existing movie."""
    name = input("Enter movie name to update: ").strip()
    if not name:
        print("Error: Movie name cannot be empty")
        return

    name_lower = name.lower()
    if name_lower in movies:
        rating = float(input("Enter new rating: "))
        if 0 <= rating <= 10:
            movies[name_lower] = rating
            print(f"'{name}' updated to rating {rating}")
        else:
            print("Error: Rating must be between 0 and 10")
    else:
        print(f"Error: '{name}' not found")


def stats():
    """Display statistics about the movies."""
    if movies:
        ratings = list(movies.values())
        average = round(statistics.mean(ratings), 2)
        median = statistics.median(ratings)
        best = max(movies, key=movies.get)
        worst = min(movies, key=movies.get)
        print(f"Average rating: {average}")
        print(f"Median rating: {median}")
        print(f"Best movie: {best}")
        print(f"Worst movie: {worst}")
    else:
        print("No movies in database")


def random_movie():
    """Display a random movie and its rating."""
    name = random.choice(list(movies.keys()))
    print(f"Random movie: {name}, Rating: {movies[name]}")


def search_movie():
    """Search for movies by a part of their name (case-insensitive)."""
    search_term = input("Enter part of movie name to search: ").lower()
    found_movies = {name: rating for name, rating in movies.items() if search_term in name.lower()}
    if found_movies:
        for name, rating in found_movies.items():
            print(f"{name}: {rating}")
    else:
        print("No matches found")


def movies_sorted_by_rating():
    """Display all movies sorted by rating in descending order"""
    sorted_movies = sorted(movies.items(), key=lambda x: x[1], reverse=True)
    for name, rating in sorted_movies:
        print(f"{name}: {rating}")


def main():
    """Main function to run the movie application."""
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
            print("Bye")
            print()
            break # Exit the loop when '0' is selected
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            movies_sorted_by_rating()
        else:
            print("Invalid choice, please try again!")


if __name__ == "__main__":
    main()