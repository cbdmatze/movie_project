import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
import webbrowser
from movie_app_api import MovieApp


class MovieAppTkGui:
    """
    The Tkinter GUI class for the Movie App. It integrates with the MovieApp
    and provides a user interface for managing and viewing movies.
    """
    def __init__(self, root, movie_app):
        """Initialize the Tkinter GUI and integrate with the MovieApp."""
        self.root = root
        self.movie_app = movie_app

        # Set window title and dimensions
        self.root.title("Movie App")
        self.root.geometry("600x400")

        # Create and pack the listbox to display movies
        self.movie_listbox = tk.Listbox(self.root, height=15, width=50)
        self.movie_listbox.pack(pady=20)

        # Create a context menu (right-click menu)
        self.create_context_menu()

        # Populate the listbox with movies from the database
        self.populate_movie_list()

        # Bind right-click event for the context menu (Windows/Linux: Button-3, macOS: Button-2)
        self.movie_listbox.bind("<Button-3>", self.show_context_menu)
        self.movie_listbox.bind("<Button-2>", self.show_context_menu)  # For macOS right-click

        # Bind double-click event to open a movie in the browser
        self.movie_listbox.bind("<Double-1>", self.watch_movie)

    def create_context_menu(self):
        """
        Create the right-click context menu.
        """
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Add Movie", command=self.add_movie)
        self.context_menu.add_command(label="Delete Movie", command=self.delete_movie)
        self.context_menu.add_command(label="Show Stats", command=self.show_stats)
        self.context_menu.add_command(label="Search Movie", command=self.search_movie)
        self.context_menu.add_command(label="Update Website", command=self.generate_website)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Exit", command=self.root.quit)

    def show_context_menu(self, event):
        """
        Show the context menu on right-click.
        """
        print("Right-click detected")  # Debugging statement
        try:
            # Using 'post' instead of 'tk_popup' to ensure cross-platform compatibility
            self.context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error showing context menu: {e}")

    def populate_movie_list(self):
        """
        Populate the listbox with movie titles from the database.
        """
        self.movie_listbox.delete(0, tk.END)
        movies = self.movie_app.get_movie_list()
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie)

    def add_movie(self):
        """
        Add a new movie to the database and update the list.
        """
        new_movie = simpledialog.askstring("Add Movie", "Enter movie name:")
        if new_movie:
            success = self.movie_app.add_movie(new_movie)
            if success:
                self.populate_movie_list()
            else:
                messagebox.showerror("Error", "Movie could not be added.")

    def delete_movie(self):
        """
        Delete a selected movie from the database and update the list.
        """
        selected_movie = self.movie_listbox.get(tk.ACTIVE)
        if selected_movie:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_movie}'?")
            if confirm:
                self.movie_app.delete_movie(selected_movie)
                self.populate_movie_list()

    def show_stats(self):
        """
        Display movie statistics in a message box.
        """
        stats = self.movie_app.get_movie_stats()
        messagebox.showinfo("Movie Stats", stats)

    def search_movie(self):
        """
        Search for a movie and display the results.
        """
        search_term = simpledialog.askstring("Search Movie", "Enter movie name:")
        if search_term:
            results = self.movie_app.search_movie(search_term)
            if results:
                result_str = "\n".join(results)
                messagebox.showinfo("Search Results", result_str)
            else:
                messagebox.showinfo("Search Results", "No movies found")

    def generate_website(self):
        """
        Generate the movie website.
        """
        self.movie_app.generate_website()
        messagebox.showinfo("Website Generated", "The movie website has been updated.")

    def watch_movie(self, event):
        """
        Handle double-click on a movie to watch it.
        """
        print("Double-click detected")  # Debugging statement
        selected = self.movie_listbox.curselection()
        if selected:
            movie_title = self.movie_listbox.get(selected)
            if movie_title:
                # Prepare the 123MoviesFree URL (ensure it’s correctly formatted)
                streaming_url = f"https://ww4.123moviesfree.net/search/?q={movie_title.replace(' ', '+')}"
                print(f"Redirecting to: {streaming_url}")  # Debugging: see URL before opening
                webbrowser.open(streaming_url)

    @staticmethod
    def run_gui(movie_app):
        """
        Run the Tkinter-based Movie App GUI.
        """
        root = tk.Tk()
        app_gui = MovieAppTkGui(root, movie_app)
        root.mainloop()
