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
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------

python_version=3.9.11
venv=djangodeeplink_env

# -----------------------------------------------------------------------------
# Environment setup
# -----------------------------------------------------------------------------

env:  ## create virtualenv
	pyenv virtualenv ${python_version} ${venv} && pyenv local ${venv}

reqs:  ## install development requirements
	python3 -m pip install -U pip \
			&& python3 -m pip install -r requirements.txt \
			&& python3 -m pip install -r requirements_dev.txt \
			&& python3 -m pip install -r requirements_test.txt

destroy_env:  ## destroy pyenv virtualenv
	pyenv uninstall ${venv}
	rm db.sqlite3

# -----------------------------------------------------------------------------
# Django
# -----------------------------------------------------------------------------

migrations:  ## create django migrations
	python3 manage.py makemigrations

migrate:  ## apply django migrations
	python3 manage.py migrate

createsuperuser:  ## create django superuser
	python3 manage.py createsuperuser

collectstatic:  ## django collect static
	python3 manage.py collectstatic

serve:  ## serve django development app
	python3 manage.py runserver 0.0.0.0:8080

scratch: env reqs migrate createsuperuser serve

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean: clean-build clean-pyc ## remove all build, test, coverage and Python3 artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python3 file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------

dist: clean ## builds source and wheel package
	python3 -m build --wheel

release_test: ## upload package to pypi test
	twine upload dist/* -r pypitest

release: dist ## package and upload a release
	twine upload dist/*
