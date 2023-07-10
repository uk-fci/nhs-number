---
title: Usage
authors: Dr Marcus Baw, Matt Stibbs
---

--8<--
docs/_assets/_snippets/live-usage-warning.md
--8<--

## `is_valid()`

Returns `True` if the NHS Number is valid, `False` if not.

**Arguments**:

- `nhs_number` (*required, `str`*): The NHS Number to validate. Valid formats are:
      - `123 456 7890`
      - `123-456-7890`
      - `1234567890`
- `for_region` (*optional, default=None, `Region`*): If provided, additionally validates number is included within the given [`Region`](#regions) range.

```python
import nhs_number

nhs_number.is_valid('4698194180')
# True

nhs_number.is_valid('1234567890')
# False
```

The `for_region` parameter takes any of the [`nhs_number.REGION_*`](#regions) constants:

```python
nhs_number.is_valid('7709030025', for_region=nhs_number.REGION_ENGLAND)
# True
```

--8<--
docs/_assets/_snippets/scottish-chi-number.md
--8<--

## `normalise_number()`

Returns normalised 10-digit NHS Number without spaces, as a string.

**Arguments**:

- `nhs_number` (*required, `str | int`*): The NHS Number `int` or `str` to normalise.

```python

import nhs_number

nhs_number.normalise_number('123 456 7891')
# '1234567891'

nhs_number.normalise_number('1234567891')
# '1234567891'

nhs_number.normalise_number('123-456-7890')
# '1234567890'
```

## `generate()`

Returns list of valid or invalid normalised NHS numbers, as strings, for testing.

**Arguments**:

- `valid` (*optional, default=True, `bool`*): Determines whether generated numbers are valid or invalid.
- `for_region` (*optional, default=None, `Region`*): If provided, generates numbers within the given [`Region`](#regions) range.
- `quantity` (*optional, default=1, `int`*): Determines number of NHS number strings returned.

```python
import nhs_number

nhs_number.generate()
# ['1633104249']

nhs_number.generate(quantity=5)
# ['1633104249', '1633104257', '1633104265', '1633104273', '1633104281']
```

The `for_region` parameter takes any of the [`nhs_number.REGION_*`](#regions) constants:

```python
nhs_number.generate(for_region=nhs_number.REGION_ENGLAND)
# ['7709030025']
```



## Regions

You can obtain Region objects via the package's `REGION_*` constants. See [NHS Number Ranges](nhs-numbers.md#nhs-number-ranges) for details on ranges.

Obtain a dictionary of available `Range` objects:
```python
import nhs_number

nhs_number.REGIONS
# {'UNALLOCATED': <nhs_number.constants.Region object at 0x7fda8e0b0e50>, 'SCOTLAND': <nhs_number.constants.Region object at 0x7fda8e0b0d10>, 'NORTHERN_IRELAND': <nhs_number.constants.Region object at 0x7fda8e0b0d90>, 'ENGLAND_WALES_IOM': <nhs_number.constants.Region object at 0x7fda8e0b0d50>, 'RESERVED': <nhs_number.constants.Region object at 0x7fda8e0b0e90>, 'EIRE': <nhs_number.constants.Region object at 0x7fda8e0b0dd0>, 'SYNTHETIC': <nhs_number.constants.Region object at 0x7fda8e0b0e10>}
```

Get a Region object for England:
```python
nhs_number.ENGLAND_WALES_IOM
# <nhs_number.constants.Region object at 0x7fda8e0b0d50>
```

Each Region has some aliases for ease of use:
```python
nhs_number.ENGLAND_WALES_IOM == nhs_number.REGION_ENGLAND
# True
```

--8<--
docs/_assets/_snippets/scottish-chi-number.md
--8<--
