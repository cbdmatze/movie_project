import requests
import json
from rapidfuzz import fuzz
from storage.istorage import IStorage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class MovieApp:
    def __init__(self, storage:IStorage):
        """Initialize the MovieApp with a storage instance."""
        self._storage = storage
        self.api_key = os.getenv("OMDB_API_KEY")  # Fetch API key from environment

    def _command_list_movies(self):
        """List all movies in the database."""
        movies = self._storage.list_movies()
        if movies:
            print(f"{len(movies)} movies in total\n")
            for movie, details in movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _fetch_movie_from_api(self, title):
        """Fetch movie details from the OMDb API."""
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            movie_data = response.json()

            # Check if movie was found
            if movie_data.get("Response") == "False":
                raise ValueError(f"Movie '{title}' not found in OMDb")
            
            # Extract relevant data
            return {
                "title": movie_data["Title"], 
                "year": int(movie_data["Year"]),
                "rating": float(movie_data["imdbRating"]), 
                "poster_url": movie_data.get("Poster", "")  # Fallback to empty string if poster is not available
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OMDb API: {e}")
        except ValueError as e:
            print(e)
            return None

    def _command_add_movie(self):
        """Add a new movie to the database."""
        name = input("Enter movie name: ").strip()
        if not name:
            print(f"Error: Movie name cannot be empty!")
            return
        if name in self._storage.list_movies():
            print(f"Error: '{name}' already exists!")
            return

        # Fetch movie details from API
        movie_data = self._fetch_movie_from_api(name)
        if not movie_data:
            return

        # Add movie to storage
        self._storage.add_movie(movie_data["title"], movie_data["year"], movie_data["rating"], movie_data["poster_url"])
        print(f"'{movie_data['title']}' added with rating {movie_data['rating']}, year {movie_data['year']}, and poster URL.")

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

    def generate_website(self):
        """Generate an HTML website from the list of movies."""
        movies = self._storage.list_movies()
        try:
            # Load the HTML template
            with open('index_template.html', 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            # Replace the title placeholder
            website_title = "My Movie App"
            template_content = template_content.replace("__TEMPLATE_TITLE__", website_title)

            # Generate the movie grid
            movie_grid_html = ""
            for title, details in movies.items():
                # Safely retrieve poster URL or use a placeholder
                poster_url = details.get('poster_url', 'https://via.placeholder.com/300x450?text=No+Poster')
                year = details.get('year', 'Unknown')  # Safeguard in case 'year' is missing
                movie_grid_html += f'''
                <div class="movie-item">
                    <img src="{poster_url}" alt="{title} Poster">
                    <h3>{title}</h3>
                    <p>{year}</p>
                </div>
                '''

            # Replace the movie grid placeholder in the template
            template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

            # Write the final HTML to a file
            with open('index.html', 'w', encoding='utf-8') as output_file:
                output_file.write(template_content)

            print("Website generated successfully.")

        except FileNotFoundError:
            print("Error: Template file or CSS not found.")


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
            print("6. Movies Sorted by Rating")
            print("9. Generate Website\n")

            choice = input("Enter a choice (0 - 9): ")
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
            elif choice == "9":
                self.generate_website()
            else:
                print("Invalid choice. Please select a valid option from the menu.\n")
