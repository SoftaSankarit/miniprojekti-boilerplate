import unittest
from util import validate_year, validate_text_field, UserInputError

class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_year_does_not_raise_error(self):
        validate_year("2020")

    def test_year_must_be_between_1_and_2024(self):
        with self.assertRaises(UserInputError):
            validate_year("0")

        with self.assertRaises(UserInputError):
            validate_year("200000000")

    def test_year_must_be_number(self):
        with self.assertRaises(UserInputError):
            validate_year("Kaksituhattakaksikymmentä")

    def test_valid_text_does_not_raise_error(self):
        validate_text_field("Toimiva teksti")

    def test_too_short_or_long_textfield_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_text_field("M")

        with self.assertRaises(UserInputError):
            validate_text_field("Todellaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa pitkä teksti")
