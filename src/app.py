import io
from flask import redirect, render_template, request, jsonify, send_file, flash
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import requests
from db_helper import setup_db
from repositories.reference_repository \
    import get_references, get_reference_by_id, create_reference, delete_reference, edit_reference, search_references
from config import app, test_env
from util import validate_form, find_crossref_type, fill_doi_fields, REFERENCE_FIELDS, FINNISH_FIELDS


# Lataa nykyiset kirjat alkunäytölle
@app.route("/")
def index():
    query = request.args.get("query")
    if query:
        references = search_references(query)
    else:
        references = get_references()
    return render_template("index.html", references=references)


#Lisää uusi viite
@app.route("/new_reference/<reference_type>")
def new_reference(reference_type):
    if reference_type not in REFERENCE_FIELDS:
        return render_template("error.html", error="Sivua ei löytynyt.")
    return render_template("new_reference.html",
                           reference_type=reference_type,
                           reference_fields=REFERENCE_FIELDS,
                           finnish_fields=FINNISH_FIELDS)


# Luo viitteen databaseen riippuen syötteistä
@app.route("/create_reference", methods=["GET","POST"])
def reference_creation():
    reftype = request.form.get("reftype")
    filled_fields = {}

    for field in REFERENCE_FIELDS[reftype][0]:
        filled_fields[field] = request.form.get(field)

    for field in REFERENCE_FIELDS[reftype][1]:
        value = request.form.get(field)
        if value:
            filled_fields[field] = value

    try:
        validate_form(reftype, filled_fields)
        create_reference(filled_fields, reftype)
        return redirect("/")

    except Exception as error:
        flash(str(error))
        return render_template(
            "new_reference.html",
            form_data=filled_fields,
            reference_type=reftype,
            reference_fields=REFERENCE_FIELDS,
            finnish_fields=FINNISH_FIELDS
        )


# Luo viitteen doi-tunnuksen perusteella
@app.route("/doi_reference", methods=["GET","POST"])
def doi_reference():
    doi = request.form.get("doi")
    if not doi:
        flash("Kenttää ei voi jättää tyhjäksi.")
        return redirect("/#doiForm")

    response = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
    if response.status_code != 200:
        flash("Virhe. Tarkista DOI.")
        return redirect("/")

    doi_data = response.json().get("message", {})
    reference_type = find_crossref_type(doi_data)
    prefilled_data = fill_doi_fields(reference_type, doi_data)

    try:
        validate_form(reference_type, prefilled_data)
        return render_template("new_doi_reference.html",
                            form_data=prefilled_data,
                            reference_type=reference_type,
                            reference_fields=REFERENCE_FIELDS,
                            finnish_fields=FINNISH_FIELDS
                            )
    except Exception as error:
        flash(str(error))
        return redirect("/#doiForm")


# Luo txt-muotoisen tiedoston, jossa ovat kaikki kirjat BibTeX muodossa
@app.route("/generate_bibtex")
def generate_bibtex():
    references = get_references()
    db_bib = BibDatabase()

    def generate_reference_id(reference):
        if reference.author:
            name = reference.author.split(" ")[-1]
            if name == "al.":
                name = reference.author.split(" ")[-3].strip(",")
        elif reference.editor:
            name = reference.editor.split(" ")[-1]
        else:
            name = "Unknown"
        if reference.title:
            title = reference.title.split(" ")[0]
        else:
            title = "Misc" + str(reference.id)
        if reference.year:
            year = reference.year
        else:
            year = "N.D" # No Date
        return name + title + year

    db_bib.entries = [
        {
            "ENTRYTYPE": reference.reftype,
            "ID": generate_reference_id(reference),
        **{
            field: getattr(reference, field)
            for field in ["author", "title", "publisher", "year", "howpublished",
    "institution", "journal", "volume", "number", "address",
    "organization", "school", "series", "issue", "edition",
    "chapter", "pages", "url", "key", "month",
    "note", "misc_details", "doi"
]

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
        return render_template(
            "edit_reference.html",
            form_data=reference,
            reference_type=entry_type,
            reference_fields=REFERENCE_FIELDS,
            finnish_fields=FINNISH_FIELDS,
            is_edit=True
        )

    if request.method == "POST":
        filled_fields = {}
        for field in REFERENCE_FIELDS[entry_type][0]:
            filled_fields[field] = request.form.get(field)

        for field in REFERENCE_FIELDS[entry_type][1]:
            value = request.form.get(field)
            if value:
                filled_fields[field] = value
        filled_fields["id"] = entry_id

        try:
            validate_form(entry_type, filled_fields)
            edit_reference(entry_id, filled_fields)
            return redirect("/")

        except Exception as error:
            flash(str(error))
            return render_template(
                "edit_reference.html",
                form_data=filled_fields,
                reference_type=entry_type,
                reference_fields=REFERENCE_FIELDS,
                finnish_fields=FINNISH_FIELDS,
                is_edit=True
            )
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        setup_db()
        return jsonify({ 'message': "db reset" })
