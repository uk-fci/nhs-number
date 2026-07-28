---
title: Implementing an NHS Numbers package in other languages
authors: Dr Marcus Baw
---

# Implementing an NHS Numbers package in other languages

**Please do.** NHS number handling should not be reimplemented badly, in a hurry, inside every project that needs it - and it certainly should not be reimplemented from a half-remembered description of the check-digit algorithm. If you are writing an NHS number library for Rust, Go, C#, TypeScript, Java, R, or anything else, you are welcome to build on this work.

To make that easier we publish a **language-agnostic test vector file** that captures how this library behaves.

## The test vectors

[`tests/vectors/nhs_number_cases.json`](https://github.com/uk-fci/nhs-number/blob/main/tests/vectors/nhs_number_cases.json)

It is plain JSON, with one section per behaviour, each a list of inputs and their expected results:

| section | pins |
| --- | --- |
| `calculate_checksum` | the Modulus 11 check digit for an identifier, including the `null` cases and the special checksum-of-10 case |
| `standardise` | cleaning up string input - spaces, hyphens, surrounding whitespace, and what counts as unparseable |
| `standardise_from_int` | integer input, including zero-padding and out-of-range integers |
| `is_valid` | overall validity, including formatted input and CHI date-of-birth rejection |
| `is_valid_for_region` | validity when a specific region is required |
| `region_of` | which region a number falls into |
| `range_boundaries` | the exact start and end of each allocated range |

Each case may carry a `note` explaining *why* it is what it is, which is often the most useful part - several of them encode decisions that are not obvious from the algorithm alone.

If your implementation passes these vectors, it agrees with this library. That is the whole point: a shared, checkable definition of correct, rather than each implementation drifting on its own.

### Using them

Read the JSON in whatever your language's test framework prefers, and drive a table test from it. There is a worked example in [`tests/test_vectors.py`](https://github.com/uk-fci/nhs-number/blob/main/tests/test_vectors.py) - it is the same file being used to check the Python implementation, so the vectors cannot quietly rot.

The `region` and `range` values are names (`"SCOTLAND"`, `"UNALLOCATED_1"`), so map them onto whatever you call those concepts.

## What is deliberately *not* in the vectors

Knowing what has been left out matters as much as what is in:

- **Language-specific input robustness.** The Python library guarantees it never raises on odd input - `None`, a list, a float, an arbitrary object all just come back invalid. That is a Python-shaped promise; your language will have its own idea of what "unparseable input" means, so it is tested natively rather than in the shared vectors.
- **Random generation.** `generate()` returns random numbers, so there is nothing fixed to pin. What you should assert instead are the *properties*: every generated number is valid, falls inside the requested region, and - with no region given - comes from the synthetic/test range and never a live one.
- **`disguise()` output.** Deliberately excluded, and worth explaining. The fake number is derived from a seeded pseudo-random generator, so reproducing our exact outputs would mean reimplementing CPython's Mersenne Twister bit-for-bit *and* consuming it in exactly the same order. That would be pinning an implementation detail, not a behaviour. Assert the properties instead:
    - the same real number and seed always give the same fake
    - a different seed gives a different fake
    - the fake is itself a valid number
    - an NHS number's fake comes from the synthetic range, so it can never collide with a live number
    - a CHI number's fake is CHI-shaped, with digits 7-8 set to `99`, and carries a *different* date of birth - the original date is not preserved, because a date of birth is identifying in its own right
    - unparseable input, and numbers from ranges that are not supported, raise rather than returning something wrong

## Licence and attribution

This project is **MIT licensed**, and that covers the test vectors as much as the code. In practice:

- **You may use the vectors freely**, including in a commercial product, and including in a library that competes with this one. You do not need to ask.
- **Attribution is appreciated but not required.** If you found this useful, a line in your README saying your implementation is checked against the vectors from [uk-fci/nhs-number](https://github.com/uk-fci/nhs-number) is genuinely helpful to us - it is how other people find the project, and how we find out our work was worth doing. But it is a courtesy, not a condition. Build the thing.
- **We would love to know.** Open an issue or a discussion to tell us your implementation exists and we will link it from these docs. If you find a case where our vectors are wrong, or a case we should have covered, that is one of the most valuable contributions you can make - please raise it.

## Before you start

Two documents will save you time:

- [About NHS Numbers](nhs-numbers.md) - the number ranges, and the Modulus 11 check digit algorithm in full
- [Walkthrough](walkthrough.md) - what the library actually does, with real worked examples

And two things that catch people out:

1. **CHI (Scottish) numbers are not opaque.** Their first six digits are a date of birth as `DDMMYY`, so a CHI number containing an impossible date is invalid however good its check digit is. Note also that two-digit years are ambiguous, and a `29/02/YY` case can hinge on which century you resolve to.
2. **A checksum of 10 means the number is invalid.** There is no single digit that can match it, so those identifiers can never form a valid number. It is an easy branch to get subtly wrong, and it is covered in the vectors.
