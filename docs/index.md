# nhs-number

```python
>>> import nhs_number

# test a valid number
>>> nhs_number.is_valid('1234567891')
True
```

A Python package to provide utilities for NHS Numbers, including validity checks, normalisation, and generation.

This package is a collaboration between a number of individuals, groups and teams, who were each separately maintaining some kind of NHS Number Python package. See [Contributors](./contributors.md) for more information.

While validating an NHS Number is not particularly difficult to achieve in code, it seems wasteful for developers to have to implement their own solutions, and it is likely that many developers will not be aware of the various rules and nuances of NHS/CHI/H&C Numbers across the UK Nations. This package aims to provide a single, well-maintained, and well-documented solution for all developers to use.

## Features

- Validation of NHS Numbers using the check-digit algorithm.
- Normalisation of NHS Numbers from various string formats to a standard 10-digit string format.
- Additional details and information on an NHS number such as the region it is valid for, and the reason it is not valid, if invalid.
- Generation of valid and invalid NHS Numbers for testing purposes, for any selected Region. Note that you should **never** need to generate an NHS Number for a live system (See [Important Note](#important-note) below)

!!! warning "Important note about Scottish CHI Number validation"
At present this library does not reliably validate Scottish CHI Numbers. This is because the first 6 digits of a Scottish CHI Number must be a valid DDMMYY Date of Birth, and this library does not currently check for this. At the moment only the correct number range is checked for.

## Roadmap

- Additional validation for Scottish CHI numbers to ensure the first 6 digits are a valid DDMMYY Date of Birth.
- Generation of valid Scottish CHI numbers along same rules.
- Validation and generation of [IHI Numbers for the Republic of Ireland](ihi-ireland.md), subject to contributors wanting to collaborate on this, and there being a demand for implementation.
