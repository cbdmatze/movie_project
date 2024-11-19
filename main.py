from movie_app_api import MovieApp
from storage_json_api import StorageJson
from storage_csv_api import StorageCsv
from istorage import IStorage

def main():
    """Main function to run the movie database application."""
    storage = StorageJson('movies.json')  # Create a StorageJson object
    app = MovieApp(storage)  # Create a MovieApp object
    app.run()  # Run the movie app

if __name__ == "__main__":
    main()
