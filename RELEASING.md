# Releasing moleql-patterns

This document describes the release process for **moleql-patterns**.
It is intended for project maintainers.

---

## Versioning

This project follows **Semantic Versioning**:

- **MAJOR** – incompatible API changes
- **MINOR** – backwards-compatible functionality
- **PATCH** – backwards-compatible bug fixes

Until `1.0.0`, minor versions may still introduce breaking changes.

---

## Pre-release Checklist

Before cutting a release:

1. Ensure `main` is clean and green
   - CI passing
   - Coverage ≥ 90%
2. Ensure `uv.lock` is up to date
3. Review public API changes
4. Update documentation if needed
5. Decide on the next version number

---

## Update Version

Update the version in:

- `pyproject.toml`
- `src/moleql_patterns/__init__.py` (if version is exposed)

Commit with a message like:

```text
chore(release): bump version to X.Y.Z
```

---

## Build Artifacts

Build source and wheel distributions:

```bash
uv build
```

Artifacts will be generated in `dist/`.

---

## Publish to PyPI

This project is intended to use **Trusted Publishing** (recommended).

If using trusted publishing:
- Ensure the GitHub repository is configured in PyPI
- Push a tagged release from GitHub

If publishing manually (not recommended):

```bash
uv publish
```

---

## Git Tagging

Create an annotated tag:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

---

## Post-release

- Verify installation from PyPI
- Verify package metadata and long description rendering
- Announce changes (release notes / changelog if applicable)

---

## Long Description (PyPI)

The PyPI long description should align with the README:

> A lightweight Python library providing reusable base classes and design patterns
> for decoupled application architecture, built on Pydantic and inspired by FastAPI.

Avoid marketing language. Keep descriptions factual and architectural.
