---
authors: Dr Marcus Baw, Dr Anchit Chandran
---

The main documentation site is at <https://nhs-number.uk-fci.tech>. Pushes of code to the `main` branch will automatically trigger a publication to Netlify.

Non-`main` branches of the documentation are automatically published to Netlify for review purposes:

* `develop` -> <https://develop.nhs-number.uk-fci.tech>
* `staging` -> <https://staging.nhs-number.uk-fci.tech>

## Material for MkDocs

We use [MkDocs](https://www.mkdocs.org/) along with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

You can suggest changes directly through PRs.

When developing the documentation site, we recommend the use of a linter such as [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) for VSCode to standardise formatting.
