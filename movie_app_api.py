import os
import requests
from rapidfuzz import fuzz
from storage.istorage import IStorage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MovieApp:
    def __init__(self, storage: IStorage):
        """Initialize the MovieApp with a storage instance."""
        self._storage = storage
        self.api_key = os.getenv("OMDB_API_KEY")  # Fetch API key from environment

    def _fetch_movie_from_api(self, title):
        """
        Fetch movie details from the OMDb API.
        
        Args:
            title (str): The title of the movie to search for.
            
        Returns:
            dict: A dictionary containing movie details such as title, year, rating, and poster URL.
        """
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            movie_data = response.json()

            if movie_data.get("Response") == "False":
                raise ValueError(f"Movie '{title}' not found in OMDb")

            imdb_rating = movie_data["imdbRating"]
            rating = float(imdb_rating) if imdb_rating != "N/A" else 0.0

            return {
                "title": movie_data["Title"],
                "year": int(movie_data["Year"]),
                "rating": rating,
                "poster_url": movie_data.get("Poster", ""),
            }
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error: {e}")
            return None

    def add_movie(self, movie_title):
        """
        Add a new movie to the database.
        
        Args:
            movie_title (str): The title of the movie to add.
            
        Checks if the movie already exists in the storage and if not, fetches the movie
        from the OMDb API, then stores the movie in the database.
        """
        if not movie_title:
            print("Error: Movie name cannot be empty!")
            return

        # Check if movie already exists
        if movie_title in self._storage.list_movies():
            print(f"Error: '{movie_title}' already exists!")
            return

        movie_data = self._fetch_movie_from_api(movie_title)
        if not movie_data:
            return

        self._storage.add_movie(movie_data["title"], movie_data["year"], movie_data["rating"], movie_data["poster_url"])
        print(f"'{movie_data['title']}' added with rating {movie_data['rating']}, year {movie_data['year']}.")

        # Update website after movie is added
        self._update_website_after_change()

    def delete_movie(self, movie_title):
        """
        Delete a movie from the database after confirming with the user.
        
        Args:
            movie_title (str): The title of the movie to delete.
        
        Uses fuzzy matching to search for movies with a similar title, then asks for user confirmation
        before deleting the movie.
        """
        if not movie_title:
            print("Error: Movie name cannot be empty")
            return

        movies = self._storage.list_movies()
        found_movies = {
            movie: details
            for movie, details in movies.items()
            if fuzz.partial_ratio(movie_title.lower(), movie.lower()) > 80
        }

        if found_movies:
            print("Found the following movie(s) to delete:")
            for movie in found_movies:
                print(f"{movie}: {found_movies[movie]['rating']} ({found_movies[movie]['year']})")

            confirm = input(f"Are you sure you want to delete '{list(found_movies.keys())[0]}'? (y/n): ").lower()
            if confirm == "y":
                self._storage.delete_movie(list(found_movies.keys())[0])
                print(f"'{list(found_movies.keys())[0]}' deleted")

                # Update website after movie is deleted
                self._update_website_after_change()
        else:
            print("No matches found.")

    def _update_website_after_change(self):
        """
        Helper method to generate the website after adding or deleting a movie.
        
        This method regenerates the website using the current list of movies after an update.
        """
        user_name = os.path.splitext(os.path.basename(self._storage.file_path))[0]
        html_filename = f"{user_name}_index.html"
        self.generate_website(html_filename)
        print("Website updated automatically.")

    def generate_website(self, output_file):
        """
        Generate an HTML website from the list of movies in the database.
        
        Args:
            output_file (str): The name of the file to save the generated HTML.
            
        The method reads a template file, generates the HTML structure with the movie details, 
        and writes the result to the output file.
        """
        movies = self._storage.list_movies()
        try:
            current_dir = os.path.dirname(__file__)
            template_path = os.path.join(current_dir, "templates", "index_template.html")

            with open(template_path, "r", encoding="utf-8") as template_file:
                template_content = template_file.read()

            website_title = "My Movie App"
            template_content = template_content.replace("__TEMPLATE_TITLE__", website_title)

            movie_grid_html = ""
            for title, details in movies.items():
                poster_url = details.get("poster_url", "https://via.placeholder.com/300x450?text=No+Poster")
                year = details.get("year", "Unknown")
                movie_grid_html += f"""
                <div class="movie-item">
                    <img src="{poster_url}" alt="{title} Poster">
                    <h3>{title}</h3>
                    <p>{year}</p>
                </div>
                """

            template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

            output_path = os.path.join(current_dir, output_file)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(template_content)

            print(f"Website generated successfully: {output_file}")

        except FileNotFoundError:
            print("Error: Template file or CSS not found.")

    def run(self):
        """
        Run the movie app manu, providing options to the user.
        
        The method continuously displays a menu to the user and handles their choice
        to list movies, add or delete movies, view movie stats, search for movies, or generate the website.
        """
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
                movie_title = input("Enter movie title to add: ").strip()
                self.add_movie(movie_title)
            elif choice == "3":
                movie_title = input("Enter movie title to delete: ").strip()
                self.delete_movie(movie_title)
            elif choice == "4":
                self._command_movie_stats()
            elif choice == "5":
                self._command_search_movie()
            elif choice == "6":
                self._command_movies_sorted_by_rating()
            elif choice == "9":
                user_name = os.path.splitext(os.path.basename(self._storage.file_path))[0]
                html_filename = f"{user_name}_index.html"
                self.generate_website(html_filename)
            else:
                print("Invalid choice. Please select a valid option from the menu.\n")

    def _command_list_movies(self):
        """
        List all movies in the database with their ratings and years.
        """
        movies = self._storage.list_movies()
        if movies:
            print(f"{len(movies)} movies in total\n")
            for movie, details in movies.items():
                print(f"{movie}: {details['rating']} ({details['year']})")
        else:
            print("No movies found.")

    def _command_movie_stats(self):
        """
        Display statistics about the movies in the database, such as the average rating,
        best movie, and worst movie.
        """
        movies = self._storage.list_movies()
        if movies:
            ratings = [details["rating"] for details in movies.values()]
            average = round(sum(ratings) / len(ratings), 2)

            best_movie = max(movies, key=lambda x: movies[x]["rating"])
            worst_movie = min(movies, key=lambda x: movies[x]["rating"])

            print(f"Average rating: {average}")
            print(f"Best movie: {best_movie} (Rating: {movies[best_movie]['rating']})")
            print(f"Worst movie: {worst_movie} (Rating: {movies[worst_movie]['rating']})")
        else:
            print("No movies in the database.")
    
    def _command_search_movie(self):
        """
        Search for movies by part of their name using fuzzy matching .
        
        The search term is case-insensitive, and movies with a fuzzy match above 80%
        will be displayed with their rating and year.
        """
        search_term = input("Enter part of the movie name to search: ").lower()
        found_movies = {
            name: details
            for name, details in self._storage.list_movies().items()
            if fuzz.partial_ratio(search_term, name.lower()) > 80
        }

        if found_movies:
            for name, details in found_movies.items():
                print(f"{name}: {details['rating']} ({details['year']})")
        else:
            print("No matches found.")

    def _command_movies_sorted_by_rating(self):
        """
        Display all movies sorted by rating in descending order.
        """
        sorted_movies = sorted(
            self._storage.list_movies().items(), key=lambda x: x[1]["rating"], reverse=True
        )
        for name, details in sorted_movies:
            print(f"{name}: {details['rating']} ({details['year']})")
