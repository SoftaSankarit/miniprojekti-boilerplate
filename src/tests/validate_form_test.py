import unittest
from util import validate_form, UserInputError

class TestValidateForm(unittest.TestCase):
    def setUp(self):
        self.valid_article_fields = {
            "author": "Valid Author",
            "title": "Valid Title",
            "journal": "Valid Journal",
            "year": "2020",
        }
        self.valid_book_fields = {
            "author": "Valid Author",
            "title": "Valid Book Title",
            "publisher": "Valid Publisher",
            "year": "2020",
        }
        self.valid_misc_fields = {
            "note": "Optional field test",
        }

    def test_validate_form_success_article(self):
        validate_form("article", self.valid_article_fields)

    def test_validate_form_success_book(self):
        validate_form("book", self.valid_book_fields)

    def test_optional_field_not_in_required(self):
        fields = self.valid_misc_fields.copy()
        fields["note"] = "This is a valid optional field"
        validate_form("misc", fields)

    def test_missing_required_field(self):
        fields = self.valid_article_fields.copy()
        fields["author"] = None
        with self.assertRaises(UserInputError) as context:
            validate_form("article", fields)
        self.assertEqual(str(context.exception), "Syöte ei saa olla tyhjä.")

    def test_invalid_year(self):
        fields = self.valid_article_fields.copy()
        fields["year"] = "abcd"
        with self.assertRaises(UserInputError) as context:
            validate_form("article", fields)
        self.assertEqual(str(context.exception), "Vuoden pitää olla numero.")

    def test_text_field_too_long(self):
        fields = self.valid_article_fields.copy()
        fields["author"] = "A"*151
        with self.assertRaises(UserInputError) as context:
            validate_form("article", fields)
        self.assertEqual(str(context.exception), "Syötteen pitää olla lyhyempi kuin 150 merkkiä.")

    def test_text_field_too_short(self):
        fields = self.valid_article_fields.copy()
        fields["title"] = "A"
        with self.assertRaises(UserInputError) as context:
            validate_form("article", fields)
        self.assertEqual(str(context.exception), "Syötteen pitää olla pidempi kuin 3 merkkiä.")

    def test_validate_form_publisher_field(self):
        fields = self.valid_book_fields.copy()
        fields["publisher"] = "P"
        with self.assertRaises(UserInputError) as context:
            validate_form("book", fields)
        self.assertEqual(str(context.exception), "Syötteen pitää olla pidempi kuin 3 merkkiä.")
