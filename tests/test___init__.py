from unittest import TestCase

from nhs_number import is_valid, normalise_number


class Test(TestCase):

    def test_is_valid_good_one(self):
        self.assertTrue(is_valid('9876543210'))

    def test_is_valid_bad_one(self):
        self.assertFalse(is_valid('1234567890'))

    def test_is_valid_good_one_pad_right(self):
        self.assertTrue(is_valid('9876543210 '))

    def test_is_valid_format_basic(self):
        input = '0123456789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_basic_pad_right(self):
        input = '0123456789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_basic_pad_left(self):
        input = ' 0123456789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_basic_pad_both(self):
        input = ' 0123456789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_internal(self):
        input = '012 345 6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_internal_pad_right(self):
        input = '012 345 6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_internal_pad_left(self):
        input = ' 012 345 6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_internal_pad_both(self):
        input = ' 012 345 6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_invalid_format_internal(self):
        input = '01 2345 6789'
        expected = ''
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_hyphen(self):
        input = '012-345-6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_hyphen_pad_right(self):
        input = '012-345-6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_hyphen_pad_left(self):
        input = ' 012-345-6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_valid_format_hyphen_pad_both(self):
        input = ' 012-345-6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(input))

    def test_is_invalid_format_hyphen(self):
        input = '01-2345-6789'
        expected = ''
        self.assertEqual(expected, normalise_number(input))

    def test_is_invalid_format_mixed(self):
        input = '012 345-6789'
        expected = ''
        self.assertEqual(expected, normalise_number(input))
