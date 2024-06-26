.PHONY: clean coverage docs help \
	quality requirements selfcheck test test-all upgrade validate

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## remove generated byte code, coverage reports, and build artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

erase: clean ## remove everthing, but the code.
	rm -fr venv/
	git clean -fx


build: ## build and install development environment requirements inside container
	docker compose up --build

test: clean ## run tests in the current virtualenv
	docker exec -it back bash -c "cd test_from_stori_card/ && python manage.py test"

migrate:
	docker exec -it back bash -c "cd test_from_stori_card/ && python manage.py migrate"

createsuperuser:
	docker exec -it back bash -c "cd test_from_stori_card/ && python manage.py createsuperuser"

run:
	docker compose up

quality:
	pylint --max-line-length=120 test_from_stori_card/transaction_management_api/api/
	pylint --max-line-length=120 test_from_stori_card/transaction_management_api/utils/

runCLI:
	./stori_card_cli/cli stori_card_cli/transactions_info.csv

qualityDocker:
	docker exec -it back bash -c "pylint --max-line-length=120 test_from_stori_card/transaction_management_api/api/"
	docker exec -it back bash -c "pylint --max-line-length=120 test_from_stori_card/transaction_management_api/utils/"

selfcheck: ## check that the Makefile is well-formed
	@echo "The Makefile is well-formed."
