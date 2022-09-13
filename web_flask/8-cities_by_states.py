#!/usr/bin/python3
"""
starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /states_list: display a HTML page: (inside the tag BODY)
        H1 tag: “States”
        UL tag: with the list of all State objects
            present in DBStorage sorted by name (A->Z) tip
        LI tag: description of one
            State: <state.id>: <B><state.name></B>
        LI tag: description of one
            City: <city.id>: <B><city.name></B>
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown;
    remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def citiesByState(n=None):
    """checking input data using templating"""
    return render_template('8-cities_by_states.html',
                           states=storage.all("State"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
