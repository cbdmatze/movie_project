import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from tkinter_gui import MovieAppTkGui  # Import the Tkinter GUI class
from storage.storage_json_api import StorageJson
from storage.storage_csv_api import StorageCsv
from movie_app_api import MovieApp  # Import the backend movie logic


class MainApp:
    def __init__(self):
        """Initialize the main app with Tkinter root."""
        self.root = tk.Tk()
        self.root.title("Movie App GUI")
        self.movie_app = None

    def open_file(self):
        """Open a file dialog to select JSON/CSV file and start the movie app."""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")]
        )
        if file_path:
            self.start_movie_app(file_path)

    def start_movie_app(self, file_path):
        """Start the movie app with the selected file (JSON/CSV)."""
        # Determine the correct storage type based on the file extension
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".json":
            storage = StorageJson(file_path)
        elif file_extension == ".csv":
            storage = StorageCsv(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format! Only .json or .csv files are allowed.")
            return

        # Initialize the backend logic with the selected storage
        movie_app = MovieApp(storage)

        # Start the Tkinter-based GUI
        MovieAppTkGui.run_gui(movie_app)

    def run(self):
        """Run the main application."""
        tk.Button(self.root, text="Open File", command=self.open_file).pack(pady=20)
        self.root.mainloop()


def main():
    """Main function to handle CLI arguments and launch the GUI if needed."""
    parser = argparse.ArgumentParser(description="Movie App GUI")
    parser.add_argument(
        '--file', 
        type=str, 
        help="Path to the movie data file (JSON/CSV)"
    )
    args = parser.parse_args()

    if args.file:
        # If a file path is provided via the command line, start the movie app with that file
        file_path = args.file
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".json":
            storage = StorageJson(file_path)
        elif file_extension == ".csv":
            storage = StorageCsv(file_path)
        else:
            print("Error: Unsupported file format! Only .json or .csv files are allowed.")
            return

        movie_app = MovieApp(storage)
        MovieAppTkGui.run_gui(movie_app)
    else:
        # No file path provided, launch the GUI to let the user select a file
        app = MainApp()
        app.run()


if __name__ == "__main__":
    main()
