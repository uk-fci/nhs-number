"""
Generates valid or invalid NHS numbers, for testing

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors
* Marcus Baw <marcusbaw@gmail.com>
"""
import random

# standard imports
from random import randint

# third-party imports

# local imports
from nhs_number.validate import calculate_checksum
from nhs_number import Region, FULL_RANGE


def generate(
    valid: bool = True,
    for_region: Region = None,
    quantity: int = 1,
) -> list:
    """
    Generates valid or invalid NHS numbers, for testing.

    IMPORTANT: This function is not intended to be used to create real NHS
    numbers. It is for testing purposes only.
    All live NHS numbers are allocated centrally and are not generated locally.

    Optional keyword arguments:

        valid: bool
            Determines whether the NHS numbers to be generated are valid or
            invalid.
        for_region: Region
            If supplied, the start and end ranges for the supplied region will
            be used and any start and end ranges supplied in the function
            call will be ignored.
        quantity: int
            How many NHS numbers to generate.

    The algorithm used here is very naive and could be significantly optimised.
    But it is fairly fast anyway and works well enough for the purposes of
    this library.
    Contributions are welcome.
    """

    # initialise the list of NHS numbers to be returned
    nhs_numbers = []

    ranges = [FULL_RANGE]

    if for_region:
        if isinstance(for_region, Region):
            ranges = for_region.ranges
        else:
            raise TypeError("The for_region argument must be of type Region")

    # generates valid random NHS numbers within the given REGION range
    while len(nhs_numbers) < quantity:
        this_range = random.choice(ranges)
        candidate = randint(this_range.start, this_range.end) // 10
        candidate_str = str(candidate).zfill(9)
        checksum_str = str(calculate_checksum(candidate_str))
        if len(checksum_str) == 1:
            if valid:
                nhs_numbers.append(candidate_str + checksum_str)
            else:
                wrong_checksum_str = checksum_str
                while wrong_checksum_str == checksum_str:
                    wrong_checksum_str = str(random.choice(range(0, 10)))
                nhs_numbers.append(candidate_str + wrong_checksum_str)

    return nhs_numbers
