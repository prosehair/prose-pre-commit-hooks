
# Create and initialize a local virtual env for dev
init-dev: clean-all
	python3 -m venv venv
	venv/bin/pip install --disable-pip-version-check -U pip
	venv/bin/pip install pip-tools
	cat requirements.in requirements-test.in requirements-dev.in | sort | uniq > requirements-env-dev.in
	venv/bin/pip-compile --no-emit-index-url requirements-env-dev.in --output-file=requirements-env-dev.txt
	venv/bin/pip install -r requirements-env-dev.txt
	venv/bin/python setup.py develop
	venv/bin/pre-commit install
	venv/bin/pre-commit install -t pre-push

# Update pre-commit
pre-commit-autoupdate:
	venv/bin/pre-commit autoupdate

# Create and initialize a local virtual env for test only
init-ci:
	python3 -m venv venv
	venv/bin/pip install --disable-pip-version-check -U pip
	venv/bin/pip install pip-tools
	venv/bin/pip install -r requirements-test.txt

# Run pre-commit hooks
pre-commit:
	venv/bin/pre-commit run --all-files

# Perform code sanity checks
lint:
	venv/bin/flake8 prose_pre_commit_hooks

# Run test suite
test:
	LOG_LEVEL=INFO venv/bin/python -m pytest -vv --capture=no --cov=prose_pre_commit_hooks --cov-report=term-missing $$TEST_OPTIONS tests

# Run test suite with coverage
test-cov:
	venv/bin/python -m pytest --cov=prose_pre_commit_hooks --cov-report=html $$TEST_OPTIONS tests

# Purge temporary files
clean:
	find . -name __pycache__ | xargs rm -rf
	find . -name '*,cover' -delete
	find . -name '*.swp' -delete

# Fully purge environment
clean-all: clean
	rm -rf .cache
	rm -rf venv
