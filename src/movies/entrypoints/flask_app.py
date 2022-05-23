from flask import Flask, request, flash, url_for, redirect, render_template
from preferenceKeyGen import PreferenceAlgorithm
from movies import movie_fetcher as MF
from movies.entrypoints.app import Website, users, movies

app = Website.app
db = Website.db

@app.route("/", methods=["GET"])
def home():
    # If the DB is empty, fill it up with IMDB list
    if(len(movies.query.all()) == 0):
        # Retrieve movies from IMDB
        fetcher = MF.IMDBFetcher()
        
        # Upload them to DB
        fetcher.toDatabase(fetcher.fetch())
        
    return render_template("home.html"), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form['username'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        if (len(request.form.getlist('preferences')) != 3):
            flash('Please select 3 categories', 'error')

        if (users.query.filter_by(username=request.form['username']).first() is not None or users.query.filter_by(email=request.form['email']).first() is not None):
            if(users.query.filter_by(username=request.form['username']).first() is not None):
                flash('Username already exists', 'error')
            if(users.query.filter_by(email=request.form['email']).first() is not None):
                flash('Email already exists', 'error')

        else:
            preferencesList = request.form.getlist('preferences')
            preferenceKey = PreferenceAlgorithm.keyGenerator(int(preferencesList[0]), int(
                preferencesList[1]), int(preferencesList[2]))
            user = users(request.form['username'], request.form['email'], int(
                preferencesList[0]), int(preferencesList[1]), int(preferencesList[2]), preferenceKey)
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
            if (request.form.get('sorted')):
                sort = 'asc'
            credentials = users.query.filter_by(username=request.form['username']).first()
            
            return redirect(url_for('movielist', sort=sort, preference=credentials.preference_key))

    return render_template("login.html"), 200


@app.route("/movielist/<preference>/<sort>", methods=["GET"])
def movielist(sort, preference):
    if(sort == 'asc'):
        movie_list = movies.query.filter_by(
            preference_key=preference).order_by(movies.rating.asc()).all()
    else:
        movie_list = movies.query.filter_by(
            preference_key=preference).order_by(movies.rating.desc()).all()

    return render_template("movies.html", movie_list=movie_list), 200
