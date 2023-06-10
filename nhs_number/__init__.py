"""
__init__.py

Explicit imports into __init__.py are used in order to allow separate files
without affecting the namespacing of the original library.
"""

# standard imports

# third-party imports

# local imports
from nhs_number.constants import REGIONS, Region
from nhs_number.constants import (
    REGION_UNALLOCATED,
    REGION_RESERVED,
    REGION_ENGLAND,
    REGION_WALES,
    REGION_IOM,
    REGION_ENGLAND_WALES_IOM,
    REGION_SCOTLAND,
    REGION_NORTHERN_IRELAND,
    REGION_SYNTHETIC,
    REGION_EIRE,
)
from nhs_number.constants import FULL_RANGE
from nhs_number.details import NhsNumber
from nhs_number.generate import generate
from nhs_number.normalise import normalise_number
from nhs_number.validate import is_valid, calculate_checksum
