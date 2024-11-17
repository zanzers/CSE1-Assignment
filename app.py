from flask import Flask, jsonify, request
from http import HTTPStatus
from function import *
from books_model import *



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/home', methods=['GET'])
def view():
 
    books = Book.query.all()

    books_list = [
        {
            "id": book.id,
            "Title": book.Title,
            "author": book.author,
            "year": book.year
        }
        for book in books
    ]
    return jsonify({
        "success": True,
        "data": books_list
    }), HTTPStatus.OK

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



    new_book = Book.create_book(data['Title'], data['author'], data['year'])

    return jsonify({
        "success": True,
        "data": {
            "id": new_book.id,
            "Title": new_book.Title,
            "author": new_book.author,
            "year": new_book.year
        }
    }),HTTPStatus.CREATED


@app.route('/api/get_books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    
    book = Book.get_book_by_id(book_id)

    if book is None:
        return jsonify({
            "success": False,
            "error": "Book does not exist"
        }), HTTPStatus.NOT_FOUND

    return jsonify({
        "success": True,
        "data": {
            "id": book.id,
            "Title": book.Title,
            "author": book.author,
            "year": book.year
        }
    }), HTTPStatus.OK


@app.route('/api/update_books/<int:book_id>', methods=['PUT'])
def update_books(book_id):
    
    book = Book.get_book_by_id(book_id)

    if book is None:
        return jsonify({
            "success": False,
            "error" : "Book not Found"
        }), HTTPStatus.NOT_FOUND

    print(f"Before Update: {book}")
    data = request.get_json()

    required_fields = ['Title', 'author', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), HTTPStatus.BAD_REQUEST

    updated_book = Book.update_book(book_id, data['Title'], data['author'], data['year'])
    if updated_book is None:
        return jsonify({
            "success": False,
            "error" : "Failed to update book"
        }), HTTPStatus.BAD_REQUEST

    print(f"After Update: {book}")

    return jsonify({
            "success": True,
            "data": {
            "id": updated_book.id,
            "Title": updated_book.Title,
            "author": updated_book.author,
            "year": updated_book.year
            }
    }),HTTPStatus.OK


@app.route('/api/remove/<int:book_id>', methods=['DELETE'])
def delete_books(book_id):
    
    book = Book.get_book_by_id(book_id)

    if book is None:
        return jsonify({
            "success": False,
            "error": "Book not found"
        }), HTTPStatus.NOT_FOUND
    

    return jsonify({
        "success": True,
        "message": f"Book with id {book_id} deleted successfully"
    }), HTTPStatus.NO_CONTENT




if __name__ == "__main__":
    app.run(debug=True)  # pragma: no cover

#  pytest --cov=app test_client.py