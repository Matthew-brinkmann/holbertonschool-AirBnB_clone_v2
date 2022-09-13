#!/usr/bin/python3
"""
starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the text variable
        (replace underscore _ symbols with a space )
    /python/(<text>): display “Python ” followed by value of the text variable
        (replace underscore _ symbols with a space )
        The default value of text is “is cool”
    /number/<n>: display “n is a number” only if n is an integer
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return ('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns HBNB"""
    return ('HBNB')


@app.route('/c/<text>', strict_slashes=False)
def cPath(text):
    """returns “C ” followed by the value of the text variable"""
    return ('C ' + text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythonPath(text='is_cool'):
    """return “Python ”, followed by the value of the text variable
    default value is cool."""
    return ('Python ' + text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def numberPath(n):
    """display “n is a number” only if n is an integer"""
    return "{:d} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
