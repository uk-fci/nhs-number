"""
Validates NHS Numbers

Originally derived from Andy Law's nhs_number Python package validation code

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors
* Andy Law <andy.law@roslin.ed.ac.uk>
* Marcus Baw <marcus@marcusbaw.com>
"""

# PEP 604 union syntax (`int | None`) is 3.10+; defer annotation evaluation
# so we keep working on Python 3.8 and 3.9. Remove this once 3.8/3.9 are
# dropped from the test matrix.
from __future__ import annotations
from datetime import datetime
from nhs_number.standardise import standardise_format
from nhs_number.constants import Region, REGION_SCOTLAND


def calculate_checksum(identifier_digits: str) -> int | None:
    """
    Calculates the checksum digit for the supplied NHS number (as a string) and
    returns it as an integer.
    IMPORTANT: Expects a string of NINE digits (ie REMOVE the check digit,
    don't supply a full NHS number)
    """
    if len(identifier_digits) != 9:
        return None

    # For the algorithm that calculates the checksum digit, see
    # https://www.closer.ac.uk/wp-content/uploads/CLOSER-NHS-ID-Resource-Report-Apr2018.pdf
    parts_list = [
        int(digit) * (10 - index)
        for index, digit in enumerate(identifier_digits)
    ]
    list_sum = sum(parts_list)
    checksum = 11 - (list_sum % 11)
    if checksum == 11:
        checksum = 0
    return checksum


def calculate_checksum_mod10(identifier_digits: str) -> int | None:
    """
    Calculates the modulus 10 check digit used by the newer CHI numbers
    (Scotland), as a Luhn-style sum over the first nine digits.

    From August 2026, CHI numbers are valid if the check digit passes either
    the modulus 11 or the modulus 10 check. The source for this algorithm is
    Public Health Scotland's own implementation
    (https://github.com/Public-Health-Scotland/phsmethods, R/chi_check.R,
    https://code.publichealthscotland.scot/phsmethods/articles/chi-operations.html):

    * double the 1st, 3rd, 5th, 7th and 9th identifier digits (counting from
      the left, so the digit next to the check digit and every second one)
    * if a doubled digit is greater than nine, subtract nine
    * sum all nine digits, take the remainder modulo 10
    * the check digit is 10 minus that remainder, with 10 mapped to 0

    IMPORTANT: Expects a string of NINE digits (ie REMOVE the check digit,
    don't supply a full CHI number). Returns None for any other length.

    See issue #107 and the CHI Managed Board minutes referenced there.
    """
    if len(identifier_digits) != 9:
        return None

    total = 0
    for index, digit in enumerate(identifier_digits):
        value = int(digit)
        if index % 2 == 0:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    check_digit = 10 - (total % 10)
    return 0 if check_digit == 10 else check_digit


def is_valid(nhs_number: str, for_region: Region = None) -> bool:
    """
    Checks the supplied NHS number (as a string) is valid and returns True
    or False.

    Internally this uses the normalise_number() function to check that this is
    a valid format to start with.
    Any non-valid input will result in returning False.

    The NHS number must:
        1. be 10 digits long
        2. The 10th digit is a check digit to confirm validity using the
           modulus 11 method

    CHI numbers (Scotland) additionally accept the modulus 10 check digit
    from August 2026: a number in the CHI range is valid if its check digit
    matches either the modulus 11 or the modulus 10 calculation.

    How NHS Number validation works:
            https://www.datadictionary.nhs.uk/attributes/nhs_number.html

    """
    # Normalise the NHS number to remove any spaces or dashes
    nhs_number = standardise_format(nhs_number)
    if not nhs_number:
        return False

    # If the NHS number is outside the range for the supplied region,
    # return False
    if for_region and not for_region.contains_number(nhs_number):
        return False

    # CHI numbers (Scotland) encode the date of birth in the first 6 digits
    # as DDMMYY. A number in the CHI range whose first 6 digits are not a real
    # calendar date is not a valid CHI number. See issue #25.
    if REGION_SCOTLAND.contains_number(nhs_number):
        try:
            datetime.strptime(nhs_number[:6], "%d%m%y")
        except ValueError:
            return False

    # Test for checksum validity
    # The first 9 numbers are used to calculate the checksum, which should
    # match the last digit
    identifier_digits, check_digit = (nhs_number[:-1], int(nhs_number[-1]))
    calculated_checksum = calculate_checksum(identifier_digits)
    if calculated_checksum == check_digit:
        return True
    # NOTE: a checksum of 10 is invalid (and is quoted as a special case),
    # but the check for equality
    # will catch that circumstance anyway

    # From August 2026, CHI numbers (Scotland) are also issued with a
    # modulus 10 check digit, so a number in the CHI range is valid if the
    # check digit matches either calculation. Other regions still use
    # modulus 11 only. See issue #107.
    if REGION_SCOTLAND.contains_number(nhs_number):
        return calculate_checksum_mod10(identifier_digits) == check_digit
    return False
