"""
Pin the public import surface of the nhs_number package.

If a name is removed or renamed accidentally — or if a new public name is
added without consideration — this test fires. Adding to PUBLIC_NAMES is a
deliberate decision; removing is a breaking-change decision.
"""

import nhs_number
from nhs_number.constants import Range

PUBLIC_NAMES = [
    # Constants module
    "REGIONS",
    "Region",
    "FULL_RANGE",
    "REGION_UNALLOCATED",
    "REGION_RESERVED",
    "REGION_ENGLAND",
    "REGION_WALES",
    "REGION_IOM",
    "REGION_ENGLAND_WALES_IOM",
    "REGION_SCOTLAND",
    "REGION_NORTHERN_IRELAND",
    "REGION_SYNTHETIC",
    "REGION_EIRE",
    # Details
    "NhsNumber",
    # Disguise
    "disguise",
    # Generate
    "generate",
    # Standardise
    "standardise_format",
    "normalise_number",
    # Validate
    "is_valid",
    "calculate_checksum",
]


def test_all_public_names_importable():
    """Every documented public name resolves on the top-level package."""
    missing = [n for n in PUBLIC_NAMES if not hasattr(nhs_number, n)]
    assert missing == [], f"missing public names: {missing}"


def test_top_level_import_does_not_expose_private_names():
    """Pin the public surface as a *closed* set: anything new that appears
    here without being added to PUBLIC_NAMES is either an accidental leak or
    a deliberate addition that should be reflected in this test.

    Submodule attributes (``nhs_number.constants``, ``nhs_number.validate``
    etc. — exposed by Python's import machinery as a side-effect of
    ``from nhs_number.X import …``) are filtered out; they are an artifact
    of imports, not part of the documented API.
    """
    import types

    public_attrs = {
        name
        for name in dir(nhs_number)
        if not name.startswith("_")
        and not isinstance(getattr(nhs_number, name), types.ModuleType)
    }
    expected = set(PUBLIC_NAMES)
    unexpected = public_attrs - expected
    missing = expected - public_attrs
    assert not unexpected, (
        f"unexpected public names (add to PUBLIC_NAMES if intended): "
        f"{sorted(unexpected)}"
    )
    assert not missing, f"missing public names: {sorted(missing)}"


def test_public_callables_are_callable():
    for name in [
        "is_valid",
        "generate",
        "standardise_format",
        "normalise_number",
        "calculate_checksum",
        "NhsNumber",
    ]:
        assert callable(getattr(nhs_number, name)), f"{name} is not callable"


def test_public_constants_are_correct_types():
    assert isinstance(nhs_number.REGIONS, dict)
    assert isinstance(nhs_number.Region, type)
    assert isinstance(nhs_number.FULL_RANGE, Range)
    # Every REGION_* alias / region must be a Region instance
    for name in [
        "REGION_UNALLOCATED",
        "REGION_RESERVED",
        "REGION_ENGLAND",
        "REGION_WALES",
        "REGION_IOM",
        "REGION_ENGLAND_WALES_IOM",
        "REGION_SCOTLAND",
        "REGION_NORTHERN_IRELAND",
        "REGION_SYNTHETIC",
        "REGION_EIRE",
    ]:
        assert isinstance(
            getattr(nhs_number, name), nhs_number.Region
        ), f"{name} is not a Region instance"
