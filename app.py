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




@app.route('/api/create_books', methods=['POST'])
def create_books():
    if not request.is_json:
        
         return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    required_fields = ['Title', 'author', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), HTTPStatus.BAD_REQUEST

    new_book = {
        'id': max([book['id'] for book in books], default=0) + 1,
        'Title' : data['Title'],
        'author': data['author'],
        'year': data['year']
    }

    books.append(new_book)

    return jsonify({
        "success": True,
        "data": new_book
    }),HTTPStatus.CREATED














# @app.route('/')
# def hello_word():
#     return "Hello Word"



if __name__ == "__main__":
    app.run(debug=True)