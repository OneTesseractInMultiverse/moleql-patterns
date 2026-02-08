# Development Guide

This document provides deeper guidance for contributors working on the internals of **moleql-patterns**.

## Tooling Overview

This project uses:

- **uv** for dependency and environment management
- **ruff** for linting and formatting
- **pytest**, **pytest-cov**, and **coverage** for testing
- **pre-commit** for local quality gates
- **GitHub Actions** for CI

All tools are configured via `pyproject.toml`.

## Environment Setup

After cloning the repository:

```bash
uv sync --all-groups
```

You can run all commands via `uv run` without activating a virtual environment.

Optional activation:

```bash
source .venv/bin/activate
```

## Common Commands

### Lint

```bash
uv run ruff check .
```

### Format

```bash
uv run ruff format .
```

### Tests and Coverage

```bash
uv run pytest
```

- Coverage is enforced at **90% minimum**
- XML report is generated at `coverage.xml`

## Pre-commit Hooks

### Pre-commit stage

Runs on every commit:

- Ruff lint (with autofix)
- Ruff formatting
- License header validation
- `uv lock --check`
- Whitespace / YAML / file-size hygiene

### Pre-push stage

Runs before every push:

- Full test suite
- Coverage gate (≥ 90%)

You can run them manually:

```bash
uv run pre-commit run --all-files
uv run pre-commit run --hook-stage pre-push
```

## Dependency Changes

If you modify dependencies in `pyproject.toml`:

```bash
uv lock
```

Commits with a stale or missing `uv.lock` will be rejected.

## License Headers

All Python files under `src/` must include the MIT license header.

The check is enforced via a local pre-commit hook. Missing headers will block commits.

## Project Structure

```text
src/moleql_patterns/
tests/
tools/
docs/
```

- `moleql_patterns/` – public and internal abstractions
- `tests/` – unit tests (coverage enforced)
- `tools/` – repo tooling (license checks, scripts)
- `docs/` – documentation assets

## Design Philosophy

- Prefer **explicitness over magic**
- Keep abstractions **small and composable**
- Avoid framework lock-in
- Use **Pydantic models** as the primary contract
- Treat this library as infrastructure, not an application

## CI

CI runs on pull requests and main branch pushes:

- Ruff lint + format check
- Pytest with coverage enforcement
- Coverage XML uploaded as an artifact

CI mirrors local hooks—if it fails locally, it will fail in CI.

## Questions / Discussions

For questions, open a GitHub issue or discussion with context and examples.
