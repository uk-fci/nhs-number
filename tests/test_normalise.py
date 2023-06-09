from unittest import TestCase

from nhs_number import normalise_number


class NormalisationTests(TestCase):
    def test_format_basic(self):
        num_string = "0123456789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_basic_pad_right(self):
        num_string = "0123456789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_basic_pad_left(self):
        num_string = " 0123456789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_basic_pad_both(self):
        num_string = " 0123456789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_internal(self):
        num_string = "012 345 6789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_internal_pad_right(self):
        num_string = "012 345 6789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_internal_pad_left(self):
        num_string = " 012 345 6789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_internal_pad_both(self):
        num_string = " 012 345 6789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_internal(self):
        num_string = "01 2345 6789"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_hyphen(self):
        num_string = "012-345-6789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_hyphen_pad_right(self):
        num_string = "012-345-6789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_hyphen_pad_left(self):
        num_string = " 012-345-6789"
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_hyphen_pad_both(self):
        num_string = " 012-345-6789 "
        expected = "0123456789"
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_hyphen(self):
        num_string = "01-2345-6789"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_mixed(self):
        num_string = "012 345-6789"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_short(self):
        num_string = "012345678"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_long(self):
        num_string = "01234567890"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))

    def test_format_letters(self):
        num_string = "ABCDEFGHIJ"
        expected = ""
        self.assertEqual(expected, normalise_number(num_string))
