###########
# Linting #
###########
lint:  ## lint python with ruff and isort
	python -m ruff check csp_citibike --per-file-ignores "__init__.py:F403,__init__.py:F401"

fix:  ## autoformat python with ruff and isort
	python -m ruff format csp_citibike

format: fix

###########
# Helpers #
###########
# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: lint fix format help
