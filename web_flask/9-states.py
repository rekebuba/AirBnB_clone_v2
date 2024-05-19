#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask
from flask import Flask, render_template
from models import storage
from models import storage_type
from models.city import City
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = []

    list_of_states = list(storage.all(State).values())
    for state in list_of_states:
        states.append(state.__dict__)

    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def find_id(id):
    list_of_keys = list(storage.all(State).keys())
    key = 'State.' + id
    if key not in list_of_keys:
        return "<H1>Not found!</H1>"

    city_in_state = []

    list_of_states = list(storage.all(State).values())
    if storage_type != 'db':
        for state in list_of_states:
            for city in state.cities:
                city_in_state.append(city.__dict__)
    else:
        tables = storage._DBStorage__session.query(
            City, State).filter(City.state_id == State.id).all()
        for table in tables:
            city_in_state.append(table.City.__dict__)

    return render_template('9-states.html',
                           city_in_state=city_in_state, id=id)


@app.template_filter('sort_by_name')
def sort_by_name(arg):
    return sorted(arg, key=lambda x: x['name'])


@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
