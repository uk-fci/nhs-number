"""
__init__.py
"""

# explicit imports into __init__.py are used in order to allow separate files
# without affecting the namespacing of the original library.
from nhs_number.validate import is_valid
from nhs_number.normalise import normalise_number



