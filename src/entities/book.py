from config import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # Valinnaiset
    volume = db.Column(db.String(50), nullable=True)  
    series = db.Column(db.String(100), nullable=True) 
    address = db.Column(db.String(200), nullable=True)
    edition = db.Column(db.String(50), nullable=True)  
    month = db.Column(db.String(20), nullable=True)  
    note = db.Column(db.Text, nullable=True) 
    key = db.Column(db.String(100), nullable=True) 
    url = db.Column(db.String(200), nullable=True)  