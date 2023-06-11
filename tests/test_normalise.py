from unittest import TestCase

from nhs_number import normalise_number


def test_format_basic():
    num_string = "0123456789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_basic_pad_right():
    num_string = "0123456789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_basic_pad_left():
    num_string = " 0123456789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_basic_pad_both():
    num_string = " 0123456789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_internal():
    num_string = "012 345 6789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_internal_pad_right():
    num_string = "012 345 6789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_internal_pad_left():
    num_string = " 012 345 6789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_internal_pad_both():
    num_string = " 012 345 6789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_internal():
    num_string = "01 2345 6789"
    expected = ""
    assert expected == normalise_number(num_string)


def test_format_hyphen():
    num_string = "012-345-6789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_hyphen_pad_right():
    num_string = "012-345-6789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_hyphen_pad_left():
    num_string = " 012-345-6789"
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_hyphen_pad_both():
    num_string = " 012-345-6789 "
    expected = "0123456789"
    assert expected == normalise_number(num_string)


def test_format_hyphen():
    num_string = "01-2345-6789"
    expected = ""
    assert expected == normalise_number(num_string)


def test_format_mixed():
    num_string = "012 345-6789"
    expected = ""
    assert expected == normalise_number(num_string)


def test_format_short():
    num_string = "012345678"
    expected = ""
    assert expected == normalise_number(num_string)


def test_format_long():
    num_string = "01234567890"
    expected = ""
    assert expected == normalise_number(num_string)


def test_format_letters():
    num_string = "ABCDEFGHIJ"
    expected = ""
    assert expected == normalise_number(num_string)
