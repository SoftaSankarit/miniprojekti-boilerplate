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
    if len(text) < 3:
        raise UserInputError("Syötteen pitää olla pidempi kuin 3 merkkiä.")
    if len(text) > 150:
        raise UserInputError("Syötteen pitää olla lyhyempi kuin 150 merkkiä.")


def validate_doi(doi):
    if not doi.startswith("10."):
        raise UserInputError("DOI:n pitää alkaa '10.'.")
    if len(doi) > 255:
        raise UserInputError("DOI:n pituus ei saa ylittää 200 merkkiä.")


def validate_form(reference_type, fields):
    print("Virheiden tarkistus")
    valid_fields = REFERENCE_FIELDS[reference_type][0] + REFERENCE_FIELDS[reference_type][1]

    for field in fields:
        if field not in valid_fields:
           raise UserInputError(f"Field '{field}' is not valid for reference type '{reference_type}'.")

        value = fields[field]
        if field in REFERENCE_FIELDS[reference_type][0] or REFERENCE_FIELDS[reference_type][1]:
            print(field)
            print(value)

            if value is None:
                raise UserInputError("Syöte ei saa olla tyhjä.")
            
            if field == "year":
                validate_year(value)
            if field in [
                "author", "title", "publisher", "institution", "journal",
                "organization", "school", "series", "issue", "edition",
                "chapter", "key", "note", "misc_details"
            ] and value != "":
                validate_text_field(value)
            if field == "doi":
                validate_doi(value)


def find_crossref_type(data):
    crossref_type = data.get("type", "unknown")
    type_dict = {
        "journal-article": "article",
        "book": "book",
        "book-chapter": "inbook",
        "proceedings-article": "inproceedings",
        "dataset": "misc",
        "report": "techreport",
        "thesis": "phdthesis",
        "other": "misc",
    }
    return type_dict.get(crossref_type, None)


def fill_doi_fields(reference_type, data):
    all_fields = REFERENCE_FIELDS[reference_type][0] + REFERENCE_FIELDS[reference_type][1]
    filled_fields = {}

    for field in all_fields:
        if field == "author" and "author" in data:
            authors = [
                f"{author.get('given', '')} {author.get('family', '')}"
                for author in data["author"]
            ]
            if len(authors) > 1:
                filled_fields[field] = authors[0] + ", et al."
            else:
                filled_fields[field] = authors[0]

        elif field == "title" and "title" in data:
            filled_fields[field] = data["title"][0]

        elif field == "volume/number" and "volume" in data:
            filled_fields[field] = data["volume"]

        elif field == "year" and "license" in data and data["license"]:
            license_date = data["license"][0].get("start", {}).get("date-parts", [[None, None, None]])[0]
            filled_fields["year"] = license_date[0]
            filled_fields["month"] = license_date[1]

        elif field == "journal" and "container-title" in data:
            filled_fields[field] = data["container-title"][0]

        elif field == "pages" and "page" in data:
            filled_fields[field] = data["page"]

        elif field == "doi" and "DOI" in data:
            filled_fields[field] = data["DOI"]

    return filled_fields
