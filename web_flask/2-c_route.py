#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def great():
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def great_2():
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def great_3(text):
    text = text.replace('_', ' ')
    return f"C {text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
