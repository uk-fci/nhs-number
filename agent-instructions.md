# Agent Instructions

`nhs-number` is a Python reference library for standardising, validating, generating, and describing UK NHS-family numbers. It is not a patient-record system: never add real patient identifiers to code, fixtures, documentation, issues, or pull requests.

## Read First

- [README.md](README.md) - project purpose and public API.
- [CONTRIBUTING.md](CONTRIBUTING.md) - local contribution and release workflow.
- [spec/testing.md](spec/testing.md) - test strategy and behavioural invariants.
- [tests/vectors/nhs_number_cases.json](tests/vectors/nhs_number_cases.json) and [tests/test_vectors.py](tests/test_vectors.py) - language-neutral conformance contract and its Python harness.
- [docs/other-languages.md](docs/other-languages.md) - how other implementations consume the vectors.
- [house style](https://github.com/pacharanero/house-style) - shared engineering standards.

## Core Invariants

- The language-agnostic test vector is a published compatibility resource for implementations in other languages. It defines shared checksum, standardisation, validation, region, and range behaviour.
- When a change intentionally affects any vectorised behaviour, update `tests/vectors/nhs_number_cases.json`, its Python harness, and the explanation in the same pull request. Review expected-output changes as carefully as code changes.
- Keep Python-only input robustness and non-deterministic generation/disguise outputs in native property tests, not fixed cross-language vectors. Update [docs/other-languages.md](docs/other-languages.md) if that boundary changes.
- The public import surface is closed and pinned by `tests/test_public_api.py`. Adding or removing a public name is deliberate compatibility work.
- `is_valid()`, `NhsNumber()`, and `standardise_format()` do not raise for unparseable input.

## Workflow

- `s/test` - run the test suite.
- `black --check .` - check formatting.
- `zensical build --clean` - build documentation after documentation changes.
- `s/version++ patch|minor|major` - create the version-bump pull request. Do not manually create release tags.

## Before Every Commit

```sh
pytest --cov=nhs_number --cov-branch --cov-fail-under=100
black --check .
```

## Git Workflow

- Use a descriptive branch and pull request for the protected `main` branch.
- Commit each validated coherent change. Push only when the user explicitly requests it.
- Do not bypass branch protection or deployment approval without explicit user approval.

## Approval Required

- Ask before publishing to PyPI, approving a deployment, deleting remote branches, force-pushing, changing secrets, or bypassing branch protection.
