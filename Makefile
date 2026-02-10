.DEFAULT_GOAL := help

.PHONY: help test format build hooks upgrade bump bump-patch bump-minor bump-major tag tag-push

## Show available commands and their descriptions
help:
	@printf "Usage: make <target>\n\n"
	@printf "Targets:\n"
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z0-9_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## Run unit tests verbosely with coverage report
	uv run pytest -vv --cov-report=term-missing

format: ## Format all code files with Ruff
	uv run ruff format .

build: ## Build the package (sdist + wheel)
	uv build

hooks: ## Run all pre-commit hooks
	uv run pre-commit run --all-files

upgrade: ## Upgrade deps and bump patch version (then run hooks + tests)
	uv lock --upgrade
	$(MAKE) bump-patch

bump: ## Bump version based on BUMP=major|minor|patch (then run hooks + tests)
	uv run python -c 'import os,re; from pathlib import Path; pyproject=Path("pyproject.toml"); text=pyproject.read_text(); m=re.search(r"^version\\s*=\\s*\\\"([^\\\"]+)\\\"", text, re.M); \
	if not m: raise SystemExit("version not found in pyproject.toml"); current=m.group(1); parts=current.split("."); \
	if len(parts) != 3 or not all(p.isdigit() for p in parts): raise SystemExit("version must be major.minor.patch"); \
	major, minor, patch = (int(p) for p in parts); bump=os.environ.get("BUMP"); \
	if bump == "major": major += 1; minor = 0; patch = 0; \
	elif bump == "minor": minor += 1; patch = 0; \
	elif bump == "patch": patch += 1; \
	else: raise SystemExit("BUMP must be major, minor, or patch"); \
	new=f"{major}.{minor}.{patch}"; \
	text, py_count = re.subn(r"^version\\s*=\\s*\\\"[^\\\"]+\\\"", f"version = \\\"{new}\\\"", text, count=1, flags=re.M); \
	if py_count != 1: raise SystemExit("version not updated in pyproject.toml"); \
	pyproject.write_text(text); \
	init=Path("src/moleql_patterns/__init__.py"); init_text=init.read_text(); \
	init_text, init_count = re.subn(r"^__version__\\s*=\\s*\\\"[^\\\"]+\\\"", f"__version__ = \\\"{new}\\\"", init_text, count=1, flags=re.M); \
	if init_count != 1: raise SystemExit("version not updated in __init__.py"); \
	init.write_text(init_text); \
	print(f"Bumped version: {current} -> {new}")'
	$(MAKE) hooks
	$(MAKE) test

bump-patch: ## Bump patch version (x.y.Z -> x.y.(Z+1))
	BUMP=patch $(MAKE) bump

bump-minor: ## Bump minor version (x.Y.z -> x.(Y+1).0)
	BUMP=minor $(MAKE) bump

bump-major: ## Bump major version (X.y.z -> (X+1).0.0)
	BUMP=major $(MAKE) bump

tag: ## Create an annotated git tag from pyproject.toml (vX.Y.Z)
	@version=$$(uv run python -c 'import re; from pathlib import Path; text=Path("pyproject.toml").read_text(); m=re.search(r"^version\\s*=\\s*\\\"([^\\\"]+)\\\"", text, re.M); \
	if not m: raise SystemExit("version not found in pyproject.toml"); print(m.group(1));'); \
	echo "Tagging v$$version"; \
	git tag -a "v$$version" -m "Release v$$version"

tag-push: ## Push the current tag to origin
	git push origin --tags
