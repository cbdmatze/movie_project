
Movie Database CLI Application

A Python-based command-line interface (CLI) application to manage a personal movie database. This application allows users to add, update, delete, list, and search for movies with fuzzy matching. It also displays statistics about the movie collection, such as the best-rated and worst-rated movies.

The application uses persistent data storage via a JSON file, ensuring that your movie collection is saved between sessions. The file operations are modularized in a separate movie_storage module for better maintainability and separation of concerns.

Features

	•	List Movies: Displays all movies in the collection with their ratings and release years.
	•	Add a Movie: Add a new movie to the collection with a rating (0-10) and release year.
	•	Delete a Movie: Remove a movie from the collection.
	•	Update Movie Rating: Update the rating of an existing movie.
	•	Search Movies: Search for movies by part of their name using fuzzy matching.
	•	Random Movie: Display a randomly selected movie from the collection.
	•	Statistics: Show statistics like the average movie rating, best-rated, and worst-rated movies.
	•	Sort Movies by Rating: Display all movies sorted by their ratings in descending order.
	•	Persistent Storage: The movie collection is stored in a JSON file and reloaded in every session.

Project Structure

movie_database_project/
│
├── movie.py              # Main application logic (MovieDatabase class and user interaction)
├── movie_storage.py      # Handles persistent storage (JSON file read/write operations)
├── data.json             # Stores the movie data in JSON format (created automatically)
├── README.md             # Project documentation
└── requirements.txt      # Project dependencies

Installation

	1.	Clone the repository:

git clone https://github.com/yourusername/movie-database-cli.git
cd movie-database-cli


	2.	Create a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


	3.	Install dependencies:
The project relies on a few external libraries like rapidfuzz for fuzzy matching and json for data handling.
Install them by running:

pip install -r requirements.txt


	4.	Run the application:

python movie.py



Usage

Once the application is running, you’ll be presented with a menu of options. Each option is explained below:

	1.	List Movies: Shows all movies stored in the database with their ratings and release years.
	2.	Add Movie: Prompts you to input the name, rating, and release year of a new movie.
	3.	Delete Movie: Allows you to remove a movie by its name.
	4.	Update Movie: Updates the rating of a movie.
	5.	Stats: Displays the average movie rating, the highest-rated movie, and the lowest-rated movie.
	6.	Random Movie: Shows a randomly selected movie from your collection.
	7.	Search Movie: Search for a movie by part of its name (case-insensitive) using fuzzy matching.
	8.	Movies Sorted by Rating: Lists all movies sorted by rating, from highest to lowest.

You can exit the program by selecting option 0.

Example

Here’s what a typical session might look like:

********** My Movies Database **********

Menu:

0. Exit
1. List movies
2. Add Movie
3. Delete Movie
4. Update Movie
5. Stats
6. Random Movie
7. Search Movie
8. Movies sorted by rating

Enter a choice (0 - 8): 2

Enter movie name: The Matrix
Enter movie rating (0-10): 9.0
Enter movie release year: 1999
'The Matrix' added with rating 9.0 and year 1999

Data Persistence

All movie data is stored in a JSON file (data.json), which will be created automatically when you add a movie for the first time. This file allows the program to maintain your movie list between sessions.

You can manually inspect the data.json file to see the structure of your stored data, which looks like this:

{
    "The Matrix": {
        "year": 1999,
        "rating": 9.0
    },
    "Inception": {
        "year": 2010,
        "rating": 8.8
    }
}

Dependencies

	•	Python 3.x
	•	rapidfuzz: For fuzzy matching during movie searches.

To install the required dependencies, run:

pip install -r requirements.txt

Contents of requirements.txt:

rapidfuzz==2.13.7

Future Enhancements

Potential improvements for this project include:

	•	Add more advanced search filters (e.g., by rating, release year, or genre).
	•	Support for handling duplicate movie names.
	•	Improve the user interface for more intuitive navigation.
	•	Add functionality to export the movie list to other formats (CSV, PDF).
	•	Include the ability to rate movies by different categories (acting, storyline, visual effects, etc.).

License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this software as per the terms of the license.

Contributions

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit issues.

Author

	•	Matthias Will (www.github.com/cbdmatze)
