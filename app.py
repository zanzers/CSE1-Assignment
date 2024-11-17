from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)


books = [
    {
        'id': 1,
        'Title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'year': 1960,
    },
    {
        'id': 2,
        'Title': '1984',
        'author': 'George Orwell',
        'year': 1949,
    },
    {
        'id': 3,
        'Title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'year': 1813,
    },
    {
        'id': 4,
        'Title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'year': 1925,
    },
    {
        'id': 5,
        'Title': 'Moby-Dick',
        'author': 'Herman Melville',
        'year': 1851,
    }
]























# @app.route('/')
# def hello_word():
#     return "Hello Word"



if __name__ == "__main__":
    app.run(debug=True)