from nhs_number import NhsNumber
from nhs_number.constants import Region


def test_valid_synthetic_nhs_number_details():
    number = NhsNumber("9876543210")

    assert number.nhs_number == "9876543210"
    assert number.identifier_digits == "987654321"
    assert number.check_digit == 0
    assert number.valid == True
    assert number.calculated_checksum == 0
    assert isinstance(number.region, Region)
    assert "test" in number.region.tags
    assert number.region_comment == ("Not to be issued "
                                     "(Synthetic/test patients PDS)")
