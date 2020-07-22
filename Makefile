install:
	poetry install

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests
	poetry run isort page_loader/*.py
	poetry run isort tests/*.py

test:
	poetry run pytest -vv --cov=page_loader --cov-report xml tests/

publish:
	poetry build
	poetry publish -r testpypi

.PHONY: install lint test publish