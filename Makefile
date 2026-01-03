.PHONY: help install dev run test lint format clean sync lock update

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev    	 - Install dev dependencies"
	@echo "  make run        - Run the application"
	@echo "  make format     - Format code"
	@echo "  make sync       - Sync dependencies with lock file"
	@echo "  make lock       - Update lock file"
	@echo "  make update     - Update dependencies"

install:
	@uv pip install .

dev:
	@uv pip install .[dev]

run: install
	@uv run octosuite

format:
	@uv run black .

sync:
	@uv sync

lock:
	@uv lock

update:
	@uv lock --upgrade
	@uv sync