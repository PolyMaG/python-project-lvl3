install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv --cov=page_loader --cov-report xml tests/

publish:
	poetry build
	poetry publish -r testpypi

.PHONY: install lint test publish