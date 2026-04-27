# Strict CHI date-of-birth validation

**Status:** draft / not implemented. Tracked at issue
[`#NN`](https://github.com/uk-fci/nhs-number/issues/NN) (replace once
opened).

This document is the design sketch for the feature foreshadowed by the
TODO at `nhs_number/validate.py:68`:

```python
# Additional checks for Scotland CHI number DOB validity will go here
```

## Background

A Scotland CHI number is 10 digits in the format **`DDMMYYsssC`**:

| segment | digits | meaning |
| --- | --- | --- |
| `DDMMYY` | 1–6 | the patient's date of birth |
| `sss`    | 7–9 | 3-digit serial; the 9th digit's parity encodes sex (odd = male, even = female) |
| `C`      | 10  | mod-11 check digit |

The first 6 digits are therefore **structured data**, not opaque, and
the checksum on its own does not catch bad inputs like `321399nnnC`
("32nd March"). Today the library treats CHI numbers as opaque: the
checksum and the range matter, the date does not.

## Goals

1. Offer an **opt-in** stricter validation mode for CHI numbers that
   additionally requires `DDMMYY` to be a real calendar date.
2. **Default behaviour is unchanged.** Existing callers must continue
   to get the current results without code changes.
3. Make the flag scope obvious — it only affects CHI numbers; non-CHI
   inputs are unaffected.

## Non-goals

- We are **not** parsing or exposing the date of birth as a structured
  value (that would be a separate, larger feature — see "Future work"
  below).
- We are **not** checking the sex parity digit. The library has never
  exposed sex information and adding it raises questions about
  presentation, terminology and edge cases that are outside the scope
  of "strict validation".
- We are **not** introducing a new top-level function. The existing
  `is_valid` and `NhsNumber` surface is sufficient with a new keyword.

## Proposed API

A single new keyword argument, `strict_chi_dob`, defaulting to `False`,
on the two functions/classes that take a number:

```python
nhs_number.is_valid(
    nhs_number,
    for_region=None,
    strict_chi_dob: bool = False,
)

nhs_number.NhsNumber(
    nhs_number,
    strict_chi_dob: bool = False,
)
```

`generate(...)` is **not** changed — generated test numbers are random
within a range and need not represent real DOBs. (If a future feature
needs "generate a CHI with a plausible DOB", that's a separate flag —
e.g. `generate_chi(dob_range=...)`.)

## Validation rules

When `strict_chi_dob=True`, the following extra check is applied **only
to numbers that fall inside the Scotland CHI range** (`REGION_SCOTLAND`):

1. Extract digits 1–6 as `DD`, `MM`, `YY`.
2. If `DD`/`MM`/`YY` cannot form a real calendar date (e.g. `31/02/85`,
   `00/01/85`, `29/02/01`), the number is **invalid**.
