SRC_DIR=profbit

clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

installdeps:
	pip install pipenv
	pipenv install --dev

lint:
	flake8 $(SRC_DIR) && isort --check-only --recursive $(SRC_DIR)

test: lint
	py.test --cov=$(SRC_DIR)
