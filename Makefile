.PHONY: test format build hooks

test:
	uv run pytest

format:
	uv run ruff format .

build:
	uv build

hooks:
	uv run pre-commit run --all-files
