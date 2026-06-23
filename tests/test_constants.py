"""
Boundary and invariant tests for nhs_number.constants.

These tests pin every documented Range edge so that off-by-one errors and
accidental edits are caught immediately — 100% line/branch coverage on its
own does NOT exercise boundaries.

RANGE_UNALLOCATED_1.end and RANGE_SCOTLAND.start were corrected in the 2.0
release to agree with the module docstring and the CHI specification: the
Scotland CHI range starts at 100_000_000 (the smallest plausible CHI,
01/01/00), not 10_000_000 - see issue #59.
"""
import pytest

from nhs_number.constants import (
    Range,
    Region,
    FULL_RANGE,
    REGIONS,
    RANGE_UNALLOCATED_1,
    RANGE_SCOTLAND,
    RANGE_UNALLOCATED_2,
    RANGE_NORTHERN_IRELAND,
    RANGE_ENGLAND_WALES_IOM_1,
    RANGE_RESERVED,
    RANGE_ENGLAND_WALES_IOM_2,
    RANGE_EIRE,
    RANGE_UNALLOCATED_3,
    RANGE_NOT_ISSUED_SYNTHETIC,
    REGION_SCOTLAND,
    REGION_NORTHERN_IRELAND,
    REGION_ENGLAND_WALES_IOM,
    REGION_RESERVED,
    REGION_EIRE,
    REGION_UNALLOCATED,
    REGION_SYNTHETIC,
    REGION_ENGLAND,
    REGION_WALES,
    REGION_IOM,
)


# (name, range_obj, start, end) — order matches the documented sequence in
# constants.py so the non-overlap test below sweeps boundaries in order.
ALL_RANGES = [
    ("UNALLOCATED_1",       RANGE_UNALLOCATED_1,        10,            99_999_999),
    ("SCOTLAND",            RANGE_SCOTLAND,             100_000_000,   3_112_999_999),
    ("UNALLOCATED_2",       RANGE_UNALLOCATED_2,        3_113_000_000, 3_199_999_999),
    ("NORTHERN_IRELAND",    RANGE_NORTHERN_IRELAND,     3_200_000_000, 3_999_999_999),
    ("ENGLAND_WALES_IOM_1", RANGE_ENGLAND_WALES_IOM_1,  4_000_000_000, 4_999_999_999),
    ("RESERVED",            RANGE_RESERVED,             5_000_000_000, 5_999_999_999),
    ("ENGLAND_WALES_IOM_2", RANGE_ENGLAND_WALES_IOM_2,  6_000_000_000, 7_999_999_999),
    ("EIRE",                RANGE_EIRE,                 8_000_000_000, 8_599_999_999),
    ("UNALLOCATED_3",       RANGE_UNALLOCATED_3,        8_600_000_000, 8_999_999_999),
    ("SYNTHETIC",           RANGE_NOT_ISSUED_SYNTHETIC, 9_000_000_000, 9_999_999_999),
]

_RANGE_IDS = [r[0] for r in ALL_RANGES]


# ---------------------------------------------------------------------------
# Pinned start/end values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,rng,start,end", ALL_RANGES, ids=_RANGE_IDS)
def test_range_pinned_boundaries(name, rng, start, end):
    """Pin the start/end of every Range so accidental edits are caught."""
    assert rng.start == start, f"{name}.start drifted from pinned value"
    assert rng.end == end, f"{name}.end drifted from pinned value"


# ---------------------------------------------------------------------------
# Inclusivity at boundaries
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,rng,start,end", ALL_RANGES, ids=_RANGE_IDS)
def test_range_contains_at_boundaries(name, rng, start, end):
    """Per the constants.py header: ranges are INCLUSIVE of start AND end."""
    assert rng.contains_number(start) is True
    assert rng.contains_number(end) is True


@pytest.mark.parametrize("name,rng,start,end", ALL_RANGES, ids=_RANGE_IDS)
def test_range_excludes_just_outside_boundaries(name, rng, start, end):
    """Off-by-one safety: start-1 and end+1 must be outside the range."""
    assert rng.contains_number(start - 1) is False
    assert rng.contains_number(end + 1) is False


# ---------------------------------------------------------------------------
# Range.contains_number accepts both int and string forms
# ---------------------------------------------------------------------------

def test_range_contains_number_accepts_int_and_string():
    """Range.contains_number coerces with int(); both forms must agree."""
    assert RANGE_NORTHERN_IRELAND.contains_number("3500000000") is True
    assert RANGE_NORTHERN_IRELAND.contains_number(3_500_000_000) is True
    assert RANGE_NORTHERN_IRELAND.contains_number("9000000000") is False
    assert RANGE_NORTHERN_IRELAND.contains_number(9_000_000_000) is False


# ---------------------------------------------------------------------------
# FULL_RANGE
# ---------------------------------------------------------------------------

def test_full_range_pinned_and_inclusive():
    assert FULL_RANGE.start == 10
    assert FULL_RANGE.end == 9_999_999_999
    assert FULL_RANGE.contains_number(FULL_RANGE.start) is True
    assert FULL_RANGE.contains_number(FULL_RANGE.end) is True
    assert FULL_RANGE.contains_number(FULL_RANGE.start - 1) is False
    assert FULL_RANGE.contains_number(FULL_RANGE.end + 1) is False


# ---------------------------------------------------------------------------
# Region ↔ Range composition
# ---------------------------------------------------------------------------

