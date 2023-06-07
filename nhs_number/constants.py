"""
Constants which define ranges of NHS Numbers

License: MIT (http://www.opensource.org/licenses/mit-license.php)

Contributors:
* Marcus Baw <marcusbaw@gmail.com>
"""

# using dataclasses would force Python 3.7 or above so we'll use a simple class instead
# from dataclasses import dataclass

"""
The most accurate information on the NHS Number ranges we could find is collated here.
This file should be considered the source of truth for NHS Number ranges.

n = the Modulo 11 check digit

    000000001n - 009999999n Unreserved (not in use)
    010000000n - 311299999n Scotland CHI numbers (DDMMYYxxxn)
    311300000n - 319999999n Unreserved
    320000000n - 399999999n Northern Ireland H&C Numbers
    400000000n - 499999999n England, Wales and IOM NHS Numbers
    500000000n - 599999999n Not to be issued
    600000000n - 799999999n England, Wales and IOM NHS Numbers
    800000000n - 859999999n Used within the Republic of Ireland Individual Health Identifier (IHI)
    860000000n - 899999999n Unreserved
    900000000n - 999999999n Not to be issued (Synthetic/test patients PDS)

"""

class Region:
    start: int
    end: int
    label: str
    tags: list

    def __init__(self, start, end, label, tags):
        self.start = start
        self.end = end
        self.label = label
        self.tags = tags


REGION_UNRESERVED_1 = Region(
    start=1,
    end=9_999_999,
    label="Unreserved (not in use)",
    tags=["unreserved"])

REGION_SCOTLAND = Region(
    start=10_000_000,
    end=311_299_999,
    label="Scotland CHI numbers",
    tags=["scotland", "chi"])

REGION_UNRESERVED_2 = Region(
    start=311_300_000,
    end=319_999_999,
    label="Unreserved",
    tags=["unreserved"])

REGION_NORTHERN_IRELAND = Region(
    start=320_000_000,
    end=399_999_999,
    label="Northern Ireland H&C Numbers",
    tags=["northern-ireland", "ni"])

REGION_ENGLAND_WALES_1 = Region(
    start=400_000_000,
    end=499_999_999,
    label="England Wales and IOM NHS Numbers",
    tags=["england-wales", "e-w-iom"])

REGION_NOT_ISSUED = Region(
    start=500_000_000,
    end=599_999_999,
    label="Not to be issued",
    tags=["not-issued"])

REGION_ENGLAND_WALES_2 = Region(
    start=600_000_000,
    end=799_999_999,
    label="England Wales and IOM NHS Numbers",
    tags=["england-wales"])

REGION_EIRE = Region(
    start=800_000_000,
    end=859_999_999,
    label="Used within the Republic of Ireland Individual Health Identifier (IHI)",
    tags=["eire", "republic-of-ireland", "ihi"])

REGION_NOT_ISSUED_SYNTHETIC = Region(
    start=900_000_000,
    end=999_999_999,
    label="Not to be issued (Synthetic/test patients PDS)",
    tags=["test", "synthetic"])

REGIONS = [
    REGION_UNRESERVED_1,
    REGION_SCOTLAND,
    REGION_UNRESERVED_2,
    REGION_NORTHERN_IRELAND,
    REGION_ENGLAND_WALES_1,
    REGION_NOT_ISSUED,
    REGION_ENGLAND_WALES_2,
    REGION_EIRE,
    REGION_NOT_ISSUED_SYNTHETIC,
]


