---
title: Cutting a release
authors: Dr Marcus Baw
---

# Cutting a release

**There is one release command, and the whole job is choosing `patch`, `minor` or `major`:**

```bash
s/version++ minor
```

Everything else - the version bump, the tag, the build, and the upload to PyPI - follows from that. You never tag by hand, and you never upload to PyPI by hand.

## The one rule to remember

**Landing a version bump on `main` is the release.** Nothing else publishes.

That is why an ordinary pull request - a bug fix, a docs tweak, a CI change - can be merged freely without publishing anything. Only a commit that changes `version` in `pyproject.toml` starts a release. If you do not bump the version, nothing is published, and that is the normal case for most merges.

## Releasing, step by step

### 1. Write the changelog entry first

Add a section to the top of `docs/changelog.md` for the version you are about to release:

```markdown
## 2.1.0

- Describe what changed, in terms a user of the library would care about.
- Note anything breaking prominently.
```

This comes first on purpose. `s/version++` refuses to run if the entry is missing, so the changelog can never drift behind the releases.

Commit the changelog entry (via a normal pull request, along with the change it describes, or on its own).

### 2. Choose the bump and run the command

From an up-to-date, clean `main`:

```bash
git switch main && git pull

s/version++ patch    # 2.0.1 -> 2.0.2   bug fixes, docs, internal changes
s/version++ minor    # 2.0.1 -> 2.1.0   new features, backwards-compatible
s/version++ major    # 2.0.1 -> 3.0.0   anything that breaks existing callers
```

Running it with no argument does a `patch`.

**What counts as breaking in this project:** a change to what `is_valid()` returns for an input that previously validated, a change to the ranges in `constants.py`, a change to the default behaviour of `generate()`, or removing anything from the public API pinned in `tests/test_public_api.py`. When in doubt, prefer `major` - the whole point of the version number is to warn people.

The script checks that you are on a clean, up-to-date `main`, that the changelog entry exists, and that the version has not already been released. Then it commits the bump as `chore(release): X.Y.Z` and, because `main` is branch-protected, pushes a `release/X.Y.Z` branch and opens a pull request for it.

### 3. Merge the release pull request

Get it reviewed as normal, then **merge it with a merge commit, not a squash**. (Squashing rewrites the `chore(release):` commit message, which makes the release history harder to follow.)

Merging is the moment the release happens.

### 4. Approve the deployment

The publish waits for a human. Go to the **Actions** tab, open the running **Auto-tag and release on version bump** workflow, and approve the deployment to the `release` environment.

Nothing reaches PyPI until someone approves this, which is the last chance to stop a release.

!!! warning "Approve it reasonably promptly"
    A pending deployment approval **expires after 30 days** and the run is then marked as failed. This has bitten us: version 2.0.1 sat unpublished for a month because its approval was never given. If that happens, see the troubleshooting section below - it is recoverable.

### 5. Check it worked

- The tag `vX.Y.Z` exists in the repository
- The new version appears on [PyPI](https://pypi.org/project/nhs-number/)
- `pip install nhs-number==X.Y.Z` works

## What happens under the hood

```
s/version++ minor
        │
        ├─ checks: clean main, changelog entry exists, version not already released
        ├─ bumps pyproject.toml, commits "chore(release): 2.1.0"
        └─ opens the release/2.1.0 pull request
                │
          (you merge it)
                │
                ▼
   auto-tag.yml   (runs on every push to main)
        │
        ├─ reads the version from pyproject.toml
        ├─ is there already a tag for it?  ──yes──▶  stop, nothing to release
        └─ no ▶ create the tag, then call…
                │
                ▼
   pypi-publish.yml
        ├─ build the distribution
        └─ upload to PyPI  ◀── waits for your approval on the `release` environment
```

The "is there already a tag for it?" check is what makes documentation-only and CI-only merges safe: the version has not changed, so its tag already exists, and the workflow stops without publishing.

## Testing a build before releasing

To put a build on [Test PyPI](https://test.pypi.org/project/nhs-number/) first, run the **Publish library to TEST.pypi.org** workflow manually from the Actions tab, choosing whichever branch or tag you want. This is a smoke test only; it does not affect the real release.

## Troubleshooting

**"I merged my pull request but nothing was published."**
That is the expected behaviour unless the merge changed the version in `pyproject.toml`. Check the **Auto-tag** run: if it says the tag already exists, no version bump landed. Run `s/version++` to actually cut a release.

**"The deployment approval expired and the run failed."**
The tag was still created, so the release just needs re-running. Run the **Publish library to pypi.org** workflow from the Actions tab, setting `ref` to the tag (for example `v2.1.0`), and approve it this time.

**"The publish failed with 'file already exists'."**
That version is already on PyPI - PyPI never allows re-uploading the same version, even if you delete it. Bump to a new patch version and release again.

**"I tagged the wrong commit / released too early."**
You cannot un-publish from PyPI. Fix forward: bump another patch version with the correction. If the tag was created but the publish had not yet been approved, reject the deployment and delete the tag before it goes out.

**"`s/version++` says my branch is not clean / not up to date."**
It only releases from a clean, current `main`. Commit or stash your work, `git pull`, and re-run.

**"`s/version++` says the changelog has no entry."**
Add the `## X.Y.Z` section to `docs/changelog.md` first (step 1), commit it, then re-run.

## Notes for maintainers

- Releases are tagged **`vX.Y.Z`**. Releases up to and including `2.0.1` were tagged bare (`2.0.1`), so both forms exist in the history; the "has this version already been released?" check accepts either, which is what stops the prefix change from re-releasing an old version.
- The `release` environment holds the PyPI trusted-publishing configuration and the approval requirement. Publishing uses OIDC trusted publishing, so there is no PyPI token stored in the repository.
- `s/version++` auto-detects branch protection: with `main` protected it opens a release pull request, and without protection it pushes directly. Force either with `--pr` or `--direct`.
