# python-projects

1. IMDb Movie Scraper
A simple Python script using requests and BeautifulSoup to fetch movies, extract their IMDb ratings, and display the movies above a user-defined rating threshold.

Features
1. Scrapes the IMDb Most Popular Movies page
2. Extracts movie titles and IMDb ratings
3. Prints a sorted list of movies with ratings greater than or equal to a specified value

Requirements
1. Python 3.x
2. requests
3. beautifulsoup4

Install requirements with:
pip install requests beautifulsoup4

Usage
1. Clone or download this repository.
2. Run the script:
python imdb_scraper.py

3. You will be prompted to enter a minimum rating (for example, 7.5).
4. The script outputs all movies from the current IMDb "Most Popular Movies" chart with a rating equal to or above your threshold.

Example
Enter the minimum rating (e.g., 7.5): 7
Movie Name: Inception, Rating: 8.8
Movie Name: Interstellar, Rating: 8.6
...

Code Structure
1. fetch_movies(url, headers) — Downloads the HTML content from IMDb.
2. extract_movie_data(soup) — Parses the HTML to extract movie titles and ratings.
3. print_sorted_movies(movies, min_rating) — Sorts and displays movies by rating.
4. if __name__ == "__main__" — Runs the script, asks the user for input, and displays results.

Notes
1. IMDb can change its site structure, which may require you to update the HTML parsing code in extract_movie_data.
2. Please do not overuse the script as frequent scraping can violate IMDb's terms of use and may get your IP blocked.
3. This script is for learning and personal use.