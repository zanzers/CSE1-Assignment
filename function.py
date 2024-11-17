
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



# Finding NEmo/Books
def find_book(book_id):
    return next((book for book in books if book ['id'] == book_id), None)


