"""
Returns more detailed information on NHS numbers.

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors
* Marcus Baw <marcus@marcusbaw.com>
"""

# standard imports

# third-party imports

# local imports
from nhs_number import REGIONS
from nhs_number.standardise import standardise_format
from nhs_number.validate import is_valid, calculate_checksum


class NhsNumber:
    """
    A class which returns more information about an NHS Number than simply
    Boolean validity.

    nhs_number: str | int | None
        The NHS number as supplied, returned to you as a sense-check. May be a
        formatted string ("987 654 3210"), an int, or any other input — in
        which case the remaining attributes report invalidity rather than
        raising.
    identifier_digits: str
        The first 9 digits of the standardised NHS number. Empty string if the
        input could not be parsed into a 10-digit NHS number format.
    check_digit: int | None
        The 10th digit of the NHS number, or ``None`` if the input could not
        be parsed.
    valid: bool
        Whether the NHS number is valid or not according to the checksum
        comparison. ``False`` for any input that ``is_valid()`` would reject.
    calculated_checksum: int | None
        The checksum calculated from the identifier digits, so you can compare
        it to the check digit. ``None`` if the input could not be parsed.
    region: Region | None
        The region the NHS number falls within, or ``None`` if it does not
        fall within any known range (including unparseable input).
    region_comment: str
        The label of the matched region, or an explanatory message if no
        region matched.

    Usage:
    >>> from nhs_number import NhsNumber
    >>> nhs = NhsNumber('9876543210')
    >>> nhs.nhs_number
    '9876543210'
    >>> nhs.identifier_digits
    '987654321'
    >>> nhs.check_digit
    0
    >>> nhs.valid
    True
    >>> nhs.calculated_checksum
    0
    >>> nhs.region_comment
    'Not to be issued (Synthetic/test patients PDS)'

    """

    def __init__(self, nhs_number):
        self.nhs_number = nhs_number

        # Standardise first so formatted strings ("987 654 3210"), ints, and
        # surrounding whitespace all parse correctly. Returns "" for inputs
        # that cannot be coerced to a 10-digit NHS number format (including
        # None and other unsupported types).
        standardised = standardise_format(nhs_number)

        if standardised:
            self.identifier_digits = standardised[:-1]
            self.check_digit = int(standardised[-1])
            self.calculated_checksum = calculate_checksum(self.identifier_digits)
            self.valid = is_valid(standardised)
        else:
            self.identifier_digits = ""
            self.check_digit = None
            self.calculated_checksum = None
            self.valid = False

        self.region = None
        self.region_comment = "Number did not match a known NHS number range"
        if standardised:
            for _, region in REGIONS.items():
                if region.contains_number(standardised):
                    self.region = region
                    self.region_comment = region.label
                    break
