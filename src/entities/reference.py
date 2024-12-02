from config import db


class References(db.Model):
    __tablename__ = "reference"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=False)

    # Valinnaiset
    publisher = db.Column(db.String(100), nullable=True)
    howpublished = db.Column(db.String(100), nullable=True)
    institution = db.Column(db.String(200), nullable=True)
    journal = db.Column(db.String(100), nullable=True)
    volume = db.Column(db.String(50), nullable=True)
    number = db.Column(db.Integer, nullable=True)
    organization = db.Column(db.String(100), nullable=True)
    school = db.Column(db.String(100), nullable=True)
    series = db.Column(db.String(100), nullable=True)
    issue = db.Column(db.String(50), nullable=True)
    edition = db.Column(db.String(100), nullable=True)
    chapter = db.Column(db.String(50), nullable=True)
    pages = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    key = db.Column(db.String(100), nullable=True)
    month = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
    misc_details = db.Column(db.Text, nullable=True)
    doi = db.Column(db.String(150), nullable=True)
