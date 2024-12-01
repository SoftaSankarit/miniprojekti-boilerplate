from config import db
from entities.book import Book

# Hakee kaikki kirjat ja niiden tiedot
def get_books():
    all_books = Book.query.order_by(Book.id).all()
    return all_books

def get_book_by_id(id): # pylint: disable=invalid-name
    return Book.query.get(id) # pylint: disable=invalid-name

# Luo uuden kirjan
def create_book(author, title, publisher, year, optionals):
    new_book = Book(author=author,
                    title=title,
                    publisher=publisher,
                    year=year)
    # Lisää kaikki valinnaiset jos eivät ole tyhjiä
    for field, value in optionals.items():
        if value:
            setattr(new_book, field, value)
    db.session.add(new_book)
    db.session.commit()

def delete_book(id): # pylint: disable=invalid-name
    Book.query.filter_by(id=id).delete() # pylint: disable=invalid-name
    db.session.commit()

def edit_book(id, author, title, publisher, year, optionals): # pylint: disable=invalid-name
    book = get_book_by_id(id) # pylint: disable=invalid-name
    book.id = id # pylint: disable=invalid-name
    book.author = author
    book.title = title
    book.publisher = publisher
    book.year = year
    for field, value in optionals.items():
        if value:
            setattr(book, field, value)
    db.session.commit()
