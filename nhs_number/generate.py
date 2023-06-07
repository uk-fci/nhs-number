"""
Generates valid or invalid NHS numbers, for testing
"""
from random import randint

from nhs_number.validate import is_valid

def generate(valid: bool = True,
             country: str = None,
             start: int = 0, # defaults to 0
             end: int = 9_999_999_999, # defaults to 9_999_999_999
             randomised: bool = False,
             quantity: int = 1) -> list:

    """
    Generates valid or invalid NHS numbers, for testing.
    The algorithm used here is very naive and could be significantly optimised.
    But it is fairly fast anyway and works well enough for the purposes of this library.
    Contributions are welcome.
    """

    nhs_numbers = []

    # generates valid NHS numbers between the start and end ranges supplied
    if not randomised:
        for candidate in range(start, end):
            candidate_str = str(candidate).zfill(10)
            if is_valid(candidate_str) == valid:
                if len(nhs_numbers) < quantity:
                    nhs_numbers.append(candidate_str)
        return nhs_numbers

    else: # (ie. randomised == True)
        # generates valid random NHS numbers between the start and end ranges supplied
        while len(nhs_numbers) < quantity:
            candidate = randint(start, end)
            candidate_str = str(candidate).zfill(10)
            if is_valid(candidate_str) == valid:
                nhs_numbers.append(candidate_str)
        return nhs_numbers



