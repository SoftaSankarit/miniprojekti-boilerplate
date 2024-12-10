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
    return new_reference


def delete_reference(id):
    References.query.filter_by(id=id).delete()
    db.session.commit()

def edit_reference(id, optionals):
    reference = get_reference_by_id(id)
    reference.id = id
    for field, value in optionals.items():
        if value:
            setattr(reference, field, value)
    db.session.commit()


def get_reference_by_id(id):
    return References.query.get(id)

def search_references(query):
    search_term = f"%{query}%"
    return References.query.filter(
        (References.reftype.ilike(search_term)) |
        (References.author.ilike(search_term)) |
        (References.title.ilike(search_term)) |
        (References.publisher.ilike(search_term)) |
        (cast(References.year, String).ilike(search_term)) |
        (References.howpublished.ilike(search_term)) |
        (References.institution.ilike(search_term)) |
        (References.journal.ilike(search_term)) |
        (References.volume.ilike(search_term)) |
        (References.address.ilike(search_term)) |
        (cast(References.number, String).ilike(search_term)) |
        (References.organization.ilike(search_term)) |
        (References.school.ilike(search_term)) |
        (References.series.ilike(search_term)) |
        (References.issue.ilike(search_term)) |
        (References.edition.ilike(search_term)) |
        (References.chapter.ilike(search_term)) |
        (References.pages.ilike(search_term)) |
        (References.url.ilike(search_term)) |
        (References.key.ilike(search_term)) |
        (References.month.ilike(search_term)) |
        (References.note.ilike(search_term)) |
        (References.misc_details.ilike(search_term)) |
        (References.doi.ilike(search_term)) |
        (References.booktitle.ilike(search_term)) |
        (References.editor.ilike(search_term)) |
        (References.type.ilike(search_term))
    ).all()
