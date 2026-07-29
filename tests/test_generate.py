from datetime import datetime

import pytest
from nhs_number import REGION_ENGLAND_WALES_IOM, generate, is_valid
from nhs_number.constants import (
    REGION_EIRE,
    REGION_NORTHERN_IRELAND,
    REGION_RESERVED,
    REGION_SCOTLAND,
    REGION_SYNTHETIC,
    REGION_UNALLOCATED,
)
from nhs_number.generate import random_chi_str


def test_create_valid_nhs_number():
    """
    Test that a valid NHS number is generated
    """
    nhs_number = generate()
    assert len(nhs_number) == 1
    assert is_valid(nhs_number[0])


def test_create_invalid_nhs_number():
    """
    Test that one invalid NHS number is generated
    """
    nhs_number = generate(valid=False)
    assert len(nhs_number) == 1
    assert not is_valid(nhs_number[0])


def test_create_large_number_of_valid_nhs_numbers():
    """
    Test that a large number of valid NHS numbers are generated
    """
    nhs_numbers = generate(quantity=10000)
    assert len(nhs_numbers) == 10000
    for nhs_number in nhs_numbers:
        assert is_valid(nhs_number)


def test_random_nhs_numbers():
    """
    Test that random NHS numbers are generated
    """
    nhs_numbers = generate(quantity=100)
    assert len(nhs_numbers) == 100
    for nhs_number in nhs_numbers:
        assert is_valid(nhs_number)


def test_nhs_numbers_for_a_specific_region():
    """
    Test that NHS numbers for a specific region are generated
    """
    nhs_numbers = generate(for_region=REGION_ENGLAND_WALES_IOM)
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert REGION_ENGLAND_WALES_IOM.contains_number(nhs_numbers[0])


def test_fail_when_non_region_supplied():
    """
    Test that we get an error if we supply something other than a Region
    object as the for_region argument
    :return:
    """
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        generate(for_region="REGION_ENGLAND_WALES_IOM")


# ---------------------------------------------------------------------------
# Quantity edge cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_generate_zero_or_negative_quantity_returns_empty(quantity):
    """The while-loop guard ``len(numbers) < quantity`` means zero and
    negative quantities never enter the loop. Pin this so a future rewrite
    can't silently change it (e.g. to "raise ValueError" — which would be a
    breaking change).
    """
    assert generate(quantity=quantity) == []


@pytest.mark.parametrize("quantity", [1, 2, 5, 50])
def test_generate_returns_exact_quantity(quantity):
    assert len(generate(quantity=quantity)) == quantity


# ---------------------------------------------------------------------------
# All Regions covered
# ---------------------------------------------------------------------------

ALL_REGIONS = [
    ("SCOTLAND", REGION_SCOTLAND),
    ("NORTHERN_IRELAND", REGION_NORTHERN_IRELAND),
    ("ENGLAND_WALES_IOM", REGION_ENGLAND_WALES_IOM),
    ("RESERVED", REGION_RESERVED),
    ("EIRE", REGION_EIRE),
    ("UNALLOCATED", REGION_UNALLOCATED),
    ("SYNTHETIC", REGION_SYNTHETIC),
]


@pytest.mark.parametrize(
    "name,region", ALL_REGIONS, ids=[r[0] for r in ALL_REGIONS]
)
def test_generate_valid_for_region_yields_in_region_valid_numbers(
    name, region
):
    """For every Region, a batch of generate(valid=True, for_region=...) must
    produce numbers that are (a) checksum-valid and (b) inside the region.
    """
    numbers = generate(valid=True, for_region=region, quantity=100)
    assert len(numbers) == 100
    for n in numbers:
        assert is_valid(n), f"{n} from region {name} is not checksum-valid"
        assert region.contains_number(n), f"{n} not in region {name}"


@pytest.mark.parametrize(
    "name,region", ALL_REGIONS, ids=[r[0] for r in ALL_REGIONS]
)
def test_generate_invalid_for_region_yields_in_region_invalid_numbers(
    name, region
):
    """generate(valid=False, for_region=...) is an "in-region but checksum-
    invalid" generator — the number should still fall inside the requested
    region's ranges. Pins the cross-cutting invariant that ``valid`` only
    affects the check digit, never the range.
    """
    numbers = generate(valid=False, for_region=region, quantity=100)
    assert len(numbers) == 100
    for n in numbers:
        assert not is_valid(n), f"{n} from region {name} unexpectedly valid"
        assert region.contains_number(n), f"{n} not in region {name}"


# ---------------------------------------------------------------------------
# valid=False at scale
# ---------------------------------------------------------------------------


def test_generate_invalid_at_scale_all_invalid():
    """Pin that generate(valid=False, quantity=N) never sneaks a checksum-
    valid number through. Catches any future bug in the wrong-checksum
    selection loop (e.g. an off-by-one that lets the real checksum slip).
    """
    numbers = generate(valid=False, quantity=1000)
    assert len(numbers) == 1000
    for n in numbers:
        assert not is_valid(n), f"{n} unexpectedly has a valid checksum"


# ---------------------------------------------------------------------------
# Default range is the synthetic / test range - issue #24
# generate() with no region must never return a number that could be a live
# NHS number. This is a breaking change from the previous FULL_RANGE default.
# ---------------------------------------------------------------------------


def test_generate_default_is_synthetic_range():
    for n in generate(quantity=100):
        assert REGION_SYNTHETIC.contains_number(n), (
            f"{n} is not in the synthetic range - generate() must default "
            f"to synthetic numbers"
        )


# ---------------------------------------------------------------------------
# random_chi_str - the internal CHI body generator used for Scotland.
# Produces nine digits (DDMMYY + serial) whose date segment is a real date.
# ---------------------------------------------------------------------------


def test_random_chi_str_is_nine_digits():
    assert len(random_chi_str()) == 9


def test_random_chi_str_starts_with_a_real_date():
    for _ in range(100):
        partial = random_chi_str()
        # strptime raises ValueError on an impossible date; a clean parse over
        # many samples pins that the date segment is always real.
        datetime.strptime(partial[:6], "%d%m%y")
