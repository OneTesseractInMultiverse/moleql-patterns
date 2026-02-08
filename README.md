# MoleQL Patterns

Reusable base classes and design patterns for clean, decoupled application architecture.

**moleql-patterns** is a lightweight Python library built on **Pydantic** and inspired by **FastAPI**.
It provides small, composable abstractions intended to standardize common application behaviors
without introducing framework lock-in.

This project is designed to be used as *infrastructure*: explicit, predictable, and easy to reason about.

---

## Documentation

- 📘 **Contributor Guide**: see [CONTRIBUTING.md](CONTRIBUTING.md)
- 🛠 **Development Guide**: see [DEVELOPMENT.md](DEVELOPMENT.md)
- 🔐 **Security Policy**: see [SECURITY.md](SECURITY.md)
- 🚀 **Release Process**: see [RELEASING.md](RELEASING.md)

---

## Make Commands

This repository includes a Makefile with common developer workflows:

```bash
make help
make test
make format
make build
make hooks
make upgrade
make bump-patch
make bump-minor
make bump-major
```

Use `make help` to see the full list of commands and descriptions.

---

## Project Principles

- Explicit over implicit
- Small, composable abstractions
- Pydantic models as primary contracts
- No hidden magic or runtime coupling
- Framework-agnostic by design

---

## Status

This project is in early development. APIs may evolve until a stable `1.0` release.

---

## Requirements

- Python **3.12+**

---

## Maintainers Only

The following applies to project maintainers.

### Responsibilities

- Review and merge pull requests
- Enforce architectural consistency
- Maintain API stability guarantees
- Manage releases and PyPI publishing
- Respond to security disclosures

### Expectations

- Changes affecting public APIs must be discussed before merging
- Breaking changes require clear documentation and versioning
- Releases must follow the documented release process
