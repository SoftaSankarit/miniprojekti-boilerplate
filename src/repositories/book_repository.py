from sqlalchemy import text
from config import db
from entities.book import Book

# Hakee kaikki kirjat ja niiden tiedot
def get_books():
    all_books = Book.query.all()
    return all_books

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