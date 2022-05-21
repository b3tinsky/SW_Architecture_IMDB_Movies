from flask import Flask, request, flash, url_for, redirect, render_template
from movies import models
from preferenceKeyGen import preference_key_gen as PFGenerator
from movies import movie_fetcher
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = models.get_postgres_uri()
app.config['SECRET_KEY'] = "B3TINSKY"
models.start_mappers()

db = SQLAlchemy(app)

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    preference_1 = db.Column(db.Integer)
    preference_2 = db.Column(db.Integer)
    preference_3 = db.Column(db.Integer)
    preference_key = db.Column(db.Integer)

    def __init__(self, username, email, preference_1, preference_2, preference_3, preference_key):   
        self.username = username
        self.email = email
        self.preference_1 = preference_1
        self.preference_2 = preference_2
        self.preference_3 = preference_3
        self.preference_key = preference_key

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

@app.route("/", methods=["GET"])
def home():
    if(len(movies.query.all()) == 0):
        movie_fetcher.main()
    return render_template("home.html"), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form['username'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        if (len(request.form.getlist('preferences')) != 3):
            flash('Please select 3 categories', 'error')
        
        elif ( users.query.filter_by(username=request.form['username']).first() is not None or users.query.filter_by(email=request.form['email']).first() is not None ):
            if(users.query.filter_by(username=request.form['username']).first() is not None):
                flash('Username already exists', 'error')
            if(users.query.filter_by(email=request.form['email']).first() is not None):
                flash('Email already exists', 'error')

        else:
            preferencesList = request.form.getlist('preferences')
            preferenceKey = PFGenerator(int(preferencesList[0]), int(preferencesList[1]), int(preferencesList[2]))
            user = users(request.form['username'], request.form['email'], int(preferencesList[0]), int(preferencesList[1]), int(preferencesList[2]), preferenceKey)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("register.html"), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form['username'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        
        elif(users.query.filter_by(username=request.form['username']).first() != users.query.filter_by(email=request.form['email']).first()):
            flash('Invalid credentials', 'info')
            
        else:
            sort = 'desc'
            if (request.form.get('sorted')): sort = 'asc' 
            return redirect(url_for('movielist', sort = sort))


    return render_template("login.html"), 200


@app.route("/movielist/<sort>", methods=["GET"])
def movielist(sort):
    if(sort=='asc'):
        movie_list = movies.query.filter_by(preference_key=1).order_by(movies.rating.asc()).all()
    else:
        movie_list = movies.query.filter_by(preference_key=1).order_by(movies.rating.desc()).all()


    return render_template("movies.html", movie_list=movie_list), 200
