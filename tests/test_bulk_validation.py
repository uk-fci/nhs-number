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
import os.path
import sys

import pytest

from nhs_number import is_valid

csv.field_size_limit(sys.maxsize)

DATA_DIR = os.path.join(os.path.dirname(__file__), "local-test-data")
DATA_FILE = os.path.join(DATA_DIR, "testdata-909090-valid-nhs-numbers.csv")


@pytest.mark.skipif(
    not os.path.exists(DATA_FILE),
    reason=(
        f"bulk-validation dataset not found at {DATA_FILE}. "
        "It is committed to the repo at tests/local-test-data/ but excluded "
        "from the PyPI package via pyproject.toml — restore it with "
        "`git checkout tests/local-test-data/`."
    ),
)
def test_with_large_numbers_of_known_valid_nhs_numbers():
    with open(DATA_FILE, newline="", encoding="utf-8-sig") as csvfile:
        testdata = []
        for line in csv.reader(csvfile):
            testdata += line

        for test_number in testdata:
            assert is_valid(test_number) is True

        print(f"\n{len(testdata)} numbers tested for validity in bulk")
