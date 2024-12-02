import io
from flask import redirect, render_template, request, jsonify, send_file, flash
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from db_helper import setup_db
from repositories.reference_repository \
    import get_references, get_reference_by_id, create_reference, delete_reference, edit_reference
from config import app, test_env
from util import validate_year

# Lataa nykyiset kirjat alkunäytölle
@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html")

# Luo kirjan databaseen riippuen syötteistä
@app.route("/create_reference", methods=["GET","POST"])
def reference_creation():
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
        create_reference(author, title, publisher, year, optionals)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_reference")

# Luo txt-muotoisen tiedoston, jossa ovat kaikki kirjat BibTeX muodossa
@app.route("/generate_bibtex")
def generate_bibtex():
    references = get_references()
    db_bib = BibDatabase()

    def generate_book_id(reference):
        author_last_name = reference.author.split(" ")[-1]
        title = reference.title.split(" ")[0]
        year = reference.year
        reference_id = author_last_name + title + str(year)
        return reference_id

    db_bib.entries = [
        {
            "ENTRYTYPE": "book",
            "ID": generate_book_id(reference),
            "author": reference.author,
            "title": reference.title,
            "year": str(reference.year),
            "publisher": reference.publisher,
        **{
            field: getattr(reference, field)
            for field in ["volume", "series", "address", "edition", "month", "note", "key", "url"]
            if getattr(reference, field) is not None
        },
        }
        for reference in references
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
    delete_reference(entry_id)
    return redirect("/")


#Muokkaa viitettä
@app.route("/edit_entry/<entry_type>/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_type,entry_id):
    reference = get_reference_by_id(entry_id)
    if request.method == "GET":
        return render_template("edit_reference.html", reference=reference, is_edit=True)
    if request.method == "POST":
        author = request.form.get("author").strip()
        title = request.form.get("title").strip()
        publisher = request.form.get("publisher").strip()
        year = request.form.get("year")
        all_options = ("volume", "series", "address", "edition", "month", "note", "key", "url")
        optionals = {}
        for i in all_options:
            test = request.form.get(i)
            if test is not None:
                optionals[i] = test
        edit_reference(id=entry_id, author=author, title=title, publisher=publisher, year=year, optionals=optionals)
        return redirect("/")
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        setup_db()
        return jsonify({ 'message': "db reset" })
