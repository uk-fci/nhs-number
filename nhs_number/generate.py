"""
Generates valid or invalid NHS numbers, for testing

License: MIT (http://www.opensource.org/licenses/mit-license.php)

Contributors
* Marcus Baw <marcusbaw@gmail.com>
"""

# standard imports
from random import randint

# third-party imports

# local imports
from nhs_number.validate import is_valid
from nhs_number.constants import Region


def generate(
    valid: bool = True,
    for_region: Region = None,
    start: int = 0,  # defaults to 0
    end: int = 9_999_999_999,  # defaults to 9_999_999_999
    randomised: bool = False,
    quantity: int = 1,
) -> list:

    """
    Generates valid or invalid NHS numbers, for testing.

    IMPORTANT: This function is not intended to be used to create real NHS numbers. It is for testing purposes only.
    All live NHS numbers are allocated centrally and are not generated locally.

    Optional keyword arguments:

        valid: bool
            Determines whether the NHS numbers to be generated are valid or invalid.
        for_region: Region
            If supplied, the start and end ranges for the supplied region will be used
            and any start and end ranges supplied in the function call will be ignored.
        start: int
            If supplied, the start range for the NHS numbers to be generated.
        end: int
            If supplied, the end range for the NHS numbers to be generated.
        randomised: bool
            If True, the NHS numbers will be generated randomly within the start and end ranges, otherwise they will be generated sequentially.
        quantity: int
            How many NHS numbers to generate.

    The algorithm used here is very naive and could be significantly optimised.
    But it is fairly fast anyway and works well enough for the purposes of this library.
    Contributions are welcome.
    """

    # initialise the list of NHS numbers to be returned
    nhs_numbers = []

    if start > end:
        raise ValueError("The start range cannot be greater than the end range")

    if for_region:
        if isinstance(for_region, Region):
            # if a region is supplied, use the start and end ranges for that region
            # and ignore any start and end ranges supplied in the function call
            start = for_region.start
            end = for_region.end
        else:
            raise TypeError("The for_region argument must be of type Region")

    # generates valid NHS numbers between the start and end ranges supplied
    if not randomised:
        for candidate in range(start, end):
            if len(nhs_numbers) < quantity:
                candidate_str = str(candidate).zfill(10)
                if is_valid(candidate_str) == valid:
                    nhs_numbers.append(candidate_str)
            else:
                break

    else:  # (ie. randomised == True)
        # generates valid random NHS numbers between the start and end ranges supplied
        while len(nhs_numbers) < quantity:
            candidate = randint(start, end)
            candidate_str = str(candidate).zfill(10)
            if is_valid(candidate_str) == valid:
                nhs_numbers.append(candidate_str)

    return nhs_numbers
