"""
Validates NHS Numbers

Originally derived from Andy Law's nhs_number Python package validation code

License: MIT (http://www.opensource.org/licenses/mit-license.php)

Contributors
* Andy Law <andy.law@roslin.ed.ac.uk>
* Marcus Baw <marcusbaw@gmail.com>
"""

from nhs_number.normalise import normalise_number
from nhs_number.constants import Region


def calculate_checksum(identifier_digits: str) -> int:
    """
    Calculates the checksum digit for the supplied NHS number (as a string) and returns it as an integer.
    IMPORTANT: Expects a string of NINE digits (ie REMOVE the check digit, don't supply a full NHS number)
    """
    if len(identifier_digits) != 9:
        return None

    # For the algorithm that calculates the checksum digit, see
    # https://www.closer.ac.uk/wp-content/uploads/CLOSER-NHS-ID-Resource-Report-Apr2018.pdf
    parts_list = [
        int(digit) * (10 - index) for index, digit in enumerate(identifier_digits)
    ]
    list_sum = sum(parts_list)
    checksum = 11 - (list_sum % 11)
    if checksum == 11:
        checksum = 0
    return checksum


def is_valid(nhs_number: str, for_region: Region = None) -> bool:
    """
    Checks the supplied NHS number (as a string) is valid and returns True or False.

    Internally this uses the normalise_number() function to check that this is a valid format to start with.
    Any non-valid input will result in returning False.

    The NHS number must:
        1. be 10 digits long
        2. The 10th digit is a check digit to confirm validity using the modulus 11 method

    How NHS Number validation works: https://www.datadictionary.nhs.uk/attributes/nhs_number.html

    """
    # Normalise the NHS number to remove any spaces or dashes
    nhs_number = normalise_number(nhs_number)
    if not nhs_number:
        return False

    # If the NHS number is outside of the range for the supplied region, return False
    if for_region:
        if not (
            int(nhs_number) >= for_region.start and int(nhs_number) <= for_region.end
        ):
            return False
        # Additional checks for Scotland CHI number DOB validity will go here

    # Test for checksum validity
    # The first 9 numbers are used to calculate the checksum, which should match the last digit
    (identifier_digits, check_digit) = (nhs_number[:-1], int(nhs_number[-1]))
    calculated_checksum = calculate_checksum(identifier_digits)
    # NOTE: a checksum of 10 is invalid (and is quoted as a special case), but the check for equality
    # will catch that circumstance anyway
    return False if calculated_checksum != check_digit else True
