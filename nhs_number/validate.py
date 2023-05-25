"""
Validates NHS Numbers
"""
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

__version__ = '1.2.1'
__author__ = "Andy Law <andy.law@roslin.ed.ac.uk>"

from nhs_number.normalise import normalise_number

def is_valid(nhs_number:str) -> bool:
    """
    Checks the supplied NHS number (as a string) is valid and returns True or False.

    Internally this uses the normalise_number() function to check that this is a valid format to start with.
    Any non-valid input will result in returning False.
    """

    nhs_number = normalise_number(nhs_number)
    if not nhs_number:
        return False

    # The first 9 numbers are used to calculate the checksum, which should match the last digit
    (first_part, check_digit) = (nhs_number[:-1], int(nhs_number[-1]))

    # For the algorithm that calculates the checksum digit, see
    # https://www.closer.ac.uk/wp-content/uploads/CLOSER-NHS-ID-Resource-Report-Apr2018.pdf
    parts_list = [int(digit) * (10 - index) for index, digit in enumerate(first_part)]
    list_sum = sum(parts_list)
    checksum = 11 - (list_sum % 11)
    if checksum == 11:
        checksum = 0

    # NOTE: a checksum of 10 is invalid (and is quoted as a special case), but the check for equality
    # will catch that circumstance anyway
    return False if checksum != check_digit else True
