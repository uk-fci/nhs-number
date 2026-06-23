import pytest

from nhs_number import standardise_format, normalise_number


def test_format_basic():
    num_string = "0123456789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_basic_pad_right():
    num_string = "0123456789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_basic_pad_left():
    num_string = " 0123456789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_basic_pad_both():
    num_string = " 0123456789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_internal():
    num_string = "012 345 6789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_internal_pad_right():
    num_string = "012 345 6789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_internal_pad_left():
    num_string = " 012 345 6789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_internal_pad_both():
    num_string = " 012 345 6789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_internal_invalid_format():
    num_string = "01 2345 6789"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_hyphen():
    num_string = "012-345-6789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_hyphen_pad_right():
    num_string = "012-345-6789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_hyphen_pad_left():
    num_string = " 012-345-6789"
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_hyphen_pad_both():
    num_string = " 012-345-6789 "
    expected = "0123456789"
    assert expected == standardise_format(num_string)


def test_format_hyphen_invalid_format():
    num_string = "01-2345-6789"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_mixed():
    num_string = "012 345-6789"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_short():
    num_string = "012345678"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_long():
    num_string = "01234567890"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_letters():
    num_string = "ABCDEFGHIJ"
    expected = ""
    assert expected == standardise_format(num_string)


def test_format_10_digit_int():
    number = 1234567890
    expected = "1234567890"
    assert expected == standardise_format(number)


def test_format_11_digit_int():
    number = 12345678901
    expected = ""
    assert expected == standardise_format(number)


def test_format_9_digit_int():
    number = 123456789
    expected = "0123456789"
    assert expected == standardise_format(number)


def test_normalise_deprecated():
    with pytest.deprecated_call():
        # noinspection PyDeprecation
        normalise_number("1234567890")


# ---------------------------------------------------------------------------
# Defensive handling of unsupported input types
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_input", [
    None,
    3.14,
    -1.0,
    [],
    {},
    set(),
    (1, 2, 3),
    object(),
    True,            # bool is a subclass of int but never a meaningful NHS num
    False,
])
def test_format_unsupported_types_return_empty_string(bad_input):
    """Unsupported input types must return "" rather than raising.

    This pins the contract that callers (is_valid, NhsNumber) rely on:
    standardise_format never raises for any input.
    """
    assert standardise_format(bad_input) == ""


def test_format_negative_int_returns_empty_string():
    """Negative ints zfill to a 10-char string starting with '-', which fails
    the format regex and so returns "" — pinning this so the behaviour can't
    silently change.
    """
    assert standardise_format(-1) == ""
    assert standardise_format(-1234567890) == ""


def test_format_zero_returns_zero_padded_string():
    """An int of 0 zfills to '0000000000' which matches the format regex.

    Note: this is structurally a "valid format" 10-digit string but is below
    FULL_RANGE.start (10) and so cannot be a real NHS number. is_valid()
    only checks checksum (without for_region) so it returns True for this
    input — see test_validate.test_is_valid_zero_int_pinned_behaviour.
    """
    assert standardise_format(0) == "0000000000"


def test_format_internal_tab_and_newline_whitespace():
    """strip() removes \\t and \\n in addition to spaces — pin this since
    only spaces are tested above.
    """
    assert standardise_format("\t1234567890\n") == "1234567890"
    assert standardise_format("\n\n1234567890\t\t") == "1234567890"
