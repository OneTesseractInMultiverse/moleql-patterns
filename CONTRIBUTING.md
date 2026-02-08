# Contributing

Thanks for your interest in contributing to **moleql-patterns**.

This project aims to provide clean, reusable, and framework-agnostic design patterns built on Pydantic. Contributions of all kinds—bug fixes, improvements, documentation, and new patterns—are welcome.

## Requirements

- Python **3.12+**
- **uv**
- git

## Quick Start

```bash
git clone <REPO_URL>
cd moleql-patterns
uv sync --all-groups
```

## Install Git Hooks (Required)

This repository uses **pre-commit** to enforce code quality and testing standards.

```bash
uv run pre-commit install --hook-type pre-commit
uv run pre-commit install --hook-type pre-push
```

### What is enforced locally

- Code formatting and linting via **ruff**
- MIT license headers on Python files
- `uv.lock` consistency
- Tests with **≥ 90% coverage** before pushing

## Basic Workflow

1. Create a feature branch
   ```bash
   git checkout -b feat/<short-description>
   ```

2. Make your changes

3. Run checks locally
   ```bash
   uv run pre-commit run --all-files
   uv run pytest
   ```

4. Push your branch
   ```bash
   git push
   ```

## Pull Requests

- Keep PRs focused and reasonably small
- Include tests for any behavioral change
- Avoid breaking public APIs without discussion
- Update documentation when relevant

## Security

Please report security issues responsibly. See **SECURITY.md** for details.
