from config import db
from entities.book import Book

# Hakee kaikki kirjat ja niiden tiedot
def get_books():
    all_books = Book.query.order_by(Book.id).all()
    return all_books

def get_book_by_id(id):
    return Book.query.get(id)

# Luo uuden kirjan
def create_book(author, title, publisher, year):
    new_book = Book(author=author,
                    title=title,
                    publisher=publisher,
                    year=year)
    db.session.add(new_book)
    db.session.commit()

def delete_book(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()

def edit_book(id, author, title, publisher, year):
    book = get_book_by_id(id)
    book.id = id
    book.author = author
    book.title = title
    book.publisher = publisher
    book.year = year
    db.session.commit()
