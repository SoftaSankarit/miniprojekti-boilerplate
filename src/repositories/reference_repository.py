from sqlalchemy import cast, String
from config import db
from entities.reference import References



# Hakee kaikki kirjat ja niiden tiedot
def get_references():
    all_references = References.query.order_by(References.id).all()
    print(all_references)
    return all_references
# Luo uuden kirjan
def create_reference(optionals):
    new_reference = References()
    # Lisää kaikki valinnaiset jos eivät ole tyhjiä
    for field, value in optionals.items():
        if value:
            setattr(new_reference, field, value)
    db.session.add(new_reference)
    db.session.commit()


def delete_reference(id): # pylint: disable=invalid-name
    References.query.filter_by(id=id).delete() # pylint: disable=invalid-name
    db.session.commit()

def edit_reference(id, optionals): # pylint: disable=invalid-name
    reference = get_reference_by_id(id) # pylint: disable=invalid-name
    reference.id = id # pylint: disable=invalid-name
    for field, value in optionals.items():
        if value:
            setattr(reference, field, value)
    db.session.commit()


def get_reference_by_id(id): # pylint: disable=invalid-name
    return References.query.get(id) # pylint: disable=invalid-name

def search_references(query):
    search_term = f"%{query}%"
    return References.query.filter(
        (References.author.ilike(search_term)) |
        (References.title.ilike(search_term)) |
        (References.publisher.ilike(search_term)) |
        (cast(References.year, String).ilike(search_term))
    ).all()
