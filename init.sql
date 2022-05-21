CREATE TABLE IF NOT EXISTS movies (
    movie_id serial PRIMARY KEY,
    preference_key INTEGER NOT NULL,
    movie_title VARCHAR NOT NULL,
    rating DOUBLE NOT NULL,
    year INTEGER NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    preference_1 INTEGER NOT NULL,
    preference_2 INTEGER NOT NULL,
    preference_3 INTEGER NOT NULL,
    preference_key INTEGER NOT NULL,
);