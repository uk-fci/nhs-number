"""
Generate deterministic fake NHS/CHI/HSC numbers for testing and
disguise/de-identification purposes.

License: MIT (https://www.opensource.org/licenses/mit-license.php)
"""

import datetime
import random
from enum import Enum
from typing import Tuple

from nhs_number.constants import (
    RANGE_NORTHERN_IRELAND,
    RANGE_NOT_ISSUED_SYNTHETIC,
    REGION_ENGLAND_WALES_IOM,
    REGION_NORTHERN_IRELAND,
    REGION_SCOTLAND,
    REGION_SYNTHETIC,
)
from nhs_number.standardise import standardise_format
from nhs_number.validate import calculate_checksum


class OrganizationType(Enum):
    NHS = "nhs"
    CHI = "chi"
    HSC = "hsc"
    UNKNOWN = "unknown"


def _get_organization(nhs_number: str) -> OrganizationType:
    """Classify the supplied number as NHS, CHI, HSC, or unknown."""
    if REGION_SCOTLAND.contains_number(nhs_number):
        return OrganizationType.CHI
    if REGION_NORTHERN_IRELAND.contains_number(nhs_number):
        return OrganizationType.HSC
    if REGION_ENGLAND_WALES_IOM.contains_number(
        nhs_number
    ) or REGION_SYNTHETIC.contains_number(nhs_number):
        return OrganizationType.NHS
    return OrganizationType.UNKNOWN


def _first_nine_digits(value: int) -> int:
    """Return the first nine digits of an integer."""
    return int(str(value)[:9])


def _fake_range(organization: OrganizationType) -> Tuple[int, int]:
    """
    Return the 9-digit fake number range for the supplied organization.

    NHS fakes use the synthetic/test range so that they cannot clash with
    live issued numbers.
    """
    if organization == OrganizationType.NHS:
        return (
            _first_nine_digits(RANGE_NOT_ISSUED_SYNTHETIC.start),
            _first_nine_digits(RANGE_NOT_ISSUED_SYNTHETIC.end),
        )
    if organization == OrganizationType.HSC:
        return (
            _first_nine_digits(RANGE_NORTHERN_IRELAND.start),
            _first_nine_digits(RANGE_NORTHERN_IRELAND.end),
        )
    raise ValueError(f"Unsupported organization: {organization}")


def _random_chi_digits(rng: random.Random) -> str:
    """Return nine CHI identifier digits using the supplied rng.

    Digits 7 and 8 are fixed to 99 to mark the number as fake.
    """
    start = datetime.datetime(1900, 1, 1)
    end = datetime.datetime(1999, 12, 31)
    random_days = rng.randint(0, (end - start).days)
    random_date = start + datetime.timedelta(days=random_days)

    date_str = random_date.strftime("%d%m%y")
    sex = str(rng.randint(0, 9))

    # 99 is not a defined standard for fake CHI numbers but may be beneficial
    # for identification and 9 is a common digit to use in fake NHS numbers
    return f"{date_str}99{sex}"


def _check_number(nhs_number: str) -> Tuple[str, OrganizationType]:
    """Validate and classify the supplied number."""
    nhs_number = standardise_format(nhs_number)
    if not nhs_number:
        raise ValueError(
            "Invalid NHS/CHI/HSC number. Expected a 10 digit number."
        )

    organization = _get_organization(nhs_number)
    if organization == OrganizationType.UNKNOWN:
        raise ValueError(
            f"Unsupported NHS/CHI/HSC number range for {nhs_number}"
        )

    return nhs_number, organization


def disguise(real_nhs_number: str, *, seed: int) -> str:
    """Generate a deterministic, valid fake NHS/CHI/HSC number.

    The same ``real_nhs_number`` and ``seed`` combination will always
    produce the same fake number. Use a different ``seed`` to generate an
    alternative fake for the same real number.
    """
    real_nhs_number, organization = _check_number(real_nhs_number)

    rng = random.Random(int(real_nhs_number) * seed)

    # The chance of 1000 failures is astronomically small
    for _ in range(1000):
        if organization == OrganizationType.CHI:
            candidate = _random_chi_digits(rng)
        else:
            min_value, max_value = _fake_range(organization)
            candidate = str(rng.randint(min_value, max_value))

        check_digit = calculate_checksum(candidate)

        if check_digit is not None and check_digit != 10:
            return f"{candidate}{check_digit}"

    raise RuntimeError(
        f"Unable to generate a valid fake number for {real_nhs_number}"
    )
