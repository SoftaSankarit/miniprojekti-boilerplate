from config import db
from entities.book import References

# Hakee kaikki kirjat ja niiden tiedot
def get_references():
    print("11111111")
    all_references = References.query.order_by(References.id).all()
    print(all_references)
    return all_references

def get_book_by_id(id): # pylint: disable=invalid-name
    return Book.query.get(id) # pylint: disable=invalid-name

# Luo uuden kirjan
def create_reference(author, title, publisher, year, optionals):
    new_reference = References(author=author,
                    title=title,
                    publisher=publisher,
                    year=year)
    # Lisää kaikki valinnaiset jos eivät ole tyhjiä
    for field, value in optionals.items():
        if value:
            setattr(new_reference, field, value)
    db.session.add(new_reference)
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
