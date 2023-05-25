"""
Normalises NHS numbers into a standard string format
"""

import re

GOOD_FORMAT = r'^(\d{10}|\d{3} \d{3} \d{4}|\d{3}-\d{3}-\d{4})$'

def normalise_number(nhs_number:str) -> str:
    """
    Extract the 10 digits of an NHS number if the supplied string is a valid
    format. If supplied as an int it will attempt to convert it to a string for processing.
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
    working_number = str(nhs_number).strip()
    if re.search(GOOD_FORMAT, working_number) is None:
        working_number = ''
    working_number = re.sub('[- ]', '', working_number)
    return working_number
