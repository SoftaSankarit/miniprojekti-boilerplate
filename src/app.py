import io
from flask import redirect, render_template, request, jsonify, send_file, flash
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from db_helper import reset_db
from repositories.book_repository \
    import get_books, get_book_by_id, create_book, delete_book, edit_book
from config import app, test_env
from util import validate_year

# Lataa nykyiset kirjat alkunäytölle
@app.route("/")
def index():
    books = get_books()
    return render_template("index.html", books=books)

@app.route("/new_book")
def new_book():
    return render_template("new_book.html")

# Luo kirjan databaseen riippuen syötteistä
@app.route("/create_book", methods=["GET","POST"])
def book_creation():
    try:
        author = request.form.get("author").strip()
        title = request.form.get("title").strip()
        publisher = request.form.get("publisher").strip()
        year = request.form.get("year")
        validate_year(year=year)
        # Tarkistaa onko valinnainen syöte täytetty ja lisää annetut lisävalinnat
        all_options = ("volume", "series", "address", "edition", "month", "note", "key", "url")
        optionals = {}
        for i in all_options:
            test = request.form.get(i)
            if test is not None:
                optionals[i] = test
        create_book(author, title, publisher, year, optionals)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_book")

# Luo txt-muotoisen tiedoston, jossa ovat kaikki kirjat BibTeX muodossa
@app.route("/generate_bibtex")
def generate_bibtex():
    books = get_books()
    db_bib = BibDatabase()

    def generate_book_id(book):
        author_last_name = book.author.split(" ")[-1]
        title = book.title.split(" ")[0]
        year = book.year
        book_id = author_last_name + title + str(year)
        return book_id

    db_bib.entries = [
        {
            "ENTRYTYPE": "book",
            "ID": generate_book_id(book),
            "author": book.author,
            "title": book.title,
            "year": str(book.year),
            "publisher": book.publisher,
        **{
            field: getattr(book, field)
            for field in ["volume", "series", "address", "edition", "month", "note", "key", "url"]
            if getattr(book, field) is not None
        },
        }
        for book in books
    ]
    writer = BibTexWriter()
    bibtex_string = writer.write(db_bib)

    return send_file(
        io.BytesIO(bibtex_string.encode("utf-8")),
        mimetype="tetx/plain",
        as_attachment=True,
        download_name= "Bibtex.txt")

#Poistaa viitteen tietokannasta
@app.route("/delete_entry/<entry_type>/<entry_id>")
def delete_entry(entry_type,entry_id):
    if entry_type == "book":
        delete_book(entry_id)
    return redirect("/")


#Muokkaa viitettä
@app.route("/edit_entry/<entry_type>/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_type,entry_id):
    if entry_type == "book":
        book = get_book_by_id(entry_id)
        if request.method == "GET":
            return render_template("new_book.html", book=book, is_edit=True)
        if request.method == "POST":
            author = request.form.get("author").strip()
            title = request.form.get("title").strip()
            publisher = request.form.get("publisher").strip()
            year = request.form.get("year")
            edit_book(id=entry_id, author=author, title=title, publisher=publisher, year=year)
            return redirect("/")
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
