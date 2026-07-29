import pytest
from nhs_number import NhsNumber
from nhs_number.constants import (
    REGION_EIRE,
    REGION_ENGLAND_WALES_IOM,
    REGION_NORTHERN_IRELAND,
    REGION_RESERVED,
    REGION_SCOTLAND,
    REGION_SYNTHETIC,
    REGION_UNALLOCATED,
    Region,
)


def test_valid_synthetic_nhs_number_details():
    number = NhsNumber("9876543210")

    assert number.nhs_number == "9876543210"
    assert number.identifier_digits == "987654321"
    assert number.check_digit == 0
    assert number.valid
    assert number.calculated_checksum == 0
    assert isinstance(number.region, Region)
    assert "test" in number.region.tags
    assert number.region_comment == (
        "Not to be issued " "(Synthetic/test patients PDS)"
    )


# --- Region coverage: one valid number per region ---------------------------


@pytest.mark.parametrize(
    "nhs_num,expected_region,expected_label_substr",
    [
        ("0101011113", REGION_SCOTLAND, "Scotland"),
        ("3462950622", REGION_NORTHERN_IRELAND, "Northern Ireland"),
        ("4149827702", REGION_ENGLAND_WALES_IOM, "England Wales"),
        ("5726600533", REGION_RESERVED, "Reserved"),
        ("8453035113", REGION_EIRE, "Republic of Ireland"),
        ("0000499927", REGION_UNALLOCATED, "Unallocated"),
        ("9234760735", REGION_SYNTHETIC, "Synthetic"),
    ],
)
def test_nhs_number_region_detection(
    nhs_num, expected_region, expected_label_substr
):
    n = NhsNumber(nhs_num)
    assert n.nhs_number == nhs_num
    assert n.identifier_digits == nhs_num[:-1]
    assert n.check_digit == int(nhs_num[-1])
    assert n.region is expected_region
    assert expected_label_substr in n.region_comment
    # Reserved / Unallocated have valid checksums but are not "issued":
    # validity is purely a checksum property, region is separate.
    assert n.valid is True


# --- Latent bug: out-of-all-ranges input ------------------------------------


def test_nhs_number_below_all_regions_has_no_region():
    """Numbers below FULL_RANGE.start (10) match no region.

    Previously this left `self.region` unset, so any access raised
    AttributeError. After the fix, `region` is None and `region_comment`
    explains why.
    """
    n = NhsNumber("0000000005")
    assert n.region is None
    assert "did not match" in n.region_comment.lower()
    assert n.valid is False


# --- Input parsing: formatted strings ---------------------------------------


@pytest.mark.parametrize(
    "formatted",
    [
        "987 654 3210",
        "987-654-3210",
        "  9876543210  ",
    ],
)
def test_nhs_number_accepts_formatted_input(formatted):
    n = NhsNumber(formatted)
    assert n.identifier_digits == "987654321"
    assert n.check_digit == 0
    assert n.valid is True
    assert n.region is REGION_SYNTHETIC


# --- Input parsing: int -----------------------------------------------------


def test_nhs_number_accepts_int_input():
    n = NhsNumber(9876543210)
    assert n.identifier_digits == "987654321"
    assert n.check_digit == 0
    assert n.valid is True
    assert n.region is REGION_SYNTHETIC


# --- Garbage / empty / None: construct cleanly, valid=False -----------------


@pytest.mark.parametrize(
    "bad_input", ["", "   ", "abcdefghij", "987654321X", None]
)
def test_nhs_number_invalid_input_constructs_cleanly(bad_input):
    n = NhsNumber(bad_input)
    assert n.valid is False
    assert n.region is None
    assert n.identifier_digits == ""
    assert n.check_digit is None
    assert n.calculated_checksum is None
