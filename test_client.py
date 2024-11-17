import pytest
from app import app
from books_model import db, Book
from unittest.mock import patch




@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all() 
        yield client  

def test_create_book_from_client(test_client):
    response = test_client.post('/api/create_books', json={
        'Title': 'Test Book',
        'author': 'Test Author',
        'year': 2024
    })

    assert response.status_code == 201
    response_json = response.get_json()
    
    assert response_json['success'] == True
    assert response_json['data']['Title'] == 'Test Book'
    assert response_json['data']['author'] == 'Test Author'
    assert response_json['data']['year'] == 2024

def test_update_book_from_client(test_client):
    book_to_Update = 2

    update_response = test_client.put(f'/api/update_books/{book_to_Update}', json={
        'Title': 'Update Book',
        'author': 'Update Author',
        'year': 2000
    })

    assert update_response.status_code == 200

    update_response_json = update_response.get_json()


    assert update_response_json['success'] == True
    assert update_response_json['data']['id'] == book_to_Update
    assert update_response_json['data']['Title'] == 'Update Book'
    assert update_response_json['data']['author'] == 'Update Author'
    assert update_response_json['data']['year'] == 2000

def test_get_books_from_client(test_client):
    
    test_get_bookID = 1

    get_response = test_client.get(f'/api/get_books/{test_get_bookID}')
    assert get_response.status_code == 200

    get_response_json = get_response.get_json()
    assert get_response_json['success'] == True
    assert get_response_json['data']['id'] == test_get_bookID
    assert get_response_json['data']['Title'] == 'Test Book'
    assert get_response_json['data']['author'] == 'Test Author'
    assert get_response_json['data']['year'] == 2024

def test_delete_book_from_client(test_client):
    delete_BookID = 1

    delete_response = test_client.delete(f'/api/remove/{delete_BookID}')
    assert delete_response.status_code == 204
    assert delete_response.data == b''

    get_response = test_client.get(f'/api/get_books/{delete_BookID}')
    
    assert get_response.status_code == 200
    get_response_json = get_response.get_json()
    assert get_response_json['success'] == True

def test_view_books_from_client(test_client):
    response = test_client.get('/api/home')
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json['success'] == True
    assert isinstance(response_json['data'], list)

    if response_json['data']:
        for book in response_json['data']:
            assert 'id' in book
            assert 'Title' in book
            assert 'author' in book
            assert 'year' in book
    else:
        assert response_json['data'] == []


def test_delete_book_not_found_from_client(test_client):
    delete_BookID = 999  

    delete_response = test_client.delete(f'/api/remove/{delete_BookID}')
    assert delete_response.status_code == 404
    delete_response_json = delete_response.get_json()
    assert delete_response_json['success'] == False
    assert "not found" in delete_response_json['error']

def test_create_book_missing_field_from_client(test_client):
    response = test_client.post('/api/create_books', json={
        'Title': 'Test Book',
        'author': 'Test Author'
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert response_json['success'] == False
    assert 'Missing required field' in response_json['error']

def test_get_book_not_found_from_client(test_client):
    
    book_id = 999
    response = test_client.get(f'/api/get_books/{book_id}')
    
    assert response.status_code == 404  
    response_json = response.get_json()
    assert response_json['success'] == False
    assert response_json['error'] == "Book does not exist" 

def test_update_book_not_Found_from_client(test_client):

    book_to_update = 999
    response = test_client.put(f'api/update_books/{book_to_update}')

    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json['success'] == False
    assert response_json['error'] == "Book not Found"

def test_create_book_badRequest_from_client(test_client):

    response = test_client.post('/api/create_books', data="Title=Test Book&author=Test Author&year=2024")
    assert response.status_code == 400
    response_json = response.get_json()
    assert response_json['success'] == False
    assert response_json['error'] == "Content-type must be application/json"

def test_update_book_missing_field(test_client):
    book_id_to_update = 1  

    response = test_client.put(f'/api/update_books/{book_id_to_update}', json={
        'author': 'New Author',
        'year': 2024
    })
    assert response.status_code == 400 
    response_json = response.get_json()
    assert response_json['success'] == False
    assert "Missing required field" in response_json['error']

def test_update_book_failed_update(test_client):
    book_id_to_update = 1
    with patch('books_model.Book.update_book', return_value=None):
        response = test_client.put(f'/api/update_books/{book_id_to_update}', json={
            'Title': 'New Title',
            'author': 'New Author',
            'year': 2024
        })
    assert response.status_code == 400
    response_json = response.get_json()

    assert response_json['success'] == False
    assert "Failed to update book" in response_json['error']


