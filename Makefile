.DEFAULT_GOAL := help
.PHONY: help install lint format test validate

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

install: ## Install dev dependencies
	uv sync --dev

lint: ## Check formatting and lint
	uv run ruff check .
	uv run ruff format --check .

format: ## Auto-fix lint and format
	uv run ruff check --fix .
	uv run ruff format .

test: ## Run the test suite
	uv run pytest

validate: ## Validate the plugin marketplace
	@if [ -f .claude-plugin/marketplace.json ]; then \
		claude plugin validate .; \
	else \
		echo "skip validate: .claude-plugin/marketplace.json not present yet"; \
	fi
