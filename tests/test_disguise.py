import pytest

from nhs_number import disguise, is_valid
from nhs_number.disguise import OrganizationType, _get_organization


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
