from sqlalchemy import cast, String
from config import db
from entities.reference import References



# Hakee kaikki kirjat ja niiden tiedot
def get_references():
    all_references = References.query.order_by(References.id).all()
    print(all_references)
    return all_references
# Luo uuden kirjan
def create_reference(optionals, reftype):
    new_reference = References()
    setattr(new_reference, "reftype", reftype)
    # Lisää kaikki valinnaiset jos eivät ole tyhjiä
    for field, value in optionals.items():
        if value:
            setattr(new_reference, field, value)
    db.session.add(new_reference)
    db.session.commit()


def delete_reference(reference_id):
    References.query.filter_by(id=reference_id).delete()
    db.session.commit()

def edit_reference(reference_id, optionals):
    reference = get_reference_by_id(reference_id)
    reference.id = reference_id
    for field, value in optionals.items():
        if value:
            setattr(reference, field, value)
    db.session.commit()


def get_reference_by_id(reference_id):
    return References.query.get(reference_id)

def search_references(query):
    search_term = f"%{query}%"
    return References.query.filter(
        (References.author.ilike(search_term)) |
        (References.title.ilike(search_term)) |
        (References.publisher.ilike(search_term)) |
        (cast(References.year, String).ilike(search_term))
    ).all()
