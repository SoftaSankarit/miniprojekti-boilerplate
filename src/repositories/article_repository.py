from sqlalchemy import text
from config import db
from entities.article import Article

# Hakee kaikki kirjat ja niiden tiedot
def get_articles():
    all_books = Article.query.all()
    return all_books

# Luo uuden kirjan
def create_article(author, title, journal, year):
    new_article = Article(author=author,
                    title=title,
                    journal=journal,
                    year=year) 
    db.session.add(new_article)
    db.session.commit()

def delete_article(id):
    Article.query.filter_by(id=id).delete()
    db.session.commit()