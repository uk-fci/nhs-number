"""
Constants which define ranges of NHS Numbers

License: MIT (http://www.opensource.org/licenses/mit-license.php)

Contributors:
* Marcus Baw <marcusbaw@gmail.com>
* Andy Law <andy.law@roslin.ed.ac.uk>

The most accurate information on the NHS Number ranges we could find is collated here.
This file should be considered the source of truth for NHS Number ranges.
Ranges are INCLUSIVE of the start and end values.

    0000000010 - 0099999999 Unreserved (not in use)
    0100000000 - 3112999999 Scotland CHI numbers (DDMMYYxxxn)
    3113000000 - 3199999999 Unreserved
    3200000000 - 3999999999 Northern Ireland H&C Numbers
    4000000000 - 4999999999 England, Wales and IOM NHS Numbers
    5000000000 - 5999999999 Not to be issued
    6000000000 - 7999999999 England, Wales and IOM NHS Numbers
    8000000000 - 8599999999 Used within the Republic of Ireland Individual Health Identifier (IHI)
    8600000000 - 8999999999 Unreserved
    9000000000 - 9999999999 Not to be issued (Synthetic/test patients PDS)
"""

# using dataclasses would force Python 3.7 or above so we'll use a simple class instead

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
    start=1, end=9_999_999, label="Unreserved (not in use)", tags=["unreserved"]
)

REGION_SCOTLAND = Region(
    start=10_000_000,
    end=3_112_999_999,
    label="Scotland CHI numbers",
    tags=["scotland", "chi"],
)

REGION_UNRESERVED_2 = Region(
    start=3_113_000_000, end=3_199_999_999, label="Unreserved", tags=["unreserved"]
)

REGION_NORTHERN_IRELAND = Region(
    start=3_200_000_000,
    end=3_999_999_999,
    label="Northern Ireland H&C Numbers",
    tags=["northern-ireland", "ni", "tuaisceart-éireann"],
)

REGION_ENGLAND_WALES_IOM_1 = Region(
    start=4_000_000_000,
    end=4_999_999_999,
    label="England Wales and IOM NHS Numbers",
    tags=["england-wales", "e-w-iom", "isle-of-man", "cymru", "wales"],
)

REGION_NOT_ISSUED = Region(
    start=5_000_000_000,
    end=5_999_999_999,
    label="Not to be issued",
    tags=["not-issued"],
)

REGION_ENGLAND_WALES_IOM_2 = Region(
    start=6_000_000_000,
    end=7_999_999_999,
    label="England Wales and IOM NHS Numbers",
    tags=["england-wales", "e-w-iom", "isle-of-man", "cymru", "wales"],
)

REGION_EIRE = Region(
    start=8_000_000_000,
    end=8_599_999_999,
    label="Used within the Republic of Ireland Individual Health Identifier (IHI)",
    tags=["eire", "republic-of-ireland", "ihi", "individual-health-identifier", "poblacht-na-héireann"],
)

REGION_UNRESERVED_3 = Region(
    start=8_600_000_000, end=8_999_999_999, label="Unreserved", tags=["unreserved"]
)

REGION_NOT_ISSUED_SYNTHETIC = Region(
    start=9_000_000_000,
    end=9_999_999_999,
    label="Not to be issued (Synthetic/test patients PDS)",
    tags=["test", "synthetic"],
)

REGIONS = {
    "UNRESERVED_1": REGION_UNRESERVED_1,
    "SCOTLAND": REGION_SCOTLAND,
    "UNRESERVED_2": REGION_UNRESERVED_2,
    "NORTHERN_IRELAND": REGION_NORTHERN_IRELAND,
    "ENGLAND_WALES_IOM_1": REGION_ENGLAND_WALES_IOM_1,
    "NOT_ISSUED": REGION_NOT_ISSUED,
    "ENGLAND_WALES_IOM_2": REGION_ENGLAND_WALES_IOM_2,
    "EIRE": REGION_EIRE,
    "UNRESERVED_3": REGION_UNRESERVED_3,
    "NOT_ISSUED_SYNTHETIC": REGION_NOT_ISSUED_SYNTHETIC,
}

