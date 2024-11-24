import argparse
import os
from storage.storage_json_api import StorageJson
from storage.storage_csv_api import StorageCsv
from movie_app_api import MovieApp


def main():
    """
    The main function to run the Movie App. It accepts a command-line argument
    that specifies the path to the storage file (JSON or CSV): Based on the 
    file extension, it selects the appropriate storage type and initializes
    the MovieApp with that storage. Additionaly it generates a user-specific
    HTML file to display their movie list.
    
    Usage:
        python3 main.py <stora_file>
        
    Arguments:
        storage_file: Path to the storage file, e.g., john.json or ashley.csv.
        
    Returns:
        None
    """
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Run the Movie App with a specified storage file.")
    parser.add_argument("storage_file", help="Path to the storage file (e.g., john.json or ashley.csv)")

    # Parse the arguments
    args = parser.parse_args()
    storage_file = args.storage_file

    # Check the file extension and select the appropriate storyge type
    file_extension = os.path.splitext(storage_file)[-1].lower()

    if file_extension == ".json":
        storage = StorageJson(storage_file)
    elif file_extension == ".csv":
        storage = StorageCsv(storage_file)
    else:
        print(F"Error: Unsupported fle extension '{file_extension}'. Only .json and .csv are supported.")
        return
    
    # Extract the filename without the extension for dynamic HTML file naming
    user_name = os.path.splitext(os.path.basename(storage_file))[0]

    # Start the MovieApp
    app = MovieApp(storage)
    
    # Generate user-specific website (e.g., matthias_index.html or martina_index.heml)
    html_filename = f"{user_name}_index.html"
    app.generate_website(html_filename)

    # Run the MovieApp
    app.run()

if __name__ == "__main__":
    main()
