import tkinter as tk
from tkinter import Menu
import webbrowser
from movie_app_api import MovieApp
import logging  # Import logging


class MovieGUI:
    """
    The GUI class that handles displaying movies, interacting with the
    movie storage, and providing user functionality like watching and deleting movies.
    """
    def __init__(self, master, storage):
        """
        Initialize the Movie GUI with the given master (Tkinter window)
        and movie storage.
        
        Args:
            master (tk.Tk): The main Tkinter window instance.
            storage (Istorage): The movie storage instance (could be CSV or JSON backend).
        """
        self.master = master
        self.storage = storage

        # Set up logging
        logging.basicConfig(filename="movie_app.log", level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info("MovieGUI initialized.")

        # Create the movie list frame
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.movie_listbox = tk.Listbox(self.frame)
        self.movie_listbox.pack()

        # Right-click context menu
        self.menu = Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Watch", command=self.watch_movie)
        self.menu.add_command(label="Delete", command=self.delete_movie)

        # Bind the right-click event
        self.movie_listbox.bind("<Button-3>", self.show_context_menu)

        # Load and display the movies
        self.refresh_movie_list()

    def refresh_movie_list(self):
        """
        Refresh the listbox with the movie titles from the storage.
        
        This method retrieves the movie data from the storage and updates
        the Listbox widget with the latest movie titles.
        """
        self.movie_listbox.delete(0, tk.END)  # Clear current list
        movies = self.storage.list_movies()  # Fetch movie data from the storage
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie)  # Insert movies into the listbox

        logging.info("Movie list refreshed.")

    def show_context_menu(self, event):
        """
        Show the right-click menu for the movie listbox.
        
        Args:
            event (tk.Event): The event triggered by the right-click.
            
        This method positions and displays the context menu at the location
        of the right-click event within the listbox.
        """
        self.menu.post(event.x_root, event.y_root)

    def watch_movie(self):
        """
        Get the selected movie and open the streaming URL in the browser.
        
        The method retrieves the movie title selected in the listbox and constructs
        a streaming URL based on the title, then opens it in the default web browser.
        """
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)  # Get movie title
            # Construct the streaming URL for JustWatch
            streaming_url = f"https://justwatch.com/search?q={movie_title.replace(' ', '+')}"
            webbrowser.open(streaming_url)  # Open the URL in the browser
            logging.info(f"Movie '{movie_title}' watched via streaming.")

    def delete_movie(self):
        """
        Delete the selected movie from the storage and refresh the list.
        
        The method removes the selected movie from the storage and updates
        the Listbox to reflect the deletion by calling the 'refresh_movie_list()' method.
        """
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)  # Get the movie title
            self.storage.delete_movie(movie_title)  # Delete the movie from storage
            self.refresh_movie_list()  # Refresh the list to reflect changes
            logging.info(f"Movie '{movie_title}' deleted.")
