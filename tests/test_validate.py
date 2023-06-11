from nhs_number import is_valid, calculate_checksum
from nhs_number import REGION_ENGLAND_WALES_IOM


def test_is_valid_good_one():
    assert is_valid("9876543210") is True


def test_is_valid_bad_one():
    assert is_valid("1234567890") is False


def test_is_valid_good_one_pad_right():
    assert is_valid("9876543210 ") is True


def test_is_invalid_wrong_format():
    assert is_valid("123 456 789") is False


def test_is_valid_randomly_generated():
    assert is_valid("9990000018") is True


def test_is_valid_leading_zero_chi():
    assert is_valid("0607230002") is True


def test_valid_england_wales_number():
    assert is_valid("4000000632", for_region=REGION_ENGLAND_WALES_IOM) is True


def test_invalid_england_wales_number():
    assert is_valid("9876543210", for_region=REGION_ENGLAND_WALES_IOM) is False


def test_checksum_returns_none_if_less_than_nine_digits():
    assert calculate_checksum("123456") is None


def test_checksum_returns_none_if_more_than_nine_digits():
    assert calculate_checksum("12345678901223456") is None
