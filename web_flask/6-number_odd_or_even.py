#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def great():
    """display Hello HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def great_2():
    """greate HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def great_3(text):
    """greate with the input text"""
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def great_4(text="is cool"):
    """greate with python {input text}"""
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def great_5(n):
    """check if the input is a number"""
    if isinstance(n, int):
        return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def great_6(n):
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def great_7(n):
    """check if the number is even or odd"""
    if isinstance(n, int):
        return render_template('6-number_odd_or_even.html', n=n)


@app.template_filter('even_odd')
def even_odd(num):
    """helper function"""
    value = "even" if num % 2 == 0 else "odd"
    return value


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