3. If the resolved date is **in the future** (later than today, in the
   system's local timezone), the number is **invalid**.

Numbers **outside** the Scotland range are unaffected by the flag —
`strict_chi_dob=True` does not turn a non-CHI number into one. This
keeps the flag's scope intuitive: "be strict about CHI dates" rather
than "apply CHI semantics to everything".

## The 2-digit year problem

`YY` is two digits, so `85` could be 1885, 1985, or 2085. We need a
documented rule.

**Proposed rule:** a CHI date resolves to the most recent past century.
That is, given today's year, the resolved 4-digit year is the latest
`19YY` or `20YY` (or `21YY`…) that is **not in the future**.

| `YY` | resolved year (today is in 2026) | rationale |
| --- | --- | --- |
| `00` | 2000 | within reasonable lifespan |
| `26` | 2026 | this year |
| `27` | 1927 | 2027 is in the future |
| `99` | 1999 | 2099 is in the future |

This means strict CHI validation is **time-dependent** — the same input
may become invalid as the year ticks over (a `27` CHI is valid in 2027
but invalid in 2026). That's acceptable for an opt-in strict mode but
worth flagging to users in the docstring.

**Alternative considered:** a hard cutoff (e.g. `YY ≤ 30 → 20YY`, else
`19YY`). Rejected because it requires picking and maintaining an
arbitrary number, and breaks for centenarians born before the cutoff
year of birth.

**Alternative considered:** delegate the decision to the caller via a
`dob_century_cutoff` parameter. Rejected as YAGNI for the strict flag
itself; can be added later as an additional kwarg if a real use case
appears.

## Edge cases the spec must handle

| input | strict result | reason |
| --- | --- | --- |
| `0101000017` (01/01/00, valid checksum) | valid | resolves to 01/01/2000 |
| `2902000026` (29/02/00, valid checksum) | valid | 2000 was a leap year |
| `2902010050` (29/02/01, valid checksum) | invalid | 2001 not a leap year |
| `3102990050` (31/02/99, …) | invalid | 31st of February |
| `0013990050` (00/13/99, …) | invalid | day 0, month 13 |
| `0101270017` (01/01/27, …) **in 2026** | invalid (future) | resolves to 2027 ahead of today |
| `0101270017` (01/01/27, …) **in 2027** | valid (today) | resolves to today |

The fact that some test fixtures will become valid or invalid as the
real-world date moves is a known consequence of the time-dependent
century rule. Tests that exercise the future-date branch must mock or
parameterise the "today" reference (see Test plan).

## Implementation sketch

`validate.py`:

```python
import datetime

def _is_valid_chi_dob(nhs_number: str, today: datetime.date) -> bool:
    dd, mm, yy = int(nhs_number[0:2]), int(nhs_number[2:4]), int(nhs_number[4:6])
    century = today.year // 100 * 100
    while True:
        candidate_year = century + yy
        try:
            d = datetime.date(candidate_year, mm, dd)
        except ValueError:
            return False
        if d <= today:
            return True
        century -= 100  # try the previous century
        if century < 0:
            return False


def is_valid(nhs_number, for_region=None, *, strict_chi_dob=False):
    # ... existing logic ...
    if strict_chi_dob and REGION_SCOTLAND.contains_number(standardised):
        if not _is_valid_chi_dob(standardised, datetime.date.today()):
            return False
    return ...
```

The `today` argument on `_is_valid_chi_dob` is for testability — public
API uses `datetime.date.today()`.

`details.py`'s `NhsNumber.__init__` does the same check and falls back
to `valid=False` if the strict check fails. `region` and
`region_comment` should still reflect the parsed region — i.e. it's
still a Scotland CHI shape, just one with an impossible date.

## Test plan

- Unit tests for `_is_valid_chi_dob` covering every row of the edge
  cases table, including the leap-year cases, the future-date case, and
  the century-rollover case.
- Property: for every CHI generated by `generate(for_region=REGION_SCOTLAND)`,
  `is_valid(..., strict_chi_dob=True)` returns the same result as
  `is_valid(..., strict_chi_dob=False)`. (Generated numbers are random
  within the range; not all will have valid DOBs, so this property
  actually fails for the current `generate` — see "Open questions"
  below.)
- Default behaviour: every existing test in `tests/test_validate.py`
  continues to pass without modification. The new flag is the only
  caller-visible change.
- The `today` reference is parametrized in the unit tests so they don't
  decay with the real-world calendar.

## Open questions

1. **Should `generate(for_region=REGION_SCOTLAND)` produce numbers
   whose first 6 digits are a valid date?** Currently it does not —
   it's a uniform pick from `[10_000_000, 3_112_999_999]`. If we add
   strict validation, callers may expect `is_valid(generate(...),
   strict_chi_dob=True)` to be True. We have three options:
   - Leave `generate` as-is and document that it doesn't produce
     date-valid CHIs.
   - Add a `strict_chi_dob` flag to `generate` that picks a random
     valid date and serial.
   - Make `generate` always produce date-valid CHIs for `REGION_SCOTLAND`.
   I lean toward (1) for the initial PR — minimum scope.

2. **Do we want `NhsNumber` to expose the parsed DOB as a `datetime.date`
   attribute?** Tempting but a real feature increase. Defer.

3. **Should the flag be available on `NhsNumber` only as a constructor
   argument, or also as a class-level toggle?** Constructor argument
   is more idiomatic; reject the class-level alternative.

## Future work (out of scope for this issue)

- Exposing parsed DOB and sex digit as structured attributes.
- A `generate_chi(date_range=...)` helper.
- A configurable century cutoff.
- Corresponding strict-format checks for English / Welsh / NI numbers
  (those identifier formats are *not* date-encoded, so this would be a
  different feature altogether).
