"""
Returns more detailed information on NHS numbers.

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors
* Marcus Baw <marcusbaw@gmail.com>
"""

# standard imports

# third-party imports

# local imports
from nhs_number import REGIONS
from nhs_number.validate import is_valid, calculate_checksum


class NhsNumber:
    nhs_number: str
    """
    A class which returns more information about an NHS Number than simply
    Boolean validity.

    nhs_number: str
        The NHS number to be validated, returned to you as a sense-check.
    identifier_digits: str
        The first 9 digits of the NHS number, which are the identifier digits.
    check_digit: int
        The 10th digit of the NHS number, which is the check digit.
    valid: bool
        Whether the NHS number is valid or not according to the checksum
        comparison.
    calculated_checksum: int
        The checksum calculated from the identifier digits, so you can compare
        it to the check digit.
    region: Region
        The region the NHS number is valid in, if any. Returns an instance of
        the Region class from the constants module.
    region_comment: str
        The name of the region the NHS number is valid in, if any. Returns a
        string.

    Usage:
    >>> from nhs_number import NhsNumber
    >>> nhs_number = NhsNumber('9876543210')
    >>> vars(nhs_number)
    {'nhs_number': '9876543210', 'identifier_digits': '987654321', 'check_digit': 0, 'valid': True, 'calculated_checksum': 0, 'region': <nhs_number.constants.Region object at 0x7fcb31de5e90>, 'region_comment': 'Not to be issued (Synthetic/test patients PDS)'}

    """

    def __init__(self, nhs_number):
        self.nhs_number = nhs_number

        # split the number into its parts
        (identifier_digits, check_digit) = (
            nhs_number[:-1],
            int(nhs_number[-1]),
        )
        self.identifier_digits = identifier_digits
        self.check_digit = check_digit

        # determine if the number is valid
        valid = is_valid(nhs_number)
        self.valid = valid

        # determine if reason for invalidity is failure of checksum match
        calculated_checksum = calculate_checksum(identifier_digits)
        self.calculated_checksum = calculated_checksum

        # default region comment is 'not found'
        region_comment = "Number did not match a known NHS number range"

        # determine the region the number is valid in
        for handle, region in REGIONS.items():
            if region.contains_number(nhs_number):
                region_comment = region.label
                self.region = region

        self.region_comment = region_comment
