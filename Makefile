# -----------------------------------------------------------------------------
# Generate help output when running just `make`
# -----------------------------------------------------------------------------
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------

python_version=3.9.11
venv=django-deep-link_env

# START - Generic commands
# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

env:  ## Create virtual environment
	pyenv virtualenv ${python_version} ${venv} && pyenv local ${venv}

env_remove:  ## Remove virtual environment
	pyenv uninstall -f ${venv}

sqllite_remove:	## Remove sqlite database
	rm -f db.sqlite3

from_scratch: sqllite_remove env_remove env pip_install migrations migrate superuser serve ## Remove and create virtual environment

# -----------------------------------------------------------------------------
# Pip
# -----------------------------------------------------------------------------

pip_install:  ## Install requirements
	python3 -m pip install --upgrade pip
	@for file in $$(ls requirements/*.txt); do \
			python3 -m pip install -r $$file; \
	done
	pre-commit install

pip_list:  ## Run pip list
	python3 -m pip list

pip_freeze:  ## Run pipfreezer
	pipfreezer

pip_checker:  ## Run pipchecker
	python3 manage.py pipchecker

# -----------------------------------------------------------------------------
# Django
# -----------------------------------------------------------------------------

manage:	## Run django manage.py (eg - make manage cmd="shell")
	python3 manage.py ${cmd}

superuser:  ## Create superuser
	python3 manage.py createsuperuser

migrations:  ## Create migrations (eg - make migrations app="core")
	python3 manage.py makemigrations ${app}

migrate:  ## Apply migrations
	python3 manage.py migrate

serve:  ## Run server
	python3 manage.py runserver 127.0.0.1:8000

show_urls:  ## Show urls
	python3 manage.py show_urls

shell:  ## Run shell
	python3 manage.py shell_plus

flush:  ## Flush database
	python3 manage.py flush

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

pytest:  ## Run tests
	pytest -vx

pytest_verbose:  ## Run tests in verbose mode
	pytest -vs

coverage:  ## Run tests with coverage
	coverage run -m pytest && coverage html
	# pytest --cov=django_project --cov=src --cov-report html -vs

coverage_verbose:  ## Run tests with coverage in verbose mode
	coverage run -m pytest -vs && coverage html

coverage_skip:  ## Run tests with coverage and skip covered
	coverage run -m pytest -vs && coverage html --skip-covered

open_coverage:  ## Open coverage report
	open htmlcov/index.html

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean_build: ## Remove build artifacts
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean_pyc: ## Remove python file artifacts
	find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' \) -exec rm -fr {} +

clean: clean_build clean_pyc ## Remove all build and python artifacts

clean_pytest_cache:  ## Clear pytest cache
	rm -rf .pytest_cache

clean_ruff_cache:  ## Clear ruff cache
	rm -rf .ruff_cache

clean_tox_cache:  ## Clear tox cache
	rm -rf .tox

clean_coverage:  ## Clear coverage cache
	rm .coverage
	rm -rf htmlcov

clean_tests: clean_pytest_cache clean_ruff_cache clean_tox_cache clean_coverage  ## Clear pytest, ruff, tox, and coverage caches

# -----------------------------------------------------------------------------
# Miscellaneous
# -----------------------------------------------------------------------------

tree:  ## Show directory tree
	tree -I 'build|dist|htmlcov|node_modules|migrations|contrib|__pycache__|*.egg-info|staticfiles|media|django_project'

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------

dist: clean ## Builds source and wheel package
	python3 -m build

release_test: dist ## Upload package to pypi test
	twine upload dist/* -r pypitest

release: dist ## Package and upload a release
	twine upload dist/*

check: dist ## Twine check
	twine check dist/*

# END - Generic commands
# -----------------------------------------------------------------------------
# Project Specific
# -----------------------------------------------------------------------------

# Add project specific targets here
