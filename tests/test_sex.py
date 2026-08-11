"""
Tests for the sex-parity check on Scotland CHI numbers - see issue #66.

Fixtures: 0101011113 (01/01/01, valid checksum, 9th digit '1' - odd, so
male by parity) and 0101011121 (same date, 9th digit '2' - even, so female
by parity). Both are valid CHI numbers with no sex check applied.
"""

import pytest

from nhs_number import NhsNumber, REGION_ENGLAND_WALES_IOM, is_valid

CHI_MALE = "0101011113"  # 9th digit odd
CHI_FEMALE = "0101011121"  # 9th digit even
NON_CHI = "4000000632"  # valid, England/Wales/IoM - no parity digit at all


# ---------------------------------------------------------------------------
# The core parity check
# ---------------------------------------------------------------------------


def test_matching_sex_is_valid():
    assert is_valid(CHI_MALE, sex="male") is True
    assert is_valid(CHI_FEMALE, sex="female") is True


def test_mismatched_sex_is_invalid():
    assert is_valid(CHI_MALE, sex="female") is False
    assert is_valid(CHI_FEMALE, sex="male") is False


def test_sex_omitted_is_unaffected():
    assert is_valid(CHI_MALE) is True
    assert is_valid(CHI_FEMALE) is True


# ---------------------------------------------------------------------------
# Inert cases - the "one rule": sex can only ever reduce validity by
# disagreeing with an actual parity digit on an actual CHI number.
# ---------------------------------------------------------------------------


def test_sex_ignored_for_non_chi_numbers():
    # A mismatch would fail this if the number were Scotland-range, but it
    # is not, so sex has no effect either way.
    assert is_valid(NON_CHI, sex="male") is True
    assert is_valid(NON_CHI, sex="female") is True


def test_sex_ignored_for_non_chi_numbers_with_region():
    assert (
        is_valid(NON_CHI, for_region=REGION_ENGLAND_WALES_IOM, sex="female")
        is True
    )


@pytest.mark.parametrize("indeterminate_value", ["indeterminate", "not_known"])
def test_indeterminate_words_are_inert(indeterminate_value):
    assert is_valid(CHI_MALE, sex=indeterminate_value) is True
    assert is_valid(CHI_FEMALE, sex=indeterminate_value) is True


@pytest.mark.parametrize("inert_code", [9, 0, "X", "x"])
def test_inert_numeric_and_letter_codes(inert_code):
    assert is_valid(CHI_MALE, sex=inert_code) is True
    assert is_valid(CHI_FEMALE, sex=inert_code) is True


# ---------------------------------------------------------------------------
# NHS numeric codes for male/female - stable across every NHS sex/gender
# code list (retired PERSON GENDER CODE and current PERSON STATED GENDER
# CODE / PERSON PHENOTYPIC SEX all agree 1=Male, 2=Female).
# ---------------------------------------------------------------------------


def test_numeric_codes_match_word_behaviour():
    assert is_valid(CHI_MALE, sex=1) is True
    assert is_valid(CHI_MALE, sex=2) is False
    assert is_valid(CHI_FEMALE, sex=2) is True
    assert is_valid(CHI_FEMALE, sex=1) is False


# ---------------------------------------------------------------------------
# Case insensitivity and whitespace
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["male", "Male", "MALE", " male ", "male\t"])
def test_words_are_case_and_whitespace_insensitive(value):
    assert is_valid(CHI_MALE, sex=value) is True


# ---------------------------------------------------------------------------
# Unrecognised values raise, matching the for_region convention
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    ["woman", "man", "M", "F", "", "  ", 3, 100, -1, 1.0, [], {}, object()],
)
def test_unrecognised_sex_value_raises(bad_value):
    with pytest.raises(ValueError):
        is_valid(CHI_MALE, sex=bad_value)


@pytest.mark.parametrize("bad_bool", [True, False])
def test_bool_is_rejected_even_though_it_is_an_int_subclass(bad_bool):
    with pytest.raises(ValueError):
        is_valid(CHI_MALE, sex=bad_bool)


def test_unrecognised_sex_value_raises_even_for_invalid_number():
    """A bad `sex` is a caller error and should surface regardless of
    whether nhs_number itself is well-formed."""
    with pytest.raises(ValueError):
        is_valid("garbage", sex="woman")


def test_unrecognised_sex_value_raises_even_when_number_is_not_chi():
    with pytest.raises(ValueError):
        is_valid(NON_CHI, sex="woman")


# ---------------------------------------------------------------------------
# NhsNumber threads sex through to is_valid()
# ---------------------------------------------------------------------------


def test_nhs_number_valid_reflects_sex_match():
    assert NhsNumber(CHI_MALE, sex="male").valid is True
    assert NhsNumber(CHI_MALE, sex="female").valid is False


def test_nhs_number_sex_default_is_unaffected():
    assert NhsNumber(CHI_MALE).valid is True


def test_nhs_number_raises_for_bad_sex_even_with_garbage_number():
    with pytest.raises(ValueError):
        NhsNumber("not a number at all", sex="woman")