# Map each Range to the single Region that should contain its endpoints.
RANGE_TO_REGION = [
    ("UNALLOCATED_1",       RANGE_UNALLOCATED_1,        REGION_UNALLOCATED),
    ("SCOTLAND",            RANGE_SCOTLAND,             REGION_SCOTLAND),
    ("UNALLOCATED_2",       RANGE_UNALLOCATED_2,        REGION_UNALLOCATED),
    ("NORTHERN_IRELAND",    RANGE_NORTHERN_IRELAND,     REGION_NORTHERN_IRELAND),
    ("ENGLAND_WALES_IOM_1", RANGE_ENGLAND_WALES_IOM_1,  REGION_ENGLAND_WALES_IOM),
    ("RESERVED",            RANGE_RESERVED,             REGION_RESERVED),
    ("ENGLAND_WALES_IOM_2", RANGE_ENGLAND_WALES_IOM_2,  REGION_ENGLAND_WALES_IOM),
    ("EIRE",                RANGE_EIRE,                 REGION_EIRE),
    ("UNALLOCATED_3",       RANGE_UNALLOCATED_3,        REGION_UNALLOCATED),
    ("SYNTHETIC",           RANGE_NOT_ISSUED_SYNTHETIC, REGION_SYNTHETIC),
]


@pytest.mark.parametrize("name,rng,region", RANGE_TO_REGION, ids=[r[0] for r in RANGE_TO_REGION])
def test_region_contains_each_of_its_ranges_endpoints(name, rng, region):
    assert region.contains_number(rng.start) is True
    assert region.contains_number(rng.end) is True


# ---------------------------------------------------------------------------
# Non-overlap invariant: every boundary belongs to exactly one Region
# ---------------------------------------------------------------------------

ALL_REGIONS = [
    REGION_UNALLOCATED,
    REGION_SCOTLAND,
    REGION_NORTHERN_IRELAND,
    REGION_ENGLAND_WALES_IOM,
    REGION_RESERVED,
    REGION_EIRE,
    REGION_SYNTHETIC,
]


def _matching_regions(number):
    return [r for r in ALL_REGIONS if r.contains_number(number)]


@pytest.mark.parametrize("name,rng,start,end", ALL_RANGES, ids=_RANGE_IDS)
def test_regions_are_mutually_exclusive_at_boundaries(name, rng, start, end):
    """Each Range start/end belongs to exactly one Region (no overlap)."""
    starts_match = _matching_regions(start)
    ends_match = _matching_regions(end)
    assert len(starts_match) == 1, (
        f"{name}.start ({start}) matches multiple regions: "
        f"{[r.label for r in starts_match]}"
    )
    assert len(ends_match) == 1, (
        f"{name}.end ({end}) matches multiple regions: "
        f"{[r.label for r in ends_match]}"
    )


def test_below_full_range_matches_no_region():
    for value in (0, 1, 9):
        assert _matching_regions(value) == [], (
            f"value {value} below FULL_RANGE.start matched a region"
        )


def test_above_full_range_matches_no_region():
    for value in (10_000_000_000, 99_999_999_999):
        assert _matching_regions(value) == [], (
            f"value {value} above FULL_RANGE.end matched a region"
        )


# ---------------------------------------------------------------------------
# Region aliases
# ---------------------------------------------------------------------------

def test_england_wales_iom_aliases_are_the_same_object():
    """REGION_ENGLAND, REGION_WALES, REGION_IOM are aliases for the combined
    region. Pin the identity so a future split (e.g. a separate REGION_WALES)
    is a deliberate, reviewed change rather than an accidental one.
    """
    assert REGION_ENGLAND is REGION_ENGLAND_WALES_IOM
    assert REGION_WALES is REGION_ENGLAND_WALES_IOM
    assert REGION_IOM is REGION_ENGLAND_WALES_IOM


# ---------------------------------------------------------------------------
# REGIONS dict — public surface
# ---------------------------------------------------------------------------

def test_regions_dict_keys():
    """NhsNumber iterates REGIONS by these handles; pin them as a public API."""
    assert set(REGIONS.keys()) == {
        "UNALLOCATED",
        "SCOTLAND",
        "NORTHERN_IRELAND",
        "ENGLAND_WALES_IOM",
        "RESERVED",
        "EIRE",
        "SYNTHETIC",
    }


# ---------------------------------------------------------------------------
# Direct construction of Range and Region (no implicit dependency on globals)
# ---------------------------------------------------------------------------

def test_range_constructor_attributes_and_contains():
    r = Range(start=100, end=200, label="test range")
    assert r.start == 100
    assert r.end == 200
    assert r.label == "test range"
    assert r.contains_number(100) is True
    assert r.contains_number(200) is True
    assert r.contains_number(99) is False
    assert r.contains_number(201) is False


def test_region_contains_across_multiple_ranges_with_a_gap():
    """A Region with two Ranges with a gap between them must NOT match values
    in the gap — pins that Region.contains_number iterates ranges correctly.
    """
    r1 = Range(start=10, end=20, label="r1")
    r2 = Range(start=100, end=110, label="r2")
    region = Region(label="composite", tags=["t"], ranges=[r1, r2])

    assert region.label == "composite"
    assert region.tags == ["t"]
    assert region.ranges == [r1, r2]

    # Inside either range
    assert region.contains_number(15) is True
    assert region.contains_number(105) is True
    # In the gap
    assert region.contains_number(50) is False
    # Outside both
    assert region.contains_number(9) is False
    assert region.contains_number(111) is False


def test_region_with_no_ranges_contains_nothing():
    region = Region(label="empty", tags=[], ranges=[])
    assert region.contains_number(0) is False
    assert region.contains_number(5_000_000_000) is False
