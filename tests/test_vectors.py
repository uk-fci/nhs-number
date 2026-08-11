"""
Language-agnostic behavioural test vectors, run against this (reference)
implementation.

The vectors in ``tests/vectors/nhs_number_cases.json`` are frozen expected
results. This harness asserts the Python implementation still matches them,
so any behaviour change is caught here. The same JSON is intended to be
consumed verbatim by ports in other languages (e.g. the Rust crate in
``../nhs-number-rs``) so the implementations stay in lockstep.

Python-specific type-robustness cases (None, lists, objects, floats) are not
in the shared vectors - they live in the native test files, because they are
not expressible across languages.
"""

import json
import pathlib

import pytest

import nhs_number
from nhs_number import (
    NhsNumber,
    calculate_checksum,
    is_valid,
    standardise_format,
)
from nhs_number.constants import (
    RANGE_NORTHERN_IRELAND,
    RANGE_NOT_ISSUED_SYNTHETIC,
    RANGE_SCOTLAND,
    RANGE_UNALLOCATED_1,
)

_VECTORS = json.loads(
    (
        pathlib.Path(__file__).parent / "vectors" / "nhs_number_cases.json"
    ).read_text()
)

REGION_MAP = {
    "SCOTLAND": nhs_number.REGION_SCOTLAND,
    "NORTHERN_IRELAND": nhs_number.REGION_NORTHERN_IRELAND,
    "ENGLAND_WALES_IOM": nhs_number.REGION_ENGLAND_WALES_IOM,
    "RESERVED": nhs_number.REGION_RESERVED,
    "EIRE": nhs_number.REGION_EIRE,
    "UNALLOCATED": nhs_number.REGION_UNALLOCATED,
    "SYNTHETIC": nhs_number.REGION_SYNTHETIC,
}

RANGE_MAP = {
    "UNALLOCATED_1": RANGE_UNALLOCATED_1,
    "SCOTLAND": RANGE_SCOTLAND,
    "NORTHERN_IRELAND": RANGE_NORTHERN_IRELAND,
    "SYNTHETIC": RANGE_NOT_ISSUED_SYNTHETIC,
}


def _cases(section):
    return _VECTORS[section]


@pytest.mark.parametrize(
    "case", _cases("calculate_checksum"), ids=lambda c: c["identifier"]
)
def test_checksum_vectors(case):
    assert calculate_checksum(case["identifier"]) == case["checksum"]


@pytest.mark.parametrize(
    "case", _cases("standardise"), ids=lambda c: repr(c["input"])
)
def test_standardise_vectors(case):
    assert standardise_format(case["input"]) == case["output"]


@pytest.mark.parametrize(
    "case", _cases("standardise_from_int"), ids=lambda c: repr(c["input"])
)
def test_standardise_from_int_vectors(case):
    assert standardise_format(case["input"]) == case["output"]


@pytest.mark.parametrize(
    "case", _cases("is_valid"), ids=lambda c: repr(c["input"])
)
def test_is_valid_vectors(case):
    assert is_valid(case["input"]) is case["valid"]


@pytest.mark.parametrize(
    "case",
    _cases("is_valid_for_region"),
    ids=lambda c: f'{c["input"]}-{c["region"]}',
)
def test_is_valid_for_region_vectors(case):
    region = REGION_MAP[case["region"]]
    assert is_valid(case["input"], for_region=region) is case["valid"]


@pytest.mark.parametrize(
    "case",
    _cases("is_valid_with_sex"),
    ids=lambda c: f'{c["input"]}-sex={c["sex"]!r}',
)
def test_is_valid_with_sex_vectors(case):
    if case.get("raises"):
        with pytest.raises(ValueError):
            is_valid(case["input"], sex=case["sex"])
    else:
        assert is_valid(case["input"], sex=case["sex"]) is case["valid"]


@pytest.mark.parametrize(
    "case", _cases("region_of"), ids=lambda c: c["number"]
)
def test_region_of_vectors(case):
    assert NhsNumber(case["number"]).region is REGION_MAP[case["region"]]


@pytest.mark.parametrize(
    "case", _cases("range_boundaries"), ids=lambda c: c["range"]
)
def test_range_boundary_vectors(case):
    rng = RANGE_MAP[case["range"]]
    assert rng.start == case["start"]
    assert rng.end == case["end"]
