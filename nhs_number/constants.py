"""
Constants which define ranges of NHS Numbers

License: MIT (https://www.opensource.org/licenses/mit-license.php)

Contributors:
* Marcus Baw <marcusbaw@gmail.com>
* Andy Law <andy.law@roslin.ed.ac.uk>

The most accurate information on the NHS Number ranges we could find is
collated here.
This file should be considered the source of truth for NHS Number ranges.
Ranges are INCLUSIVE of the start and end values.

    0000000010 - 0099999999 Unreserved (not in use)
    0100000000 - 3112999999 Scotland CHI numbers (DDMMYYxxxn)
    3113000000 - 3199999999 Unreserved
    3200000000 - 3999999999 Northern Ireland H&C Numbers
    4000000000 - 4999999999 England, Wales and IOM NHS Numbers
    5000000000 - 5999999999 Not to be issued
    6000000000 - 7999999999 England, Wales and IOM NHS Numbers
    8000000000 - 8599999999 Used within the Republic of Ireland Individual
                            Health Identifier (IHI)
    8600000000 - 8999999999 Unreserved
    9000000000 - 9999999999 Not to be issued (Synthetic/test patients PDS)
"""

from enum import Enum


# using dataclasses would force Python 3.7 or above so we'll use a simple
# class instead
class Range:
    """
    A class to represent contiguous blocks of allocated NHS Numbers
    """

    start: int
    end: int

    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def contains_number(self, number):
        if self.start <= int(number) <= self.end:
            return True
        else:
            return False


class Region:
    """
    A class to represent the blocks of numbers allocated to a given region
    """

    ranges: list
    label: str
    tags: list

    def __init__(self, label, tags, ranges):
        self.label = label
        self.tags = tags
        self.ranges = ranges

    def contains_number(self, number):
        for _range in self.ranges:
            if _range.contains_number(number):
                return True
        return False


class Sex(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


RANGE_UNALLOCATED_1 = Range(
    start=10,
    end=9_999_999,
    label="Unallocated 1 (not in use)",
)

RANGE_SCOTLAND = Range(
    start=10_000_000,
    end=3_112_999_999,
    label="Scotland CHI numbers",
)

RANGE_UNALLOCATED_2 = Range(
    start=3_113_000_000,
    end=3_199_999_999,
    label="Unallocated 2 (not in use)",
)

RANGE_NORTHERN_IRELAND = Range(
    start=3_200_000_000,
    end=3_999_999_999,
    label="Northern Ireland H&C Numbers",
)

RANGE_ENGLAND_WALES_IOM_1 = Range(
    start=4_000_000_000,
    end=4_999_999_999,
    label="England Wales and IOM NHS Numbers Range 1",
)

RANGE_RESERVED = Range(
    start=5_000_000_000,
    end=5_999_999_999,
    label="Reserved Range - not to be issued",
)

RANGE_ENGLAND_WALES_IOM_2 = Range(
    start=6_000_000_000,
    end=7_999_999_999,
    label="England Wales and IOM NHS Numbers Range 2",
)

RANGE_EIRE = Range(
    start=8_000_000_000,
    end=8_599_999_999,
    label=(
        "Used within the Republic of Ireland Individual Health Identifier"
        " (IHI)"
    ),
)

RANGE_UNALLOCATED_3 = Range(
    start=8_600_000_000,
    end=8_999_999_999,
    label="Unallocated 3 (not in use)",
)

RANGE_NOT_ISSUED_SYNTHETIC = Range(
    start=9_000_000_000,
    end=9_999_999_999,
    label="Not to be issued (Synthetic/test patients PDS)",
)

FULL_RANGE = Range(
    start=10,
    end=9_999_999_999,
    label="Full range of possible numbers, not all are actually valid",
)


REGION_SCOTLAND = Region(
    label="Scotland CHI numbers",
    tags=["scotland", "chi"],
    ranges=[RANGE_SCOTLAND],
)

REGION_ENGLAND_WALES_IOM = Region(
    label="England Wales and IOM NHS Numbers",
    tags=["england-wales", "e-w-iom", "isle-of-man", "cymru", "wales"],
    ranges=[RANGE_ENGLAND_WALES_IOM_1, RANGE_ENGLAND_WALES_IOM_2],
)

REGION_ENGLAND = REGION_WALES = REGION_IOM = REGION_ENGLAND_WALES_IOM

REGION_NORTHERN_IRELAND = Region(
    label="Northern Ireland H&C Numbers",
    tags=["northern-ireland", "ni", "tuaisceart-éireann"],
    ranges=[RANGE_NORTHERN_IRELAND],
)

REGION_EIRE = Region(
    label=(
        "Used within the Republic of Ireland Individual Health Identifier"
        " (IHI)"
    ),
    tags=[
        "eire",
        "republic-of-ireland",
        "ihi",
        "individual-health-identifier",
        "poblacht-na-héireann",
    ],
    ranges=[RANGE_EIRE],
)

REGION_SYNTHETIC = Region(
    label="Not to be issued (Synthetic/test patients PDS)",
    tags=["test", "synthetic"],
    ranges=[RANGE_NOT_ISSUED_SYNTHETIC],
)

REGION_UNALLOCATED = Region(
    label="Unallocated - should not be a valid Number",
    tags=["unallocated"],
    ranges=[RANGE_UNALLOCATED_1, RANGE_UNALLOCATED_2, RANGE_UNALLOCATED_3],
)

REGION_RESERVED = Region(
    label="Reserved and not issued", tags=["reserved"], ranges=[RANGE_RESERVED]
)

REGIONS = {
    "UNALLOCATED": REGION_UNALLOCATED,
    "SCOTLAND": REGION_SCOTLAND,
    "NORTHERN_IRELAND": REGION_NORTHERN_IRELAND,
    "ENGLAND_WALES_IOM": REGION_ENGLAND_WALES_IOM,
    "RESERVED": REGION_RESERVED,
    "EIRE": REGION_EIRE,
    "SYNTHETIC": REGION_SYNTHETIC,
}
