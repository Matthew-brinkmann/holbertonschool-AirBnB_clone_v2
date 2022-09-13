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
Honestly, does more... can't be bothered keeping up.
Now handles amenities... but not gonna explain how
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


@app.route('/hbnb_filters', strict_slashes=False)
def fullyWorkingFilters():
    """display a HTML page like 6-index.html from web-static"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
