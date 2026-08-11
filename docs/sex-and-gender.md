---
title: Sex and gender in this library
authors: Dr Marcus Baw
---

# Sex and gender in this library

A Scotland CHI number's 9th digit encodes a person's sex by parity: odd for male, even for female. `is_valid()` and `NhsNumber()` can optionally check a number against a supplied sex - this page explains what that check does, why the parameter is called `sex` and not `gender`, and how to skip the check safely for records where sex isn't recorded as a determinate value.

## Why `sex`, not `gender`

NHS's own data standards draw a clear line between these two concepts, and have split what used to be a single field into two:

| Attribute | Meaning |
| --- | --- |
| [`PERSON STATED GENDER CODE`](https://www.datadictionary.nhs.uk/data_elements/person_stated_gender_code.html) | self-declared or inferred **gender** |
| [`PERSON PHENOTYPIC SEX`](https://www.datadictionary.nhs.uk/data_elements/person_phenotypic_sex.html) | biological **sex** |

A CHI number's 9th-digit parity is fixed at the point the number is issued and encodes biological sex, not declared gender identity - so `PERSON PHENOTYPIC SEX` is the standard this library follows, and `sex` is the accurate name for the parameter.

The older, single `PERSON GENDER CODE` field these two replaced has been formally retired:

> "PERSON GENDER CODE will be replaced with PERSON STATED GENDER CODE or PERSON PHENOTYPIC SEX CLASSIFICATION, which is the most recent approved national information standard."
> — [NHS Data Dictionary](https://www.datadictionary.nhs.uk/attributes/person_gender_code.html)

NHS's live Personal Demographics Service (PDS) FHIR API keeps the same distinction: an NHS response on the [developer community forum](https://developer.community.nhs.uk/t/admin-gender-in-pds/8970) states that the API's `gender` field "should not [be] conflated with 'sex at birth'."

## What the check actually does

**One rule governs all behaviour: the check can only ever reduce validity by disagreeing with an actual parity digit on an actual CHI number. In every other circumstance it is inert.**

That single rule covers every case:

- the number isn't a CHI number → `sex` is accepted, but has no effect
- `sex` is a value that can't express a determinate sex (see below) → accepted, no effect
- `sex` is omitted (the default) → no check at all, today's behaviour

Only a determinate `"male"` or `"female"` value, checked against an actual CHI number, can ever flip a result from valid to invalid.

```python
from nhs_number import is_valid

is_valid("0101011113")                    # True  - no sex check
is_valid("0101011113", sex="male")        # True  - 9th digit is odd, matches
is_valid("0101011113", sex="female")      # False - 9th digit is odd, mismatch
is_valid("4000000632", sex="female")      # True  - not a CHI number, sex is ignored
is_valid("0101011113", sex="not_known")   # True  - can't be checked, ignored
```

## Accepted values

Both words and the NHS numeric/letter codes are accepted, so you can pass a value straight from a database column without translating it first:

| Meaning | Word | Retired `PERSON GENDER CODE` | Current `PERSON STATED GENDER CODE` / `PERSON PHENOTYPIC SEX` | Affects the result? |
| --- | --- | --- | --- | --- |
| Male | `"male"` | `1` | `1` | Yes |
| Female | `"female"` | `2` | `2` | Yes |
| Indeterminate / Not Specified | `"indeterminate"` | `9` | `9` | No - inert |
| Not Known | `"not_known"` | `0` | `"X"` | No - inert |

Male and Female are `1`/`2` in every version of the NHS coding, so those two are unambiguous regardless of which standard your data came from. The "not known"/"indeterminate" codes differ between the retired and current standards (`0` vs `"X"`, "Not Specified" vs "Indeterminate") - it doesn't matter which one your data uses, because both are inert here: a single parity digit cannot distinguish "not known" from "indeterminate" from "not specified", so there is nothing to gain by treating them differently.

Words are case-insensitive and tolerate surrounding whitespace (`"Male"`, `" male "`, `"MALE"` all work).

## What happens with an unrecognised value

`sex` is caller-supplied configuration, not the messy real-world data that `nhs_number` itself can be - so unlike an unparseable NHS number (which returns `False`, never raises), an unrecognised `sex` value raises `ValueError`:

```python
is_valid("0101011113", sex="woman")   # raises ValueError
is_valid("0101011113", sex=3)         # raises ValueError
```

This matches the existing convention for other caller-configuration errors in this library, such as passing something other than a `Region` to `generate(for_region=...)`.

This is deliberate: a typo in a hard-coded literal (`"mael"` instead of `"male"`) is a programming bug, and should fail loudly rather than being silently treated as "no check" - which is what would happen if it were ignored instead.

## Using it with `NhsNumber`

`NhsNumber` accepts the same `sex` keyword, with identical behaviour - a mismatch is reflected in `.valid`:

```python
from nhs_number import NhsNumber

NhsNumber("0101011113", sex="male").valid    # True
NhsNumber("0101011113", sex="female").valid  # False
```

## References

- [`PERSON STATED GENDER CODE`](https://www.datadictionary.nhs.uk/data_elements/person_stated_gender_code.html) - NHS Data Dictionary
- [`PERSON PHENOTYPIC SEX`](https://www.datadictionary.nhs.uk/data_elements/person_phenotypic_sex.html) - NHS Data Dictionary
- [`PERSON GENDER CODE`](https://www.datadictionary.nhs.uk/attributes/person_gender_code.html) - NHS Data Dictionary (retired)
- [Personal Demographics Service - FHIR API](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir) - NHS Digital
- [Issue #66](https://github.com/uk-fci/nhs-number/issues/66) - the discussion this design came out of
