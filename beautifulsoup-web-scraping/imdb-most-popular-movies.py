import requests
from bs4 import BeautifulSoup

def fetch_movies(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def extract_movie_data(soup):
    movie_data = []
    movie_names = soup.find_all('h3', class_='ipc-title__text')
    movie_ratings = soup.find_all('span', class_='ipc-rating-star--rating') 

    for name, rating in zip(movie_names, movie_ratings):
        movie_name = name.text.strip()
        movie_rating_str = rating.text.split()[0]
        
        try:
            movie_rating = float(movie_rating_str)
            movie_data.append((movie_name, movie_rating))
        except ValueError:
            print(f"Could not convert rating '{movie_rating_str}' for movie '{movie_name}' to a float.")
    
    return movie_data

def print_sorted_movies(movies, min_rating):
    sorted_movies = sorted(movies, key=lambda x: x[1], reverse=False)
    for movie in sorted_movies:
        if movie[1] >= min_rating:
            print(f"Movie Name: {movie[0]}, Rating: {movie[1]}")

if __name__ == "__main__":       
    url = "https://www.imdb.com/chart/moviemeter"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    soup = fetch_movies(url, headers)
    movies = extract_movie_data(soup)
    min_rating = float(input("Enter the minimum rating (e.g., 7.5): "))
    print_sorted_movies(movies, min_rating)