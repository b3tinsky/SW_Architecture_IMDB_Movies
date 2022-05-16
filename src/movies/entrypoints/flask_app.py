from flask import Flask, request
from movies import models

app = Flask(__name__)
models.start_mappers()


@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello World!", 200

@app.route("/testdict", methods=["GET"])
def test_list():
    test = {"one":1, "two":2, "three":3}
    return test, 200