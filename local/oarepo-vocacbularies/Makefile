.PHONY: help test typecheck clean clean-test clean-pyc clean-build

.DEFAULT_GOAL := help

PACKAGE_NAME = oarepo_vocacbularies

VIRTUALENV ?= python -m venv
VIRTUAL_ENV ?= $(PWD)/.venv
PYTHON ?= $(VIRTUAL_ENV)/bin/python
PIP ?= $(VIRTUAL_ENV)/bin/pip
BROWSER ?= firefox


help:
	@python make_help.py

$(PYTHON):
	$(VIRTUALENV) $(VIRTUAL_ENV)
	$(PIP) install "setuptools >= 30.3.0"

develop: $(PYTHON)
	@## install the package in develop mode
	$(PIP) install -e ".[testing]"
	$(PIP) install -e ".[develop]"
	$(PIP) install -e .

test:
	@## run tests quickly with the default Python
	$(PYTHON) -m pytest

typecheck:
	@## check types with mypy
	$(PYTHON) -m mypy $(PACKAGE_NAME)

lint:
	@## check style with flake8
	$(PYTHON) -m flake8 $(PACKAGE_NAME) tests

coverage:
	@## show coverage in the console
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m

coverage-html:
	@## show coverage in the browser
	@## uses $BROWSER if present
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage html
	$(BROWSER) htmlcov/index.html

watch: COMMAND = $(MAKE) $(filter-out watch, $(MAKECMDGOALS))
watch:
	@## Run make on source changes
	@## Exemple: 'make watch test' will run make test on source changes
	@ $(COMMAND) || exit 0
	@ $(PYTHON) -m watchdog.watchmedo \
	     shell-command --patterns='*.py' \
	                   --recursive \
	                   --wait \
	                   --command='$(COMMAND)'

dist: clean
	@## build source and wheel package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

clean: clean-build clean-pyc clean-test
	@## remove all build, test, coverage and Python artifacts

clean-build:
	@## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	@## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	@## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .mypy_cache
rm -fr .pytest_cache
