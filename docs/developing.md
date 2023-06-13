---
title: Developing
authors: Dr Marcus Baw
---

## Folder overview

```bash
├── docs/               # documentation source files in Markdown format
├── nhs_number/         # Python package source code
├── tests/              # Python package tests
├── __init__.py
├── LICENSE             # MIT License
├── mkdocs.yml          # configuration file for the Material for MkDocs documentation site
├── netlify.toml        # Netlify build file - required for Netlify to build the documentation site
├── pyproject.toml      # Poetry configuration file - defines dependencies, etc
├── pytest.ini          # pytest configuration file - defines test discovery, etc
├── README.md
├── requirements.txt
├── runtime.txt         # Python version specification for Netlify
└── setup.cfg
```

## Useful URLs

### Github :simple-github

`nhs-number` GitHub repo <https://github.com/uk-fci/nhs-number>

### PyPi :simple-pypi

`nhs-number` on PyPI <https://pypi.org/project/nhs-number/>
`nhs-number` on **Test** PyPi <https://test.pypi.org/project/nhs-number/>

### Netlify :simple-netlify

<https://app.netlify.com/sites/nhs-number/overview>

### uk-fci.tech domain :material-domain

The `uk-fci.tech` domain is managed on NameCheap by @pacharanero

## Documentation

The main documentation site is at <https://nhs-number.uk-fci.tech>. Pushes of code to the `main` branch will trigger a publication to Netlify automatically.

Non-`main` branches of the documentation are automatically published to Netlify for review purposes:

* `develop` -> <https://develop.nhs-number.uk-fci.tech>
* `staging` -> <https://staging.nhs-number.uk-fci.tech>

When developing the documentation site, we recommend the use of a linter such as [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) for VSCode to standardise formatting.

## Testing

This project uses `pytest` for testing. The test suite can be run with:

```bash
poetry run pytest
```

## Building locally

## Publishing to PyPi

Publication to PyPi is handled by GitHub Actions. The workflows are defined in the `.github/workflows` folder.

Pushes of code to the `staging` branch will trigger a publication to Test PyPi.

Pushes of code to the `main` branch will trigger a publication to live PyPi.

## External Documentation References

* Poetry <https://python-poetry.org/docs/>
* Material for MkDocs <https://squidfunk.github.io/mkdocs-material/getting-started/>
* Netlify available build environments <https://docs.netlify.com/configure-builds/available-software-at-build-time/>
