#!/usr/bin/python3
"""
starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /: display “Hello HBNB!”
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return ('Hello HBNB!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
