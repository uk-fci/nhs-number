import pytest

from nhs_number import is_valid, calculate_checksum
from nhs_number import REGION_ENGLAND_WALES_IOM
from nhs_number.constants import (
    REGION_SCOTLAND,
    REGION_NORTHERN_IRELAND,
    REGION_RESERVED,
    REGION_EIRE,
    REGION_UNALLOCATED,
    REGION_SYNTHETIC,
)


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


def test_valid_england_wales_number():
    assert is_valid("4000000632", for_region=REGION_ENGLAND_WALES_IOM) is True


def test_invalid_england_wales_number():
    assert is_valid("9876543210", for_region=REGION_ENGLAND_WALES_IOM) is False


def test_checksum_returns_none_if_less_than_nine_digits():
    assert calculate_checksum("123456") is None


def test_checksum_returns_none_if_more_than_nine_digits():
    assert calculate_checksum("12345678901223456") is None


# ---------------------------------------------------------------------------
# is_valid(..., for_region=...) across every Region
# ---------------------------------------------------------------------------

# (region, in-range valid checksum, out-of-range valid checksum)
# - in-range: a valid-checksum NHS number that falls inside ``region``
# - out-of-range: a different valid-checksum NHS number that falls OUTSIDE
#   ``region`` (used to assert for_region rejects numbers outside the region
#   even though their checksum is fine)
REGION_CASES = [
    ("SCOTLAND",         REGION_SCOTLAND,         "0101011113", "9876543210"),
    ("NORTHERN_IRELAND", REGION_NORTHERN_IRELAND, "3462950622", "9876543210"),
    ("ENGLAND_WALES",    REGION_ENGLAND_WALES_IOM, "4149827702", "9876543210"),
    ("RESERVED",         REGION_RESERVED,         "5726600533", "9876543210"),
    ("EIRE",             REGION_EIRE,             "8453035113", "9876543210"),
    ("UNALLOCATED",      REGION_UNALLOCATED,      "0000499927", "9876543210"),
    ("SYNTHETIC",        REGION_SYNTHETIC,        "9234760735", "0101011113"),
]


@pytest.mark.parametrize("name,region,in_range,out_of_range", REGION_CASES,
                         ids=[c[0] for c in REGION_CASES])
def test_is_valid_for_region_accepts_in_range_numbers(name, region, in_range, out_of_range):
    assert is_valid(in_range, for_region=region) is True


@pytest.mark.parametrize("name,region,in_range,out_of_range", REGION_CASES,
                         ids=[c[0] for c in REGION_CASES])
def test_is_valid_for_region_rejects_out_of_range_numbers(name, region, in_range, out_of_range):
    """Even with a valid checksum, a number outside ``region`` must be False."""
    # Sanity: the out-of-range fixture itself must have a valid checksum
    # (otherwise the test would pass for the wrong reason).
    assert is_valid(out_of_range) is True
    assert is_valid(out_of_range, for_region=region) is False


# ---------------------------------------------------------------------------
# CHI (Scotland) date-of-birth validation - issue #25
# A CHI number encodes the date of birth in its first 6 digits as DDMMYY.
# A number in the Scotland CHI range whose date segment is not a real
# calendar date is invalid, regardless of checksum. Applied by default.
# ---------------------------------------------------------------------------

def test_chi_valid_date_is_accepted():
    # 01/01/01 (1 Jan 2001), valid checksum, in the Scotland CHI range
    assert is_valid("0101011113") is True


def test_chi_impossible_date_rejected_with_region():
    # 01/13/01 - month 13 - checksum is valid, so only the date can reject it
    assert is_valid("0113011113", for_region=REGION_SCOTLAND) is False


def test_chi_impossible_date_rejected_by_default():
    # The CHI date check applies to any number in the Scotland range, even
    # without an explicit for_region.
    assert is_valid("0113011113") is False


# ---------------------------------------------------------------------------
# Checksum == 10 (special case noted in validate.py)
# ---------------------------------------------------------------------------

def test_calculate_checksum_can_return_10():
    """For some 9-digit identifiers the formula yields 10. validate.py
    relies on the equality check (10 != any single digit) to mark such
    numbers invalid. Pin a known identifier that produces this value so the
    rest of the family below makes sense.

    Identifier "000000006" has weighted sum 6*2 = 12; 12 % 11 = 1; checksum
    = 11 - 1 = 10.
    """
    assert calculate_checksum("000000006") == 10


@pytest.mark.parametrize("check_digit", list(range(10)))
def test_is_valid_rejects_every_check_digit_when_real_checksum_is_10(check_digit):
    """When the real checksum is 10, NO single-digit check digit can match,
    so every candidate full number must be rejected.

    This pins the comment in validate.py:75-77 ("a checksum of 10 is
    invalid... the equality check will catch that"). If the formula is ever
    rewritten and accidentally returns a different value (e.g. 0) for
    sum % 11 == 1, this whole family will flip and be caught.
    """
    candidate = "000000006" + str(check_digit)
    assert is_valid(candidate) is False


# ---------------------------------------------------------------------------
# Input-type robustness — is_valid never raises
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_input", [
    None,
    "",
    "   ",
    "abc",
    "987654321X",
    3.14,
    -1.0,
    -1,
    -1234567890,
    99_999_999_999,    # > 10 digits, zfill is a no-op so format regex fails
    [],
    {},
    object(),
    True,
    False,
])
def test_is_valid_returns_false_for_unparseable_input(bad_input):
    """is_valid must never raise — anything it can't standardise is False."""
    assert is_valid(bad_input) is False


def test_is_valid_zero_int_pinned_behaviour():
    """``is_valid(0)`` returns True.

    Rationale: 0 zfills to "0000000000", whose checksum is 0 (matching the
    last digit). is_valid() without for_region only validates the checksum,
    not whether the number is in any issuable range — so this is the
    documented behaviour.

    If you want to also reject below-FULL_RANGE numbers, pass
    ``for_region=REGION_<X>`` or use ``NhsNumber`` and inspect ``.region``.
    """
    assert is_valid(0) is True
    # The "is in any region" question is a separate concern:
    assert is_valid(0, for_region=REGION_SYNTHETIC) is False
    assert is_valid(0, for_region=REGION_UNALLOCATED) is False


def test_is_valid_for_region_returns_false_for_unparseable_input():
    """When for_region is set, garbage input must still return False (not
    raise) — pin this via None and a few representative bad values.
    """
    for bad in (None, "", "garbage", 3.14, []):
        assert is_valid(bad, for_region=REGION_ENGLAND_WALES_IOM) is False
