from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Book {self.Title}>"
    
    @classmethod
    def get_book_by_id(cls, book_id):
        return db.session.get(cls, book_id)
    
    @classmethod
    def create_book(cls, title, author, year):
        new_book = cls(Title=title, author=author, year=year)
        db.session.add(new_book)
        db.session.commit()
        return new_book
    
    @classmethod
    def update_book(cls, book_id, title, author, year):
        book = db.session.get(cls,book_id)

        if book:
            book.Title = title
            book.author = author
            book.year = year
            db.session.commit()
            return book
        
    @classmethod
    def delete_book(cls, book_id):
        book = db.session.get(cls,book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return book
        return None

