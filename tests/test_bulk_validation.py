"""
Bulk validation of 909,090 known-valid synthetic NHS numbers.

The dataset lives at tests/local-test-data/ and is committed to the repo
deliberately (see commit 713268d) but excluded from the published package
via pyproject.toml's `exclude` rule, so PyPI consumers don't download it.

If someone runs the suite without the dataset present (e.g. a sparse
checkout), the test skips with a pointer rather than failing — but the
default expectation is that it runs.
"""

import csv
import pathlib
import sys

import pytest
from nhs_number import is_valid

# The csv module's field size limit is a C long. On Windows that is 32-bit,
# so sys.maxsize overflows it and raises at import time (see issue #80). Fall
# back to the largest value a 32-bit signed long can hold.
try:
    csv.field_size_limit(sys.maxsize)
except OverflowError:
    csv.field_size_limit(2**31 - 1)

DATA_DIR = pathlib.Path(__file__).parent / "local-test-data"
DATA_FILE = DATA_DIR / "testdata-909090-valid-nhs-numbers.csv"


@pytest.mark.skipif(
    not DATA_FILE.exists(),
    reason=(
        f"bulk-validation dataset not found at {DATA_FILE}. "
        "It is committed to the repo at tests/local-test-data/ but excluded "
        "from the PyPI package via pyproject.toml — restore it with "
        "`git checkout tests/local-test-data/`."
    ),
)
def test_with_large_numbers_of_known_valid_nhs_numbers():
    with DATA_FILE.open(newline="", encoding="utf-8-sig") as csvfile:
        testdata = []
        for line in csv.reader(csvfile):
            testdata += line

        for test_number in testdata:
            assert is_valid(test_number) is True

        print(f"\n{len(testdata)} numbers tested for validity in bulk")
