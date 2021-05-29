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

interpreter_found := $(shell [ -n "$$VIRTUAL_ENV" ] && echo "yes")



check-venv:
	$(if $(interpreter_found),, $(error No virtual environment found, either run "make venv" or "poetry shell"))

githooks: ## Install git hooks
	@pre-commit install -t=pre-commit -t=pre-push

run_demo_app: ## Build local version and run demo_app
	@poetry build

	@cd demo_app
	@poetry run pip install ../dist/django_explorer-*.*.*-py3-none-any.whl --force-reinstall
	@poetry run ./manage.py runserver $(port)


###############
# Code checks #
###############

check: check-venv ## Run linters
	@printf "$(CYAN)flake8$(COFF)\n"
	@echo "======"
	@flake8 || exit 1
	@echo "OK"
	@echo;
	@printf "$(CYAN)black$(COFF)\n"
	@echo "======"
	@black --check . || exit 1
	@echo;
	@printf "$(CYAN)isort$(COFF)\n"
	@echo "======"
	@isort --check-only .

test: check-venv ## Test code with pytest
	@printf "$(CYAN)pytest$(COFF)\n"
	@echo "========="
	@pytest .

fix: check-venv ## Run code formatters
	@printf "$(CYAN)autoflake$(COFF)\n"
	@echo "========="
	@autoflake -ri --remove-all-unused-imports --exclude __init__.py,conftest.py .
	@printf "$(CYAN)black$(COFF)\n"
	@echo "====="
	@black .
	@echo;
	@printf "$(CYAN)isort$(COFF)\n"
	@echo "====="
	@isort .