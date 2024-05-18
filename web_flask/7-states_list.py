#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def state_list():
    result = []
    list_of_objects = list(storage.all(State).values())
    for lists in list_of_objects:
        result.append(lists.__dict__)
    
    return render_template('7-states_list.html', list_of_dict=result)

@app.template_filter('sort_by_name')
def sort_by_name(list_of_dict):
    return sorted(list_of_dict, key=lambda x: x['name'])

@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
