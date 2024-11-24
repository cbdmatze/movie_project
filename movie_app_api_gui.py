import tkinter as tk
from tkinter import Menu
import webbrowser
from movie_app_api import MovieApp
from movie_app_api_gui import MovieGUI
from tkinter_gui import MovieAppTkGui


class MovieGUI:
    def __init__(self, master, storage):
        self.master = master
        self.storage = storage

        # Create the move list frame
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
        # Clear the listbox
        self.movie_listbox.delete(0, tk.END)

        # Load movies from the storage and display them
        movies = self.storage.list_movies()
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie)

    
    def show_context_menu(self, event):
        # Show the right-click menu
        self.menu.post(event.x_root, event.y_root)
    

    def watch_movie(self):
        # Get selected movie and redirect to streaming platform
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)
            streaming_url = f"https://justwatch.com/search?q={movie_title.replace(' ', '+')}"
            webbrowser.open(streaming_url)


    def delete_movie(self):
        # Get selected movie and delete it 
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)
            self.storage.delete_movie(movie_title)
            self.refresh_movie_list()
