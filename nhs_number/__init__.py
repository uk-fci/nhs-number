"""
Python code to check the validity of NHS Numbers
"""
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

__version__ = '1.2.1'
__author__ = "Andy Law <andy.law@roslin.ed.ac.uk>"

import re

GOOD_FORMAT = r'^(\d{10}|\d{3} \d{3} \d{4}|\d{3}-\d{3}-\d{4})$'


def is_valid(nhs_number):
    """
        Checks the supplied NHS number (as a string) is valid and returns True or False
    """
    # Use the normalise_number() function to check that this is a valid format to start with
    # Any non-valid input will result in an empty string return
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


def normalise_number(nhs_number):
    """
    Extract the 10 digits of an NHS number if the supplied string is a valid
    format.
    Valid formats are:
      123 456 7890
      123-456-7890
      1234567890
    with any amount of leading and trailing white space
    If Valid, this routine will return '1234567890' for all of the above inputs.
    An invalid input will result in the empty string which makes it possible to use a call
    to this function to test for valid format (but not valid checksum)
    :type nhs_number: basestring
    :param nhs_number:
    :return: 10 digit numerical string or the empty string
    """
    working_number = nhs_number.strip()
    if re.search(GOOD_FORMAT, working_number) is None:
        working_number = ''
    working_number = re.sub('[- ]', '', working_number)
    return working_number
