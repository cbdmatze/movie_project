from previous_versions.storage_json import StorageJson
from previous_versions.movie_app import MovieApp

def main():
    """Main function to run the movie database application."""
    storage = StorageJson('movies.json')  # Create a StorageJson object
    app = MovieApp(storage)  # Create a MovieApp object
    app.run()  # Run the movie app

if __name__ == "__main__":
    main()
