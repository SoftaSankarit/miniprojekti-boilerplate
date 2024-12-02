import io
from flask import redirect, render_template, request, jsonify, send_file, flash
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from db_helper import reset_db
from repositories.reference_repository \
    import get_references, get_reference_by_id, create_reference, delete_reference, edit_reference
from config import app, test_env
from util import validate_year

# Alkunäyttö, lataa kaikki viitteet
@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html")

# Luo uusi viite tietokantaan syötteiden perusteella
@app.route("/create_reference", methods=["GET", "POST"])
def reference_creation():
    try:
        type_name = request.form.get("type_name").strip()
        author = request.form.get("author", "").strip()
        title = request.form.get("title").strip()
        year = request.form.get("year")
        validate_year(year=year)

        # Tarkistaa valinnaiset kentät
        all_options = (
            "publisher", "howpublished", "institution", "journal", "volume",
            "number", "organization", "school", "series", "issue", "edition",
            "chapter", "pages", "url", "key", "month", "note", "misc_details", "doi"
        )
        optionals = {}
        for field in all_options:
            value = request.form.get(field)
            if value:
                optionals[field] = value

        create_reference(type_name, title, author, year, optionals)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_reference")

# Luo txt-muotoisen BibTeX-tiedoston kaikista viitteistä
@app.route("/generate_bibtex")
def generate_bibtex():
    references = get_references()
    db_bib = BibDatabase()

    def generate_reference_id(reference):
        author_last_name = (reference.author or "").split(" ")[-1]
        title = reference.title.split(" ")[0]
        year = reference.year or ""
        return f"{author_last_name}{title}{year}"

    db_bib.entries = [
        {
            "ENTRYTYPE": ref.type.name,
            "ID": generate_reference_id(ref),
            "title": ref.title,
            "author": ref.author or "",
            "year": str(ref.year) if ref.year else "",
            **{
                field: getattr(ref, field)
                for field in (
                    "publisher", "howpublished", "institution", "journal", "volume",
                    "number", "organization", "school", "series", "issue", "edition",
                    "chapter", "pages", "url", "key", "month", "note", "misc_details", "doi"
                )
                if getattr(ref, field) is not None
            }
        }
        for ref in references
    ]

    writer = BibTexWriter()
    bibtex_string = writer.write(db_bib)

    return send_file(
        io.BytesIO(bibtex_string.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name="Bibtex.txt"
    )

# Poistaa viitteen tietokannasta
@app.route("/delete_entry/<entry_id>")
def delete_entry(entry_id):
    delete_reference(entry_id)
    return redirect("/")

# Muokkaa viitettä
@app.route("/edit_entry/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    reference = get_reference_by_id(entry_id)
    if not reference:
        flash("Viitettä ei löytynyt.")
        return redirect("/")

    if request.method == "GET":
        return render_template("new_reference.html", reference=reference, is_edit=True)

    if request.method == "POST":
        try:
            type_name = request.form.get("type_name").strip()
            author = request.form.get("author", "").strip()
            title = request.form.get("title").strip()
            year = request.form.get("year")
            validate_year(year=year)

            all_options = (
                "publisher", "howpublished", "institution", "journal", "volume",
                "number", "organization", "school", "series", "issue", "edition",
                "chapter", "pages", "url", "key", "month", "note", "misc_details", "doi"
            )
            optionals = {}
            for field in all_options:
                value = request.form.get(field)
                if value:
                    optionals[field] = value

            edit_reference(entry_id, type_name, title, author, year, optionals)
            return redirect("/")
        except Exception as error:
            flash(str(error))
            return redirect(f"/edit_entry/{entry_id}")

# Testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({'message': "db reset"})
