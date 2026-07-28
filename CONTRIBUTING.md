# Contributing

Thanks for considering a contribution to `nhs-number`. This is a small library maintained by a couple of people in their own time, and pull requests, issues and questions are all welcome.

## Branching: everything targets `main`

**There is one long-lived branch: `main`.** Please branch from `main` and open your pull request against `main`.

There is no `develop` or `staging` branch. Both previously existed, drifted a long way behind `main`, and repeatedly caught contributors out - a pull request opened against one of them shows dozens of unrelated files as though they were your changes. If you have an older fork that still has those branches, delete them and re-branch from an up-to-date `main`.

If you find your PR shows far more changed files than you expected, that is almost always the symptom of a stale base branch. Rebase onto current `main` and it should shrink to just your work.

## Getting set up

```bash
git clone https://github.com/uk-fci/nhs-number.git
cd nhs-number
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Before you open a pull request

Three things run in CI and will block a merge if they fail, so it is worth running them locally first.

**1. Tests, with 100% coverage.** The suite must pass and coverage must stay at 100% for both lines and branches:

```bash
pytest --cov=nhs_number --cov-branch --cov-fail-under=100
```

The 100% requirement is deliberate but is treated as a floor, not a goal - see [`spec/testing.md`](spec/testing.md) for the testing philosophy, including how we pin behaviour and what we deliberately do not test. If your change adds a defensive branch that genuinely cannot be reached, say so in the PR rather than contriving a test for it, and we will work out the right answer together.

**2. Formatting with black.** Line length is 79, configured in `pyproject.toml`:

```bash
black .
```

**3. The shared test vectors.** `tests/vectors/nhs_number_cases.json` freezes the library's core behaviour (checksum, standardisation, validation, region detection, range boundaries) in a language-agnostic form, so that ports in other languages can be checked against the same contract. If you intentionally change any of that behaviour, update the vectors in the same pull request and explain why.

Optionally, `tox` will run the suite across the supported Python versions plus the formatting check, if you have those interpreters available:

```bash
tox
```

## Changelog and versioning

If your change should be released, bump the version and add a changelog entry. Use the helper script, which takes `patch`, `minor` or `major`:

```bash
s/version++ patch
```

It refuses to run unless `docs/changelog.md` already contains a `## <new version>` section, so **write the changelog entry first**. Every released version has an entry; please keep it that way.

Not every change needs a release. Documentation-only and CI-only changes are usually merged without a version bump.

## How releases happen

Merging to `main` triggers the PyPI publish workflow. The upload step is gated behind a manual deployment approval on the `release` environment, so nothing reaches PyPI without a maintainer approving it.

To smoke-test a build on Test PyPI first, run the **Publish library to TEST.pypi.org** workflow manually from the Actions tab against any branch or tag.

## Conventions worth knowing

- **GitHub Actions are pinned to a full commit SHA** with a trailing `# vX.Y.Z` comment, rather than a mutable tag. A tag can be re-pointed if an action's repository is compromised; a SHA cannot. Dependabot keeps the pins current. If you add a step, pin it the same way and confirm the SHA from the action's repository rather than from memory.
- **Public API is a closed set.** `tests/test_public_api.py` pins every name exported from the package, so adding one is a deliberate decision and removing one is a breaking change. If you add a public name, add it to that test too.
- **Input handling never raises.** `is_valid()`, `NhsNumber()` and `standardise_format()` return `False` / construct cleanly / return `""` for input they cannot parse, rather than throwing. Please preserve that.

## Issues

Bug reports, questions and feature ideas are all welcome in [GitHub Issues](https://github.com/uk-fci/nhs-number/issues). For a bug, the most useful thing you can include is the exact input and what you expected to happen - NHS numbers are full of edge cases, and a concrete example is worth a lot.

Please do not include real patients' NHS numbers in issues, pull requests, tests or documentation. Use `generate()`, which produces numbers from the synthetic/test range by default.

## Licence

By contributing, you agree that your contributions will be licensed under the [MIT Licence](LICENSE) that covers this project.
