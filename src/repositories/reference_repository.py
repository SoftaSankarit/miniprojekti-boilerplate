from config import db
from models.reference import Reference
from models.type import Type

# Hakee kaikki viitteet ja niiden tiedot
def get_references():
    all_references = Reference.query.order_by(Reference.id).all()
    return all_references

# Hakee viitteen id:n perusteella
def get_reference_by_id(id):  # pylint: disable=invalid-name
    return Reference.query.get(id)

# Luo uuden viitteen
def create_reference(type_name, title, author=None, year=None, optionals={}):
    # Hae viitteen tyyppi type-taulusta
    ref_type = Type.query.filter_by(name=type_name).first()
    if not ref_type:
        raise ValueError(f"Viitteen tyyppiä '{type_name}' ei löytynyt.")

    new_reference = Reference(
        type_id=ref_type.id,
        title=title,
        author=author,
        year=year
    )
    # Lisää kaikki valinnaiset kentät, jos ne eivät ole tyhjiä
    for field, value in optionals.items():
        if value:
            setattr(new_reference, field, value)

    db.session.add(new_reference)
    db.session.commit()

# Poistaa viitteen id:n perusteella
def delete_reference(id):  # pylint: disable=invalid-name
    Reference.query.filter_by(id=id).delete()  # pylint: disable=invalid-name
    db.session.commit()

# Muokkaa viitettä
def edit_reference(id, type_name, title, author=None, year=None, optionals={}):  # pylint: disable=invalid-name
    ref = get_reference_by_id(id)  # pylint: disable=invalid-name
    if not ref:
        raise ValueError(f"Viitettä id:llä '{id}' ei löytynyt.")

    # Päivitä tyyppi
    ref_type = Type.query.filter_by(name=type_name).first()
    if not ref_type:
        raise ValueError(f"Viitteen tyyppiä '{type_name}' ei löytynyt.")
    ref.type_id = ref_type.id

    # Päivitä yleiset tiedot
    ref.title = title
    ref.author = author
    ref.year = year

    # Päivitä valinnaiset tiedot
    for field, value in optionals.items():
        if value:
            setattr(ref, field, value)

    db.session.commit()
