import unittest
from util import validate_year, UserInputError

class TestTodoValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_year_does_not_raise_error(self):
        validate_year("2020")

    def test_too_short_or_long_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_year("0")

        with self.assertRaises(UserInputError):
            validate_year("200000000")
