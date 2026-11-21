---
name: release
description: Cut a new demo-ledger-service release (version bump and vX.Y.Z Git tag). Use when asked to release, bump the version, or tag the library for consumers.
---

# Release demo-ledger-service

The library is not published to a registry. Consumers
(`eventflow-order-service`, `eventflow-payment-service`) pin a Git tag via a
Poetry/pip git dependency, so a release is a version bump plus a tag.

1. Choose the next version `X.Y.Z` (semver; a change to settlement, fee,
   position or P&L behaviour is not a patch).
2. Bump the version in both places, to the same value:
   - `version` in `pyproject.toml`
   - `__version__` in `ledger/__init__.py`
3. Update the `v0.4.0`-style tag examples in `README.md` ("Installing as a
   dependency") to the new tag.
4. If test dependencies changed, keep them pinned in `requirements.txt`.
5. Run `pytest -q`; `tests/test_package.py` fails if the two versions differ.
6. Open a PR with the bump and get it merged to `main`.
7. After merge, tag the merge commit on `main` and push the tag:

   ```bash
   git checkout main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

8. Tell consumers the new tag so they can update their pin.
