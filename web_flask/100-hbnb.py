#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask
from flask import Flask, render_template
from models import storage
from models import storage_type
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def find_id():
    states = []
    city_in_state = []
    user_in_place = []
    amenitys = []
    places = []

    list_of_states = list(storage.all(State).values())
    list_of_amenitys = list(storage.all(Amenity).values())
    list_of_place = list(storage.all(Place).values())
    
    for amenity in list_of_amenitys:
        amenitys.append(amenity.__dict__)
    
    if storage_type != 'db':
        for state in list_of_states:
            states.append(state.__dict__)
            for city in state.cities:
                city_in_state.append(city.__dict__)
    
        for place in list_of_place:
            places.append(place.__dict__)
            for user in place.users:
                user_in_place.append(user.__dict__)
    else:
        tables = storage._DBStorage__session.query(City, State).filter(City.state_id == State.id).all()
        user_tables = storage._DBStorage__session.query(Place, User).filter(Place.user_id == User.id).all()
        for table in tables:
            city_in_state.append(table.City.__dict__)
        
        for user_table in user_tables:
            user_in_place.append(user_table.User.__dict__)
    return render_template('100-hbnb.html',
                           states=states,
                           city_in_state=city_in_state,
                           amenitys=amenitys,
                           places=places,
                           user_in_place=user_in_place)

@app.template_filter('sort_by_name')
def sort_by_name(arg):
    return sorted(arg, key=lambda x: x['name'])

@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
