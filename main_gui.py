import argparse
import os
import tkinter as tk
from tkinter_gui import MovieAppTkGui  # Import the Tkinter GUI class
from storage.storage_json_api import StorageJson
from storage.storage_csv_api import StorageCsv
from movie_app_api import MovieApp  # Import the backend movie logic


def main():
    """
    The main function to run the Movie App. It accepts a command-line argument
    that specifies the path to the storage file (JSON or CSV). Based on the 
    file extension, it selects the appropriate storage type and initializes
    the MovieApp with that storage. Additionally, it generates a user-specific
    HTML file to display their movie list.

    Usage:
        python3 main_gui.py <storage_file>
    
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

    # Check the file extension and select the appropriate storage type
    file_extension = os.path.splitext(storage_file)[-1].lower()

    if file_extension == ".json":
        storage = StorageJson(storage_file)
    elif file_extension == ".csv":
        storage = StorageCsv(storage_file)
    else:
        print(f"Error: Unsupported file extension '{file_extension}'. Only .json and .csv are supported.")
        return

    # Initialize the MovieApp backend with the appropriate storage
    movie_app = MovieApp(storage)

    # Create the main application window for Tkinter
    root = tk.Tk()
    root.title("My Movie App")

    # Initialize the Tkinter-based GUI and pass the MovieApp backend to it
    MovieAppTkGui.run_gui(movie_app)

    # Generate the website after the Tkinter main loop ends (if necessary)
    user_name = os.path.splitext(os.path.basename(storage_file))[0]
    html_filename = f"{user_name}_index.html"
    movie_app.generate_website(html_filename)


if __name__ == "__main__":
    main()
