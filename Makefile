.PHONY: help install install-dev clean lint format type-check test test-cov test-watch run run-dev run-api run-celery run-redis build docker-build docker-run docker-stop migrate migrate-upgrade migrate-downgrade setup pre-commit-install pre-commit-run

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	uv sync

install-dev: ## Install development dependencies
	uv sync --dev

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Code quality
lint: ## Run linting checks
	uv run flake8 lessonly tests
	uv run black --check lessonly tests
	uv run isort --check-only lessonly tests

format: ## Format code with black and isort
	uv run black lessonly tests
	uv run isort lessonly tests

type-check: ## Run type checking with mypy
	uv run mypy lessonly

# Testing
test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=lessonly --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	uv run pytest-watch

# Running the application
run: ## Run the Streamlit app
	uv run streamlit run src/ui/main.py


# Docker
docker-build: ## Build Docker image
	docker build -t lessonly .

docker-run: ## Run Docker container
	docker run -p 8501:8501 -p 8000:8000 lessonly

docker-stop: ## Stop Docker containers
	docker stop $$(docker ps -q --filter ancestor=lessonly)

# Development utilities
jupyter: ## Start Jupyter notebook
	uv run jupyter notebook

# Environment
env-example: ## Create example environment file
	cp .env.example .env

# Documentation
docs: ## Generate documentation
	uv run pdoc --html --output-dir docs lessonly

# Security
security-check: ## Run security checks
	uv run bandit -r lessonly
	uv run safety check

# Performance
profile: ## Run performance profiling
	uv run python -m cProfile -o profile.stats src/app/main.py
