from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template
from movies import models

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Website(metaclass=Singleton):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = models.get_postgres_uri()
    app.config['SECRET_KEY'] = "B3TINSKY"
    models.start_mappers()

    db = SQLAlchemy(app)

class users(Website.db.Model):
    user_id = Website.db.Column(Website.db.Integer, primary_key=True)
    username = Website.db.Column(Website.db.String)
    email = Website.db.Column(Website.db.String)
    preference_1 = Website.db.Column(Website.db.Integer)
    preference_2 = Website.db.Column(Website.db.Integer)
    preference_3 = Website.db.Column(Website.db.Integer)
    preference_key = Website.db.Column(Website.db.Integer)

    def __init__(self, username, email, preference_1, preference_2, preference_3, preference_key):
        self.username = username
        self.email = email
        self.preference_1 = preference_1
        self.preference_2 = preference_2
        self.preference_3 = preference_3
        self.preference_key = preference_key

class movies(Website.db.Model):
    movie_id = Website.db.Column(Website.db.Integer, primary_key=True)
    preference_key = Website.db.Column(Website.db.Integer)
    movie_title = Website.db.Column(Website.db.String)
    rating = Website.db.Column(Website.db.Float)
    year = Website.db.Column(Website.db.Integer)
    create_time = Website.db.Column(Website.db.TIMESTAMP(timezone=True), index=True)

    def __init__(self, preference_key, movie_title, rating, year, create_time):
        self.preference_key = preference_key
        self.movie_title = movie_title
        self.rating = rating
        self.year = year
        self.create_time = create_time