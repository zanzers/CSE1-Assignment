from flask import Flask, jsonify, request
from http import HTTPStatus
from function import *

app = Flask(__name__)





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

@app.route('/api/get_books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "success": False,
            "error": "Book does not exist"
        }), HTTPStatus.NOT_FOUND

    return jsonify({
        "success": True,
        "data": book
    }), HTTPStatus.OK











# @app.route('/')
# def hello_word():
#     return "Hello Word"



if __name__ == "__main__":
    app.run(debug=True)