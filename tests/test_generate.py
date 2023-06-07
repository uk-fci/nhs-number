import pytest


from nhs_number import generate, is_valid
from nhs_number.constants import REGIONS


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
    nhs_numbers = generate(quantity=100, randomised=True)
    assert len(nhs_numbers) == 100
    for nhs_number in nhs_numbers:
        assert is_valid(nhs_number)


def test_nhs_numbers_within_a_specific_range():
    """
    Test that NHS numbers within a specific range are generated
    """
    nhs_numbers = generate(start=1000000000, end=1000000009)
    assert len(nhs_numbers) == 1
    assert nhs_numbers[0] >= "1000000000" and nhs_numbers[0] <= "1000000009"
    assert is_valid(nhs_numbers[0])


def test_nhs_numbers_for_a_specific_region():
    """
    Test that NHS numbers for a specific region are generated
    """
    nhs_numbers = generate(for_region=REGIONS["ENGLAND_WALES_IOM_1"])
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert nhs_numbers[0] >= "4000000000" and nhs_numbers[0] <= "4999999999"
