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
├── mkdocs.yml          # Configuration file for the Zensical documentation site
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

This project uses [Poetry](https://python-poetry.org/docs/) for dependency management and packaging, and publication is handled by GitHub Actions - the workflows are in the `.github/workflows` folder.

**There is one release command, `s/version++`, and the full process is documented in [Cutting a release](releasing.md).** Start there.

In brief: landing a version bump on `main` is what releases the package. An ordinary merge that does not change the version in `pyproject.toml` publishes nothing, so documentation and CI changes can be merged freely. When the version does change, the publish workflow creates the tag and starts the PyPI upload, which then waits for a deployment approval on the `release` environment.

To smoke-test a build on Test PyPi, run the **Publish library to TEST.pypi.org** workflow manually from the Actions tab, choosing whichever branch or tag you want. (This replaced an older `staging` branch, which drifted behind `main` and kept catching contributors out by becoming the base branch for their pull requests.)
