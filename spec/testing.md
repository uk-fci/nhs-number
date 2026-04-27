# Testing strategy

This document describes the intent behind the test suite for `nhs_number`.
It is the answer to "what counts as a good test in this repo, and why?".
The goal is a suite that catches real regressions, surfaces ambiguities in
the spec, and pins behaviour explicitly enough that future maintainers can
change the code with confidence — not a suite that exists to satisfy a
coverage number.

## Principles

### 1. Coverage is a floor, not a ceiling

The package previously hit 100% line and branch coverage with 42 tests, yet
contained a latent `AttributeError` in `NhsNumber`, an order-of-magnitude
boundary error between two ranges (issue #59), and several input types that
crashed `is_valid` instead of returning `False`. Coverage measures whether a
line *executed*; it does not measure whether anything *was asserted about
it*. Treat the coverage report as a check that no whole branch is unloved,
not as proof that the code is correct.

### 2. Tests must fail when the code is wrong

Every test should be specific enough that flipping a related line of source
code makes it fail. In practice:

- Assert exact values (`region is REGION_SCOTLAND`), not just truthiness
  (`region is not None`). Identity-vs-truthiness is the difference between
  catching "the wrong region was returned" and not.
- When you parametrize, include a **negative** case alongside the positive.
  `is_valid(in_range, for_region=R)` returning `True` is much weaker
  evidence than the *pair* (in-range → True, out-of-range → False).
- Sanity-assert your fixtures. If a "checksum-valid number outside region X"
  fixture has a *bad* checksum, the negative test passes for the wrong
  reason.
- Pin the special cases (`is_valid(0) == True`, `calculate_checksum("000000006") == 10`)
  so they read as deliberate design decisions, not accidents.

### 3. Red-Green for new behaviour

When a test exposes a bug, write it first against unmodified source and
confirm it fails. Then change the source. The commit message should make
clear that the test was red before being green. This prevents the
"I wrote the test after the fix and it accidentally always passed"
failure mode.

For *characterisation* tests — pinning behaviour that is already correct —
red-green doesn't apply. Mark them clearly so future readers know this is
intentional pinning, not bug-fix evidence.

### 4. Standard library only

The suite uses `pytest` and Python's standard library. No `hypothesis`, no
`freezegun`, no fixtures from third-party plugins. The reasoning:

- The library has only two maintainers; every dependency is a long-term
  cost.
- Boundary tests against an explicit list of values are clearer to read
  than property-based assertions for this domain — there are only ~10
  ranges.

If a future change makes property-based testing genuinely worthwhile
(e.g. a new public function with a non-trivial input domain), introduce
`hypothesis` deliberately, with the change documented here.

### 5. Public API surface is a closed set

`tests/test_public_api.py` asserts both that every documented name is
importable AND that no *unexpected* public name has appeared. This means
adding a new public name fails the test until it is registered in
`PUBLIC_NAMES`. Removing a public name is a breaking change and should be
coordinated with a major version bump.

## What we test

### Boundaries

For every range, every value, and every input domain we consider:

- The exact start and end values (pinned).
- Inclusivity at both endpoints (per the documented contract).
- `start - 1` and `end + 1` — the off-by-one classic.
- The values just below the documented universe (`< FULL_RANGE.start`) and
  just above (`> FULL_RANGE.end`).

### Input robustness

Every public function that accepts user input must handle, without
raising, at least:

- `None`
- The empty string `""`
- Whitespace-only strings (`"   "`, `"\t"`, `"\n"`)
- Garbage strings (`"abc"`, `"987654321X"`)
- Floats (`3.14`, `-1.0`)
- Negative ints (`-1`, `-1234567890`)
- Very long ints (`> 10` digits)
- `0`
- `bool` (which is a subclass of `int` in Python and would otherwise
  silently slip through `isinstance(..., int)`)
- Lists, dicts, arbitrary objects

The contract is "return `False` (or construct cleanly with `valid=False`),
never raise". This is enforced at the lowest layer — `standardise_format`
returns `""` for any input it cannot parse — so callers never need their
own try/except.

### Invariants

- **Region non-overlap** — every documented boundary value belongs to
  exactly one `Region`. Sweeped in `tests/test_constants.py`.
- **`generate(valid=False, for_region=R)`** — invalid numbers must still
  fall inside `R`'s ranges. The `valid` flag must only affect the check
  digit, never the range.
- **`generate(valid=True)`** — every number returned passes `is_valid`
  (tested at scale, n=1000+).
- **`is_valid` orthogonality** — without `for_region`, `is_valid` only
  checks the checksum; the question "is this in an issuable range?" is
  separate and answered by `for_region` or `NhsNumber.region`. Pinned
  explicitly because it's a common source of confusion.

### Special cases

- **Checksum == 10** — the formula can produce 10 for some 9-digit
  identifiers; no single check digit can match, so all 10 candidate full
  numbers must be rejected. Pinned via a known-checksum-10 identifier
  (`"000000006"`) and parametrized over all 10 candidate check digits.
- **`is_valid(0)` returning `True`** — `0` zero-fills to `"0000000000"`
  whose checksum is 0. Pinned with a docstring explaining why.

### Public API surface

`tests/test_public_api.py` pins:

- The list of importable top-level names.
- The kind of object each is (callable vs constant vs type).
- That no unexpected public name has leaked.

## What we deliberately don't test

- **Implementation internals.** Test the contract, not the algorithm. The
  weighting in `calculate_checksum` is the modulus-11 spec; if it ever gets
  rewritten to be more efficient, our tests should keep passing.
- **Random output reproducibility.** `generate` uses the system random; we
  test invariants over batches (every number is valid, every number is in
  region) rather than pinning specific outputs.
- **Doctest in non-public modules.** Doctests are a documentation aid for
  the library's public surface — `NhsNumber`'s usage example is one. We
  don't add doctests purely to bump coverage.

## Tripwires

Some tests are written specifically as **tripwires** — they pass today
against known-buggy code, with an inline comment pointing at the open
issue. The intent is that whoever fixes the underlying bug must update the
test in the same commit, making the test update part of the conscious
review surface rather than a separate forgotten step.

Active tripwires:

- `tests/test_constants.py::ALL_RANGES` — `RANGE_UNALLOCATED_1.end` and
  `RANGE_SCOTLAND.start` pinned at the (incorrect) code values rather than
  the docstring/CHI-spec values. See **issue #59**.

When adding a new tripwire:

1. Pin the *current* (incorrect) value.
2. Add `# see issue #X` next to the pinned value.
3. Reference the issue number from this document.

## Test organisation

```
tests/
├── test_constants.py        # Range / Region boundaries and invariants
├── test_details.py          # NhsNumber class
├── test_generate.py         # generate() — quantity, regions, invariants
├── test_public_api.py       # importable surface
├── test_standardise.py      # standardise_format / normalise_number
├── test_validate.py         # is_valid + calculate_checksum
├── test_bulk_validation.py  # 909,090 known-valid numbers from local dataset
└── local-test-data/         # synthetic NHS numbers, committed to repo,
                             # excluded from the published wheel via
                             # pyproject.toml's `exclude` rule
```

In-package doctests live in `nhs_number/details.py` (the `NhsNumber` usage
example) and are collected via `--doctest-modules` (configured in
`pytest.ini`). Add new doctests sparingly and only as documentation for the
public surface.

### Bulk-validation dataset

`tests/local-test-data/testdata-909090-valid-nhs-numbers.csv` contains
909,090 known-valid synthetic NHS numbers (all in the `999…` synthetic
range — no real patient data). It's used by `test_bulk_validation.py` as a
backstop against any change that breaks `is_valid` for inputs that look
nothing like the small set we hand-craft elsewhere.

The dataset is committed to the repo deliberately (commit `713268d`,
June 2023) and excluded from the published PyPI package via
`pyproject.toml`'s `exclude` rule, so library consumers don't pay the
download cost. The bulk test runs by default; the cost is ~1.5s on a
modern machine.

If you add another opt-in or large-dataset test, follow these rules to
avoid the gotcha that hid the bulk test as a silent skip for ~3 years:

1. **Resolve dataset paths via `__file__`**, not relative to the cwd.
   `os.path.join(os.path.dirname(__file__), "local-test-data", "...")`
   works regardless of where pytest is invoked from. A bare relative path
   like `"local-test-data/..."` skips silently if the test is run from a
   subdirectory or via an IDE.
2. **Have the `skipif` reason name the path** it's looking for. A reason
   like "dataset not present" is mute; "dataset not found at
   /full/path/here.csv" tells the developer immediately whether the
   skipif itself is wrong.
3. **Periodically check skips aren't load-bearing.** A test that always
   skips is a test that doesn't exist. `pytest -rs` (or the existing
   `-r a` in `pytest.ini`) makes skips visible in the summary — read
   them.

## Running tests

```bash
# Standard suite
s/test
# or, equivalently:
python -m pytest

# With coverage
python -m pytest --cov=nhs_number --cov-branch --cov-report=term

# A single file or pattern
s/test tests/test_constants.py
s/test -k for_region
```

`tests/test_bulk_validation.py` runs by default and adds ~1.5s to the
total runtime. It uses the dataset committed at
`tests/local-test-data/` — see the **Bulk-validation dataset** section
above for context. If you've removed or moved the dataset locally, the
test skips with a path-specific reason rather than failing.

## Acceptance criteria for new tests

A test belongs in this suite if it:

1. Asserts a specific, observable outcome — not just "didn't crash".
2. Would fail if a related line of source code were wrong.
3. Either (a) was red before a code change was made, or (b) explicitly
   pins existing behaviour and says so in a comment.
4. Doesn't depend on test order or shared mutable state.
5. Runs in milliseconds (the whole suite should stay under a couple of
   seconds; `test_bulk_validation` is the one deliberate exception).

A test does **not** belong if it:

- Only exists to bump coverage.
- Asserts an implementation detail (an internal function, a private name,
  a specific algorithm).
- Repeats what a more specific test already covers.
- Relies on system clock, network, or filesystem state outside `tests/`.
