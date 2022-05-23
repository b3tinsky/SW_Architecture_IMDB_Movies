from abc import ABC, abstractmethod
from datetime import datetime
import requests
import re
import csv
from bs4 import BeautifulSoup
from movies.entrypoints.app import Website, movies

app = Website.app
db = Website.db

# S - Single responsibility: Handles fetching the movies
# O - Open/Closed: Can later add fetching for other sites
# I - Interface Segregation: Specific to the source used to fetch

class Fetcher(ABC):
    @abstractmethod
    def fetch():
        pass
    
    @abstractmethod
    def toDatabase():
        pass
    
    @abstractmethod
    def toCSV():
        pass

class IMDBFetcher(Fetcher):
    def fetch(self):
        # Downloading imdb top 250 movie's data
        url = 'http://www.imdb.com/chart/top'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Separating response components
        moviesSoup = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

        movieList = []
        for index in range(0, len(moviesSoup)):

            # Separating movie into: 'place','title', 'year'
            movie_string = moviesSoup[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index)) + 1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index)) - (len(movie))]

            data = {"movie_title": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index],
                    "preference_key": index % 4 + 1}
            movieList.append(data)

        return movieList

    def toDatabase(self, movieList):
        for movie in movieList:
            movieObj = movies(movie['preference_key'], movie['movie_title'], movie['rating'], movie['year'], datetime.now())
            db.session.add(movieObj)
            db.session.commit()

    def toCSV(self, movieList):
        fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]
        with open("movie_results.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for movie in movieList:
                writer.writerow({**movie})