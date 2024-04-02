import pytest

from datetime import datetime


from nhs_number import (
    generate,
    random_chi_str,
    is_valid,
    REGION_ENGLAND_WALES_IOM,
    REGION_SCOTLAND,
    REGION_NORTHERN_IRELAND,
    REGION_SYNTHETIC,
)


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


def test_nhs_numbers_with_no_region():
    nhs_numbers = generate()
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert REGION_SYNTHETIC.contains_number(nhs_numbers[0])


def test_nhs_numbers_for_specific_regions():
    """
    Test that NHS numbers for a specific region are generated
    """
    nhs_numbers = generate(for_region=REGION_ENGLAND_WALES_IOM)
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert REGION_ENGLAND_WALES_IOM.contains_number(nhs_numbers[0])

    nhs_numbers = generate(for_region=REGION_SCOTLAND)
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert REGION_SCOTLAND.contains_number(nhs_numbers[0])

    nhs_numbers = generate(for_region=REGION_NORTHERN_IRELAND)
    assert len(nhs_numbers) == 1
    assert is_valid(nhs_numbers[0])
    assert REGION_NORTHERN_IRELAND.contains_number(nhs_numbers[0])


def test_fail_when_non_region_supplied():
    """
    Test that we get an error if we supply something other than a Region
    object as the for_region argument
    :return:
    """
    with pytest.raises(TypeError) as error:
        # noinspection PyTypeChecker
        nhs_numbers = generate(for_region="REGION_ENGLAND_WALES_IOM")


def test_random_chi_str_len():
    partial_chi_number = random_chi_str()
    assert len(partial_chi_number) == 9


def test_random_chi_str_is_real_date():
    partial_chi_number = random_chi_str()
    try:
        datetime.strptime(partial_chi_number[:6], "%d%m%y")
    except ValueError as e:
        pytest.fail(f"Unexpected ValueError: {e}")
