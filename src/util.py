import re

class UserInputError(Exception):
    pass


REFERENCE_FIELDS = {
    "article": [
        ["author", "title", "journal", "year"],
        ["volume/number", "pages", "month", "doi", "note", "key"]
    ],
    "book": [
        ["author", "title", "publisher", "year"],
        ["volume/number", "series", "address", "edition", "month", "note", "key", "url"]
    ],
    "booklet": [
        ["title"],
        ["author", "howpublished", "address", "month", "year", "note", "key"]
    ],
    "conference": [
        ["author", "title", "booktitle", "year"],
        ["editor", "volume/number", "series", "pages", "address", "month", "organization", "publisher", "note", "key"]
    ],
    "inbook": [
        ["author", "title", "chapter/pages", "publisher", "year"],
        ["volume/number", "series", "type", "address", "edition", "month", "note", "key"]
    ],
    "incollection": [
        ["author", "title", "booktitle", "publisher", "year"],
        ["editor", "volume/number", "series", "type", "chapter", "pages", "address", "edition", "month", "note", "key"]
    ],
    "inproceedings": [
        ["author", "title", "booktitle", "year"],
        ["editor", "volume/number", "series", "pages", "address", "month", "organization", "publisher", "note", "key"]
    ],
    "manual": [
        ["title"],
        ["author", "organization", "address", "edition", "month", "year", "note", "key"]
    ],
    "mastersthesis": [
        ["author", "title", "school", "year"],
        ["type", "address", "month", "note", "key"]
    ],
    "misc": [
        [],
        ["author", "title", "howpublished", "month", "year", "note", "key"]
    ],
    "phdthesis": [
        ["author", "title", "school", "year"],
        ["type", "address", "month", "note", "key"]
    ],
    "proceedings": [
        ["title", "year"],
        ["editor", "volume/number", "series", "address", "month", "publisher", "organization", "note", "key"]
    ],
    "techreport": [
        ["author", "title", "institution", "year"],
        ["type", "number", "address", "month", "note", "key"]
    ],
    "unpublished": [
        ["author", "title", "note"],
        ["month", "year", "key"]
    ]
}


def validate_year(year):
    try:
        int(year)
    except ValueError:
        raise UserInputError("Vuoden pitää olla numero.")

    if int(year) > 2024 or int(year) < 1:
        raise UserInputError("Vuoden pitää olla välillä 1-2024.")

def validate_text_field(text):
    print(text)
    if len(text) > 40:
        raise UserInputError("Syötteen pitää olla lyhyempi kuin 40 merkkiä.")
    if len(text) < 3:
        raise UserInputError("Syötteen pitää olla pidempi kuin 3 merkkiä.")


def validate_form(reference_type, fields):
    print("Virheiden tarkistus")
    for field in fields:
        value = fields[field]
        # jos kenttä on pakollinen
        if field in REFERENCE_FIELDS[reference_type][0]:
            if value is None:
                raise UserInputError("Syöte ei saa olla tyhjä.")
            if not re.match(r'^[a-zA-Z0-9äöåÄÖÅ\s.,&\'"()-]*$', value):
                raise UserInputError(f"""{value} sisältää kiellettyjä merkkejä.
                                     Sallitut erikoismerkit ovat: . , & ' \" ( ) -""")
            if field == "year":
                validate_year(value)
            if field == "author":
                validate_text_field(value)
            if field == "title":
                validate_text_field(value)
            if field == "journal":
                validate_text_field(value)
            if field == "publisher":
                validate_text_field(value)
