#!/usr/bin/python3

from gettext import install
from flask import Flask, render_template
from models import storage
from models import storage_type
from models.city import City
from models.state import State

app = Flask(__name__)

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    states = []
    city_in_state = []

    list_of_objects = list(storage.all(State).values())
    for state in list_of_objects:
        states.append(state.__dict__)
        if storage_type != 'db':
            for city in state.cities:
                city_in_state.append(city.__dict__)

    if storage_type == 'db':
        tables = storage._DBStorage__session.query(City, State).filter(City.state_id == State.id).all()
        for table in tables:
            city_in_state.append(table.City.__dict__)

    return render_template('8-cities_by_states.html', states=states, city_in_state=city_in_state)

@app.template_filter('sort_by_name')
def sort_by_name(arg):
    return sorted(arg, key=lambda x: x['name'])

@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
