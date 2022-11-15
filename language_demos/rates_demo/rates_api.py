""" rates api """

from flask import Flask, Response

app = Flask(__name__)

@app.route("/") # decorator
def hello_world() -> Response:
    """ hello world """
    return "<b>Hello, World!</b>"

@app.route("/goodnight")
def goodnight_world() -> Response:
    """ hello world """
    return "<b>Good Night, World!</b>"


app.run(port=5050)
