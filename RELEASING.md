# Releasing

This repository is currently distributed from GitHub and GitHub Pages. Before
publishing a package, confirm the checks below from a clean checkout:

1. Run `python scripts/verify_surface.py` and confirm the documented counts.
2. Run `pytest -q` and `mkdocs build --strict`.
3. Update `CHANGELOG.md`, `docs/changelog.md`, and the version in `pyproject.toml`.
4. Push the release commit and wait for both GitHub Actions workflows to pass.
5. Only publish to PyPI after choosing a license and configuring a trusted
   publishing environment. The current package metadata is deliberately not a
   PyPI release configuration.

The client remains unofficial and uses browser-facing PGA TOUR services. A
release must not be described as an official PGA TOUR API.
