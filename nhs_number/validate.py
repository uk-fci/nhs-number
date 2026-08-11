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

_SEX_MALE = "male"
_SEX_FEMALE = "female"

# Values that are accepted but can never affect the result, because CHI
# parity is a single digit and can only ever encode two states. Covers both
# the current NHS PERSON PHENOTYPIC SEX / PERSON STATED GENDER CODE
# ("indeterminate", "not_known", 9, "X") and the retired PERSON GENDER CODE
# (0 for "Not Known"; 9 there means "Not Specified", already covered above).
# See https://uk-fci.github.io/nhs-number/sex-and-gender/ for the full
# mapping and the reasoning behind it.
_SEX_INERT = frozenset({"indeterminate", "not_known", 9, 0, "x"})


def _normalise_sex(sex: str | int | None) -> str | None:
    """
    Normalise a caller-supplied sex value to "male", "female", or None.

    Accepts the words "male" / "female" / "indeterminate" / "not_known"
    (case insensitive), and the NHS numeric/letter codes: 1 / 2 for
    male/female (stable across every NHS sex/gender code list), and
    9 / 0 / "X" for the various "indeterminate" / "not known" / "not
    specified" states - which are all treated identically, since a single
    parity digit cannot distinguish between them.

    Returns None for anything that should never affect validation: no
    value supplied, or one of the inert states above. Raises ValueError for
    anything unrecognised, including True/False (bool is a subclass of int
    in Python, but is never a meaningful sex code).
    """
    if sex is None:
        return None

    error = ValueError(
        f"Unrecognised sex value: {sex!r}. Use 'male', 'female', "
        "'indeterminate', or 'not_known', or the NHS numeric/letter codes "
        "1, 2, 9, 0, 'X'."
    )

    if isinstance(sex, bool):
        raise error
    if isinstance(sex, str):
        key = sex.strip().lower()
    elif isinstance(sex, int):
        key = sex
    else:
        raise error

    if key in (_SEX_MALE, 1):
        return _SEX_MALE
    if key in (_SEX_FEMALE, 2):
        return _SEX_FEMALE
    if key in _SEX_INERT:
        return None
    raise error


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


def is_valid(
    nhs_number: str, for_region: Region = None, *, sex: str | int = None
) -> bool:
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

    How NHS Number validation works:
            https://www.datadictionary.nhs.uk/attributes/nhs_number.html

    :param sex: optional. If the number is a Scotland CHI number, checks
        that the parity of its 9th digit (odd=male, even=female) matches the
        supplied sex - a mismatch makes the number invalid. Has no effect on
        non-CHI numbers, or on a sex value that cannot express a determinate
        sex ("indeterminate", "not_known", or their NHS numeric/letter
        codes). Accepts "male", "female", "indeterminate", "not_known"
        (case insensitive), or the NHS codes 1, 2, 9, 0, "X". Raises
        ValueError for any other value. See
        https://uk-fci.github.io/nhs-number/sex-and-gender/ for the
        reasoning and the full code mapping.
    """
    # A bad sex value is a caller error, and is checked before anything else
    # so it raises consistently regardless of whether nhs_number is valid.
    normalised_sex = _normalise_sex(sex)

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

        # The 9th digit's parity encodes sex: odd=male, even=female. Only
        # meaningful for a determinate sex value - see #66.
        if normalised_sex is not None:
            ninth_digit_is_odd = int(nhs_number[8]) % 2 == 1
            if normalised_sex == _SEX_MALE and not ninth_digit_is_odd:
                return False
            if normalised_sex == _SEX_FEMALE and ninth_digit_is_odd:
                return False

    # Test for checksum validity
    # The first 9 numbers are used to calculate the checksum, which should
    # match the last digit
    identifier_digits, check_digit = (nhs_number[:-1], int(nhs_number[-1]))
    calculated_checksum = calculate_checksum(identifier_digits)
    # NOTE: a checksum of 10 is invalid (and is quoted as a special case),
    # but the check for equality
    # will catch that circumstance anyway
    return False if calculated_checksum != check_digit else True
