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
        num_string = '0123456789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_basic_pad_right(self):
        num_string = '0123456789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_basic_pad_left(self):
        num_string = ' 0123456789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_basic_pad_both(self):
        num_string = ' 0123456789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_internal(self):
        num_string = '012 345 6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_internal_pad_right(self):
        num_string = '012 345 6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_internal_pad_left(self):
        num_string = ' 012 345 6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_internal_pad_both(self):
        num_string = ' 012 345 6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_internal(self):
        num_string = '01 2345 6789'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_hyphen(self):
        num_string = '012-345-6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_hyphen_pad_right(self):
        num_string = '012-345-6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_hyphen_pad_left(self):
        num_string = ' 012-345-6789'
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_valid_format_hyphen_pad_both(self):
        num_string = ' 012-345-6789 '
        expected = '0123456789'
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_hyphen(self):
        num_string = '01-2345-6789'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_mixed(self):
        num_string = '012 345-6789'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_short(self):
        num_string = '012345678'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_long(self):
        num_string = '01234567890'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_format_letters(self):
        num_string = 'ABCDEFGHIJ'
        expected = ''
        self.assertEqual(expected, normalise_number(num_string))

    def test_is_invalid_wrong_format(self):
        num_string = '123 456 789'
        self.assertFalse(is_valid(num_string))
