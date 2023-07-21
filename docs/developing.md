---
authors: Dr Marcus Baw
---

## Folder overview

```bash
├── docs/               # documentation source files in Markdown format
├── nhs_number/         # Python package source code
├── tests/              # Python package tests
├── __init__.py
├── LICENSE             # MIT License
├── mkdocs.yml          # Configuration file for the Material for MkDocs documentation site
├── netlify.toml        # Netlify build file - required for Netlify to build the documentation site
├── pyproject.toml      # Poetry configuration file - defines dependencies, etc
├── pytest.ini          # pytest configuration file - defines test discovery, etc
├── README.md
├── requirements.txt
├── runtime.txt         # Python version specification for Netlify
└── setup.cfg
```

## Testing

This project uses `pytest` for testing. The test suite can be run with:

```bash
poetry run pytest
```

<!-- ## Building locally @pacharanero is something meant to go here? -->

## Publishing to PyPi

This project uses [Poetry](https://python-poetry.org/docs/) for dependency management and packaging.

Any edit **MUST** have a new version number otherwise it will be rejected by PyPi.

To publish a new version to PyPi, update the version number in `pyproject.toml`.

Also add a note to the `docs/changelog.md` file to explain the updates.

Publication to PyPi is handled by GitHub Actions. The workflows are defined in the `.github/workflows` folder.

Pushes of code to the `staging` branch will trigger a publication to Test PyPi.

Pushes of code to the `main` branch will trigger a publication to live PyPi.
