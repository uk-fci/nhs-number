import sys

import pytest

import nhs_number.disguise  # noqa: F401  (registers the submodule)
from nhs_number import disguise, is_valid

# ``nhs_number.disguise`` resolves to the exported *function*, because the
# package re-exports it under the same name as its module (as it does for
# ``generate``). Reach the module itself through sys.modules so that
# monkeypatching targets the module's globals.
disguise_module = sys.modules["nhs_number.disguise"]
from nhs_number.disguise import (
    OrganizationType,
    _fake_range,
    _get_organization,
)


def test_disguise_is_valid():
    fake = disguise("4000000632", seed=1)
    assert is_valid(fake)


def test_disguise_is_deterministic():
    assert disguise("4000000632", seed=1) == disguise("4000000632", seed=1)


def test_generate_fake_chi_number_is_deterministic():
    assert disguise("0101011113", seed=1) == disguise("0101011113", seed=1)


def test_generate_fake_hsc_number_is_deterministic():
    assert disguise("3200000010", seed=1) == disguise("3200000010", seed=1)


def test_disguise_seed_changes_output():
    fake1 = disguise("4000000632", seed=1)
    fake2 = disguise("4000000632", seed=2)
    assert fake1 != fake2


def test_generate_fake_chi_number_has_99_constraint():
    fake = disguise("0101011113", seed=1)
    assert fake[6:8] == "99"
    assert len(fake) == 10


def test_generate_fake_hsc_number_is_valid():
    fake = disguise("3200000010", seed=1)
    assert is_valid(fake)
    assert len(fake) == 10


def test_get_organization():
    assert _get_organization("0101011113") == OrganizationType.CHI
    assert _get_organization("3200000010") == OrganizationType.HSC
    assert _get_organization("4000000632") == OrganizationType.NHS
    assert _get_organization("9990000018") == OrganizationType.NHS
    assert _get_organization("5000000000") == OrganizationType.UNKNOWN


def test_generate_fake_invalid_input():
    with pytest.raises(ValueError):
        disguise("not-a-number", seed=1)


def test_generate_fake_unknown_range():
    with pytest.raises(ValueError):
        disguise("5000000000", seed=1)


# ---------------------------------------------------------------------------
# Defensive paths
#
# These guard against a future change routing an unexpected organization into
# _fake_range, or a candidate whose checksum can never be a single digit. They
# are unreachable through disguise() today, so they are exercised directly.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "organization", [OrganizationType.CHI, OrganizationType.UNKNOWN]
)
def test_fake_range_rejects_unsupported_organizations(organization):
    """Only NHS and HSC have a numeric fake range.

    CHI numbers are built from a random date by _random_chi_digits, and
    UNKNOWN is rejected earlier by _check_number, so neither has a range.
    """
    with pytest.raises(ValueError, match="Unsupported organization"):
        _fake_range(organization)


def test_disguise_retries_when_checksum_is_ten(monkeypatch):
    """A candidate whose checksum is 10 cannot yield a valid number, so it is
    discarded and another candidate is generated."""
    real_calculate_checksum = disguise_module.calculate_checksum
    calls = []

    def fake_checksum(identifier_digits):
        calls.append(identifier_digits)
        # Reject the first candidate, then defer to the real calculation.
        if len(calls) == 1:
            return 10
        return real_calculate_checksum(identifier_digits)

    monkeypatch.setattr(disguise_module, "calculate_checksum", fake_checksum)

    fake = disguise("4000000632", seed=1)

    assert len(calls) > 1, "the checksum-10 candidate should have been retried"
    assert is_valid(fake)


def test_disguise_raises_if_no_valid_candidate_is_found(monkeypatch):
    """If every candidate is unusable the loop gives up rather than spinning
    or returning an invalid number."""
    monkeypatch.setattr(
        disguise_module, "calculate_checksum", lambda digits: 10
    )

    with pytest.raises(RuntimeError, match="Unable to generate a valid fake"):
        disguise("4000000632", seed=1)
