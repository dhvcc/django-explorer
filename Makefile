##########
# Config #
##########

CYAN ?= \033[0;36m
COFF ?= \033[0m
port ?= 8000

.PHONY: githooks \
		init_demo_app run_demo_app \
		check fix

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	{printf "$(CYAN)%-30s$(COFF) %s\n", $$1, $$2}\n'

###########
# Project #
###########

interpreter := $(shell poetry env info > /dev/null 2>&1 && echo "poetry run")
project_version = $(shell poetry version | cut -d' ' -f2)

check-venv:
	$(if $(interpreter),, $(error No virtual environment found, run "make venv"))

githooks: ## Install git hooks
	@$(interpreter) pre-commit install -t=pre-commit -t=pre-push

run_demo_app: ## Build local version and run demo_app
	@poetry build

	@cd demo_app
	@$(interpreter) pip install ../dist/django_explorer-$(project_version)-py3-none-any.whl --force-reinstall
	@$(interpreter) ./manage.py migrate --noinput
	@$(interpreter) ./manage.py runserver $(port)

run_demo_shell: ## Run django-extension's shell_plus for demo_app
	@$(interpreter) pip install ./manage.py shell_plus --ipython -- -i -c """from rich import pretty, inspect
	pretty.install()
	"""

###############
# Code checks #
###############

check: check-venv ## Run linters
	@printf "$(CYAN)flake8$(COFF)\n"
	@echo "======"
	@$(interpreter) flake8 || exit 1
	@echo "OK"
	@echo;
	@printf "$(CYAN)black$(COFF)\n"
	@echo "======"
	@$(interpreter) black --check . || exit 1
	@echo;
	@printf "$(CYAN)isort$(COFF)\n"
	@echo "======"
	@$(interpreter) isort --check-only .

test: check-venv ## Test code with pytest
	@printf "$(CYAN)pytest$(COFF)\n"
	@echo "========="
	@$(interpreter) pytest .

fix: check-venv ## Run code formatters
	@printf "$(CYAN)autoflake$(COFF)\n"
	@echo "========="
	@$(interpreter) autoflake -ri --remove-all-unused-imports --exclude __init__.py,conftest.py .
	@echo ;
	@printf "$(CYAN)black$(COFF)\n"
	@echo "====="
	@$(interpreter) black .
	@echo;
	@printf "$(CYAN)isort$(COFF)\n"
	@echo "====="
	@$(interpreter) isort .
