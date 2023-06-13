---
title: Individual Health Identifier (IHI) - Ireland
authors: Dr Marcus Baw
---

## What is an IHI?

The Individual Health Identifier (IHI) is a single patient identifier used across the Republic of Ireland. It is a 16-digit [GS1](https://www.gs1.org/industries/healthcare/standards) code, which embeds the 'NHS number' section *within* it.

We were unable to find much detail about the detailed technical structure of the IHI published on the open internet, but following some inquiries we were able to obtain the following information from the HSE:

A subset of NHS Numbers were reserved for the Republic of Ireland. Core IHI numbers align with this bank of numbers and are currently drawn from a range of 81200000n to 85999999n, where `n` is a standard NHS number modulo 11 check digit from 0 to 9.

The **full** IHI number is 18 digits long and the 'core' number (NHS number portion) resides in positions 8 to 17 of the full 18 digit number. There are 2 check digits in place – one at the end of the core 10 digit number (Modulus 11 check) and one at the end of the full 18 digit number (GS1 check digit).

The first seven digits of the GS1 code are intended to ensure that the IHI number is globally unique:

- **Production** – IHI numbers starting with GS1 value ‘5393014’
- **Test** – IHI numbers starting with GS1 value ‘5393054’

```code
IHI number: 5393014 81200000 0 0
            |       |        | |
            GS1     |        | |
            Prefix  Core     | |
                    IHI      | |
                             | GS1 check digit
                             |
                             Modulus 11 check digit
```

## `nhs-number` package support for IHI

At present we consider validation and generation of IHI numbers to be **out of scope** for this project.

We would be very willing to collaborate with any interested parties to add support for IHI numbers to this project.

## Sources / References

- <https://www.hse.ie/eng/about/who/national-services/individual-health-identifier/>

- <https://github.com/uk-fci/nhs-number/issues/9>
