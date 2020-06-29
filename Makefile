all: test

init-dev: ## Create and initialize a local virtual env for dev
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip install --disable-pip-version-check -U pip
	venv/bin/pip install pip-tools
	cat requirements.in requirements-test.in requirements-dev.in | sort | uniq > requirements-env-dev.in
	venv/bin/pip-compile --no-emit-index-url requirements-env-dev.in --output-file=requirements-env-dev.txt
	venv/bin/pip install -r requirements-env-dev.txt
	venv/bin/python setup.py develop
	venv/bin/pre-commit install && venv/bin/pre-commit install -t pre-push
	venv/bin/pre-commit autoupdate


init-ci: ## Create and initialize a local virtual env for test only
	python3 -m venv venv
	venv/bin/pip install --disable-pip-version-check -U pip
	venv/bin/pip install pip-tools
	venv/bin/pip install -r requirements-test.txt


freeze:
	cat requirements.in requirements-test.in | sort | uniq > requirements-test-full.in \
	&& venv/bin/pip-compile  --no-emit-index-url requirements-test-full.in --output-file=requirements-test.txt
	venv/bin/pip-compile  --no-emit-index-url requirements.in --output-file=requirements.txt


pre-commit: ## Run pre-commit hooks
	venv/bin/pre-commit run --all-files

package-upload:  ## Upload to private prose pypi server
	rm -r dist
	python setup.py sdist
	# venv/bin/twine upload --verbose --repository-url $$PIP_PROSE_PYPI -u $$PROSE_PYPI_USERNAME -p $$PROSE_PYPI_PASSWORD dist/*

lint:  ## Perform code sanity checks if needed
	venv/bin/flake8 prose_etl_utils


lint-fix:  ## Try to automatically fix lint error
	find prose_pre_commit_hooks -name '*.py' | xargs venv/bin/isort -q -y
	find tests -name '*.py' | xargs venv/bin/isort -q -y
	venv/bin/pre-commit run --all-files


test: ## Run the test suite
	LOG_LEVEL=INFO venv/bin/python -m pytest -vv --capture=no  --cov-fail-under 80 --cov=prose_pre_commit_hooks --cov-report=term-missing $$TEST_OPTIONS tests


test-cov: ## Annotate source code with coverage information
	venv/bin/python -m pytest --cov=prose_pre_commit_hooks --cov-fail-under 80 --cov-report=html $$TEST_OPTIONS tests


clean: ## Purge temporary files
	find . -name __pycache__ | xargs rm -rf
	find . -name '*,cover' -delete
	find . -name '*.swp' -delete


clean-all: clean ## Fully purge environment
	rm -rf .cache
	rm -rf venv


help:  ## Show this help.
	@grep -E "^[^._][a-zA-Z_-]*:" Makefile | awk -F '[:#]' '{print $$1, ":", $$NF}' | sort | column -t -s:


.SILENT: all help lint lint-fix package-upload test test-cov
.PHONY: all help lint lint-fix package-upload test test-cov
