---
title: Changelog
authors: Dr Marcus Baw
---

## 2.0.1

- Adds a `py.typed` marker (PEP 561) so type-checkers and IDEs pick up the package's type annotations when it is installed as a dependency. No API or behaviour change. Resolves #65.

## 2.0.0

**Breaking changes** to CHI number validation and to `generate()`. The changes make the library more accurate for real-world use; callers relying on the previous behaviour may see different results.

- **CHI (Scotland) numbers now validate the date of birth.** A CHI number encodes the date of birth in its first 6 digits as `DDMMYY`. A number in the Scotland CHI range whose date segment is not a real calendar date is now reported as invalid by `is_valid()` and `NhsNumber`; previously only the checksum and range were checked. The check is applied by default - a CHI number is either valid or it is not, there is no opt-out. Resolves #25.
- **`generate()` now defaults to the synthetic / test range** instead of the full range of all NHS numbers, so a generated number can never be mistaken for a live NHS number. Pass `for_region=` to target a specific region; `generate(for_region=REGION_SCOTLAND)` produces CHI numbers with a valid date of birth. Resolves #24.
- **Corrects the Scotland CHI range boundary** (#59): the range now starts at `100_000_000` (the smallest plausible CHI, 01/01/00), not `10_000_000`, matching the module docstring and the CHI specification. Numbers in `10_000_000`-`99_999_999` are now correctly classified as unallocated rather than Scotland CHI.
- Removes the documentation warnings about CHI numbers being unsupported.
- No change to the public import surface.

## 1.4.0

- Major test robustness pass: increases the suite from 42 to 200 tests while maintaining 100% line and branch coverage, adding boundary, invariant, region-coverage, checksum-edge, input-type, and public-API tests. Adds `spec/testing.md` documenting the testing strategy and conventions.
- `is_valid()`, `NhsNumber()`, and `standardise_format()` no longer raise on unexpected input. Previously `None`, integers, pre-formatted strings (e.g. `"987 654 3210"`), empty strings, and other unsupported types could raise an exception; they now return `False` / construct cleanly / return `""` as documented.
- `NhsNumber` now standardises its input before parsing, and sets `region` to `None` for numbers that fall outside all known ranges (previously accessing `.region` raised `AttributeError`).
- Fixes the in-package doctest so `pytest --doctest-modules` actually collects and runs it.
- No public API surface change: all previously-supported calls behave identically.

## 1.3.10

- Fixes artifact naming and the `repository_url` key (normalised hyphenated form) in the PyPI / test.pypi publishing workflows so automated publishing succeeds. No changes to the `nhs_number` library code.

## 1.3.9

- Fixes the `packages-dir` path in the test.pypi publishing workflow, tidies workflow formatting, and bumps `actions/cache`. No changes to the `nhs_number` library code.

## 1.3.8

- Adds the `s/version++` script to automate version bumping and tagging, extends Dependabot to pip dependencies, adds Python 3.13 to the publishing CI, and clarifies the mkdocs configuration. No changes to the `nhs_number` library code.

## 1.3.7

- Migrates the documentation site from MkDocs to Zensical (including the GitHub Pages deployment), adds Dependabot for GitHub Actions, bumps the pinned GitHub Actions across the workflows, and adds the PyPI and test.pypi publishing workflows. No changes to the `nhs_number` library code.

## 1.3.6
- Adds Python 3.13 to the supported versions which are tested in the GitHub Action CI/CD pipeline. No versions have been removed.
- Adds a Github Action workflow to publish the documentation site to GitHub Pages.
- Removes the now-defunct `uk-fci.tech` domain in all of this package, replacing with (for now) uk-fci.github.io until we decide what to do with the `uk-fci` GH organisation.
- Removes all references to Netlify, as we no longer use it for the documentation site.

## 1.3.5

- Adds Python 3.12 to the supported versions which are tested in the GitHub Action CI/CD pipeline.
- Removes Python 3.7 from the supported versions which are tested in the GitHub Action CI/CD pipeline.
- Adds a source document regarding the NHS number specification to the docs/_source-documents folder.
- Upgrades all GitHub Actions within workflows (eg `actions/checkout@v3`) to latest version of the Node 20-based actions

## 1.3.4

- Revert of the new logo, minor edits to the documentation, accepted Anchit PR
- Reverted to plain code rather than Carbon for the code snippets.
- No changes to Python code

## 1.3.3

- Aesthetic documentation updates

## 1.3.2

- GitHub action for CI/CD to publish to live PyPi
- Minor documentation updates

## 1.3.1

- Changed to Netlify for documentation site deployment
- GitHub action for CI/CD to publish to Test PyPi

## 1.3.0 (Refactor, June 2023)

- GitHub repo is transferred from Andy Law to the Faculty of Clinical Informatics.
- Extensive refactor to add new features such as generation of NHS numbers.
- Adds documentation site published to GitHub Pages with GitHub Actions publication.
- Adds GitHub Actions for CI/CD to publish to PyPI.
- Python version support added for 3.11
- Python version support dropped for 3.5, Python 2, etc

## 1.2.2

- Adds support for additional Python versions (3.8, 3.9, 3.10).

## 1.2.1

- Original package is known as `nhs-number` on PyPI and [NhsNumberChecks](https://github.com/andylaw/NhsNumberChecks) on GitHub.
