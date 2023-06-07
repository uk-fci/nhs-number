from nhs_number import REGIONS
from nhs_number.validate import is_valid, calculate_checksum

class NhsNumber:
    nhs_number: str
    """
    A class which returns more information about an NHS Number than simply validity.

    Usage:
    >>> from nhs_number import NhsNumber
    >>> nhs_number = NhsNumber('9876543210')
    >>> vars(nhs_number)
    {'nhs_number': '9876543210', 'identifier_digits': '987654321', 'check_digit': 0, 'valid': True, 'calculated_checksum': 0, 'region_comment': 'Not to be issued (Synthetic/test patients PDS)'}

    """

    def __init__(self, nhs_number):
        self.nhs_number = nhs_number

        # split the number into its parts
        (identifier_digits, check_digit) = (nhs_number[:-1], int(nhs_number[-1]))
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
        for region in REGIONS:
            if int(identifier_digits) >= region.start and int(identifier_digits) <= region.end:
                region_comment = region.label
                self.region = region

        self.region_comment = region_comment
