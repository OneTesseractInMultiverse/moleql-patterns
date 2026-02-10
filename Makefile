.DEFAULT_GOAL := help

.PHONY: help test format build hooks upgrade bump bump-patch bump-minor bump-major tag tag-push release

## Show available commands and their descriptions
help:
	@printf "Usage: make <target>\n\n"
	@printf "Targets:\n"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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
	uv run python tools/version.py bump $(BUMP)
	$(MAKE) hooks
	$(MAKE) test

bump-patch: ## Bump patch version (x.y.Z -> x.y.(Z+1))
	BUMP=patch $(MAKE) bump

bump-minor: ## Bump minor version (x.Y.z -> x.(Y+1).0)
	BUMP=minor $(MAKE) bump

bump-major: ## Bump major version (X.y.z -> (X+1).0.0)
	BUMP=major $(MAKE) bump

tag: ## Create an annotated git tag from pyproject.toml (vX.Y.Z)
	@version=$$(uv run python tools/version.py get) && echo "Tagging v$$version" && git tag -a "v$$version" -m "Release v$$version"

tag-push: ## Push the current tag to origin
	git push origin --tags

release: ## Interactive version bump (patch, minor, major)
	uv run python tools/release.py
