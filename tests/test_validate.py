import pytest

from nhs_number import is_valid, calculate_checksum, calculate_checksum_mod10
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
    ("SCOTLAND", REGION_SCOTLAND, "0101011113", "9876543210"),
    ("NORTHERN_IRELAND", REGION_NORTHERN_IRELAND, "3462950622", "9876543210"),
    ("ENGLAND_WALES", REGION_ENGLAND_WALES_IOM, "4149827702", "9876543210"),
    ("RESERVED", REGION_RESERVED, "5726600533", "9876543210"),
    ("EIRE", REGION_EIRE, "8453035113", "9876543210"),
    ("UNALLOCATED", REGION_UNALLOCATED, "0000499927", "9876543210"),
    ("SYNTHETIC", REGION_SYNTHETIC, "9234760735", "0101011113"),
]


@pytest.mark.parametrize(
    "name,region,in_range,out_of_range",
    REGION_CASES,
    ids=[c[0] for c in REGION_CASES],
)
def test_is_valid_for_region_accepts_in_range_numbers(
    name, region, in_range, out_of_range
):
    assert is_valid(in_range, for_region=region) is True


@pytest.mark.parametrize(
    "name,region,in_range,out_of_range",
    REGION_CASES,
    ids=[c[0] for c in REGION_CASES],
)
def test_is_valid_for_region_rejects_out_of_range_numbers(
    name, region, in_range, out_of_range
):
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
def test_is_valid_rejects_every_check_digit_when_real_checksum_is_10(
    check_digit,
):
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


@pytest.mark.parametrize(
    "bad_input",
    [
        None,
        "",
        "   ",
        "abc",
        "987654321X",
        3.14,
        -1.0,
        -1,
        -1234567890,
        99_999_999_999,  # > 10 digits, zfill is a no-op so format regex fails
        [],
        {},
        object(),
        True,
        False,
    ],
)
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


# From August 2026, CHI numbers (Scotland) are issued with a modulus 10
# check digit as well as modulus 11. These are the worked examples from
# Public Health Scotland's own implementation (phsmethods, R/chi_check.R),
# which is the source of truth for the algorithm. See issue #107.


def test_mod10_checksum_matches_phs_examples():
    # "0101201234" is valid under mod 10 only; "0101011237" passes both.
    assert calculate_checksum_mod10("010120123") == 4
    assert calculate_checksum_mod10("010101123") == 7


def test_mod10_checksum_returns_none_for_wrong_lengths():
    assert calculate_checksum_mod10("12345") is None
    assert calculate_checksum_mod10("1234567890123") is None


def test_chi_number_valid_under_mod10_only():
    # Mod 11 gives 0 for this identifier, so this number was rejected before
    # mod 10 support: it is PHS's own example of a valid CHI.
    assert is_valid("0101201234") is True


def test_chi_number_valid_under_mod11_still_valid():
    assert is_valid("0101011237") is True


def test_number_failing_both_checks_stays_invalid():
    # PHS's worked example of an invalid checksum: passes neither mod 11
    # nor mod 10 (and is outside the CHI range in any case).
    assert is_valid("3213201234") is False


def test_mod10_is_not_applied_outside_the_chi_range():
    # "4000000630": the mod 10 calculation gives 0 and matches the check
    # digit, but this is an England/Wales range number, where only the
    # mod 11 check digit (2 here) applies.
    assert is_valid("4000000630") is False


def test_chi_mod10_still_requires_a_real_date():
    # "0113201230" passes the mod 10 check but 01/13/20 is not a real date,
    # so it is rejected by the CHI date-of-birth rule.
    assert is_valid("0113201230") is False


def test_check_mod10_false_restores_v2_behaviour():
    # "0101201234" passes the mod 10 check only: with check_mod10=False the
    # number is rejected again, restoring the version 2.x behaviour.
    assert is_valid("0101201234") is True
    assert is_valid("0101201234", check_mod10=False) is False


def test_check_mod10_false_still_accepts_mod11_chi():
    # "0101011237" passes both checks, so it stays valid with the flag off.
    assert is_valid("0101011237", check_mod10=False) is True
