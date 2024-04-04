help: ## Show help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test-api: ## Run API tests
	python -m pytest -v -o log_cli=true

test:
	pytest -vm sanity 

test-prod:
	pytest -vm prod 
