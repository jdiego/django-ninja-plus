.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Removing cached python compiled files
	find . -name \*pyc -type f | xargs rm -fv
	find . -name \*pyo | xargs rm -fv
	find . -name \*~  | xargs rm -fv
	find . -name __pycache__  | xargs  rm -rfv
	find . -name .ruff_cache  | xargs  rm -rfv
	find . -name .mypy_cache  | xargs  rm -rfv

install:clean ## Install dependencies
	uv sync --group dev

install-full:install ## Install dependencies
	uv run pre-commit install -f

lint:fmt ## Run code linters
	uv run ruff check ninja_plus tests
	uv run mypy ninja_plus

fmt format:clean ## Run code formatters
	uv run ruff format ninja_plus tests
	uv run ruff check --fix ninja_plus tests


test:clean ## Run tests
	uv run pytest .

test-cov:clean ## Run tests with coverage
	uv run pytest --cov=ninja_plus --cov-report term-missing tests

doc-deploy:clean ## Run Deploy Documentation
	uv run mkdocs gh-deploy --force

doc-serve: ## Launch doc local server
	uv run mkdocs serve
