#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """display a HTML page with the states listed in alphabetical order"""
    result = []
    list_of_states = list(storage.all("State").values())

    for lists in list_of_states:
        result.append(lists.__dict__)

    return render_template('7-states_list.html', list_of_dict=result)


@app.template_filter('sort_by_name')
def sort_by_name(list_of_dict):
    """helper function to sort the list"""
    return sorted(list_of_dict, key=lambda x: x['name'])


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
