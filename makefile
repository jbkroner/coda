.PHONY: install install-dev lint format test pre-commit

install:
	pip install .

install-dev:
	pip install .[dev]

lint:
	ruff check .

format:
	black .
	ruff check --fix .

test:
	pytest

pre-commit:
	pre-commit run --all-files

docker-build:
	docker build -t coda:dev_latest .

setup: install-dev
	pre-commit install

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
