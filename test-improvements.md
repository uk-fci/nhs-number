# Test coverage analysis & improvement plan

## Current state

- 42 passing tests, 1 skipped (the `local-test-data` bulk validation test).
- `coverage` reports **100% line and 100% branch** coverage across all 6
  source files.

| File | Stmts | Branch | Cover |
| --- | --- | --- | --- |
| `nhs_number/__init__.py` | 7 | 0 | 100% |
| `nhs_number/constants.py` | 44 | 6 | 100% |
| `nhs_number/details.py` | 20 | 4 | 100% |
| `nhs_number/generate.py` | 24 | 12 | 100% |
| `nhs_number/standardise.py` | 15 | 4 | 100% |
| `nhs_number/validate.py` | 22 | 10 | 100% |
| **TOTAL** | **132** | **36** | **100%** |

100% coverage is misleading here. The tests exercise every line and branch but
do not exercise enough **inputs, boundaries, and error paths**. The gaps below
are ordered roughly by impact.

---

## 1. `details.py` (`NhsNumber`) — biggest gap

Only **one** test (`test_valid_synthetic_nhs_number_details`) exists for this
whole class. Missing:

- **Invalid number behaviour**: when no region matches, `self.region` is never
  set, so accessing `nhs.region` raises `AttributeError`. There is no test
  exposing this — likely a latent bug.
- **Region coverage**: no `NhsNumber` test for Scotland, Northern Ireland,
  England/Wales/IoM, Eire, Reserved, or Unallocated — only Synthetic.
- **Robustness of input parsing**: `NhsNumber.__init__` slices
  `nhs_number[:-1]` and calls `int(nhs_number[-1])` *before* standardising.
  Inputs like `"987 654 3210"`, `"987654321A"`, `9876543210` (int), `""`, or
  `None` will all crash or behave inconsistently. None are tested.
- The doctest in `details.py:46-48` shows a `vars()` output containing a memory
  address (`0x7fcb31de5e90`) — if `--doctest-modules` ever picks it up it
  would fail. It currently isn't running, which is itself worth fixing.

## 2. `constants.py` — no boundary tests

The whole file is "covered" only because other tests happen to walk through
`contains_number`. Critical missing tests:

- **Boundary values** at every range edge:
  `9`, `10`, `9_999_999`, `10_000_000`,
  `3_112_999_999`, `3_113_000_000`,
  `3_199_999_999`, `3_200_000_000`,
  `3_999_999_999`, `4_000_000_000`,
  `4_999_999_999`, `5_000_000_000`,
  `5_999_999_999`, `6_000_000_000`,
  `7_999_999_999`, `8_000_000_000`,
  `8_599_999_999`, `8_600_000_000`,
  `8_999_999_999`, `9_000_000_000`,
  `9_999_999_999`. Off-by-one errors in `Range` are exactly the kind of bug
  that 100% coverage hides.
- **Non-overlap invariant**: no test asserts the regions are mutually
  exclusive, or that their union plus unallocated covers `FULL_RANGE`. A
  property-based test (`hypothesis`) over `FULL_RANGE` would catch any future
  range changes that introduce overlap or gaps.
- **Aliases**: `REGION_ENGLAND`, `REGION_WALES`, `REGION_IOM` are aliases for
  `REGION_ENGLAND_WALES_IOM` (`constants.py:154`). No test pins this.
- `Range` and `Region` classes have no direct unit tests.

## 3. `validate.py` — most regions never exercised

- `is_valid(..., for_region=...)` is only tested for
  `REGION_ENGLAND_WALES_IOM`. Scotland, NI, Eire, Synthetic, Reserved, and
  Unallocated are untested.
- The "checksum == 10 → invalid number" case is mentioned in a comment
  (`validate.py:75-77`) but not tested with a specific identifier known to
  produce checksum 10 (e.g. an identifier where
  `(sum_of_weighted_digits) % 11 == 1`).
- No tests for: `is_valid("")`, `is_valid(None)`, `is_valid(0)`, negative
  ints, floats, very long ints.
- The `"Additional checks for Scotland CHI number DOB validity will go here"`
  comment (`validate.py:68`) flags an unimplemented feature — at minimum,
  decide whether to add a `TODO` test or remove the comment.

## 4. `generate.py` — quantity and region edge cases

- `generate(quantity=0)` — no test (currently returns `[]` cleanly, worth
  pinning).
- `generate(quantity=-1)` — would loop on length check immediately and return
  `[]`, but uncovered.
- `generate(valid=False, for_region=...)` — no test that an invalid generated
  number still falls inside the supplied region's ranges (it should, by
  construction; pin the invariant).
- All regions other than `REGION_ENGLAND_WALES_IOM` are untested for
  `for_region`.
- The `len(checksum_str) == 1` branch (`generate.py:69`) silently discards
  candidates whose checksum is 10 — fine, but the discard path has no explicit
  test.

## 5. `standardise.py` — input-type edge cases

- No test for `None`, `""`, `0`, negative ints, or floats.
- The `int` branch uses `zfill(10)` but **doesn't** validate the regex against
  the result — `standardise_format(0)` returns `"0000000000"` without passing
  through the regex. That's probably a deliberate choice but isn't documented
  or pinned.
- No test for `\t` or `\n` whitespace (`strip()` handles them, but only spaces
  are tested).
- No test for long ints (e.g. `99_999_999_999`) — currently returns `""`
  because the `zfill` is a no-op, but uncovered.

## 6. Public API & cross-module

- No test that `from nhs_number import ...` exposes the documented surface
  (`generate`, `is_valid`, `standardise_format`, `normalise_number`,
  `NhsNumber`, `Region`, `REGIONS`, all the `REGION_*` constants,
  `FULL_RANGE`).
- README/`docs/` examples are not exercised as doctests.
- No property-based tests (hypothesis would be a great fit: "for all 10-digit
  ints, `is_valid(generate(quantity=1)[0])` is `True`").

## 7. Test infrastructure

- `tests/context.py` (sys.path shim) is unused.
- `--doctest-modules` is enabled in `pytest.ini` but no module currently has a
  runnable doctest — either remove the flag or fix the broken example in
  `details.py`.
- No CI check for branch coverage thresholds, so future regressions to
  coverage wouldn't be caught.

---

## Recommended priorities

1. **Add an `NhsNumber` test for invalid input** — likely uncovers a real bug
   where `self.region` is unset.
2. **Add boundary tests for every `Range` edge** in `constants.py`.
3. **Add `for_region` tests covering all regions** in both `is_valid` and
   `generate`.
4. **Add input-type robustness tests** (`None`, `""`, ints, floats) for
   `is_valid`, `standardise_format`, and `NhsNumber`.
5. **Fix or remove the broken doctest** in `details.py` and the unused
   `tests/context.py`.
6. **Add a hypothesis-based property test** asserting region disjointness and
   the round-trip `is_valid(generate(...))`.
