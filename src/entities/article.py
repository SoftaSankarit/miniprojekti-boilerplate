from config import db


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    journal = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
