from nhs_number import is_valid, calculate_checksum
from nhs_number import REGION_ENGLAND_WALES_IOM, REGION_SCOTLAND
from nhs_number import Sex
import pytest


def test_string_is_valid_good_one():
    assert is_valid("9876543210") is True


def test_int_is_valid_good_one():
    assert is_valid(9876543210) is True


def test_string_is_valid_bad_one():
    assert is_valid("1234567890") is False


def test_int_is_valid_bad_one():
    assert is_valid(1234567890) is False


def test_is_valid_good_one_pad_right():
    assert is_valid("9876543210 ") is True


def test_is_invalid_wrong_format():
    assert is_valid("123 456 789") is False


def test_is_valid_randomly_generated():
    assert is_valid("9990000018") is True


def test_string_is_valid_leading_zero_chi():
    assert is_valid("0607230002") is True


def test_int_is_valid_leading_zero_chi():
    assert is_valid(607230002) is True


def test_chi_impossible_date():
    assert is_valid("0113011113", for_region=REGION_SCOTLAND) is False


def test_chi_impossible_date_no_region():
    assert is_valid("0113011113") is False


def test_chi_correct_sex_male():
    assert is_valid("0101011113", sex=Sex.MALE) is True


def test_chi_incorrect_sex_male():
    assert is_valid("0101011121", sex=Sex.MALE) is False


def test_chi_correct_sex_female():
    assert is_valid("0101011121", sex=Sex.FEMALE) is True


def test_chi_incorrect_sex_female():
    assert is_valid("0101011113", sex=Sex.FEMALE) is False


def test_nhs_pass_when_sex_supplied():
    assert is_valid("4000000632", sex=Sex.FEMALE) is True


def test_warning_if_not_sex_type_given():
    with pytest.warns(UserWarning, match="Sex argument must be of type Sex"):
        is_valid("0101011113", sex="female")


def test_valid_england_wales_number():
    assert is_valid("4000000632", for_region=REGION_ENGLAND_WALES_IOM) is True


def test_invalid_england_wales_number():
    assert is_valid("9876543210", for_region=REGION_ENGLAND_WALES_IOM) is False


def test_checksum_returns_none_if_less_than_nine_digits():
    assert calculate_checksum("123456") is None


def test_checksum_returns_none_if_more_than_nine_digits():
    assert calculate_checksum("12345678901223456") is None
