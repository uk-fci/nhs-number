"""
Development-only bulk testing of testing NHS numbers against the code
"""
# standard imports
import os.path
import csv
import sys

# third-party imports
import pytest

# local imports
from nhs_number import is_valid


csv.field_size_limit(sys.maxsize)


@pytest.mark.skipif(
    not os.path.exists("local-test-data/testdata-909090-valid-nhs-numbers.csv"),
    reason="This test requires a large list of valid NHS numbers which we do not want to include in the repo by default for reasons of file size",
)
def test_with_large_numbers_of_known_valid_nhs_numbers():
    with open(
        "local-test-data/testdata-909090-valid-nhs-numbers.csv",
        newline="",
        encoding="utf-8-sig",
    ) as csvfile:
        testdata = []
        for line in csv.reader(csvfile):
            testdata += line

        for test_number in testdata:
            assert is_valid(test_number) == True

        print(f"\n{len(testdata)} numbers tested for validity in bulk")
