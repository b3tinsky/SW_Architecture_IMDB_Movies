from abc import ABC, abstractmethod
from flask import Flask, request
from datetime import datetime
import requests
import re
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from movies import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = models.get_postgres_uri()
app.config['SECRET_KEY'] = "B3TINSKY"
models.start_mappers()

db = SQLAlchemy(app)

class movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    preference_key = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    rating = db.Column(db.Float)
    year = db.Column(db.Integer)
    create_time = db.Column(db.TIMESTAMP(timezone=True), index=True)
    
    def __init__(self, preference_key, movie_title, rating, year, create_time):   
        self.preference_key = preference_key
        self.movie_title = movie_title
        self.rating = rating
        self.year = year
        self.create_time = create_time

# S - Single responsibility: Handles fetching the movies
# O - Open/Closed: Can later add fetching for other sites
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