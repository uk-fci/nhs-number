"""
Normalises NHS numbers into a standard string format

Originally derived from Andy Law's nhs_number Python package validation code

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors
* Andy Law <andy.law@roslin.ed.ac.uk>
* Marcus Baw <marcusbaw@gmail.com>
"""
# standard imports
import re
import warnings

# third-party imports

# local imports


GOOD_FORMAT = r"^(\d{10}|\d{3} \d{3} \d{4}|\d{3}-\d{3}-\d{4})$"


def standardise_format(nhs_number: str | int) -> str:
    """
    Extract the 10 digits of an NHS number if the supplied string is a valid
    format. If supplied as an int it will attempt to convert it to a string for
    processing.
    Valid formats are:
      123 456 7890
      123-456-7890
      1234567890
    with any amount of leading and trailing white space
    If Valid, this routine will return '1234567890' for all of the above inputs.
    An invalid input will result in the empty string which makes it possible
    to use a call to this function to test for valid format (but not valid
    checksum)
    :type nhs_number: basestring
    :param nhs_number:
    :return: 10 digit numerical string or the empty string
    """
    if isinstance(nhs_number, int):
        working_number = str(nhs_number).zfill(10)
    else:
        working_number = nhs_number.strip()
    if re.search(GOOD_FORMAT, working_number) is None:
        working_number = ""
    working_number = re.sub("[- ]", "", working_number)
    return working_number


def normalise_number(nhs_number: str) -> str:
    warnings.warn("The normalise_number() function is deprecated - use "
                  "standardise_format() instead", DeprecationWarning)
    return standardise_format(nhs_number)
