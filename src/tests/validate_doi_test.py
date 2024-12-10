import unittest
from util import find_crossref_type, fill_doi_fields

class TestFindCrossrefType(unittest.TestCase):
    def test_known_crossref_type(self):
        self.assertEqual(find_crossref_type({"type": "journal-article"}), "article")
        self.assertEqual(find_crossref_type({"type": "book"}), "book")
        self.assertEqual(find_crossref_type({"type": "book-chapter"}), "inbook")

    def test_unknown_crossref_type(self):
        self.assertIsNone(find_crossref_type({"type": "random"}))

    def test_missing_type_key(self):
        self.assertEqual(find_crossref_type({}), None)

class TestFillDoiFields(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "author": [
                {"given": "John", "family": "Doe"},
                {"given": "Jane", "family": "Smith"}
            ],
            "title": ["Sample Title"],
            "volume": "42",
            "license": [{"start": {"date-parts": [[2023, 5, 15]]}}],
            "container-title": ["Sample Journal"],
            "page": "100-200",
            "DOI": "10.1234/sample.doi"
        }

    def test_fill_doi_fields_with_complete_data(self):
        filled = fill_doi_fields("article", self.sample_data)
        self.assertEqual(filled["author"], "John Doe, et al.")
        self.assertEqual(filled["title"], "Sample Title")
        self.assertEqual(filled["volume"], "42")
        self.assertEqual(filled["year"], 2023)
        self.assertEqual(filled["month"], 5)
        self.assertEqual(filled["journal"], "Sample Journal")
        self.assertEqual(filled["pages"], "100-200")
        self.assertEqual(filled["doi"], "10.1234/sample.doi")

    def test_fill_doi_fields_with_partial_data(self):
        partial_data = {
            "author": [{"given": "John", "family": "Doe"}],
            "title": ["Partial Title"]
        }
        filled = fill_doi_fields("book", partial_data)
        self.assertEqual(filled["author"], "John Doe")
        self.assertEqual(filled["title"], "Partial Title")
        self.assertNotIn("year", filled)
