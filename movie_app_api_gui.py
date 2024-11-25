import tkinter as tk
from tkinter import Menu
import webbrowser
from movie_app_api import MovieApp


class MovieGUI:
    """
    The GUI class that handles displaying movies, interacting with the
    movie storage, and providing user functionality like watching and deleting movies.
    """
    def __init__(self, master, storage):
        """
        Initialize the Movie GUI with the given master (Tkinter window)
        and movie storage.
        """
        self.master = master
        self.storage = storage

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
        """
        self.movie_listbox.delete(0, tk.END)
        movies = self.storage.list_movies()
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie)

    def show_context_menu(self, event):
        """
        Show the right-click menu for the movie listbox.
        """
        self.menu.post(event.x_root, event.y_root)

    def watch_movie(self):
        """
        Get the selected movie and open the streaming URL in the browser.
        """
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)
            streaming_url = f"https://justwatch.com/search?q={movie_title.replace(' ', '+')}"
            webbrowser.open(streaming_url)

    def delete_movie(self):
        """
        Delete the selected movie from the storage and refresh the list.
        """
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)
            self.storage.delete_movie(movie_title)
            self.refresh_movie_list()
